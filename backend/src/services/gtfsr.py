from __future__ import annotations

import asyncio
import os
import time

import httpx
from google.transit import gtfs_realtime_pb2

_BASE = "https://api.opendata.transport.vic.gov.au/opendata/public-transport/gtfs/realtime/v1"

# Metro Train + Yarra Trams use Ocp-Apim-Subscription-Key
# Metro Bus + V/Line use KeyId
_OCP_KEY   = os.getenv("GTFSR_OCP_KEY", "")    # train + tram
_KEYID_KEY = os.getenv("GTFSR_KEYID", "")      # bus + vline

_FEEDS = [
    {"mode": "train",  "path": "/metro/vehicle-positions",  "header": "Ocp-Apim-Subscription-Key", "key": lambda: _OCP_KEY},
    {"mode": "tram",   "path": "/tram/vehicle-positions",   "header": "Ocp-Apim-Subscription-Key", "key": lambda: _OCP_KEY},
    {"mode": "bus",    "path": "/bus/vehicle-positions",    "header": "KeyId",                      "key": lambda: _KEYID_KEY},
    {"mode": "vline",  "path": "/vline/vehicle-positions",  "header": "KeyId",                      "key": lambda: _KEYID_KEY},
]

_TRIP_UPDATE_FEEDS = {
    "train": {"path": "/metro/trip-updates",  "header": "Ocp-Apim-Subscription-Key", "key": lambda: _OCP_KEY},
    "tram":  {"path": "/tram/trip-updates",   "header": "Ocp-Apim-Subscription-Key", "key": lambda: _OCP_KEY},
    "bus":   {"path": "/bus/trip-updates",    "header": "KeyId",                      "key": lambda: _KEYID_KEY},
    "vline": {"path": "/vline/trip-updates",  "header": "KeyId",                      "key": lambda: _KEYID_KEY},
}

_vehicles_cache: dict = {"data": None, "ts": 0.0}
CACHE_TTL = 30  # seconds — feed caching time per spec


def _parse_feed(raw: bytes) -> gtfs_realtime_pb2.FeedMessage:
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(raw)
    return feed


async def _fetch_one_feed(client: httpx.AsyncClient, feed_cfg: dict) -> list[dict]:
    key = feed_cfg["key"]()
    if not key:
        return []
    try:
        r = await client.get(
            _BASE + feed_cfg["path"],
            headers={feed_cfg["header"]: key},
            timeout=10,
        )
        r.raise_for_status()
        feed = _parse_feed(r.content)
    except Exception:
        return []

    vehicles = []
    for entity in feed.entity:
        if not entity.HasField("vehicle"):
            continue
        vp = entity.vehicle
        pos = vp.position
        trip = vp.trip
        if not (pos.latitude and pos.longitude):
            continue
        vehicles.append(
            {
                "id": entity.id,
                "mode": feed_cfg["mode"],
                "trip_id": trip.trip_id or None,
                "route_id": trip.route_id or None,
                "direction_id": trip.direction_id,
                "lat": pos.latitude,
                "lon": pos.longitude,
                "bearing": pos.bearing,
                "speed": pos.speed if pos.speed else None,
                "timestamp": vp.timestamp or None,
            }
        )
    return vehicles


async def fetch_vehicle_positions() -> list[dict]:
    """Fetch and cache live vehicle positions across all modes (train, tram, bus, V/Line)."""
    now = time.time()
    if _vehicles_cache["data"] is not None and now - _vehicles_cache["ts"] < CACHE_TTL:
        return _vehicles_cache["data"]

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *[_fetch_one_feed(client, f) for f in _FEEDS],
            return_exceptions=True,
        )

    vehicles: list[dict] = []
    for r in results:
        if isinstance(r, list):
            vehicles.extend(r)

    _vehicles_cache["data"] = vehicles
    _vehicles_cache["ts"] = now
    return vehicles


async def fetch_trip_updates(trip_id: str, mode: str = "train") -> list[dict]:
    """Return stop_time_updates for a specific trip from the appropriate mode feed."""
    feed_cfg = _TRIP_UPDATE_FEEDS.get(mode, _TRIP_UPDATE_FEEDS["train"])
    key = feed_cfg["key"]()
    if not key:
        return []

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(
            _BASE + feed_cfg["path"],
            headers={feed_cfg["header"]: key},
        )
        r.raise_for_status()
        feed = _parse_feed(r.content)

    for entity in feed.entity:
        if not entity.HasField("trip_update"):
            continue
        tu = entity.trip_update
        if tu.trip.trip_id == trip_id:
            updates = []
            for stu in tu.stop_time_update:
                updates.append(
                    {
                        "stop_id": stu.stop_id,
                        "stop_sequence": stu.stop_sequence,
                        "arrival_delay": stu.arrival.delay if stu.HasField("arrival") else None,
                        "arrival_time": stu.arrival.time if stu.HasField("arrival") else None,
                        "departure_delay": stu.departure.delay if stu.HasField("departure") else None,
                        "departure_time": stu.departure.time if stu.HasField("departure") else None,
                    }
                )
            return updates
    return []
