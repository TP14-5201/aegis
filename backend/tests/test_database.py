import importlib
import os
from unittest.mock import MagicMock, patch

# Keep import-time engine creation independent from a developer's .env DATABASE_URL.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import src.database as database


def test_database_url_rewrites_render_postgres_scheme(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgres://user:pass@host/db")

    with patch("sqlalchemy.create_engine") as mock_create_engine:
        importlib.reload(database)

    mock_create_engine.assert_called_once()
    assert mock_create_engine.call_args.args[0] == "postgresql://user:pass@host/db"
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    importlib.reload(database)


def test_get_db_yields_session_and_closes_it(monkeypatch):
    session = MagicMock()
    monkeypatch.setattr(database, "SessionLocal", MagicMock(return_value=session))

    db_generator = database.get_db()
    assert next(db_generator) is session

    try:
        next(db_generator)
    except StopIteration:
        pass

    session.close.assert_called_once()
