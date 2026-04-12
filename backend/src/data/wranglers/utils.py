import pandas as pd
import numpy as np


# Sentinel values to treat as missing/null across all datasets
_NA_SENTINEL_VALUES = ["", "N/A", "n/a", "None", "NULL", "https://"]


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
    """Trims leading/trailing whitespace from all string cells."""
    # Use DataFrame.map (pandas >= 2.1) or applymap for element-wise operation.
    # df.apply operates on columns (Series), so isinstance(col, str) is always
    # False — the previous implementation was a no-op.
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())
    return df


def clean_na_values(df: pd.DataFrame) -> pd.DataFrame:
    """Replaces common sentinel strings (and bare 'https://') with NaN."""
    df = df.replace(_NA_SENTINEL_VALUES, np.nan)
    return df


def normalize_coordinates(df: pd.DataFrame, lat_col: str, lon_col: str) -> pd.DataFrame:
    """Ensures lat/lon are numeric and handles conversion errors."""
    df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
    df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')
    return df


def initial_cleaning_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Runs the initial structural cleaning pipeline.

    Note: clean_na_values is intentionally NOT called here. It is the
    responsibility of each wrangler to call it as the final step, after all
    transformations (including placeholder column creation) have completed.
    """
    df = df.copy()
    df = standardize_columns(df)
    df = clean_whitespaces(df)
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
    """Ensures the URL is lowercase and starts with https://.

    Empty or whitespace-only values are left as empty strings so that the
    subsequent clean_na_values call can convert them to NaN uniformly.
    """
    url = df["website"].fillna("").astype(str).str.strip().str.lower()
    # Remove any existing protocol to re-add it cleanly
    url = url.str.replace("http://", "", regex=False).str.replace("https://", "", regex=False)
    df["website"] = ("https://" + url).where(url != "", "")

    return df
