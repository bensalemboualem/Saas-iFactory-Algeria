"""
Course management API routes.
"""
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role, require_admin
from app.models.user import User, UserRole
from app.schemas.course import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    CourseFilterParams,
)
from app.schemas.base import PaginationParams, PaginatedResponse
from app.services.course_service import CourseService


router = APIRouter()


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course_data: CourseCreate,
    current_user: Annotated[User, Depends(require_role([UserRole.INSTRUCTOR, UserRole.ADMIN]))],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Create a new course (Instructor/Admin only).
    
    - **title**: Course title
    - **slug**: URL-friendly identifier
    - **description**: Full course description
    - **short_description**: Brief summary
    - **level**: Course difficulty level
    - **category**: Course category
    - **price**: Course price
    """
    course = CourseService.create_course(db, course_data, current_user.id)
    return course


@router.get("/", response_model=PaginatedResponse[CourseResponse])
def get_courses(
    pagination: Annotated[PaginationParams, Depends()],
    filters: Annotated[CourseFilterParams, Depends()],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Optional[User], Depends(get_current_user)] = None
):
    """
    Get list of courses with filters and pagination.
    
    Public endpoint, but returns different data based on authentication:
    - Public: Only published courses
    - Instructors: Their own courses + published courses
    - Admins: All courses
    
    **Filters:**
    - **level**: Filter by course level
    - **category**: Filter by category
    - **instructor_id**: Filter by instructor
    - **is_published**: Filter by publication status
    - **search**: Search in title/description
    - **tags**: Filter by tags
    - **min_price/max_price**: Price range
    - **language**: Filter by language
    - **sort_by**: Sort field (title, price, rating, enrollments, created_at)
    - **sort_order**: asc or desc
    """
    # Adjust filters based on user role
    if not current_user or current_user.role == UserRole.STUDENT:
        # Public/students only see published courses
        filters.is_published = True
    elif current_user.role == UserRole.INSTRUCTOR:
        # Instructors see their courses + published courses
        if not filters.instructor_id:
            pass  # Show all published courses unless filtering by instructor
    # Admins see everything (no filter modification)
    
    courses = CourseService.get_courses(
        db,
        filters,
        skip=(pagination.page - 1) * pagination.page_size,
        limit=pagination.page_size,
        include_instructor=True
    )
    total = CourseService.count_courses(db, filters)
    
    return PaginatedResponse(
        items=courses,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        pages=(total + pagination.page_size - 1) // pagination.page_size
    )


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Optional[User], Depends(get_current_user)] = None
):
    """
    Get course by ID.
    
    - Public: Only published courses
    - Instructors: Their own courses + published courses
    - Admins: All courses
    """
    course = CourseService.get_course_by_id(db, course_id, include_instructor=True)
    
    # Check access permissions
    if not current_user:
        # Public access - only published courses
        if not course.is_published:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
    elif current_user.role == UserRole.STUDENT:
        # Students only see published courses
        if not course.is_published:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
    elif current_user.role == UserRole.INSTRUCTOR:
        # Instructors see their own courses + published courses
        if not course.is_published and course.instructor_id != current_user.id:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this course"
            )
    # Admins see everything
    
    return course


@router.get("/slug/{slug}", response_model=CourseResponse)
def get_course_by_slug(
    slug: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Optional[User], Depends(get_current_user)] = None
):
    """
    Get course by slug.
    
    Same access rules as get_course.
    """
    course = CourseService.get_course_by_slug(db, slug)
    
    # Apply same access checks as get_course
    if not current_user:
        if not course.is_published:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
    elif current_user.role == UserRole.STUDENT:
        if not course.is_published:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
    elif current_user.role == UserRole.INSTRUCTOR:
        if not course.is_published and course.instructor_id != current_user.id:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this course"
            )
    
    return course


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: str,
    course_data: CourseUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Update course (Instructor owner or Admin only).
    """
    course = CourseService.get_course_by_id(db, course_id)
    CourseService.verify_instructor_access(course, current_user)
    
    updated_course = CourseService.update_course(db, course, course_data)
    return updated_course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Delete course (Instructor owner or Admin only).
    
    Cannot delete courses with active enrollments.
    """
    course = CourseService.get_course_by_id(db, course_id)
    CourseService.verify_instructor_access(course, current_user)
    
    CourseService.delete_course(db, course)


@router.post("/{course_id}/publish", response_model=CourseResponse)
def publish_course(
    course_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Publish course (Instructor owner or Admin only).
    
    Course must have:
    - Title and description
    - At least one module
    """
    course = CourseService.get_course_by_id(db, course_id)
    CourseService.verify_instructor_access(course, current_user)
    
    published_course = CourseService.publish_course(db, course)
    return published_course


@router.post("/{course_id}/unpublish", response_model=CourseResponse)
def unpublish_course(
    course_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Unpublish course (Instructor owner or Admin only).
    
    Makes course unavailable to public.
    """
    course = CourseService.get_course_by_id(db, course_id)
    CourseService.verify_instructor_access(course, current_user)
    
    unpublished_course = CourseService.unpublish_course(db, course)
    return unpublished_course


@router.post("/{course_id}/update-stats", response_model=CourseResponse)
def update_course_stats(
    course_id: str,
    current_user: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Update course statistics (Admin only).
    
    Recalculates:
    - Total enrollments
    - Module count
    - Lesson count
    - Average rating
    - Review count
    """
    course = CourseService.get_course_by_id(db, course_id)
    updated_course = CourseService.update_course_stats(db, course)
    return updated_course


@router.get("/instructor/{instructor_id}", response_model=PaginatedResponse[CourseResponse])
def get_instructor_courses(
    instructor_id: str,
    pagination: Annotated[PaginationParams, Depends()],
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Optional[User], Depends(get_current_user)] = None,
    is_published: Optional[bool] = None
):
    """
    Get courses by instructor.
    
    - Public: Only published courses
    - Same instructor: All their courses
    - Admins: All courses
    """
    filters = CourseFilterParams(instructor_id=instructor_id)
    
    # Adjust visibility based on user
    if not current_user:
        filters.is_published = True
    elif current_user.role == UserRole.STUDENT:
        filters.is_published = True
    elif current_user.role == UserRole.INSTRUCTOR:
        if current_user.id != instructor_id:
            filters.is_published = True
    # Admin sees all
    
    if is_published is not None:
        filters.is_published = is_published
    
    courses = CourseService.get_courses(
        db,
        filters,
        skip=(pagination.page - 1) * pagination.page_size,
        limit=pagination.page_size,
        include_instructor=True
    )
    total = CourseService.count_courses(db, filters)
    
    return PaginatedResponse(
        items=courses,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        pages=(total + pagination.page_size - 1) // pagination.page_size
    )
