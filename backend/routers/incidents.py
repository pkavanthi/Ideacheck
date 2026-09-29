from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Incident, IncidentSeverity, IncidentStatus

router = APIRouter(prefix="/incidents", tags=["incidents"])


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class IncidentCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    location: str = Field(..., min_length=2, max_length=500)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    severity: IncidentSeverity = IncidentSeverity.MEDIUM
    reported_by: Optional[str] = Field(None, max_length=255)
    affected_count: Optional[int] = Field(None, ge=0)


class IncidentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    location: Optional[str] = Field(None, min_length=2, max_length=500)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    severity: Optional[IncidentSeverity] = None
    status: Optional[IncidentStatus] = None
    reported_by: Optional[str] = Field(None, max_length=255)
    affected_count: Optional[int] = Field(None, ge=0)


class IncidentResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    location: str
    latitude: Optional[float]
    longitude: Optional[float]
    severity: IncidentSeverity
    status: IncidentStatus
    reported_by: Optional[str]
    affected_count: Optional[int]
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_model(cls, incident: Incident) -> "IncidentResponse":
        return cls(
            id=incident.id,
            title=incident.title,
            description=incident.description,
            location=incident.location,
            latitude=incident.latitude,
            longitude=incident.longitude,
            severity=incident.severity,
            status=incident.status,
            reported_by=incident.reported_by,
            affected_count=incident.affected_count,
            created_at=incident.created_at.isoformat(),
            updated_at=incident.updated_at.isoformat(),
        )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/", response_model=List[IncidentResponse], summary="List all incidents")
def list_incidents(
    severity: Optional[IncidentSeverity] = Query(None, description="Filter by severity"),
    status: Optional[IncidentStatus] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    query = db.query(Incident)
    if severity:
        query = query.filter(Incident.severity == severity)
    if status:
        query = query.filter(Incident.status == status)
    incidents = query.order_by(Incident.created_at.desc()).offset(skip).limit(limit).all()
    return [IncidentResponse.from_orm_model(i) for i in incidents]


@router.post("/", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED, summary="Report a new incident")
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    incident = Incident(**payload.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return IncidentResponse.from_orm_model(incident)


@router.get("/{incident_id}", response_model=IncidentResponse, summary="Get incident details")
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return IncidentResponse.from_orm_model(incident)


@router.put("/{incident_id}", response_model=IncidentResponse, summary="Update an incident")
def update_incident(incident_id: int, payload: IncidentUpdate, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(incident, field, value)
    db.commit()
    db.refresh(incident)
    return IncidentResponse.from_orm_model(incident)


@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an incident")
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    db.delete(incident)
    db.commit()
