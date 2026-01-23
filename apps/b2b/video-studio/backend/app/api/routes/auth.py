from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
import uuid

from app.schemas import UserCreate, UserResponse, TokenResponse
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

# In-memory user storage (use DB in production)
users_db = {}


@router.post("/register", response_model=TokenResponse)
async def register(user: UserCreate):
    """Register a new user"""
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user.password)
    
    users_db[user.email] = {
        "id": user_id,
        "email": user.email,
        "name": user.name,
        "hashed_password": hashed_password,
        "credits": 50,  # Initial free credits
        "created_at": datetime.utcnow(),
    }
    
    token = create_access_token(data={"sub": user.email})
    
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user_id,
            email=user.email,
            name=user.name,
            credits=50,
            created_at=datetime.utcnow(),
        ),
    )


@router.post("/login", response_model=TokenResponse)
async def login(email: str, password: str):
    """Login user"""
    if email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = users_db[email]
    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": email})
    
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            credits=user["credits"],
            created_at=user["created_at"],
        ),
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """Get current user info"""
    # In production: decode JWT and get user from DB
    # For demo: return mock user
    return UserResponse(
        id="demo-user",
        email="demo@iafactory.dz",
        name="Demo User",
        credits=150,
        created_at=datetime.utcnow(),
    )
