from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    age = Column(Integer)
    fitness_level = Column(String)  # beginner, intermediate, advanced
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workouts = relationship("Workout", back_populates="user", cascade="all, delete-orphan")


class Exercise(Base):
    """Exercise model"""
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    category = Column(String)  # strength, cardio, flexibility, balance
    difficulty = Column(String)  # beginner, intermediate, advanced
    muscle_groups = Column(String)  # JSON string of muscle groups
    equipment_needed = Column(String)  # JSON string of equipment
    instructions = Column(Text)
    video_url = Column(String)
    duration_seconds = Column(Integer)
    calories_per_minute = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workout_exercises = relationship("WorkoutExercise", back_populates="exercise")


class Workout(Base):
    """Workout model"""
    __tablename__ = "workouts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    workout_type = Column(String)  # strength, cardio, mixed, flexibility
    duration_minutes = Column(Integer)
    difficulty = Column(String)
    calories_burned = Column(Float)
    completed = Column(Boolean, default=False)
    scheduled_date = Column(DateTime)
    completed_date = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="workouts")
    workout_exercises = relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")


class WorkoutExercise(Base):
    """Workout-Exercise association model"""
    __tablename__ = "workout_exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    sets = Column(Integer)
    reps = Column(Integer)
    duration_seconds = Column(Integer)
    rest_seconds = Column(Integer)
    order = Column(Integer)  # Order in the workout
    notes = Column(Text)
    completed = Column(Boolean, default=False)
    
    # Relationships
    workout = relationship("Workout", back_populates="workout_exercises")
    exercise = relationship("Exercise", back_populates="workout_exercises")
