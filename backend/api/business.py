"""
Business profile API routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict

from core.database import get_db
from core.security import get_current_user
from models.user import User

router = APIRouter()

class BusinessProfile(BaseModel):
    business_name: str
    gst_number: Optional[str] = None
    udyam_id: Optional[str] = None
    business_address: Optional[Dict] = None
    business_type: Optional[str] = None
    phone: Optional[str] = None

@router.get("/profile")
async def get_business_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get business profile"""
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "business_name": user.business_name,
        "gst_number": user.gst_number,
        "udyam_id": user.udyam_id,
        "business_address": user.business_address,
        "business_type": user.business_type,
        "phone": user.phone
    }

@router.put("/profile")
async def update_business_profile(
    profile: BusinessProfile,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update business profile"""
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields
    user.business_name = profile.business_name
    user.gst_number = profile.gst_number
    user.udyam_id = profile.udyam_id
    user.business_address = profile.business_address
    user.business_type = profile.business_type
    if profile.phone:
        user.phone = profile.phone
    
    db.commit()
    
    return {"message": "Profile updated successfully"}
