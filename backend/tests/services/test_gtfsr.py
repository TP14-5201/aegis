from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.services import gtfsr


class FakeResponse:
    def __init__(self, content=b"feed", raise_error=False):
        self.content = content
        self._raise_error = raise_error

    def raise_for_status(self):
        if self._raise_error:
            raise RuntimeError("HTTP error")


class FakeAsyncClient:
    def __init__(self, response=None):
        self.response = response or FakeResponse()
        self.get = AsyncMock(return_value=self.response)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FakeEntity:
    def __init__(self, entity_id="E1", vehicle=None, trip_update=None):
        self.id = entity_id
        self.vehicle = vehicle
        self.trip_update = trip_update

    def HasField(self, name):
        return getattr(self, name) is not None


class FakeStopTimeUpdate:
    def __init__(self, stop_id="S1", stop_sequence=1, arrival=None, departure=None):
        self.stop_id = stop_id
        self.stop_sequence = stop_sequence
        self.arrival = arrival or SimpleNamespace(delay=0, time=0)
        self.departure = departure or SimpleNamespace(delay=0, time=0)
        self._has_arrival = arrival is not None
        self._has_departure = departure is not None

    def HasField(self, name):
        return {"arrival": self._has_arrival, "departure": self._has_departure}[name]


def test_parse_feed_delegates_to_feed_message_parser():
    fake_feed = MagicMock()

    with patch("src.services.gtfsr.gtfs_realtime_pb2.FeedMessage", return_value=fake_feed):
        result = gtfsr._parse_feed(b"raw")

    fake_feed.ParseFromString.assert_called_once_with(b"raw")
    assert result is fake_feed


@pytest.mark.asyncio
async def test_fetch_one_feed_returns_empty_when_key_missing():
    client = FakeAsyncClient()
    cfg = {"key": lambda: "", "path": "/feed", "header": "Key", "mode": "bus"}

    assert await gtfsr._fetch_one_feed(client, cfg) == []
    client.get.assert_not_called()


@pytest.mark.asyncio
async def test_fetch_one_feed_returns_empty_on_http_or_parse_error():
    client = FakeAsyncClient(FakeResponse(raise_error=True))
    cfg = {"key": lambda: "key", "path": "/feed", "header": "Key", "mode": "bus"}

    assert await gtfsr._fetch_one_feed(client, cfg) == []


@pytest.mark.asyncio
async def test_fetch_one_feed_skips_non_vehicle_and_missing_position_rows():
    good_vehicle = SimpleNamespace(
        position=SimpleNamespace(latitude=-37.8, longitude=144.9, bearing=12.0, speed=0.0),
        trip=SimpleNamespace(trip_id="", route_id="R1", direction_id=1),
        timestamp=123,
    )
    missing_position = SimpleNamespace(
        position=SimpleNamespace(latitude=0.0, longitude=144.9, bearing=0.0, speed=10.0),
        trip=SimpleNamespace(trip_id="T2", route_id="R2", direction_id=0),
        timestamp=0,
    )
    feed = SimpleNamespace(
        entity=[
            FakeEntity("no-vehicle"),
            FakeEntity("missing-position", vehicle=missing_position),
            FakeEntity("good", vehicle=good_vehicle),
        ]
    )
    client = FakeAsyncClient()
    cfg = {"key": lambda: "key", "path": "/feed", "header": "Key", "mode": "tram"}

    with patch("src.services.gtfsr._parse_feed", return_value=feed):
        result = await gtfsr._fetch_one_feed(client, cfg)

    client.get.assert_awaited_once_with(
        gtfsr._BASE + "/feed",
        headers={"Key": "key"},
        timeout=10,
    )
    assert result == [
        {
            "id": "good",
            "mode": "tram",
            "trip_id": None,
            "route_id": "R1",
            "direction_id": 1,
            "lat": -37.8,
            "lon": 144.9,
            "bearing": 12.0,
            "speed": None,
            "timestamp": 123,
        }
    ]


@pytest.mark.asyncio
async def test_fetch_vehicle_positions_uses_cache_when_fresh(monkeypatch):
    monkeypatch.setitem(gtfsr._vehicles_cache, "data", [{"id": "cached"}])
    monkeypatch.setitem(gtfsr._vehicles_cache, "ts", 100.0)

    with patch("src.services.gtfsr.time.time", return_value=110.0):
        result = await gtfsr.fetch_vehicle_positions()

    assert result == [{"id": "cached"}]


@pytest.mark.asyncio
async def test_fetch_vehicle_positions_fetches_all_feeds_and_caches_lists(monkeypatch):
    monkeypatch.setitem(gtfsr._vehicles_cache, "data", None)
    monkeypatch.setitem(gtfsr._vehicles_cache, "ts", 0.0)

    async def fake_fetch(client, cfg):
        if cfg["mode"] == "bus":
            raise RuntimeError("ignored by gather")
        return [{"mode": cfg["mode"]}]

    with patch("src.services.gtfsr.httpx.AsyncClient", return_value=FakeAsyncClient()), \
         patch("src.services.gtfsr._fetch_one_feed", side_effect=fake_fetch), \
         patch("src.services.gtfsr.time.time", return_value=200.0):
        result = await gtfsr.fetch_vehicle_positions()

    assert result == [{"mode": "train"}, {"mode": "tram"}, {"mode": "vline"}]
    assert gtfsr._vehicles_cache["data"] == result
    assert gtfsr._vehicles_cache["ts"] == 200.0


@pytest.mark.asyncio
async def test_fetch_trip_updates_returns_empty_when_key_missing(monkeypatch):
    monkeypatch.setattr(gtfsr, "_OCP_KEY", "")

    assert await gtfsr.fetch_trip_updates("T1", mode="train") == []


@pytest.mark.asyncio
async def test_fetch_trip_updates_defaults_unknown_mode_to_train_and_serialises_updates(monkeypatch):
    monkeypatch.setattr(gtfsr, "_OCP_KEY", "key")
    stop_updates = [
        FakeStopTimeUpdate(
            stop_id="S1",
            stop_sequence=1,
            arrival=SimpleNamespace(delay=60, time=1000),
            departure=None,
        ),
        FakeStopTimeUpdate(
            stop_id="S2",
            stop_sequence=2,
            arrival=None,
            departure=SimpleNamespace(delay=30, time=2000),
        ),
    ]
    matching = FakeEntity(
        "match",
        trip_update=SimpleNamespace(
            trip=SimpleNamespace(trip_id="T1"),
            stop_time_update=stop_updates,
        ),
    )
    feed = SimpleNamespace(
        entity=[
            FakeEntity("vehicle-row", vehicle=SimpleNamespace()),
            FakeEntity("wrong-trip", trip_update=SimpleNamespace(trip=SimpleNamespace(trip_id="T2"), stop_time_update=[])),
            matching,
        ]
    )
    client = FakeAsyncClient()

    with patch("src.services.gtfsr.httpx.AsyncClient", return_value=client), \
         patch("src.services.gtfsr._parse_feed", return_value=feed):
        result = await gtfsr.fetch_trip_updates("T1", mode="unknown")

    client.get.assert_awaited_once_with(
        gtfsr._BASE + "/metro/trip-updates",
        headers={"Ocp-Apim-Subscription-Key": "key"},
    )
    assert result == [
        {
            "stop_id": "S1",
            "stop_sequence": 1,
            "arrival_delay": 60,
            "arrival_time": 1000,
            "departure_delay": None,
            "departure_time": None,
        },
        {
            "stop_id": "S2",
            "stop_sequence": 2,
            "arrival_delay": None,
            "arrival_time": None,
            "departure_delay": 30,
            "departure_time": 2000,
        },
    ]


@pytest.mark.asyncio
async def test_fetch_trip_updates_returns_empty_when_trip_not_found(monkeypatch):
    monkeypatch.setattr(gtfsr, "_KEYID_KEY", "key")
    feed = SimpleNamespace(entity=[FakeEntity("other", trip_update=SimpleNamespace(trip=SimpleNamespace(trip_id="T2"), stop_time_update=[]))])

    with patch("src.services.gtfsr.httpx.AsyncClient", return_value=FakeAsyncClient()), \
         patch("src.services.gtfsr._parse_feed", return_value=feed):
        result = await gtfsr.fetch_trip_updates("T1", mode="bus")

    assert result == []
