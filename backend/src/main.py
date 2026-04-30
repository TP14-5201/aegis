from __future__ import annotations

import json
from typing import List, Optional
import math
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from src.core.logging import logger
from src.database import Base, engine, get_db
from src.models import LgaPopulation, FoodInsecurity, VicLgaBoundary, SupportService
from src.schemas import NearbyServiceOut, FoodInsecurityRegion, LgaStatsOut
from src.services.nearby_search import DEFAULT_KEYWORDS, find_nearby_support_services
from src.utils.opening_hours import is_open_now, _now_in_tz

from sqlalchemy import func, Integer, case, distinct, Numeric
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_AsGeoJSON


app = FastAPI(title="Aegis Support Services API", version="0.1.0")

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Production
    "https://cherebowl.vercel.app",
    # Archived version
    "https://cherebowl-v1.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET"],
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
            return {
                "type": "FeatureCollection",
                "features": [],
                "message": "No boundaries found",
            }

        return {"type": "FeatureCollection", "features": features}
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

