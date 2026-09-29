from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class IncidentBase(BaseModel):
    title: str = Field(..., example="Flash flood warning in Aluva")
    district: str = Field(..., example="Ernakulam")
    location_name: str = Field(..., example="Aluva River Basin")
    latitude: float = Field(..., example=10.1076)
    longitude: float = Field(..., example=76.3516)
    threat_level: str = Field(default="HIGH", example="HIGH")
    status: str = Field(default="ACTIVE", example="ACTIVE")
    description: Optional[str] = Field(None, example="Water level crossed warning mark")
    affected_population: int = Field(default=0, example=1500)

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    district: Optional[str] = None
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    threat_level: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    affected_population: Optional[int] = None

class IncidentResponse(IncidentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ResourceBase(BaseModel):
    name: str = Field(..., example="Inflatable Rescue Boats")
    resource_type: str = Field(default="RESCUE_BOAT", example="RESCUE_BOAT")
    district: str = Field(..., example="Ernakulam")
    quantity: int = Field(..., example=25)
    available_quantity: int = Field(..., example=20)
    location_hub: str = Field(..., example="Kochi Central Relief Depot")
    status: str = Field(default="AVAILABLE", example="AVAILABLE")

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    resource_type: Optional[str] = None
    district: Optional[str] = None
    quantity: Optional[int] = None
    available_quantity: Optional[int] = None
    location_hub: Optional[str] = None
    status: Optional[str] = None

class ResourceResponse(ResourceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
