from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.models import Incident, ResourceDeployment, get_db

router = APIRouter(prefix="/incidents/{incident_id}/resources", tags=["resources"])


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class ResourceCreate(BaseModel):
    resource_type: str = Field(..., min_length=2, max_length=100)
    resource_name: str = Field(..., min_length=2, max_length=255)
    quantity: int = Field(1, ge=1)
    notes: Optional[str] = None


class ResourceUpdate(BaseModel):
    resource_type: Optional[str] = Field(None, min_length=2, max_length=100)
    resource_name: Optional[str] = Field(None, min_length=2, max_length=255)
    quantity: Optional[int] = Field(None, ge=1)
    notes: Optional[str] = None


class ResourceResponse(BaseModel):
    id: int
    incident_id: int
    resource_type: str
    resource_name: str
    quantity: int
    deployed_at: str
    notes: Optional[str]

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_model(cls, obj: ResourceDeployment) -> "ResourceResponse":
        return cls(
            id=obj.id,
            incident_id=obj.incident_id,
            resource_type=obj.resource_type,
            resource_name=obj.resource_name,
            quantity=obj.quantity,
            deployed_at=obj.deployed_at.isoformat(),
            notes=obj.notes,
        )


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _get_incident_or_404(incident_id: int, db: Session) -> Incident:
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


# ---------------------------------------------------------------------------
# CRUD routes
# ---------------------------------------------------------------------------

@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
def deploy_resource(incident_id: int, payload: ResourceCreate, db: Session = Depends(get_db)):
    """Deploy a resource to an existing incident."""
    _get_incident_or_404(incident_id, db)
    resource = ResourceDeployment(incident_id=incident_id, **payload.model_dump())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return ResourceResponse.from_orm_model(resource)


@router.get("/", response_model=List[ResourceResponse])
def list_resources(
    incident_id: int,
    resource_type: Optional[str] = Query(None, description="Filter by resource type"),
    db: Session = Depends(get_db),
):
    """List all resources deployed for an incident."""
    _get_incident_or_404(incident_id, db)
    query = db.query(ResourceDeployment).filter(ResourceDeployment.incident_id == incident_id)
    if resource_type:
        query = query.filter(ResourceDeployment.resource_type.ilike(f"%{resource_type}%"))
    return [ResourceResponse.from_orm_model(r) for r in query.all()]


@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(incident_id: int, resource_id: int, db: Session = Depends(get_db)):
    """Retrieve a single resource deployment."""
    _get_incident_or_404(incident_id, db)
    resource = (
        db.query(ResourceDeployment)
        .filter(ResourceDeployment.id == resource_id, ResourceDeployment.incident_id == incident_id)
        .first()
    )
    if not resource:
        raise HTTPException(status_code=404, detail="Resource deployment not found")
    return ResourceResponse.from_orm_model(resource)


@router.patch("/{resource_id}", response_model=ResourceResponse)
def update_resource(incident_id: int, resource_id: int, payload: ResourceUpdate, db: Session = Depends(get_db)):
    """Update a resource deployment."""
    _get_incident_or_404(incident_id, db)
    resource = (
        db.query(ResourceDeployment)
        .filter(ResourceDeployment.id == resource_id, ResourceDeployment.incident_id == incident_id)
        .first()
    )
    if not resource:
        raise HTTPException(status_code=404, detail="Resource deployment not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(resource, field, value)
    db.commit()
    db.refresh(resource)
    return ResourceResponse.from_orm_model(resource)


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_resource(incident_id: int, resource_id: int, db: Session = Depends(get_db)):
    """Remove a resource deployment from an incident."""
    _get_incident_or_404(incident_id, db)
    resource = (
        db.query(ResourceDeployment)
        .filter(ResourceDeployment.id == resource_id, ResourceDeployment.incident_id == incident_id)
        .first()
    )
    if not resource:
        raise HTTPException(status_code=404, detail="Resource deployment not found")
    db.delete(resource)
    db.commit()
