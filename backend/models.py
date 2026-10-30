"""Database models and Pydantic schemas for key entities: Incident and Resource."""
import enum
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import DateTime, Enum, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Severity(str, enum.Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"


class IncidentStatus(str, enum.Enum):
    reported = "reported"
    active = "active"
    contained = "contained"
    resolved = "resolved"


class ResourceStatus(str, enum.Enum):
    available = "available"
    deployed = "deployed"
    maintenance = "maintenance"


# ---------------------------- ORM models ----------------------------
class Incident(Base):
    __tablename__ = "incidents"
    __table_args__ = (Index("ix_incidents_status_severity", "status", "severity"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    disaster_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    severity: Mapped[Severity] = mapped_column(Enum(Severity), default=Severity.low, nullable=False)
    status: Mapped[IncidentStatus] = mapped_column(
        Enum(IncidentStatus), default=IncidentStatus.reported, nullable=False
    )
    region: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    affected_population: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)

    resources: Mapped[list["Resource"]] = relationship(back_populates="incident")


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[ResourceStatus] = mapped_column(
        Enum(ResourceStatus), default=ResourceStatus.available, nullable=False
    )
    location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    incident_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("incidents.id", ondelete="SET NULL"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)

    incident: Mapped[Optional[Incident]] = relationship(back_populates="resources")


# --------------------------- Pydantic schemas ---------------------------
class IncidentBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=5000)
    disaster_type: str = Field(min_length=1, max_length=50)
    severity: Severity = Severity.low
    status: IncidentStatus = IncidentStatus.reported
    region: str = Field(min_length=1, max_length=100)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    affected_population: int = Field(default=0, ge=0)


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=5000)
    disaster_type: Optional[str] = Field(default=None, min_length=1, max_length=50)
    severity: Optional[Severity] = None
    status: Optional[IncidentStatus] = None
    region: Optional[str] = Field(default=None, min_length=1, max_length=100)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    affected_population: Optional[int] = Field(default=None, ge=0)


class IncidentOut(IncidentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class ResourceBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    resource_type: str = Field(min_length=1, max_length=50)
    quantity: int = Field(default=1, ge=0)
    status: ResourceStatus = ResourceStatus.available
    location: Optional[str] = Field(default=None, max_length=200)
    incident_id: Optional[int] = None


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    resource_type: Optional[str] = Field(default=None, min_length=1, max_length=50)
    quantity: Optional[int] = Field(default=None, ge=0)
    status: Optional[ResourceStatus] = None
    location: Optional[str] = Field(default=None, max_length=200)
    incident_id: Optional[int] = None


class ResourceOut(ResourceBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
