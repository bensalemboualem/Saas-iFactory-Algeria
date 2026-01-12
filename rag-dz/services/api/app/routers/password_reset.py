"""
Password Reset Router
Handles forgot password and reset password flows
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.notification_service import get_notification_service
from app.prompts import get_user_profile_from_domain
import secrets
from datetime import datetime, timedelta
from passlib.context import CryptContext

router = APIRouter(prefix="/api/auth", tags=["Password Reset"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory store for reset tokens (for production, use Redis or database)
# Structure: {token: {"email": str, "expires": datetime}}
reset_tokens = {}


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class ResetPasswordResponse(BaseModel):
    message: str


@router.post("/forgot-password", response_model=dict)
def forgot_password(
    request_data: ForgotPasswordRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Send password reset email with token
    """
    # Check if user exists
    user = db.query(User).filter(User.email == request_data.email).first()

    # Always return success to prevent email enumeration
    if not user:
        return {
            "message": "Si un compte existe avec cet email, vous recevrez un lien de réinitialisation.",
            "success": True
        }

    # Generate reset token (32 random bytes)
    reset_token = secrets.token_urlsafe(32)

    # Store token with 1-hour expiration
    reset_tokens[reset_token] = {
        "email": user.email,
        "expires": datetime.utcnow() + timedelta(hours=1)
    }

    # Detect profile from domain
    origin = request.headers.get("origin", "")
    host = request.headers.get("host", "")
    domain = origin or host or "geneva.localhost"
    profile, domain_context = get_user_profile_from_domain(domain)

    # Send reset email
    notification_service = get_notification_service()

    # Determine reset URL based on domain
    if "iafactory.ch" in domain:
        reset_url = f"https://iafactory.ch/reset-password?token={reset_token}"
    elif "iafactoryalgeria.com" in domain:
        reset_url = f"https://iafactoryalgeria.com/reset-password?token={reset_token}"
    else:
        reset_url = f"http://localhost:3000/reset-password?token={reset_token}"

    try:
        notification_service.send_reset_password_email(
            to_email=user.email,
            user_name=user.full_name or user.email.split("@")[0],
            reset_url=reset_url,
            profile=profile,
            domain_context=domain_context
        )
    except Exception as e:
        print(f"Failed to send reset email: {e}")
        # Still return success to prevent email enumeration

    return {
        "message": "Si un compte existe avec cet email, vous recevrez un lien de réinitialisation.",
        "success": True
    }


@router.post("/reset-password", response_model=ResetPasswordResponse)
def reset_password(
    request_data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Reset password using valid token
    """
    # Validate token
    if request_data.token not in reset_tokens:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token invalide ou expiré"
        )

    token_data = reset_tokens[request_data.token]

    # Check expiration
    if datetime.utcnow() > token_data["expires"]:
        del reset_tokens[request_data.token]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expiré. Veuillez demander un nouveau lien de réinitialisation."
        )

    # Validate password strength
    if len(request_data.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le mot de passe doit contenir au moins 8 caractères"
        )

    # Find user
    user = db.query(User).filter(User.email == token_data["email"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable"
        )

    # Update password
    user.hashed_password = pwd_context.hash(request_data.new_password)
    db.commit()

    # Invalidate token
    del reset_tokens[request_data.token]

    return ResetPasswordResponse(
        message="Votre mot de passe a été réinitialisé avec succès. Vous pouvez maintenant vous connecter."
    )


@router.get("/verify-reset-token/{token}")
def verify_reset_token(token: str):
    """
    Verify if a reset token is valid (for frontend validation)
    """
    if token not in reset_tokens:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token invalide"
        )

    token_data = reset_tokens[token]

    if datetime.utcnow() > token_data["expires"]:
        del reset_tokens[token]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expiré"
        )

    return {"valid": True, "email": token_data["email"]}
