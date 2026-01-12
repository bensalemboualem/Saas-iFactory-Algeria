"""
Progress service for lesson progress tracking.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from fastapi import HTTPException, status

from app.models.enrollment import Enrollment, Progress
from app.models.content import Lesson
from app.schemas.enrollment import ProgressCreate, ProgressUpdate


class ProgressService:
    """Progress tracking service."""
    
    @staticmethod
    def track_lesson_progress(
        db: Session,
        enrollment_id: str,
        lesson_id: str,
        progress_data: ProgressCreate
    ) -> Progress:
        """
        Track or update lesson progress.
        
        Args:
            db: Database session
            enrollment_id: Enrollment ID
            lesson_id: Lesson ID
            progress_data: Progress data
            
        Returns:
            Progress: Progress record
        """
        # Check if progress already exists
        progress = db.query(Progress).filter(
            Progress.enrollment_id == enrollment_id,
            Progress.lesson_id == lesson_id
        ).first()
        
        if progress:
            # Update existing progress
            progress.time_spent = progress_data.time_spent
            progress.last_position = progress_data.last_position
            progress.notes = progress_data.notes
            progress.updated_at = datetime.utcnow()
        else:
            # Create new progress
            progress = Progress(
                enrollment_id=enrollment_id,
                lesson_id=lesson_id,
                time_spent=progress_data.time_spent,
                last_position=progress_data.last_position,
                notes=progress_data.notes,
                is_completed=False,
            )
            db.add(progress)
        
        db.commit()
        db.refresh(progress)
        
        return progress
    
    @staticmethod
    def update_lesson_progress(
        db: Session,
        progress: Progress,
        progress_data: ProgressUpdate
    ) -> Progress:
        """
        Update lesson progress.
        
        Args:
            db: Database session
            progress: Progress object
            progress_data: Progress update data
            
        Returns:
            Progress: Updated progress
        """
        update_data = progress_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(progress, field, value)
        
        progress.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(progress)
        
        return progress
    
    @staticmethod
    def complete_lesson(db: Session, progress: Progress) -> Progress:
        """
        Mark lesson as completed.
        
        Args:
            db: Database session
            progress: Progress object
            
        Returns:
            Progress: Updated progress with completion
        """
        if not progress.is_completed:
            progress.is_completed = True
            progress.completed_at = datetime.utcnow()
            progress.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(progress)
            
            # Update enrollment progress
            from app.services.enrollment_service import EnrollmentService
            enrollment = db.query(Enrollment).filter(
                Enrollment.id == progress.enrollment_id
            ).first()
            
            if enrollment:
                EnrollmentService.update_enrollment_progress(db, enrollment)
        
        return progress
    
    @staticmethod
    def get_progress_by_id(db: Session, progress_id: str) -> Progress:
        """
        Get progress by ID.
        
        Args:
            db: Database session
            progress_id: Progress ID
            
        Returns:
            Progress: Progress object
            
        Raises:
            HTTPException: If progress not found
        """
        progress = db.query(Progress).filter(Progress.id == progress_id).first()
        
        if not progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Progress record not found"
            )
        
        return progress
    
    @staticmethod
    def get_lesson_progress(
        db: Session,
        enrollment_id: str,
        lesson_id: str
    ) -> Optional[Progress]:
        """
        Get progress for a specific lesson.
        
        Args:
            db: Database session
            enrollment_id: Enrollment ID
            lesson_id: Lesson ID
            
        Returns:
            Optional[Progress]: Progress object or None
        """
        return db.query(Progress).filter(
            Progress.enrollment_id == enrollment_id,
            Progress.lesson_id == lesson_id
        ).first()
    
    @staticmethod
    def get_enrollment_progress(
        db: Session,
        enrollment_id: str,
        include_lesson: bool = False
    ) -> List[Progress]:
        """
        Get all progress records for an enrollment.
        
        Args:
            db: Database session
            enrollment_id: Enrollment ID
            include_lesson: Whether to include lesson data
            
        Returns:
            List[Progress]: List of progress records
        """
        query = db.query(Progress).filter(Progress.enrollment_id == enrollment_id)
        
        if include_lesson:
            query = query.options(joinedload(Progress.lesson))
        
        return query.order_by(Progress.updated_at.desc()).all()
    
    @staticmethod
    def get_course_progress_summary(db: Session, enrollment_id: str) -> dict:
        """
        Get progress summary for a course enrollment.
        
        Args:
            db: Database session
            enrollment_id: Enrollment ID
            
        Returns:
            dict: Progress summary with stats
        """
        enrollment = db.query(Enrollment).filter(
            Enrollment.id == enrollment_id
        ).first()
        
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )
        
        # Get total lessons in course
        from app.models.content import Module, Lesson
        
        total_lessons = db.query(func.count(Lesson.id)).join(
            Module, Lesson.module_id == Module.id
        ).filter(Module.course_id == enrollment.course_id).scalar()
        
        # Get completed lessons
        completed_lessons = db.query(func.count(Progress.id)).filter(
            Progress.enrollment_id == enrollment_id,
            Progress.is_completed == True
        ).scalar()
        
        # Get in-progress lessons
        in_progress_lessons = db.query(func.count(Progress.id)).filter(
            Progress.enrollment_id == enrollment_id,
            Progress.is_completed == False
        ).scalar()
        
        # Get total time spent
        total_time = db.query(func.sum(Progress.time_spent)).filter(
            Progress.enrollment_id == enrollment_id
        ).scalar() or 0
        
        # Get recent progress (last 5 lessons)
        recent_progress = db.query(Progress).options(
            joinedload(Progress.lesson)
        ).filter(
            Progress.enrollment_id == enrollment_id
        ).order_by(Progress.updated_at.desc()).limit(5).all()
        
        return {
            "enrollment_id": enrollment_id,
            "course_id": enrollment.course_id,
            "progress_percentage": enrollment.progress,
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "in_progress_lessons": in_progress_lessons,
            "remaining_lessons": total_lessons - completed_lessons,
            "total_time_spent": int(total_time),
            "status": enrollment.status.value,
            "enrolled_at": enrollment.enrolled_at,
            "completed_at": enrollment.completed_at,
            "recent_progress": recent_progress
        }
    
    @staticmethod
    def get_module_progress(db: Session, enrollment_id: str, module_id: str) -> dict:
        """
        Get progress for a specific module.
        
        Args:
            db: Database session
            enrollment_id: Enrollment ID
            module_id: Module ID
            
        Returns:
            dict: Module progress summary
        """
        # Get total lessons in module
        from app.models.content import Lesson
        
        total_lessons = db.query(func.count(Lesson.id)).filter(
            Lesson.module_id == module_id
        ).scalar()
        
        # Get completed lessons in module
        completed_lessons = db.query(func.count(Progress.id)).join(
            Lesson, Progress.lesson_id == Lesson.id
        ).filter(
            Progress.enrollment_id == enrollment_id,
            Lesson.module_id == module_id,
            Progress.is_completed == True
        ).scalar()
        
        # Calculate module progress
        progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        
        return {
            "module_id": module_id,
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "progress_percentage": progress_percentage,
            "is_completed": progress_percentage >= 100
        }
    
    @staticmethod
    def delete_progress(db: Session, progress: Progress) -> None:
        """
        Delete progress record.
        
        Args:
            db: Database session
            progress: Progress object
        """
        enrollment_id = progress.enrollment_id
        
        db.delete(progress)
        db.commit()
        
        # Update enrollment progress
        from app.services.enrollment_service import EnrollmentService
        enrollment = db.query(Enrollment).filter(
            Enrollment.id == enrollment_id
        ).first()
        
        if enrollment:
            EnrollmentService.update_enrollment_progress(db, enrollment)
    
    @staticmethod
    def reset_lesson_progress(db: Session, progress: Progress) -> Progress:
        """
        Reset lesson progress (mark as incomplete).
        
        Args:
            db: Database session
            progress: Progress object
            
        Returns:
            Progress: Reset progress
        """
        progress.is_completed = False
        progress.completed_at = None
        progress.time_spent = 0
        progress.last_position = 0
        progress.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(progress)
        
        # Update enrollment progress
        from app.services.enrollment_service import EnrollmentService
        enrollment = db.query(Enrollment).filter(
            Enrollment.id == progress.enrollment_id
        ).first()
        
        if enrollment:
            EnrollmentService.update_enrollment_progress(db, enrollment)
        
        return progress
