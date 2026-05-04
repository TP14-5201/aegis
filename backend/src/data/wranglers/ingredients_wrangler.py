import json
from datetime import datetime

import pandas as pd

from .utils import initial_cleaning_pipeline, add_source_column, clean_na_values

# Snapshot date for thedevastator/grocery-product-prices-for-australian-states
_KAGGLE_SNAPSHOT_DATE = "2022-09-01"
_KAGGLE_PRICE_SOURCE = "open_food_facts"


def rename_size_price_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalises varied column names from the pricing CSV to standard names."""
    rename_map: dict[str, str] = {}
    for col in df.columns:
        cl = col.lower()
        if cl in ("pack_size_g", "size_g", "weight_g", "grams"):
            rename_map[col] = "pack_grams"
        elif cl in ("pack_price_aud", "price", "price_aud"):
            rename_map[col] = "price_aud"
        elif cl == "package_price" and "price_per_100g" not in df.columns:
            rename_map[col] = "price_per_100g"
    if rename_map:
        df = df.rename(columns=rename_map)
    return df


def pick_lower_price(df: pd.DataFrame) -> pd.DataFrame:
    """Selects the lower of Coles/Woolworths price where both columns exist.

    Falls back gracefully to whatever numeric column is available.
    """
    coles = next((c for c in df.columns if "coles" in c.lower()), None)
    woolworths = next((c for c in df.columns if "woolworths" in c.lower() or "woolies" in c.lower()), None)
    if coles and woolworths:
        df[coles] = pd.to_numeric(df[coles], errors="coerce")
        df[woolworths] = pd.to_numeric(df[woolworths], errors="coerce")
        df["price_aud"] = df[[coles, woolworths]].min(axis=1)
    elif "price_aud" not in df.columns:
        # Last resort: take first numeric column
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if numeric_cols:
            df["price_aud"] = df[numeric_cols[0]]
    return df


def compute_price_per_100g(df: pd.DataFrame) -> pd.DataFrame:
    """Derives price_per_100g from price_aud / pack_grams.

    Skipped when price_per_100g is already populated (e.g. from a pre-computed
    package_price column in the source dataset).
    """
    if "pack_grams" in df.columns:
        df["pack_grams"] = pd.to_numeric(df["pack_grams"], errors="coerce")
    if "price_aud" in df.columns:
        df["price_aud"] = pd.to_numeric(df["price_aud"], errors="coerce")
    if "price_per_100g" in df.columns and df["price_per_100g"].notna().any():
        df["price_per_100g"] = pd.to_numeric(df["price_per_100g"], errors="coerce")
        return df
    pack_size = df["pack_grams"].replace(0, float("nan")) if "pack_grams" in df.columns else float("nan")
    df["price_per_100g"] = (df["price_aud"] / pack_size * 100).round(4)
    return df


def generate_pack_label(df: pd.DataFrame) -> pd.DataFrame:
    """Creates a human-readable pack_label from pack_grams (e.g. '500g pack', '1 kg bag').

    If a pack_label column already exists in the source data it is kept as-is.
    """
    if "pack_label" in df.columns:
        return df

    def _label(grams):
        if pd.isna(grams) or grams <= 0:
            return "1 pack"
        g = float(grams)
        if g >= 1000:
            kg = g / 1000
            kg_str = f"{kg:.0f}" if kg == int(kg) else f"{kg:.1f}"
            return f"{kg_str} kg"
        return f"{int(g)}g pack"

    df["pack_label"] = df["pack_grams"].apply(_label)
    return df


def add_pricing_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """Adds price_source and price_as_of from the Kaggle snapshot.

    Uses the DATE column from the dataset if available (format dd.mm.yyyy),
    otherwise falls back to the hardcoded snapshot constant.
    """
    if "price_source" not in df.columns:
        df["price_source"] = _KAGGLE_PRICE_SOURCE
    if "price_as_of" not in df.columns:
        df["price_as_of"] = _KAGGLE_SNAPSHOT_DATE
    return df


def add_nullable_usda_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Ensures benefit_tags column exists as a JSON array placeholder.

    Populated later by fetch_usda_nutrients.py.
    Handles the legacy single-value 'benefit_tag' column by wrapping it.
    """
    if "benefit_tags" not in df.columns:
        if "benefit_tag" in df.columns:
            df["benefit_tags"] = df["benefit_tag"].apply(
                lambda v: json.dumps([v]) if pd.notna(v) and v else None
            )
            df = df.drop(columns=["benefit_tag"])
        else:
            df["benefit_tags"] = None
    return df


def wrangle_ingredients(df: pd.DataFrame) -> pd.DataFrame:
    df = initial_cleaning_pipeline(df)
    # Normalise the product name column to "name" regardless of source column header
    for candidate in ("item_name", "product_name", "product", "item", "description", "title"):
        if candidate in df.columns and "name" not in df.columns:
            df = df.rename(columns={candidate: "name"})
            break
    df = rename_size_price_columns(df)
    df = pick_lower_price(df)
    df = compute_price_per_100g(df)
    df = generate_pack_label(df)
    df = add_pricing_metadata(df)
    df = add_nullable_usda_columns(df)
    if "source" not in df.columns:
        df = add_source_column(df, _KAGGLE_PRICE_SOURCE)
    # Preserve category columns if the source data provided them
    for col in ("category", "sub_category", "pack_grams"):
        if col in df.columns:
            df[col] = df[col]
    df = clean_na_values(df)
    return df
