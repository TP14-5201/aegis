"""Matches ingredient names against the OpenNutrition dataset and writes:

  src/data/raw/ingredient_nutrients_raw.csv
      ingredient_name, nutrient_name, amount_per_100g, unit

  src/data/raw/ingredients_pricing_raw.csv  (updated in-place)
      Adds / overwrites the benefit_tags column.

Run once before seeding (called automatically by data_seeding.py):
    python -m src.scripts.fetch_usda_nutrients
"""

import difflib
import json
import re

import pandas as pd

from src.core.config import settings
from src.core.logging import logger
from src.core.nutrition import NUTRIENT_BENEFIT_MAP, NRV_PER_100G
from src.scripts.download_dev_data import fetch_opennutrition

# OpenNutrition TSV column → canonical nutrient name used in DB
# Column names are detected at runtime; this map covers common variants.
_TSV_NUTRIENT_MAP: dict[str, str] = {
    "protein":                  "protein",
    "proteins":                 "protein",
    "carbohydrate":             "carbohydrate",
    "carbohydrates":            "carbohydrate",
    "carbohydrate_":            "carbohydrate",
    "fat":                      "total_fat",
    "fats":                     "total_fat",
    "total_fat":                "total_fat",
    "energy_kcal":              "energy_kcal",
    "energy-kcal":              "energy_kcal",
    "energykcal":               "energy_kcal",
    "iron":                     "iron",
    "calcium":                  "calcium",
    "vitamin_c":                "vitamin_c",
    "vitaminc":                 "vitamin_c",
    "vitamin-c":                "vitamin_c",
    "vitamin_d":                "vitamin_d",
    "vitamind":                 "vitamin_d",
    "vitamin-d":                "vitamin_d",
    "zinc":                     "zinc",
    "magnesium":                "magnesium",
    "potassium":                "potassium",
    "vitamin_b12":              "vitamin_b12",
    "vitamin-b12":              "vitamin_b12",
    "vitaminb12":               "vitamin_b12",
    "vitamin_b6":               "vitamin_b6",
    "vitamin-b6":               "vitamin_b6",
    "vitaminb6":                "vitamin_b6",
    "folate":                   "folate",
    "omega_3":                  "omega_3_polyunsaturated",
    "omega-3":                  "omega_3_polyunsaturated",
    "omega3":                   "omega_3_polyunsaturated",
    "omega_3_fat":              "omega_3_polyunsaturated",
    "omega-3-fat":              "omega_3_polyunsaturated",
}

_QTY_RE = re.compile(r"\b\d[\d.,]*\s*(g|kg|ml|l|mg|mcg|iu)?\b", re.IGNORECASE)


def _normalize(name: str) -> str:
    name = _QTY_RE.sub("", name.lower())
    return " ".join(name.split()).strip()


def _detect_name_col(df: pd.DataFrame) -> str:
    candidates = ["name", "product_name", "food_name", "item_name", "description", "product", "title"]
    cols_lower = {c.lower().strip(): c for c in df.columns}
    for cand in candidates:
        if cand in cols_lower:
            return cols_lower[cand]
    str_cols = df.select_dtypes(include="object").columns.tolist()
    avg_len = {c: df[c].dropna().astype(str).str.len().mean() for c in str_cols}
    return max(avg_len, key=avg_len.get)


def _map_nutrient_columns(df: pd.DataFrame) -> dict[str, str]:
    """Returns {tsv_column: canonical_name} for flat nutrient columns present in df."""
    mapped = {}
    for col in df.columns:
        key = col.lower().strip().replace(" ", "_")
        if key in _TSV_NUTRIENT_MAP:
            mapped[col] = _TSV_NUTRIENT_MAP[key]
    return mapped


def _nutrients_from_json_col(row: pd.Series) -> dict[str, float]:
    """Extract nutrients from OpenNutrition's nutrition_100g JSON column."""
    raw = row.get("nutrition_100g")
    if raw is None or (isinstance(raw, float)):
        return {}
    try:
        data = json.loads(raw) if isinstance(raw, str) else raw
    except (json.JSONDecodeError, TypeError):
        return {}
    if not isinstance(data, dict):
        return {}
    result = {}
    for key, val in data.items():
        canonical_key = key.lower().strip().replace(" ", "_").replace("-", "_")
        canonical = _TSV_NUTRIENT_MAP.get(canonical_key)
        if canonical:
            try:
                result[canonical] = float(val)
            except (TypeError, ValueError):
                pass
    return result


def _compute_benefit_tags(nutrients: dict[str, float]) -> list[str]:
    """Returns up to 2 distinct ChildBenefit tags ordered by highest % NRV contribution."""
    scored: list[tuple[float, str]] = []
    for canonical, amount in nutrients.items():
        nrv = NRV_PER_100G.get(canonical)
        if nrv and nrv > 0 and canonical in NUTRIENT_BENEFIT_MAP:
            scored.append((amount / nrv, NUTRIENT_BENEFIT_MAP[canonical]))
    scored.sort(key=lambda x: x[0], reverse=True)
    seen: list[str] = []
    for _, tag in scored:
        if tag not in seen:
            seen.append(tag)
        if len(seen) == 2:
            break
    return seen if seen else ["Energy"]


def run() -> None:
    # Ensure OpenNutrition TSV is downloaded
    fetch_opennutrition()

    logger.info(f"Loading OpenNutrition TSV from {settings.OPENNUTRITION_TSV_PATH} ...")
    df_nutrition = pd.read_csv(settings.OPENNUTRITION_TSV_PATH, sep="\t", low_memory=False)
    logger.info(f"OpenNutrition loaded: {len(df_nutrition)} rows, columns: {df_nutrition.columns.tolist()[:10]}...")

    name_col_nutrition = _detect_name_col(df_nutrition)
    nutrient_col_map = _map_nutrient_columns(df_nutrition)
    has_json_col = "nutrition_100g" in df_nutrition.columns
    logger.info(
        f"Name column: '{name_col_nutrition}' | "
        f"Flat nutrient columns: {list(nutrient_col_map.values())} | "
        f"JSON nutrition_100g column: {has_json_col}"
    )

    nutrition_names = df_nutrition[name_col_nutrition].dropna().astype(str).tolist()
    norm_nutrition = {_normalize(n): i for i, n in enumerate(nutrition_names)}
    norm_keys = list(norm_nutrition.keys())

    # Load ingredient names from pricing CSV
    pricing_df = pd.read_csv(settings.INGREDIENTS_PRICING_RAW_PATH)
    pricing_name_candidates = ["name", "item_name", "product_name", "product", "item"]
    pricing_name_col = next((c for c in pricing_name_candidates if c in pricing_df.columns), None)
    if not pricing_name_col:
        pricing_name_col = _detect_name_col(pricing_df)
    ingredient_names = pricing_df[pricing_name_col].dropna().unique().tolist()
    logger.info(f"Matching {len(ingredient_names)} ingredients against OpenNutrition ...")

    nutrient_rows: list[dict] = []
    benefit_tags_map: dict[str, str] = {}

    for i, ing_name in enumerate(ingredient_names):
        norm_ing = _normalize(ing_name)
        hits = difflib.get_close_matches(norm_ing, norm_keys, n=1, cutoff=0.45)
        if not hits:
            logger.warning(f"  [{i+1}/{len(ingredient_names)}] No match for '{ing_name}'")
            continue

        row_idx = norm_nutrition[hits[0]]
        row = df_nutrition.iloc[row_idx]
        nutrients: dict[str, float] = {}
        # Try flat columns first, fall back to nutrition_100g JSON column
        for col, canonical in nutrient_col_map.items():
            val = pd.to_numeric(row.get(col), errors="coerce")
            if pd.notna(val):
                nutrients[canonical] = float(val)
        if not nutrients and has_json_col:
            nutrients = _nutrients_from_json_col(row)

        benefit_tags = _compute_benefit_tags(nutrients)
        benefit_tags_map[ing_name] = json.dumps(benefit_tags)

        for canonical, amount in nutrients.items():
            nutrient_rows.append({
                "ingredient_name": ing_name,
                "nutrient_name":   canonical,
                "amount_per_100g": amount,
                "unit":            "g",
            })

        logger.info(f"  [{i+1}/{len(ingredient_names)}] '{ing_name}' → matched '{nutrition_names[row_idx]}' | tags={benefit_tags}")

    nutrients_df = pd.DataFrame(nutrient_rows)
    nutrients_df.to_csv(settings.INGREDIENT_NUTRIENTS_RAW_PATH, index=False)
    logger.info(f"Wrote {len(nutrients_df)} nutrient rows to {settings.INGREDIENT_NUTRIENTS_RAW_PATH}")

    pricing_df["benefit_tags"] = pricing_df[pricing_name_col].map(benefit_tags_map)
    pricing_df.to_csv(settings.INGREDIENTS_PRICING_RAW_PATH, index=False)
    logger.info(f"Updated {settings.INGREDIENTS_PRICING_RAW_PATH} with benefit_tags.")


if __name__ == "__main__":
    run()
