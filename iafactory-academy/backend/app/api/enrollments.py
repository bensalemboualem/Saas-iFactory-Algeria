"""
Enrollment and Progress API routes.
"""
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_admin
from app.models.user import User
from app.models.enrollment import EnrollmentStatus
from app.schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentResponse,
    ProgressCreate,
    ProgressUpdate,
    ProgressResponse,
)
from app.schemas.base import PaginationParams, PaginatedResponse
from app.services.enrollment_service import EnrollmentService
from app.services.progress_service import ProgressService


router = APIRouter()


# ============ Enrollment Endpoints ============

@router.post("/courses/{course_id}/enroll", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_in_course(
    course_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Enroll current user in a course.
    
    - Course must be published
    - User cannot be already enrolled
    """
    enrollment = EnrollmentService.enroll_user(db, current_user.id, course_id)
    return enrollment


@router.get("/", response_model=PaginatedResponse[EnrollmentResponse])
def get_all_enrollments(
    pagination: Annotated[PaginationParams, Depends()],
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_admin)],
    status: Optional[EnrollmentStatus] = None
):
    """
    Get all enrollments (Admin only).
    
    - **status**: Filter by enrollment status
    """
    enrollments = EnrollmentService.get_all_enrollments(
        db,
        status=status,
        skip=(pagination.page - 1) * pagination.page_size,
        limit=pagination.page_size
    )
    total = EnrollmentService.count_all_enrollments(db, status=status)
    
    return PaginatedResponse(
        items=enrollments,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        pages=(total + pagination.page_size - 1) // pagination.page_size
    )


@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
def get_enrollment(
    enrollment_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get enrollment by ID.
    
    Users can only view their own enrollments unless admin.
    """
    enrollment = EnrollmentService.get_enrollment_by_id(
        db,
        enrollment_id,
        include_course=True,
        include_user=True
    )
    
    EnrollmentService.verify_enrollment_access(enrollment, current_user)
    
    return enrollment


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def unenroll_from_course(
    enrollment_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Unenroll from a course.
    
    Users can only unenroll themselves unless admin.
    """
    enrollment = EnrollmentService.get_enrollment_by_id(db, enrollment_id)
    
    EnrollmentService.verify_enrollment_access(enrollment, current_user)
    
    EnrollmentService.unenroll_user(db, enrollment)


@router.get("/my/courses", response_model=PaginatedResponse[EnrollmentResponse])
def get_my_enrollments(
    pagination: Annotated[PaginationParams, Depends()],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    status: Optional[EnrollmentStatus] = None
):
    """
    Get current user's enrollments.
    
    - **status**: Filter by enrollment status
    """
    enrollments = EnrollmentService.get_user_enrollments(
        db,
        current_user.id,
        status=status,
        skip=(pagination.page - 1) * pagination.page_size,
        limit=pagination.page_size
    )
    total = EnrollmentService.count_user_enrollments(db, current_user.id, status=status)
    
    return PaginatedResponse(
        items=enrollments,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        pages=(total + pagination.page_size - 1) // pagination.page_size
    )


@router.get("/my/progress/{course_id}")
def get_my_course_progress(
    course_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get current user's progress in a course.
    
    Returns detailed progress breakdown with all lessons.
    """
    enrollment = EnrollmentService.get_user_enrollment(db, current_user.id, course_id)
    
    if not enrollment:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not enrolled in this course"
        )
    
    progress_summary = ProgressService.get_course_progress_summary(db, enrollment.id)
    return progress_summary


@router.get("/my/stats")
def get_my_learning_stats(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get current user's learning statistics.
    
    Returns:
    - Total enrollments
    - Completed courses
    - In progress courses
    - Total time spent
    - Completed lessons
    - Average progress
    """
    stats = EnrollmentService.get_user_learning_stats(db, current_user.id)
    return stats


# ============ Progress Endpoints ============

@router.post("/lessons/{lesson_id}/progress", response_model=ProgressResponse, status_code=status.HTTP_201_CREATED)
def track_lesson_progress(
    lesson_id: str,
    progress_data: ProgressCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Track progress for a lesson.
    
    - **time_spent**: Time spent in seconds
    - **last_position**: Last video position in seconds
    - **notes**: Student notes
    
    User must be enrolled in the course.
    """
    # Get lesson to find course
    from app.services.content_service import ContentService
    lesson = ContentService.get_lesson_by_id(db, lesson_id)
    
    # Get module to find course
    module = ContentService.get_module_by_id(db, lesson.module_id)
    
    # Check enrollment
    enrollment = EnrollmentService.get_user_enrollment(db, current_user.id, module.course_id)
    
    if not enrollment:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Must be enrolled in course to track progress"
        )
    
    progress = ProgressService.track_lesson_progress(
        db,
        enrollment.id,
        lesson_id,
        progress_data
    )
    
    return progress


@router.put("/lessons/{lesson_id}/progress", response_model=ProgressResponse)
def update_lesson_progress(
    lesson_id: str,
    progress_data: ProgressUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Update progress for a lesson.
    """
    # Get lesson to find course
    from app.services.content_service import ContentService
    lesson = ContentService.get_lesson_by_id(db, lesson_id)
    module = ContentService.get_module_by_id(db, lesson.module_id)
    
    # Check enrollment
    enrollment = EnrollmentService.get_user_enrollment(db, current_user.id, module.course_id)
    
    if not enrollment:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Must be enrolled in course"
        )
    
    # Get existing progress
    progress = ProgressService.get_lesson_progress(db, enrollment.id, lesson_id)
    
    if not progress:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress record not found"
        )
    
    updated_progress = ProgressService.update_lesson_progress(db, progress, progress_data)
    return updated_progress


@router.post("/lessons/{lesson_id}/complete", response_model=ProgressResponse)
def complete_lesson(
    lesson_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Mark a lesson as completed.
    
    Automatically updates course progress percentage.
    """
    # Get lesson to find course
    from app.services.content_service import ContentService
    lesson = ContentService.get_lesson_by_id(db, lesson_id)
    module = ContentService.get_module_by_id(db, lesson.module_id)
    
    # Check enrollment
    enrollment = EnrollmentService.get_user_enrollment(db, current_user.id, module.course_id)
    
    if not enrollment:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Must be enrolled in course"
        )
    
    # Get or create progress
    progress = ProgressService.get_lesson_progress(db, enrollment.id, lesson_id)
    
    if not progress:
        # Create progress record if doesn't exist
        progress_data = ProgressCreate(time_spent=0, last_position=0)
        progress = ProgressService.track_lesson_progress(
            db,
            enrollment.id,
            lesson_id,
            progress_data
        )
    
    completed_progress = ProgressService.complete_lesson(db, progress)
    return completed_progress


@router.get("/lessons/{lesson_id}/progress", response_model=ProgressResponse)
def get_lesson_progress(
    lesson_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get current user's progress for a specific lesson.
    """
    # Get lesson to find course
    from app.services.content_service import ContentService
    lesson = ContentService.get_lesson_by_id(db, lesson_id)
    module = ContentService.get_module_by_id(db, lesson.module_id)
    
    # Check enrollment
    enrollment = EnrollmentService.get_user_enrollment(db, current_user.id, module.course_id)
    
    if not enrollment:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not enrolled in this course"
        )
    
    progress = ProgressService.get_lesson_progress(db, enrollment.id, lesson_id)
    
    if not progress:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No progress record found for this lesson"
        )
    
    return progress
