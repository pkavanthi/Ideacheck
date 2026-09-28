import logging
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Alert, AlertSeverity, AlertStatus, HazardType

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/alerts", tags=["alerts"])


# ── Schemas ──────────────────────────────────────────────────────────────────


class AlertCreate(BaseModel):
    district_id: int
    title: str
    description: Optional[str] = None
    hazard_type: HazardType
    severity: AlertSeverity = AlertSeverity.MEDIUM
    affected_population: Optional[int] = None
    evacuation_required: bool = False
    evacuation_zones: Optional[str] = None
    issued_by: Optional[str] = None
    expires_at: Optional[datetime] = None


class AlertUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[AlertSeverity] = None
    status: Optional[AlertStatus] = None
    affected_population: Optional[int] = None
    evacuation_required: Optional[bool] = None
    evacuation_zones: Optional[str] = None
    expires_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None


class AlertResponse(BaseModel):
    id: int
    district_id: int
    title: str
    description: Optional[str]
    hazard_type: HazardType
    severity: AlertSeverity
    status: AlertStatus
    affected_population: Optional[int]
    evacuation_required: bool
    evacuation_zones: Optional[str]
    issued_by: Optional[str]
    issued_at: datetime
    expires_at: Optional[datetime]
    resolved_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ── Endpoints ─────────────────────────────────────────────────────────────────


@router.post("/", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
def create_alert(payload: AlertCreate, db: Session = Depends(get_db)):
    alert = Alert(**payload.model_dump())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    logger.info("Alert created: id=%s district_id=%s", alert.id, alert.district_id)
    return alert


@router.get("/", response_model=List[AlertResponse])
def list_alerts(
    district_id: Optional[int] = Query(None),
    hazard_type: Optional[HazardType] = Query(None),
    severity: Optional[AlertSeverity] = Query(None),
    status: Optional[AlertStatus] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(Alert)
    if district_id is not None:
        q = q.filter(Alert.district_id == district_id)
    if hazard_type is not None:
        q = q.filter(Alert.hazard_type == hazard_type)
    if severity is not None:
        q = q.filter(Alert.severity == severity)
    if status is not None:
        q = q.filter(Alert.status == status)
    return q.order_by(Alert.issued_at.desc()).offset(skip).limit(limit).all()


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.patch("/{alert_id}", response_model=AlertResponse)
def update_alert(alert_id: int, payload: AlertUpdate, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(alert, field, value)
    alert.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(alert)
    logger.info("Alert updated: id=%s", alert_id)
    return alert


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(alert)
    db.commit()
    logger.info("Alert deleted: id=%s", alert_id)
