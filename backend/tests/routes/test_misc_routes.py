import json
import math
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from src import main
from src.main import (
    app,
    get_all_macronutrient_goals,
    get_all_services,
    get_diet_indicators,
    get_health_outcomes,
    get_ingredient_substitutes,
    get_lga_boundaries,
    get_lga_food_inaccessibility_reasons,
    get_low_cost_diet_health_outcomes,
    get_low_cost_diet_stats,
    get_nearby_services,
    gtfsr_trip_update,
    gtfsr_vehicles,
    health,
    on_startup,
)
from src.services.ingredient_substitution import SubstituteResult, SubstituteSlot


class ChainQuery:
    def __init__(self, rows):
        self._rows = rows

    def all(self):
        return self._rows

    def distinct(self, *args, **kwargs):
        return self

    def filter(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self


class FakeDB:
    def __init__(self, rows):
        self._rows = rows

    def query(self, *args, **kwargs):
        return ChainQuery(self._rows)


class BrokenDB:
    def query(self, *args, **kwargs):
        raise RuntimeError("database unavailable")


def _json_response_body(response):
    return json.loads(response.body.decode("utf-8"))


def test_on_startup_creates_tables_and_logs_warmup_failures():
    db = MagicMock()

    with patch("src.main.Base.metadata.create_all") as mock_create_all, \
         patch("src.main.get_db", return_value=iter([db])), \
         patch("src.main.recommendation_service.warm_percentiles", side_effect=RuntimeError("warm fail")) as mock_warm, \
         patch("src.main.substitution_engine.load_index", side_effect=RuntimeError("index fail")) as mock_load_index, \
         patch("src.main.logger") as mock_logger:
        on_startup()

    mock_create_all.assert_called_once_with(bind=main.engine)
    mock_warm.assert_called_once_with(db)
    mock_load_index.assert_called_once_with(db)
    assert mock_logger.warning.call_count == 2
    mock_logger.info.assert_called_once_with("API startup complete; database ready.")


def test_health_returns_ok():
    assert health() == {"status": "ok"}


def test_get_lga_boundaries_skips_rows_without_geojson():
    rows = [
        SimpleNamespace(lga_pid="LGA001", lga_name="Missing", geojson=None),
        SimpleNamespace(lga_pid="LGA002", lga_name="Present", geojson='{"type":"Point","coordinates":[1,2]}'),
    ]

    response = get_lga_boundaries(db=FakeDB(rows))

    assert _json_response_body(response)["features"] == [
        {
            "type": "Feature",
            "properties": {"lga_name": "Present", "lga_pid": "LGA002"},
            "geometry": {"type": "Point", "coordinates": [1, 2]},
        }
    ]


def test_get_lga_boundaries_raises_500_on_db_error():
    with pytest.raises(HTTPException) as exc_info:
        get_lga_boundaries(db=BrokenDB())

    assert exc_info.value.status_code == 500


def test_get_lga_food_inaccessibility_reasons_raises_500_on_db_error():
    with pytest.raises(HTTPException) as exc_info:
        get_lga_food_inaccessibility_reasons(db=BrokenDB())

    assert exc_info.value.status_code == 500


def test_get_all_services_returns_sorted_services_and_handles_open_status_error():
    rows = [
        SimpleNamespace(
            id=2,
            name="Zulu",
            description=None,
            target_audience=None,
            address=None,
            suburb=None,
            primary_phone=None,
            phone_display=None,
            email=None,
            website=None,
            social_media=None,
            opening_hours="not-a-dict",
            cost=None,
            tram_routes=None,
            bus_routes=None,
            nearest_train_station=None,
            categories="not-a-list",
            longitude=145.0,
            latitude=-37.0,
            source="test",
        ),
        SimpleNamespace(
            id=1,
            name="Alpha",
            description="Food pantry",
            target_audience="All",
            address="1 Main St",
            suburb="Melbourne",
            primary_phone="123",
            phone_display="123",
            email="a@example.com",
            website="https://example.com",
            social_media=None,
            opening_hours={"Monday": ["09:00-17:00"]},
            cost="Free",
            tram_routes="1",
            bus_routes="2",
            nearest_train_station="Central",
            categories=["food"],
            longitude=144.0,
            latitude=-38.0,
            source="test",
        ),
    ]

    with patch("src.main._now_in_tz", return_value="now"), \
         patch("src.main.is_open_now", side_effect=[RuntimeError("bad hours"), True]):
        result = get_all_services(db=FakeDB(rows), tz="Australia/Sydney")

    assert [item["name"] for item in result] == ["Alpha", "Zulu"]
    assert result[0]["is_open_now"] is True
    assert result[1]["opening_hours"] == {}
    assert result[1]["categories"] == []
    assert result[1]["is_open_now"] is None


def test_get_all_services_raises_500_on_db_error():
    with pytest.raises(HTTPException) as exc_info:
        get_all_services(db=BrokenDB())

    assert exc_info.value.status_code == 500


def test_get_nearby_services_normalises_shapes_filters_closed_and_handles_open_errors():
    found = [
        {"name": "Open", "categories": math.nan, "opening_hours": math.nan},
        {"name": "Closed", "categories": None, "opening_hours": None},
        {"name": "Unknown", "categories": ["food"], "opening_hours": {}},
    ]

    with patch("src.main.find_nearby_support_services", return_value=found) as mock_find, \
         patch("src.main._now_in_tz", return_value="now"), \
         patch("src.main.is_open_now", side_effect=[True, False, RuntimeError("bad hours")]):
        result = get_nearby_services(
            lat=-37.8,
            lon=144.9,
            radius_km=5,
            limit=25,
            include_datagov=True,
            keywords=[],
            tz="Australia/Sydney",
            db=MagicMock(),
        )

    assert mock_find.call_args.kwargs["keywords"] == main.DEFAULT_KEYWORDS
    assert [item["name"] for item in result] == ["Open", "Unknown"]
    assert result[0]["categories"] == []
    assert result[0]["opening_hours"] == {}
    assert result[1]["is_open_now"] is None


def test_get_nearby_services_raises_500_on_search_error():
    with patch("src.main.find_nearby_support_services", side_effect=RuntimeError("search failed")):
        with pytest.raises(HTTPException) as exc_info:
            get_nearby_services(
                lat=0,
                lon=0,
                radius_km=5,
                limit=25,
                include_datagov=True,
                keywords=None,
                tz=None,
                db=MagicMock(),
            )

    assert exc_info.value.status_code == 500


@pytest.mark.parametrize(
    "handler,empty_detail,non_empty_rows",
    [
        (get_diet_indicators, "Internal error fetching dietary data", [{"category": "Food"}]),
        (get_health_outcomes, "Internal error fetching health outcome data", [{"category": "Health"}]),
        (get_low_cost_diet_stats, "Internal error fetching low-cost diet data", [{"category": "Diet"}]),
        (
            get_low_cost_diet_health_outcomes,
            "Internal error fetching dietary health outcome data",
            [{"category": "Diet", "health_outcome": "Outcome"}],
        ),
        (
            get_all_macronutrient_goals,
            "Internal error fetching recommended macronutrients",
            [{"age": "19-30", "nutrient": "Protein"}],
        ),
    ],
)
def test_json_list_endpoints_return_empty_non_empty_and_error_responses(handler, empty_detail, non_empty_rows):
    empty_response = handler(db=FakeDB([]))
    assert _json_response_body(empty_response) == []

    non_empty_response = handler(db=FakeDB(non_empty_rows))
    assert _json_response_body(non_empty_response) == non_empty_rows

    with pytest.raises(HTTPException) as exc_info:
        handler(db=BrokenDB())

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == empty_detail


def test_result_to_dict_serialises_substitute_slots_and_none_slots():
    slot = SubstituteSlot(
        ingredient_code="A1",
        product_name="Apples",
        sub_category="Fruit",
        health_benefits=["fibre"],
        retail_price=2.5,
        nutrition_grade="a",
        proteins_100g=1.0,
        fat_100g=0.1,
        carbohydrates_100g=14.0,
        energy_100g=220.0,
        similarity_score=0.95,
        objective_score=0.88,
    )
    result = SubstituteResult(query_code="Q1", query_name="Query", budget=slot, nutrition=None, balanced=slot)

    body = main._result_to_dict(result)

    assert body["budget"]["ingredient_code"] == "A1"
    assert body["nutrition"] is None
    assert body["balanced"]["objective_score"] == 0.88


def test_get_ingredient_substitutes_returns_serialised_result():
    result = SubstituteResult(query_code="Q1", query_name="Query", error="No candidates")

    with patch("src.main.substitution_engine.get_substitutes", return_value=result) as mock_get:
        body = get_ingredient_substitutes("Q1", db=MagicMock())

    mock_get.assert_called_once()
    assert body == {
        "query_code": "Q1",
        "query_name": "Query",
        "budget": None,
        "nutrition": None,
        "balanced": None,
        "error": "No candidates",
    }


def test_get_ingredient_substitutes_raises_500_on_engine_error():
    with patch("src.main.substitution_engine.get_substitutes", side_effect=RuntimeError("engine failed")):
        with pytest.raises(HTTPException) as exc_info:
            get_ingredient_substitutes("Q1", db=MagicMock())

    assert exc_info.value.status_code == 500


class FakeWeatherResponse:
    def __init__(self, payload=None, status_code=200, fail_http=False):
        self._payload = payload or {}
        self.status_code = status_code
        self._fail_http = fail_http

    def raise_for_status(self):
        if self._fail_http:
            request = main.httpx.Request("GET", "https://weather.example")
            response = main.httpx.Response(self.status_code, request=request)
            raise main.httpx.HTTPStatusError("bad response", request=request, response=response)

    def json(self):
        return self._payload


class FakeAsyncClient:
    def __init__(self, response=None, error=None, timeout=None):
        self._response = response
        self._error = error
        self.timeout = timeout

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def get(self, url):
        if self._error:
            raise self._error
        return self._response


def test_weather_returns_503_when_api_key_missing(monkeypatch):
    monkeypatch.setattr(main, "_OPENWEATHER_KEY", "")
    client = TestClient(app)

    response = client.get("/weather?lat=-37.8&lon=144.9")

    assert response.status_code == 503


def test_weather_returns_normalised_weather_payload(monkeypatch):
    monkeypatch.setattr(main, "_OPENWEATHER_KEY", "key")
    payload = {
        "main": {"temp": 18.6, "feels_like": 17.5},
        "rain": {"1h": 1.24},
        "wind": {"speed": 4.0},
        "weather": [{"description": "light rain", "icon": "10d"}],
    }
    fake_response = FakeWeatherResponse(payload=payload)

    monkeypatch.setattr(main.httpx, "AsyncClient", lambda timeout: FakeAsyncClient(response=fake_response, timeout=timeout))
    client = TestClient(app)

    response = client.get("/weather?lat=-37.8&lon=144.9")

    assert response.status_code == 200
    assert response.json() == {
        "temp": 19,
        "feels_like": 18,
        "rain_mm": 1.2,
        "wind_kph": 14.4,
        "description": "Light rain",
        "icon": "10d",
    }


def test_weather_returns_502_for_openweather_http_error(monkeypatch):
    monkeypatch.setattr(main, "_OPENWEATHER_KEY", "key")
    fake_response = FakeWeatherResponse(status_code=401, fail_http=True)
    monkeypatch.setattr(main.httpx, "AsyncClient", lambda timeout: FakeAsyncClient(response=fake_response, timeout=timeout))
    client = TestClient(app)

    response = client.get("/weather?lat=-37.8&lon=144.9")

    assert response.status_code == 502
    assert response.json() == {"detail": "OpenWeather error: 401"}


def test_weather_returns_502_for_generic_fetch_error(monkeypatch):
    monkeypatch.setattr(main, "_OPENWEATHER_KEY", "key")
    monkeypatch.setattr(main.httpx, "AsyncClient", lambda timeout: FakeAsyncClient(error=RuntimeError("network down")))
    client = TestClient(app)

    response = client.get("/weather?lat=-37.8&lon=144.9")

    assert response.status_code == 502
    assert response.json() == {"detail": "Could not fetch weather data"}


@pytest.mark.asyncio
async def test_gtfsr_vehicles_returns_all_or_filtered_vehicle_positions():
    vehicles = [{"route_id": "1"}, {"route_id": "2"}]

    with patch("src.main.fetch_vehicle_positions", new=AsyncMock(return_value=vehicles)):
        assert await gtfsr_vehicles() == vehicles
        assert await gtfsr_vehicles(route_ids="2,3") == [{"route_id": "2"}]


@pytest.mark.asyncio
async def test_gtfsr_vehicles_raises_502_on_feed_error():
    with patch("src.main.fetch_vehicle_positions", new=AsyncMock(side_effect=RuntimeError("feed down"))):
        with pytest.raises(HTTPException) as exc_info:
            await gtfsr_vehicles()

    assert exc_info.value.status_code == 502


@pytest.mark.asyncio
async def test_gtfsr_trip_update_returns_updates_and_raises_502_on_error():
    updates = [{"stop_id": "S1"}]

    with patch("src.main.fetch_trip_updates", new=AsyncMock(return_value=updates)) as mock_fetch:
        assert await gtfsr_trip_update("trip-1", mode="tram") == updates
    mock_fetch.assert_awaited_once_with("trip-1", mode="tram")

    with patch("src.main.fetch_trip_updates", new=AsyncMock(side_effect=RuntimeError("feed down"))):
        with pytest.raises(HTTPException) as exc_info:
            await gtfsr_trip_update("trip-1")

    assert exc_info.value.status_code == 502
