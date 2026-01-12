"""
Security utilities: JWT tokens, password hashing, authentication.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# =============================================================================
# SECURITY: JWT Algorithm Allowlist
# =============================================================================
# Only allow secure signing algorithms. NEVER allow "none" algorithm.
# Reference: https://www.invicti.com/web-vulnerability-scanner/vulnerabilities/jwt-signature-bypass-via-none-algorithm

ALLOWED_JWT_ALGORITHMS = ["HS256", "HS384", "HS512", "RS256", "RS384", "RS512", "ES256", "ES384", "ES512"]

def _validate_jwt_algorithm(algorithm: str) -> str:
    """
    SECURITY: Validate that the JWT algorithm is in the allowlist.
    Prevents JWT signature bypass via 'none' algorithm attack.
    """
    if algorithm.lower() == "none":
        raise ValueError("SECURITY ERROR: JWT algorithm 'none' is not allowed. This is a known vulnerability.")
    if algorithm not in ALLOWED_JWT_ALGORITHMS:
        raise ValueError(f"SECURITY ERROR: JWT algorithm '{algorithm}' is not in the allowlist: {ALLOWED_JWT_ALGORITHMS}")
    return algorithm

# Validate configured algorithm at startup
_validate_jwt_algorithm(settings.JWT_ALGORITHM)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Optional custom expiration time
        
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        data: Data to encode in the token
        
    Returns:
        str: Encoded JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify a JWT token.

    SECURITY: Only accepts tokens signed with algorithms in ALLOWED_JWT_ALGORITHMS.
    Explicitly rejects tokens with alg="none" to prevent signature bypass attacks.

    Args:
        token: JWT token to decode

    Returns:
        Optional[Dict]: Decoded token payload or None if invalid
    """
    try:
        # SECURITY: Explicitly specify allowed algorithms to prevent alg=none attack
        # The algorithms parameter is a whitelist - only these algorithms are accepted
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],  # Only accept configured algorithm
            options={
                "verify_signature": True,  # Always verify signature
                "require": ["exp", "type"],  # Require expiration and type claims
            }
        )
        return payload
    except JWTError:
        return None


def create_email_verification_token(email: str) -> str:
    """
    Create a token for email verification.
    
    Args:
        email: User email address
        
    Returns:
        str: Verification token
    """
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = {"sub": email, "exp": expire, "type": "email_verification"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    return encoded_jwt


def create_password_reset_token(email: str) -> str:
    """
    Create a token for password reset.
    
    Args:
        email: User email address
        
    Returns:
        str: Reset token
    """
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {"sub": email, "exp": expire, "type": "password_reset"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    return encoded_jwt


def verify_email_token(token: str) -> Optional[str]:
    """
    Verify an email verification token.
    
    Args:
        token: Email verification token
        
    Returns:
        Optional[str]: Email address if valid, None otherwise
    """
    payload = decode_token(token)
    if payload and payload.get("type") == "email_verification":
        return payload.get("sub")
    return None


def verify_password_reset_token(token: str) -> Optional[str]:
    """
    Verify a password reset token.
    
    Args:
        token: Password reset token
        
    Returns:
        Optional[str]: Email address if valid, None otherwise
    """
    payload = decode_token(token)
    if payload and payload.get("type") == "password_reset":
        return payload.get("sub")
    return None
