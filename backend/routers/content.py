from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from backend.database import get_db
from backend.models import Content
from backend.schemas import ContentCreate, ContentUpdate, ContentResponse, ContentWithTranslations

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
def create_content(content: ContentCreate, db: Session = Depends(get_db)):
    """Create new educational content"""
    try:
        db_content = Content(**content.model_dump())
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        logger.info(f"Created content with ID: {db_content.id}")
        return db_content
    except Exception as e:
        logger.error(f"Error creating content: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create content"
        )


@router.get("/", response_model=List[ContentResponse])
def list_contents(
    skip: int = 0,
    limit: int = 100,
    content_type: str = None,
    db: Session = Depends(get_db)
):
    """List all educational contents with optional filtering"""
    try:
        query = db.query(Content)
        
        if content_type:
            query = query.filter(Content.content_type == content_type)
        
        contents = query.offset(skip).limit(limit).all()
        return contents
    except Exception as e:
        logger.error(f"Error listing contents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve contents"
        )


@router.get("/{content_id}", response_model=ContentWithTranslations)
def get_content(content_id: int, db: Session = Depends(get_db)):
    """Get specific content by ID with translations"""
    content = db.query(Content).filter(Content.id == content_id).first()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content with ID {content_id} not found"
        )
    
    return content


@router.put("/{content_id}", response_model=ContentResponse)
def update_content(
    content_id: int,
    content_update: ContentUpdate,
    db: Session = Depends(get_db)
):
    """Update existing content"""
    db_content = db.query(Content).filter(Content.id == content_id).first()
    
    if not db_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content with ID {content_id} not found"
        )
    
    try:
        update_data = content_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_content, field, value)
        
        db.commit()
        db.refresh(db_content)
        logger.info(f"Updated content with ID: {content_id}")
        return db_content
    except Exception as e:
        logger.error(f"Error updating content: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update content"
        )


@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_content(content_id: int, db: Session = Depends(get_db)):
    """Delete content by ID"""
    db_content = db.query(Content).filter(Content.id == content_id).first()
    
    if not db_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content with ID {content_id} not found"
        )
    
    try:
        db.delete(db_content)
        db.commit()
        logger.info(f"Deleted content with ID: {content_id}")
    except Exception as e:
        logger.error(f"Error deleting content: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete content"
        )
