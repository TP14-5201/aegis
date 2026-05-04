import pandas as pd
from typing import Callable

from src.core.config import settings
from src.core.logging import logger

from src.data.wranglers.melbourne_wrangler import wrangle_melbourne
from src.data.wranglers.datagov_wrangler import wrangle_datagov
from src.data.wranglers.food_insecurity_wrangler import wrangle_food_insecurity
from src.data.wranglers.vic_lga_boundaries_wrangler import wrangle_viclga_boundaries, add_lga_pid_from_lga_population_data
from src.data.wranglers.lga_population_wrangler import wrangle_lga_population
from src.data.wranglers.diet_indicator_wrangler import wrangle_diet_indicator
from src.data.wranglers.health_outcome_wrangler import wrangle_health_outcome
from src.data.wranglers.low_cost_diet_wrangler import wrangle_low_cost_diet
from src.data.wranglers.low_cost_diet_health_outcome_wrangler import wrangle_low_cost_diet_health_outcome
from src.data.wranglers.recommended_macronutrients_intake_wrangler import wrangle_recommended_macronutrients_intake
from src.data.wranglers.dishes_wrangler import wrangle_dishes
from src.data.wranglers.ingredients_wrangler import wrangle_ingredients
from src.data.wranglers.dish_ingredients_wrangler import wrangle_dish_ingredients
from src.data.wranglers.ingredient_nutrients_wrangler import wrangle_ingredient_nutrients
from src.data.wranglers.ingredient_substitutes_wrangler import wrangle_ingredient_substitutes


def _load_and_wrangle(
    path: str, 
    wrangler_func: Callable[..., pd.DataFrame], # Flexible arguments to support different wranglers
    label: str,
    is_excel: bool = False,
    *args,
    **kwargs
) -> pd.DataFrame:
    """Helper to handle the repetitive read/log/wrangle logic."""
    try:
        df = pd.read_excel(path, sheet_name=0) if is_excel else pd.read_csv(path)
        return wrangler_func(df, *args, **kwargs)
    except Exception as e:
        logger.error(f"Failed to read {label} raw data from '{path}': {e}")
        raise


def load_lga_population_dataset() -> pd.DataFrame:
    """Load VIC LGA population dataset."""
    return _load_and_wrangle(settings.LGA_POPULATION_RAW_PATH, wrangle_lga_population, "LGA population")


def load_lga_boundaries_dataset() -> pd.DataFrame:
    """Load VIC LGA boundaries dataset."""
    df_boundaries = _load_and_wrangle(
        settings.VICLGA_BOUNDARY_RAW_PATH,
        wrangle_viclga_boundaries, 
        "LGA boundaries", 
        df_population=load_lga_population_dataset()) # Take the lga_pid from the population dataset
    return df_boundaries


def load_emergency_services_dataset() -> pd.DataFrame:
    """Load and combine Melbourne and DataGov datasets."""
    df_melbourne = _load_and_wrangle(
        settings.MELBOURNE_RAW_PATH, 
        wrangle_melbourne, 
        "Melbourne",
        df_lga_boundaries=load_lga_boundaries_dataset()) # Take the lga_pid from the population dataset
    df_datagov = _load_and_wrangle(
        settings.DATAGOV_RAW_PATH, 
        wrangle_datagov, 
        "DataGov",
        df_lga_boundaries=load_lga_boundaries_dataset()) # Take the lga_pid from the population dataset
    return pd.concat([df_melbourne, df_datagov], ignore_index=True).sort_values(by="name")


def load_food_insecurity_dataset() -> pd.DataFrame:
    """Load food insecurity dataset (Excel).

    The wrangler requires the wrangled vic_boundaries and viclga_boundaries
    DataFrames to resolve `ufi` and `lga_pid` via joins.
    """
    try:
        df_raw = pd.read_excel(settings.FOOD_INSECURITY_RAW_PATH, sheet_name=0)
        df_lga = _load_and_wrangle(
            settings.VICLGA_BOUNDARY_RAW_PATH, 
            wrangle_viclga_boundaries, 
            "VIC LGA boundaries", 
            df_population=load_lga_population_dataset()) # Take the lga_pid from the population dataset
        return wrangle_food_insecurity(df_raw, df_lga)
    except Exception as e:
        logger.error(f"Failed to load food insecurity dataset: {e}")
        raise


def load_diet_indicator_dataset() -> pd.DataFrame:
    """Load VPHS 2014 food insecurity diet indicators dataset (Table A1-18)."""
    return _load_and_wrangle(settings.DIET_INDICATOR_RAW_PATH, wrangle_diet_indicator, "Diet Indicator")


def load_health_outcome_dataset() -> pd.DataFrame:
    """Load VPHS 2014 food insecurity health outcomes dataset (Table A1-19)."""
    return _load_and_wrangle(settings.HEALTH_OUTCOME_RAW_PATH, wrangle_health_outcome, "Health Outcome")


def load_low_cost_diet_dataset() -> pd.DataFrame:
    """Load VPHS 2014 parents low cost diet table (Table A1-27)."""
    return _load_and_wrangle(settings.LOW_COST_DIET_RAW_PATH, wrangle_low_cost_diet, "Low Cost Diet")


def load_low_cost_diet_health_outcome_dataset() -> pd.DataFrame:
    """Load VPHS 2014 parents low cost diet health outcomes table (Table A1-28)."""
    return _load_and_wrangle(settings.LOW_COST_DIET_HEALTH_OUTCOME_RAW_PATH, wrangle_low_cost_diet_health_outcome, "Low Cost Diet Health Outcome")


def load_recommended_macronutrients_intake_dataset() -> pd.DataFrame:
    """Load recommended macronutrients intake dataset (Table A1-27)."""
    return _load_and_wrangle(settings.RECOMMENDED_MACRONUTRIENTS_INTAKE_RAW_PATH, wrangle_recommended_macronutrients_intake, "Recommended Macronutrients Intake")


# ---------------------------------------------------------------------------
# ChereBowl grocery recommendation loaders
# ---------------------------------------------------------------------------

def load_dishes_dataset() -> pd.DataFrame:
    """Load Yummly dishes (id, cuisine, ingredients) and wrangle into DB-ready shape."""
    return _load_and_wrangle(settings.DISHES_RAW_PATH, wrangle_dishes, "Dishes")


def load_ingredients_dataset() -> pd.DataFrame:
    """Load VIC grocery pricing CSV and wrangle into Ingredient records."""
    return _load_and_wrangle(settings.INGREDIENTS_PRICING_RAW_PATH, wrangle_ingredients, "Ingredients pricing")


def load_dish_ingredients_dataset() -> pd.DataFrame:
    """Load dish_ingredients_raw.csv (generated by fetch_dish_ingredients.py).

    Returns an empty DataFrame if the file does not yet exist — callers must
    guard against this and skip seeding gracefully.
    """
    import os
    if not os.path.exists(settings.DISH_INGREDIENTS_RAW_PATH):
        logger.warning(
            f"dish_ingredients_raw.csv not found at {settings.DISH_INGREDIENTS_RAW_PATH}. "
            "Run 'python -m src.scripts.fetch_dish_ingredients' first."
        )
        return pd.DataFrame(columns=["dish_name", "ingredient_name", "quantity_g", "is_optional"])
    return _load_and_wrangle(settings.DISH_INGREDIENTS_RAW_PATH, wrangle_dish_ingredients, "Dish-ingredient links")


def load_ingredient_nutrients_dataset() -> pd.DataFrame:
    """Load ingredient_nutrients_raw.csv (generated by fetch_usda_nutrients.py).

    Returns an empty DataFrame if the file is absent or empty.
    """
    import os
    path = settings.INGREDIENT_NUTRIENTS_RAW_PATH
    if not os.path.exists(path) or os.path.getsize(path) < 10:
        logger.warning(
            f"ingredient_nutrients_raw.csv absent or empty at {path}. "
            "Run 'python -m src.scripts.fetch_usda_nutrients' first."
        )
        return pd.DataFrame(columns=["ingredient_name", "nutrient_name", "amount_per_100g", "unit"])
    return _load_and_wrangle(path, wrangle_ingredient_nutrients, "Ingredient nutrients")


def load_ingredient_substitutes_dataset() -> pd.DataFrame:
    """Load ingredient_substitutes_raw.csv (generated by fetch_miskg_substitutes or manually).

    Returns an empty DataFrame if the file is absent.
    """
    import os
    if not os.path.exists(settings.INGREDIENT_SUBSTITUTES_RAW_PATH):
        logger.warning(
            f"ingredient_substitutes_raw.csv not found at {settings.INGREDIENT_SUBSTITUTES_RAW_PATH}. "
            "Run 'python -m src.scripts.fetch_miskg_substitutes' first."
        )
        return pd.DataFrame(columns=["ingredient_name", "substitute_name", "similarity_score", "reason", "source"])
    return _load_and_wrangle(settings.INGREDIENT_SUBSTITUTES_RAW_PATH, wrangle_ingredient_substitutes, "Ingredient substitutes")