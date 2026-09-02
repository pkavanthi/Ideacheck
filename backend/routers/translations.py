from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from backend.database import get_db
from backend.models import Course, CourseTranslation, CourseMaterial, MaterialTranslation

router = APIRouter()


# Pydantic schemas
class TranslationBase(BaseModel):
    target_language: str
    translated_title: str | None = None
    translated_description: str | None = None


class CourseTranslationCreate(TranslationBase):
    pass


class CourseTranslationResponse(TranslationBase):
    id: int
    course_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MaterialTranslationBase(BaseModel):
    target_language: str
    translated_title: str | None = None
    translated_content: str | None = None


class MaterialTranslationCreate(MaterialTranslationBase):
    pass


class MaterialTranslationResponse(MaterialTranslationBase):
    id: int
    material_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Course translation endpoints
@router.post("/courses/{course_id}", response_model=CourseTranslationResponse, status_code=status.HTTP_201_CREATED)
async def create_course_translation(
    course_id: int,
    translation: CourseTranslationCreate,
    db: Session = Depends(get_db)
):
    """Create a translation for a course"""
    # Check if course exists
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    
    # Check if translation already exists for this language
    existing = db.query(CourseTranslation).filter(
        CourseTranslation.course_id == course_id,
        CourseTranslation.target_language == translation.target_language
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Translation for language {translation.target_language} already exists"
        )
    
    db_translation = CourseTranslation(course_id=course_id, **translation.model_dump())
    db.add(db_translation)
    db.commit()
    db.refresh(db_translation)
    return db_translation


@router.get("/courses/{course_id}", response_model=List[CourseTranslationResponse])
async def list_course_translations(course_id: int, db: Session = Depends(get_db)):
    """List all translations for a course"""
    # Check if course exists
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    
    translations = db.query(CourseTranslation).filter(
        CourseTranslation.course_id == course_id
    ).all()
    return translations


@router.get("/courses/{course_id}/{language}", response_model=CourseTranslationResponse)
async def get_course_translation(
    course_id: int,
    language: str,
    db: Session = Depends(get_db)
):
    """Get a specific course translation by language"""
    translation = db.query(CourseTranslation).filter(
        CourseTranslation.course_id == course_id,
        CourseTranslation.target_language == language
    ).first()
    
    if not translation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Translation for course {course_id} in language {language} not found"
        )
    
    return translation


@router.delete("/courses/{course_id}/{language}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course_translation(
    course_id: int,
    language: str,
    db: Session = Depends(get_db)
):
    """Delete a course translation"""
    translation = db.query(CourseTranslation).filter(
        CourseTranslation.course_id == course_id,
        CourseTranslation.target_language == language
    ).first()
    
    if not translation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Translation for course {course_id} in language {language} not found"
        )
    
    db.delete(translation)
    db.commit()
    return None


# Material translation endpoints
@router.post("/materials/{material_id}", response_model=MaterialTranslationResponse, status_code=status.HTTP_201_CREATED)
async def create_material_translation(
    material_id: int,
    translation: MaterialTranslationCreate,
    db: Session = Depends(get_db)
):
    """Create a translation for a course material"""
    # Check if material exists
    material = db.query(CourseMaterial).filter(CourseMaterial.id == material_id).first()
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Material with id {material_id} not found"
        )
    
    # Check if translation already exists for this language
    existing = db.query(MaterialTranslation).filter(
        MaterialTranslation.material_id == material_id,
        MaterialTranslation.target_language == translation.target_language
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Translation for language {translation.target_language} already exists"
        )
    
    db_translation = MaterialTranslation(material_id=material_id, **translation.model_dump())
    db.add(db_translation)
    db.commit()
    db.refresh(db_translation)
    return db_translation


@router.get("/materials/{material_id}", response_model=List[MaterialTranslationResponse])
async def list_material_translations(material_id: int, db: Session = Depends(get_db)):
    """List all translations for a material"""
    # Check if material exists
    material = db.query(CourseMaterial).filter(CourseMaterial.id == material_id).first()
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Material with id {material_id} not found"
        )
    
    translations = db.query(MaterialTranslation).filter(
        MaterialTranslation.material_id == material_id
    ).all()
    return translations
