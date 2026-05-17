from datetime import datetime

from src.utils import opening_hours
from src.utils.opening_hours import (
    _iter_ranges,
    _now_in_tz,
    _parse_range,
    _parse_time_component,
    _status_for_day,
    is_open_now,
)


def _dt(year=2026, month=5, day=18, hour=12, minute=0):
    return datetime(year, month, day, hour, minute)


def test_parse_time_component_accepts_hour_minute_and_hour_only_formats():
    assert _parse_time_component("09:30am") == (9, 30)
    assert _parse_time_component("5pm") == (17, 0)
    assert _parse_time_component(" 12:00AM ") == (0, 0)
    assert _parse_time_component("12pm") == (12, 0)


def test_parse_time_component_returns_none_for_blank_or_invalid_values():
    assert _parse_time_component("") is None
    assert _parse_time_component("not-a-time") is None


def test_parse_range_returns_start_end_tuple_or_none_for_malformed_values():
    assert _parse_range("9am - 5pm") == ((9, 0), (17, 0))
    assert _parse_range("9am") is None
    assert _parse_range("bad - 5pm") is None
    assert _parse_range("9am - bad") is None


def test_iter_ranges_handles_multiple_separators_and_skips_invalid_chunks():
    result = list(_iter_ranges("9am-12pm; 1pm-5pm / bad & 6pm-7pm and 8pm-9pm,"))

    assert result == [
        ((9, 0), (12, 0)),
        ((13, 0), (17, 0)),
        ((18, 0), (19, 0)),
        ((20, 0), (21, 0)),
    ]


def test_status_for_day_returns_none_when_hours_missing_or_blank():
    monday = _dt(hour=12)

    assert _status_for_day({}, monday, monday) is None
    assert _status_for_day({"monday": "  "}, monday, monday) is None


def test_status_for_day_returns_false_for_explicit_closed():
    monday = _dt(hour=12)

    assert _status_for_day({"monday": "closed"}, monday, monday) is False
    assert _status_for_day({"monday": " CLOSED "}, monday, monday) is False


def test_status_for_day_returns_true_inside_range_and_false_outside_range():
    monday = _dt(hour=12)

    assert _status_for_day({"monday": "9am - 5pm"}, monday, _dt(hour=10)) is True
    assert _status_for_day({"monday": "9am - 5pm"}, monday, _dt(hour=18)) is False


def test_status_for_day_includes_exact_start_and_end_times():
    monday = _dt(hour=12)

    assert _status_for_day({"monday": "9am - 5pm"}, monday, _dt(hour=9)) is True
    assert _status_for_day({"monday": "9am - 5pm"}, monday, _dt(hour=17)) is True


def test_status_for_day_handles_overnight_range():
    monday = _dt(hour=12)

    assert _status_for_day({"monday": "10pm - 2am"}, monday, _dt(hour=23)) is True
    assert _status_for_day({"monday": "10pm - 2am"}, monday, _dt(day=19, hour=1)) is True


def test_status_for_day_returns_none_when_text_contains_no_valid_range():
    monday = _dt(hour=12)

    assert _status_for_day({"monday": "by appointment"}, monday, monday) is None


def test_is_open_now_returns_none_for_missing_or_non_dict_hours():
    assert is_open_now(None, _dt()) is None
    assert is_open_now([], _dt()) is None
    assert is_open_now({}, _dt()) is None


def test_is_open_now_checks_previous_day_overnight_before_today():
    tuesday_early = _dt(day=19, hour=1)

    assert is_open_now({"monday": "10pm - 2am", "tuesday": "closed"}, tuesday_early) is True


def test_is_open_now_uses_today_status_when_previous_day_not_open():
    monday_noon = _dt(hour=12)

    assert is_open_now({"sunday": "closed", "monday": "9am - 5pm"}, monday_noon) is True
    assert is_open_now({"sunday": "closed", "monday": "closed"}, monday_noon) is False


def test_is_open_now_returns_none_when_today_status_unknown():
    monday_noon = _dt(hour=12)

    assert is_open_now({"sunday": "closed"}, monday_noon) is None


def test_now_in_tz_returns_timezone_aware_datetime_for_valid_timezone():
    result = _now_in_tz("Australia/Sydney")

    assert result.tzinfo is not None


def test_now_in_tz_falls_back_for_invalid_timezone_or_missing_timezone():
    invalid = _now_in_tz("Not/AZone")
    missing = _now_in_tz(None)

    assert isinstance(invalid, datetime)
    assert isinstance(missing, datetime)


def test_now_in_tz_falls_back_when_zoneinfo_is_unavailable(monkeypatch):
    monkeypatch.setattr(opening_hours, "ZoneInfo", None)

    result = _now_in_tz("Australia/Sydney")

    assert isinstance(result, datetime)
