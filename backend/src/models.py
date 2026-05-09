from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, PrimaryKeyConstraint
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


class Recipe(Base):
    __tablename__ = "recipe"
 
    recipe_id = Column(String, primary_key=True, index=True)
    country = Column(String)
 
    ingredients = relationship("RecipeIngredient", back_populates="recipe")


class Ingredient(Base):
    __tablename__ = "ingredient"

    ingredient_code = Column(String, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    brands = Column(String)
    main_category = Column(String)

    nutrition = relationship("Nutrition", back_populates="ingredient", uselist=False)
    recipes = relationship("RecipeIngredient", back_populates="ingredient_info")


class Nutrition(Base):
    __tablename__ = "nutrition"
 
    ingredient_code = Column(String, ForeignKey("ingredient.ingredient_code"), primary_key=True, index=True)
    nutrition_grade_fr = Column(String)
    energy_100g = Column(Float)
    proteins_100g = Column(Float)
    carbohydrates_100g = Column(Float)
    fat_100g = Column(Float)

    ingredient = relationship("Ingredient", back_populates="nutrition")


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredient"

    recipe_id = Column(String, ForeignKey("recipe.recipe_id"), index=True)
    ingredient_code = Column(String, ForeignKey("ingredient.ingredient_code"), index=True)

    __table_args__ = (
        PrimaryKeyConstraint("recipe_id", "ingredient_code"),
    )

    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient_info = relationship("Ingredient", back_populates="recipes")


class IngredientPrice(Base):
    __tablename__ = "ingredient_price"

    ingredient_code = Column(String, ForeignKey("ingredient.ingredient_code"), index=True, primary_key=True)
    sub_category = Column(String)
    retail_price = Column(Float)
    
