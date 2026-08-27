from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TranslationBase(BaseModel):
    source_text: str = Field(..., min_length=1, description="Text to be translated")
    source_language: str = Field(..., min_length=2, max_length=10, description="Source language code")
    target_language: str = Field(..., min_length=2, max_length=10, description="Target language code")


class TranslationCreate(TranslationBase):
    pass


class TranslationUpdate(BaseModel):
    source_text: Optional[str] = Field(None, min_length=1)
    source_language: Optional[str] = Field(None, min_length=2, max_length=10)
    target_language: Optional[str] = Field(None, min_length=2, max_length=10)
    translated_text: Optional[str] = Field(None, min_length=1)


class TranslationResponse(TranslationBase):
    id: int
    translated_text: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
