from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from src.database import Base


class SupportService(Base):
    __tablename__ = "support_services"

    id = Column(Integer, primary_key=True, index=True)
    lga_pid = Column(String, index=True)     # FK → vic_lga_boundaries.lga_pid
    name = Column(String, index=True)
    description = Column(String)
    target_audience = Column(String)
    address = Column(String)
    suburb = Column(String)
    primary_phone = Column(String)
    phone_display = Column(String)
    email = Column(String)
    website = Column(String)
    social_media = Column(String)
    opening_hours = Column(JSON)
    cost = Column(String)
    tram_routes = Column(String)
    bus_routes = Column(String)
    nearest_train_station = Column(String)
    categories = Column(JSON)
    longitude = Column(Float)
    latitude = Column(Float)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FoodInsecurity(Base):
    __tablename__ = "food_insecurity"

    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String)
    indicator = Column(String)
    indicator_category = Column(String)
    lga_pid = Column(String, index=True)     # FK → vic_lga_boundaries.lga_pid
    subpopulation = Column(String)
    estimate_pct = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    

class VicLgaBoundary(Base):
    __tablename__ = "vic_lga_boundaries"

    lga_pid = Column(String, primary_key=True, index=True)
    lga_name = Column(String)
    geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LgaPopulation(Base):
    __tablename__ = "vic_lga_population"

    lga_pid = Column(String, primary_key=True, index=True)
    lga_name = Column(String)
    pop_2024_total = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DietIndicator(Base):
    __tablename__ = "diet_indicator"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    indicator_response = Column(String)
    worried_pct = Column(Float)
    worried_95ci_ll = Column(Float)
    worried_95ci_ul = Column(Float)
    not_worried_pct = Column(Float)
    not_worried_95ci_ll = Column(Float)
    not_worried_95ci_ul = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class HealthOutcome(Base):
    __tablename__ = "health_outcomes"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    health_outcome = Column(String)
    insecure_hunger_pct = Column(Float)
    insecure_hunger_95ci_ll = Column(Float)
    insecure_hunger_95ci_ul = Column(Float)
    food_secure_pct = Column(Float)
    food_secure_95ci_ll = Column(Float)
    food_secure_95ci_ul = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LowCostDiet(Base):
    __tablename__ = "low_cost_diet"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    indicator_response = Column(String)
    relied_lowcost_yes_pct = Column(Float)
    relied_lowcost_yes_95ci_ll = Column(Float)
    relied_lowcost_yes_95ci_ul = Column(Float)
    relied_lowcost_no_pct = Column(Float)
    relied_lowcost_no_95ci_ll = Column(Float)
    relied_lowcost_no_95ci_ul = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class LowCostDietHealthOutcome(Base):
    __tablename__ = "low_cost_diet_health_outcome"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    health_outcome = Column(String)
    relied_lowcost_yes_pct = Column(Float)
    relied_lowcost_yes_95ci_ll = Column(Float)
    relied_lowcost_yes_95ci_ul = Column(Float)
    relied_lowcost_no_pct = Column(Float)
    relied_lowcost_no_95ci_ll = Column(Float)
    relied_lowcost_no_95ci_ul = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RecommendedMacronutrientsIntake(Base):
    __tablename__ = "recommended_macronutrients_intake"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(String)
    nutrient = Column(String)
    goal = Column(String)
    portion_guide = Column(String)
    rationale_summary = Column(String)
    actionable_guidance = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ---------------------------------------------------------------------------
# ChereBowl grocery recommendation models
# ---------------------------------------------------------------------------

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)             # e.g. "Meat & seafood", "Fruit & vegetables"
    pack_label = Column(String)           # e.g. "500g pack", "1 bulb", "400g tin"
    pack_grams = Column(Float)            # normalised gram weight of the pack
    price_aud = Column(Float)             # snapshot price (AUD)
    price_per_100g = Column(Float)
    price_source = Column(String)         # "open_food_facts" | "manual_snapshot"
    price_as_of = Column(String)          # ISO date of snapshot
    benefit_tags = Column(JSON)           # list[ChildBenefit], e.g. ["Energy", "Brain"]
    source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    nutrients = relationship("IngredientNutrient", back_populates="ingredient", cascade="all, delete-orphan")
    substitute_links = relationship("IngredientSubstitute", foreign_keys="IngredientSubstitute.ingredient_id", back_populates="ingredient", cascade="all, delete-orphan")
    dish_links = relationship("DishIngredient", back_populates="ingredient")


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cuisine = Column(String, index=True)
    base_servings = Column(Integer, default=4)
    dietary_flags = Column(JSON)          # list[str], e.g. ["vegetarian", "gluten-free"]
    source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    raw_ingredients = Column(JSON)          # original ingredient name list from Yummly
    ingredient_links = relationship("DishIngredient", back_populates="dish", cascade="all, delete-orphan")


class DishIngredient(Base):
    __tablename__ = "dish_ingredients"

    id = Column(Integer, primary_key=True, index=True)
    dish_id = Column(Integer, ForeignKey("dishes.id"), nullable=False, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False, index=True)
    quantity_g = Column(Float)
    is_optional = Column(Boolean, default=False)

    dish = relationship("Dish", back_populates="ingredient_links")
    ingredient = relationship("Ingredient", back_populates="dish_links")


class IngredientNutrient(Base):
    __tablename__ = "ingredient_nutrients"

    id = Column(Integer, primary_key=True, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False, index=True)
    nutrient_name = Column(String)        # canonical name, e.g. "protein", "vitamin_c"
    amount_per_100g = Column(Float)
    unit = Column(String)

    ingredient = relationship("Ingredient", back_populates="nutrients")


class IngredientSubstitute(Base):
    __tablename__ = "ingredient_substitutes"

    id = Column(Integer, primary_key=True, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False, index=True)
    substitute_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False, index=True)
    similarity_score = Column(Float)
    reason = Column(String)               # "cheaper" | "healthier" | "dietary_swap" | "availability"
    source = Column(String)

    ingredient = relationship("Ingredient", foreign_keys=[ingredient_id], back_populates="substitute_links")
    substitute = relationship("Ingredient", foreign_keys=[substitute_id])
