from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

DAY_KEYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
    "public_holidays",
]


def _parse_time_component(s: str) -> Optional[Tuple[int, int]]:
    s = s.strip()
    if not s:
        return None
    # Expect like 09:00am or 5:30pm (lower/upper tolerated)
    try:
        t = datetime.strptime(s.upper(), "%I:%M%p")
        return t.hour, t.minute
    except ValueError:
        # Try hour only like 9am
        try:
            t = datetime.strptime(s.upper(), "%I%p")
            return t.hour, 0
        except ValueError:
            return None


def _parse_range(text: str) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Parse a single range like '09:00am - 05:00pm'."""
    parts = [p.strip() for p in text.split("-")]
    if len(parts) != 2:
        return None
    start = _parse_time_component(parts[0])
    end = _parse_time_component(parts[1])
    if start is None or end is None:
        return None
    return start, end


def _iter_ranges(value: str):
    """Yield one or more time ranges from a potentially composite string.

    Supports separators like ';', '/', '&', ' and ', ','. Falls back to single range.
    """
    normalized = value.replace(" and ", ";").replace("/", ";").replace("&", ";")
    # Also accept commas as separators, but avoid splitting times like '09:00am'
    normalized = normalized.replace(",", ";")
    for chunk in normalized.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        rng = _parse_range(chunk)
        if rng:
            yield rng


def _status_for_day(opening_hours: Dict[str, str], day_dt: datetime, now_local: datetime) -> Optional[bool]:
    day_key = day_dt.strftime("%A").lower()
    value = opening_hours.get(day_key)
    if value is None or str(value).strip() == "":
        return None
    if str(value).strip().lower() == "closed":
        return False

    any_range = False
    for (sh, sm), (eh, em) in _iter_ranges(str(value)):
        any_range = True
        start_dt = day_dt.replace(hour=sh, minute=sm, second=0, microsecond=0)
        end_dt = day_dt.replace(hour=eh, minute=em, second=0, microsecond=0)
        overnight = end_dt <= start_dt
        if overnight:
            end_dt = end_dt + timedelta(days=1)
        if start_dt <= now_local <= end_dt:
            return True
    return False if any_range else None


def is_open_now(opening_hours: Optional[Dict[str, str]], now_local: datetime) -> Optional[bool]:
    """Return True if open, False if closed, or None if unknown.

    Considers overnight ranges from the previous day (e.g., 22:00-02:00)
    so that early-morning times are matched correctly.
    """
    if not opening_hours or not isinstance(opening_hours, dict):
        return None

    # Check previous day's overnight coverage first
    prev_midday = (now_local - timedelta(days=1)).replace(hour=12, minute=0, second=0, microsecond=0)
    prev_status = _status_for_day(opening_hours, prev_midday, now_local)
    if prev_status is True:
        return True

    # Then check today's ranges
    today_midday = now_local.replace(hour=12, minute=0, second=0, microsecond=0)
    today_status = _status_for_day(opening_hours, today_midday, now_local)
    if today_status is not None:
        return today_status

    return None
