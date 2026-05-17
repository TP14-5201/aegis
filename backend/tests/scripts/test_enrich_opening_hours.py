import argparse
import importlib
import sys
import types
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
import requests


class FakeColumn:
    def isnot(self, value):
        return self


class FakeSupportService:
    latitude = FakeColumn()
    longitude = FakeColumn()


_original_database = sys.modules.get("src.database")
_original_models = sys.modules.get("src.models")
sys.modules["src.database"] = types.SimpleNamespace(SessionLocal=MagicMock())
sys.modules["src.models"] = types.SimpleNamespace(SupportService=FakeSupportService)
script = importlib.import_module("src.scripts.enrich_opening_hours")
if _original_database is None:
    sys.modules.pop("src.database", None)
else:
    sys.modules["src.database"] = _original_database
if _original_models is None:
    sys.modules.pop("src.models", None)
else:
    sys.modules["src.models"] = _original_models


class FakeQuery:
    def __init__(self, rows):
        self.rows = rows

    def filter(self, *args, **kwargs):
        return self

    def all(self):
        return self.rows


class FakeDb:
    def __init__(self, rows):
        self.rows = rows
        self.commits = 0
        self.closed = False

    def query(self, *args, **kwargs):
        return FakeQuery(self.rows)

    def commit(self):
        self.commits += 1

    def close(self):
        self.closed = True


def service(name, address="1 Test St", opening_hours=None):
    return SimpleNamespace(
        name=name,
        address=address,
        latitude=-37.8,
        longitude=144.9,
        opening_hours=opening_hours,
    )


def args(**overrides):
    values = {"api_key": "key", "dry_run": False, "limit": None, "sleep": 0}
    values.update(overrides)
    return argparse.Namespace(**values)


@pytest.mark.parametrize(
    ("hhmm", "expected"),
    [
        ("0000", "12:00am"),
        ("0905", "09:05am"),
        ("1200", "12:00pm"),
        ("1700", "05:00pm"),
    ],
)
def test_hhmm_to_12h(hhmm, expected):
    assert script._hhmm_to_12h(hhmm) == expected


def test_periods_to_hours_dict_handles_edge_cases():
    periods = [
        {"open": {"day": 1, "time": "0900"}, "close": {"day": 1, "time": "1200"}},
        {"open": {"day": 1, "time": "1300"}, "close": {"day": 1, "time": "1700"}},
        {"open": {"day": 2, "time": "0000"}},
        {"open": {"time": "0900"}, "close": {"day": 3, "time": "1000"}},
        {"open": {"day": 4, "time": "0900"}},
    ]

    assert script.periods_to_hours_dict(periods) == {
        "monday": "09:00am - 12:00pm; 01:00pm - 05:00pm",
        "tuesday": "open 24 hours",
    }


def test_find_place_returns_first_candidate_place_id():
    response = MagicMock()
    response.json.return_value = {"candidates": [{"place_id": "abc"}]}
    with patch("src.scripts.enrich_opening_hours.requests.get", return_value=response) as get:
        assert script.find_place("1 Test St", -37.8, 144.9, "key") == "abc"

    response.raise_for_status.assert_called_once()
    assert get.call_args.kwargs["params"]["locationbias"] == "circle:5000@-37.8,144.9"


def test_find_place_returns_none_without_candidates():
    response = MagicMock()
    response.json.return_value = {"candidates": []}
    with patch("src.scripts.enrich_opening_hours.requests.get", return_value=response):
        assert script.find_place("1 Test St", -37.8, 144.9, "key") is None


def test_get_place_hours_returns_opening_hours_or_none():
    response = MagicMock()
    response.json.return_value = {"result": {"opening_hours": {"periods": []}}}
    with patch("src.scripts.enrich_opening_hours.requests.get", return_value=response) as get:
        assert script.get_place_hours("place", "key") == {"periods": []}

    response.raise_for_status.assert_called_once()
    assert get.call_args.kwargs["params"]["fields"] == "opening_hours"

    response.json.return_value = {"result": {}}
    with patch("src.scripts.enrich_opening_hours.requests.get", return_value=response):
        assert script.get_place_hours("place", "key") is None


def test_enrich_exits_without_api_key():
    with patch("src.scripts.enrich_opening_hours.sys.exit", side_effect=SystemExit) as exit_:
        with pytest.raises(SystemExit):
            script.enrich(args(api_key=None))

    exit_.assert_called_once_with(1)


def test_enrich_skips_existing_hours_and_missing_address():
    rows = [service("Done", opening_hours={"monday": "open 24 hours"}), service("No Address", address="")]
    db = FakeDb(rows)

    with patch("src.scripts.enrich_opening_hours.SessionLocal", return_value=db), \
         patch("src.scripts.enrich_opening_hours.find_place") as find_place:
        script.enrich(args())

    find_place.assert_not_called()
    assert db.commits == 0
    assert db.closed is True


def test_enrich_writes_hours_when_place_periods_are_valid():
    row = service("Kitchen")
    db = FakeDb([row])

    with patch("src.scripts.enrich_opening_hours.SessionLocal", return_value=db), \
         patch("src.scripts.enrich_opening_hours.find_place", return_value="place") as find_place, \
         patch("src.scripts.enrich_opening_hours.get_place_hours", return_value={
             "periods": [{"open": {"day": 1, "time": "0900"}, "close": {"day": 1, "time": "1700"}}]
         }), \
         patch("src.scripts.enrich_opening_hours.time.sleep"):
        script.enrich(args())

    find_place.assert_called_once()
    assert row.opening_hours == {"monday": "09:00am - 05:00pm"}
    assert db.commits == 1


def test_enrich_dry_run_does_not_commit():
    row = service("Kitchen")
    db = FakeDb([row])

    with patch("src.scripts.enrich_opening_hours.SessionLocal", return_value=db), \
         patch("src.scripts.enrich_opening_hours.find_place", return_value="place"), \
         patch("src.scripts.enrich_opening_hours.get_place_hours", return_value={
             "periods": [{"open": {"day": 1, "time": "0900"}, "close": {"day": 1, "time": "1700"}}]
         }), \
         patch("src.scripts.enrich_opening_hours.time.sleep"):
        script.enrich(args(dry_run=True))

    assert row.opening_hours is None
    assert db.commits == 0


def test_enrich_counts_not_found_no_hours_empty_periods_and_errors():
    rows = [service("Missing"), service("No Hours"), service("Empty"), service("HTTP"), service("Boom")]
    db = FakeDb(rows)

    def find_side_effect(address, lat, lon, api_key):
        if address == rows[0].address:
            return None
        if address == rows[3].address:
            raise requests.RequestException("timeout")
        if address == rows[4].address:
            raise RuntimeError("bad")
        return "place"

    rows[0].address = "missing"
    rows[1].address = "no-hours"
    rows[2].address = "empty"
    rows[3].address = "http"
    rows[4].address = "boom"

    def hours_side_effect(place_id, api_key):
        return {"periods": []} if rows[2].address == "empty" else {}

    with patch("src.scripts.enrich_opening_hours.SessionLocal", return_value=db), \
         patch("src.scripts.enrich_opening_hours.find_place", side_effect=find_side_effect), \
         patch("src.scripts.enrich_opening_hours.get_place_hours", side_effect=hours_side_effect), \
         patch("src.scripts.enrich_opening_hours.time.sleep"):
        script.enrich(args())

    assert db.commits == 0
    assert db.closed is True


def test_enrich_applies_limit():
    rows = [service("One"), service("Two")]
    db = FakeDb(rows)

    with patch("src.scripts.enrich_opening_hours.SessionLocal", return_value=db), \
         patch("src.scripts.enrich_opening_hours.find_place", return_value=None) as find_place, \
         patch("src.scripts.enrich_opening_hours.time.sleep"):
        script.enrich(args(limit=1))

    assert find_place.call_count == 1


def test_parse_args_reads_cli_values():
    with patch(
        "sys.argv",
        ["enrich", "--api-key", "abc", "--dry-run", "--limit", "3", "--sleep", "0.25"],
    ):
        parsed = script._parse_args()

    assert parsed.api_key == "abc"
    assert parsed.dry_run is True
    assert parsed.limit == 3
    assert parsed.sleep == 0.25
