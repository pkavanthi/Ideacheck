from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Column, DateTime, Enum, Float, Integer, String, Text, create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings

# ---------------------------------------------------------------------------
# Database bootstrap
# ---------------------------------------------------------------------------
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------
class HazardType(str, PyEnum):
    FLOOD = "flood"
    CYCLONE = "cyclone"
    EARTHQUAKE = "earthquake"
    HEATWAVE = "heatwave"


class SeverityLevel(str, PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class ClimateRiskEvent(Base):
    """Represents a recorded climate-risk event."""

    __tablename__ = "climate_risk_events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    hazard_type = Column(Enum(HazardType), nullable=False)
    severity = Column(Enum(SeverityLevel), nullable=False)
    location = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    affected_population = Column(Integer, nullable=True)
    reported_by = Column(String(255), nullable=True)  # authority / organisation
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class RiskAlert(Base):
    """Active alert issued by a disaster management authority."""

    __tablename__ = "risk_alerts"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, nullable=True)          # optional link to an event
    hazard_type = Column(Enum(HazardType), nullable=False)
    severity = Column(Enum(SeverityLevel), nullable=False)
    region = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    issued_by = Column(String(255), nullable=True)
    active = Column(Integer, default=1)                # 1 = active, 0 = resolved
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def get_db():
    """FastAPI dependency – yields a DB session and ensures it is closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables (called once at startup)."""
    Base.metadata.create_all(bind=engine)
