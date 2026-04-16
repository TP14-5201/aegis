import pandas as pd

from src.core.config import settings
from .utils import initial_cleaning_pipeline


def filter_by_phu(df: pd.DataFrame) -> pd.DataFrame:
    """Filter the data by their local Public Health Unit (PHU)"""
    df = df[df["stratified_by"].isin(settings.SELECTED_REGIONS)]
    return df


def filter_by_gender(df: pd.DataFrame) -> pd.DataFrame:
    """Filter the data by gender"""
    df = df[df["gender"]=="People"]
    return df


def filter_by_estimate_type(df: pd.DataFrame) -> pd.DataFrame:
    """Filter the data by estimate type"""
    df = df[df["estimate_type"]=="Crude"]
    return df


def filter_by_indicator_category(df: pd.DataFrame) -> pd.DataFrame:
    """"""
    df = df[df["indicator_category"].isin(["Yes", "Yes, definitely"])]
    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename the columns to be more readable"""
    df = df.rename(columns={
        "": "estimate_pct", # Empty string due to the initial cleaning pipeline to clean the column headers (initially was '%')
        "stratified_by": "region"
    })
    return df


def select_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Select the columns needed for the data"""
    df = df[["estimate_type", "gender", "indicator", "indicator_category", "region", "subpopulation", "estimate_pct"]]
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


def aggregate_estimate_count(df: pd.DataFrame) -> pd.DataFrame:
    df = df.groupby(["indicator", "indicator_category", "vic_region_code"]).agg({"estimate_pct": "mean"}).reset_index()
    return df


def add_vic_region_code(df: pd.DataFrame) -> pd.DataFrame:
    REGION_CODES = {
        "LGAs of Barwon South-West PHU": 10,
        "LGAS of North Eastern PHU": 11,
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
    df = initial_cleaning_pipeline(df)
    df = filter_records(df)
    df = rename_columns(df)
    df = select_columns(df)
    df = impute_estimate(df)
    df = add_vic_region_code(df)
    df = aggregate_estimate_count(df)

    return df
