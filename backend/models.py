from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base


class User(Base):
    """User model for authentication and profile management"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workouts = relationship("Workout", back_populates="user", cascade="all, delete-orphan")
    exercises = relationship("Exercise", back_populates="user", cascade="all, delete-orphan")


class Exercise(Base):
    """Exercise model for tracking individual exercises"""
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    category = Column(String, index=True)  # e.g., "strength", "cardio", "flexibility"
    difficulty_level = Column(String)  # e.g., "beginner", "intermediate", "advanced"
    target_muscles = Column(String)  # Comma-separated muscle groups
    equipment_needed = Column(String)  # Comma-separated equipment
    form_tips = Column(Text)  # Tips for proper form
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="exercises")
    workout_exercises = relationship("WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan")


class Workout(Base):
    """Workout model for tracking workout sessions"""
    __tablename__ = "workouts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    duration_minutes = Column(Integer)  # Total workout duration
    calories_burned = Column(Float)
    difficulty_level = Column(String)
    status = Column(String, default="planned")  # planned, in_progress, completed
    scheduled_date = Column(DateTime)
    completed_date = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="workouts")
    workout_exercises = relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")


class WorkoutExercise(Base):
    """Junction table for workout-exercise relationship with additional data"""
    __tablename__ = "workout_exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)  # Weight in kg or lbs
    duration_seconds = Column(Integer)  # For timed exercises
    rest_seconds = Column(Integer)  # Rest between sets
    order = Column(Integer)  # Order in the workout
    form_score = Column(Float)  # AI-assessed form quality (0-100)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workout = relationship("Workout", back_populates="workout_exercises")
    exercise = relationship("Exercise", back_populates="workout_exercises")
