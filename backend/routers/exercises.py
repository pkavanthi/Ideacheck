from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from backend.database import get_db
from backend.models import Exercise, FormAssessment
from backend.schemas import (
    ExerciseCreate, ExerciseResponse, ExerciseUpdate,
    FormAssessmentCreate, FormAssessmentResponse, FormAssessmentUpdate
)

logger = logging.getLogger(__name__)

router = APIRouter()


# Exercise endpoints
@router.post("/", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
def create_exercise(exercise: ExerciseCreate, user_id: int, db: Session = Depends(get_db)):
    """Create a new exercise"""
    db_exercise = Exercise(
        user_id=user_id,
        name=exercise.name,
        description=exercise.description,
        category=exercise.category,
        difficulty_level=exercise.difficulty_level,
        target_muscles=exercise.target_muscles,
        equipment_needed=exercise.equipment_needed
    )
    
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    
    logger.info(f"Exercise created: {db_exercise.name} for user {user_id}")
    return db_exercise


@router.get("/", response_model=List[ExerciseResponse])
def get_exercises(
    skip: int = 0,
    limit: int = 100,
    user_id: int = None,
    category: str = None,
    db: Session = Depends(get_db)
):
    """Get all exercises with optional filters"""
    query = db.query(Exercise)
    
    if user_id:
        query = query.filter(Exercise.user_id == user_id)
    
    if category:
        query = query.filter(Exercise.category == category)
    
    exercises = query.offset(skip).limit(limit).all()
    return exercises


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """Get a specific exercise by ID"""
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    
    return exercise


@router.put("/{exercise_id}", response_model=ExerciseResponse)
def update_exercise(
    exercise_id: int,
    exercise_update: ExerciseUpdate,
    db: Session = Depends(get_db)
):
    """Update an exercise"""
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    
    # Update fields
    update_data = exercise_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(exercise, field, value)
    
    db.commit()
    db.refresh(exercise)
    
    logger.info(f"Exercise updated: {exercise.name}")
    return exercise


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """Delete an exercise"""
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    
    db.delete(exercise)
    db.commit()
    
    logger.info(f"Exercise deleted: {exercise.name}")
    return None


# Form Assessment endpoints
@router.post("/{exercise_id}/assessments", response_model=FormAssessmentResponse, status_code=status.HTTP_201_CREATED)
def create_form_assessment(
    exercise_id: int,
    assessment: FormAssessmentCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create a new form assessment for an exercise"""
    # Verify exercise exists
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    
    db_assessment = FormAssessment(
        user_id=user_id,
        exercise_id=exercise_id,
        form_score=assessment.form_score,
        feedback=assessment.feedback,
        key_points=assessment.key_points,
        video_url=assessment.video_url,
        notes=assessment.notes
    )
    
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    
    logger.info(f"Form assessment created for exercise {exercise_id}")
    return db_assessment


@router.get("/{exercise_id}/assessments", response_model=List[FormAssessmentResponse])
def get_exercise_assessments(
    exercise_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all form assessments for a specific exercise"""
    assessments = db.query(FormAssessment).filter(
        FormAssessment.exercise_id == exercise_id
    ).offset(skip).limit(limit).all()
    
    return assessments


@router.get("/assessments/{assessment_id}", response_model=FormAssessmentResponse)
def get_form_assessment(assessment_id: int, db: Session = Depends(get_db)):
    """Get a specific form assessment by ID"""
    assessment = db.query(FormAssessment).filter(FormAssessment.id == assessment_id).first()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form assessment not found"
        )
    
    return assessment


@router.put("/assessments/{assessment_id}", response_model=FormAssessmentResponse)
def update_form_assessment(
    assessment_id: int,
    assessment_update: FormAssessmentUpdate,
    db: Session = Depends(get_db)
):
    """Update a form assessment"""
    assessment = db.query(FormAssessment).filter(FormAssessment.id == assessment_id).first()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form assessment not found"
        )
    
    # Update fields
    update_data = assessment_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(assessment, field, value)
    
    db.commit()
    db.refresh(assessment)
    
    logger.info(f"Form assessment updated: {assessment_id}")
    return assessment


@router.delete("/assessments/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_form_assessment(assessment_id: int, db: Session = Depends(get_db)):
    """Delete a form assessment"""
    assessment = db.query(FormAssessment).filter(FormAssessment.id == assessment_id).first()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form assessment not found"
        )
    
    db.delete(assessment)
    db.commit()
    
    logger.info(f"Form assessment deleted: {assessment_id}")
    return None
