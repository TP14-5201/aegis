from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from src.database import Base


class SupportService(Base):
    __tablename__ = "support_services"

    id = Column(Integer, primary_key=True, index=True)
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
