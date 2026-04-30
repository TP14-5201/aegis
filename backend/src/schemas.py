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
    distance_km: Optional[float] = Field(None, description="Distance from the user in kilometers")


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


class LgaStatsOut(BaseModel):
    lga_name: Optional[str] = None
    men_pct: float = 0.0
    women_pct: float = 0.0
    pop_2024_total: Optional[int] = None
    emergency_services_count: int = 0


class DietIndicatorOut(BaseModel):
    category: str
    indicator_response: str
    worried_pct: float
    worried_95ci_ll: float
    worried_95ci_ul: float
    not_worried_pct: float
    not_worried_95ci_ll: float
    not_worried_95ci_ul: float

    class Config:
        from_attributes = True


class HealthOutcomeOut(BaseModel):
    category: str
    health_outcome: str
    insecure_hunger_pct: float
    insecure_hunger_95ci_ll: float
    insecure_hunger_95ci_ul: float
    food_secure_pct: float
    food_secure_95ci_ll: float
    food_secure_95ci_ul: float

    class Config:
        from_attributes = True


class LowCostDietOut(BaseModel):
    category: str
    indicator_response: str
    relied_lowcost_yes_pct: float
    relied_lowcost_yes_95ci_ll: float
    relied_lowcost_yes_95ci_ul: float
    relied_lowcost_no_pct: float
    relied_lowcost_no_95ci_ll: float
    relied_lowcost_no_95ci_ul: float

    class Config:
        from_attributes = True


class LowCostDietHealthOutcomeOut(BaseModel):
    category: str
    health_outcome: str
    relied_lowcost_yes_pct: float
    relied_lowcost_yes_95ci_ll: float
    relied_lowcost_yes_95ci_ul: float
    relied_lowcost_no_pct: float
    relied_lowcost_no_95ci_ll: float
    relied_lowcost_no_95ci_ul: float

    class Config:
        from_attributes = True