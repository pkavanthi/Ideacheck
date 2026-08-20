from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import Consultation, Patient, HealthWorker
from backend.schemas import Consultation as ConsultationSchema, ConsultationCreate, ConsultationUpdate

router = APIRouter()


@router.post("/", response_model=ConsultationSchema, status_code=status.HTTP_201_CREATED)
def create_consultation(consultation: ConsultationCreate, db: Session = Depends(get_db)):
    """Create a new consultation"""
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == consultation.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Verify health worker exists
    worker = db.query(HealthWorker).filter(HealthWorker.id == consultation.health_worker_id).first()
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health worker not found"
        )
    
    new_consultation = Consultation(**consultation.model_dump())
    db.add(new_consultation)
    db.commit()
    db.refresh(new_consultation)
    return new_consultation


@router.get("/", response_model=List[ConsultationSchema])
def get_consultations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all consultations with pagination"""
    consultations = db.query(Consultation).offset(skip).limit(limit).all()
    return consultations


@router.get("/{consultation_id}", response_model=ConsultationSchema)
def get_consultation(consultation_id: int, db: Session = Depends(get_db)):
    """Get a specific consultation by ID"""
    consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    return consultation


@router.put("/{consultation_id}", response_model=ConsultationSchema)
def update_consultation(consultation_id: int, consultation_update: ConsultationUpdate, db: Session = Depends(get_db)):
    """Update a consultation"""
    consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    update_data = consultation_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(consultation, field, value)
    
    db.commit()
    db.refresh(consultation)
    return consultation


@router.delete("/{consultation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_consultation(consultation_id: int, db: Session = Depends(get_db)):
    """Delete a consultation"""
    consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    db.delete(consultation)
    db.commit()
    return None


@router.get("/patient/{patient_id}", response_model=List[ConsultationSchema])
def get_patient_consultations(patient_id: int, db: Session = Depends(get_db)):
    """Get all consultations for a specific patient"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    consultations = db.query(Consultation).filter(Consultation.patient_id == patient_id).all()
    return consultations


@router.get("/health-worker/{worker_id}", response_model=List[ConsultationSchema])
def get_worker_consultations(worker_id: int, db: Session = Depends(get_db)):
    """Get all consultations for a specific health worker"""
    worker = db.query(HealthWorker).filter(HealthWorker.id == worker_id).first()
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health worker not found"
        )
    
    consultations = db.query(Consultation).filter(Consultation.health_worker_id == worker_id).all()
    return consultations
