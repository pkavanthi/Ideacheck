from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from backend.database import get_db
from backend.models import Translation
from backend.schemas import TranslationCreate, TranslationResponse, TranslationUpdate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=TranslationResponse, status_code=status.HTTP_201_CREATED)
async def create_translation(
    translation: TranslationCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new translation entry.
    """
    try:
        # Simulate translation (in production, integrate with translation API)
        translated_text = f"[Translated from {translation.source_language} to {translation.target_language}]: {translation.source_text}"
        
        db_translation = Translation(
            source_text=translation.source_text,
            source_language=translation.source_language,
            target_language=translation.target_language,
            translated_text=translated_text
        )
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


@router.get("/", response_model=List[TranslationResponse])
async def get_translations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve all translations with pagination.
    """
    try:
        translations = db.query(Translation).offset(skip).limit(limit).all()
        return translations
    except Exception as e:
        logger.error(f"Error retrieving translations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve translations"
        )


@router.get("/{translation_id}", response_model=TranslationResponse)
async def get_translation(
    translation_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific translation by ID.
    """
    translation = db.query(Translation).filter(Translation.id == translation_id).first()
    if not translation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Translation with ID {translation_id} not found"
        )
    return translation


@router.put("/{translation_id}", response_model=TranslationResponse)
async def update_translation(
    translation_id: int,
    translation_update: TranslationUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing translation.
    """
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
async def delete_translation(
    translation_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a translation by ID.
    """
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
