"""
Content service for module and lesson management.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from app.models.content import Module, Lesson, LessonType
from app.models.course import Course
from app.schemas.content import ModuleCreate, ModuleUpdate, LessonCreate, LessonUpdate


class ContentService:
    """Content management service."""
    
    # ============ Module Operations ============
    
    @staticmethod
    def create_module(db: Session, course_id: str, module_data: ModuleCreate) -> Module:
        """
        Create a new module in a course.
        
        Args:
            db: Database session
            course_id: Course ID
            module_data: Module creation data
            
        Returns:
            Module: Created module
        """
        # Get max order number
        max_order = db.query(Module).filter(
            Module.course_id == course_id
        ).count()
        
        module = Module(
            course_id=course_id,
            title=module_data.title,
            description=module_data.description,
            order=max_order + 1,
            is_published=False,
        )
        
        db.add(module)
        db.commit()
        db.refresh(module)
        
        return module
    
    @staticmethod
    def get_module_by_id(db: Session, module_id: str) -> Module:
        """
        Get module by ID.
        
        Args:
            db: Database session
            module_id: Module ID
            
        Returns:
            Module: Module object
            
        Raises:
            HTTPException: If module not found
        """
        module = db.query(Module).filter(Module.id == module_id).first()
        
        if not module:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Module not found"
            )
        
        return module
    
    @staticmethod
    def get_course_modules(
        db: Session,
        course_id: str,
        include_lessons: bool = False
    ) -> List[Module]:
        """
        Get all modules for a course.
        
        Args:
            db: Database session
            course_id: Course ID
            include_lessons: Whether to include lessons
            
        Returns:
            List[Module]: List of modules
        """
        query = db.query(Module).filter(Module.course_id == course_id)
        
        if include_lessons:
            query = query.options(joinedload(Module.lessons))
        
        return query.order_by(Module.order.asc()).all()
    
    @staticmethod
    def update_module(db: Session, module: Module, module_data: ModuleUpdate) -> Module:
        """
        Update module.
        
        Args:
            db: Database session
            module: Module object to update
            module_data: Update data
            
        Returns:
            Module: Updated module
        """
        update_data = module_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(module, field, value)
        
        module.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(module)
        
        return module
    
    @staticmethod
    def delete_module(db: Session, module: Module) -> None:
        """
        Delete module.
        
        Args:
            db: Database session
            module: Module object to delete
        """
        db.delete(module)
        db.commit()
    
    @staticmethod
    def reorder_modules(db: Session, course_id: str, module_orders: List[dict]) -> List[Module]:
        """
        Reorder modules in a course.
        
        Args:
            db: Database session
            course_id: Course ID
            module_orders: List of {module_id, order} dicts
            
        Returns:
            List[Module]: Reordered modules
        """
        modules = []
        
        for item in module_orders:
            module = db.query(Module).filter(
                Module.id == item["module_id"],
                Module.course_id == course_id
            ).first()
            
            if module:
                module.order = item["order"]
                modules.append(module)
        
        db.commit()
        
        return sorted(modules, key=lambda m: m.order)
    
    # ============ Lesson Operations ============
    
    @staticmethod
    def create_lesson(db: Session, module_id: str, lesson_data: LessonCreate) -> Lesson:
        """
        Create a new lesson in a module.
        
        Args:
            db: Database session
            module_id: Module ID
            lesson_data: Lesson creation data
            
        Returns:
            Lesson: Created lesson
        """
        # Get max order number
        max_order = db.query(Lesson).filter(
            Lesson.module_id == module_id
        ).count()
        
        lesson = Lesson(
            module_id=module_id,
            title=lesson_data.title,
            description=lesson_data.description,
            type=lesson_data.type,
            content=lesson_data.content,
            video_url=lesson_data.video_url,
            duration_minutes=lesson_data.duration_minutes,
            order=max_order + 1,
            is_published=False,
            is_free_preview=lesson_data.is_free_preview or False,
        )
        
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        
        return lesson
    
    @staticmethod
    def get_lesson_by_id(db: Session, lesson_id: str) -> Lesson:
        """
        Get lesson by ID.
        
        Args:
            db: Database session
            lesson_id: Lesson ID
            
        Returns:
            Lesson: Lesson object
            
        Raises:
            HTTPException: If lesson not found
        """
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        
        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found"
            )
        
        return lesson
    
    @staticmethod
    def get_module_lessons(db: Session, module_id: str) -> List[Lesson]:
        """
        Get all lessons for a module.
        
        Args:
            db: Database session
            module_id: Module ID
            
        Returns:
            List[Lesson]: List of lessons
        """
        return db.query(Lesson).filter(
            Lesson.module_id == module_id
        ).order_by(Lesson.order.asc()).all()
    
    @staticmethod
    def update_lesson(db: Session, lesson: Lesson, lesson_data: LessonUpdate) -> Lesson:
        """
        Update lesson.
        
        Args:
            db: Database session
            lesson: Lesson object to update
            lesson_data: Update data
            
        Returns:
            Lesson: Updated lesson
        """
        update_data = lesson_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(lesson, field, value)
        
        lesson.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(lesson)
        
        return lesson
    
    @staticmethod
    def delete_lesson(db: Session, lesson: Lesson) -> None:
        """
        Delete lesson.
        
        Args:
            db: Database session
            lesson: Lesson object to delete
        """
        db.delete(lesson)
        db.commit()
    
    @staticmethod
    def reorder_lessons(db: Session, module_id: str, lesson_orders: List[dict]) -> List[Lesson]:
        """
        Reorder lessons in a module.
        
        Args:
            db: Database session
            module_id: Module ID
            lesson_orders: List of {lesson_id, order} dicts
            
        Returns:
            List[Lesson]: Reordered lessons
        """
        lessons = []
        
        for item in lesson_orders:
            lesson = db.query(Lesson).filter(
                Lesson.id == item["lesson_id"],
                Lesson.module_id == module_id
            ).first()
            
            if lesson:
                lesson.order = item["order"]
                lessons.append(lesson)
        
        db.commit()
        
        return sorted(lessons, key=lambda l: l.order)
    
    @staticmethod
    def get_course_content_tree(db: Session, course_id: str) -> List[Module]:
        """
        Get complete content tree for a course (modules with lessons).
        
        Args:
            db: Database session
            course_id: Course ID
            
        Returns:
            List[Module]: List of modules with nested lessons
        """
        modules = db.query(Module).filter(
            Module.course_id == course_id
        ).options(joinedload(Module.lessons)).order_by(Module.order.asc()).all()
        
        # Sort lessons within each module
        for module in modules:
            module.lessons.sort(key=lambda l: l.order)
        
        return modules
