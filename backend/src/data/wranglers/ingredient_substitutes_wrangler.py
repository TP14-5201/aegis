import pandas as pd

from .utils import initial_cleaning_pipeline, add_source_column, clean_na_values


def coerce_similarity_score(df: pd.DataFrame) -> pd.DataFrame:
    """Clamps similarity_score to [0, 1] range."""
    df["similarity_score"] = pd.to_numeric(df["similarity_score"], errors="coerce").clip(0, 1)
    return df


def wrangle_ingredient_substitutes(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a name-keyed DataFrame.

    ingredient_name and substitute_name are resolved to ingredient_id /
    substitute_id by the seeder after the ingredients table is written.
    """
    if df.empty or len(df.dropna(how="all")) == 0:
        return pd.DataFrame(columns=["ingredient_name", "substitute_name", "similarity_score", "reason", "source"])

    df = initial_cleaning_pipeline(df)
    df = coerce_similarity_score(df)
    if "source" not in df.columns:
        df = add_source_column(df, "manual")
    df = clean_na_values(df)
    return df
