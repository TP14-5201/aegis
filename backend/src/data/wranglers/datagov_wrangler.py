import re

import pandas as pd

from .utils import initial_cleaning_pipeline, clean_na_values, normalize_website, normalize_coordinates, select_columns, add_source_column, rename_columns, determine_emergency_service_lga
from src.core.config import settings


def filter_victoria_services(df: pd.DataFrame) -> pd.DataFrame:
    """Filters the dataframe to only include services in Victoria."""
    is_vic = df['address'].astype(str).str.contains(r'\bVIC\b', case=False, na=False)
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


def create_placeholder_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Creates placeholder columns for fields not present in this dataset.

    These are intentionally set to empty strings here; clean_na_values (called
    at the end of the pipeline) will convert them to NaN before DB insert.
    """
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


def wrangle_datagov(df: pd.DataFrame, df_lga_boundaries: pd.DataFrame) -> pd.DataFrame:
    """Main wrangling pipeline for DataGov emergency relief services data."""
    
    DATAGOV_COLUMN_MAP = {
        "outlet_name": "name",
        "organistaion_website": "website",
        "outlet_address": "address",
        "town_or_suburb": "suburb",
    }

    df = initial_cleaning_pipeline(df)
    df = rename_columns(df, DATAGOV_COLUMN_MAP)
    df = filter_victoria_services(df)
    df = extract_organisation_url(df)
    df = normalize_website(df)
    df = normalize_coordinates(df, lat_col="latitude", lon_col="longitude")
    df = create_placeholder_columns(df)
    df = select_columns(df, settings.EMERGENCY_INCLUDED_COLS)
    df = add_source_column(df, source="DataGov")
    # clean_na_values is called last so that placeholder/empty strings set
    # during transformation are correctly converted to NaN before DB insert.
    df = clean_na_values(df)
    df = determine_emergency_service_lga(df, df_lga_boundaries)

    return df
