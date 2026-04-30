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
    df_raw = pd.read_csv(settings.DIET_INDICATOR_RAW_PATH)
    return wrangle_diet_indicator(df_raw)


def load_health_outcome_dataset() -> pd.DataFrame:
    """Load VPHS 2014 food insecurity health outcomes dataset (Table A1-19)."""
    df_raw = pd.read_csv(settings.HEALTH_OUTCOME_RAW_PATH)
    return wrangle_health_outcome(df_raw)


def load_low_cost_diet_dataset() -> pd.DataFrame:
    """Load VPHS 2014 parents low cost diet table (Table A1-27)."""
    df_raw = pd.read_csv(settings.LOW_COST_DIET_RAW_PATH)
    return wrangle_low_cost_diet(df_raw)