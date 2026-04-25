import pandas as pd

from .utils import initial_cleaning_pipeline, select_columns, rename_columns


def take_latest_lga_boundaries(df: pd.DataFrame) -> pd.DataFrame:
    """Take the latest LGA boundaries and drop duplicated ones."""
    df['dt_create'] = pd.to_datetime(df['dt_create'])
    df_latest = (
        df
            .sort_values('dt_create')
            .drop_duplicates(subset=['abb_name'], keep='last')
            .reset_index(drop=True)
    )
    return df_latest
    

def clean_lga_names(df: pd.DataFrame) -> pd.DataFrame:
    """Some LGA names have the postfix (Uninc) in them because they are not really part of Victorian LGA but included in the original data."""
    df["abb_name"] = df["abb_name"].str.split("(").str[0].str.strip()
    return df

def wrangle_viclga_boundaries(df: pd.DataFrame) -> pd.DataFrame:
    """Main wrangling pipeline for VIC LGA SA4 boundaries data."""
    VICLGA_COLUMN_MAP = {
        "lg_ply_pid": "lga_ply_pid",
        "abb_name": "lga_name"
    }
    VICLGA_INCLUED_COLS = ["lga_pid", "lga_name", "geometry"]

    df = initial_cleaning_pipeline(df)
    df = take_latest_lga_boundaries(df)
    df = clean_lga_names(df)
    df = rename_columns(df, VICLGA_COLUMN_MAP)
    df = select_columns(df, VICLGA_INCLUED_COLS)

    return df