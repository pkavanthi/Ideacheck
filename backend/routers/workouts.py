from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from backend.database import get_db
from backend.models import Workout, WorkoutExercise

router = APIRouter()


# Pydantic schemas
class WorkoutExerciseBase(BaseModel):
    exercise_id: int
    sets: int | None = None
    reps: int | None = None
    weight: float | None = None
    duration_seconds: int | None = None
    rest_seconds: int | None = None
    order: int | None = None
    form_score: float | None = None
    notes: str | None = None


class WorkoutExerciseResponse(WorkoutExerciseBase):
    id: int
    workout_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class WorkoutBase(BaseModel):
    title: str
    description: str | None = None
    duration_minutes: int | None = None
    calories_burned: float | None = None
    difficulty_level: str | None = None
    status: str = "planned"
    scheduled_date: datetime | None = None
    notes: str | None = None


class WorkoutCreate(WorkoutBase):
    user_id: int
    exercises: List[WorkoutExerciseBase] = []


class WorkoutUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    duration_minutes: int | None = None
    calories_burned: float | None = None
    difficulty_level: str | None = None
    status: str | None = None
    scheduled_date: datetime | None = None
    completed_date: datetime | None = None
    notes: str | None = None


class WorkoutResponse(WorkoutBase):
    id: int
    user_id: int
    completed_date: datetime | None = None
    created_at: datetime
    updated_at: datetime
    workout_exercises: List[WorkoutExerciseResponse] = []
    
    class Config:
        from_attributes = True


@router.post("/", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    """Create a new workout"""
    # Create workout
    workout_data = workout.model_dump(exclude={'exercises'})
    db_workout = Workout(**workout_data)
    
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    
    # Add exercises to workout
    for exercise in workout.exercises:
        db_workout_exercise = WorkoutExercise(
            workout_id=db_workout.id,
            **exercise.model_dump()
        )
        db.add(db_workout_exercise)
    
    db.commit()
    db.refresh(db_workout)
    
    return db_workout


@router.get("/", response_model=List[WorkoutResponse])
def get_workouts(
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    user_id: int | None = None,
    db: Session = Depends(get_db)
):
    """Get all workouts with optional filtering"""
    query = db.query(Workout)
    
    if status:
        query = query.filter(Workout.status == status)
    
    if user_id:
        query = query.filter(Workout.user_id == user_id)
    
    workouts = query.offset(skip).limit(limit).all()
    return workouts


@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    """Get a specific workout by ID"""
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    return workout


@router.put("/{workout_id}", response_model=WorkoutResponse)
def update_workout(
    workout_id: int,
    workout_update: WorkoutUpdate,
    db: Session = Depends(get_db)
):
    """Update a workout"""
    db_workout = db.query(Workout).filter(Workout.id == workout_id).first()
    
    if not db_workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    # Update fields if provided
    update_data = workout_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_workout, field, value)
    
    db_workout.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_workout)
    
    return db_workout


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    """Delete a workout"""
    db_workout = db.query(Workout).filter(Workout.id == workout_id).first()
    
    if not db_workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    db.delete(db_workout)
    db.commit()
    
    return None


@router.post("/{workout_id}/exercises", response_model=WorkoutExerciseResponse, status_code=status.HTTP_201_CREATED)
def add_exercise_to_workout(
    workout_id: int,
    exercise: WorkoutExerciseBase,
    db: Session = Depends(get_db)
):
    """Add an exercise to a workout"""
    # Check if workout exists
    db_workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not db_workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    # Create workout exercise
    db_workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        **exercise.model_dump()
    )
    
    db.add(db_workout_exercise)
    db.commit()
    db.refresh(db_workout_exercise)
    
    return db_workout_exercise
