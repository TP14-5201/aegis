import pandas as pd
from tqdm import tqdm

from src.core.logging import logger


# Official Nutri-Score negative point thresholds (solid foods)
_ENERGY_KJ_THRESHOLDS  = [335, 670, 1005, 1340, 1675, 2010, 2345, 2680, 3015, 3350]
_SAT_FAT_THRESHOLDS    = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
_SUGARS_THRESHOLDS     = [4.5, 9, 13.5, 18, 22.5, 27, 31, 36, 40, 45]
_SODIUM_THRESHOLDS     = [90, 180, 270, 360, 450, 540, 630, 720, 810, 900]

# Official Nutri-Score positive point thresholds
_FIBRE_THRESHOLDS      = [0.9, 1.9, 2.8, 3.7, 4.7]
_PROTEIN_THRESHOLDS    = [1.6, 3.2, 4.8, 6.4, 8.0]

# Final score → grade (solid foods); score range: -10 (healthiest) to 40 (least healthy)
_GRADE_THRESHOLDS = [(-1, "A"), (2, "B"), (10, "C"), (18, "D")]

# Normalise raw score [-10, 40] → [100, 0]
_SCORE_MIN = -10.0
_SCORE_MAX = 40.0


def _points(value: float, thresholds: list) -> int:
    for i, threshold in enumerate(thresholds):
        if value <= threshold:
            return i
    return len(thresholds)


def _grade(score: int) -> str:
    for threshold, letter in _GRADE_THRESHOLDS:
        if score <= threshold:
            return letter
    return "E"


def _score_to_100(raw: int) -> float:
    normalised = (raw - _SCORE_MIN) / (_SCORE_MAX - _SCORE_MIN)
    return round(max(0.0, min(100.0, (1.0 - normalised) * 100.0)), 1)


def compute_nutriscore(
    protein_g: float,
    fat_total_g: float,
    fibre_g: float,
    sugars_g: float,
    sodium_mg: float,
    carb_g: float,
) -> dict:
    """Compute Nutri-Score grade, raw score, and 0–100 health score from nutrition values.

    All inputs are per 100g. Uses the official FSA nutrient profiling algorithm with
    two proxies for missing columns:
      - Saturated fat: estimated as 35% of total fat
      - Energy (kJ): estimated from macros using Atwater factors (protein×17 + fat×37 + carb×17)
    """
    sat_fat_g = fat_total_g * 0.35
    energy_kj = (protein_g * 17.0) + (fat_total_g * 37.0) + (carb_g * 17.0)

    n_total = (
        _points(energy_kj, _ENERGY_KJ_THRESHOLDS)
        + _points(sat_fat_g, _SAT_FAT_THRESHOLDS)
        + _points(sugars_g,  _SUGARS_THRESHOLDS)
        + _points(sodium_mg, _SODIUM_THRESHOLDS)
    )
    p_total = _points(fibre_g, _FIBRE_THRESHOLDS) + _points(protein_g, _PROTEIN_THRESHOLDS)

    raw_score = n_total - p_total
    return {
        "nutriscore_grade":   _grade(raw_score),
        "nutriscore_score":   raw_score,
        "final_health_score": _score_to_100(raw_score),
    }


def wrangle_ingredient_health_ratings(
    ingredient_df: pd.DataFrame,
    nutrition_df: pd.DataFrame,
) -> pd.DataFrame:
    """Build a health rating row for every ingredient using the Nutri-Score algorithm.

    Merges ingredient and nutrition data, computes Nutri-Score from AFCD nutrition
    columns, and returns a DataFrame ready for bulk insert into ingredient_health_rating.
    Ingredients with no matched nutrition data receive all-zero inputs (mid-range score).
    """
    nutrition_cols = [
        "ingredient_code",
        "protein_g",
        "fat_total_g",
        "total_dietary_fibre_g",
        "total_sugars_g",
        "available_carbohydrate_without_sugar_alcohols_g",
        "sodium_na_mg",
    ]

    merged = ingredient_df[["ingredient_code"]].merge(
        nutrition_df[nutrition_cols], on="ingredient_code", how="left",
    ).fillna(0)

    logger.info("Computing Nutri-Score for %d ingredients...", len(merged))

    records = []
    for _, row in tqdm(merged.iterrows(), total=len(merged), desc="Nutri-Score computation"):
        result = compute_nutriscore(
            protein_g   = float(row["protein_g"]),
            fat_total_g = float(row["fat_total_g"]),
            fibre_g     = float(row["total_dietary_fibre_g"]),
            sugars_g    = float(row["total_sugars_g"]),
            sodium_mg   = float(row["sodium_na_mg"]),
            carb_g      = float(row["available_carbohydrate_without_sugar_alcohols_g"]),
        )
        records.append({
            "ingredient_code":       row["ingredient_code"],
            "nutriscore_grade":      result["nutriscore_grade"],
            "nutriscore_score":      result["nutriscore_score"],
            "nova_score":            None,
            "computed_health_score": result["final_health_score"],
            "final_health_score":    result["final_health_score"],
            "health_source":         "computed",
        })

    grade_counts: dict[str, int] = {}
    for r in records:
        g = r["nutriscore_grade"]
        grade_counts[g] = grade_counts.get(g, 0) + 1
    logger.info("Nutri-Score distribution: %s", dict(sorted(grade_counts.items())))

    return pd.DataFrame(records)
