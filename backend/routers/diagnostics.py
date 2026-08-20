from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from backend.database import get_db
from backend.models import Diagnostic, HealthCenter
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class DiagnosticCreate(BaseModel):
    health_center_id: int
    patient_name: str
    patient_age: int | None = None
    patient_gender: str | None = None
    diagnosis_type: str
    symptoms: str | None = None
    priority: str = "normal"


class DiagnosticUpdate(BaseModel):
    patient_name: str | None = None
    patient_age: int | None = None
    patient_gender: str | None = None
    diagnosis_type: str | None = None
    symptoms: str | None = None
    diagnosis_result: str | None = None
    status: str | None = None
    priority: str | None = None
    assigned_specialist: str | None = None


class DiagnosticResponse(BaseModel):
    id: int
    health_center_id: int
    patient_name: str
    patient_age: int | None
    patient_gender: str | None
    diagnosis_type: str
    symptoms: str | None
    diagnosis_result: str | None
    status: str
    priority: str
    assigned_specialist: str | None
    
    class Config:
        from_attributes = True


@router.post("/", response_model=DiagnosticResponse, status_code=status.HTTP_201_CREATED)
async def create_diagnostic(
    diagnostic: DiagnosticCreate,
    db: Session = Depends(get_db)
):
    try:
        health_center = db.query(HealthCenter).filter(HealthCenter.id == diagnostic.health_center_id).first()
        if not health_center:
            raise HTTPException(status_code=404, detail="Health center not found")
        
        db_diagnostic = Diagnostic(**diagnostic.model_dump())
        db.add(db_diagnostic)
        db.commit()
        db.refresh(db_diagnostic)
        logger.info(f"Created diagnostic record: {db_diagnostic.id}")
        return db_diagnostic
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating diagnostic: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create diagnostic record")


@router.get("/", response_model=List[DiagnosticResponse])
async def get_diagnostics(
    skip: int = 0,
    limit: int = 100,
    health_center_id: int | None = None,
    status_filter: str | None = None,
    priority: str | None = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Diagnostic)
        if health_center_id:
            query = query.filter(Diagnostic.health_center_id == health_center_id)
        if status_filter:
            query = query.filter(Diagnostic.status == status_filter)
        if priority:
            query = query.filter(Diagnostic.priority == priority)
        
        diagnostics = query.offset(skip).limit(limit).all()
        return diagnostics
    except Exception as e:
        logger.error(f"Error fetching diagnostics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch diagnostic records")


@router.get("/{diagnostic_id}", response_model=DiagnosticResponse)
async def get_diagnostic(
    diagnostic_id: int,
    db: Session = Depends(get_db)
):
    diagnostic = db.query(Diagnostic).filter(Diagnostic.id == diagnostic_id).first()
    if not diagnostic:
        raise HTTPException(status_code=404, detail="Diagnostic record not found")
    return diagnostic


@router.put("/{diagnostic_id}", response_model=DiagnosticResponse)
async def update_diagnostic(
    diagnostic_id: int,
    diagnostic_update: DiagnosticUpdate,
    db: Session = Depends(get_db)
):
    try:
        db_diagnostic = db.query(Diagnostic).filter(Diagnostic.id == diagnostic_id).first()
        if not db_diagnostic:
            raise HTTPException(status_code=404, detail="Diagnostic record not found")
        
        update_data = diagnostic_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_diagnostic, key, value)
        
        db.commit()
        db.refresh(db_diagnostic)
        logger.info(f"Updated diagnostic record: {db_diagnostic.id}")
        return db_diagnostic
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating diagnostic: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update diagnostic record")


@router.delete("/{diagnostic_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diagnostic(
    diagnostic_id: int,
    db: Session = Depends(get_db)
):
    try:
        db_diagnostic = db.query(Diagnostic).filter(Diagnostic.id == diagnostic_id).first()
        if not db_diagnostic:
            raise HTTPException(status_code=404, detail="Diagnostic record not found")
        
        db.delete(db_diagnostic)
        db.commit()
        logger.info(f"Deleted diagnostic record: {diagnostic_id}")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting diagnostic: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete diagnostic record")
