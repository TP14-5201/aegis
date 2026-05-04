import pandas as pd

from .utils import initial_cleaning_pipeline, clean_na_values


def coerce_amount(df: pd.DataFrame) -> pd.DataFrame:
    """Ensures amount_per_100g is numeric."""
    df["amount_per_100g"] = pd.to_numeric(df["amount_per_100g"], errors="coerce")
    return df


def wrangle_ingredient_nutrients(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a name-keyed DataFrame.

    ingredient_name is resolved to ingredient_id by the seeder after
    the ingredients table is written to the database.
    Returns an empty DataFrame if the source file has no data rows yet
    (e.g. before fetch_usda_nutrients.py has been run).
    """
    if df.empty or len(df.dropna(how="all")) == 0:
        return pd.DataFrame(columns=["ingredient_name", "nutrient_name", "amount_per_100g", "unit"])

    df = initial_cleaning_pipeline(df)
    df = coerce_amount(df)
    df = clean_na_values(df)
    return df
