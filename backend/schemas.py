from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from backend.models import ContentType, LanguageCode


# Content Schemas
class ContentBase(BaseModel):
    """Base content schema"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    content_type: ContentType
    original_language: LanguageCode
    original_text: str = Field(..., min_length=1)
    created_by: str = Field(..., min_length=1, max_length=255)


class ContentCreate(ContentBase):
    """Schema for creating content"""
    pass


class ContentUpdate(BaseModel):
    """Schema for updating content"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    content_type: Optional[ContentType] = None
    original_text: Optional[str] = Field(None, min_length=1)


class ContentResponse(ContentBase):
    """Schema for content response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ContentWithTranslations(ContentResponse):
    """Schema for content with translations"""
    translations: List["TranslationResponse"] = []

    class Config:
        from_attributes = True


# Translation Schemas
class TranslationBase(BaseModel):
    """Base translation schema"""
    target_language: LanguageCode
    translated_text: str = Field(..., min_length=1)
    translated_title: Optional[str] = Field(None, max_length=255)


class TranslationCreate(TranslationBase):
    """Schema for creating translation"""
    content_id: int


class TranslationUpdate(BaseModel):
    """Schema for updating translation"""
    translated_text: Optional[str] = Field(None, min_length=1)
    translated_title: Optional[str] = Field(None, max_length=255)


class TranslationResponse(TranslationBase):
    """Schema for translation response"""
    id: int
    content_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
