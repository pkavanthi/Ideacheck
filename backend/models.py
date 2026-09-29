from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Column, DateTime, Enum, Float, ForeignKey,
    Integer, String, Text, func,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class IncidentSeverity(str, PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(str, PyEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class ResourceType(str, PyEnum):
    PERSONNEL = "personnel"
    VEHICLE = "vehicle"
    EQUIPMENT = "equipment"
    MEDICAL = "medical"
    FOOD = "food"
    WATER = "water"
    SHELTER = "shelter"
    OTHER = "other"


class ResourceStatus(str, PyEnum):
    AVAILABLE = "available"
    DEPLOYED = "deployed"
    UNAVAILABLE = "unavailable"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class Incident(Base):
    """A disaster incident reported in the field."""

    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(500), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    severity = Column(Enum(IncidentSeverity), nullable=False, default=IncidentSeverity.MEDIUM)
    status = Column(Enum(IncidentStatus), nullable=False, default=IncidentStatus.OPEN)
    reported_by = Column(String(255), nullable=True)
    affected_count = Column(Integer, nullable=True, default=0)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    resource_deployments = relationship("ResourceDeployment", back_populates="incident")


class Resource(Base):
    """A relief resource (personnel, vehicle, equipment, etc.)."""

    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    resource_type = Column(Enum(ResourceType), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    status = Column(Enum(ResourceStatus), nullable=False, default=ResourceStatus.AVAILABLE)
    location = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    contact_info = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    resource_deployments = relationship("ResourceDeployment", back_populates="resource")


class ResourceDeployment(Base):
    """Tracks which resources are deployed to which incidents."""

    __tablename__ = "resource_deployments"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id", ondelete="CASCADE"), nullable=False)
    quantity_deployed = Column(Integer, nullable=False, default=1)
    notes = Column(Text, nullable=True)
    deployed_at = Column(DateTime, server_default=func.now(), nullable=False)
    recalled_at = Column(DateTime, nullable=True)

    # Relationships
    incident = relationship("Incident", back_populates="resource_deployments")
    resource = relationship("Resource", back_populates="resource_deployments")
