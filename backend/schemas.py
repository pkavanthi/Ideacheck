"""Pydantic request/response schemas with input validation."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models import AssetStatus, AssetType, HazardType, IncidentStatus, Severity


class IncidentBase(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: Optional[str] = Field(default=None, max_length=5000)
    hazard_type: HazardType
    severity: Severity
    status: IncidentStatus = IncidentStatus.reported
    district: str = Field(min_length=1, max_length=120)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=200)
    description: Optional[str] = Field(default=None, max_length=5000)
    hazard_type: Optional[HazardType] = None
    severity: Optional[Severity] = None
    status: Optional[IncidentStatus] = None
    district: Optional[str] = Field(default=None, min_length=1, max_length=120)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)


class IncidentOut(IncidentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class AssetBase(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    asset_type: AssetType
    status: AssetStatus = AssetStatus.available
    district: str = Field(min_length=1, max_length=120)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    incident_id: Optional[int] = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    asset_type: Optional[AssetType] = None
    status: Optional[AssetStatus] = None
    district: Optional[str] = Field(default=None, min_length=1, max_length=120)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    incident_id: Optional[int] = None


class AssetOut(AssetBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
