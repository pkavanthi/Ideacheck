import logging
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models import HazardType, RiskAlert, SeverityLevel, get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/alerts", tags=["Risk Alerts"])


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class AlertCreate(BaseModel):
    event_id: Optional[int] = None
    hazard_type: HazardType
    severity: SeverityLevel
    region: str = Field(..., min_length=2, max_length=255)
    message: str = Field(..., min_length=5)
    issued_by: Optional[str] = None
    expires_at: Optional[datetime] = None


class AlertUpdate(BaseModel):
    severity: Optional[SeverityLevel] = None
    region: Optional[str] = Field(None, min_length=2, max_length=255)
    message: Optional[str] = Field(None, min_length=5)
    active: Optional[int] = Field(None, ge=0, le=1)
    expires_at: Optional[datetime] = None


class AlertResponse(BaseModel):
    id: int
    event_id: Optional[int]
    hazard_type: HazardType
    severity: SeverityLevel
    region: str
    message: str
    issued_by: Optional[str]
    active: int
    issued_at: str
    expires_at: Optional[str]

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@router.post("/", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
def create_alert(payload: AlertCreate, db: Session = Depends(get_db)):
    """Issue a new risk alert."""
    alert = RiskAlert(**payload.model_dump())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    logger.info("Issued alert id=%s region=%s", alert.id, alert.region)
    return _to_response(alert)


@router.get("/", response_model=List[AlertResponse])
def list_alerts(
    hazard_type: Optional[HazardType] = Query(None),
    active_only: bool = Query(True),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """List risk alerts with optional filtering."""
    query = db.query(RiskAlert)
    if hazard_type:
        query = query.filter(RiskAlert.hazard_type == hazard_type)
    if active_only:
        query = query.filter(RiskAlert.active == 1)
    return [_to_response(a) for a in query.offset(skip).limit(limit).all()]


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """Fetch a single alert by ID."""
    return _to_response(_get_or_404(db, alert_id))


@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(alert_id: int, payload: AlertUpdate, db: Session = Depends(get_db)):
    """Update an existing alert (e.g. resolve it by setting active=0)."""
    alert = _get_or_404(db, alert_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(alert, field, value)
    db.commit()
    db.refresh(alert)
    logger.info("Updated alert id=%s active=%s", alert.id, alert.active)
    return _to_response(alert)


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    """Delete an alert."""
    alert = _get_or_404(db, alert_id)
    db.delete(alert)
    db.commit()
    logger.info("Deleted alert id=%s", alert_id)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _get_or_404(db: Session, alert_id: int) -> RiskAlert:
    alert = db.query(RiskAlert).filter(RiskAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


def _to_response(alert: RiskAlert) -> dict:
    data = {c.name: getattr(alert, c.name) for c in alert.__table__.columns if c.name not in ("issued_at", "expires_at")}
    data["issued_at"] = alert.issued_at.isoformat()
    data["expires_at"] = alert.expires_at.isoformat() if alert.expires_at else None
    return data
