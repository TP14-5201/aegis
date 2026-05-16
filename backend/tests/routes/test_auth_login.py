import bcrypt
from fastapi.testclient import TestClient

from src.main import app


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def test_auth_login_accepts_password_matching_configured_bcrypt_hash(monkeypatch):
    monkeypatch.setenv("LOGIN_PASSWORD_HASH", _hash_password("password123"))
    client = TestClient(app)

    response = client.post("/auth/login", json={"password": "password123"})

    assert response.status_code == 200
    assert response.json() == {"success": True}


def test_auth_login_rejects_incorrect_password(monkeypatch):
    monkeypatch.setenv("LOGIN_PASSWORD_HASH", _hash_password("password123"))
    client = TestClient(app)

    response = client.post("/auth/login", json={"password": "wrong-password"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect password"}


def test_auth_login_returns_503_when_password_hash_is_missing(monkeypatch):
    monkeypatch.delenv("LOGIN_PASSWORD_HASH", raising=False)
    client = TestClient(app)

    response = client.post("/auth/login", json={"password": "password123"})

    assert response.status_code == 503
    assert response.json() == {"detail": "Login is not configured"}


def test_auth_login_returns_503_when_password_hash_is_invalid(monkeypatch):
    monkeypatch.setenv("LOGIN_PASSWORD_HASH", "not-a-bcrypt-hash")
    client = TestClient(app)

    response = client.post("/auth/login", json={"password": "password123"})

    assert response.status_code == 503
    assert response.json() == {"detail": "Login is not configured"}
