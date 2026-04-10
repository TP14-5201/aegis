import pandas as pd
import numpy as np


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Converts columns to snake_case, removes special chars and whitespace."""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r'[^\w\s]', '', regex=True)
        .str.replace(' ', '_')
    )
    return df


def clean_whitespaces(df: pd.DataFrame) -> pd.DataFrame:
    """Trims all strings."""
    df = df.apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df


def clean_na_values(df: pd.DataFrame) -> pd.DataFrame:
    """Replaces 'N/A', 'n/a', 'None', 'NULL' with NaN."""
    df = df.replace(['', 'N/A', 'n/a', 'None', 'NULL'], np.nan)
    return df


def normalize_coordinates(df: pd.DataFrame, lat_col: str, lon_col: str) -> pd.DataFrame:
    """Ensures lat/lon are numeric and handles conversion errors."""
    df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
    df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')
    return df


def initial_cleaning_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Runs the initial cleaning pipeline."""
    df = df.copy()
    df = standardize_columns(df)
    df = clean_whitespaces(df)
    df = clean_na_values(df)
    return df


def select_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Select final columns and drop the rest."""
    included_cols = [
        "name", 
        "description", 
        "target_audience", 
        "address", 
        "suburb",
        "primary_phone",
        "phone_display",
        "email", 
        "website", 
        "social_media", 
        "opening_hours", 
        "cost",
        "tram_routes",
        "bus_routes",
        "nearest_train_station",
        "categories",
        "longitude",
        "latitude"
    ]
    return df[included_cols]


def add_source_column(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """Adds a source column to the dataframe."""
    df["source"] = source
    return df


def normalize_website(df: pd.DataFrame) -> pd.DataFrame:
    """Ensures the URL is lowercase and starts with https://"""
    url = df["website"].fillna("").astype(str).str.strip().str.lower()    
    # Remove any existing protocol to re-add it cleanly
    url = url.str.replace("http://", "").str.replace("https://", "")
    df["website"] = ("https://" + url).where(url != "", "")

    return df