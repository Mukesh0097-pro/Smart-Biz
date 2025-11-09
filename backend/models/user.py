"""
User model for authentication and profiles
"""

from sqlalchemy import Column, String, Boolean, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from backend.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=True)  # Nullable for OAuth users
    full_name = Column(String)
    phone = Column(String)
    
    # Authentication
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    auth_provider = Column(String, default="email")  # email, google, firebase
    
    # Business Profile
    business_name = Column(String)
    gst_number = Column(String)
    udyam_id = Column(String)
    business_address = Column(JSON)  # Store as JSON
    business_type = Column(String)  # MSME, Startup, etc.
    
    # Preferences
    language_preference = Column(String, default="en")  # en, hi, ta, etc.
    timezone = Column(String, default="Asia/Kolkata")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    def __repr__(self):
        return f"<User {self.email}>"
