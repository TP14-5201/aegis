from __future__ import annotations

import difflib
import json
import random
import re
from typing import Any, List, Optional
import math
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


def _sanitize(obj: Any) -> Any:
    """Recursively replace NaN/Infinity floats with None so json.dumps never crashes."""
    if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    return obj


class _SafeJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return json.dumps(
            _sanitize(content),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        ).encode("utf-8")

from src.core.logging import logger
from src.database import Base, engine, get_db
from src.models import LgaPopulation, FoodInsecurity, VicLgaBoundary, SupportService, DietIndicator, HealthOutcome, LowCostDiet, LowCostDietHealthOutcome, RecommendedMacronutrientsIntake, Ingredient, Dish, DishIngredient, IngredientNutrient, IngredientSubstitute
from src.schemas import NearbyServiceOut, FoodInsecurityRegion, LgaStatsOut, DietIndicatorOut, HealthOutcomeOut, LowCostDietOut, LowCostDietHealthOutcomeOut, RecommendedMacronutrientsIntakeOut, RecommendationRequest, RecommendationResponse, DishOut, IngredientOut, AlternativeOut, NutritionPer100g, Citation
from src.core.nutrition import NRV_PER_100G, SCORED_NUTRIENTS
from src.services.nearby_search import DEFAULT_KEYWORDS, find_nearby_support_services
from src.utils.opening_hours import is_open_now, _now_in_tz

from sqlalchemy import func, Integer, case, distinct, Numeric
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_AsGeoJSON


app = FastAPI(title="Aegis Support Services API", version="0.1.0", default_response_class=_SafeJSONResponse)

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Production
    "https://cherebowl.vercel.app",
    # Dev
    "https://cherebowl-underdevelopment.vercel.app",
    # Archived version
    "https://cherebowl-v1.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    # Ensure tables exist; seeding is handled elsewhere
    Base.metadata.create_all(bind=engine)
    logger.info("API startup complete; database ready.")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/lga/boundaries")
def get_lga_boundaries(db: Session = Depends(get_db)) -> dict:
    """Return GeoJSON polygons for all Victorian LGAs from the boundary table."""
    try:
        rows = (
            db.query(
                VicLgaBoundary.lga_name,
                ST_AsGeoJSON(VicLgaBoundary.geometry).label("geojson"),
            )
            .distinct(VicLgaBoundary.lga_name)
            .all()
        )

        features = []
        for row in rows:
            if not row.geojson:
                continue
            geometry = json.loads(row.geojson)
            features.append(
                {
                    "type": "Feature",
                    "properties": {"lga_name": row.lga_name},
                    "geometry": geometry,
                }
            )

        if not features:
            return JSONResponse(
                content={"type": "FeatureCollection", "features": [], "message": "No boundaries found"},
                headers={"Cache-Control": "public, max-age=86400, stale-while-revalidate=604800"},
            )

        return JSONResponse(
            content={"type": "FeatureCollection", "features": features},
            headers={"Cache-Control": "public, max-age=86400, stale-while-revalidate=604800"},
        )
    except Exception as exc:
        logger.exception("Failed to fetch LGA boundaries: %s", exc)
        raise HTTPException(status_code=500, detail="Internal error fetching LGA boundaries")


@app.get("/lga/stats", response_model=List[LgaStatsOut])
def get_lga_stats(db: Session = Depends(get_db)) -> List[dict]:
    """Return population, gendered food insecurity averages, and emergency service counts per LGA."""
    try:
        men_pct = func.coalesce(
            func.round(
                func.avg(
                    case(
                        (FoodInsecurity.gender == "Men", FoodInsecurity.estimate_pct),
                        else_=None,
                    )
                ).cast(Numeric),
                2,
            ),
            0,
        )

        women_pct = func.coalesce(
            func.round(
                func.avg(
                    case(
                        (FoodInsecurity.gender == "Women", FoodInsecurity.estimate_pct),
                        else_=None,
                    )
                ).cast(Numeric),
                2,
            ),
            0,
        )

        emergency_services_count = func.coalesce(
            func.count(distinct(SupportService.id)),
            0,
        )

        rows = (
            db.query(
                LgaPopulation.lga_pid,
                LgaPopulation.lga_name,
                LgaPopulation.pop_2024_total,
                men_pct.label("men_pct"),
                women_pct.label("women_pct"),
                emergency_services_count.label("emergency_services_count"),
            )
            .outerjoin(FoodInsecurity, FoodInsecurity.lga_pid == LgaPopulation.lga_pid)
            .outerjoin(SupportService, SupportService.lga_pid == LgaPopulation.lga_pid)
            .group_by(LgaPopulation.lga_pid, LgaPopulation.lga_name, LgaPopulation.pop_2024_total)
            .all()
        )

        return [
            {
                "lga_name": row.lga_name,
                "men_pct": float(row.men_pct),
                "women_pct": float(row.women_pct),
                "pop_2024_total": row.pop_2024_total,
                "emergency_services_count": int(row.emergency_services_count),
            }
            for row in rows
        ]
    except Exception as exc:
        logger.exception("Failed to fetch LGA stats: %s", exc)
        raise HTTPException(status_code=500, detail="Internal error fetching LGA stats")


@app.get("/services", response_model=List[NearbyServiceOut])
def get_all_services(
    db: Session = Depends(get_db),
    tz: Optional[str] = Query(None, description="IANA timezone for open/closed status"),
):
    """Return all support services. Used for full-map browse mode."""
    try:
        rows = db.query(SupportService).filter(
            SupportService.latitude.isnot(None),
            SupportService.longitude.isnot(None),
        ).all()

        results = []
        now_local = _now_in_tz(tz)
        for row in rows:
            r = {
                "id": row.id,
                "name": row.name,
                "description": row.description,
                "target_audience": row.target_audience,
                "address": row.address,
                "suburb": row.suburb,
                "primary_phone": row.primary_phone,
                "phone_display": row.phone_display,
                "email": row.email,
                "website": row.website,
                "social_media": row.social_media,
                "opening_hours": row.opening_hours if isinstance(row.opening_hours, dict) else {},
                "cost": row.cost,
                "tram_routes": row.tram_routes,
                "bus_routes": row.bus_routes,
                "nearest_train_station": row.nearest_train_station,
                "categories": row.categories if isinstance(row.categories, list) else [],
                "longitude": row.longitude,
                "latitude": row.latitude,
                "source": row.source,
                "distance_km": None,
            }
            try:
                r["is_open_now"] = is_open_now(r["opening_hours"], now_local)
            except Exception:
                r["is_open_now"] = None
            results.append(r)

        results.sort(key=lambda x: x["name"] or "")
        return results
    except Exception as exc:
        logger.exception("Failed to fetch all services: %s", exc)
        raise HTTPException(status_code=500, detail="Internal error fetching services")


@app.get("/nearby", response_model=List[NearbyServiceOut])
def get_nearby_services(
    lat: float = Query(..., description="User latitude"),
    lon: float = Query(..., description="User longitude"),
    radius_km: float = Query(5.0, ge=0.1, le=50.0, description="Search radius in km (0.1-50)"),
    limit: int = Query(25, ge=1, le=200, description="Max number of results"),
    include_datagov: bool = Query(True, description="Include DataGov emergency relief outlets"),
    keywords: Optional[List[str]] = Query(None, description="Override default keywords to match services"),
    tz: Optional[str] = Query(None, description="IANA timezone, e.g. Australia/Sydney"),
    db: Session = Depends(get_db),
):
    """Return nearby food banks and relevant welfare centres.

    By default, matches against common welfare/relief keywords and always
    includes DataGov emergency relief outlets within the radius. When a
    timezone is provided, each result includes an `is_open_now` flag derived
    from its opening hours.
    """
    if keywords is not None and len(keywords) == 0:
        keywords = None

    try:
        results = find_nearby_support_services(
            db=db,
            user_lat=lat,
            user_lon=lon,
            radius_km=radius_km,
            limit=limit,
            keywords=keywords if keywords is not None else DEFAULT_KEYWORDS,
            include_datagov=include_datagov,
        )
        # Coerce categories/opening_hours to expected shapes to be safe
        for r in results:
            # Use isinstance(x, float) because pd.nan or np.nan crashes on strings/lists
            for key in ["categories", "opening_hours"]:
                val = r.get(key)
                if isinstance(val, float) and math.isnan(val):
                    r[key] = [] if key == "categories" else {}
                elif val is None:
                    r[key] = [] if key == "categories" else {}

        # Compute real-time open status in user's timezone (if provided) and filter that are closed
        now_local = _now_in_tz(tz)
        for r in results:
            try:
                r["is_open_now"] = is_open_now(r.get("opening_hours"), now_local)
            except Exception:
                r["is_open_now"] = None
        # Only exclude services explicitly marked closed; keep open + unknown
        results = [r for r in results if r.get("is_open_now") is not False]
        return results
    except Exception as exc:
        logger.exception("Failed to fetch nearby services: %s", exc)
        raise HTTPException(status_code=500, detail="Internal error while searching for services")


@app.get("/diet-indicators", response_model=List[DietIndicatorOut])
def get_diet_indicators(db: Session = Depends(get_db)):
    """
    Fetch all diet indicators, returning only the 
    statistical columns and categories.
    """
    try:
        # We fetch the full rows; the response_model filters the fields
        indicators = db.query(DietIndicator).all()

        if not indicators:
            return JSONResponse(content=[], headers={"Cache-Control": "public, max-age=86400, stale-while-revalidate=604800"})

        from fastapi.encoders import jsonable_encoder
        return JSONResponse(
            content=jsonable_encoder(indicators),
            headers={"Cache-Control": "public, max-age=86400, stale-while-revalidate=604800"},
        )
    except Exception as exc:
        logger.exception("Failed to fetch diet indicators: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Internal error fetching dietary data"
        )


@app.get("/health-outcomes", response_model=List[HealthOutcomeOut])
def get_health_outcomes(db: Session = Depends(get_db)):
    """
    Fetch all health outcomes related to food security status.
    Returns statistical percentages and confidence intervals.
    """
    try:
        # Fetching and ordering by category to keep the data organized
        results = db.query(HealthOutcome).order_by(HealthOutcome.category).all()

        if not results:
            return JSONResponse(content=[], headers={"Cache-Control": "public, max-age=86400, stale-while-revalidate=604800"})

        from fastapi.encoders import jsonable_encoder
        return JSONResponse(
            content=jsonable_encoder(results),
            headers={"Cache-Control": "public, max-age=86400, stale-while-revalidate=604800"},
        )
    except Exception as exc:
        logger.exception("Failed to fetch health outcomes: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Internal error fetching health outcome data"
        )


@app.get("/low-cost-diet", response_model=List[LowCostDietOut])
def get_low_cost_diet_stats(db: Session = Depends(get_db)):
    """
    Fetch statistics on populations relying on low-cost diets.
    Returns percentages and 95% confidence intervals for 'Yes' and 'No' responses.
    """
    try:
        # Fetching all records from the low_cost_diet table
        rows = db.query(LowCostDiet).all()

        if not rows:
            return JSONResponse(content=[], headers={"Cache-Control": "public, max-age=86400, stale-while-revalidate=604800"})

        from fastapi.encoders import jsonable_encoder
        return JSONResponse(
            content=jsonable_encoder(rows),
            headers={"Cache-Control": "public, max-age=86400, stale-while-revalidate=604800"},
        )
    except Exception as exc:
        logger.exception("Failed to fetch low-cost diet stats: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Internal error fetching low-cost diet data"
        )


@app.get("/low-cost-diet-health-outcomes", response_model=List[LowCostDietHealthOutcomeOut])
def get_low_cost_diet_health_outcomes(db: Session = Depends(get_db)):
    """
    Fetch health outcomes specifically categorized by whether 
    populations relied on low-cost diets.
    """
    try:
        # Ordering by category and outcome for a consistent frontend display
        results = (
            db.query(LowCostDietHealthOutcome)
            .order_by(LowCostDietHealthOutcome.category, LowCostDietHealthOutcome.health_outcome)
            .all()
        )

        if not results:
            return JSONResponse(content=[], headers={"Cache-Control": "public, max-age=86400, stale-while-revalidate=604800"})

        from fastapi.encoders import jsonable_encoder
        return JSONResponse(
            content=jsonable_encoder(results),
            headers={"Cache-Control": "public, max-age=86400, stale-while-revalidate=604800"},
        )
    except Exception as exc:
        logger.exception("Failed to fetch low-cost diet health outcomes: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Internal error fetching dietary health outcome data"
        )


@app.get("/recommended-macronutrients", response_model=List[RecommendedMacronutrientsIntakeOut])
def get_all_macronutrient_goals(db: Session = Depends(get_db)):
    """
    Retrieve all nutritional records based on age, nutrient, and goals 
    """
    try:
        # Fetching and ordering by category to keep the data organized
        results = (
            db.query(RecommendedMacronutrientsIntake)
            .order_by(RecommendedMacronutrientsIntake.age, RecommendedMacronutrientsIntake.nutrient)
            .all()
        )

        if not results:
            return JSONResponse(content=[], headers={"Cache-Control": "public, max-age=86400, stale-while-revalidate=604800"})

        from fastapi.encoders import jsonable_encoder
        return JSONResponse(
            content=jsonable_encoder(results),
            headers={"Cache-Control": "public, max-age=86400, stale-while-revalidate=604800"},
        )
    except Exception as exc:
        logger.exception("Failed to fetch recommended macronutrients: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Internal error fetching recommended macronutrients"
        )


# ---------------------------------------------------------------------------
# Grocery recommendations
# ---------------------------------------------------------------------------

_DIETARY_FLAG_MAP: dict[str, str] = {
    "vegetarian": "vegetarian",
    "vegan":       "vegan",
    "gluten-free": "gluten_free",
    "dairy-free":  "dairy_free",
    "halal":       "halal",
}

_CITATIONS = [
    Citation(
        name="Australian Grocery Product Prices (thedevastator, Kaggle)",
        version="2022",
        url="https://www.kaggle.com/datasets/thedevastator/grocery-product-prices-for-australian-states",
    ),
    Citation(
        name="Open Food Facts",
        url="https://world.openfoodfacts.org/",
    ),
    Citation(
        name="USDA FoodData Central",
        url="https://fdc.nal.usda.gov/",
    ),
    Citation(
        name="ACCC Supermarkets Inquiry 2024–25",
        url="https://www.accc.gov.au/inquiries-and-consultations/supermarkets-inquiry-2024-25",
    ),
    Citation(
        name="NHMRC Nutrient Reference Values",
        url="https://www.nrv.gov.au/",
    ),
    Citation(
        name="Yummly 'What's Cooking' dataset",
        url="https://www.kaggle.com/c/whats-cooking",
    ),
]


def _build_nutrition(nutrients: list[IngredientNutrient]) -> NutritionPer100g:
    data: dict = {}
    for n in nutrients:
        if n.nutrient_name in NutritionPer100g.model_fields:
            data[n.nutrient_name] = n.amount_per_100g
    return NutritionPer100g(**data)


def _build_alternative(substitute: IngredientSubstitute) -> AlternativeOut:
    sub = substitute.substitute
    reason = substitute.reason or "availability"
    valid_reasons = {"cheaper", "healthier", "dietary_swap", "availability"}
    if reason not in valid_reasons:
        reason = "availability"
    return AlternativeOut(
        id=sub.id,
        name=sub.name or "Unknown",
        priceAUD=sub.price_aud or 0.0,
        packLabel=sub.pack_label or "1 pack",
        benefits=sub.benefit_tags or [],
        reason=reason,
    )


def _build_ingredient_out(
    ingredient: Ingredient,
    cost_per_serving: float,
) -> IngredientOut:
    return IngredientOut(
        id=ingredient.id,
        name=ingredient.name or "Unknown",
        packLabel=ingredient.pack_label or "1 pack",
        packGrams=ingredient.pack_grams,
        priceAUD=round(cost_per_serving, 2),
        priceSource=ingredient.price_source or "kaggle_supermarkets_2024",
        priceAsOf=ingredient.price_as_of or "2024-01-01",
        benefits=ingredient.benefit_tags or [],
        alternatives=[_build_alternative(s) for s in (ingredient.substitute_links or [])[:3]],
        nutrition=_build_nutrition(ingredient.nutrients or []),
    )


_QTY_RE = re.compile(
    r"^\s*[\d/½¼¾⅓⅔]+\s*(cup|c\.|tbsp|tsp|tablespoon|teaspoon|oz|lb|g|kg|ml|l|pound|ounce|clove|head|bunch|slice|can|jar|pkg|package|medium|large|small|piece|pinch|dash|handful)s?\s*",
    re.IGNORECASE,
)
_DESCRIPTOR_TOKENS = {
    "fresh", "dried", "chopped", "diced", "minced", "sliced", "grated",
    "peeled", "crushed", "ground", "cooked", "raw", "frozen", "canned",
    "optional", "to", "taste", "finely", "roughly", "thinly", "and", "or",
}

# Keywords that identify a Pantry/Bakery item as an actual cooking ingredient
_COOKING_PANTRY_KEYWORDS = {
    "sauce", "oil", "vinegar", "honey", "mustard", "paste", "butter",
    "flour", "sugar", "spice", "herb", "stock", "broth", "bread", "loaf",
    "crumb", "biscuit", "cracker",
}


def _is_cooking_ingredient(ing: Ingredient) -> bool:
    """Returns True only for ingredients that are actual cooking/grocery items.

    Filters out beverages, confectionery, coffee capsules, energy drinks, etc.
    that exist in the Coles dataset but are not recipe ingredients.
    """
    cat = (ing.category or "").lower()
    name = (ing.name or "").lower()
    if cat in {"meat & seafood", "dairy, eggs & fridge"}:
        return True
    if cat == "pantry":
        return any(kw in name for kw in _COOKING_PANTRY_KEYWORDS)
    if cat == "bakery":
        return any(kw in name for kw in {"bread", "loaf", "crumb"})
    return False


def _normalize_ingredient_name(raw: str) -> str:
    raw = _QTY_RE.sub("", raw).strip()
    tokens = [t for t in raw.lower().split() if t not in _DESCRIPTOR_TOKENS]
    return " ".join(tokens).strip()


def _match_ingredients(
    raw_ingredients: list[str],
    db_ingredients: list[Ingredient],
    cutoff: float = 0.70,
) -> list[Ingredient]:
    """Fuzzy-match a dish's raw ingredient names against the priced ingredient pool.

    Only cooking-appropriate ingredients are considered (beverages/snacks excluded).
    Cutoff is intentionally strict so that only meaningful ingredient matches are kept.
    """
    cooking_pool = [ing for ing in db_ingredients if _is_cooking_ingredient(ing)]
    name_map = {ing.name.lower(): ing for ing in cooking_pool if ing.name and ing.price_aud}
    norm_keys = list(name_map.keys())

    matched: list[Ingredient] = []
    seen_ids: set[int] = set()
    for raw in raw_ingredients:
        normalized = _normalize_ingredient_name(raw)
        if not normalized:
            continue
        hits = difflib.get_close_matches(normalized, norm_keys, n=1, cutoff=cutoff)
        if hits:
            ing = name_map[hits[0]]
            if ing.id not in seen_ids:
                matched.append(ing)
                seen_ids.add(ing.id)
    return matched


def _clean_dish_name(name: str) -> str:
    """Remove accidental duplicate cuisine prefix from generated dish names.

    Generated names are built as "{Cuisine} {top-ingredient} & {top-ingredient}".
    When a recipe ingredient starts with the cuisine word (e.g. "Chinese five spice"),
    the name becomes "Chinese Chinese & ...". This strips the duplicate.
    """
    parts = name.split(" ", 1)
    if len(parts) == 2 and parts[1].lower().startswith(parts[0].lower() + " "):
        return parts[0] + " " + parts[1][len(parts[0]) + 1:]
    return name


@app.post("/api/recommendations", response_model=RecommendationResponse)
def get_recommendations(
    body: RecommendationRequest,
    db: Session = Depends(get_db),
) -> RecommendationResponse:
    """Return budget-aware dish and ingredient recommendations.

    Uses pre-computed DishIngredient mappings (populated by fetch_dish_ingredients.py
    + data_seeding.py) so no ML inference happens at request time.

    Falls back to runtime fuzzy matching when the dish_ingredients table is empty
    (i.e. before the pre-computation script has been run).
    """
    try:
        dietary_flags = [_DIETARY_FLAG_MAP.get(d.lower(), d.lower()) for d in body.dietaryNeeds]
        per_dish_budget = body.budget / body.numberOfDishes
        _OVERLAP_WEIGHT = 5.0

        # ------------------------------------------------------------------ #
        # Decide path: pre-computed JOIN vs runtime fuzzy fallback            #
        # ------------------------------------------------------------------ #
        use_precomputed = db.query(func.count(DishIngredient.id)).scalar() > 0

        if use_precomputed:
            # -------------------------------------------------------------- #
            # Fast path: JOIN dishes → dish_ingredients → ingredients         #
            # Only dishes with at least 2 linked ingredients are considered.  #
            # -------------------------------------------------------------- #
            from sqlalchemy import and_

            dish_rows = (
                db.query(Dish)
                .join(DishIngredient, DishIngredient.dish_id == Dish.id)
                .join(Ingredient, and_(
                    Ingredient.id == DishIngredient.ingredient_id,
                    Ingredient.price_aud.isnot(None),
                ))
                .group_by(Dish.id)
                .having(func.count(DishIngredient.id) >= 2)
                .all()
            )

            if dietary_flags:
                dish_rows = [
                    d for d in dish_rows
                    if any(flag in (d.dietary_flags or []) for flag in dietary_flags)
                    or not d.dietary_flags
                ]

            random.shuffle(dish_rows)

            def _get_ingredients(dish: Dish) -> list[Ingredient]:
                return [
                    link.ingredient for link in dish.ingredient_links
                    if link.ingredient and link.ingredient.price_aud
                ]

            candidates_pool = []
            for dish in dish_rows:
                matched = _get_ingredients(dish)
                if len(matched) < 2:
                    continue
                scale = body.numberOfPeople / max(dish.base_servings or 4, 1)
                cost = sum((ing.price_aud or 0) * scale for ing in matched)
                over = max(0.0, cost - per_dish_budget)
                nutrient_total: dict[str, float] = {}
                for ing in matched:
                    for n in (ing.nutrients or []):
                        if n.nutrient_name in SCORED_NUTRIENTS:
                            nutrient_total[n.nutrient_name] = nutrient_total.get(n.nutrient_name, 0.0) + (n.amount_per_100g or 0.0)
                nutrition_score = sum(
                    min(nutrient_total.get(k, 0.0) / NRV_PER_100G[k], 1.0)
                    for k in SCORED_NUTRIENTS
                )
                candidates_pool.append((over, -nutrition_score, dish, matched))
        else:
            # -------------------------------------------------------------- #
            # Fallback: runtime fuzzy matching (used before pre-computation)  #
            # -------------------------------------------------------------- #
            logger.warning(
                "dish_ingredients table is empty — using runtime fuzzy matching. "
                "Run: python -m src.scripts.fetch_dish_ingredients && python -m src.services.data_seeding"
            )
            all_ingredients: list[Ingredient] = (
                db.query(Ingredient).filter(Ingredient.price_aud.isnot(None)).all()
            )
            dishes_pool = db.query(Dish).filter(Dish.raw_ingredients.isnot(None)).all()
            random.shuffle(dishes_pool)
            if dietary_flags:
                dishes_pool = [
                    d for d in dishes_pool
                    if any(flag in (d.dietary_flags or []) for flag in dietary_flags)
                    or not d.dietary_flags
                ]
            candidates_pool = []
            for dish in dishes_pool:
                matched = _match_ingredients(dish.raw_ingredients or [], all_ingredients)
                if len(matched) < 2:
                    continue
                scale = body.numberOfPeople / max(dish.base_servings or 4, 1)
                cost = sum((ing.price_aud or 0) * scale for ing in matched)
                over = max(0.0, cost - per_dish_budget)
                nutrient_total = {}
                for ing in matched:
                    for n in (ing.nutrients or []):
                        if n.nutrient_name in SCORED_NUTRIENTS:
                            nutrient_total[n.nutrient_name] = nutrient_total.get(n.nutrient_name, 0.0) + (n.amount_per_100g or 0.0)
                nutrition_score = sum(
                    min(nutrient_total.get(k, 0.0) / NRV_PER_100G[k], 1.0)
                    for k in SCORED_NUTRIENTS
                )
                candidates_pool.append((over, -nutrition_score, dish, matched))

        # ------------------------------------------------------------------ #
        # Greedy diversity selection across all qualifying dishes             #
        # ------------------------------------------------------------------ #
        candidates_pool.sort(key=lambda x: (x[0], x[1]))
        selected: list[tuple[float, float, Dish, list[Ingredient]]] = []
        used_ids: set[int] = set()

        while candidates_pool:
            best_idx = 0
            best_key = None
            for i, (over, neg_nutrition, dish, matched) in enumerate(candidates_pool):
                matched_ids = {ing.id for ing in matched}
                overlap = len(matched_ids & used_ids) / len(matched_ids) if matched_ids else 0.0
                key = (over + overlap * _OVERLAP_WEIGHT, neg_nutrition)
                if best_key is None or key < best_key:
                    best_key = key
                    best_idx = i

            chosen = candidates_pool.pop(best_idx)
            selected.append(chosen)
            used_ids.update(ing.id for ing in chosen[3])

        dish_outs: list[DishOut] = []
        for *_, dish, matched_ingredients in selected:
            dish_id: int = dish.id  # type: ignore[assignment]
            dish_name: str = _clean_dish_name(dish.name or "Unnamed Dish")  # type: ignore[assignment]
            dish_cuisine: str = dish.cuisine or "Mixed"  # type: ignore[assignment]
            dish_flags: list[str] = dish.dietary_flags or []  # type: ignore[assignment]
            dish_servings: int = dish.base_servings or 4  # type: ignore[assignment]

            scale = body.numberOfPeople / max(dish_servings, 1)
            ingredient_outs: list[IngredientOut] = []
            dish_cost = 0.0
            for ing in matched_ingredients:
                price: float = ing.price_aud or 0.0  # type: ignore[assignment]
                cost_per_serving = price * scale
                dish_cost += cost_per_serving
                ingredient_outs.append(_build_ingredient_out(ing, cost_per_serving))

            dish_outs.append(DishOut(
                id=dish_id,
                name=dish_name,
                cuisine=dish_cuisine,
                ingredientCount=len(ingredient_outs),
                dishCostAUD=round(dish_cost, 2),
                ingredients=ingredient_outs,
                dietaryFlags=dish_flags,
            ))

        total = round(sum(d.dishCostAUD for d in dish_outs), 2)

        return RecommendationResponse(
            dishes=dish_outs,
            totalEstimatedAUD=total,
            budgetAUD=body.budget,
            people=body.numberOfPeople,
            cuisine="mixed",
            generatedAt=datetime.utcnow().isoformat() + "Z",
            citations=_CITATIONS,
        )

    except Exception as exc:
        logger.exception("Failed to generate recommendations: %s", exc)
        raise HTTPException(status_code=500, detail="Internal error generating recommendations")