import os
import pandas as pd

from sqlalchemy.orm import Session
from src.database import SessionLocal, engine
from src.models import (
    Base, SupportService, FoodInsecurity,
    VicLgaBoundary, LgaPopulation,
    DietIndicator, HealthOutcome, LowCostDiet,
    LowCostDietHealthOutcome, RecommendedMacronutrientsIntake, FoodInaccessibilityReasons,
    Ingredient, IngredientNutrition, IngredientHealthRating
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
    load_low_cost_diet_health_outcome_dataset,
    load_recommended_macronutrients_intake_dataset,
    load_food_inaccessibility_reasons_dataset,
    load_ingredient_dataset,
    load_ingredient_nutrition_dataset,
    load_ingredient_health_rating_dataset,
)


def seed_database(db: Session, df: pd.DataFrame, model: Base) -> None:
    """Clears and re-seeds the table from the given DataFrame.

    Deletes all existing rows before inserting to avoid duplicates on re-runs.
    Rolls back and re-raises on any error.
    """
    logger.info(f"Starting database seed with {len(df)} records...")

    records = df.to_dict(orient='records')
    try:
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
        settings.DIET_INDICATOR_RAW_PATH,
        settings.HEALTH_OUTCOME_RAW_PATH,
        settings.LOW_COST_DIET_RAW_PATH,
        settings.LOW_COST_DIET_HEALTH_OUTCOME_RAW_PATH,
        settings.RECOMMENDED_MACRONUTRIENTS_INTAKE_RAW_PATH,
        settings.FOOD_INACCESSIBILITY_REASONS_RAW_PATH,
        settings.GROCERY_PRICES_RAW_PATH,
        settings.FOOD_FACTS_RAW_PATH
    ]
    if any(not os.path.exists(cfg) for cfg in data_configs):
        logger.info(f"Missing files detected. Downloading...")
        save_local_copy()
    else:
        logger.info("All data has been downloaded.")


def load_dataset() -> pd.DataFrame:
    """Load all datasets"""
    DATASET_REGISTRY = [
        (load_lga_population_dataset, LgaPopulation),
        (load_lga_boundaries_dataset, VicLgaBoundary),
        (load_emergency_services_dataset, SupportService),
        (load_food_insecurity_dataset, FoodInsecurity),
        (load_diet_indicator_dataset, DietIndicator),
        (load_health_outcome_dataset, HealthOutcome),
        (load_low_cost_diet_dataset, LowCostDiet),
        (load_low_cost_diet_health_outcome_dataset, LowCostDietHealthOutcome),
        (load_recommended_macronutrients_intake_dataset, RecommendedMacronutrientsIntake),
        (load_food_inaccessibility_reasons_dataset, FoodInaccessibilityReasons),
        (load_ingredient_dataset, Ingredient),
        (load_ingredient_nutrition_dataset, IngredientNutrition),
        (load_ingredient_health_rating_dataset, IngredientHealthRating),
    ]
    
    return [(loader(), model) for loader, model in DATASET_REGISTRY]


if __name__ == "__main__":
    from src.services.ingredient_substitution import engine as substitution_engine

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    download_dataset()
    datasets = load_dataset()
    db = SessionLocal()
    try:
        for df, model in datasets:
            seed_database(db, df, model)
        logger.info("Building FAISS substitution index…")
        substitution_engine.build_index(db)
        logger.info("FAISS index built successfully.")
    finally:
        db.close()