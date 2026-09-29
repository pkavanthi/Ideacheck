from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Resource, ResourceDeployment, ResourceStatus, ResourceType

router = APIRouter(prefix="/resources", tags=["resources"])


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class ResourceCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    resource_type: ResourceType
    quantity: int = Field(1, ge=1)
    location: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    contact_info: Optional[str] = Field(None, max_length=500)


class ResourceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    resource_type: Optional[ResourceType] = None
    quantity: Optional[int] = Field(None, ge=0)
    status: Optional[ResourceStatus] = None
    location: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    contact_info: Optional[str] = Field(None, max_length=500)


class ResourceResponse(BaseModel):
    id: int
    name: str
    resource_type: ResourceType
    quantity: int
    status: ResourceStatus
    location: Optional[str]
    description: Optional[str]
    contact_info: Optional[str]
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_model(cls, resource: Resource) -> "ResourceResponse":
        return cls(
            id=resource.id,
            name=resource.name,
            resource_type=resource.resource_type,
            quantity=resource.quantity,
            status=resource.status,
            location=resource.location,
            description=resource.description,
            contact_info=resource.contact_info,
            created_at=resource.created_at.isoformat(),
            updated_at=resource.updated_at.isoformat(),
        )


class DeploymentCreate(BaseModel):
    resource_id: int
    quantity_deployed: int = Field(1, ge=1)
    notes: Optional[str] = None


class DeploymentResponse(BaseModel):
    id: int
    incident_id: int
    resource_id: int
    quantity_deployed: int
    notes: Optional[str]
    deployed_at: str
    recalled_at: Optional[str]

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_model(cls, dep: ResourceDeployment) -> "DeploymentResponse":
        return cls(
            id=dep.id,
            incident_id=dep.incident_id,
            resource_id=dep.resource_id,
            quantity_deployed=dep.quantity_deployed,
            notes=dep.notes,
            deployed_at=dep.deployed_at.isoformat(),
            recalled_at=dep.recalled_at.isoformat() if dep.recalled_at else None,
        )


# ---------------------------------------------------------------------------
# Resource CRUD endpoints
# ---------------------------------------------------------------------------

@router.get("/", response_model=List[ResourceResponse], summary="List all resources")
def list_resources(
    resource_type: Optional[ResourceType] = Query(None, description="Filter by type"),
    status: Optional[ResourceStatus] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    query = db.query(Resource)
    if resource_type:
        query = query.filter(Resource.resource_type == resource_type)
    if status:
        query = query.filter(Resource.status == status)
    resources = query.order_by(Resource.created_at.desc()).offset(skip).limit(limit).all()
    return [ResourceResponse.from_orm_model(r) for r in resources]


@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED, summary="Register a new resource")
def create_resource(payload: ResourceCreate, db: Session = Depends(get_db)):
    resource = Resource(**payload.model_dump())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return ResourceResponse.from_orm_model(resource)


@router.get("/{resource_id}", response_model=ResourceResponse, summary="Get resource details")
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return ResourceResponse.from_orm_model(resource)


@router.put("/{resource_id}", response_model=ResourceResponse, summary="Update a resource")
def update_resource(resource_id: int, payload: ResourceUpdate, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(resource, field, value)
    db.commit()
    db.refresh(resource)
    return ResourceResponse.from_orm_model(resource)


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a resource")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    db.delete(resource)
    db.commit()


# ---------------------------------------------------------------------------
# Resource Deployment endpoints (nested under incidents via this router)
# ---------------------------------------------------------------------------

@router.post(
    "/deployments/incident/{incident_id}",
    response_model=DeploymentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Deploy a resource to an incident",
)
def deploy_resource(incident_id: int, payload: DeploymentCreate, db: Session = Depends(get_db)):
    from backend.models import Incident  # local import to avoid circular

    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")

    resource = db.query(Resource).filter(Resource.id == payload.resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    if resource.quantity < payload.quantity_deployed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient quantity. Available: {resource.quantity}",
        )

    deployment = ResourceDeployment(
        incident_id=incident_id,
        resource_id=payload.resource_id,
        quantity_deployed=payload.quantity_deployed,
        notes=payload.notes,
    )
    resource.quantity -= payload.quantity_deployed
    if resource.quantity == 0:
        resource.status = ResourceStatus.DEPLOYED

    db.add(deployment)
    db.commit()
    db.refresh(deployment)
    return DeploymentResponse.from_orm_model(deployment)
