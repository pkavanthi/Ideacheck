from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import HealthWorker
from backend.schemas import HealthWorker as HealthWorkerSchema, HealthWorkerCreate, HealthWorkerUpdate

router = APIRouter()


@router.post("/", response_model=HealthWorkerSchema, status_code=status.HTTP_201_CREATED)
def create_health_worker(health_worker: HealthWorkerCreate, db: Session = Depends(get_db)):
    """Create a new health worker"""
    db_worker = db.query(HealthWorker).filter(HealthWorker.email == health_worker.email).first()
    if db_worker:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_worker = HealthWorker(**health_worker.model_dump())
    db.add(new_worker)
    db.commit()
    db.refresh(new_worker)
    return new_worker


@router.get("/", response_model=List[HealthWorkerSchema])
def get_health_workers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all health workers with pagination"""
    workers = db.query(HealthWorker).offset(skip).limit(limit).all()
    return workers


@router.get("/{worker_id}", response_model=HealthWorkerSchema)
def get_health_worker(worker_id: int, db: Session = Depends(get_db)):
    """Get a specific health worker by ID"""
    worker = db.query(HealthWorker).filter(HealthWorker.id == worker_id).first()
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health worker not found"
        )
    return worker


@router.put("/{worker_id}", response_model=HealthWorkerSchema)
def update_health_worker(worker_id: int, worker_update: HealthWorkerUpdate, db: Session = Depends(get_db)):
    """Update a health worker's information"""
    worker = db.query(HealthWorker).filter(HealthWorker.id == worker_id).first()
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health worker not found"
        )
    
    update_data = worker_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(worker, field, value)
    
    db.commit()
    db.refresh(worker)
    return worker


@router.delete("/{worker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_health_worker(worker_id: int, db: Session = Depends(get_db)):
    """Delete a health worker"""
    worker = db.query(HealthWorker).filter(HealthWorker.id == worker_id).first()
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health worker not found"
        )
    
    db.delete(worker)
    db.commit()
    return None
