from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_active: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Exercise Schemas
class ExerciseBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    target_muscles: Optional[str] = None
    equipment_needed: Optional[str] = None


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    target_muscles: Optional[str] = None
    equipment_needed: Optional[str] = None


class ExerciseResponse(ExerciseBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Form Assessment Schemas
class FormAssessmentBase(BaseModel):
    exercise_id: int
    form_score: Optional[float] = Field(None, ge=0, le=100)
    feedback: Optional[str] = None
    key_points: Optional[str] = None
    video_url: Optional[str] = None
    notes: Optional[str] = None


class FormAssessmentCreate(FormAssessmentBase):
    pass


class FormAssessmentUpdate(BaseModel):
    form_score: Optional[float] = Field(None, ge=0, le=100)
    feedback: Optional[str] = None
    key_points: Optional[str] = None
    video_url: Optional[str] = None
    notes: Optional[str] = None


class FormAssessmentResponse(FormAssessmentBase):
    id: int
    user_id: int
    assessment_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True
