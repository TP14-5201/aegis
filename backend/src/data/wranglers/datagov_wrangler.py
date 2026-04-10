import re

import pandas as pd
import numpy as np

from .utils import initial_cleaning_pipeline, clean_na_values, normalize_website, normalize_coordinates, select_columns, add_source_column


def filter_victoria_services(df: pd.DataFrame) -> pd.DataFrame:
    """Filters the dataframe to only include services in Victoria."""
    is_vic = df['address'].str.contains(r'\bVIC\b', case=False, na=False)
    # Victorian postcodes mostly start with 3 or 8
    is_vic_postcode = df['postcode'].astype(str).str.startswith(('3', '8'))

    return df[is_vic & is_vic_postcode]


def extract_organisation_url(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts the URL from the <a href='...'> string."""
    def _extract(val):
        if pd.isna(val) or not str(val).strip():
            return None
        # Use regex to find text between single or double quotes
        match = re.search(r"href=['\"]([^'\"]+)['\"]", str(val))
        return match.group(1) if match else val
    
    df["website"] = df["website"].apply(_extract)

    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Renames the 'What' and 'Who' column headers to make it more descriptive"""
    cols_rename_map = {
        "outlet_name": "name",
        "organistaion_website": "website",
        "outlet_address": "address",
        "town_or_suburb": "suburb",
    }
    df = df.rename(columns=cols_rename_map)
    return df


def create_placeholder_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Creates placeholder columns for the dataframe."""
    df["description"] = ""
    df["target_audience"] = ""
    df["primary_phone"] = ""
    df["phone_display"] = ""
    df["email"] = ""
    df["social_media"] = ""
    df["opening_hours"] = ""
    df["cost"] = ""
    df["tram_routes"] = ""
    df["bus_routes"] = ""
    df["nearest_train_station"] = ""
    df["categories"] = ""
    return df


def wrangle_datagov(df: pd.DataFrame) -> pd.DataFrame:
    """Wrangling pipeline for Melbourne data."""
    df = initial_cleaning_pipeline(df)
    df = rename_columns(df)
    df = filter_victoria_services(df)
    df = extract_organisation_url(df)
    df = normalize_website(df)
    df = normalize_coordinates(df, lat_col="latitude", lon_col="longitude")
    df = create_placeholder_columns(df)
    df = select_columns(df)
    df = add_source_column(df, source="DataGov")
    df = clean_na_values(df)

    return df