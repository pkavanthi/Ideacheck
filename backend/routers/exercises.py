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
    difficulty: str | None = None
    muscle_groups: str | None = None
    equipment_needed: str | None = None
    instructions: str | None = None
    video_url: str | None = None
    duration_seconds: int | None = None
    calories_per_minute: float | None = None


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    difficulty: str | None = None
    muscle_groups: str | None = None
    equipment_needed: str | None = None
    instructions: str | None = None
    video_url: str | None = None
    duration_seconds: int | None = None
    calories_per_minute: float | None = None


class ExerciseResponse(ExerciseBase):
    id: int
    is_active: bool
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
    difficulty: str | None = None,
    db: Session = Depends(get_db)
):
    """Get all exercises with optional filters"""
    query = db.query(Exercise).filter(Exercise.is_active == True)
    
    if category:
        query = query.filter(Exercise.category == category)
    
    if difficulty:
        query = query.filter(Exercise.difficulty == difficulty)
    
    exercises = query.offset(skip).limit(limit).all()
    return exercises


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """Get an exercise by ID"""
    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.is_active == True
    ).first()
    
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
    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.is_active == True
    ).first()
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    
    # Update fields
    update_data = exercise_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(exercise, field, value)
    
    exercise.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(exercise)
    
    return exercise


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """Delete an exercise (soft delete)"""
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    
    # Soft delete
    exercise.is_active = False
    exercise.updated_at = datetime.utcnow()
    db.commit()
    
    return None
