from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

from backend.models import BondStatus, FarmerStatus


# ---------------------------------------------------------------------------
# Farmer schemas
# ---------------------------------------------------------------------------

class FarmerBase(BaseModel):
    name: str
    phone: str
    village: str
    district: str
    state: str
    land_area_acres: float
    crop_type: str
    fpo_id: Optional[int] = None


class FarmerCreate(FarmerBase):
    pass


class FarmerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    village: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    land_area_acres: Optional[float] = None
    crop_type: Optional[str] = None
    fpo_id: Optional[int] = None
    status: Optional[FarmerStatus] = None


class FarmerOut(FarmerBase):
    id: int
    status: FarmerStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# FPO schemas
# ---------------------------------------------------------------------------

class FPOBase(BaseModel):
    name: str
    registration_number: str
    treasurer_name: str
    treasurer_phone: str
    district: str
    state: str


class FPOCreate(FPOBase):
    pass


class FPOUpdate(BaseModel):
    name: Optional[str] = None
    treasurer_name: Optional[str] = None
    treasurer_phone: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None


class FPOOut(FPOBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Bond schemas
# ---------------------------------------------------------------------------

class BondBase(BaseModel):
    farmer_id: int
    crop_type: str
    harvest_quantity_kg: float
    harvest_fraction: float
    face_value: float
    interest_rate_pct: float
    maturity_date: datetime

    @field_validator("harvest_fraction")
    @classmethod
    def fraction_range(cls, v: float) -> float:
        if not 0.0 < v <= 1.0:
            raise ValueError("harvest_fraction must be between 0 (exclusive) and 1 (inclusive)")
        return v

    @field_validator("face_value", "harvest_quantity_kg")
    @classmethod
    def positive_value(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Value must be positive")
        return v


class BondCreate(BondBase):
    pass


class BondUpdate(BaseModel):
    verifier_name: Optional[str] = None
    verification_notes: Optional[str] = None
    issued_capital: Optional[float] = None
    buyer_id: Optional[int] = None
    status: Optional[BondStatus] = None


class BondOut(BondBase):
    id: int
    issued_capital: Optional[float] = None
    verifier_name: Optional[str] = None
    verification_notes: Optional[str] = None
    buyer_id: Optional[int] = None
    status: BondStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Buyer schemas
# ---------------------------------------------------------------------------

class BuyerBase(BaseModel):
    name: str
    organisation: str
    phone: str
    email: EmailStr


class BuyerCreate(BuyerBase):
    pass


class BuyerUpdate(BaseModel):
    name: Optional[str] = None
    organisation: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class BuyerOut(BuyerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
