from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Boolean,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class HazardType(str, PyEnum):
    FLOOD = "flood"
    CYCLONE = "cyclone"
    EARTHQUAKE = "earthquake"
    DROUGHT = "drought"
    HEATWAVE = "heatwave"
    OTHER = "other"


class AlertSeverity(str, PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, PyEnum):
    ACTIVE = "active"
    RESOLVED = "resolved"
    CANCELLED = "cancelled"


class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False)
    district_code = Column(String(20), unique=True, nullable=False, index=True)
    population = Column(Integer, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    collector_name = Column(String(150), nullable=True)
    collector_contact = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    alerts = relationship("Alert", back_populates="district", cascade="all, delete-orphan")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    hazard_type = Column(Enum(HazardType), nullable=False)
    severity = Column(Enum(AlertSeverity), nullable=False, default=AlertSeverity.MEDIUM)
    status = Column(Enum(AlertStatus), nullable=False, default=AlertStatus.ACTIVE)
    affected_population = Column(Integer, nullable=True)
    evacuation_required = Column(Boolean, default=False)
    evacuation_zones = Column(Text, nullable=True)  # JSON string of zone names
    issued_by = Column(String(150), nullable=True)
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    district = relationship("District", back_populates="alerts")
