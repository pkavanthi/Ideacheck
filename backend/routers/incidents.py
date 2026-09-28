from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.models import Incident, IncidentStatus, SeverityLevel, get_db

router = APIRouter(prefix="/incidents", tags=["incidents"])


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class IncidentCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    hazard_type: str = Field(..., min_length=2, max_length=100)
    severity: SeverityLevel = SeverityLevel.MEDIUM
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    district: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    reported_by: str = Field(..., min_length=2, max_length=255)


class IncidentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    hazard_type: Optional[str] = Field(None, min_length=2, max_length=100)
    severity: Optional[SeverityLevel] = None
    status: Optional[IncidentStatus] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    district: Optional[str] = Field(None, min_length=2, max_length=100)
    state: Optional[str] = Field(None, min_length=2, max_length=100)


class IncidentResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    hazard_type: str
    severity: SeverityLevel
    status: IncidentStatus
    latitude: Optional[float]
    longitude: Optional[float]
    district: str
    state: str
    reported_by: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_model(cls, obj: Incident) -> "IncidentResponse":
        return cls(
            id=obj.id,
            title=obj.title,
            description=obj.description,
            hazard_type=obj.hazard_type,
            severity=obj.severity,
            status=obj.status,
            latitude=obj.latitude,
            longitude=obj.longitude,
            district=obj.district,
            state=obj.state,
            reported_by=obj.reported_by,
            created_at=obj.created_at.isoformat(),
            updated_at=obj.updated_at.isoformat(),
        )


# ---------------------------------------------------------------------------
# CRUD routes
# ---------------------------------------------------------------------------

@router.post("/", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    """Report a new disaster incident."""
    incident = Incident(**payload.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return IncidentResponse.from_orm_model(incident)


@router.get("/", response_model=List[IncidentResponse])
def list_incidents(
    state: Optional[str] = Query(None, description="Filter by state"),
    district: Optional[str] = Query(None, description="Filter by district"),
    severity: Optional[SeverityLevel] = Query(None, description="Filter by severity"),
    incident_status: Optional[IncidentStatus] = Query(None, alias="status", description="Filter by status"),
    hazard_type: Optional[str] = Query(None, description="Filter by hazard type"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """List all incidents with optional filters."""
    query = db.query(Incident)
    if state:
        query = query.filter(Incident.state.ilike(f"%{state}%"))
    if district:
        query = query.filter(Incident.district.ilike(f"%{district}%"))
    if severity:
        query = query.filter(Incident.severity == severity)
    if incident_status:
        query = query.filter(Incident.status == incident_status)
    if hazard_type:
        query = query.filter(Incident.hazard_type.ilike(f"%{hazard_type}%"))
    incidents = query.order_by(Incident.created_at.desc()).offset(skip).limit(limit).all()
    return [IncidentResponse.from_orm_model(i) for i in incidents]


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    """Retrieve a single incident by ID."""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return IncidentResponse.from_orm_model(incident)


@router.patch("/{incident_id}", response_model=IncidentResponse)
def update_incident(incident_id: int, payload: IncidentUpdate, db: Session = Depends(get_db)):
    """Update fields of an existing incident."""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(incident, field, value)
    db.commit()
    db.refresh(incident)
    return IncidentResponse.from_orm_model(incident)


@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    """Delete an incident and all its resource deployments."""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    db.delete(incident)
    db.commit()
