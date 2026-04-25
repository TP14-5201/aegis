import pandas as pd

from src.core.config import settings
from .utils import initial_cleaning_pipeline, rename_columns, select_columns

# Maps PHU region names (as they appear in the raw food insecurity data) to
# the corresponding vicgov_region values used in vic_boundaries.
_PHU_TO_VICGOV_REGION = {
    "LGAs of Barwon South-West PHU":                  "BARWON SOUTH WEST",
    "LGAs of Gippsland PHU":                          "GIPPSLAND",
    "LGAs of Grampians Wimmera Southern Mallee PHU":  "GRAMPIANS",
    "LGAs of Goulburn Valley PHU":                    "HUME",
    "LGAs of Ovens-Murray PHU":                       "HUME",
    "LGAs of Loddon Mallee PHU":                      "LODDON MALLEE",
    "LGAs of North Eastern PHU":                      "EASTERN METROPOLITAN",
    "LGAs of South East PHU":                         "SOUTHERN METROPOLITAN",
    "LGAs of Western PHU":                            "NORTHERN AND WESTERN METROPOLITAN",
}


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


def add_region_ids(
    df: pd.DataFrame,
    vic_boundaries: pd.DataFrame,
    viclga_boundaries: pd.DataFrame,
) -> pd.DataFrame:
    """Enrich the food insecurity data with `ufi` and `lga_pid` by joining
    against the wrangled boundary tables.

    - `ufi` is resolved by mapping each PHU region name to its corresponding
      vicgov_region value and then looking up the `ufi` from vic_boundaries.
    - `lga_pid` is resolved by matching the `subpopulation` column (which
      contains the abbreviated LGA name) against the `lga_name` column in
      viclga_boundaries.
    """
    # --- ufi: PHU region → vicgov_region → ufi ---
    # Normalise to uppercase for a case-insensitive match (the wrangler may
    # title-case vicgov_region, while _PHU_TO_VICGOV_REGION uses uppercase).
    vic_region_to_ufi = (
        vic_boundaries[["vicgov_region", "ufi"]]
        .drop_duplicates("vicgov_region")
        .assign(vicgov_region_upper=lambda d: d["vicgov_region"].str.upper())
        .set_index("vicgov_region_upper")["ufi"]
    )
    # Build the PHU-region → ufi mapping directly from _PHU_TO_VICGOV_REGION so
    # that multiple PHU regions sharing the same vicgov_region all get resolved.
    region_to_ufi = pd.Series({
        phu: vic_region_to_ufi.get(vicgov)
        for phu, vicgov in _PHU_TO_VICGOV_REGION.items()
    })
    df["ufi"] = df["region"].map(region_to_ufi)

    # --- lga_pid: subpopulation → lga_name → lga_pid ---
    # viclga_boundaries may have duplicate lga_name columns (original full name
    # + cleaned abb_name). Keep only the last occurrence (cleaned abb_name) so
    # the lookup key matches the food insecurity subpopulation values.
    lga_df = viclga_boundaries.loc[:, ~viclga_boundaries.columns.duplicated(keep="last")]
    lga_lookup = (
        lga_df[["lga_name", "lga_pid"]]
        .drop_duplicates("lga_name")
        .set_index("lga_name")["lga_pid"]
    )
    df["lga_pid"] = df["subpopulation"].map(lga_lookup)

    return df


def wrangle_food_insecurity(
    df: pd.DataFrame,
    vic_boundaries: pd.DataFrame,
    viclga_boundaries: pd.DataFrame,
) -> pd.DataFrame:
    """Main wrangling pipeline for the food insecurity data.

    Args:
        df: Raw food insecurity Excel data.
        vic_boundaries: Wrangled vic_boundaries DataFrame (must contain
            ``ufi`` and ``vicgov_region`` columns).
        viclga_boundaries: Wrangled viclga_boundaries DataFrame (must contain
            ``lga_name`` and ``lga_pid`` columns).
    """
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
    df = add_region_ids(df, vic_boundaries, viclga_boundaries)

    return df
