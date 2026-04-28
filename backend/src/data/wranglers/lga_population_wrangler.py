import pandas as pd

from src.core.config import settings
from .utils import initial_cleaning_pipeline, rename_columns, select_columns


def filter_victorian_lga_population(df: pd.DataFrame) -> pd.DataFrame:
    """Filter the LGA population dataset to include only Victorian LGAs."""
    df = df[df["state_and_territory_2021_name"] == "Victoria"]
    return df


def filter_non_lga_population(df: pd.DataFrame) -> pd.DataFrame:
    """Filter out non-LGA population records."""
    df = df[~df["local_government_areas_2021_code"].isin(["29499", "29799"])]
    return df


def wrangle_lga_population(df: pd.DataFrame) -> pd.DataFrame:
    """Wrangle the LGA population dataset."""
    LGA_POPULATION_COLS = [
        "local_government_areas_2021_code",
        "local_government_areas_2021_name",
        "estimated_resident_population_persons_no_data_year_2024",
    ]

    LGA_POPULATION_COL_MAPPING = {
        "local_government_areas_2021_code": "lga_pid",
        "local_government_areas_2021_name": "lga_name",
        "estimated_resident_population_persons_no_data_year_2024": "pop_2024_total",
    }

    df = initial_cleaning_pipeline(df)
    df = filter_victorian_lga_population(df)
    df = filter_non_lga_population(df)
    df = select_columns(df, LGA_POPULATION_COLS)
    df = rename_columns(df, LGA_POPULATION_COL_MAPPING)
    return df   