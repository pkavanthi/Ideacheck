from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# Student Schemas
class StudentBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    grade_level: Optional[str] = None
    learning_style: Optional[str] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    grade_level: Optional[str] = None
    learning_style: Optional[str] = None


class Student(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Course Schemas
class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    subject: str = Field(..., min_length=1, max_length=100)
    difficulty_level: Optional[str] = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    subject: Optional[str] = Field(None, min_length=1, max_length=100)
    difficulty_level: Optional[str] = None


class Course(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Enrollment Schemas
class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(BaseModel):
    progress: Optional[float] = Field(None, ge=0.0, le=100.0)
    status: Optional[str] = None


class Enrollment(EnrollmentBase):
    id: int
    enrollment_date: datetime
    progress: float
    status: str

    class Config:
        from_attributes = True
