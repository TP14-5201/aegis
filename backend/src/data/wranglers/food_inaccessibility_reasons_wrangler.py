import pandas as pd

from src.core.config import settings
from .utils import initial_cleaning_pipeline, rename_columns, select_columns


def _clean_lga_names(reason_df: pd.DataFrame) -> pd.DataFrame:
    """Clean the lga names"""
    reason_df["lga"] = reason_df["lga"].str.split("(").str[0].str.strip()
    return reason_df


def _find_lga_pid(reason_df: pd.DataFrame, lga_df: pd.DataFrame) -> pd.DataFrame:
    """Find the lga_pid for each lga in the reason_df"""
    reason_df["lga_pid"] = reason_df["lga"].map(lga_df.set_index("lga_name")["lga_pid"])
    return reason_df


def _filter_null_pid(reason_df: pd.DataFrame) -> pd.DataFrame:
    """Filter out rows with null lga_pid"""
    reason_df = reason_df[reason_df["lga_pid"].notna()]
    return reason_df


def wrangle_food_inaccessibility_reasons(reason_df: pd.DataFrame, lga_df: pd.DataFrame) -> pd.DataFrame:
    """Main wrangling pipeline for the food insecurity data."""
    FOOD_INACCESSIBILITY_COLUMN_MAP = {
        "variety_": "limited_variety",
        "expensive_": "too_expensive",
        "quality_": "wrong_quality",
        "transport_": "transport_gap"
    }
    FOOD_INACCESSIBILITY_INCLUDED_COLS = ["lga_pid", "limited_variety", "too_expensive", "wrong_quality", "transport_gap"]

    reason_df = initial_cleaning_pipeline(reason_df)
    reason_df = _clean_lga_names(reason_df)
    reason_df = _find_lga_pid(reason_df, lga_df)
    reason_df = _filter_null_pid(reason_df)
    reason_df = rename_columns(reason_df, FOOD_INACCESSIBILITY_COLUMN_MAP)
    reason_df = select_columns(reason_df, FOOD_INACCESSIBILITY_INCLUDED_COLS)

    return reason_df
