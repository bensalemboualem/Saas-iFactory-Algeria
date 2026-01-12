"""
Authentication Routes - Login, Register, Profile
Multi-Tenant Support: JWT includes tenant_id + role for RLS isolation
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Optional
import logging

from app.models.user import UserCreate, UserLogin, UserResponse, Token, User, TokenResponse
from app.services.user_repository import user_repository
from app.services.auth_service import auth_service, ACCESS_TOKEN_EXPIRE_MINUTES
from app.dependencies import get_current_active_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate):
    """
    Register a new user with multi-tenant support

    Args:
        user_data: User registration data (email, password, full_name, tenant_id optional)

    Returns:
        User object with access token containing tenant_id

    Raises:
        HTTPException 400: If user already exists
    """
    try:
        # Create user in database (repository handles tenant creation if needed)
        user = user_repository.create_user(user_data)

        # Get tenant_id and role from user (set during creation)
        tenant_id = getattr(user, 'tenant_id', None)
        role = getattr(user, 'role', 'member')

        # Generate access token WITH tenant context
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_service.create_access_token(
            data={"sub": user.email, "user_id": str(user.id)},
            expires_delta=access_token_expires,
            tenant_id=tenant_id,
            role=role
        )

        # Generate refresh token
        refresh_token = None
        if tenant_id:
            refresh_token = auth_service.create_refresh_token(
                user_id=str(user.id),
                tenant_id=tenant_id
            )

        logger.info(f"✅ User registered: {user.email} | tenant: {tenant_id}")

        return UserResponse(
            user=User(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                created_at=user.created_at,
                updated_at=user.updated_at
            ),
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login user with email and password (OAuth2 compatible)
    Multi-tenant: JWT includes tenant_id for RLS isolation

    Args:
        form_data: OAuth2 form with username (email) and password

    Returns:
        Access token with tenant context

    Raises:
        HTTPException 401: If credentials are invalid
    """
    # Authenticate user
    user = user_repository.authenticate_user(
        email=form_data.username,  # OAuth2 uses 'username' field
        password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get tenant_id and role from user
    tenant_id = getattr(user, 'tenant_id', None)
    role = getattr(user, 'role', 'member')

    # Generate access token WITH tenant context
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "user_id": str(user.id)},
        expires_delta=access_token_expires,
        tenant_id=tenant_id,
        role=role
    )

    logger.info(f"✅ User logged in: {user.email} | tenant: {tenant_id}")

    return Token(access_token=access_token, token_type="bearer")


@router.post("/login/json", response_model=Token)
def login_json(credentials: UserLogin):
    """
    Login user with JSON body (alternative to OAuth2 form)
    Multi-tenant: JWT includes tenant_id for RLS isolation

    Args:
        credentials: User login data (email, password)

    Returns:
        Access token with tenant context

    Raises:
        HTTPException 401: If credentials are invalid
    """
    # Authenticate user
    user = user_repository.authenticate_user(
        email=credentials.email,
        password=credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get tenant_id and role from user
    tenant_id = getattr(user, 'tenant_id', None)
    role = getattr(user, 'role', 'member')

    # Generate access token WITH tenant context
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "user_id": str(user.id)},
        expires_delta=access_token_expires,
        tenant_id=tenant_id,
        role=role
    )

    logger.info(f"✅ User logged in (JSON): {user.email} | tenant: {tenant_id}")

    return Token(access_token=access_token, token_type="bearer")


@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str):
    """
    Refresh access token using refresh token

    Args:
        refresh_token: Valid refresh token

    Returns:
        New access token with same tenant context
    """
    try:
        # Decode refresh token
        token_data = auth_service.decode_refresh_token(refresh_token)
        user_id = token_data["user_id"]
        tenant_id = token_data["tenant_id"]

        # Get user to verify still active
        user = user_repository.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )

        # Get role from user
        role = getattr(user, 'role', 'member')

        # Generate new access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_service.create_access_token(
            data={"sub": user.email, "user_id": str(user.id)},
            expires_delta=access_token_expires,
            tenant_id=tenant_id,
            role=role
        )

        logger.info(f"✅ Token refreshed: {user.email} | tenant: {tenant_id}")

        return Token(access_token=access_token, token_type="bearer")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.get("/me", response_model=User)
def get_current_user_profile(current_user = Depends(get_current_active_user)):
    """
    Get current user profile

    Args:
        current_user: Current authenticated user (from dependency)

    Returns:
        User profile
    """
    return User(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )


@router.get("/health")
def auth_health():
    """Auth service health check"""
    return {
        "status": "healthy",
        "service": "Authentication Service",
        "token_expiry_minutes": ACCESS_TOKEN_EXPIRE_MINUTES
    }
