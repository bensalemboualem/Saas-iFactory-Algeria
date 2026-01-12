"""
User service for user management operations.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserUpdate, UserPasswordChange
from app.core.security import verify_password, get_password_hash


class UserService:
    """User management service."""
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> User:
        """
        Get user by ID.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            User: User object
            
        Raises:
            HTTPException: If user not found
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            db: Database session
            email: User email
            
        Returns:
            Optional[User]: User object or None
        """
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_users(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        is_active: Optional[bool] = None
    ) -> List[User]:
        """
        Get list of users with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            is_active: Filter by active status
            
        Returns:
            List[User]: List of users
        """
        query = db.query(User)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def count_users(db: Session, is_active: Optional[bool] = None) -> int:
        """
        Count total users.
        
        Args:
            db: Database session
            is_active: Filter by active status
            
        Returns:
            int: Total user count
        """
        query = db.query(User)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        return query.count()
    
    @staticmethod
    def update_user(db: Session, user: User, user_data: UserUpdate) -> User:
        """
        Update user profile.
        
        Args:
            db: Database session
            user: User object to update
            user_data: Update data
            
        Returns:
            User: Updated user
        """
        update_data = user_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def change_password(
        db: Session,
        user: User,
        password_data: UserPasswordChange
    ) -> User:
        """
        Change user password.
        
        Args:
            db: Database session
            user: User object
            password_data: Password change data
            
        Returns:
            User: Updated user
            
        Raises:
            HTTPException: If current password is incorrect
        """
        # Verify current password
        if not verify_password(password_data.current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Update password
        user.password_hash = get_password_hash(password_data.new_password)
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def activate_user(db: Session, user: User) -> User:
        """
        Activate user account.
        
        Args:
            db: Database session
            user: User object
            
        Returns:
            User: Activated user
        """
        user.is_active = True
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def deactivate_user(db: Session, user: User) -> User:
        """
        Deactivate user account.
        
        Args:
            db: Database session
            user: User object
            
        Returns:
            User: Deactivated user
        """
        user.is_active = False
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def delete_user(db: Session, user: User) -> None:
        """
        Delete user account.
        
        Args:
            db: Database session
            user: User object
        """
        db.delete(user)
        db.commit()
