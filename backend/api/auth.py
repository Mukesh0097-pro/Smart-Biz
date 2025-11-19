"""
Authentication API routes
"""

from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from core.database import get_db
from core.security import hash_password, verify_password, create_access_token, get_current_user
from models.user import User

router = APIRouter()

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    business_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

@router.post("/register", response_model=Token)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        business_name=user_data.business_name,
        full_name=user_data.business_name or user_data.email.split('@')[0]
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(data={"sub": str(new_user.id), "email": new_user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(new_user.id),
            "email": new_user.email,
            "full_name": new_user.full_name,
            "business_name": new_user.business_name
        }
    }

@router.post("/login", response_model=Token)
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Login user - accepts form data (username as email, password)"""
    # Find user by email (username field contains email)
    user = db.query(User).filter(User.email == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "business_name": getattr(user, 'business_name', None)
        }
    }

@router.get("/me")
async def get_me(db: Session = Depends(get_db)):
    """Get current user profile (for testing - returns first user)"""
    # For testing: return first user if no auth provided
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="No users found. Please register first.")
    
    return {   
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name
    }
