import pandas as pd

from src.core.config import settings
from .utils import initial_cleaning_pipeline, rename_columns, select_columns


def filter_by_phu(df: pd.DataFrame) -> pd.DataFrame:
    """Filter the data by their local Public Health Unit (PHU)"""
    df = df[df["stratified_by"].isin(settings.SELECTED_REGIONS)]
    return df


def filter_by_gender(df: pd.DataFrame) -> pd.DataFrame:
    """Filter the data by gender"""
    df = df[df["gender"].isin(["Men", "Women"])]
    return df


def filter_by_estimate_type(df: pd.DataFrame) -> pd.DataFrame:
    """Filter the data by estimate type"""
    df = df[df["estimate_type"]=="Crude"]
    return df


def filter_by_indicator_category(df: pd.DataFrame) -> pd.DataFrame:
    """"""
    df = df[df["indicator_category"].isin(["Yes", "Yes, definitely", "Sometimes"])]
    return df


def clean_subpopulation(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the subpopulation column"""
    df["subpopulation"] = df["subpopulation"].str.split("(").str[0].str.strip()
    return df


def impute_estimate(df: pd.DataFrame) -> pd.DataFrame:
    """Impute the estimate column 0"""
    df["estimate_pct"] = df["estimate_pct"].fillna(0)
    return df


def filter_records(df: pd.DataFrame) -> pd.DataFrame:
    """Filter records by PHU, gender, and estimate type"""
    df = filter_by_phu(df)
    df = filter_by_gender(df)
    df = filter_by_estimate_type(df)
    df = filter_by_indicator_category(df)

    return df


def add_region_ids(df: pd.DataFrame, viclga_boundaries: pd.DataFrame) -> pd.DataFrame:
    """Enrich the food insecurity data with `lga_pid` by joining against the wrangled boundary tables."""
    lga_lookup = (
        viclga_boundaries[["lga_name", "lga_pid"]]
        .drop_duplicates("lga_name")
        .set_index("lga_name")["lga_pid"]
    )
    df["lga_pid"] = df["subpopulation"].map(lga_lookup)
    df = df.dropna(subset=["lga_pid"]) # Drop rows where lga_pid is NaN

    return df


def wrangle_food_insecurity(df: pd.DataFrame, viclga_boundaries: pd.DataFrame) -> pd.DataFrame:
    """Main wrangling pipeline for the food insecurity data."""
    FOOD_INSECURITY_COLUMN_MAP = {
        "": "estimate_pct", # Empty string due to the initial cleaning pipeline to clean the column headers (initially was '%')
    }
    FOOD_INSECURITY_INCLUDED_COLS = ["gender", "indicator", "indicator_category", "subpopulation", "estimate_pct"]

    df = initial_cleaning_pipeline(df)
    df = filter_records(df)
    df = clean_subpopulation(df)
    df = rename_columns(df, FOOD_INSECURITY_COLUMN_MAP)
    df = select_columns(df, FOOD_INSECURITY_INCLUDED_COLS)
    df = impute_estimate(df)
    df = add_region_ids(df, viclga_boundaries)

    return df
