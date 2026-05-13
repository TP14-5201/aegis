from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from src.database import Base


class LgaPopulation(Base):
    """Moved above VicLgaBoundary because VicLgaBoundary now FKs into it."""
    __tablename__ = "vic_lga_population"

    lga_pid = Column(String, primary_key=True, index=True)
    lga_name = Column(String)
    pop_2024_total = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    lga_boundary = relationship("VicLgaBoundary", back_populates="population", uselist=False)


class VicLgaBoundary(Base):
    __tablename__ = "vic_lga_boundaries"

    lga_pid = Column(String, ForeignKey("vic_lga_population.lga_pid"), primary_key=True, index=True)  # FK → vic_lga_population
    lga_name = Column(String)
    geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to parent population record
    population = relationship("LgaPopulation", back_populates="lga_boundary")

    # Back-references from child tables
    support_services = relationship("SupportService", back_populates="lga")
    food_insecurity_records = relationship("FoodInsecurity", back_populates="lga")
    food_inaccessibility_reasons = relationship("FoodInaccessibilityReasons", back_populates="lga")


class SupportService(Base):
    __tablename__ = "support_services"

    id = Column(Integer, primary_key=True, index=True)
    lga_pid = Column(String, ForeignKey("vic_lga_boundaries.lga_pid"), index=True)
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

    lga = relationship("VicLgaBoundary", back_populates="support_services")


class FoodInsecurity(Base):
    __tablename__ = "food_insecurity"

    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String)
    indicator = Column(String)
    indicator_category = Column(String)
    lga_pid = Column(String, ForeignKey("vic_lga_boundaries.lga_pid"), index=True)
    subpopulation = Column(String)
    estimate_pct = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    lga = relationship("VicLgaBoundary", back_populates="food_insecurity_records")



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


class FoodInaccessibilityReasons(Base):
    __tablename__ = "food_inaccessibility_reasons"

    id = Column(Integer, primary_key=True, index=True)
    lga_pid = Column(String, ForeignKey("vic_lga_boundaries.lga_pid"), index=True)
    limited_variety = Column(Float)
    too_expensive = Column(Float)
    wrong_quality = Column(Float)
    transport_gap = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    lga = relationship("VicLgaBoundary", back_populates="food_inaccessibility_reasons")


class Ingredient(Base):
    __tablename__ = "ingredient"

    ingredient_code = Column(String, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    sub_category = Column(String, nullable=False)
    retail_price = Column(Float, nullable=False)

    ingredient_nutrition = relationship("IngredientNutrition", back_populates="ingredient", uselist=False)


class IngredientNutrition(Base):
    __tablename__ = "ingredient_nutrition"

    ingredient_code = Column(String, ForeignKey("ingredient.ingredient_code"), primary_key=True, index=True)
    protein_g = Column(Float)
    fat_total_g = Column(Float)
    total_dietary_fibre_g = Column(Float)
    total_sugars_g = Column(Float)
    available_carbohydrate_without_sugar_alcohols_g = Column(Float)
    sodium_na_mg = Column(Float)

    ingredient = relationship("Ingredient", back_populates="ingredient_nutrition")