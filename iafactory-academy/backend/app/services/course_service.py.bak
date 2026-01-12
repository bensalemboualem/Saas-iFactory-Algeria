"""
Course service for course management operations.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_
from fastapi import HTTPException, status

from app.models.course import Course, CourseLevel, CourseStatus
from app.models.user import User, UserRole
from app.schemas.course import CourseCreate, CourseUpdate, CourseFilterParams


class CourseService:
    """Course management service."""
    
    @staticmethod
    def create_course(db: Session, course_data: CourseCreate, instructor_id: str) -> Course:
        """
        Create a new course.
        
        Args:
            db: Database session
            course_data: Course creation data
            instructor_id: ID of the instructor creating the course
            
        Returns:
            Course: Created course
        """
        course = Course(
            title=course_data.title,
            slug=course_data.slug,
            description=course_data.description,
            short_description=course_data.short_description,
            thumbnail_url=course_data.thumbnail_url,
            trailer_url=course_data.trailer_url,
            level=course_data.level,
            category=course_data.category,
            tags=course_data.tags or [],
            requirements=course_data.requirements or [],
            learning_outcomes=course_data.learning_outcomes or [],
            price=course_data.price,
            discount_price=course_data.discount_price,
            duration_hours=course_data.duration_hours,
            language=course_data.language,
            status=CourseStatus.DRAFT,  # Always start as draft
            instructor_id=instructor_id,
            is_published=False,
        )
        
        db.add(course)
        db.commit()
        db.refresh(course)
        
        return course
    
    @staticmethod
    def get_course_by_id(
        db: Session,
        course_id: str,
        include_instructor: bool = False
    ) -> Course:
        """
        Get course by ID.
        
        Args:
            db: Database session
            course_id: Course ID
            include_instructor: Whether to include instructor data
            
        Returns:
            Course: Course object
            
        Raises:
            HTTPException: If course not found
        """
        query = db.query(Course)
        
        if include_instructor:
            query = query.options(joinedload(Course.instructor))
        
        course = query.filter(Course.id == course_id).first()
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        return course
    
    @staticmethod
    def get_course_by_slug(db: Session, slug: str) -> Course:
        """
        Get course by slug.
        
        Args:
            db: Database session
            slug: Course slug
            
        Returns:
            Course: Course object
            
        Raises:
            HTTPException: If course not found
        """
        course = db.query(Course).filter(Course.slug == slug).first()
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        return course
    
    @staticmethod
    def get_courses(
        db: Session,
        filters: CourseFilterParams,
        skip: int = 0,
        limit: int = 20,
        include_instructor: bool = False
    ) -> List[Course]:
        """
        Get list of courses with filters and pagination.
        
        Args:
            db: Database session
            filters: Filter parameters
            skip: Number of records to skip
            limit: Maximum number of records to return
            include_instructor: Whether to include instructor data
            
        Returns:
            List[Course]: List of courses
        """
        query = db.query(Course)
        
        if include_instructor:
            query = query.options(joinedload(Course.instructor))
        
        # Apply filters
        if filters.level:
            query = query.filter(Course.level == filters.level)
        
        if filters.category:
            query = query.filter(Course.category == filters.category)
        
        if filters.instructor_id:
            query = query.filter(Course.instructor_id == filters.instructor_id)
        
        if filters.is_published is not None:
            query = query.filter(Course.is_published == filters.is_published)
        
        if filters.status:
            query = query.filter(Course.status == filters.status)
        
        if filters.min_price is not None:
            query = query.filter(Course.price >= filters.min_price)
        
        if filters.max_price is not None:
            query = query.filter(Course.price <= filters.max_price)
        
        if filters.language:
            query = query.filter(Course.language == filters.language)
        
        if filters.search:
            search_term = f"%{filters.search}%"
            query = query.filter(
                or_(
                    Course.title.ilike(search_term),
                    Course.description.ilike(search_term),
                    Course.short_description.ilike(search_term)
                )
            )
        
        if filters.tags:
            for tag in filters.tags:
                query = query.filter(Course.tags.contains([tag]))
        
        # Apply sorting
        if filters.sort_by == "title":
            query = query.order_by(Course.title.asc() if filters.sort_order == "asc" else Course.title.desc())
        elif filters.sort_by == "price":
            query = query.order_by(Course.price.asc() if filters.sort_order == "asc" else Course.price.desc())
        elif filters.sort_by == "rating":
            query = query.order_by(Course.rating.desc() if filters.sort_order == "desc" else Course.rating.asc())
        elif filters.sort_by == "enrollments":
            query = query.order_by(Course.total_enrollments.desc() if filters.sort_order == "desc" else Course.total_enrollments.asc())
        else:  # created_at (default)
            query = query.order_by(Course.created_at.desc() if filters.sort_order == "desc" else Course.created_at.asc())
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def count_courses(db: Session, filters: CourseFilterParams) -> int:
        """
        Count total courses matching filters.
        
        Args:
            db: Database session
            filters: Filter parameters
            
        Returns:
            int: Total course count
        """
        query = db.query(Course)
        
        # Apply same filters as get_courses
        if filters.level:
            query = query.filter(Course.level == filters.level)
        
        if filters.category:
            query = query.filter(Course.category == filters.category)
        
        if filters.instructor_id:
            query = query.filter(Course.instructor_id == filters.instructor_id)
        
        if filters.is_published is not None:
            query = query.filter(Course.is_published == filters.is_published)
        
        if filters.status:
            query = query.filter(Course.status == filters.status)
        
        if filters.min_price is not None:
            query = query.filter(Course.price >= filters.min_price)
        
        if filters.max_price is not None:
            query = query.filter(Course.price <= filters.max_price)
        
        if filters.language:
            query = query.filter(Course.language == filters.language)
        
        if filters.search:
            search_term = f"%{filters.search}%"
            query = query.filter(
                or_(
                    Course.title.ilike(search_term),
                    Course.description.ilike(search_term),
                    Course.short_description.ilike(search_term)
                )
            )
        
        if filters.tags:
            for tag in filters.tags:
                query = query.filter(Course.tags.contains([tag]))
        
        return query.count()
    
    @staticmethod
    def update_course(db: Session, course: Course, course_data: CourseUpdate) -> Course:
        """
        Update course.
        
        Args:
            db: Database session
            course: Course object to update
            course_data: Update data
            
        Returns:
            Course: Updated course
        """
        update_data = course_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(course, field, value)
        
        course.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(course)
        
        return course
    
    @staticmethod
    def delete_course(db: Session, course: Course) -> None:
        """
        Delete course.
        
        Args:
            db: Database session
            course: Course object to delete
            
        Raises:
            HTTPException: If course has enrollments
        """
        if course.total_enrollments > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete course with active enrollments"
            )
        
        db.delete(course)
        db.commit()
    
    @staticmethod
    def publish_course(db: Session, course: Course) -> Course:
        """
        Publish course.
        
        Args:
            db: Database session
            course: Course object to publish
            
        Returns:
            Course: Published course
            
        Raises:
            HTTPException: If course is not ready to publish
        """
        # Validate course is ready to publish
        if not course.title or not course.description:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course must have title and description"
            )
        
        if course.modules_count == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course must have at least one module"
            )
        
        course.is_published = True
        course.status = CourseStatus.PUBLISHED
        course.published_at = datetime.utcnow()
        course.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(course)
        
        return course
    
    @staticmethod
    def unpublish_course(db: Session, course: Course) -> Course:
        """
        Unpublish course.
        
        Args:
            db: Database session
            course: Course object to unpublish
            
        Returns:
            Course: Unpublished course
        """
        course.is_published = False
        course.status = CourseStatus.DRAFT
        course.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(course)
        
        return course
    
    @staticmethod
    def update_course_stats(db: Session, course: Course) -> Course:
        """
        Update course statistics (enrollments, modules, lessons, rating).
        
        Args:
            db: Database session
            course: Course object
            
        Returns:
            Course: Course with updated stats
        """
        # Count enrollments
        from app.models.enrollment import Enrollment
        course.total_enrollments = db.query(func.count(Enrollment.id)).filter(
            Enrollment.course_id == course.id
        ).scalar()
        
        # Count modules
        from app.models.content import Module
        course.modules_count = db.query(func.count(Module.id)).filter(
            Module.course_id == course.id
        ).scalar()
        
        # Count lessons
        from app.models.content import Lesson
        course.lessons_count = db.query(func.count(Lesson.id)).join(
            Module, Lesson.module_id == Module.id
        ).filter(Module.course_id == course.id).scalar()
        
        # Calculate average rating
        from app.models.course import Review
        avg_rating = db.query(func.avg(Review.rating)).filter(
            Review.course_id == course.id
        ).scalar()
        
        if avg_rating:
            course.rating = float(avg_rating)
        
        # Count reviews
        course.reviews_count = db.query(func.count(Review.id)).filter(
            Review.course_id == course.id
        ).scalar()
        
        db.commit()
        db.refresh(course)
        
        return course
    
    @staticmethod
    def verify_instructor_access(course: Course, user: User) -> None:
        """
        Verify that user is the course instructor or admin.
        
        Args:
            course: Course object
            user: User object
            
        Raises:
            HTTPException: If user doesn't have access
        """
        if user.role != UserRole.ADMIN and course.instructor_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this course"
            )
