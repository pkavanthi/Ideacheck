import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models import ClimateRiskEvent, HazardType, SeverityLevel, get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/risks", tags=["Climate Risk Events"])


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class RiskEventCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    hazard_type: HazardType
    severity: SeverityLevel
    location: str = Field(..., min_length=2, max_length=255)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    description: Optional[str] = None
    affected_population: Optional[int] = Field(None, ge=0)
    reported_by: Optional[str] = None


class RiskEventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    hazard_type: Optional[HazardType] = None
    severity: Optional[SeverityLevel] = None
    location: Optional[str] = Field(None, min_length=2, max_length=255)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    description: Optional[str] = None
    affected_population: Optional[int] = Field(None, ge=0)
    reported_by: Optional[str] = None


class RiskEventResponse(BaseModel):
    id: int
    title: str
    hazard_type: HazardType
    severity: SeverityLevel
    location: str
    latitude: Optional[float]
    longitude: Optional[float]
    description: Optional[str]
    affected_population: Optional[int]
    reported_by: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@router.post("/", response_model=RiskEventResponse, status_code=status.HTTP_201_CREATED)
def create_risk_event(payload: RiskEventCreate, db: Session = Depends(get_db)):
    """Record a new climate-risk event."""
    event = ClimateRiskEvent(**payload.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    logger.info("Created risk event id=%s type=%s", event.id, event.hazard_type)
    return _to_response(event)


@router.get("/", response_model=List[RiskEventResponse])
def list_risk_events(
    hazard_type: Optional[HazardType] = Query(None),
    severity: Optional[SeverityLevel] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """List climate-risk events with optional filtering."""
    query = db.query(ClimateRiskEvent)
    if hazard_type:
        query = query.filter(ClimateRiskEvent.hazard_type == hazard_type)
    if severity:
        query = query.filter(ClimateRiskEvent.severity == severity)
    return [_to_response(e) for e in query.offset(skip).limit(limit).all()]


@router.get("/{event_id}", response_model=RiskEventResponse)
def get_risk_event(event_id: int, db: Session = Depends(get_db)):
    """Fetch a single risk event by ID."""
    event = _get_or_404(db, event_id)
    return _to_response(event)


@router.put("/{event_id}", response_model=RiskEventResponse)
def update_risk_event(event_id: int, payload: RiskEventUpdate, db: Session = Depends(get_db)):
    """Update an existing risk event."""
    event = _get_or_404(db, event_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(event, field, value)
    db.commit()
    db.refresh(event)
    logger.info("Updated risk event id=%s", event.id)
    return _to_response(event)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_risk_event(event_id: int, db: Session = Depends(get_db)):
    """Delete a risk event."""
    event = _get_or_404(db, event_id)
    db.delete(event)
    db.commit()
    logger.info("Deleted risk event id=%s", event_id)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _get_or_404(db: Session, event_id: int) -> ClimateRiskEvent:
    event = db.query(ClimateRiskEvent).filter(ClimateRiskEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Risk event not found")
    return event


def _to_response(event: ClimateRiskEvent) -> dict:
    return {
        **{c.name: getattr(event, c.name) for c in event.__table__.columns if c.name not in ("created_at", "updated_at")},
        "created_at": event.created_at.isoformat(),
        "updated_at": event.updated_at.isoformat(),
    }
