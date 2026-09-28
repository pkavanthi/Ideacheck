"""
Health Records router — CRUD for health observations per village.
Categories: maternal_health, immunisation, nutrition, disease_outbreak, other
"""

import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import HealthRecord, Village, ASHAWorker

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health-records", tags=["Health Records"])

VALID_CATEGORIES = {
    "maternal_health",
    "immunisation",
    "nutrition",
    "disease_outbreak",
    "sanitation",
    "other",
}

# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class HealthRecordCreate(BaseModel):
    village_id: int = Field(..., gt=0)
    reported_by_id: Optional[int] = Field(None, gt=0)
    record_date: Optional[datetime] = None
    category: str = Field(..., min_length=1, max_length=100)
    indicator: str = Field(..., min_length=1, max_length=200)
    value: Optional[float] = None
    unit: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None
    is_gap_detected: bool = False

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        if v not in VALID_CATEGORIES:
            raise ValueError(f"category must be one of {sorted(VALID_CATEGORIES)}")
        return v


class HealthRecordUpdate(BaseModel):
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    indicator: Optional[str] = Field(None, min_length=1, max_length=200)
    value: Optional[float] = None
    unit: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None
    is_gap_detected: Optional[bool] = None
    record_date: Optional[datetime] = None

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_CATEGORIES:
            raise ValueError(f"category must be one of {sorted(VALID_CATEGORIES)}")
        return v


class HealthRecordResponse(BaseModel):
    id: int
    village_id: int
    reported_by_id: Optional[int]
    record_date: datetime
    category: str
    indicator: str
    value: Optional[float]
    unit: Optional[str]
    notes: Optional[str]
    is_gap_detected: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/", response_model=list[HealthRecordResponse], summary="List health records")
def list_health_records(
    village_id: Optional[int] = Query(None, gt=0, description="Filter by village"),
    category: Optional[str] = Query(None, description="Filter by category"),
    is_gap_detected: Optional[bool] = Query(None, description="Filter gap-detected records"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    stmt = select(HealthRecord)
    if village_id is not None:
        stmt = stmt.where(HealthRecord.village_id == village_id)
    if category is not None:
        stmt = stmt.where(HealthRecord.category == category)
    if is_gap_detected is not None:
        stmt = stmt.where(HealthRecord.is_gap_detected == is_gap_detected)
    stmt = stmt.order_by(HealthRecord.record_date.desc()).offset(skip).limit(limit)
    records = db.execute(stmt).scalars().all()
    return records


@router.post("/", response_model=HealthRecordResponse, status_code=status.HTTP_201_CREATED, summary="Create health record")
def create_health_record(payload: HealthRecordCreate, db: Session = Depends(get_db)):
    # Verify village exists
    village = db.get(Village, payload.village_id)
    if not village:
        raise HTTPException(status_code=404, detail=f"Village {payload.village_id} not found")

    # Verify ASHA worker exists if provided
    if payload.reported_by_id is not None:
        worker = db.get(ASHAWorker, payload.reported_by_id)
        if not worker:
            raise HTTPException(status_code=404, detail=f"ASHAWorker {payload.reported_by_id} not found")

    data = payload.model_dump(exclude_none=False)
    data["record_date"] = payload.record_date or datetime.utcnow()
    record = HealthRecord(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    logger.info("Created HealthRecord id=%s for village_id=%s", record.id, record.village_id)
    return record


@router.get("/{record_id}", response_model=HealthRecordResponse, summary="Get health record")
def get_health_record(record_id: int, db: Session = Depends(get_db)):
    record = db.get(HealthRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"HealthRecord {record_id} not found")
    return record


@router.patch("/{record_id}", response_model=HealthRecordResponse, summary="Update health record")
def update_health_record(record_id: int, payload: HealthRecordUpdate, db: Session = Depends(get_db)):
    record = db.get(HealthRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"HealthRecord {record_id} not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)
    logger.info("Updated HealthRecord id=%s", record_id)
    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete health record")
def delete_health_record(record_id: int, db: Session = Depends(get_db)):
    record = db.get(HealthRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"HealthRecord {record_id} not found")
    db.delete(record)
    db.commit()
    logger.info("Deleted HealthRecord id=%s", record_id)


@router.get("/summary/gaps", response_model=list[dict], summary="Villages with most health gaps")
def health_gaps_summary(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Return the villages with the highest number of gap-detected health records."""
    rows = (
        db.execute(
            select(
                Village.id.label("village_id"),
                Village.name.label("village_name"),
                Village.district,
                Village.state,
                func.count(HealthRecord.id).label("gap_count"),
            )
            .join(HealthRecord, HealthRecord.village_id == Village.id)
            .where(HealthRecord.is_gap_detected == True)  # noqa: E712
            .group_by(Village.id, Village.name, Village.district, Village.state)
            .order_by(func.count(HealthRecord.id).desc())
            .limit(limit)
        )
        .mappings()
        .all()
    )
    return [dict(row) for row in rows]
