from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from backend.database import get_db
from backend import models, schemas

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=schemas.Course, status_code=status.HTTP_201_CREATED)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    """Create a new course"""
    try:
        db_course = models.Course(**course.model_dump())
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        logger.info(f"Created course with ID: {db_course.id}")
        return db_course
    except Exception as e:
        logger.error(f"Error creating course: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create course"
        )


@router.get("/", response_model=List[schemas.Course])
def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all courses with pagination"""
    try:
        courses = db.query(models.Course).offset(skip).limit(limit).all()
        return courses
    except Exception as e:
        logger.error(f"Error fetching courses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch courses"
        )


@router.get("/{course_id}", response_model=schemas.Course)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Get a specific course by ID"""
    try:
        course = db.query(models.Course).filter(models.Course.id == course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        return course
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching course {course_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch course"
        )


@router.put("/{course_id}", response_model=schemas.Course)
def update_course(
    course_id: int,
    course_update: schemas.CourseUpdate,
    db: Session = Depends(get_db)
):
    """Update a course"""
    try:
        db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
        if not db_course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        update_data = course_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_course, field, value)
        
        db.commit()
        db.refresh(db_course)
        logger.info(f"Updated course with ID: {course_id}")
        return db_course
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating course {course_id}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update course"
        )


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    """Delete a course"""
    try:
        db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
        if not db_course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        db.delete(db_course)
        db.commit()
        logger.info(f"Deleted course with ID: {course_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting course {course_id}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete course"
        )
