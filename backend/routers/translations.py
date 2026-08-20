from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from backend.database import get_db
from backend.models import Translation, Content
from backend.schemas import TranslationCreate, TranslationUpdate, TranslationResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=TranslationResponse, status_code=status.HTTP_201_CREATED)
def create_translation(translation: TranslationCreate, db: Session = Depends(get_db)):
    """Create new translation for content"""
    # Check if content exists
    content = db.query(Content).filter(Content.id == translation.content_id).first()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content with ID {translation.content_id} not found"
        )
    
    # Check if translation already exists for this language
    existing = db.query(Translation).filter(
        Translation.content_id == translation.content_id,
        Translation.target_language == translation.target_language
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Translation for language {translation.target_language} already exists"
        )
    
    try:
        db_translation = Translation(**translation.model_dump())
        db.add(db_translation)
        db.commit()
        db.refresh(db_translation)
        logger.info(f"Created translation with ID: {db_translation.id}")
        return db_translation
    except Exception as e:
        logger.error(f"Error creating translation: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create translation"
        )


@router.get("/content/{content_id}", response_model=List[TranslationResponse])
def list_translations_by_content(content_id: int, db: Session = Depends(get_db)):
    """List all translations for specific content"""
    # Check if content exists
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content with ID {content_id} not found"
        )
    
    translations = db.query(Translation).filter(
        Translation.content_id == content_id
    ).all()
    
    return translations


@router.get("/{translation_id}", response_model=TranslationResponse)
def get_translation(translation_id: int, db: Session = Depends(get_db)):
    """Get specific translation by ID"""
    translation = db.query(Translation).filter(Translation.id == translation_id).first()
    
    if not translation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Translation with ID {translation_id} not found"
        )
    
    return translation


@router.put("/{translation_id}", response_model=TranslationResponse)
def update_translation(
    translation_id: int,
    translation_update: TranslationUpdate,
    db: Session = Depends(get_db)
):
    """Update existing translation"""
    db_translation = db.query(Translation).filter(Translation.id == translation_id).first()
    
    if not db_translation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Translation with ID {translation_id} not found"
        )
    
    try:
        update_data = translation_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_translation, field, value)
        
        db.commit()
        db.refresh(db_translation)
        logger.info(f"Updated translation with ID: {translation_id}")
        return db_translation
    except Exception as e:
        logger.error(f"Error updating translation: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update translation"
        )


@router.delete("/{translation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_translation(translation_id: int, db: Session = Depends(get_db)):
    """Delete translation by ID"""
    db_translation = db.query(Translation).filter(Translation.id == translation_id).first()
    
    if not db_translation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Translation with ID {translation_id} not found"
        )
    
    try:
        db.delete(db_translation)
        db.commit()
        logger.info(f"Deleted translation with ID: {translation_id}")
    except Exception as e:
        logger.error(f"Error deleting translation: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete translation"
        )
