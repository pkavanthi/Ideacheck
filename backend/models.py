import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class FarmerStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class BondStatus(str, enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    ACTIVE = "active"
    REDEEMED = "redeemed"
    CANCELLED = "cancelled"


class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    phone = Column(String(20), unique=True, nullable=False, index=True)
    village = Column(String(200), nullable=False)
    district = Column(String(200), nullable=False)
    state = Column(String(100), nullable=False)
    land_area_acres = Column(Float, nullable=False)
    crop_type = Column(String(100), nullable=False)
    fpo_id = Column(Integer, ForeignKey("fpos.id"), nullable=True)
    status = Column(Enum(FarmerStatus), default=FarmerStatus.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    fpo = relationship("FPO", back_populates="farmers")
    bonds = relationship("Bond", back_populates="farmer")


class FPO(Base):
    """Farmer Producer Organisation"""

    __tablename__ = "fpos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300), nullable=False)
    registration_number = Column(String(100), unique=True, nullable=False, index=True)
    treasurer_name = Column(String(200), nullable=False)
    treasurer_phone = Column(String(20), nullable=False)
    district = Column(String(200), nullable=False)
    state = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    farmers = relationship("Farmer", back_populates="fpo")


class Bond(Base):
    """Harvest-backed rural bond"""

    __tablename__ = "bonds"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False, index=True)
    # Harvest fraction details
    crop_type = Column(String(100), nullable=False)
    harvest_quantity_kg = Column(Float, nullable=False)
    harvest_fraction = Column(Float, nullable=False)  # 0.0 – 1.0 fraction of harvest
    # Financial details
    face_value = Column(Float, nullable=False)  # INR
    issued_capital = Column(Float, nullable=True)  # INR actually disbursed
    interest_rate_pct = Column(Float, nullable=False)
    maturity_date = Column(DateTime, nullable=False)
    # Provenance & verification
    verifier_name = Column(String(200), nullable=True)
    verification_notes = Column(Text, nullable=True)
    buyer_id = Column(Integer, ForeignKey("buyers.id"), nullable=True, index=True)
    status = Column(Enum(BondStatus), default=BondStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    farmer = relationship("Farmer", back_populates="bonds")
    buyer = relationship("Buyer", back_populates="bonds")


class Buyer(Base):
    """Institutional agri-buyer"""

    __tablename__ = "buyers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300), nullable=False)
    organisation = Column(String(300), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(254), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bonds = relationship("Bond", back_populates="buyer")
