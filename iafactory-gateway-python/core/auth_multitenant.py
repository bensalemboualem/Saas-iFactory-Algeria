"""
Authentication Service - JWT + Password Hashing
Multi-Tenant Support: JWT includes tenant_id for RLS isolation
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import HTTPException, status
import logging

from app.config import get_settings
from app.models.user import TokenData

settings = get_settings()
logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = settings.api_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Extended to 1 hour
REFRESH_TOKEN_EXPIRE_DAYS = 7


class AuthService:
    """Service for authentication operations with multi-tenant support"""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password for storing"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None,
        tenant_id: Optional[str] = None,
        role: Optional[str] = None
    ) -> str:
        """
        Create a JWT access token with multi-tenant support

        Args:
            data: Data to encode (sub=email, user_id)
            expires_delta: Optional expiration time override
            tenant_id: Tenant UUID for RLS isolation
            role: User role within tenant (owner, admin, member, viewer)

        Returns:
            Encoded JWT token with tenant context
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "tenant_id": tenant_id,
            "role": role
        })

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info(f"Access token created for: {data.get('sub', 'unknown')} | tenant: {tenant_id}")

        return encoded_jwt

    @staticmethod
    def create_refresh_token(user_id: str, tenant_id: str) -> str:
        """
        Create a refresh token for token renewal

        Args:
            user_id: User UUID
            tenant_id: Tenant UUID

        Returns:
            Encoded refresh token (7 days validity)
        """
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        to_encode = {
            "sub": user_id,
            "tenant_id": tenant_id,
            "type": "refresh",
            "exp": expire,
            "iat": datetime.utcnow()
        }

        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_access_token(token: str) -> TokenData:
        """
        Decode and validate a JWT token with tenant context

        Args:
            token: JWT token string

        Returns:
            TokenData with user and tenant information

        Raises:
            HTTPException: If token is invalid or expired
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            user_id: str = payload.get("user_id")
            tenant_id: str = payload.get("tenant_id")
            role: str = payload.get("role")

            if email is None:
                raise credentials_exception

            token_data = TokenData(
                email=email,
                user_id=user_id,
                tenant_id=tenant_id,
                role=role
            )
            return token_data

        except JWTError as e:
            logger.error(f"JWT decode error: {e}")
            raise credentials_exception

    @staticmethod
    def decode_refresh_token(token: str) -> dict:
        """
        Decode refresh token for token renewal

        Args:
            token: Refresh token string

        Returns:
            dict with user_id, tenant_id

        Raises:
            HTTPException: If token is invalid
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type"
                )

            return {
                "user_id": payload.get("sub"),
                "tenant_id": payload.get("tenant_id")
            }

        except JWTError as e:
            logger.error(f"Refresh token decode error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )


# Global instance
auth_service = AuthService()
