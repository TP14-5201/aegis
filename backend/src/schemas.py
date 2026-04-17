from typing import List, Optional, Any

from pydantic import BaseModel, Field


class NearbyServiceOut(BaseModel):
    is_open_now: Optional[bool] = None
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    target_audience: Optional[str] = None
    address: Optional[str] = None
    suburb: Optional[str] = None
    primary_phone: Optional[str] = None
    phone_display: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    social_media: Optional[str] = None
    opening_hours: Optional[dict] = None
    cost: Optional[str] = None
    tram_routes: Optional[str] = None
    bus_routes: Optional[str] = None
    nearest_train_station: Optional[str] = None
    categories: Optional[List[str]] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    source: Optional[str] = None
    distance_km: float = Field(..., description="Distance from the user in kilometers")


class FoodInsecurityRegion(BaseModel):
    ufi: int
    vicgov_region_code: str
    vicgov_region_sname: str
    vicgov_region: str
    indicator: str
    indicator_category: str
    vic_region_code: int
    estimate_pct: float
    geometry: Any  # GeoJSON dict

    class Config:
        from_attributes = True