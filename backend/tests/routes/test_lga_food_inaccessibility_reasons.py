import math

from fastapi.testclient import TestClient

from src.main import app, get_db


class FakeQuery:
    def __init__(self, rows):
        self._rows = rows

    def order_by(self, *args, **kwargs):
        return self

    def all(self):
        return self._rows


class FakeDB:
    def __init__(self, rows):
        self._rows = rows

    def query(self, *args, **kwargs):
        return FakeQuery(self._rows)


class FakeRow:
    def __init__(self, lga_pid, limited_variety, too_expensive, wrong_quality, transport_gap):
        self.lga_pid = lga_pid
        self.limited_variety = limited_variety
        self.too_expensive = too_expensive
        self.wrong_quality = wrong_quality
        self.transport_gap = transport_gap


def test_get_lga_food_inaccessibility_reasons_returns_selected_fields():
    def fake_get_db():
        yield FakeDB(
            [
                FakeRow(
                    lga_pid="LGA001",
                    limited_variety=12.5,
                    too_expensive=45.0,
                    wrong_quality=8.25,
                    transport_gap=3.0,
                )
            ]
        )

    app.dependency_overrides[get_db] = fake_get_db
    client = TestClient(app)

    response = client.get("/lga/food-inaccessibility-reasons")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == [
        {
            "lga_pid": "LGA001",
            "limited_variety": 12.5,
            "too_expensive": 45.0,
            "wrong_quality": 8.25,
            "transport_gap": 3.0,
        }
    ]


def test_get_lga_food_inaccessibility_reasons_returns_empty_list_when_no_data():
    def fake_get_db():
        yield FakeDB([])

    app.dependency_overrides[get_db] = fake_get_db
    client = TestClient(app)

    response = client.get("/lga/food-inaccessibility-reasons")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == []


def test_get_lga_food_inaccessibility_reasons_returns_unknown_for_missing_values():
    def fake_get_db():
        yield FakeDB(
            [
                FakeRow(
                    lga_pid="LGA002",
                    limited_variety=None,
                    too_expensive=math.nan,
                    wrong_quality=0.0,
                    transport_gap=None,
                )
            ]
        )

    app.dependency_overrides[get_db] = fake_get_db
    client = TestClient(app)

    response = client.get("/lga/food-inaccessibility-reasons")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == [
        {
            "lga_pid": "LGA002",
            "limited_variety": "Unknown",
            "too_expensive": "Unknown",
            "wrong_quality": 0.0,
            "transport_gap": "Unknown",
        }
    ]
