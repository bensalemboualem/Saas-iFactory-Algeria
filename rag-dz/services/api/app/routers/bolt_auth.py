"""
Bolt.diy Authentication Bridge
Exchange Bolt.diy sessions for rag-dz JWT tokens
"""
from fastapi import APIRouter, HTTPException, status, Header
from pydantic import BaseModel
from datetime import timedelta, datetime
from typing import Optional
import logging
import hashlib
import secrets

from app.services.auth_service import auth_service, ACCESS_TOKEN_EXPIRE_MINUTES
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/bolt/auth", tags=["bolt-auth"])

# Store for session exchange tokens (in production, use Redis)
_session_store: dict = {}


class BoltSessionExchange(BaseModel):
    """Request model for session exchange"""
    bolt_session_id: str
    client_type: str = "bolt-diy"
    api_key: Optional[str] = None


class BoltTokenResponse(BaseModel):
    """Response model for token exchange"""
    access_token: str
    token_type: str = "bearer"
    expires_at: int
    user_id: Optional[str] = None
    email: Optional[str] = None


class BoltValidateResponse(BaseModel):
    """Response model for token validation"""
    valid: bool
    user_id: Optional[str] = None
    expires_at: Optional[int] = None


@router.post("/exchange", response_model=BoltTokenResponse)
async def exchange_session(
    request: BoltSessionExchange,
    x_api_key: Optional[str] = Header(None),
):
    """
    Exchange Bolt.diy session for rag-dz JWT token

    This endpoint allows Bolt.diy to obtain a JWT token that can be used
    to authenticate with the rag-dz API, enabling features like:
    - BMAD chat with agent personalities
    - RAG context injection
    - Credits tracking

    Args:
        request: Session exchange request with bolt_session_id
        x_api_key: Optional API key for additional authentication

    Returns:
        JWT token response with access_token and expiration
    """
    try:
        # Validate API key if required
        api_key = x_api_key or request.api_key
        if settings.api_secret_key and api_key != settings.api_secret_key:
            # If no API key but session ID is valid, create anonymous token
            if not _validate_bolt_session(request.bolt_session_id):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid API key or session"
                )

        # Generate a hash-based user ID from session
        session_hash = hashlib.sha256(request.bolt_session_id.encode()).hexdigest()[:16]
        user_id = f"bolt_{session_hash}"

        # Create JWT token with bolt user context
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expires_at = int((datetime.utcnow() + expires_delta).timestamp() * 1000)

        access_token = auth_service.create_access_token(
            data={
                "sub": user_id,
                "user_id": user_id,
                "client_type": request.client_type,
                "source": "bolt-exchange",
            },
            expires_delta=expires_delta,
            tenant_id=None,  # Bolt users are anonymous by default
            role="bolt_user"
        )

        # Store session mapping for validation
        _session_store[request.bolt_session_id] = {
            "user_id": user_id,
            "token_hash": hashlib.sha256(access_token.encode()).hexdigest()[:32],
            "expires_at": expires_at,
            "created_at": datetime.utcnow().isoformat(),
        }

        logger.info(f"✅ Bolt session exchanged: {user_id} | client: {request.client_type}")

        return BoltTokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_at=expires_at,
            user_id=user_id,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Session exchange error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Session exchange failed"
        )


@router.get("/validate", response_model=BoltValidateResponse)
async def validate_token(
    authorization: str = Header(...),
):
    """
    Validate a Bolt JWT token

    Args:
        authorization: Bearer token in Authorization header

    Returns:
        Validation result with user info
    """
    try:
        # Extract token from header
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header"
            )

        token = authorization[7:]  # Remove "Bearer " prefix

        # Verify token
        payload = auth_service.verify_token(token)
        if not payload:
            return BoltValidateResponse(valid=False)

        return BoltValidateResponse(
            valid=True,
            user_id=payload.get("user_id"),
            expires_at=payload.get("exp", 0) * 1000,  # Convert to milliseconds
        )

    except Exception as e:
        logger.warning(f"Token validation error: {e}")
        return BoltValidateResponse(valid=False)


@router.post("/refresh", response_model=BoltTokenResponse)
async def refresh_token(
    authorization: str = Header(...),
):
    """
    Refresh a Bolt JWT token before expiration

    Args:
        authorization: Bearer token in Authorization header

    Returns:
        New JWT token response
    """
    try:
        # Extract and verify current token
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header"
            )

        token = authorization[7:]
        payload = auth_service.verify_token(token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        # Create new token with same user context
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expires_at = int((datetime.utcnow() + expires_delta).timestamp() * 1000)

        new_token = auth_service.create_access_token(
            data={
                "sub": payload.get("sub"),
                "user_id": payload.get("user_id"),
                "client_type": payload.get("client_type", "bolt-diy"),
                "source": "bolt-refresh",
            },
            expires_delta=expires_delta,
            tenant_id=payload.get("tenant_id"),
            role=payload.get("role", "bolt_user")
        )

        logger.info(f"✅ Bolt token refreshed: {payload.get('user_id')}")

        return BoltTokenResponse(
            access_token=new_token,
            token_type="bearer",
            expires_at=expires_at,
            user_id=payload.get("user_id"),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


def _validate_bolt_session(session_id: str) -> bool:
    """
    Validate Bolt session ID format
    In production, this could verify against a session store
    """
    # Basic validation: session should be a non-empty string
    if not session_id or len(session_id) < 10:
        return False

    # Check if session is in store and not expired
    if session_id in _session_store:
        session = _session_store[session_id]
        if session.get("expires_at", 0) > datetime.utcnow().timestamp() * 1000:
            return True

    # For anonymous sessions, accept any valid-looking ID
    # This allows Bolt.diy users to get tokens without pre-registration
    return True
