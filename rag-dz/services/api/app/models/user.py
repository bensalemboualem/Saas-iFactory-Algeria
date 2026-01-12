"""
User Models - Authentication & Authorization
Multi-Tenant Support: Each user belongs to a tenant
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User roles within a tenant"""
    owner = "owner"
    admin = "admin"
    member = "member"
    viewer = "viewer"


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    tenant_id: Optional[str] = None  # UUID as string
    role: UserRole = UserRole.member


class UserCreate(BaseModel):
    """User creation schema"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    tenant_id: Optional[str] = None  # If None, create new tenant


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """User update schema"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    """User as stored in database"""
    id: str  # UUID as string
    hashed_password: str
    created_at: datetime
    updated_at: datetime


class User(UserBase):
    """User response schema (no password)"""
    id: str  # UUID as string
    created_at: datetime
    updated_at: datetime
    tenant_name: Optional[str] = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """User response with token (multi-tenant)"""
    user: User
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class Token(BaseModel):
    """JWT Token response"""
    access_token: str
    token_type: str = "bearer"


class TokenResponse(BaseModel):
    """Full token response with refresh (multi-tenant)"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 3600  # 1 hour in seconds


class TokenData(BaseModel):
    """Token payload data - Multi-tenant aware"""
    email: Optional[str] = None
    user_id: Optional[str] = None  # UUID as string
    tenant_id: Optional[str] = None  # UUID as string
    role: Optional[str] = None


class TenantCreate(BaseModel):
    """Tenant creation schema"""
    name: str
    slug: Optional[str] = None
    region: str = "DZ"
    plan: str = "free"


class TenantResponse(BaseModel):
    """Tenant response schema"""
    id: str
    name: str
    slug: Optional[str] = None
    region: str
    plan: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
