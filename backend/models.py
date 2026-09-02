from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    language = Column(String(10), nullable=False)
    instructor_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    translations = relationship("CourseTranslation", back_populates="course", cascade="all, delete-orphan")
    materials = relationship("CourseMaterial", back_populates="course", cascade="all, delete-orphan")


class CourseTranslation(Base):
    __tablename__ = "course_translations"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    target_language = Column(String(10), nullable=False, index=True)
    translated_title = Column(String(255))
    translated_description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="translations")


class CourseMaterial(Base):
    __tablename__ = "course_materials"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    material_type = Column(String(50))  # lecture, assignment, reading, etc.
    language = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="materials")
    translations = relationship("MaterialTranslation", back_populates="material", cascade="all, delete-orphan")


class MaterialTranslation(Base):
    __tablename__ = "material_translations"
    
    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("course_materials.id"), nullable=False)
    target_language = Column(String(10), nullable=False, index=True)
    translated_title = Column(String(255))
    translated_content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    material = relationship("CourseMaterial", back_populates="translations")
