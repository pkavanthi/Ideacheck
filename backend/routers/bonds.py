from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Bond, BondStatus, Farmer
from backend.schemas import BondCreate, BondOut, BondUpdate

router = APIRouter(prefix="/bonds", tags=["bonds"])


@router.post("/", response_model=BondOut, status_code=status.HTTP_201_CREATED)
def create_bond(payload: BondCreate, db: Session = Depends(get_db)):
    farmer = db.get(Farmer, payload.farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    bond = Bond(**payload.model_dump())
    db.add(bond)
    db.commit()
    db.refresh(bond)
    return bond


@router.get("/", response_model=List[BondOut])
def list_bonds(
    skip: int = 0,
    limit: int = 100,
    status: BondStatus | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Bond)
    if status:
        query = query.filter(Bond.status == status)
    return query.offset(skip).limit(limit).all()


@router.get("/{bond_id}", response_model=BondOut)
def get_bond(bond_id: int, db: Session = Depends(get_db)):
    bond = db.get(Bond, bond_id)
    if not bond:
        raise HTTPException(status_code=404, detail="Bond not found")
    return bond


@router.patch("/{bond_id}", response_model=BondOut)
def update_bond(bond_id: int, payload: BondUpdate, db: Session = Depends(get_db)):
    bond = db.get(Bond, bond_id)
    if not bond:
        raise HTTPException(status_code=404, detail="Bond not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(bond, field, value)
    db.commit()
    db.refresh(bond)
    return bond


@router.delete("/{bond_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bond(bond_id: int, db: Session = Depends(get_db)):
    bond = db.get(Bond, bond_id)
    if not bond:
        raise HTTPException(status_code=404, detail="Bond not found")
    # Only pending bonds can be deleted; verified/active/redeemed are immutable
    if bond.status not in (BondStatus.PENDING, BondStatus.CANCELLED):
        raise HTTPException(
            status_code=400,
            detail="Only pending or cancelled bonds can be deleted",
        )
    db.delete(bond)
    db.commit()
