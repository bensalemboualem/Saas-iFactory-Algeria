"""
Enrollment service for course enrollment management.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from fastapi import HTTPException, status

from app.models.enrollment import Enrollment, EnrollmentStatus
from app.models.course import Course
from app.models.user import User, UserRole
from app.schemas.enrollment import EnrollmentCreate


class EnrollmentService:
    """Enrollment management service."""
    
    @staticmethod
    def enroll_user(db: Session, user_id: str, course_id: str) -> Enrollment:
        """
        Enroll user in a course.
        
        Args:
            db: Database session
            user_id: User ID
            course_id: Course ID
            
        Returns:
            Enrollment: Created enrollment
            
        Raises:
            HTTPException: If course not found, not published, or already enrolled
        """
        # Check if course exists and is published
        course = db.query(Course).filter(Course.id == course_id).first()
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        if not course.is_published:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot enroll in unpublished course"
            )
        
        # Check if already enrolled
        existing_enrollment = db.query(Enrollment).filter(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id
        ).first()
        
        if existing_enrollment:
            if existing_enrollment.status == EnrollmentStatus.ACTIVE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Already enrolled in this course"
                )
            else:
                # Reactivate enrollment
                existing_enrollment.status = EnrollmentStatus.ACTIVE
                existing_enrollment.enrolled_at = datetime.utcnow()
                db.commit()
                db.refresh(existing_enrollment)
                return existing_enrollment
        
        # Create new enrollment
        enrollment = Enrollment(
            user_id=user_id,
            course_id=course_id,
            status=EnrollmentStatus.ACTIVE,
            progress=0.0,
            enrolled_at=datetime.utcnow(),
        )
        
        db.add(enrollment)
        
        # Update course enrollment count
        course.total_enrollments = db.query(func.count(Enrollment.id)).filter(
            Enrollment.course_id == course_id,
            Enrollment.status == EnrollmentStatus.ACTIVE
        ).scalar() + 1
        
        db.commit()
        db.refresh(enrollment)
        
        return enrollment
    
    @staticmethod
    def get_enrollment_by_id(
        db: Session,
        enrollment_id: str,
        include_course: bool = False,
        include_user: bool = False
    ) -> Enrollment:
        """
        Get enrollment by ID.
        
        Args:
            db: Database session
            enrollment_id: Enrollment ID
            include_course: Whether to include course data
            include_user: Whether to include user data
            
        Returns:
            Enrollment: Enrollment object
            
        Raises:
            HTTPException: If enrollment not found
        """
        query = db.query(Enrollment)
        
        if include_course:
            query = query.options(joinedload(Enrollment.course))
        
        if include_user:
            query = query.options(joinedload(Enrollment.user))
        
        enrollment = query.filter(Enrollment.id == enrollment_id).first()
        
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )
        
        return enrollment
    
    @staticmethod
    def get_user_enrollment(
        db: Session,
        user_id: str,
        course_id: str
    ) -> Optional[Enrollment]:
        """
        Get user's enrollment in a course.
        
        Args:
            db: Database session
            user_id: User ID
            course_id: Course ID
            
        Returns:
            Optional[Enrollment]: Enrollment object or None
        """
        return db.query(Enrollment).filter(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id
        ).first()
    
    @staticmethod
    def check_user_enrolled(db: Session, user_id: str, course_id: str) -> bool:
        """
        Check if user is enrolled in a course.
        
        Args:
            db: Database session
            user_id: User ID
            course_id: Course ID
            
        Returns:
            bool: True if enrolled and active
        """
        enrollment = EnrollmentService.get_user_enrollment(db, user_id, course_id)
        return enrollment is not None and enrollment.status == EnrollmentStatus.ACTIVE
    
    @staticmethod
    def get_user_enrollments(
        db: Session,
        user_id: str,
        status: Optional[EnrollmentStatus] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Enrollment]:
        """
        Get user's enrollments.
        
        Args:
            db: Database session
            user_id: User ID
            status: Filter by enrollment status
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Enrollment]: List of enrollments
        """
        query = db.query(Enrollment).options(
            joinedload(Enrollment.course)
        ).filter(Enrollment.user_id == user_id)
        
        if status:
            query = query.filter(Enrollment.status == status)
        
        return query.order_by(Enrollment.enrolled_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def count_user_enrollments(
        db: Session,
        user_id: str,
        status: Optional[EnrollmentStatus] = None
    ) -> int:
        """
        Count user's enrollments.
        
        Args:
            db: Database session
            user_id: User ID
            status: Filter by enrollment status
            
        Returns:
            int: Total enrollment count
        """
        query = db.query(Enrollment).filter(Enrollment.user_id == user_id)
        
        if status:
            query = query.filter(Enrollment.status == status)
        
        return query.count()
    
    @staticmethod
    def get_course_enrollments(
        db: Session,
        course_id: str,
        status: Optional[EnrollmentStatus] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Enrollment]:
        """
        Get course enrollments.
        
        Args:
            db: Database session
            course_id: Course ID
            status: Filter by enrollment status
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Enrollment]: List of enrollments
        """
        query = db.query(Enrollment).options(
            joinedload(Enrollment.user)
        ).filter(Enrollment.course_id == course_id)
        
        if status:
            query = query.filter(Enrollment.status == status)
        
        return query.order_by(Enrollment.enrolled_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def count_course_enrollments(
        db: Session,
        course_id: str,
        status: Optional[EnrollmentStatus] = None
    ) -> int:
        """
        Count course enrollments.
        
        Args:
            db: Database session
            course_id: Course ID
            status: Filter by enrollment status
            
        Returns:
            int: Total enrollment count
        """
        query = db.query(Enrollment).filter(Enrollment.course_id == course_id)
        
        if status:
            query = query.filter(Enrollment.status == status)
        
        return query.count()
    
    @staticmethod
    def get_all_enrollments(
        db: Session,
        status: Optional[EnrollmentStatus] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Enrollment]:
        """
        Get all enrollments (Admin only).
        
        Args:
            db: Database session
            status: Filter by enrollment status
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Enrollment]: List of enrollments
        """
        query = db.query(Enrollment).options(
            joinedload(Enrollment.user),
            joinedload(Enrollment.course)
        )
        
        if status:
            query = query.filter(Enrollment.status == status)
        
        return query.order_by(Enrollment.enrolled_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def count_all_enrollments(
        db: Session,
        status: Optional[EnrollmentStatus] = None
    ) -> int:
        """
        Count all enrollments (Admin only).
        
        Args:
            db: Database session
            status: Filter by enrollment status
            
        Returns:
            int: Total enrollment count
        """
        query = db.query(Enrollment)
        
        if status:
            query = query.filter(Enrollment.status == status)
        
        return query.count()
    
    @staticmethod
    def unenroll_user(db: Session, enrollment: Enrollment) -> None:
        """
        Unenroll user from course.
        
        Args:
            db: Database session
            enrollment: Enrollment object to delete
        """
        course_id = enrollment.course_id
        
        db.delete(enrollment)
        
        # Update course enrollment count
        course = db.query(Course).filter(Course.id == course_id).first()
        if course:
            course.total_enrollments = db.query(func.count(Enrollment.id)).filter(
                Enrollment.course_id == course_id,
                Enrollment.status == EnrollmentStatus.ACTIVE
            ).scalar()
        
        db.commit()
    
    @staticmethod
    def update_enrollment_progress(db: Session, enrollment: Enrollment) -> Enrollment:
        """
        Update enrollment progress based on lesson completions.
        
        Args:
            db: Database session
            enrollment: Enrollment object
            
        Returns:
            Enrollment: Updated enrollment
        """
        # Get total lessons in course
        from app.models.content import Module, Lesson
        
        total_lessons = db.query(func.count(Lesson.id)).join(
            Module, Lesson.module_id == Module.id
        ).filter(Module.course_id == enrollment.course_id).scalar()
        
        if total_lessons == 0:
            enrollment.progress = 0.0
        else:
            # Get completed lessons
            from app.models.enrollment import Progress
            
            completed_lessons = db.query(func.count(Progress.id)).filter(
                Progress.enrollment_id == enrollment.id,
                Progress.is_completed == True
            ).scalar()
            
            enrollment.progress = (completed_lessons / total_lessons) * 100
            
            # Mark enrollment as completed if 100%
            if enrollment.progress >= 100:
                enrollment.status = EnrollmentStatus.COMPLETED
                if not enrollment.completed_at:
                    enrollment.completed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(enrollment)
        
        return enrollment
    
    @staticmethod
    def get_user_learning_stats(db: Session, user_id: str) -> dict:
        """
        Get user's learning statistics.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            dict: Learning statistics
        """
        # Total enrollments
        total_enrollments = db.query(func.count(Enrollment.id)).filter(
            Enrollment.user_id == user_id,
            Enrollment.status.in_([EnrollmentStatus.ACTIVE, EnrollmentStatus.COMPLETED])
        ).scalar()
        
        # Completed courses
        completed_courses = db.query(func.count(Enrollment.id)).filter(
            Enrollment.user_id == user_id,
            Enrollment.status == EnrollmentStatus.COMPLETED
        ).scalar()
        
        # In progress courses
        in_progress_courses = db.query(func.count(Enrollment.id)).filter(
            Enrollment.user_id == user_id,
            Enrollment.status == EnrollmentStatus.ACTIVE,
            Enrollment.progress > 0
        ).scalar()
        
        # Total time spent (from progress records)
        from app.models.enrollment import Progress
        
        total_time = db.query(func.sum(Progress.time_spent)).join(
            Enrollment, Progress.enrollment_id == Enrollment.id
        ).filter(Enrollment.user_id == user_id).scalar() or 0
        
        # Completed lessons
        from app.models.enrollment import Progress
        
        completed_lessons = db.query(func.count(Progress.id)).join(
            Enrollment, Progress.enrollment_id == Enrollment.id
        ).filter(
            Enrollment.user_id == user_id,
            Progress.is_completed == True
        ).scalar()
        
        # Average progress
        avg_progress = db.query(func.avg(Enrollment.progress)).filter(
            Enrollment.user_id == user_id,
            Enrollment.status == EnrollmentStatus.ACTIVE
        ).scalar() or 0
        
        return {
            "total_enrollments": total_enrollments,
            "completed_courses": completed_courses,
            "in_progress_courses": in_progress_courses,
            "total_time_spent": int(total_time),
            "completed_lessons": completed_lessons,
            "average_progress": float(avg_progress)
        }
    
    @staticmethod
    def verify_enrollment_access(enrollment: Enrollment, user: User) -> None:
        """
        Verify that user has access to enrollment.
        
        Args:
            enrollment: Enrollment object
            user: User object
            
        Raises:
            HTTPException: If user doesn't have access
        """
        if user.role == UserRole.ADMIN:
            return
        
        if enrollment.user_id != user.id:
            # Check if user is course instructor
            course = enrollment.course
            if not course or course.instructor_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to access this enrollment"
                )
