import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Incident, IncidentSeverity, IncidentStatus

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/incidents", tags=["Incidents"])


# ── Schemas ─────────────────────────────────────────────────────────────────

class IncidentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    location: str = Field(..., min_length=1, max_length=255)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    severity: IncidentSeverity = IncidentSeverity.MEDIUM
    affected_population: int = Field(default=0, ge=0)
    reported_by: Optional[str] = Field(None, max_length=100)


class IncidentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    location: Optional[str] = Field(None, min_length=1, max_length=255)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    severity: Optional[IncidentSeverity] = None
    status: Optional[IncidentStatus] = None
    affected_population: Optional[int] = Field(None, ge=0)
    reported_by: Optional[str] = Field(None, max_length=100)


class IncidentResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    location: str
    latitude: Optional[float]
    longitude: Optional[float]
    severity: IncidentSeverity
    status: IncidentStatus
    affected_population: int
    reported_by: Optional[str]
    created_at: str
    updated_at: Optional[str]

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_safe(cls, obj: Incident) -> "IncidentResponse":
        return cls(
            id=obj.id,
            title=obj.title,
            description=obj.description,
            location=obj.location,
            latitude=obj.latitude,
            longitude=obj.longitude,
            severity=obj.severity,
            status=obj.status,
            affected_population=obj.affected_population,
            reported_by=obj.reported_by,
            created_at=obj.created_at.isoformat(),
            updated_at=obj.updated_at.isoformat() if obj.updated_at else None,
        )


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    incident = Incident(**payload.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    logger.info("Created incident id=%s title=%r", incident.id, incident.title)
    return IncidentResponse.from_orm_safe(incident)


@router.get("/", response_model=List[IncidentResponse])
def list_incidents(
    status: Optional[IncidentStatus] = Query(None),
    severity: Optional[IncidentSeverity] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(Incident)
    if status:
        query = query.filter(Incident.status == status)
    if severity:
        query = query.filter(Incident.severity == severity)
    incidents = query.order_by(Incident.created_at.desc()).offset(skip).limit(limit).all()
    return [IncidentResponse.from_orm_safe(i) for i in incidents]


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return IncidentResponse.from_orm_safe(incident)


@router.patch("/{incident_id}", response_model=IncidentResponse)
def update_incident(incident_id: int, payload: IncidentUpdate, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(incident, field, value)
    db.commit()
    db.refresh(incident)
    logger.info("Updated incident id=%s", incident_id)
    return IncidentResponse.from_orm_safe(incident)


@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    db.delete(incident)
    db.commit()
    logger.info("Deleted incident id=%s", incident_id)
