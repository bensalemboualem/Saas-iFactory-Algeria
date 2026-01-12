"""
Content management API routes (Modules and Lessons).
"""
from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.content import (
    ModuleCreate,
    ModuleUpdate,
    ModuleResponse,
    ModuleReorder,
    LessonCreate,
    LessonUpdate,
    LessonResponse,
    LessonReorder,
)
from app.services.course_service import CourseService
from app.services.content_service import ContentService


router = APIRouter()


# ============ Module Endpoints ============

@router.post("/courses/{course_id}/modules", response_model=ModuleResponse, status_code=status.HTTP_201_CREATED)
def create_module(
    course_id: str,
    module_data: ModuleCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Create a new module in a course (Instructor owner or Admin only).
    
    - **title**: Module title
    - **description**: Module description
    """
    course = CourseService.get_course_by_id(db, course_id)
    CourseService.verify_instructor_access(course, current_user)
    
    module = ContentService.create_module(db, course_id, module_data)
    return module


@router.get("/courses/{course_id}/modules", response_model=List[ModuleResponse])
def get_course_modules(
    course_id: str,
    db: Annotated[Session, Depends(get_db)],
    include_lessons: bool = False
):
    """
    Get all modules for a course.
    
    - **include_lessons**: Include lessons in response
    """
    modules = ContentService.get_course_modules(db, course_id, include_lessons=include_lessons)
    return modules


@router.get("/modules/{module_id}", response_model=ModuleResponse)
def get_module(
    module_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get module by ID.
    """
    module = ContentService.get_module_by_id(db, module_id)
    return module


@router.put("/modules/{module_id}", response_model=ModuleResponse)
def update_module(
    module_id: str,
    module_data: ModuleUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Update module (Instructor owner or Admin only).
    """
    module = ContentService.get_module_by_id(db, module_id)
    course = CourseService.get_course_by_id(db, module.course_id)
    CourseService.verify_instructor_access(course, current_user)
    
    updated_module = ContentService.update_module(db, module, module_data)
    return updated_module


@router.delete("/modules/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_module(
    module_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Delete module (Instructor owner or Admin only).
    
    Will also delete all lessons in the module.
    """
    module = ContentService.get_module_by_id(db, module_id)
    course = CourseService.get_course_by_id(db, module.course_id)
    CourseService.verify_instructor_access(course, current_user)
    
    ContentService.delete_module(db, module)


@router.post("/courses/{course_id}/modules/reorder", response_model=List[ModuleResponse])
def reorder_modules(
    course_id: str,
    reorder_data: ModuleReorder,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Reorder modules in a course (Instructor owner or Admin only).
    
    - **module_orders**: List of {module_id, order} objects
    """
    course = CourseService.get_course_by_id(db, course_id)
    CourseService.verify_instructor_access(course, current_user)
    
    modules = ContentService.reorder_modules(db, course_id, reorder_data.module_orders)
    return modules


# ============ Lesson Endpoints ============

@router.post("/modules/{module_id}/lessons", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
def create_lesson(
    module_id: str,
    lesson_data: LessonCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Create a new lesson in a module (Instructor owner or Admin only).
    
    - **title**: Lesson title
    - **description**: Lesson description
    - **type**: Lesson type (video, article, quiz, assignment)
    - **content**: Lesson content (markdown/HTML)
    - **video_url**: Video URL (for video lessons)
    - **duration_minutes**: Lesson duration
    - **is_free_preview**: Whether lesson is available for preview
    """
    module = ContentService.get_module_by_id(db, module_id)
    course = CourseService.get_course_by_id(db, module.course_id)
    CourseService.verify_instructor_access(course, current_user)
    
    lesson = ContentService.create_lesson(db, module_id, lesson_data)
    return lesson


@router.get("/modules/{module_id}/lessons", response_model=List[LessonResponse])
def get_module_lessons(
    module_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get all lessons for a module.
    """
    lessons = ContentService.get_module_lessons(db, module_id)
    return lessons


@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
def get_lesson(
    lesson_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get lesson by ID.
    """
    lesson = ContentService.get_lesson_by_id(db, lesson_id)
    return lesson


@router.put("/lessons/{lesson_id}", response_model=LessonResponse)
def update_lesson(
    lesson_id: str,
    lesson_data: LessonUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Update lesson (Instructor owner or Admin only).
    """
    lesson = ContentService.get_lesson_by_id(db, lesson_id)
    module = ContentService.get_module_by_id(db, lesson.module_id)
    course = CourseService.get_course_by_id(db, module.course_id)
    CourseService.verify_instructor_access(course, current_user)
    
    updated_lesson = ContentService.update_lesson(db, lesson, lesson_data)
    return updated_lesson


@router.delete("/lessons/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lesson(
    lesson_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Delete lesson (Instructor owner or Admin only).
    """
    lesson = ContentService.get_lesson_by_id(db, lesson_id)
    module = ContentService.get_module_by_id(db, lesson.module_id)
    course = CourseService.get_course_by_id(db, module.course_id)
    CourseService.verify_instructor_access(course, current_user)
    
    ContentService.delete_lesson(db, lesson)


@router.post("/modules/{module_id}/lessons/reorder", response_model=List[LessonResponse])
def reorder_lessons(
    module_id: str,
    reorder_data: LessonReorder,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Reorder lessons in a module (Instructor owner or Admin only).
    
    - **lesson_orders**: List of {lesson_id, order} objects
    """
    module = ContentService.get_module_by_id(db, module_id)
    course = CourseService.get_course_by_id(db, module.course_id)
    CourseService.verify_instructor_access(course, current_user)
    
    lessons = ContentService.reorder_lessons(db, module_id, reorder_data.lesson_orders)
    return lessons


@router.get("/courses/{course_id}/content-tree", response_model=List[ModuleResponse])
def get_course_content_tree(
    course_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get complete content tree for a course (modules with nested lessons).
    
    Returns hierarchical structure of all modules and lessons.
    """
    modules = ContentService.get_course_content_tree(db, course_id)
    return modules
