from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from backend.database import get_db
from backend.models import HealthCenter
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class HealthCenterCreate(BaseModel):
    name: str
    location: str
    latitude: float | None = None
    longitude: float | None = None
    contact_number: str | None = None
    email: str | None = None
    capacity: int = 0


class HealthCenterUpdate(BaseModel):
    name: str | None = None
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    contact_number: str | None = None
    email: str | None = None
    capacity: int | None = None
    is_active: bool | None = None


class HealthCenterResponse(BaseModel):
    id: int
    name: str
    location: str
    latitude: float | None
    longitude: float | None
    contact_number: str | None
    email: str | None
    capacity: int
    is_active: bool
    
    class Config:
        from_attributes = True


@router.post("/", response_model=HealthCenterResponse, status_code=status.HTTP_201_CREATED)
async def create_health_center(
    health_center: HealthCenterCreate,
    db: Session = Depends(get_db)
):
    try:
        db_health_center = HealthCenter(**health_center.model_dump())
        db.add(db_health_center)
        db.commit()
        db.refresh(db_health_center)
        logger.info(f"Created health center: {db_health_center.name}")
        return db_health_center
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating health center: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create health center")


@router.get("/", response_model=List[HealthCenterResponse])
async def get_health_centers(
    skip: int = 0,
    limit: int = 100,
    is_active: bool | None = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(HealthCenter)
        if is_active is not None:
            query = query.filter(HealthCenter.is_active == is_active)
        health_centers = query.offset(skip).limit(limit).all()
        return health_centers
    except Exception as e:
        logger.error(f"Error fetching health centers: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch health centers")


@router.get("/{health_center_id}", response_model=HealthCenterResponse)
async def get_health_center(
    health_center_id: int,
    db: Session = Depends(get_db)
):
    health_center = db.query(HealthCenter).filter(HealthCenter.id == health_center_id).first()
    if not health_center:
        raise HTTPException(status_code=404, detail="Health center not found")
    return health_center


@router.put("/{health_center_id}", response_model=HealthCenterResponse)
async def update_health_center(
    health_center_id: int,
    health_center_update: HealthCenterUpdate,
    db: Session = Depends(get_db)
):
    try:
        db_health_center = db.query(HealthCenter).filter(HealthCenter.id == health_center_id).first()
        if not db_health_center:
            raise HTTPException(status_code=404, detail="Health center not found")
        
        update_data = health_center_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_health_center, key, value)
        
        db.commit()
        db.refresh(db_health_center)
        logger.info(f"Updated health center: {db_health_center.id}")
        return db_health_center
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating health center: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update health center")


@router.delete("/{health_center_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_health_center(
    health_center_id: int,
    db: Session = Depends(get_db)
):
    try:
        db_health_center = db.query(HealthCenter).filter(HealthCenter.id == health_center_id).first()
        if not db_health_center:
            raise HTTPException(status_code=404, detail="Health center not found")
        
        db.delete(db_health_center)
        db.commit()
        logger.info(f"Deleted health center: {health_center_id}")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting health center: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete health center")
