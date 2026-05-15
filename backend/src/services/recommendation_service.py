"""
recommendation_service.py
-------------------------
Deterministic value-based ingredient ranking for the get-food planner.

rec_score = 0.50 × affordability + 0.30 × health + 0.20 × nutrient_density

affordability:    0.6 × absolute budget fit + 0.4 × relative-to-sub_category-median fit
health:           Nutri-Score grade value (A=1.0 … E=0.2) minus NOVA deduction
nutrient_density: (protein_g/30 + fibre_g/10) / 2, capped at 1.0

Hard veto: dietary incompatibility or price > 3× budget-per-dish-per-person → score = 0.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pandas as pd
from sqlalchemy.orm import Session

from src.models import Ingredient, IngredientHealthRating, IngredientNutrition
from src.services.ingredient_substitution import engine as _sub_engine

if TYPE_CHECKING:
    from src.services.personalisation_service import ShoppingPreferences

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Startup cache — populated by warm_percentiles(), None until then
# ---------------------------------------------------------------------------
_PERCENTILES: dict[str, dict[str, float]] | None = None

# ---------------------------------------------------------------------------
# Dietary restriction → exact sub_category names to veto
# Only 15 distinct sub_categories in the dataset — exact matching is safe.
# ---------------------------------------------------------------------------
_DIETARY_VETO: dict[str, set[str]] = {
    "vegetarian":  {"Seafood", "Poultry", "Beef & veal", "Pork", "Lamb", "Mince"},
    "vegan":       {"Seafood", "Poultry", "Beef & veal", "Pork", "Lamb", "Mince",
                    "Cheese", "Dairy", "Milk", "Eggs"},
    "dairy-free":  {"Cheese", "Dairy", "Milk"},
    "gluten-free": {"Packaged Breads", "Breakfast"},
    "halal":       {"Pork"},
}

# Nutri-Score grade → health value (0–1)
_NUTRISCORE_MAP: dict[str | None, float] = {
    "a": 1.0, "b": 0.8, "c": 0.6, "d": 0.4, "e": 0.2, None: 0.4,
}

# NOVA processing level → penalty subtracted from health value
_NOVA_DEDUCTION: dict[int | None, float] = {
    1: 0.00,
    2: 0.05,
    3: 0.15,
    4: 0.40,
    None: 0.10,
}

# Scoring weights — must sum to 1.0
_W_AFFORDABILITY = 0.50
_W_HEALTH        = 0.30
_W_NUTRIENT      = 0.20

# Nutrient badge thresholds (based on real dataset percentiles; fixed to avoid
# p25=0 noise on fibre and sugars columns)
_BADGE_THRESHOLDS: list[tuple[str, str, str, float]] = [
    # (badge_label, column, operator, threshold)
    ("High protein", "protein_g",  ">", 12.4),
    ("High fibre",   "fibre_g",    ">",  3.4),
    ("Low fat",      "fat_g",      "<",  3.0),
    ("Low sugar",    "sugars_g",   "<",  5.0),
]

# nutrient_priorities values → internal DataFrame column names
_NUTRIENT_PRIORITY_COLS: dict[str, str] = {
    "protein_g":      "protein_g",
    "fibre_g":        "fibre_g",
    "fat_total_g":    "fat_g",
    "total_sugars_g": "sugars_g",
}


# ---------------------------------------------------------------------------
# Startup helper
# ---------------------------------------------------------------------------

def warm_percentiles(db: Session) -> None:
    """Compute and cache dataset-wide nutrient percentiles. Called once at startup."""
    global _PERCENTILES
    df = _load_ingredients_df(db)
    _PERCENTILES = {
        "protein_g":      {"p25": float(df["protein_g"].quantile(0.25)),
                           "p75": float(df["protein_g"].quantile(0.75))},
        "fibre_g":        {"p25": float(df["fibre_g"].quantile(0.25)),
                           "p75": float(df["fibre_g"].quantile(0.75))},
        "fat_total_g":    {"p25": float(df["fat_g"].quantile(0.25)),
                           "p75": float(df["fat_g"].quantile(0.75))},
        "total_sugars_g": {"p25": float(df["sugars_g"].quantile(0.25)),
                           "p75": float(df["sugars_g"].quantile(0.75))},
    }
    logger.info("Nutrient percentile cache warmed: %s", _PERCENTILES)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _dietary_vetoed(sub_category: str, dietary_needs: list[str]) -> bool:
    for need in dietary_needs:
        key = need.lower().strip()
        vetoed = _DIETARY_VETO.get(key, set())
        if sub_category in vetoed:
            return True
    return False


def _load_ingredients_df(db: Session) -> pd.DataFrame:
    rows = (
        db.query(
            Ingredient.ingredient_code,
            Ingredient.product_name,
            Ingredient.sub_category,
            Ingredient.retail_price,
            IngredientHealthRating.nutriscore_grade,
            IngredientHealthRating.nova_score,
            IngredientHealthRating.final_health_score,
            IngredientNutrition.protein_g,
            IngredientNutrition.total_dietary_fibre_g.label("fibre_g"),
            IngredientNutrition.fat_total_g.label("fat_g"),
            IngredientNutrition.total_sugars_g.label("sugars_g"),
        )
        .outerjoin(IngredientHealthRating,
                   Ingredient.ingredient_code == IngredientHealthRating.ingredient_code)
        .outerjoin(IngredientNutrition,
                   Ingredient.ingredient_code == IngredientNutrition.ingredient_code)
        .all()
    )

    df = pd.DataFrame(rows, columns=[
        "ingredient_code", "product_name", "sub_category", "retail_price",
        "nutriscore_grade", "nova_score", "final_health_score",
        "protein_g", "fibre_g", "fat_g", "sugars_g",
    ])
    df = df[df["retail_price"].notna() & (df["retail_price"] > 0)].reset_index(drop=True)
    return df


def _compute_rec_score(
    row: pd.Series,
    price_cap: float,
    cat_median_prices: dict[str, float],
    dietary_needs: list[str],
) -> float:
    sub_cat = str(row.get("sub_category") or "")
    price   = float(row["retail_price"])

    if _dietary_vetoed(sub_cat, dietary_needs):
        return 0.0

    if price > price_cap:
        return 0.0

    price_abs = max(0.0, 1.0 - price / max(price_cap, 0.01))
    median    = cat_median_prices.get(sub_cat, price) or price
    price_rel = max(0.0, 1.0 - price / max(median, 0.01))
    affordability = 0.6 * price_abs + 0.4 * price_rel

    grade      = (row.get("nutriscore_grade") or "").lower() or None
    health_base = _NUTRISCORE_MAP.get(grade, _NUTRISCORE_MAP[None])
    nova        = row.get("nova_score")
    try:
        nova_val = int(nova) if nova is not None and not pd.isna(nova) else None
    except (TypeError, ValueError):
        nova_val = None
    health = max(0.0, health_base - _NOVA_DEDUCTION.get(nova_val, _NOVA_DEDUCTION[None]))

    protein  = float(row.get("protein_g") or 0.0)
    fibre    = float(row.get("fibre_g") or 0.0)
    nutrient = min(1.0, (protein / 30.0 + fibre / 10.0) / 2.0)

    return _W_AFFORDABILITY * affordability + _W_HEALTH * health + _W_NUTRIENT * nutrient


def _compute_nutrient_badges(row: pd.Series) -> list[str]:
    badges = []
    for label, col, op, threshold in _BADGE_THRESHOLDS:
        val = float(row.get(col) or 0.0)
        if op == ">" and val > threshold:
            badges.append(label)
        elif op == "<" and val < threshold:
            badges.append(label)
    return badges


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def score_ingredients(
    db: Session,
    budget: float,
    people: int,
    days: int,
    dietary_needs: list[str],
) -> pd.DataFrame:
    """Score all ingredients and return DataFrame sorted by rec_score descending.

    Columns returned include: all ingredient fields + rec_score + nutrient_badges.
    """
    df = _load_ingredients_df(db)
    price_cap = budget / 5.0
    cat_median_prices = df.groupby("sub_category")["retail_price"].median().to_dict()

    df["rec_score"] = df.apply(
        _compute_rec_score,
        axis=1,
        price_cap=price_cap,
        cat_median_prices=cat_median_prices,
        dietary_needs=dietary_needs,
    )
    df["nutrient_badges"] = df.apply(_compute_nutrient_badges, axis=1)
    return df.sort_values("rec_score", ascending=False).reset_index(drop=True)


def score_ingredients_with_preferences(
    db: Session,
    budget: float,
    people: int,
    days: int,
    dietary_needs: list[str],
    preferences: "ShoppingPreferences",
    description: str | None = None,
) -> pd.DataFrame:
    """Score ingredients and apply Claude-derived preference re-ranking.

    final_score = rec_score × 0.7 + preference_alignment × 0.3

    avoid_sub_categories are hard-filtered before scoring.
    Returns DataFrame with rec_score, nutrient_badges, preference_alignment,
    and final_score columns, sorted by final_score descending.
    """
    df = _load_ingredients_df(db)

    # Hard filter: avoid sub_categories
    avoid = [s.lower() for s in (preferences.get("avoid_sub_categories") or [])]
    if avoid:
        def _is_avoided(sub_cat: str) -> bool:
            text = (sub_cat or "").lower()
            return any(av in text or text in av for av in avoid)
        df = df[~df["sub_category"].apply(_is_avoided)].copy()

    price_cap = budget / 5.0
    cat_median_prices = df.groupby("sub_category")["retail_price"].median().to_dict()

    df["rec_score"] = df.apply(
        _compute_rec_score,
        axis=1,
        price_cap=price_cap,
        cat_median_prices=cat_median_prices,
        dietary_needs=dietary_needs,
    )
    df["nutrient_badges"] = df.apply(_compute_nutrient_badges, axis=1)

    # FAISS text similarity map: ingredient_code → normalised score [0, 1]
    similarity_map: dict[str, float] = {}
    if description:
        raw_sim = _sub_engine.find_similar_to_text(description, top_k=300)
        if raw_sim:
            max_sim = max(raw_sim.values()) or 1.0
            similarity_map = {k: v / max_sim for k, v in raw_sim.items()}

    preferred = [s.lower() for s in (preferences.get("preferred_sub_categories") or [])]
    nutrient_priorities = [
        p for p in (preferences.get("nutrient_priorities") or [])
        if p in _NUTRIENT_PRIORITY_COLS
    ]
    has_preferences = bool(preferred or nutrient_priorities or similarity_map)

    if not has_preferences:
        df["preference_alignment"] = 0.0
        df["final_score"] = df["rec_score"]
        return df.sort_values("final_score", ascending=False).reset_index(drop=True)

    threshold_map = {t[1]: t[3] for t in _BADGE_THRESHOLDS if t[2] == ">"}

    def _preference_alignment(row: pd.Series) -> float:
        score = 0.0

        # FAISS ingredient-level similarity (0.5 weight)
        faiss_score = similarity_map.get(row["ingredient_code"], 0.0)
        score += faiss_score * 0.5

        # Sub-category boost from Groq extraction (0.3 weight)
        sub_cat_text = (str(row.get("sub_category") or "")).lower()
        if preferred:
            matched = any(pref in sub_cat_text or sub_cat_text in pref for pref in preferred)
            score += 0.3 if matched else 0.0

        # Nutrient priority boost (0.2 weight split across priorities)
        if nutrient_priorities:
            boost_per = 0.2 / len(nutrient_priorities)
            for priority in nutrient_priorities:
                col = _NUTRIENT_PRIORITY_COLS[priority]
                if float(row.get(col) or 0.0) > threshold_map.get(col, 0.0):
                    score += boost_per

        return min(score, 1.0)

    df["preference_alignment"] = df.apply(_preference_alignment, axis=1)
    df["final_score"] = df["rec_score"] * 0.7 + df["preference_alignment"] * 0.3
    return df.sort_values("final_score", ascending=False).reset_index(drop=True)


def select_bag(
    scored: pd.DataFrame,
    bag_size: int = 15,
    max_per_category: int = 3,
    score_col: str = "rec_score",
) -> pd.DataFrame:
    """Return up to bag_size rows from a score-sorted DataFrame.

    No more than max_per_category rows share the same sub_category.
    The DataFrame must already be sorted by score_col descending.
    """
    per_cat: dict[str, int] = {}
    rows = []
    for _, row in scored.iterrows():
        cat = row["sub_category"] or ""
        if per_cat.get(cat, 0) < max_per_category:
            rows.append(row)
            per_cat[cat] = per_cat.get(cat, 0) + 1
        if len(rows) >= bag_size:
            break
    return pd.DataFrame(rows).reset_index(drop=True)
