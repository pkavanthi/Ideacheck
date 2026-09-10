from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from backend.database import get_db
from backend.models import Exercise

router = APIRouter()


# Pydantic schemas
class ExerciseBase(BaseModel):
    name: str
    description: str | None = None
    category: str | None = None
    difficulty_level: str | None = None
    target_muscles: str | None = None
    equipment_needed: str | None = None
    form_tips: str | None = None


class ExerciseCreate(ExerciseBase):
    user_id: int


class ExerciseUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    difficulty_level: str | None = None
    target_muscles: str | None = None
    equipment_needed: str | None = None
    form_tips: str | None = None


class ExerciseResponse(ExerciseBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


@router.post("/", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    """Create a new exercise"""
    db_exercise = Exercise(**exercise.model_dump())
    
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    
    return db_exercise


@router.get("/", response_model=List[ExerciseResponse])
def get_exercises(
    skip: int = 0,
    limit: int = 100,
    category: str | None = None,
    difficulty_level: str | None = None,
    db: Session = Depends(get_db)
):
    """Get all exercises with optional filtering"""
    query = db.query(Exercise)
    
    if category:
        query = query.filter(Exercise.category == category)
    
    if difficulty_level:
        query = query.filter(Exercise.difficulty_level == difficulty_level)
    
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
    db_exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    
    if not db_exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    
    # Update fields if provided
    update_data = exercise_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_exercise, field, value)
    
    db_exercise.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_exercise)
    
    return db_exercise


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """Delete an exercise"""
    db_exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    
    if not db_exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    
    db.delete(db_exercise)
    db.commit()
    
    return None
