from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
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