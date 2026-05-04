"""Pre-computes dish→ingredient mappings using Food2Vec semantic matching.

Reads dishes_raw.csv (Yummly recipes) and ingredients_pricing_raw.csv
(Coles/VIC grocery products), semantically matches each recipe ingredient
to the closest grocery product, and writes dish_ingredients_raw.csv.

This script runs OFFLINE (once, or whenever the ingredient DB changes).
The output is seeded into the dish_ingredients table so runtime queries
are plain DB joins with no ML inference.

Usage:
    python -m src.scripts.fetch_dish_ingredients
"""

from __future__ import annotations

import json
import os
import re

import pandas as pd

from src.core.config import settings
from src.core.logging import logger
from src.data.wranglers.dishes_wrangler import _CUISINE_LABELS, _top_ingredients
from src.services.embedding import food2vec, _tokenize

_QTY_PATTERN = re.compile(
    r"^\s*[\d/½¼¾⅓⅔]+\s*(cup|c\.|tbsp|tsp|tablespoon|teaspoon|oz|lb|g|kg|ml|l"
    r"|pound|ounce|clove|head|bunch|slice|can|jar|pkg|package|medium|large|small"
    r"|piece|pinch|dash|handful)s?\s*",
    re.IGNORECASE,
)

_BRAND_TOKENS = {
    "coles", "woolworths", "aldi", "harris", "farm", "select",
    "rspca", "approved", "gluten", "free", "organic", "natural",
    "premium", "classic", "original", "traditional",
}
_UNIT_RE = re.compile(r"\b\d+(\.\d+)?\s*(g|kg|ml|l|pk|pack|x|ct|ea)\b", re.IGNORECASE)


def _normalize_recipe_ingredient(raw: str) -> str:
    raw = _QTY_PATTERN.sub("", raw).strip()
    tokens = _tokenize(raw)
    return " ".join(tokens).strip()


def _normalize_product_name(name: str) -> str:
    name = _UNIT_RE.sub("", name.lower())
    tokens = [t for t in name.split() if t not in _BRAND_TOKENS and len(t) > 1]
    return " ".join(tokens).strip()


def _detect_name_column(df: pd.DataFrame) -> str:
    candidates = ["name", "product", "product_name", "item", "item_name", "description"]
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand in cols_lower:
            return cols_lower[cand]
    str_cols = df.select_dtypes(include="object").columns.tolist()
    avg_len = {c: df[c].dropna().astype(str).str.len().mean() for c in str_cols}
    return max(avg_len, key=avg_len.get)


def generate_dish_ingredients(threshold: float = 0.60) -> None:
    """Match Yummly recipe ingredients to grocery products via Food2Vec, write CSV."""

    if not os.path.exists(settings.DISHES_RAW_PATH):
        logger.error("dishes_raw.csv not found — run download_dev_data.py first")
        return
    if not os.path.exists(settings.INGREDIENTS_PRICING_RAW_PATH):
        logger.error("ingredients_pricing_raw.csv not found — run download_dev_data.py first")
        return

    if food2vec.available:
        logger.info("Food2Vec model loaded — using semantic embedding matching")
    else:
        logger.warning("Food2Vec model not available — using token-overlap fallback")

    # ------------------------------------------------------------------ #
    # Load dishes                                                          #
    # ------------------------------------------------------------------ #
    df_dishes = pd.read_csv(settings.DISHES_RAW_PATH)
    df_dishes.columns = df_dishes.columns.str.strip().str.lower()

    cuisine_col = "cuisine" if "cuisine" in df_dishes.columns else None
    id_col = "id" if "id" in df_dishes.columns else None

    def _dish_name(row: pd.Series) -> str:
        cuisine_raw = str(row[cuisine_col]).lower() if cuisine_col else ""
        cuisine_label = _CUISINE_LABELS.get(
            cuisine_raw, cuisine_raw.replace("_", " ").title() or "Mixed"
        )
        top = _top_ingredients(row["ingredients"]) if "ingredients" in row.index else []
        if top:
            return f"{cuisine_label} {' & '.join(top)}"
        rid = str(int(row[id_col])) if id_col else str(row.name)
        return f"{cuisine_label} Dish {rid}"

    # Build (dish_name, raw_ingredient) pairs
    records = []
    for _, row in df_dishes.iterrows():
        name = _dish_name(row)
        try:
            ings = json.loads(row["ingredients"]) if isinstance(row["ingredients"], str) else row["ingredients"]
        except (json.JSONDecodeError, TypeError):
            continue
        if not isinstance(ings, list):
            continue
        for ing in ings:
            records.append({"dish_name": name, "raw_ingredient": str(ing)})

    if not records:
        logger.error("No ingredient records extracted from dishes_raw.csv")
        return

    df_pairs = pd.DataFrame(records)
    df_pairs["norm_ingredient"] = df_pairs["raw_ingredient"].apply(_normalize_recipe_ingredient)

    # ------------------------------------------------------------------ #
    # Load grocery products                                                #
    # ------------------------------------------------------------------ #
    df_pricing = pd.read_csv(settings.INGREDIENTS_PRICING_RAW_PATH)
    df_pricing.columns = df_pricing.columns.str.strip().str.lower()

    name_col = _detect_name_column(df_pricing)
    logger.info("Using '%s' as product name column", name_col)

    product_names: list[str] = df_pricing[name_col].dropna().astype(str).unique().tolist()
    # Build normalised → original mapping so we return the original product name
    norm_to_original: dict[str, str] = {_normalize_product_name(n): n for n in product_names}
    norm_products = list(norm_to_original.keys())

    # ------------------------------------------------------------------ #
    # Semantic batch match (all unique ingredient strings at once)         #
    # ------------------------------------------------------------------ #
    unique_norm = df_pairs["norm_ingredient"].dropna().unique().tolist()
    unique_norm = [n for n in unique_norm if n]

    logger.info(
        "Matching %d unique ingredient tokens against %d products (threshold=%.2f)...",
        len(unique_norm),
        len(norm_products),
        threshold,
    )

    norm_to_match = food2vec.batch_match(unique_norm, norm_products, threshold=threshold)

    # Map matched normalised product name back to original product name
    def _resolve(norm_ing: str) -> str | None:
        matched_norm = norm_to_match.get(norm_ing)
        if matched_norm is None:
            return None
        return norm_to_original.get(matched_norm)

    df_pairs["ingredient_name"] = df_pairs["norm_ingredient"].map(
        lambda n: _resolve(n) if n else None
    )

    total = len(df_pairs)
    matched = df_pairs["ingredient_name"].notna().sum()
    logger.info(
        "Matched %d / %d (%.1f%%) dish-ingredient pairs",
        matched, total, matched / total * 100 if total else 0,
    )

    # ------------------------------------------------------------------ #
    # Write output                                                         #
    # ------------------------------------------------------------------ #
    df_out = (
        df_pairs[df_pairs["ingredient_name"].notna()][["dish_name", "ingredient_name"]]
        .copy()
        .assign(quantity_g=None, is_optional=False)
        .drop_duplicates(subset=["dish_name", "ingredient_name"])
    )

    df_out.to_csv(settings.DISH_INGREDIENTS_RAW_PATH, index=False)
    logger.info(
        "dish_ingredients_raw.csv written: %d rows → %s",
        len(df_out),
        settings.DISH_INGREDIENTS_RAW_PATH,
    )


if __name__ == "__main__":
    generate_dish_ingredients()
