from fastapi.testclient import TestClient

from src.main import app, get_db


class FakeQuery:
    def __init__(self, rows):
        self._rows = rows

    def outerjoin(self, *args, **kwargs):
        return self

    def group_by(self, *args, **kwargs):
        return self

    def all(self):
        return self._rows


class FakeDB:
    def __init__(self, rows):
        self._rows = rows

    def query(self, *args, **kwargs):
        return FakeQuery(self._rows)


class FakeRow:
    def __init__(self, lga_pid, lga_name, pop_2024_total, men_pct, women_pct, emergency_services_count):
        self.lga_pid = lga_pid
        self.lga_name = lga_name
        self.pop_2024_total = pop_2024_total
        self.men_pct = men_pct
        self.women_pct = women_pct
        self.emergency_services_count = emergency_services_count


def test_get_lga_stats_returns_aggregated_stats():
    def fake_get_db():
        yield FakeDB(
            [
                FakeRow(
                    lga_pid="123",
                    lga_name="Sample LGA",
                    pop_2024_total=10000,
                    men_pct=12.345,
                    women_pct=8.901,
                    emergency_services_count=4,
                )
            ]
        )

    app.dependency_overrides[get_db] = fake_get_db
    client = TestClient(app)

    response = client.get("/lga/stats")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == [
        {
            "lga_name": "Sample LGA",
            "pop_2024_total": 10000,
            "men_pct": 12.345,
            "women_pct": 8.901,
            "emergency_services_count": 4,
        }
    ]


def test_get_lga_stats_returns_empty_list_when_no_data():
    def fake_get_db():
        yield FakeDB([])

    app.dependency_overrides[get_db] = fake_get_db
    client = TestClient(app)

    response = client.get("/lga/stats")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == []
