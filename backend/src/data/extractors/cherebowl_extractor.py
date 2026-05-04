"""ChereBowl dataset extractors.

Each public function downloads a Kaggle dataset via kagglehub and returns a
pandas DataFrame, matching the same contract as support_services_extractor.py.

Authentication uses KAGGLE_USERNAME + KAGGLE_KEY from .env (no kaggle.json needed).
kagglehub caches downloads locally so subsequent runs don't re-download.
"""

import json
import os

import pandas as pd

from src.core.config import settings
from src.core.logging import logger


def _set_kaggle_env():
    """Exports Kaggle credentials as env vars so kagglehub picks them up."""
    username = settings.KAGGLE_USERNAME
    key = settings.KAGGLE_KEY
    if not username or not key:
        raise ValueError(
            "KAGGLE_USERNAME and KAGGLE_KEY must be set in .env. "
            "Generate an API key at https://www.kaggle.com/settings → API → Create New Token."
        )
    os.environ["KAGGLE_USERNAME"] = username
    os.environ["KAGGLE_KEY"] = key


def _load(slug: str, file_path: str = "") -> pd.DataFrame:
    """Loads a Kaggle dataset file directly into a DataFrame via kagglehub."""
    import kagglehub
    from kagglehub import KaggleDatasetAdapter
    _set_kaggle_env()
    logger.info(f"Fetching Kaggle dataset: {slug}" + (f" ({file_path})" if file_path else ""))
    return kagglehub.load_dataset(KaggleDatasetAdapter.PANDAS, slug, file_path)


# ---------------------------------------------------------------------------
# Dataset-specific fetchers
# ---------------------------------------------------------------------------

def fetch_yummly_dishes() -> pd.DataFrame:
    """Fetches kaggle/recipe-ingredients-dataset (Yummly 'What's Cooking').

    Source: train.json — each record has {id, cuisine, ingredients: [...]}.
    Ingredients list is serialised to a JSON string so it survives CSV round-trips.
    """
    df = _load(settings.YUMMLY_DISHES_DATASET, file_path="train.json")
    if "ingredients" in df.columns:
        df["ingredients"] = df["ingredients"].apply(
            lambda v: json.dumps(v) if isinstance(v, list) else v
        )
    return df


def fetch_miskg_substitutes() -> pd.DataFrame:
    """Fetches only substitution_pairs.json from the MISKG dataset.

    Uses kagglehub file_path to pull just that file, avoiding the full ~27GB download.
    Returns a DataFrame with columns: ingredient_name, substitute_name,
    similarity_score, reason, source.
    """
    df = _load(settings.MISKG_SUBSTITUTES_DATASET, file_path="substitution_pairs.json")

    rename_map = {}
    if "ingredient" in df.columns:
        rename_map["ingredient"] = "ingredient_name"
    if "substitution" in df.columns:
        rename_map["substitution"] = "substitute_name"
    if rename_map:
        df = df.rename(columns=rename_map)

    if "similarity_score" not in df.columns:
        df["similarity_score"] = None
    if "reason" not in df.columns:
        df["reason"] = None

    df["source"] = "MISKG"

    keep = ["ingredient_name", "substitute_name", "similarity_score", "reason", "source"]
    return df[[c for c in keep if c in df.columns]]
