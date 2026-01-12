"""
Authentication service for user registration, login, and token management.
"""
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserRegister, UserLogin, TokenResponse
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    create_email_verification_token,
    verify_email_token,
    create_password_reset_token,
    verify_password_reset_token,
)
from app.core.config import settings


class AuthService:
    """Authentication service."""
    
    @staticmethod
    def register_user(db: Session, user_data: UserRegister) -> User:
        """
        Register a new user.
        
        Args:
            db: Database session
            user_data: User registration data
            
        Returns:
            User: Created user
            
        Raises:
            HTTPException: If email already exists
        """
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        user = User(
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=UserRole.STUDENT,  # Default role for public registration
            is_active=True,
            email_verified=False,
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # TODO: Send verification email
        # verification_token = create_email_verification_token(user.email)
        # send_verification_email(user.email, verification_token)
        
        return user
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        Create a new user (admin only).
        
        Args:
            db: Database session
            user_data: User creation data
            
        Returns:
            User: Created user
            
        Raises:
            HTTPException: If email already exists
        """
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        user = User(
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=user_data.role,
            is_active=True,
            email_verified=False,
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin) -> User:
        """
        Authenticate user with email and password.
        
        Args:
            db: Database session
            login_data: Login credentials
            
        Returns:
            User: Authenticated user
            
        Raises:
            HTTPException: If credentials are invalid
        """
        user = db.query(User).filter(User.email == login_data.email).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Update last login
        user.last_login_at = datetime.utcnow()
        db.commit()
        
        return user
    
    @staticmethod
    def create_tokens(user: User) -> TokenResponse:
        """
        Create access and refresh tokens for user.
        
        Args:
            user: User object
            
        Returns:
            TokenResponse: Token response with access and refresh tokens
        """
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> TokenResponse:
        """
        Refresh access token using refresh token.
        
        Args:
            db: Database session
            refresh_token: Refresh token
            
        Returns:
            TokenResponse: New token response
            
        Raises:
            HTTPException: If refresh token is invalid
        """
        payload = decode_token(refresh_token)
        
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        return AuthService.create_tokens(user)
    
    @staticmethod
    def verify_email(db: Session, token: str) -> User:
        """
        Verify user email with token.
        
        Args:
            db: Database session
            token: Verification token
            
        Returns:
            User: Verified user
            
        Raises:
            HTTPException: If token is invalid
        """
        email = verify_email_token(token)
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token"
            )
        
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if user.email_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already verified"
            )
        
        user.email_verified = True
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def request_password_reset(db: Session, email: str) -> str:
        """
        Request password reset token.
        
        Args:
            db: Database session
            email: User email
            
        Returns:
            str: Password reset token
            
        Raises:
            HTTPException: If user not found
        """
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            # Don't reveal if user exists
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="If this email exists, a password reset link will be sent"
            )
        
        reset_token = create_password_reset_token(user.email)
        
        # TODO: Send password reset email
        # send_password_reset_email(user.email, reset_token)
        
        return reset_token
    
    @staticmethod
    def reset_password(db: Session, token: str, new_password: str) -> User:
        """
        Reset user password with token.
        
        Args:
            db: Database session
            token: Password reset token
            new_password: New password
            
        Returns:
            User: User with updated password
            
        Raises:
            HTTPException: If token is invalid
        """
        email = verify_password_reset_token(token)
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.password_hash = get_password_hash(new_password)
        db.commit()
        db.refresh(user)
        
        return user
