"""CRUD routes for disaster incidents."""
import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import (
    Incident,
    IncidentCreate,
    IncidentOut,
    IncidentStatus,
    IncidentUpdate,
    Severity,
)
from security import require_api_key

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/incidents", tags=["incidents"], dependencies=[Depends(require_api_key)])


def _get_or_404(db: Session, incident_id: int) -> Incident:
    incident = db.get(Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return incident


@router.post("", response_model=IncidentOut, status_code=status.HTTP_201_CREATED)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    incident = Incident(**payload.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    logger.info("Created incident %s", incident.id)
    return incident


@router.get("", response_model=List[IncidentOut])
def list_incidents(
    region: Optional[str] = None,
    severity: Optional[Severity] = None,
    status_filter: Optional[IncidentStatus] = Query(default=None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    stmt = select(Incident)
    if region:
        stmt = stmt.where(Incident.region == region)
    if severity:
        stmt = stmt.where(Incident.severity == severity)
    if status_filter:
        stmt = stmt.where(Incident.status == status_filter)
    stmt = stmt.order_by(Incident.created_at.desc()).offset(skip).limit(limit)
    return db.scalars(stmt).all()


@router.get("/{incident_id}", response_model=IncidentOut)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, incident_id)


@router.patch("/{incident_id}", response_model=IncidentOut)
def update_incident(incident_id: int, payload: IncidentUpdate, db: Session = Depends(get_db)):
    incident = _get_or_404(db, incident_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        if value is None and key in {"title", "disaster_type", "region", "severity", "status", "affected_population"}:
            raise HTTPException(status_code=422, detail=f"{key} cannot be null")
        setattr(incident, key, value)
    db.commit()
    db.refresh(incident)
    logger.info("Updated incident %s", incident_id)
    return incident


@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = _get_or_404(db, incident_id)
    db.delete(incident)
    db.commit()
    logger.info("Deleted incident %s", incident_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
