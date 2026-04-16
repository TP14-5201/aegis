from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

from sqlalchemy import String, and_, cast, or_
from sqlalchemy.orm import Session

from src.models import SupportService

# Keywords that typically indicate food banks or welfare/relief services
DEFAULT_KEYWORDS: List[str] = []  # Empty = return all services in radius


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two points on Earth (km)."""
    R = 6371.0088  # mean Earth radius in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = phi2 - phi1
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def _bounding_box(lat: float, lon: float, radius_km: float) -> tuple[float, float, float, float]:
    """Return (lat_min, lat_max, lon_min, lon_max) for a radius around a point.

    Uses a quick degrees-per-km approximation to prefilter rows in SQL.
    """
    # ~111.32 km per degree latitude
    lat_delta = radius_km / 111.32

    # Guard against extreme latitudes where cos approaches 0
    cos_lat = max(0.01, math.cos(math.radians(lat)))
    lon_delta = radius_km / (111.32 * cos_lat)

    return (lat - lat_delta, lat + lat_delta, lon - lon_delta, lon + lon_delta)


def _keyword_filter(keywords: List[str]):
    """Build a SQLAlchemy OR filter across name/description/categories."""
    terms = []
    for kw in keywords:
        like = f"%{kw}%"
        terms.append(SupportService.name.ilike(like))
        terms.append(SupportService.description.ilike(like))
        # categories is JSON; cast to string for a simple contains check (works on SQLite/Postgres)
        terms.append(cast(SupportService.categories, String).ilike(like))
    return or_(*terms) if terms else None


def find_nearby_support_services(
    db: Session,
    user_lat: float,
    user_lon: float,
    radius_km: float = 5.0,
    *,
    limit: int = 50,
    keywords: Optional[List[str]] = None,
    include_datagov: bool = True,
) -> List[Dict[str, Any]]:
    """Find nearby support services within a radius.

    - Prefilters by a bounding box in SQL for performance, then computes exact
      haversine distances in Python and sorts/limits.
    - If keywords is provided, matches against name/description/categories.
      When include_datagov=True, always includes DataGov rows (many lack categories)
      that fall within the radius.
    """
    if keywords is None:
        keywords = DEFAULT_KEYWORDS

    lat_min, lat_max, lon_min, lon_max = _bounding_box(user_lat, user_lon, radius_km)

    base_filters = [
        SupportService.latitude.isnot(None),
        SupportService.longitude.isnot(None),
        SupportService.latitude.between(lat_min, lat_max),
        SupportService.longitude.between(lon_min, lon_max),
    ]

    query = db.query(SupportService).filter(and_(*base_filters))

    kw_filter = _keyword_filter(keywords)
    if kw_filter is not None:
        if include_datagov:
            query = query.filter(or_(kw_filter, SupportService.source == "DataGov"))
        else:
            query = query.filter(kw_filter)

    rows: List[SupportService] = query.all()

    results: List[Dict[str, Any]] = []
    for row in rows:
        # Defensive: some rows may have nulls; skip if so
        if row.latitude is None or row.longitude is None:
            continue
        dist = haversine_km(user_lat, user_lon, row.latitude, row.longitude)
        if dist <= radius_km + 1e-6:  # final precise filter
            results.append(
                {
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
                    "opening_hours": row.opening_hours,
                    "cost": row.cost,
                    "tram_routes": row.tram_routes,
                    "bus_routes": row.bus_routes,
                    "nearest_train_station": row.nearest_train_station,
                    "categories": row.categories,
                    "longitude": row.longitude,
                    "latitude": row.latitude,
                    "source": row.source,
                    "distance_km": round(dist, 3),
                }
            )

    results.sort(key=lambda x: x["distance_km"])  # nearest first
    return results[: max(0, limit)]
