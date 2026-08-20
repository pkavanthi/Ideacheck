from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from backend.database import get_db
from backend.models import Workout, WorkoutExercise, User, Exercise

router = APIRouter()


# Pydantic schemas
class WorkoutExerciseBase(BaseModel):
    exercise_id: int
    sets: int | None = None
    reps: int | None = None
    duration_seconds: int | None = None
    rest_seconds: int | None = None
    order: int
    notes: str | None = None


class WorkoutExerciseCreate(WorkoutExerciseBase):
    pass


class WorkoutExerciseResponse(WorkoutExerciseBase):
    id: int
    workout_id: int
    completed: bool
    
    class Config:
        from_attributes = True


class WorkoutBase(BaseModel):
    name: str
    description: str | None = None
    workout_type: str | None = None
    duration_minutes: int | None = None
    difficulty: str | None = None
    scheduled_date: datetime | None = None
    notes: str | None = None


class WorkoutCreate(WorkoutBase):
    user_id: int
    exercises: List[WorkoutExerciseCreate] = []


class WorkoutUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    workout_type: str | None = None
    duration_minutes: int | None = None
    difficulty: str | None = None
    scheduled_date: datetime | None = None
    completed: bool | None = None
    notes: str | None = None


class WorkoutResponse(WorkoutBase):
    id: int
    user_id: int
    calories_burned: float | None = None
    completed: bool
    completed_date: datetime | None = None
    created_at: datetime
    updated_at: datetime
    exercises: List[WorkoutExerciseResponse] = []
    
    class Config:
        from_attributes = True


@router.post("/", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    """Create a new workout"""
    # Verify user exists
    user = db.query(User).filter(User.id == workout.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create workout
    workout_data = workout.model_dump(exclude={'exercises'})
    db_workout = Workout(**workout_data)
    
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    
    # Add exercises to workout
    for exercise_data in workout.exercises:
        # Verify exercise exists
        exercise = db.query(Exercise).filter(Exercise.id == exercise_data.exercise_id).first()
        if not exercise:
            continue
        
        workout_exercise = WorkoutExercise(
            workout_id=db_workout.id,
            **exercise_data.model_dump()
        )
        db.add(workout_exercise)
    
    db.commit()
    db.refresh(db_workout)
    
    return db_workout


@router.get("/", response_model=List[WorkoutResponse])
def get_workouts(
    skip: int = 0,
    limit: int = 100,
    user_id: int | None = None,
    completed: bool | None = None,
    db: Session = Depends(get_db)
):
    """Get all workouts with optional filters"""
    query = db.query(Workout)
    
    if user_id:
        query = query.filter(Workout.user_id == user_id)
    
    if completed is not None:
        query = query.filter(Workout.completed == completed)
    
    workouts = query.offset(skip).limit(limit).all()
    return workouts


@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    """Get a workout by ID"""
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
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    # Update fields
    update_data = workout_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(workout, field, value)
    
    # Set completed date if marking as completed
    if workout_update.completed and not workout.completed:
        workout.completed_date = datetime.utcnow()
    
    workout.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(workout)
    
    return workout


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    """Delete a workout"""
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    db.delete(workout)
    db.commit()
    
    return None
