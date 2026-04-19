import pandas as pd

from src.core.config import settings
from .utils import initial_cleaning_pipeline


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
    df = df[df["indicator_category"].isin(["Yes", "Yes, definitely"])]
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


def add_vic_region_code(df: pd.DataFrame) -> pd.DataFrame:
    """Add VIC Primary Health Networks (PHN) region code to the dataframe"""
    REGION_CODES = {
        "LGAs of Barwon South-West PHU": 10,
        "LGAs of North Eastern PHU": 11,
        "LGAs of Gippsland PHU": 12,
        "LGAs of Grampians Wimmera Southern Mallee PHU": 13,
        "LGAs of Goulburn Valley PHU": 14,
        "LGAs of Ovens-Murray PHU": 14,
        "LGAs of Loddon Mallee PHU": 15,
        "LGAs of Western PHU": 16,
        "LGAs of South East PHU": 17,
    }
    df["vic_region_code"] = df["region"].map(REGION_CODES)
    return df


def wrangle_food_insecurity(df: pd.DataFrame) -> pd.DataFrame:
    """Main wrangling pipeline for the food insecurity data"""
    FOOD_INSECURITY_COLUMN_MAP = {
        "": "estimate_pct", # Empty string due to the initial cleaning pipeline to clean the column headers (initially was '%')
        "stratified_by": "region"
    }
    FOOD_INSECURITY_INCLUDED_COLS = ["gender", "indicator", "indicator_category", "region", "subpopulation", "estimate_pct"]

    df = initial_cleaning_pipeline(df)
    df = filter_records(df)
    df = clean_subpopulation(df)
    df = rename_columns(df, FOOD_INSECURITY_COLUMN_MAP)
    df = select_columns(df, FOOD_INSECURITY_INCLUDED_COLS)
    df = impute_estimate(df)
    df = add_vic_region_code(df)

    return df
