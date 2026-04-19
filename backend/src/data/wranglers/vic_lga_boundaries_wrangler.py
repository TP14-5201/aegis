import pandas as pd

from .utils import initial_cleaning_pipeline


def select_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df[["lg_ply_pid", "lga_pid", "abb_name", "geometry"]]
    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={
        "lg_ply_pid": "lga_ply_pid",
        "abb_name": "lga_name"
    })
    return df


def wrangle_viclga_boundaries(df: pd.DataFrame) -> pd.DataFrame:
    df = initial_cleaning_pipeline(df)
    df = select_columns(df)
    df = rename_columns(df)

    return df