from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from backend.database import get_db
from backend.models import CourseContent, ContentTranslation
from backend.schemas import (
    TranslationRequest, TranslationResponse,
    ContentTranslationCreate, ContentTranslationResponse
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/translate", response_model=TranslationResponse)
def translate_text(request: TranslationRequest):
    """
    Translate text from source language to target language
    Note: This is a placeholder implementation. In production, integrate with a translation API.
    """
    try:
        # Placeholder implementation - returns mock translation
        # In production, integrate with Google Translate API, DeepL, or similar service
        translated_text = f"[Translated to {request.target_language}] {request.text}"
        
        logger.info(f"Translation requested: {request.source_language} -> {request.target_language}")
        
        return TranslationResponse(
            original_text=request.text,
            translated_text=translated_text,
            source_language=request.source_language,
            target_language=request.target_language
        )
    except Exception as e:
        logger.error(f"Error translating text: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Translation failed"
        )


@router.post("/content", response_model=ContentTranslationResponse, status_code=status.HTTP_201_CREATED)
def create_content_translation(translation: ContentTranslationCreate, db: Session = Depends(get_db)):
    """Create a translation for course content"""
    try:
        # Verify content exists
        content = db.query(CourseContent).filter(CourseContent.id == translation.content_id).first()
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content not found"
            )
        
        # Check if translation already exists for this language
        existing = db.query(ContentTranslation).filter(
            ContentTranslation.content_id == translation.content_id,
            ContentTranslation.language == translation.language
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Translation already exists for this language"
            )
        
        db_translation = ContentTranslation(**translation.model_dump())
        db.add(db_translation)
        db.commit()
        db.refresh(db_translation)
        
        logger.info(f"Created translation for content {translation.content_id} in {translation.language}")
        return db_translation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating content translation: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create translation"
        )


@router.get("/content/{content_id}", response_model=List[ContentTranslationResponse])
def get_content_translations(content_id: int, db: Session = Depends(get_db)):
    """Get all translations for a specific content item"""
    try:
        translations = db.query(ContentTranslation).filter(
            ContentTranslation.content_id == content_id
        ).all()
        return translations
    except Exception as e:
        logger.error(f"Error fetching translations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch translations"
        )


@router.get("/content/{content_id}/language/{language}", response_model=ContentTranslationResponse)
def get_content_translation_by_language(content_id: int, language: str, db: Session = Depends(get_db)):
    """Get a specific translation for content in a given language"""
    try:
        translation = db.query(ContentTranslation).filter(
            ContentTranslation.content_id == content_id,
            ContentTranslation.language == language
        ).first()
        
        if not translation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Translation not found for this language"
            )
        
        return translation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching translation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch translation"
        )


@router.delete("/content/{translation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_content_translation(translation_id: int, db: Session = Depends(get_db)):
    """Delete a content translation"""
    try:
        translation = db.query(ContentTranslation).filter(ContentTranslation.id == translation_id).first()
        if not translation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Translation not found"
            )
        
        db.delete(translation)
        db.commit()
        
        logger.info(f"Deleted translation: {translation_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting translation: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete translation"
        )
