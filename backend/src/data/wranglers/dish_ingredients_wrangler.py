import pandas as pd

from .utils import initial_cleaning_pipeline, clean_na_values


def coerce_quantity(df: pd.DataFrame) -> pd.DataFrame:
    """Ensures quantity_g is numeric."""
    df["quantity_g"] = pd.to_numeric(df["quantity_g"], errors="coerce")
    return df


def coerce_is_optional(df: pd.DataFrame) -> pd.DataFrame:
    """Normalises is_optional to a Python bool."""
    df["is_optional"] = df["is_optional"].astype(str).str.strip().str.lower().map(
        {"true": True, "false": False, "1": True, "0": False}
    ).fillna(False)
    return df


def wrangle_dish_ingredients(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a name-keyed DataFrame.

    dish_name and ingredient_name are resolved to dish_id / ingredient_id
    by the seeder after parent tables are written to the database.
    """
    df = initial_cleaning_pipeline(df)
    df = coerce_quantity(df)
    df = coerce_is_optional(df)
    df = clean_na_values(df)
    return df
