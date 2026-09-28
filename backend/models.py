from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker

from backend.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Incident(Base):
    """Disaster incident reported by field or district officers."""

    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    hazard_type = Column(String(100), nullable=False)  # flood, earthquake, cyclone, etc.
    severity = Column(String(20), default=SeverityLevel.MEDIUM, nullable=False)
    status = Column(String(20), default=IncidentStatus.OPEN, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    district = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    reported_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    resources = relationship("ResourceDeployment", back_populates="incident", cascade="all, delete-orphan")


class ResourceDeployment(Base):
    """Resources (NDRF teams, hospitals, equipment) deployed for an incident."""

    __tablename__ = "resource_deployments"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    resource_type = Column(String(100), nullable=False)  # ndrf_team, hospital, equipment
    resource_name = Column(String(255), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    deployed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    notes = Column(Text, nullable=True)

    incident = relationship("Incident", back_populates="resources")


def get_db():
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)
