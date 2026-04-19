import pandas as pd

from .utils import initial_cleaning_pipeline, select_columns, rename_columns


def wrangle_viclga_boundaries(df: pd.DataFrame) -> pd.DataFrame:
    """Main wrangling pipeline for VIC LGA SA4 boundaries data."""
    VICLGA_COLUMN_MAP = {
        "lg_ply_pid": "lga_ply_pid",
        "abb_name": "lga_name"
    }
    VICLGA_INCLUED_COLS = ["lga_ply_pid", "lga_pid", "lga_name", "geometry"]

    df = initial_cleaning_pipeline(df)
    df = rename_columns(df, VICLGA_COLUMN_MAP)
    df = select_columns(df, VICLGA_INCLUED_COLS)

    return df