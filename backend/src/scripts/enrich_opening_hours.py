"""One-time script: enrich opening_hours via Google Places API.

Run from the aegis/backend/ directory:
    python -m src.scripts.enrich_opening_hours --api-key <key> [--dry-run] [--limit 10]

Environment variable alternative:
    GOOGLE_MAPS_API_KEY=<key> python -m src.scripts.enrich_opening_hours
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
import time

import requests
from dotenv import load_dotenv

# Ensure src.* imports resolve when invoked directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

load_dotenv()

from src.database import SessionLocal  # noqa: E402
from src.models import SupportService  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger(__name__)

# Google Places API endpoints
PLACES_BASE = "https://maps.googleapis.com/maps/api/place"

# Google day index → our dict key (0 = Sunday, 1 = Monday … 6 = Saturday)
_DAY_KEY = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]


# ── Time conversion ────────────────────────────────────────────────────────────

def _hhmm_to_12h(hhmm: str) -> str:
    """Convert '0900' → '09:00am', '1700' → '05:00pm'."""
    h = int(hhmm[:2])
    m = int(hhmm[2:])
    period = "am" if h < 12 else "pm"
    h12 = h % 12 or 12
    return f"{h12:02d}:{m:02d}{period}"


def periods_to_hours_dict(periods: list) -> dict:
    """Convert Google Places API ``periods`` list to our DB format.

    Input:
        [{"open": {"day": 1, "time": "0900"}, "close": {"day": 1, "time": "1700"}}, ...]

    Output:
        {"monday": "09:00am - 05:00pm", ...}

    Edge cases:
    - 24-hour service (no ``close`` entry, open at 0000) → "open 24 hours"
    - Split shift → ranges joined with "; "  (handled by opening_hours.py parser)
    - Overnight (close.day ≠ open.day) → stored under the opening day
    """
    result: dict[str, str] = {}
    for period in periods:
        open_info = period.get("open", {})
        close_info = period.get("close")

        day_idx = open_info.get("day")
        if day_idx is None:
            continue

        day_key = _DAY_KEY[day_idx]
        open_time = open_info.get("time", "")

        # 24-hour indicator: Google omits the close entry and uses time="0000"
        if close_info is None and open_time == "0000":
            result[day_key] = "open 24 hours"
            continue

        if not close_info:
            continue  # Malformed period — skip

        close_time = close_info.get("time", "")
        range_str = f"{_hhmm_to_12h(open_time)} - {_hhmm_to_12h(close_time)}"

        # Split shift: append to existing entry with "; "
        if day_key in result and result[day_key] != "open 24 hours":
            result[day_key] = result[day_key] + "; " + range_str
        else:
            result[day_key] = range_str

    return result


# ── Google Places API calls ────────────────────────────────────────────────────

def find_place(address: str, lat: float, lon: float, api_key: str) -> str | None:
    """Call 'Find Place From Text' using street address; return ``place_id`` or ``None``."""
    resp = requests.get(
        f"{PLACES_BASE}/findplacefromtext/json",
        params={
            "input": address,
            "inputtype": "textquery",
            "fields": "place_id",
            "locationbias": f"circle:5000@{lat},{lon}",
            "key": api_key,
        },
        timeout=10,
    )
    resp.raise_for_status()
    candidates = resp.json().get("candidates", [])
    return candidates[0].get("place_id") if candidates else None


def get_place_hours(place_id: str, api_key: str) -> dict | None:
    """Call 'Place Details' requesting only ``opening_hours``.

    Returns the ``opening_hours`` sub-dict from the response, or ``None``.
    Requesting only one field keeps billing in the Basic tier (~$0.017/call).
    """
    resp = requests.get(
        f"{PLACES_BASE}/details/json",
        params={
            "place_id": place_id,
            "fields": "opening_hours",
            "key": api_key,
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json().get("result", {}).get("opening_hours")


# ── Main enrichment loop ───────────────────────────────────────────────────────

def enrich(args: argparse.Namespace) -> None:
    if not args.api_key:
        log.error("No API key provided. Set GOOGLE_MAPS_API_KEY or pass --api-key.")
        sys.exit(1)

    db = SessionLocal()
    try:
        # Process all geocoded services. Skip writing if hours already exist.
        services = (
            db.query(SupportService)
            .filter(
                SupportService.latitude.isnot(None),
                SupportService.longitude.isnot(None),
            )
            .all()
        )
        if args.limit:
            services = services[: args.limit]

        total = len(services)
        log.info(f"Services to process: {total}")
        if args.dry_run:
            log.info("DRY RUN — no changes will be written to the database.")

        found = not_found = no_hours = errors = api_calls = 0

        skipped = 0
        for i, svc in enumerate(services, 1):
            # Skip if already has hours — avoids redundant API calls on re-runs
            existing = svc.opening_hours
            if isinstance(existing, dict) and existing:
                skipped += 1
                continue

            if not svc.address:
                log.info(f"[{i}/{total}] {svc.name!r} — no address, skipping")
                skipped += 1
                continue

            log.info(f"[{i}/{total}] {svc.name!r} → {svc.address!r}")
            try:
                place_id = find_place(
                    svc.address,
                    svc.latitude, svc.longitude,
                    args.api_key,
                )
                api_calls += 1
                time.sleep(args.sleep)

                if not place_id:
                    log.info("  → Not found on Google Maps")
                    not_found += 1
                    continue

                oh = get_place_hours(place_id, args.api_key)
                api_calls += 1
                time.sleep(args.sleep)

                if not oh or "periods" not in oh:
                    log.info("  → Place found but no hours data available")
                    no_hours += 1
                    continue

                hours_dict = periods_to_hours_dict(oh["periods"])
                if not hours_dict:
                    log.info("  → Periods produced empty dict")
                    no_hours += 1
                    continue

                log.info(f"  → Got hours: {hours_dict}")
                found += 1

                if not args.dry_run:
                    svc.opening_hours = hours_dict
                    db.commit()

            except requests.RequestException as exc:
                log.warning(f"  → HTTP error: {exc}")
                errors += 1
                time.sleep(1)  # back off on network errors
            except Exception as exc:
                log.warning(f"  → Unexpected error: {exc}")
                errors += 1

        estimated_cost = api_calls * 0.017
        log.info("=" * 52)
        log.info(f"Done. Processed {total} services.")
        log.info(f"  Already had hours (skipped):             {skipped}")
        log.info(f"  Hours enriched {'(dry run)' if args.dry_run else '(written)':>10}: {found}")
        log.info(f"  Not found on Google Maps:                {not_found}")
        log.info(f"  Found but no hours data:                 {no_hours}")
        log.info(f"  Errors:                                  {errors}")
        log.info(f"  Total API calls:                         {api_calls}")
        log.info(f"  Estimated cost:                          ~${estimated_cost:.2f}")

    finally:
        db.close()


# ── CLI ────────────────────────────────────────────────────────────────────────

def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Enrich service opening_hours via Google Places API (one-time script)."
    )
    p.add_argument(
        "--api-key",
        default=os.getenv("GOOGLE_MAPS_API_KEY"),
        help="Google Maps API key (default: GOOGLE_MAPS_API_KEY env var)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Query the API but do NOT write results to the database",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process at most N services (useful for testing)",
    )
    p.add_argument(
        "--sleep",
        type=float,
        default=0.1,
        help="Seconds to sleep between each API call (default: 0.1)",
    )
    return p.parse_args()


if __name__ == "__main__":
    enrich(_parse_args())
