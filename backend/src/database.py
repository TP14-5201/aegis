import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Render provides "postgres://" URLs — SQLAlchemy 2.0 requires "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

if DATABASE_URL.startswith("sqlite"):
    # SpatiaLite is required for GeoAlchemy2 geometry columns on SQLite.
    # The .dll lives in the conda env's Library/bin directory.
    _SPATIALITE_PATH = os.getenv(
        "SPATIALITE_LIBRARY_PATH",
        r"C:\Users\Priyank\anaconda3\envs\aegis\Library\bin\mod_spatialite",
    )

    @event.listens_for(engine, "connect")
    def _load_spatialite(dbapi_conn, _):
        dbapi_conn.enable_load_extension(True)
        try:
            dbapi_conn.load_extension(_SPATIALITE_PATH)
        except Exception:
            # Fallback: rely on PATH (works when the conda env is activated)
            dbapi_conn.load_extension("mod_spatialite")
        finally:
            dbapi_conn.enable_load_extension(False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
