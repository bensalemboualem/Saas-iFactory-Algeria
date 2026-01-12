"""
Authentication API routes.
"""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import (
    UserRegister,
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
    TokenRefresh,
    EmailVerification,
    PasswordResetRequest,
    PasswordReset,
)
from app.services.auth_service import AuthService


router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegister,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Register a new user account.
    
    - **email**: Valid email address
    - **password**: At least 8 characters
    - **first_name**: User's first name
    - **last_name**: User's last name
    """
    user = AuthService.register_user(db, user_data)
    return user


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: UserLogin,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Authenticate user and return access tokens.
    
    - **email**: User's email
    - **password**: User's password
    """
    user = AuthService.authenticate_user(db, login_data)
    return AuthService.create_tokens(user)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    token_data: TokenRefresh,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Refresh access token using refresh token.
    
    - **refresh_token**: Valid refresh token
    """
    return AuthService.refresh_access_token(db, token_data.refresh_token)


@router.post("/verify-email", response_model=UserResponse)
def verify_email(
    verification_data: EmailVerification,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Verify user email with verification token.
    
    - **token**: Email verification token
    """
    user = AuthService.verify_email(db, verification_data.token)
    return user


@router.post("/resend-verification", status_code=status.HTTP_200_OK)
def resend_verification(
    email_data: PasswordResetRequest,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Resend email verification link.
    
    - **email**: User's email address
    """
    user = db.query(User).filter(User.email == email_data.email).first()
    
    if not user:
        # Don't reveal if user exists
        return {"message": "If this email exists, a verification link will be sent"}
    
    if user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified"
        )
    
    # TODO: Send verification email
    # verification_token = create_email_verification_token(user.email)
    # send_verification_email(user.email, verification_token)
    
    return {"message": "Verification email sent"}


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
def forgot_password(
    email_data: PasswordResetRequest,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Request password reset link.
    
    - **email**: User's email address
    """
    try:
        AuthService.request_password_reset(db, email_data.email)
    except HTTPException:
        pass  # Don't reveal if user exists
    
    return {"message": "If this email exists, a password reset link will be sent"}


@router.post("/reset-password", response_model=UserResponse)
def reset_password(
    reset_data: PasswordReset,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Reset password with reset token.
    
    - **token**: Password reset token
    - **new_password**: New password (min 8 characters)
    """
    user = AuthService.reset_password(db, reset_data.token, reset_data.new_password)
    return user


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Logout current user.
    
    Note: Token invalidation should be handled client-side.
    For server-side invalidation, implement token blacklisting with Redis.
    """
    # TODO: Add token to Redis blacklist
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Get current authenticated user profile.
    """
    return current_user
