"""
Villages router — CRUD operations for village entities.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Village

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/villages", tags=["Villages"])


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class VillageCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    district: str = Field(..., min_length=1, max_length=200)
    state: str = Field(..., min_length=1, max_length=100)
    block: Optional[str] = Field(None, max_length=200)
    gram_panchayat: Optional[str] = Field(None, max_length=200)
    population: Optional[int] = Field(None, ge=0)
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    phc_name: Optional[str] = Field(None, max_length=200)


class VillageUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    district: Optional[str] = Field(None, min_length=1, max_length=200)
    state: Optional[str] = Field(None, min_length=1, max_length=100)
    block: Optional[str] = Field(None, max_length=200)
    gram_panchayat: Optional[str] = Field(None, max_length=200)
    population: Optional[int] = Field(None, ge=0)
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    phc_name: Optional[str] = Field(None, max_length=200)


class VillageResponse(BaseModel):
    id: int
    name: str
    district: str
    state: str
    block: Optional[str]
    gram_panchayat: Optional[str]
    population: Optional[int]
    latitude: Optional[float]
    longitude: Optional[float]
    phc_name: Optional[str]

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/", response_model=list[VillageResponse], summary="List villages")
def list_villages(
    search: Optional[str] = Query(None, description="Search by name, district, or state"),
    state: Optional[str] = Query(None, description="Filter by state"),
    district: Optional[str] = Query(None, description="Filter by district"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    stmt = select(Village)
    if search:
        term = f"%{search}%"
        stmt = stmt.where(
            or_(
                Village.name.ilike(term),
                Village.district.ilike(term),
                Village.state.ilike(term),
            )
        )
    if state:
        stmt = stmt.where(Village.state.ilike(f"%{state}%"))
    if district:
        stmt = stmt.where(Village.district.ilike(f"%{district}%"))
    stmt = stmt.order_by(Village.name).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


@router.post("/", response_model=VillageResponse, status_code=status.HTTP_201_CREATED, summary="Create village")
def create_village(payload: VillageCreate, db: Session = Depends(get_db)):
    village = Village(**payload.model_dump())
    db.add(village)
    db.commit()
    db.refresh(village)
    logger.info("Created Village id=%s name=%r", village.id, village.name)
    return village


@router.get("/{village_id}", response_model=VillageResponse, summary="Get village")
def get_village(village_id: int, db: Session = Depends(get_db)):
    village = db.get(Village, village_id)
    if not village:
        raise HTTPException(status_code=404, detail=f"Village {village_id} not found")
    return village


@router.patch("/{village_id}", response_model=VillageResponse, summary="Update village")
def update_village(village_id: int, payload: VillageUpdate, db: Session = Depends(get_db)):
    village = db.get(Village, village_id)
    if not village:
        raise HTTPException(status_code=404, detail=f"Village {village_id} not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(village, field, value)

    db.commit()
    db.refresh(village)
    logger.info("Updated Village id=%s", village_id)
    return village


@router.delete("/{village_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete village")
def delete_village(village_id: int, db: Session = Depends(get_db)):
    village = db.get(Village, village_id)
    if not village:
        raise HTTPException(status_code=404, detail=f"Village {village_id} not found")
    db.delete(village)
    db.commit()
    logger.info("Deleted Village id=%s", village_id)
