from types import SimpleNamespace

import pytest

from src.services.nearby_search import (
    _bounding_box,
    _keyword_filter,
    find_nearby_support_services,
    haversine_km,
    search_support_service_suburbs,
)


class ChainQuery:
    def __init__(self, rows):
        self.rows = rows
        self.filters = []
        self.limit_value = None

    def filter(self, *args):
        self.filters.append(args)
        return self

    def group_by(self, *args):
        return self

    def order_by(self, *args):
        return self

    def limit(self, value):
        self.limit_value = value
        return self

    def all(self):
        return self.rows


class FakeDB:
    def __init__(self, rows):
        self.query_obj = ChainQuery(rows)
        self.query_args = None

    def query(self, *args):
        self.query_args = args
        return self.query_obj


def _service(**overrides):
    row = {
        "id": 1,
        "name": "Food Bank",
        "description": "Emergency food",
        "target_audience": "All",
        "address": "1 Main St",
        "suburb": "Melbourne",
        "primary_phone": "123",
        "phone_display": "123",
        "email": "a@example.com",
        "website": "https://example.com",
        "social_media": None,
        "opening_hours": {"monday": "9am-5pm"},
        "cost": "Free",
        "tram_routes": "1",
        "bus_routes": "2",
        "nearest_train_station": "Central",
        "categories": ["food"],
        "longitude": 144.9631,
        "latitude": -37.8136,
        "source": "Test",
    }
    row.update(overrides)
    return SimpleNamespace(**row)


def test_haversine_km_zero_for_same_point_and_known_melbourne_sydney_distance():
    assert haversine_km(-37.8136, 144.9631, -37.8136, 144.9631) == pytest.approx(0.0)
    assert haversine_km(-37.8136, 144.9631, -33.8688, 151.2093) == pytest.approx(714, rel=0.03)


def test_bounding_box_expands_around_point_and_handles_extreme_latitudes():
    lat_min, lat_max, lon_min, lon_max = _bounding_box(-37.8, 144.9, 10)
    assert lat_min < -37.8 < lat_max
    assert lon_min < 144.9 < lon_max

    polar_box = _bounding_box(90.0, 0.0, 10)
    assert polar_box[2] < 0.0 < polar_box[3]


def test_keyword_filter_returns_none_for_empty_keywords_and_filter_for_terms():
    assert _keyword_filter([]) is None
    assert _keyword_filter(["food"]) is not None


def test_find_nearby_support_services_defaults_keywords_and_returns_sorted_limited_results():
    near = _service(id=1, name="Near", latitude=-37.8136, longitude=144.9631)
    nearer = _service(id=2, name="Nearer", latitude=-37.8140, longitude=144.9631)
    far = _service(id=3, name="Far", latitude=-35.0, longitude=144.9631)
    null_lat = _service(id=4, name="Null", latitude=None, longitude=144.9631)
    db = FakeDB([far, near, null_lat, nearer])

    result = find_nearby_support_services(
        db,
        user_lat=-37.8136,
        user_lon=144.9631,
        radius_km=2,
        limit=1,
        keywords=None,
    )

    assert len(db.query_obj.filters) == 1
    assert [item["name"] for item in result] == ["Near"]
    assert result[0]["distance_km"] == 0.0


def test_find_nearby_support_services_applies_keyword_filter_with_and_without_datagov():
    db_with_datagov = FakeDB([_service()])
    find_nearby_support_services(
        db_with_datagov,
        user_lat=-37.8,
        user_lon=144.9,
        radius_km=5,
        keywords=["food"],
        include_datagov=True,
    )
    assert len(db_with_datagov.query_obj.filters) == 2

    db_without_datagov = FakeDB([_service()])
    find_nearby_support_services(
        db_without_datagov,
        user_lat=-37.8,
        user_lon=144.9,
        radius_km=5,
        keywords=["food"],
        include_datagov=False,
    )
    assert len(db_without_datagov.query_obj.filters) == 2


def test_find_nearby_support_services_negative_limit_returns_empty():
    db = FakeDB([_service()])

    result = find_nearby_support_services(db, -37.8136, 144.9631, radius_km=5, limit=-1)

    assert result == []


def test_search_support_service_suburbs_formats_rows_and_applies_limit_and_search_filter():
    rows = [SimpleNamespace(suburb="Melbourne", latitude=-37.8136123, longitude=144.9631456)]
    db = FakeDB(rows)

    result = search_support_service_suburbs(db, q=" mel ", limit=3)

    assert db.query_obj.limit_value == 3
    assert len(db.query_obj.filters) == 2
    assert result == [
        {
            "label": "Melbourne, VIC",
            "suburb": "Melbourne",
            "latitude": -37.813612,
            "longitude": 144.963146,
        }
    ]


def test_search_support_service_suburbs_skips_search_filter_for_blank_query():
    db = FakeDB([])

    result = search_support_service_suburbs(db, q="   ", limit=8)

    assert result == []
    assert len(db.query_obj.filters) == 1
