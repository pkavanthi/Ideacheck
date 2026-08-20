from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from backend.models import ConsultationStatus


# Patient Schemas
class PatientBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    date_of_birth: datetime
    address: Optional[str] = None
    medical_history: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    date_of_birth: Optional[datetime] = None
    address: Optional[str] = None
    medical_history: Optional[str] = None


class Patient(PatientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Health Worker Schemas
class HealthWorkerBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    certification: Optional[str] = None
    location: str = Field(..., min_length=1, max_length=255)


class HealthWorkerCreate(HealthWorkerBase):
    pass


class HealthWorkerUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    certification: Optional[str] = None
    location: Optional[str] = Field(None, min_length=1, max_length=255)


class HealthWorker(HealthWorkerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Consultation Schemas
class ConsultationBase(BaseModel):
    patient_id: int
    health_worker_id: int
    scheduled_at: datetime
    symptoms: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment_plan: Optional[str] = None
    notes: Optional[str] = None


class ConsultationCreate(ConsultationBase):
    pass


class ConsultationUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    status: Optional[ConsultationStatus] = None
    symptoms: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment_plan: Optional[str] = None
    notes: Optional[str] = None


class Consultation(ConsultationBase):
    id: int
    status: ConsultationStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
