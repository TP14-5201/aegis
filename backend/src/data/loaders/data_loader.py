import pandas as pd
from typing import Callable
from src.core.config import settings
from src.core.logging import logger
from src.data.wranglers.utils import initial_cleaning_pipeline
from src.data.wranglers.melbourne_wrangler import wrangle_melbourne
from src.data.wranglers.datagov_wrangler import wrangle_datagov
from src.data.wranglers.food_insecurity_wrangler import wrangle_food_insecurity
from src.data.wranglers.vic_boundaries_wrangler import wrangle_vic_boundaries
from src.data.wranglers.vic_lga_boundaries_wrangler import wrangle_viclga_boundaries

def _load_and_wrangle(
    path: str, 
    wrangler_func: Callable[[pd.DataFrame], pd.DataFrame], 
    label: str,
    is_excel: bool = False
) -> pd.DataFrame:
    """Helper to handle the repetitive read/log/wrangle logic."""
    try:
        df = pd.read_excel(path, sheet_name=0) if is_excel else pd.read_csv(path)
        return wrangler_func(df)
    except Exception as e:
        logger.error(f"Failed to read {label} raw data from '{path}': {e}")
        raise

def load_emergency_services_dataset() -> pd.DataFrame:
    """Load and combine Melbourne and DataGov datasets."""
    df_melbourne = _load_and_wrangle(settings.MELBOURNE_RAW_PATH, wrangle_melbourne, "Melbourne")
    df_datagov = _load_and_wrangle(settings.DATAGOV_RAW_PATH, wrangle_datagov, "DataGov")
    
    return pd.concat([df_melbourne, df_datagov], ignore_index=True).sort_values(by="name")

def load_food_insecurity_dataset() -> pd.DataFrame:
    """Load food insecurity dataset (Excel)."""

    def _get_lga_service_counts() -> pd.DataFrame:
        """Internal helper to calculate emergency service counts per LGA."""
        df = pd.read_csv(settings.DATAGOV_RAW_PATH)
        df = initial_cleaning_pipeline(df)
        
        # Process LGA names and aggregate
        counts = (
            df.assign(lga=df["lga"].astype(str).str.split("(").str[0].str.strip())
            .groupby("lga")
            .size()
            .reset_index(name="emergency_services_count")
        )
        return counts

    food_insecurity_df = _load_and_wrangle(
        settings.FOOD_INSECURITY_RAW_PATH, 
        wrangle_food_insecurity, 
        "food insecurity", 
        is_excel=True
    )
    lga_counts = _get_lga_service_counts()

    # Merge and filter for valid LGAs only
    return pd.merge(
        food_insecurity_df, 
        lga_counts, 
        left_on="subpopulation", 
        right_on="lga", 
        how="inner"
    )

def load_vic_boundaries_dataset() -> pd.DataFrame:
    """Load VIC PHN boundaries dataset."""
    return _load_and_wrangle(settings.VICGOV_BOUNDARY_RAW_PATH, wrangle_vic_boundaries, "VIC boundaries")

def load_viclga_boundaries_dataset() -> pd.DataFrame:
    """Load VIC LGA boundaries dataset."""
    return _load_and_wrangle(settings.VICLGA_BOUNDARY_RAW_PATH, wrangle_viclga_boundaries, "VIC LGA boundaries")