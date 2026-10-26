"""CRUD routes for flood/landslide incidents."""
import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import HazardType, Incident, IncidentStatus, Severity, get_db
from schemas import IncidentCreate, IncidentOut, IncidentUpdate
from security import require_api_key

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/incidents", tags=["incidents"], dependencies=[Depends(require_api_key)])


def _get_or_404(db: Session, incident_id: int) -> Incident:
    incident = db.get(Incident, incident_id)
    if incident is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return incident


@router.post("", response_model=IncidentOut, status_code=status.HTTP_201_CREATED)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    incident = Incident(**payload.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    logger.info("Incident created id=%s", incident.id)
    return incident


@router.get("", response_model=List[IncidentOut])
def list_incidents(
    district: Optional[str] = None,
    hazard_type: Optional[HazardType] = None,
    severity: Optional[Severity] = None,
    status_filter: Optional[IncidentStatus] = Query(default=None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    stmt = select(Incident).order_by(Incident.created_at.desc())
    if district:
        stmt = stmt.where(Incident.district == district)
    if hazard_type:
        stmt = stmt.where(Incident.hazard_type == hazard_type)
    if severity:
        stmt = stmt.where(Incident.severity == severity)
    if status_filter:
        stmt = stmt.where(Incident.status == status_filter)
    return db.scalars(stmt.offset(skip).limit(limit)).all()


@router.get("/{incident_id}", response_model=IncidentOut)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, incident_id)


@router.patch("/{incident_id}", response_model=IncidentOut)
def update_incident(incident_id: int, payload: IncidentUpdate, db: Session = Depends(get_db)):
    incident = _get_or_404(db, incident_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        if value is None and field in {"title", "hazard_type", "severity", "status", "district"}:
            raise HTTPException(status_code=422, detail=f"'{field}' cannot be null")
        setattr(incident, field, value)
    db.commit()
    db.refresh(incident)
    logger.info("Incident updated id=%s", incident.id)
    return incident


@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = _get_or_404(db, incident_id)
    for asset in incident.assets:  # unassign assets (SQLite does not enforce FK cascades by default)
        asset.incident_id = None
    db.delete(incident)
    db.commit()
    logger.info("Incident deleted id=%s", incident_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
