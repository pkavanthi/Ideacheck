import logging
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import District

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/districts", tags=["districts"])


# ── Schemas ──────────────────────────────────────────────────────────────────


class DistrictCreate(BaseModel):
    name: str
    state: str
    district_code: str
    population: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    collector_name: Optional[str] = None
    collector_contact: Optional[str] = None


class DistrictUpdate(BaseModel):
    name: Optional[str] = None
    state: Optional[str] = None
    population: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    collector_name: Optional[str] = None
    collector_contact: Optional[str] = None
    is_active: Optional[bool] = None


class DistrictResponse(BaseModel):
    id: int
    name: str
    state: str
    district_code: str
    population: Optional[int]
    latitude: Optional[float]
    longitude: Optional[float]
    collector_name: Optional[str]
    collector_contact: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ── Endpoints ─────────────────────────────────────────────────────────────────


@router.post("/", response_model=DistrictResponse, status_code=status.HTTP_201_CREATED)
def create_district(payload: DistrictCreate, db: Session = Depends(get_db)):
    existing = db.query(District).filter(District.district_code == payload.district_code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"District with code '{payload.district_code}' already exists",
        )
    district = District(**payload.model_dump())
    db.add(district)
    db.commit()
    db.refresh(district)
    logger.info("District created: id=%s code=%s", district.id, district.district_code)
    return district


@router.get("/", response_model=List[DistrictResponse])
def list_districts(
    state: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(District)
    if state is not None:
        q = q.filter(District.state.ilike(f"%{state}%"))
    if is_active is not None:
        q = q.filter(District.is_active == is_active)
    return q.order_by(District.name).offset(skip).limit(limit).all()


@router.get("/{district_id}", response_model=DistrictResponse)
def get_district(district_id: int, db: Session = Depends(get_db)):
    district = db.query(District).filter(District.id == district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail="District not found")
    return district


@router.patch("/{district_id}", response_model=DistrictResponse)
def update_district(district_id: int, payload: DistrictUpdate, db: Session = Depends(get_db)):
    district = db.query(District).filter(District.id == district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail="District not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(district, field, value)
    district.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(district)
    logger.info("District updated: id=%s", district_id)
    return district


@router.delete("/{district_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_district(district_id: int, db: Session = Depends(get_db)):
    district = db.query(District).filter(District.id == district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail="District not found")
    db.delete(district)
    db.commit()
    logger.info("District deleted: id=%s", district_id)
