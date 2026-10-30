"""CRUD routes for response resources (teams, equipment, supplies)."""
import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import (
    Incident,
    Resource,
    ResourceCreate,
    ResourceOut,
    ResourceStatus,
    ResourceUpdate,
)
from security import require_api_key

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/resources", tags=["resources"], dependencies=[Depends(require_api_key)])


def _get_or_404(db: Session, resource_id: int) -> Resource:
    resource = db.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return resource


def _check_incident(db: Session, incident_id: Optional[int]) -> None:
    if incident_id is not None and not db.get(Incident, incident_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Referenced incident not found")


@router.post("", response_model=ResourceOut, status_code=status.HTTP_201_CREATED)
def create_resource(payload: ResourceCreate, db: Session = Depends(get_db)):
    _check_incident(db, payload.incident_id)
    resource = Resource(**payload.model_dump())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    logger.info("Created resource %s", resource.id)
    return resource


@router.get("", response_model=List[ResourceOut])
def list_resources(
    resource_type: Optional[str] = None,
    status_filter: Optional[ResourceStatus] = Query(default=None, alias="status"),
    incident_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    stmt = select(Resource)
    if resource_type:
        stmt = stmt.where(Resource.resource_type == resource_type)
    if status_filter:
        stmt = stmt.where(Resource.status == status_filter)
    if incident_id is not None:
        stmt = stmt.where(Resource.incident_id == incident_id)
    stmt = stmt.order_by(Resource.created_at.desc()).offset(skip).limit(limit)
    return db.scalars(stmt).all()


@router.get("/{resource_id}", response_model=ResourceOut)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, resource_id)


@router.patch("/{resource_id}", response_model=ResourceOut)
def update_resource(resource_id: int, payload: ResourceUpdate, db: Session = Depends(get_db)):
    resource = _get_or_404(db, resource_id)
    data = payload.model_dump(exclude_unset=True)
    if data.get("incident_id") is not None:
        _check_incident(db, data["incident_id"])
    for key, value in data.items():
        if value is None and key in {"name", "resource_type", "quantity", "status"}:
            raise HTTPException(status_code=422, detail=f"{key} cannot be null")
        setattr(resource, key, value)
    db.commit()
    db.refresh(resource)
    logger.info("Updated resource %s", resource_id)
    return resource


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = _get_or_404(db, resource_id)
    db.delete(resource)
    db.commit()
    logger.info("Deleted resource %s", resource_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
