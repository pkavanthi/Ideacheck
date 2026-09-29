from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database import get_db
from backend.models import Incident
from backend.schemas import IncidentCreate, IncidentUpdate, IncidentResponse

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.get("/", response_model=List[IncidentResponse])
def get_incidents(
    district: Optional[str] = None,
    threat_level: Optional[str] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Incident)
    if district:
        query = query.filter(Incident.district.ilike(f"%{district}%"))
    if threat_level:
        query = query.filter(Incident.threat_level == threat_level)
    if status_filter:
        query = query.filter(Incident.status == status_filter)
    return query.order_by(Incident.created_at.desc()).all()

@router.post("/", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    incident = Incident(**payload.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident

@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident #{incident_id} not found")
    return incident

@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident(incident_id: int, payload: IncidentUpdate, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident #{incident_id} not found")
    
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(incident, field, value)
    
    db.commit()
    db.refresh(incident)
    return incident

@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident #{incident_id} not found")
    db.delete(incident)
    db.commit()
    return None
