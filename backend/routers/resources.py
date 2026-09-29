from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database import get_db
from backend.models import ReliefResource
from backend.schemas import ResourceCreate, ResourceUpdate, ResourceResponse

router = APIRouter(prefix="/resources", tags=["Relief Resources"])

@router.get("/", response_model=List[ResourceResponse])
def get_resources(
    district: Optional[str] = None,
    resource_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ReliefResource)
    if district:
        query = query.filter(ReliefResource.district.ilike(f"%{district}%"))
    if resource_type:
        query = query.filter(ReliefResource.resource_type == resource_type)
    return query.order_by(ReliefResource.id.asc()).all()

@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
def create_resource(payload: ResourceCreate, db: Session = Depends(get_db)):
    resource = ReliefResource(**payload.model_dump())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource

@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(ReliefResource).filter(ReliefResource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail=f"Resource #{resource_id} not found")
    return resource

@router.put("/{resource_id}", response_model=ResourceResponse)
def update_resource(resource_id: int, payload: ResourceUpdate, db: Session = Depends(get_db)):
    resource = db.query(ReliefResource).filter(ReliefResource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail=f"Resource #{resource_id} not found")
    
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(resource, field, value)
    
    db.commit()
    db.refresh(resource)
    return resource

@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(ReliefResource).filter(ReliefResource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail=f"Resource #{resource_id} not found")
    db.delete(resource)
    db.commit()
    return None
