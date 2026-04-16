import os
import pandas as pd

from sqlalchemy.orm import Session
from src.database import SessionLocal, engine
from src.models import Base, SupportService, FoodInsecurity, VicBoundary

from src.core.config import settings
from src.core.logging import logger
from src.scripts.download_dev_data import save_local_copy
from src.data.wranglers.melbourne_wrangler import wrangle_melbourne
from src.data.wranglers.datagov_wrangler import wrangle_datagov
from src.data.wranglers.food_insecurity_wrangler import wrangle_food_insecurity


def seed_support_services(db: Session, df: pd.DataFrame, model: Base) -> None:
    """Clears and re-seeds the support_services table from the given DataFrame.

    Deletes all existing rows before inserting to avoid duplicates on re-runs.
    Rolls back and re-raises on any error.
    """
    logger.info(f"Starting database seed with {len(df)} records...")

    records = df.to_dict(orient='records')
    try:
        # Clear existing data to avoid duplicates if re-running
        db.query(model).delete()
        service_objects = [model(**data) for data in records]
        db.bulk_save_objects(service_objects)
        db.commit()

        logger.info(f"Database seeding completed successfully! Inserted {len(service_objects)} records.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise


def download_dataset() -> pd.DataFrame:
    """Download raw datasets if they don't exist"""
    data_configs = [
        settings.MELBOURNE_RAW_PATH, 
        settings.DATAGOV_RAW_PATH, 
        settings.FOOD_INSECURITY_RAW_PATH,
        settings.VICGOV_BOUNDARY_RAW_PATH    
    ]
    if any(not os.path.exists(cfg) for cfg in data_configs):
        logger.info(f"Missing files detected. Downloading...")
        save_local_copy()
    else:
        logger.info("All data has been downloaded.")


def load_emergency_services_dataset() -> pd.DataFrame:
    """Download (if needed), load, wrangle, and combine datasets.

    Downloads the raw CSVs if either local file is absent, then applies the
    source-specific wrangling pipelines before concatenating into one DataFrame.
    """
    try:
        df_melbourne = pd.read_csv(settings.MELBOURNE_RAW_PATH)
    except Exception as e:
        logger.error(f"Failed to read Melbourne raw data from '{settings.MELBOURNE_RAW_PATH}': {e}")
        raise

    try:
        df_datagov = pd.read_csv(settings.DATAGOV_RAW_PATH)
    except Exception as e:
        logger.error(f"Failed to read DataGov raw data from '{settings.DATAGOV_RAW_PATH}': {e}")
        raise

    df_melbourne = wrangle_melbourne(df_melbourne)
    df_datagov = wrangle_datagov(df_datagov)
    df_final = pd.concat([df_melbourne, df_datagov], ignore_index=True).sort_values(by="name")

    return df_final


def load_food_insecurity_dataset() -> pd.DataFrame:
    try:
        df_food_insecurity = pd.read_excel(settings.FOOD_INSECURITY_RAW_PATH, sheet_name=0)
    except Exception as e:
        logger.error(f"Failed to read food insecurity raw data from '{settings.FOOD_INSECURITY_RAW_PATH}': {e}")
        raise

    df_food_insecurity = wrangle_food_insecurity(df_food_insecurity)

    return df_food_insecurity


def load_vic_boundaries_dataset() -> pd.DataFrame:
    try:
        df_vic_boundaries = pd.read_csv(settings.VICGOV_BOUNDARY_RAW_PATH)
        df_vic_boundaries.columns = df_vic_boundaries.columns.str.lower()
    except Exception as e:
        logger.error(f"Failed to read VIC boundaries raw data from '{settings.VICGOV_BOUNDARY_RAW_PATH}': {e}")
        raise

    return df_vic_boundaries


def load_dataset() -> pd.DataFrame:
    df_emergency_services = load_emergency_services_dataset()
    df_food_insecurity = load_food_insecurity_dataset()
    df_vic_boundaries = load_vic_boundaries_dataset()

    return df_emergency_services, df_food_insecurity, df_vic_boundaries


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    download_dataset()
    df_emergency_services, df_food_insecurity, df_vic_boundaries = load_dataset()
    db = SessionLocal()
    try:
        seed_support_services(db, df_emergency_services, SupportService)
        seed_support_services(db, df_food_insecurity, FoodInsecurity)
        seed_support_services(db, df_vic_boundaries, VicBoundary)
    finally:
        db.close()
