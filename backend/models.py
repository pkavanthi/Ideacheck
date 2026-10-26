"""Database setup and ORM models for the key entities: Incident and Asset."""
import enum
from datetime import datetime, timezone
from typing import Iterator, Optional

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Index, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker

from config import get_settings

settings = get_settings()

_connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=_connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class HazardType(str, enum.Enum):
    flood = "flood"
    landslide = "landslide"


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


class AssetType(str, enum.Enum):
    rescue_team = "rescue_team"
    drone = "drone"
    floodgate = "floodgate"
    pump = "pump"
    grid_node = "grid_node"


class AssetStatus(str, enum.Enum):
    available = "available"
    deployed = "deployed"
    maintenance = "maintenance"
    offline = "offline"


class Incident(Base):
    __tablename__ = "incidents"
    __table_args__ = (Index("ix_incidents_district_status", "district", "status"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    hazard_type: Mapped[HazardType] = mapped_column(Enum(HazardType), index=True)
    severity: Mapped[Severity] = mapped_column(Enum(Severity), index=True)
    status: Mapped[IncidentStatus] = mapped_column(Enum(IncidentStatus), default=IncidentStatus.reported)
    district: Mapped[str] = mapped_column(String(120), index=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow)

    assets: Mapped[list["Asset"]] = relationship(back_populates="incident")


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)
    asset_type: Mapped[AssetType] = mapped_column(Enum(AssetType), index=True)
    status: Mapped[AssetStatus] = mapped_column(Enum(AssetStatus), default=AssetStatus.available, index=True)
    district: Mapped[str] = mapped_column(String(120), index=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    incident_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("incidents.id", ondelete="SET NULL"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow)

    incident: Mapped[Optional[Incident]] = relationship(back_populates="assets")
