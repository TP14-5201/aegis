from typing import List, Optional, Any, Union
import math

from pydantic import BaseModel, Field, validator


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
    food_insecurity_pct: float = 0.0
    pop_2024_total: Optional[int] = None
    emergency_services_count: int = 0


class LgaFoodInaccessibilityReasonsOut(BaseModel):
    lga_pid: str
    limited_variety: Union[float, str]
    too_expensive: Union[float, str]
    wrong_quality: Union[float, str]
    transport_gap: Union[float, str]


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


class RecommendedMacronutrientsIntakeOut(BaseModel):
    id: int
    age: str
    nutrient: str
    goal: str
    portion_guide: str
    rationale_summary: str
    actionable_guidance: str

    class Config:
        from_attributes = True


class SubstituteSlotOut(BaseModel):
    """A single ingredient substitution candidate."""

    ingredient_code: str
    product_name: str
    brands: Optional[str] = None
    sub_category: Optional[str] = None
    health_benefits: Optional[List[str]] = None
    dietary_tags: Optional[List[str]] = None
    retail_price: Optional[float] = None
    nutrition_grade: Optional[str] = None
    proteins_100g: Optional[float] = None
    fat_100g: Optional[float] = None
    carbohydrates_100g: Optional[float] = None
    energy_100g: Optional[float] = None
    similarity_score: float = Field(
        ...,
        description="Cosine-similarity-based ANN distance to the query ingredient",
    )
    objective_score: float = Field(
        ...,
        description="Score on the objective that selected this candidate (0–1)",
    )

    @validator("sub_category", "brands", pre=True)
    def handle_nan(cls, v: Any) -> Optional[str]:
        # If the value is a float and is NaN, return None
        if isinstance(v, float) and math.isnan(v):
            return None
        return v


class IngredientSubstitutesOut(BaseModel):
    """
    Response envelope for GET /ingredients/{ingredient_code}/substitutes.

    Contains three curated alternatives, one per optimisation goal.
    Any slot may be null if there are insufficient culinary-valid candidates.
    """

    query_code: str
    query_name: str
    budget: Optional[SubstituteSlotOut] = Field(
        None,
        description="Cheapest culinary-valid alternative",
    )
    nutrition: Optional[SubstituteSlotOut] = Field(
        None,
        description="Highest-nutrition (Nutri-Score + protein) alternative",
    )
    balanced: Optional[SubstituteSlotOut] = Field(
        None,
        description="Best price-to-nutrition trade-off alternative",
    )
    error: Optional[str] = Field(
        None,
        description="Set when the engine cannot produce results",
    )
