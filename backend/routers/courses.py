from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from backend.database import get_db
from backend.models import Course, Enrollment, CourseContent
from backend.schemas import (
    CourseCreate, CourseUpdate, CourseResponse,
    EnrollmentCreate, EnrollmentResponse,
    CourseContentCreate, CourseContentUpdate, CourseContentResponse
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    """Create a new course"""
    try:
        db_course = Course(**course.model_dump())
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        
        logger.info(f"Created course: {db_course.id}")
        return db_course
    except Exception as e:
        logger.error(f"Error creating course: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create course"
        )


@router.get("/", response_model=List[CourseResponse])
def get_courses(skip: int = 0, limit: int = 100, active_only: bool = True, db: Session = Depends(get_db)):
    """Get all courses"""
    try:
        query = db.query(Course)
        if active_only:
            query = query.filter(Course.is_active == True)
        courses = query.offset(skip).limit(limit).all()
        return courses
    except Exception as e:
        logger.error(f"Error fetching courses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch courses"
        )


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Get a specific course by ID"""
    try:
        course = db.query(Course).filter(Course.id == course_id).first()
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


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course_update: CourseUpdate, db: Session = Depends(get_db)):
    """Update a course"""
    try:
        db_course = db.query(Course).filter(Course.id == course_id).first()
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
        
        logger.info(f"Updated course: {course_id}")
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
        db_course = db.query(Course).filter(Course.id == course_id).first()
        if not db_course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        db.delete(db_course)
        db.commit()
        
        logger.info(f"Deleted course: {course_id}")
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


@router.post("/{course_id}/enroll", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_student(course_id: int, enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    """Enroll a student in a course"""
    try:
        # Verify course exists
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Check if already enrolled
        existing = db.query(Enrollment).filter(
            Enrollment.student_id == enrollment.student_id,
            Enrollment.course_id == course_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student already enrolled in this course"
            )
        
        db_enrollment = Enrollment(student_id=enrollment.student_id, course_id=course_id)
        db.add(db_enrollment)
        db.commit()
        db.refresh(db_enrollment)
        
        logger.info(f"Enrolled student {enrollment.student_id} in course {course_id}")
        return db_enrollment
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enrolling student: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to enroll student"
        )


@router.post("/{course_id}/content", response_model=CourseContentResponse, status_code=status.HTTP_201_CREATED)
def create_course_content(course_id: int, content: CourseContentCreate, db: Session = Depends(get_db)):
    """Create course content"""
    try:
        # Verify course exists
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        content_data = content.model_dump()
        content_data['course_id'] = course_id
        db_content = CourseContent(**content_data)
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        
        logger.info(f"Created content for course {course_id}")
        return db_content
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating course content: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create course content"
        )


@router.get("/{course_id}/content", response_model=List[CourseContentResponse])
def get_course_content(course_id: int, db: Session = Depends(get_db)):
    """Get all content for a course"""
    try:
        content = db.query(CourseContent).filter(
            CourseContent.course_id == course_id
        ).order_by(CourseContent.order).all()
        return content
    except Exception as e:
        logger.error(f"Error fetching course content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch course content"
        )
