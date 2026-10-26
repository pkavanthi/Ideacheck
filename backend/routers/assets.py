"""CRUD routes for response assets (rescue teams, drones, floodgates, pumps, grid nodes)."""
import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Asset, AssetStatus, AssetType, Incident, get_db
from schemas import AssetCreate, AssetOut, AssetUpdate
from security import require_api_key

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/assets", tags=["assets"], dependencies=[Depends(require_api_key)])


def _get_or_404(db: Session, asset_id: int) -> Asset:
    asset = db.get(Asset, asset_id)
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return asset


def _check_incident(db: Session, incident_id: Optional[int]) -> None:
    if incident_id is not None and db.get(Incident, incident_id) is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="incident_id does not exist")


@router.post("", response_model=AssetOut, status_code=status.HTTP_201_CREATED)
def create_asset(payload: AssetCreate, db: Session = Depends(get_db)):
    _check_incident(db, payload.incident_id)
    asset = Asset(**payload.model_dump())
    db.add(asset)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Asset name already exists")
    db.refresh(asset)
    logger.info("Asset created id=%s", asset.id)
    return asset


@router.get("", response_model=List[AssetOut])
def list_assets(
    district: Optional[str] = None,
    asset_type: Optional[AssetType] = None,
    status_filter: Optional[AssetStatus] = Query(default=None, alias="status"),
    incident_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    stmt = select(Asset).order_by(Asset.id)
    if district:
        stmt = stmt.where(Asset.district == district)
    if asset_type:
        stmt = stmt.where(Asset.asset_type == asset_type)
    if status_filter:
        stmt = stmt.where(Asset.status == status_filter)
    if incident_id is not None:
        stmt = stmt.where(Asset.incident_id == incident_id)
    return db.scalars(stmt.offset(skip).limit(limit)).all()


@router.get("/{asset_id}", response_model=AssetOut)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, asset_id)


@router.patch("/{asset_id}", response_model=AssetOut)
def update_asset(asset_id: int, payload: AssetUpdate, db: Session = Depends(get_db)):
    asset = _get_or_404(db, asset_id)
    data = payload.model_dump(exclude_unset=True)
    for field in ("name", "asset_type", "status", "district"):
        if field in data and data[field] is None:
            raise HTTPException(status_code=422, detail=f"'{field}' cannot be null")
    _check_incident(db, data.get("incident_id"))
    for field, value in data.items():
        setattr(asset, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Asset name already exists")
    db.refresh(asset)
    logger.info("Asset updated id=%s", asset.id)
    return asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = _get_or_404(db, asset_id)
    db.delete(asset)
    db.commit()
    logger.info("Asset deleted id=%s", asset_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
