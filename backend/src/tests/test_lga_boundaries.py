from fastapi.testclient import TestClient

from src.main import app, get_db


class FakeQuery:
    def __init__(self, rows):
        self._rows = rows

    def distinct(self, *args, **kwargs):
        return self

    def all(self):
        return self._rows


class FakeDB:
    def __init__(self, rows):
        self._rows = rows

    def query(self, *args, **kwargs):
        return FakeQuery(self._rows)


class FakeRow:
    def __init__(self, lga_name, geojson):
        self.lga_name = lga_name
        self.geojson = geojson


def test_get_lga_boundaries_returns_feature_collection():
    def fake_get_db():
        yield FakeDB([FakeRow("Melbourne", '{"type":"Polygon","coordinates":[]}')])

    app.dependency_overrides[get_db] = fake_get_db
    client = TestClient(app)

    response = client.get("/lga/boundaries")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"lga_name": "Melbourne"},
                "geometry": {"type": "Polygon", "coordinates": []},
            }
        ],
    }


def test_get_lga_boundaries_returns_empty_feature_collection_when_no_data():
    def fake_get_db():
        yield FakeDB([])

    app.dependency_overrides[get_db] = fake_get_db
    client = TestClient(app)

    response = client.get("/lga/boundaries")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "type": "FeatureCollection",
        "features": [],
        "message": "No boundaries found",
    }
