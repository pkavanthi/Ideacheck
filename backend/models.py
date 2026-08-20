from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class HealthCenter(Base):
    __tablename__ = "health_centers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    contact_number = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    capacity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    diagnostics = relationship("Diagnostic", back_populates="health_center")


class Diagnostic(Base):
    __tablename__ = "diagnostics"
    
    id = Column(Integer, primary_key=True, index=True)
    health_center_id = Column(Integer, ForeignKey("health_centers.id"), nullable=False)
    patient_name = Column(String(255), nullable=False)
    patient_age = Column(Integer, nullable=True)
    patient_gender = Column(String(10), nullable=True)
    diagnosis_type = Column(String(100), nullable=False)
    symptoms = Column(Text, nullable=True)
    diagnosis_result = Column(Text, nullable=True)
    status = Column(String(50), default="pending")
    priority = Column(String(20), default="normal")
    assigned_specialist = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    health_center = relationship("HealthCenter", back_populates="diagnostics")
