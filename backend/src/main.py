from __future__ import annotations

import json
from typing import List, Optional
import math
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query

from src.core.logging import logger
from src.database import Base, engine, get_db
from src.models import VicBoundary, FoodInsecurity, VicLgaBoundary
from src.schemas import NearbyServiceOut, FoodInsecurityRegion
from src.services.nearby_search import DEFAULT_KEYWORDS, find_nearby_support_services
from src.utils.opening_hours import is_open_now, _now_in_tz

from sqlalchemy import func, Integer
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_AsGeoJSON


app = FastAPI(title="Aegis Support Services API", version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    # Ensure tables exist; seeding is handled elsewhere
    Base.metadata.create_all(bind=engine)
    logger.info("API startup complete; database ready.")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


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
        results = [r for r in results if r.get("is_open_now") is True]
        return results
    except Exception as exc:
        logger.exception("Failed to fetch nearby services: %s", exc)
        raise HTTPException(status_code=500, detail="Internal error while searching for services")


@app.get("/boundaries/phu")
def get_phu_boundaries(db: Session = Depends(get_db)):
    results = db.query(
        VicBoundary.vicgov_region_code,
        ST_AsGeoJSON(VicBoundary.geometry).label("geometry")
    ).all()

    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"code": r.vicgov_region_code},
                "geometry": json.loads(r.geometry) # Convert string to JSON object
            } for r in results
        ]
    }


@app.get("/boundaries/lga/{phu_code}")
def get_lga_boundaries(phu_code: int, db: Session = Depends(get_db)):
    results = (
        db.query(
            VicLgaBoundary.lga_name,
            ST_AsGeoJSON(VicLgaBoundary.geometry).label("geometry")
        )
        .join(FoodInsecurity, VicLgaBoundary.lga_name == FoodInsecurity.subpopulation)
        .filter(FoodInsecurity.vic_region_code == phu_code)
        .distinct(VicLgaBoundary.lga_name) # One polygon per suburb
        .all()
    )

    if not results:
        return {"type": "FeatureCollection", "features": [], "message": "No boundaries found"}

    # Construct the GeoJSON FeatureCollection
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "lga_name": r.lga_name,
                },
                "geometry": json.loads(r.geometry)
            } for r in results
        ]
    }


@app.get("/food-insecurity/all-data")
def get_all_food_data(db: Session = Depends(get_db)):
    results = db.query(
        FoodInsecurity.subpopulation,
        FoodInsecurity.vic_region_code,
        FoodInsecurity.gender,
        FoodInsecurity.indicator,
        FoodInsecurity.indicator_category,
        FoodInsecurity.estimate_pct
    ).all()
    
    return [
        {
            "subpopulation": r.subpopulation,
            "vic_region_code": r.vic_region_code,
            "gender": r.gender,
            "indicator": r.indicator,
            "indicator_category": r.indicator_category,
            "estimate_pct": r.estimate_pct
        } for r in results
    ]