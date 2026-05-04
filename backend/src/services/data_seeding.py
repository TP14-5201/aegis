import json
import math
import os

import pandas as pd

from sqlalchemy.orm import Session
from src.database import SessionLocal, engine
from src.models import (
    Base, SupportService, FoodInsecurity,
    VicLgaBoundary, LgaPopulation,
    DietIndicator, HealthOutcome, LowCostDiet,
    LowCostDietHealthOutcome, RecommendedMacronutrientsIntake,
    Ingredient, Dish, DishIngredient, IngredientNutrient, IngredientSubstitute,
)

from src.core.config import settings
from src.core.logging import logger
from src.scripts.download_dev_data import save_local_copy
from src.scripts.fetch_vic_grocery_ingredients import fetch_vic_grocery_ingredients
from src.data.loaders.data_loader import (
    load_emergency_services_dataset,
    load_food_insecurity_dataset,
    load_lga_boundaries_dataset,
    load_lga_population_dataset,
    load_diet_indicator_dataset,
    load_health_outcome_dataset,
    load_low_cost_diet_dataset,
    load_low_cost_diet_health_outcome_dataset,
    load_recommended_macronutrients_intake_dataset,
    load_dishes_dataset,
    load_ingredients_dataset,
    load_dish_ingredients_dataset,
    load_ingredient_nutrients_dataset,
    load_ingredient_substitutes_dataset,
)


def seed_simple(db: Session, df: pd.DataFrame, model) -> None:
    """Clears and re-seeds a table using a direct column→field mapping.

    Suitable for tables whose columns map 1-to-1 to model attributes with no
    cross-table foreign-key resolution required.
    """
    logger.info(f"Seeding {model.__tablename__} with {len(df)} records...")
    records = df.to_dict(orient="records")
    try:
        db.query(model).delete()
        db.bulk_save_objects([model(**r) for r in records])
        db.commit()
        logger.info(f"  → {len(records)} rows inserted into {model.__tablename__}.")
    except Exception as exc:
        db.rollback()
        logger.error(f"Error seeding {model.__tablename__}: {exc}")
        raise


def seed_ingredients(db: Session, df: pd.DataFrame) -> dict[str, int]:
    """Seeds the ingredients table and returns a name→id lookup map.

    The lookup map is required by subsequent seeders that resolve foreign keys
    by ingredient name (nutrients, substitutes, dish-ingredients).
    """
    logger.info(f"Seeding ingredients with {len(df)} records...")
    db.query(Ingredient).delete()

    def _float(val):
        v = pd.to_numeric(val, errors="coerce")
        return None if (v is None or (isinstance(v, float) and math.isnan(v))) else float(v)

    name_to_id: dict[str, int] = {}
    for _, row in df.iterrows():
        benefit_tags = row.get("benefit_tags")
        if isinstance(benefit_tags, str):
            try:
                benefit_tags = json.loads(benefit_tags)
            except (json.JSONDecodeError, TypeError):
                benefit_tags = [benefit_tags]
        elif not isinstance(benefit_tags, list):
            benefit_tags = []

        obj = Ingredient(
            name=row.get("name"),
            pack_label=row.get("pack_label"),
            pack_grams=_float(row.get("pack_grams") or row.get("pack_size_g")),
            price_aud=_float(row.get("price_aud") or row.get("pack_price_aud")),
            price_per_100g=_float(row.get("price_per_100g")),
            price_source=row.get("price_source", "kaggle_supermarkets_2024"),
            price_as_of=row.get("price_as_of", "2024-01-01"),
            benefit_tags=benefit_tags,
            source=row.get("source", "kaggle_supermarkets_2024"),
        )
        db.add(obj)
        db.flush()  # assigns obj.id without committing
        if obj.name:
            name_to_id[obj.name.lower()] = obj.id

    db.commit()
    logger.info(f"  → {len(name_to_id)} ingredients inserted.")
    return name_to_id


_MEAT_TOKENS = {
    "chicken", "beef", "pork", "lamb", "turkey", "bacon", "ham", "sausage",
    "fish", "shrimp", "prawn", "salmon", "tuna", "anchovy", "pepperoni",
    "salami", "veal", "duck", "venison", "crab", "lobster", "mussel", "clam",
}
_DAIRY_TOKENS = {"milk", "cheese", "butter", "cream", "yogurt", "yoghurt", "ghee", "whey", "custard"}
_GLUTEN_TOKENS = {"flour", "wheat", "bread", "pasta", "noodle", "barley", "rye", "breadcrumb", "couscous", "semolina"}
_PORK_ALCOHOL_TOKENS = {"pork", "bacon", "ham", "lard", "wine", "beer", "alcohol", "brandy", "rum", "whiskey", "vodka", "sake"}


def _infer_dietary_flags(raw_ingredients: list) -> list[str]:
    flat = " ".join(str(i).lower() for i in raw_ingredients)
    tokens = set(flat.split())
    flags = []
    has_meat = bool(tokens & _MEAT_TOKENS)
    has_dairy = bool(tokens & _DAIRY_TOKENS)
    has_gluten = bool(tokens & _GLUTEN_TOKENS)
    has_pork_alcohol = bool(tokens & _PORK_ALCOHOL_TOKENS)
    if not has_meat:
        flags.append("vegetarian")
    if not has_meat and not has_dairy:
        flags.append("vegan")
    if not has_gluten:
        flags.append("gluten-free")
    if not has_dairy:
        flags.append("dairy-free")
    if not has_pork_alcohol:
        flags.append("halal")
    return flags


def seed_dishes(db: Session, df: pd.DataFrame) -> dict[str, int]:
    """Seeds the dishes table and returns a name→id lookup map."""
    logger.info(f"Seeding dishes with {len(df)} records...")
    db.query(Dish).delete()

    name_to_id: dict[str, int] = {}
    for _, row in df.iterrows():
        raw_ingredients = row.get("ingredients")
        if isinstance(raw_ingredients, str):
            try:
                raw_ingredients = json.loads(raw_ingredients)
            except (json.JSONDecodeError, TypeError):
                raw_ingredients = []
        if not isinstance(raw_ingredients, list):
            raw_ingredients = []

        obj = Dish(
            name=row.get("name"),
            cuisine=row.get("cuisine"),
            base_servings=int(row.get("base_servings", 4)),
            dietary_flags=_infer_dietary_flags(raw_ingredients),
            raw_ingredients=raw_ingredients,
            source=row.get("source", "yummly"),
        )
        db.add(obj)
        db.flush()
        if obj.name:
            name_to_id[obj.name.lower()] = obj.id

    db.commit()
    logger.info(f"  → {len(name_to_id)} dishes inserted.")
    return name_to_id


def seed_ingredient_nutrients(
    db: Session,
    df: pd.DataFrame,
    ingredient_name_to_id: dict[str, int],
) -> None:
    """Seeds ingredient_nutrients, resolving ingredient_name → FK id."""
    if df.empty:
        logger.warning("ingredient_nutrients DataFrame is empty — skipping. Run fetch_usda_nutrients.py first.")
        return

    logger.info(f"Seeding ingredient_nutrients with {len(df)} records...")
    db.query(IngredientNutrient).delete()

    skipped = 0
    objects = []
    for _, row in df.iterrows():
        ingredient_id = ingredient_name_to_id.get(str(row.get("ingredient_name", "")).lower())
        if ingredient_id is None:
            skipped += 1
            continue
        objects.append(IngredientNutrient(
            ingredient_id=ingredient_id,
            nutrient_name=row.get("nutrient_name"),
            amount_per_100g=row.get("amount_per_100g"),
            unit=row.get("unit"),
        ))

    db.bulk_save_objects(objects)
    db.commit()
    logger.info(f"  → {len(objects)} nutrient rows inserted ({skipped} skipped).")


def seed_ingredient_substitutes(
    db: Session,
    df: pd.DataFrame,
    ingredient_name_to_id: dict[str, int],
) -> None:
    """Seeds ingredient_substitutes, resolving both ingredient and substitute names → FK ids."""
    if df.empty:
        logger.warning("ingredient_substitutes DataFrame is empty — skipping.")
        return

    logger.info(f"Seeding ingredient_substitutes with {len(df)} records...")
    db.query(IngredientSubstitute).delete()

    skipped = 0
    objects = []
    for _, row in df.iterrows():
        ingredient_id = ingredient_name_to_id.get(str(row.get("ingredient_name", "")).lower())
        substitute_id = ingredient_name_to_id.get(str(row.get("substitute_name", "")).lower())
        if ingredient_id is None or substitute_id is None:
            skipped += 1
            continue
        if ingredient_id == substitute_id:
            skipped += 1
            continue
        objects.append(IngredientSubstitute(
            ingredient_id=ingredient_id,
            substitute_id=substitute_id,
            similarity_score=row.get("similarity_score"),
            reason=row.get("reason"),
            source=row.get("source", "MISKG"),
        ))

    db.bulk_save_objects(objects)
    db.commit()
    logger.info(f"  → {len(objects)} substitute pairs inserted ({skipped} skipped).")




def seed_dish_ingredients(
    db: Session,
    df: pd.DataFrame,
    dish_name_to_id: dict[str, int],
    ingredient_name_to_id: dict[str, int],
) -> None:
    """Seeds dish_ingredients from pre-computed dish_ingredients_raw.csv.

    Resolves dish_name → dish_id and ingredient_name → ingredient_id.
    Rows where either FK can't be resolved are skipped with a warning.
    """
    if df.empty:
        logger.warning(
            "dish_ingredients DataFrame is empty — skipping. "
            "Run: python -m src.scripts.fetch_dish_ingredients"
        )
        return

    logger.info("Seeding dish_ingredients with %d records...", len(df))
    db.query(DishIngredient).delete()

    skipped = 0
    objects = []
    for _, row in df.iterrows():
        dish_id = dish_name_to_id.get(str(row.get("dish_name", "")).lower())
        ingredient_id = ingredient_name_to_id.get(str(row.get("ingredient_name", "")).lower())
        if dish_id is None or ingredient_id is None:
            skipped += 1
            continue
        objects.append(DishIngredient(
            dish_id=dish_id,
            ingredient_id=ingredient_id,
            quantity_g=row.get("quantity_g") or None,
            is_optional=bool(row.get("is_optional", False)),
        ))

    db.bulk_save_objects(objects)
    db.commit()
    logger.info("  → %d dish-ingredient links inserted (%d skipped).", len(objects), skipped)


def _fetch_nutrients() -> None:
    """Runs the OpenNutrition fetch unless ingredient_nutrients_raw.csv already covers the current ingredients."""
    path = settings.INGREDIENT_NUTRIENTS_RAW_PATH
    if os.path.exists(path) and os.path.getsize(path) > 0:
        try:
            nutrient_df = pd.read_csv(path)
            if len(nutrient_df) > 0:
                pricing_df = pd.read_csv(settings.INGREDIENTS_PRICING_RAW_PATH)
                pricing_name_col = next(
                    (c for c in ["name", "ITEM_NAME", "item_name", "product_name"] if c in pricing_df.columns),
                    pricing_df.columns[0],
                )
                current_names = set(pricing_df[pricing_name_col].dropna().str.lower())
                cached_names = set(nutrient_df["ingredient_name"].dropna().str.lower())
                overlap = len(current_names & cached_names)
                if overlap >= len(current_names) * 0.5:
                    logger.info(f"ingredient_nutrients_raw.csv covers {overlap}/{len(current_names)} current ingredients — skipping fetch.")
                    return
                logger.warning(
                    f"ingredient_nutrients_raw.csv only covers {overlap}/{len(current_names)} current ingredients — regenerating."
                )
                os.remove(path)
        except Exception:
            pass

    logger.info("Running OpenNutrition nutrient fetch ...")
    from src.scripts.fetch_usda_nutrients import run as fetch_nutrients
    fetch_nutrients()


def download_dataset() -> None:
    """Download and prepare all raw datasets, including ChereBowl pipeline steps."""
    base_paths = [
        settings.MELBOURNE_RAW_PATH,
        settings.DATAGOV_RAW_PATH,
        settings.FOOD_INSECURITY_RAW_PATH,
        settings.VICLGA_BOUNDARY_RAW_PATH,
        settings.LGA_POPULATION_RAW_PATH,
        settings.DIET_INDICATOR_RAW_PATH,
        settings.HEALTH_OUTCOME_RAW_PATH,
        settings.LOW_COST_DIET_RAW_PATH,
        settings.LOW_COST_DIET_HEALTH_OUTCOME_RAW_PATH,
        settings.RECOMMENDED_MACRONUTRIENTS_INTAKE_RAW_PATH,
    ]
    if any(not os.path.exists(p) for p in base_paths):
        logger.info("Missing base datasets detected — downloading...")
        save_local_copy()
    else:
        logger.info("Base datasets present.")

    fetch_vic_grocery_ingredients()
    _fetch_nutrients()


if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    download_dataset()

    db = SessionLocal()
    try:
        # --- Existing support-service datasets (no FK resolution needed) ---
        SIMPLE_REGISTRY = [
            (load_emergency_services_dataset, SupportService),
            (load_food_insecurity_dataset, FoodInsecurity),
            (load_lga_boundaries_dataset, VicLgaBoundary),
            (load_lga_population_dataset, LgaPopulation),
            (load_diet_indicator_dataset, DietIndicator),
            (load_health_outcome_dataset, HealthOutcome),
            (load_low_cost_diet_dataset, LowCostDiet),
            (load_low_cost_diet_health_outcome_dataset, LowCostDietHealthOutcome),
            (load_recommended_macronutrients_intake_dataset, RecommendedMacronutrientsIntake),
        ]
        for loader, model in SIMPLE_REGISTRY:
            seed_simple(db, loader(), model)

        # --- ChereBowl datasets (order matters: parents before children) ---
        ingredient_name_to_id = seed_ingredients(db, load_ingredients_dataset())

        df_dishes = load_dishes_dataset()
        df_dishes = df_dishes.groupby("cuisine", group_keys=False).head(30).reset_index(drop=True)
        dish_name_to_id = seed_dishes(db, df_dishes)

        seed_dish_ingredients(
            db,
            load_dish_ingredients_dataset(),
            dish_name_to_id,
            ingredient_name_to_id,
        )

        seed_ingredient_nutrients(db, load_ingredient_nutrients_dataset(), ingredient_name_to_id)
        seed_ingredient_substitutes(db, load_ingredient_substitutes_dataset(), ingredient_name_to_id)

    finally:
        db.close()
