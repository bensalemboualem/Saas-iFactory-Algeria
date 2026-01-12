"""
User management API routes.
"""
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_admin
from app.models.user import User
from app.schemas.user import (
    UserResponse,
    UserUpdate,
    UserPasswordChange,
)
from app.schemas.base import PaginationParams, PaginatedResponse
from app.services.user_service import UserService


router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Get current user's profile.
    """
    return current_user


@router.put("/me", response_model=UserResponse)
def update_my_profile(
    user_data: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Update current user's profile.
    
    - **first_name**: User's first name
    - **last_name**: User's last name
    - **bio**: User's biography
    - **avatar_url**: Profile picture URL
    """
    return UserService.update_user(db, current_user, user_data)


@router.put("/me/password", response_model=UserResponse)
def change_my_password(
    password_data: UserPasswordChange,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Change current user's password.
    
    - **current_password**: Current password
    - **new_password**: New password (min 8 characters)
    """
    return UserService.change_password(db, current_user, password_data)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_account(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Delete current user's account.
    
    This action is permanent and cannot be undone.
    """
    UserService.delete_user(db, current_user)


@router.get("/", response_model=PaginatedResponse[UserResponse])
def get_users(
    pagination: Annotated[PaginationParams, Depends()],
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_admin)],
    is_active: Optional[bool] = None
):
    """
    Get list of all users (Admin only).
    
    - **page**: Page number (starts at 1)
    - **page_size**: Number of items per page
    - **is_active**: Filter by active status
    """
    users = UserService.get_users(
        db,
        skip=(pagination.page - 1) * pagination.page_size,
        limit=pagination.page_size,
        is_active=is_active
    )
    total = UserService.count_users(db, is_active=is_active)
    
    return PaginatedResponse(
        items=users,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        pages=(total + pagination.page_size - 1) // pagination.page_size
    )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_admin)]
):
    """
    Get user by ID (Admin only).
    """
    return UserService.get_user_by_id(db, user_id)


@router.put("/{user_id}/activate", response_model=UserResponse)
def activate_user(
    user_id: str,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_admin)]
):
    """
    Activate user account (Admin only).
    """
    user = UserService.get_user_by_id(db, user_id)
    return UserService.activate_user(db, user)


@router.put("/{user_id}/deactivate", response_model=UserResponse)
def deactivate_user(
    user_id: str,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_admin)]
):
    """
    Deactivate user account (Admin only).
    """
    user = UserService.get_user_by_id(db, user_id)
    return UserService.deactivate_user(db, user)
