import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class IncidentSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(str, enum.Enum):
    REPORTED = "reported"
    ACTIVE = "active"
    CONTAINED = "contained"
    RESOLVED = "resolved"


class ResourceStatus(str, enum.Enum):
    AVAILABLE = "available"
    DEPLOYED = "deployed"
    UNAVAILABLE = "unavailable"


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    severity = Column(Enum(IncidentSeverity), default=IncidentSeverity.MEDIUM, nullable=False)
    status = Column(Enum(IncidentStatus), default=IncidentStatus.REPORTED, nullable=False)
    affected_population = Column(Integer, default=0)
    reported_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    resources = relationship("ResourceDeployment", back_populates="incident", cascade="all, delete-orphan")


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)  # e.g. "rescue_team", "vehicle", "medical_unit"
    quantity = Column(Integer, default=1, nullable=False)
    unit = Column(String(50), nullable=True)  # e.g. "units", "personnel", "kits"
    location = Column(String(255), nullable=True)
    status = Column(Enum(ResourceStatus), default=ResourceStatus.AVAILABLE, nullable=False)
    contact_info = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    deployments = relationship("ResourceDeployment", back_populates="resource")


class ResourceDeployment(Base):
    """Junction table tracking which resources are deployed to which incidents."""
    __tablename__ = "resource_deployments"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    quantity_deployed = Column(Integer, default=1, nullable=False)
    deployed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    recalled_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    incident = relationship("Incident", back_populates="resources")
    resource = relationship("Resource", back_populates="deployments")
