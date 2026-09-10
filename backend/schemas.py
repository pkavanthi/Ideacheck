from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List


# Student Schemas
class StudentBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    native_language: str = Field(..., min_length=2, max_length=50)
    preferred_language: str = Field(..., min_length=2, max_length=50)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    native_language: Optional[str] = Field(None, min_length=2, max_length=50)
    preferred_language: Optional[str] = Field(None, min_length=2, max_length=50)


class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Course Schemas
class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    original_language: str = Field(..., min_length=2, max_length=50)
    instructor_name: str = Field(..., min_length=1, max_length=255)
    is_active: bool = True


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    instructor_name: Optional[str] = Field(None, min_length=1, max_length=255)
    is_active: Optional[bool] = None


class CourseResponse(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Enrollment Schemas
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime
    
    class Config:
        from_attributes = True


# Course Content Schemas
class CourseContentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    content_type: str = Field(default="text", max_length=50)
    order: int = Field(default=0, ge=0)


class CourseContentCreate(CourseContentBase):
    course_id: int


class CourseContentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1)
    content_type: Optional[str] = Field(None, max_length=50)
    order: Optional[int] = Field(None, ge=0)


class CourseContentResponse(CourseContentBase):
    id: int
    course_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Translation Schemas
class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1)
    source_language: str = Field(..., min_length=2, max_length=50)
    target_language: str = Field(..., min_length=2, max_length=50)


class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str


class ContentTranslationCreate(BaseModel):
    content_id: int
    language: str = Field(..., min_length=2, max_length=50)
    translated_title: str = Field(..., min_length=1, max_length=255)
    translated_content: str = Field(..., min_length=1)


class ContentTranslationResponse(BaseModel):
    id: int
    content_id: int
    language: str
    translated_title: str
    translated_content: str
    created_at: datetime
    
    class Config:
        from_attributes = True
