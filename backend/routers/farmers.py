from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Buyer, FPO, Farmer
from backend.schemas import (
    BuyerCreate,
    BuyerOut,
    BuyerUpdate,
    FPOCreate,
    FPOOut,
    FPOUpdate,
    FarmerCreate,
    FarmerOut,
    FarmerUpdate,
)

router = APIRouter(tags=["farmers"])

# ---------------------------------------------------------------------------
# Farmer endpoints
# ---------------------------------------------------------------------------

farmers_router = APIRouter(prefix="/farmers")


@farmers_router.post("/", response_model=FarmerOut, status_code=status.HTTP_201_CREATED)
def create_farmer(payload: FarmerCreate, db: Session = Depends(get_db)):
    existing = db.query(Farmer).filter(Farmer.phone == payload.phone).first()
    if existing:
        raise HTTPException(status_code=409, detail="Phone number already registered")
    farmer = Farmer(**payload.model_dump())
    db.add(farmer)
    db.commit()
    db.refresh(farmer)
    return farmer


@farmers_router.get("/", response_model=List[FarmerOut])
def list_farmers(
    skip: int = 0,
    limit: int = 100,
    district: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Farmer)
    if district:
        query = query.filter(Farmer.district.ilike(f"%{district}%"))
    return query.offset(skip).limit(limit).all()


@farmers_router.get("/{farmer_id}", response_model=FarmerOut)
def get_farmer(farmer_id: int, db: Session = Depends(get_db)):
    farmer = db.get(Farmer, farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return farmer


@farmers_router.patch("/{farmer_id}", response_model=FarmerOut)
def update_farmer(farmer_id: int, payload: FarmerUpdate, db: Session = Depends(get_db)):
    farmer = db.get(Farmer, farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(farmer, field, value)
    db.commit()
    db.refresh(farmer)
    return farmer


@farmers_router.delete("/{farmer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_farmer(farmer_id: int, db: Session = Depends(get_db)):
    farmer = db.get(Farmer, farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    db.delete(farmer)
    db.commit()


# ---------------------------------------------------------------------------
# FPO endpoints
# ---------------------------------------------------------------------------

fpo_router = APIRouter(prefix="/fpos")


@fpo_router.post("/", response_model=FPOOut, status_code=status.HTTP_201_CREATED)
def create_fpo(payload: FPOCreate, db: Session = Depends(get_db)):
    existing = db.query(FPO).filter(FPO.registration_number == payload.registration_number).first()
    if existing:
        raise HTTPException(status_code=409, detail="FPO registration number already exists")
    fpo = FPO(**payload.model_dump())
    db.add(fpo)
    db.commit()
    db.refresh(fpo)
    return fpo


@fpo_router.get("/", response_model=List[FPOOut])
def list_fpos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(FPO).offset(skip).limit(limit).all()


@fpo_router.get("/{fpo_id}", response_model=FPOOut)
def get_fpo(fpo_id: int, db: Session = Depends(get_db)):
    fpo = db.get(FPO, fpo_id)
    if not fpo:
        raise HTTPException(status_code=404, detail="FPO not found")
    return fpo


@fpo_router.patch("/{fpo_id}", response_model=FPOOut)
def update_fpo(fpo_id: int, payload: FPOUpdate, db: Session = Depends(get_db)):
    fpo = db.get(FPO, fpo_id)
    if not fpo:
        raise HTTPException(status_code=404, detail="FPO not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(fpo, field, value)
    db.commit()
    db.refresh(fpo)
    return fpo


@fpo_router.delete("/{fpo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fpo(fpo_id: int, db: Session = Depends(get_db)):
    fpo = db.get(FPO, fpo_id)
    if not fpo:
        raise HTTPException(status_code=404, detail="FPO not found")
    db.delete(fpo)
    db.commit()


# ---------------------------------------------------------------------------
# Buyer endpoints
# ---------------------------------------------------------------------------

buyer_router = APIRouter(prefix="/buyers")


@buyer_router.post("/", response_model=BuyerOut, status_code=status.HTTP_201_CREATED)
def create_buyer(payload: BuyerCreate, db: Session = Depends(get_db)):
    existing = db.query(Buyer).filter(Buyer.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    buyer = Buyer(**payload.model_dump())
    db.add(buyer)
    db.commit()
    db.refresh(buyer)
    return buyer


@buyer_router.get("/", response_model=List[BuyerOut])
def list_buyers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Buyer).offset(skip).limit(limit).all()


@buyer_router.get("/{buyer_id}", response_model=BuyerOut)
def get_buyer(buyer_id: int, db: Session = Depends(get_db)):
    buyer = db.get(Buyer, buyer_id)
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return buyer


@buyer_router.patch("/{buyer_id}", response_model=BuyerOut)
def update_buyer(buyer_id: int, payload: BuyerUpdate, db: Session = Depends(get_db)):
    buyer = db.get(Buyer, buyer_id)
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(buyer, field, value)
    db.commit()
    db.refresh(buyer)
    return buyer


@buyer_router.delete("/{buyer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_buyer(buyer_id: int, db: Session = Depends(get_db)):
    buyer = db.get(Buyer, buyer_id)
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    db.delete(buyer)
    db.commit()
