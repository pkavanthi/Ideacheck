"""
Database models for Rural India Village Health Monitor.
Key entities: Village, HealthRecord, ASHAWorker
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    DateTime, ForeignKey, Text, Enum
)
from sqlalchemy.orm import relationship, DeclarativeBase
import enum


class Base(DeclarativeBase):
    pass


class StateEnum(str, enum.Enum):
    ANDHRA_PRADESH = "Andhra Pradesh"
    BIHAR = "Bihar"
    CHHATTISGARH = "Chhattisgarh"
    GUJARAT = "Gujarat"
    JHARKHAND = "Jharkhand"
    KARNATAKA = "Karnataka"
    MADHYA_PRADESH = "Madhya Pradesh"
    MAHARASHTRA = "Maharashtra"
    ODISHA = "Odisha"
    RAJASTHAN = "Rajasthan"
    UTTAR_PRADESH = "Uttar Pradesh"
    WEST_BENGAL = "West Bengal"
    OTHER = "Other"


class Village(Base):
    """Represents a rural village unit being monitored."""

    __tablename__ = "villages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    district = Column(String(200), nullable=False, index=True)
    state = Column(String(100), nullable=False, index=True)
    block = Column(String(200))                    # administrative block
    gram_panchayat = Column(String(200))           # gram panchayat name
    population = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    phc_name = Column(String(200))                 # linked Primary Health Centre
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    asha_workers = relationship("ASHAWorker", back_populates="village", cascade="all, delete-orphan")
    health_records = relationship("HealthRecord", back_populates="village", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Village id={self.id} name={self.name!r} district={self.district!r}>"


class ASHAWorker(Base):
    """Accredited Social Health Activist assigned to a village."""

    __tablename__ = "asha_workers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    phone = Column(String(15), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, index=True)
    village_id = Column(Integer, ForeignKey("villages.id", ondelete="SET NULL"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    village = relationship("Village", back_populates="asha_workers")
    health_records = relationship("HealthRecord", back_populates="reported_by")

    def __repr__(self) -> str:
        return f"<ASHAWorker id={self.id} name={self.name!r}>"


class HealthRecord(Base):
    """Health observation/metric reported for a village."""

    __tablename__ = "health_records"

    id = Column(Integer, primary_key=True, index=True)
    village_id = Column(Integer, ForeignKey("villages.id", ondelete="CASCADE"), nullable=False, index=True)
    reported_by_id = Column(Integer, ForeignKey("asha_workers.id", ondelete="SET NULL"), nullable=True)

    # Observation fields
    record_date = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    category = Column(
        String(100), nullable=False, index=True
    )  # e.g., "maternal_health", "immunisation", "nutrition", "disease_outbreak"
    indicator = Column(String(200), nullable=False)   # specific metric name
    value = Column(Float)
    unit = Column(String(50))                         # e.g., "count", "percent", "per 1000"
    notes = Column(Text)
    is_gap_detected = Column(Boolean, default=False, nullable=False)  # AI/rule-flagged gap

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    village = relationship("Village", back_populates="health_records")
    reported_by = relationship("ASHAWorker", back_populates="health_records")

    def __repr__(self) -> str:
        return (
            f"<HealthRecord id={self.id} village_id={self.village_id} "
            f"category={self.category!r} indicator={self.indicator!r}>"
        )
