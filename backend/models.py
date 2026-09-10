from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class User(Base):
    """User model for authentication and profile management"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    exercises = relationship("Exercise", back_populates="user", cascade="all, delete-orphan")
    form_assessments = relationship("FormAssessment", back_populates="user", cascade="all, delete-orphan")


class Exercise(Base):
    """Exercise model for tracking different exercise types"""
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))  # e.g., strength, cardio, flexibility
    difficulty_level = Column(String(50))  # beginner, intermediate, advanced
    target_muscles = Column(Text)  # JSON string of muscle groups
    equipment_needed = Column(Text)  # JSON string of equipment
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="exercises")
    form_assessments = relationship("FormAssessment", back_populates="exercise", cascade="all, delete-orphan")


class FormAssessment(Base):
    """Form assessment model for tracking exercise form quality"""
    __tablename__ = "form_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    assessment_date = Column(DateTime, default=datetime.utcnow)
    form_score = Column(Float)  # 0-100 score
    feedback = Column(Text)  # Detailed feedback on form
    key_points = Column(Text)  # JSON string of key improvement points
    video_url = Column(String(500))  # Optional video reference
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="form_assessments")
    exercise = relationship("Exercise", back_populates="form_assessments")
