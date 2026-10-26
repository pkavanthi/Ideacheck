import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Resource, ResourceStatus

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/resources", tags=["Resources"])


# ── Schemas ─────────────────────────────────────────────────────────────────

class ResourceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    type: str = Field(..., min_length=1, max_length=100)
    quantity: int = Field(default=1, ge=1)
    unit: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=255)
    status: ResourceStatus = ResourceStatus.AVAILABLE
    contact_info: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = None


class ResourceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[str] = Field(None, min_length=1, max_length=100)
    quantity: Optional[int] = Field(None, ge=1)
    unit: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=255)
    status: Optional[ResourceStatus] = None
    contact_info: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = None


class ResourceResponse(BaseModel):
    id: int
    name: str
    type: str
    quantity: int
    unit: Optional[str]
    location: Optional[str]
    status: ResourceStatus
    contact_info: Optional[str]
    notes: Optional[str]
    created_at: str
    updated_at: Optional[str]

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_safe(cls, obj: Resource) -> "ResourceResponse":
        return cls(
            id=obj.id,
            name=obj.name,
            type=obj.type,
            quantity=obj.quantity,
            unit=obj.unit,
            location=obj.location,
            status=obj.status,
            contact_info=obj.contact_info,
            notes=obj.notes,
            created_at=obj.created_at.isoformat(),
            updated_at=obj.updated_at.isoformat() if obj.updated_at else None,
        )


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
def create_resource(payload: ResourceCreate, db: Session = Depends(get_db)):
    resource = Resource(**payload.model_dump())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    logger.info("Created resource id=%s name=%r", resource.id, resource.name)
    return ResourceResponse.from_orm_safe(resource)


@router.get("/", response_model=List[ResourceResponse])
def list_resources(
    status: Optional[ResourceStatus] = Query(None),
    type: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(Resource)
    if status:
        query = query.filter(Resource.status == status)
    if type:
        query = query.filter(Resource.type == type)
    resources = query.order_by(Resource.created_at.desc()).offset(skip).limit(limit).all()
    return [ResourceResponse.from_orm_safe(r) for r in resources]


@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return ResourceResponse.from_orm_safe(resource)


@router.patch("/{resource_id}", response_model=ResourceResponse)
def update_resource(resource_id: int, payload: ResourceUpdate, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(resource, field, value)
    db.commit()
    db.refresh(resource)
    logger.info("Updated resource id=%s", resource_id)
    return ResourceResponse.from_orm_safe(resource)


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(resource)
    db.commit()
    logger.info("Deleted resource id=%s", resource_id)
