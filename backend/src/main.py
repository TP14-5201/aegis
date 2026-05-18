from __future__ import annotations

import json
import os
from typing import List, Optional
import math
from datetime import datetime

import bcrypt
import httpx
from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.core.logging import logger
from src.database import Base, engine, get_db
from src.models import (
    DietIndicator,
    FoodInaccessibilityReasons,
    FoodInsecurity,
    HealthOutcome,
    LgaPopulation,
    LowCostDiet,
    LowCostDietHealthOutcome,
    RecommendedMacronutrientsIntake,
    SupportService,
    VicLgaBoundary,
)
from src.schemas import (
    DietIndicatorOut,
    FoodInsecurityRegion,
    HealthOutcomeOut,
    IngredientSubstitutesOut,
    LgaFoodInaccessibilityReasonsOut,
    LgaStatsOut,
    LowCostDietHealthOutcomeOut,
    LowCostDietOut,
    NearbyServiceOut,
    RecommendedMacronutrientsIntakeOut,
)
from src.services.ingredient_substitution import engine as substitution_engine, SubstituteResult
from src.services import recommendation_service
from src.services import personalisation_service
from src.services.nearby_search import DEFAULT_KEYWORDS, find_nearby_support_services, search_support_service_suburbs
from src.services.gtfsr import fetch_vehicle_positions, fetch_trip_updates
from src.utils.opening_hours import is_open_now, _now_in_tz

from sqlalchemy import func, Integer, case, distinct, Numeric
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_AsGeoJSON

app = FastAPI(title="Aegis Support Services API", version="0.1.0")

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # ngrok dev tunnel (accessWidget testing) — remove or update when URL changes
    "https://resurrect-activity-chaffing.ngrok-free.dev",
    # Production
    "https://cherebowl.vercel.app",
    # Dev
    "https://cherebowl-underdevelopment.vercel.app",
    "https://cherebowl-dev.vercel.app",
    # Archived version
    "https://cherebowl-v1.vercel.app",
    "https://cherebowl-v2.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        recommendation_service.warm_percentiles(db)
    except Exception as exc:
        logger.warning("Could not warm nutrient percentiles at startup: %s", exc)
    try:
        substitution_engine.load_index(db)
    except Exception as exc:
        logger.warning("Could not load substitution index at startup: %s", exc)
    logger.info("API startup complete; database ready.")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


class _LoginRequest(BaseModel):
    password: str


_LOGIN_PASSWORD_HASH_ENV = "LOGIN_PASSWORD_HASH"


def _get_login_password_hash() -> str:
    print( os.getenv(_LOGIN_PASSWORD_HASH_ENV, "").strip())
    return os.getenv(_LOGIN_PASSWORD_HASH_ENV, "").strip()


@app.post("/auth/login")
def auth_login(body: _LoginRequest):
    password_hash = _get_login_password_hash()
    if not password_hash:
        logger.error("%s is not configured", _LOGIN_PASSWORD_HASH_ENV)
        raise HTTPException(status_code=503, detail="Login is not configured")

    try:
        is_valid = bcrypt.checkpw(
            body.password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except ValueError:
        logger.error("%s is not a valid bcrypt hash", _LOGIN_PASSWORD_HASH_ENV)
        raise HTTPException(status_code=503, detail="Login is not configured")

    if is_valid:
        return {"success": True}
    raise HTTPException(status_code=401, detail="Incorrect password")


@app.get("/lga/boundaries")
def get_lga_boundaries(db: Session = Depends(get_db)) -> dict:
    """Return GeoJSON polygons for all Victorian LGAs from the boundary table."""
    try:
        rows = (
            db.query(
                VicLgaBoundary.lga_pid,
                VicLgaBoundary.lga_name,
                ST_AsGeoJSON(VicLgaBoundary.geometry).label("geojson"),
            )
            .distinct(VicLgaBoundary.lga_pid)
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
                    "properties": {"lga_name": row.lga_name, "lga_pid": row.lga_pid},
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
    """Return population, combined food insecurity percentage, and emergency service counts per LGA."""
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
                (men_pct + women_pct).label("food_insecurity_pct"),
                emergency_services_count.label("emergency_services_count"),
            )
            .outerjoin(FoodInsecurity, FoodInsecurity.lga_pid == LgaPopulation.lga_pid)
            .outerjoin(SupportService, SupportService.lga_pid == LgaPopulation.lga_pid)
            .group_by(LgaPopulation.lga_pid, LgaPopulation.lga_name, LgaPopulation.pop_2024_total)
            .all()
        )

        return [
            {
                "lga_pid": row.lga_pid,
                "lga_name": row.lga_name,
                "food_insecurity_pct": float(row.food_insecurity_pct),
                "pop_2024_total": row.pop_2024_total,
                "emergency_services_count": int(row.emergency_services_count),
            }
            for row in rows
        ]
    except Exception as exc:
        logger.exception("Failed to fetch LGA stats: %s", exc)
        raise HTTPException(status_code=500, detail="Internal error fetching LGA stats")


def _unknown_if_missing(value):
    if value is None:
        return "Unknown"
    try:
        if math.isnan(value):
            return "Unknown"
    except TypeError:
        pass
    return value


@app.get("/lga/food-inaccessibility-reasons", response_model=List[LgaFoodInaccessibilityReasonsOut])
def get_lga_food_inaccessibility_reasons(db: Session = Depends(get_db)) -> List[dict]:
    """Return food inaccessibility reason percentages by LGA."""
    try:
        rows = (
            db.query(
                FoodInaccessibilityReasons.lga_pid,
                FoodInaccessibilityReasons.limited_variety,
                FoodInaccessibilityReasons.too_expensive,
                FoodInaccessibilityReasons.wrong_quality,
                FoodInaccessibilityReasons.transport_gap,
            )
            .order_by(FoodInaccessibilityReasons.lga_pid)
            .all()
        )

        return [
            {
                "lga_pid": row.lga_pid,
                "limited_variety": _unknown_if_missing(row.limited_variety),
                "too_expensive": _unknown_if_missing(row.too_expensive),
                "wrong_quality": _unknown_if_missing(row.wrong_quality),
                "transport_gap": _unknown_if_missing(row.transport_gap),
            }
            for row in rows
        ]
    except Exception as exc:
        logger.exception("Failed to fetch LGA food inaccessibility reasons: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Internal error fetching LGA food inaccessibility reasons",
        )


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
# Ingredient Substitution
# ---------------------------------------------------------------------------

def _result_to_dict(result: SubstituteResult) -> dict:
    """Serialise a SubstituteResult dataclass into a JSON-serialisable dict."""

    def _slot(s):
        if s is None:
            return None
        return {
            "ingredient_code": s.ingredient_code,
            "product_name": s.product_name,
            "sub_category": s.sub_category,
            "health_benefits": s.health_benefits,
            "retail_price": s.retail_price,
            "nutrition_grade": s.nutrition_grade,
            "proteins_100g": s.proteins_100g,
            "fat_100g": s.fat_100g,
            "carbohydrates_100g": s.carbohydrates_100g,
            "energy_100g": s.energy_100g,
            "similarity_score": s.similarity_score,
            "objective_score": s.objective_score,
        }

    return {
        "query_code": result.query_code,
        "query_name": result.query_name,
        "budget": _slot(result.budget),
        "nutrition": _slot(result.nutrition),
        "balanced": _slot(result.balanced),
        "error": result.error,
    }


@app.get(
    "/ingredients/{ingredient_code}/substitutes",
    response_model=IngredientSubstitutesOut,
    summary="Smart Ingredient Switch",
    description=(
        "Return three curated substitutes for a given ingredient: "
        "Budget (cheapest), Nutrition (highest Nutri-Score / protein), "
        "and Balanced (best price-to-nutrition ratio)."
    ),
    tags=["ingredients"],
)
def get_ingredient_substitutes(
    ingredient_code: str,
    db: Session = Depends(get_db),
) -> dict:
    """
    Two-stage retrieval-ranking:
    1. FAISS ANN (K=50) filtered by functional food role.
    2. Three deterministic scorers for Budget / Nutrition / Balanced.
    """
    try:
        result = substitution_engine.get_substitutes(ingredient_code, db)
        return _result_to_dict(result)
    except Exception as exc:
        logger.exception("Substitution engine error for '%s': %s", ingredient_code, exc)
        raise HTTPException(
            status_code=500,
            detail="Internal error generating ingredient substitutes",
        )


# ---------------------------------------------------------------------------
# Weather — proxied from backend so the API key never reaches the browser
# ---------------------------------------------------------------------------

_OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY", "")

@app.get("/weather")
async def get_weather(lat: float = Query(...), lon: float = Query(...)):
    if not _OPENWEATHER_KEY:
        raise HTTPException(status_code=503, detail="Weather service not configured")
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={_OPENWEATHER_KEY}&units=metric"
    )
    async with httpx.AsyncClient(timeout=8) as client:
        try:
            r = await client.get(url)
            r.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=502, detail=f"OpenWeather error: {exc.response.status_code}")
        except Exception as exc:
            logger.exception("Weather fetch failed: %s", exc)
            raise HTTPException(status_code=502, detail="Could not fetch weather data")
    data = r.json()
    return {
        "temp": round(data["main"]["temp"]),
        "feels_like": round(data["main"]["feels_like"]),
        "rain_mm": round(data.get("rain", {}).get("1h", 0), 1),
        "wind_kph": round(data["wind"]["speed"] * 3.6, 1),
        "description": data["weather"][0]["description"].capitalize(),
        "icon": data["weather"][0]["icon"],
    }


# ---------------------------------------------------------------------------
# GTFSR — real-time vehicle positions + trip updates (proxied from backend
# so the API key never reaches the browser)
# ---------------------------------------------------------------------------

@app.get("/gtfsr/vehicles")
async def gtfsr_vehicles(route_ids: Optional[str] = None):
    """Return live vehicle positions, optionally filtered by comma-separated route IDs."""
    try:
        vehicles = await fetch_vehicle_positions()
        if route_ids:
            ids = set(route_ids.split(","))
            vehicles = [v for v in vehicles if v.get("route_id") in ids]
        return vehicles
    except Exception as exc:
        logger.exception("GTFSR vehicle positions error: %s", exc)
        raise HTTPException(status_code=502, detail="Could not fetch vehicle positions from GTFSR feed")


@app.get("/gtfsr/trip-update")
async def gtfsr_trip_update(trip_id: str, mode: str = "train"):
    """Return real-time stop_time_updates for a specific trip.
    mode: train | tram | bus | vline
    """
    try:
        updates = await fetch_trip_updates(trip_id, mode=mode)
        return updates
    except Exception as exc:
        logger.exception("GTFSR trip update error for trip %s: %s", trip_id, exc)
        raise HTTPException(status_code=502, detail="Could not fetch trip updates from GTFSR feed")


# ---------------------------------------------------------------------------
# Recommendations — value-based ingredient ranking
# ---------------------------------------------------------------------------

class RecommendationRequest(BaseModel):
    budget: float
    people: int
    days: int
    description: Optional[str] = None
    dietary_goal: Optional[str] = None
    dietary_needs: List[str] = []


class ScoredIngredient(BaseModel):
    ingredient_code: str
    product_name: str
    sub_category: str
    retail_price: float
    health_score: float
    rec_score: float
    nutrient_badges: List[str] = []


class RecommendationResponse(BaseModel):
    ingredients: List[ScoredIngredient]
    budget_per_dish_per_person: float


@app.post(
    "/recommendations",
    response_model=RecommendationResponse,
    summary="Budget-aware ingredient recommendations",
    tags=["recommendations"],
)
def get_recommendations(
    body: RecommendationRequest,
    bag_size: int = Query(default=15, ge=5, le=40),
    db: Session = Depends(get_db),
) -> dict:
    """
    Score all ingredients for the user's planner profile and return globally
    ranked top items (up to bag_size, max 3 per sub_category), ranked by
    rec_score (or final_score when a description is provided).

    rec_score = 0.50 × affordability + 0.30 × health + 0.20 × nutrient_density.
    Dietary incompatibility and prices above budget/5 are hard-vetoed to 0.
    health_score is returned normalised to [0, 1].
    """
    description = body.description and body.description.strip()
    dietary_goal = body.dietary_goal and body.dietary_goal.strip()
    combined_text = " ".join(filter(None, [description, dietary_goal])) or None

    if combined_text:
        preferences = personalisation_service.extract_preferences(combined_text)
        scored = recommendation_service.score_ingredients_with_preferences(
            db=db,
            budget=body.budget,
            people=body.people,
            days=body.days,
            dietary_needs=body.dietary_needs,
            preferences=preferences,
            description=combined_text,
        )
        score_col = "final_score"
    else:
        scored = recommendation_service.score_ingredients(
            db=db,
            budget=body.budget,
            people=body.people,
            days=body.days,
            dietary_needs=body.dietary_needs,
        )
        score_col = "rec_score"

    bdpp = body.budget / max(body.people, 1) / max(body.days, 1) / 3

    viable = scored[scored[score_col] > 0]
    top = recommendation_service.select_bag(viable, bag_size=bag_size, max_per_category=3, score_col=score_col)

    ingredients = [
        {
            "ingredient_code": row["ingredient_code"],
            "product_name":    row["product_name"],
            "sub_category":    row["sub_category"] or "",
            "retail_price":    float(row["retail_price"]),
            "health_score":    float(row["final_health_score"] or 0.0) / 100.0,
            "rec_score":       float(row[score_col]),
            "nutrient_badges": row["nutrient_badges"],
        }
        for _, row in top.iterrows()
    ]

    return {"ingredients": ingredients, "budget_per_dish_per_person": bdpp}
