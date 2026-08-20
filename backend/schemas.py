from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    native_language: str = Field(..., min_length=2, max_length=50)
    proficiency_level: str = Field(..., pattern="^(beginner|intermediate|advanced|native)$")


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    native_language: Optional[str] = Field(None, min_length=2, max_length=50)
    proficiency_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced|native)$")


class Student(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    original_language: str = Field(..., min_length=2, max_length=50)
    instructor_name: str = Field(..., min_length=1, max_length=255)


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    original_language: Optional[str] = Field(None, min_length=2, max_length=50)
    instructor_name: Optional[str] = Field(None, min_length=1, max_length=255)


class Course(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    status: str = Field(default="active", pattern="^(active|completed|dropped)$")


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(active|completed|dropped)$")
    grade: Optional[float] = Field(None, ge=0, le=100)


class Enrollment(EnrollmentBase):
    id: int
    enrollment_date: datetime
    grade: Optional[float] = None

    class Config:
        from_attributes = True
