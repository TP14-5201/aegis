import pandas as pd

from .utils import initial_cleaning_pipeline, select_columns, rename_columns


def _capitalise_country(df: pd.DataFrame) -> pd.DataFrame:
    df["cuisine"] = df["cuisine"].str.capitalize()
    return df

def wrangle_recipe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare price dataset."""
    df = initial_cleaning_pipeline(df)
    df = _capitalise_country(df)
    df = select_columns(df, included_cols=["id", "cuisine"])
    df = df.drop_duplicates()
    df = df.sort_values(by="cuisine")
    df = rename_columns(df, cols_rename_map={"id": "recipe_id", "cuisine": "country"})
    return df