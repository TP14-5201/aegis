import pandas as pd

from src.core.config import settings
from src.core.logging import logger
from src.data.wranglers.melbourne_wrangler import wrangle_melbourne
from src.data.wranglers.datagov_wrangler import wrangle_datagov
from src.data.wranglers.food_insecurity_wrangler import wrangle_food_insecurity
from src.data.wranglers.vic_boundaries_wrangler import wrangle_vic_boundaries
from src.data.wranglers.vic_lga_boundaries_wrangler import wrangle_viclga_boundaries


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
    """Load food insecurity dataset"""
    try:
        df_food_insecurity = pd.read_excel(settings.FOOD_INSECURITY_RAW_PATH, sheet_name=0)
    except Exception as e:
        logger.error(f"Failed to read food insecurity raw data from '{settings.FOOD_INSECURITY_RAW_PATH}': {e}")
        raise

    df_food_insecurity = wrangle_food_insecurity(df_food_insecurity)

    return df_food_insecurity


def load_vic_boundaries_dataset() -> pd.DataFrame:
    """Load VIC Primary Health Networks (PHN) boundaries dataset"""
    try:
        df_vic_boundaries = pd.read_csv(settings.VICGOV_BOUNDARY_RAW_PATH)
    except Exception as e:
        logger.error(f"Failed to read VIC boundaries raw data from '{settings.VICGOV_BOUNDARY_RAW_PATH}': {e}")
        raise

    df_vic_boundaries = wrangle_vic_boundaries(df_vic_boundaries)

    return df_vic_boundaries


def load_viclga_boundaries_dataset() -> pd.DataFrame:
    """Load VIC LGA (Local Government Area) SA4 (Statistical Area Level 4) boundaries dataset"""
    try:
        df_viclga_boundaries = pd.read_csv(settings.VICLGA_BOUNDARY_RAW_PATH)
    except Exception as e:
        logger.error(f"Failed to read VIC LGA boundaries raw data from '{settings.VICLGA_BOUNDARY_RAW_PATH}': {e}")
        raise

    df_viclga_boundaries = wrangle_viclga_boundaries(df_viclga_boundaries)

    return df_viclga_boundaries