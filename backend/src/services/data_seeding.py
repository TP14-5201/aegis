import os
import pandas as pd

from sqlalchemy.orm import Session
from src.database import SessionLocal, engine
from src.models import (
    Base, SupportService, FoodInsecurity, 
    VicLgaBoundary, LgaPopulation, 
    DietIndicator, HealthOutcome, LowCostDiet,
    LowCostDietHealthOutcome
)

from src.core.config import settings
from src.core.logging import logger
from src.scripts.download_dev_data import save_local_copy
from src.data.loaders.data_loader import (
    load_emergency_services_dataset, 
    load_food_insecurity_dataset, 
    load_lga_boundaries_dataset, 
    load_lga_population_dataset, 
    load_diet_indicator_dataset,
    load_health_outcome_dataset,
    load_low_cost_diet_dataset,
    load_low_cost_diet_health_outcome_dataset
)


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
        settings.VICLGA_BOUNDARY_RAW_PATH,
        settings.LGA_POPULATION_RAW_PATH,
        settings.DIET_INDICATOR_RAW_PATH
    ]
    if any(not os.path.exists(cfg) for cfg in data_configs):
        logger.info(f"Missing files detected. Downloading...")
        save_local_copy()
    else:
        logger.info("All data has been downloaded.")


def load_dataset() -> pd.DataFrame:
    """Load all datasets"""
    DATASET_REGISTRY = [
        (load_emergency_services_dataset, SupportService),
        (load_food_insecurity_dataset, FoodInsecurity),
        (load_lga_boundaries_dataset, VicLgaBoundary),
        (load_lga_population_dataset, LgaPopulation),
        (load_diet_indicator_dataset, DietIndicator),
        (load_health_outcome_dataset, HealthOutcome),
        (load_low_cost_diet_dataset, LowCostDiet),
        (load_low_cost_diet_health_outcome_dataset, LowCostDietHealthOutcome)
    ]
    
    return [(loader(), model) for loader, model in DATASET_REGISTRY]


if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    download_dataset()
    datasets = load_dataset()
    db = SessionLocal()
    try:
        for df, model in datasets:
            seed_support_services(db, df, model)
    finally:
        db.close()
