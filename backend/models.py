from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum
from datetime import datetime
import enum
from backend.database import Base

class ThreatLevel(str, enum.Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class IncidentStatus(str, enum.Enum):
    REPORTED = "REPORTED"
    ACTIVE = "ACTIVE"
    CONTAINED = "CONTAINED"
    RESOLVED = "RESOLVED"

class ResourceType(str, enum.Enum):
    RESCUE_BOAT = "RESCUE_BOAT"
    MEDICAL_KIT = "MEDICAL_KIT"
    FOOD_RATION = "FOOD_RATION"
    SHELTER_KIT = "SHELTER_KIT"
    WATER_PUMP = "WATER_PUMP"
    PERSONNEL = "PERSONNEL"

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    district = Column(String(100), nullable=False, index=True)
    location_name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    threat_level = Column(String(50), default=ThreatLevel.HIGH.value, nullable=False)
    status = Column(String(50), default=IncidentStatus.ACTIVE.value, nullable=False)
    description = Column(Text, nullable=True)
    affected_population = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ReliefResource(Base):
    __tablename__ = "relief_resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    resource_type = Column(String(50), default=ResourceType.RESCUE_BOAT.value, nullable=False)
    district = Column(String(100), nullable=False, index=True)
    quantity = Column(Integer, default=0, nullable=False)
    available_quantity = Column(Integer, default=0, nullable=False)
    location_hub = Column(String(255), nullable=False)
    status = Column(String(50), default="AVAILABLE")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
