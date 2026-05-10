from __future__ import annotations

import json
from typing import List, Optional
import math
from datetime import datetime
import os

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.core.logging import logger
from src.database import Base, engine, get_db
from src.models import LgaPopulation, FoodInsecurity, VicLgaBoundary, SupportService, DietIndicator, HealthOutcome, LowCostDiet, LowCostDietHealthOutcome, RecommendedMacronutrientsIntake
from src.schemas import NearbyServiceOut, FoodInsecurityRegion, LgaStatsOut, DietIndicatorOut, HealthOutcomeOut, LowCostDietOut, LowCostDietHealthOutcomeOut, RecommendedMacronutrientsIntakeOut, IngredientSubstitutesOut
from src.services.ingredient_substitution import engine as substitution_engine, SubstituteResult
from src.services.nearby_search import DEFAULT_KEYWORDS, find_nearby_support_services, search_support_service_suburbs
from src.utils.opening_hours import is_open_now, _now_in_tz

from sqlalchemy import func, Integer, case, distinct, Numeric
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_AsGeoJSON
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Aegis Support Services API", version="0.1.0")

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
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
    # Ensure tables exist; seeding is handled elsewhere
    Base.metadata.create_all(bind=engine)
    logger.info("API startup complete; database ready.")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


class _LoginRequest(BaseModel):
    password: str

_DEMO_PASSWORD = "password123"

class LatLng(BaseModel):
    lat: float
    lng: float

class TransitRouteRequest(BaseModel):
    origin: LatLng
    destination: LatLng

@app.post("/google/transit-route")
def get_google_transit_route(body: TransitRouteRequest):
    api_key = os.getenv("GOOGLE_ROUTES_API_KEY")

    if not api_key:
        raise HTTPException(status_code=500, detail="GOOGLE_ROUTES_API_KEY is missing")

    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    payload = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": body.origin.lat,
                    "longitude": body.origin.lng,
                }
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": body.destination.lat,
                    "longitude": body.destination.lng,
                }
            }
        },
        "travelMode": "TRANSIT",
        "computeAlternativeRoutes": False,
        "languageCode": "en-AU",
        "units": "METRIC",
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": (
            "routes.duration,"
            "routes.distanceMeters,"
            "routes.legs.steps.polyline.encodedPolyline,"
            "routes.legs.steps.travelMode,"
            "routes.legs.steps.navigationInstruction,"
            "routes.legs.steps.localizedValues,"
            "routes.legs.steps.transitDetails"
        ),
    }

    try:
        google_response = requests.post(url, json=payload, headers=headers, timeout=15)

        print("GOOGLE ROUTES STATUS:", google_response.status_code)
        print("GOOGLE ROUTES RESPONSE:", google_response.text)

        if google_response.status_code != 200:
            raise HTTPException(
                status_code=google_response.status_code,
                detail=google_response.json(),
            )

        return google_response.json()

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to fetch Google transit route: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to fetch Google transit route")

@app.post("/auth/login")
def auth_login(body: _LoginRequest):
    if body.password == _DEMO_PASSWORD:
        return {"success": True}
    raise HTTPException(status_code=401, detail="Incorrect password")


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
        rows = [
            row for row in db.query(SupportService).all()
            if (
                row.latitude is not None
                and row.longitude is not None
                and isinstance(row.latitude, (int, float))
                and isinstance(row.longitude, (int, float))
                and math.isfinite(row.latitude)
                and math.isfinite(row.longitude)
            )
        ]

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

@app.get("/services/search-locations")
def search_locations(
    q: str = Query("", description="Search suburb"),
    limit: int = Query(8, ge=1, le=20),
    db: Session = Depends(get_db),
):
    try:
        return search_support_service_suburbs(
            db=db,
            q=q,
            limit=limit,
        )

    except Exception as exc:
        logger.exception("Failed to search locations: %s", exc)

        raise HTTPException(
            status_code=500,
            detail="Internal error searching locations",
        )

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
    
@app.get("/search-address")
def search_address(q: str = Query(..., min_length=3)):
    api_key = os.getenv("GOOGLE_ROUTES_API_KEY")

    if not api_key:
        raise HTTPException(status_code=500, detail="Google Maps API key is missing")

    try:
        url = "https://places.googleapis.com/v1/places:autocomplete"

        payload = {
            "input": q,
            "locationRestriction": {
                "rectangle": {
                    "low": {
                        "latitude": -39.2,
                        "longitude": 140.9,
                    },
                    "high": {
                        "latitude": -33.9,
                        "longitude": 150.1,
                    },
                }
            },
            "languageCode": "en-AU",
            "regionCode": "AU",
        }

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)

        print("GOOGLE PLACES STATUS:", response.status_code)
        print("GOOGLE PLACES RESPONSE:", response.text[:500])

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json(),
            )

        data = response.json()

        suggestions = []

        for item in data.get("suggestions", []):
            prediction = item.get("placePrediction")
            if not prediction:
                continue

            place_id = prediction.get("placeId")
            label = prediction.get("text", {}).get("text")

            if place_id and label:
                suggestions.append(
                    {
                        "place_id": place_id,
                        "display_name": label,
                    }
                )

        return suggestions

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to search address: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to search address")
    
@app.get("/place-details")
def place_details(place_id: str = Query(...)):
    api_key = os.getenv("GOOGLE_ROUTES_API_KEY")

    if not api_key:
        raise HTTPException(status_code=500, detail="Google Maps API key is missing")

    try:
        url = f"https://places.googleapis.com/v1/places/{place_id}"

        headers = {
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "id,displayName,formattedAddress,location",
        }

        response = requests.get(url, headers=headers, timeout=10)

        print("GOOGLE PLACE DETAILS STATUS:", response.status_code)
        print("GOOGLE PLACE DETAILS RESPONSE:", response.text[:500])

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json(),
            )

        data = response.json()
        location = data.get("location", {})

        return {
            "place_id": data.get("id"),
            "display_name": data.get("formattedAddress")
            or data.get("displayName", {}).get("text"),
            "lat": location.get("latitude"),
            "lon": location.get("longitude"),
        }

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to fetch place details: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to fetch place details")
