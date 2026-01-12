"""
FastAPI Dependencies for authentication and authorization
"""
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
import logging
import asyncpg
import os

from app.services.auth_service import auth_service
from app.services.user_repository import user_repository
from app.models.user import User, UserInDB

logger = logging.getLogger(__name__)

# Database Pool (singleton)
_db_pool: Optional[asyncpg.Pool] = None

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
    auto_error=False  # Don't auto-raise on missing token
)


def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[UserInDB]:
    """
    Get current authenticated user from JWT token

    Args:
        token: JWT token from Authorization header

    Returns:
        User if token is valid, None otherwise

    Raises:
        HTTPException: If token is invalid or user not found
    """
    if not token:
        return None

    # Decode token
    token_data = auth_service.decode_access_token(token)

    # Get user from database
    user = user_repository.get_user_by_email(token_data.email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user


def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    """
    Get current active user (required authentication)

    Args:
        current_user: User from get_current_user dependency

    Returns:
        Active user

    Raises:
        HTTPException: If user is not authenticated or inactive
    """
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return current_user


def get_current_superuser(current_user: UserInDB = Depends(get_current_active_user)) -> UserInDB:
    """
    Get current superuser (admin only)

    Args:
        current_user: User from get_current_active_user dependency

    Returns:
        Superuser

    Raises:
        HTTPException: If user is not a superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return current_user


def optional_user(current_user: Optional[UserInDB] = Depends(get_current_user)) -> Optional[UserInDB]:
    """
    Optional user dependency - doesn't require authentication

    Args:
        current_user: User from get_current_user dependency (may be None)

    Returns:
        User if authenticated, None otherwise
    """
    return current_user


async def get_db_pool() -> asyncpg.Pool:
    """
    Get database connection pool

    Returns:
        PostgreSQL connection pool
    """
    global _db_pool

    if _db_pool is None:
        # Create pool if not exists
        database_url = os.getenv("POSTGRES_URL")
        if not database_url:
            raise ValueError("POSTGRES_URL environment variable is required")
        _db_pool = await asyncpg.create_pool(
            database_url,
            min_size=5,
            max_size=20,
            command_timeout=60
        )
        logger.info("Database pool created")

    return _db_pool


async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """
    Verify API key from header

    Args:
        x_api_key: API key from X-API-Key header

    Returns:
        Validated API key

    Raises:
        HTTPException: If API key is invalid or missing
    """
    valid_api_key = os.getenv("API_SECRET_KEY")

    if not valid_api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API_SECRET_KEY not configured"
        )

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
            headers={"WWW-Authenticate": "ApiKey"}
        )

    if x_api_key != valid_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"}
        )

    return x_api_key
