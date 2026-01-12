# -*- coding: utf-8 -*-
"""
Module d'authentification JWT + API Key
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

security = HTTPBearer()

JWT_SECRET = os.getenv("JWT_SECRET", "default-secret-change-me")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DAYS = 7

def create_jwt_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """Crée un JWT token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=JWT_EXPIRATION_DAYS)
    
    to_encode = {"user_id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token: str) -> dict:
    """Vérifie un JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Dépendance FastAPI pour vérifier l'auth"""
    token = credentials.credentials
    
    # API Key (commence par iaf_)
    if token.startswith("iaf_"):
        # TODO: Vérifier en base de données
        return {"user_id": "api-key-user", "type": "api_key"}
    
    # JWT Token
    payload = verify_jwt_token(token)
    return {"user_id": payload.get("user_id"), "type": "jwt"}
