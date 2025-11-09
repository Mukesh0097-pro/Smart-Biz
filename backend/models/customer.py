"""
Customer model for managing business contacts
"""

from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from backend.core.database import Base

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Basic Info
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    company_name = Column(String)
    
    # Business Details
    gst_number = Column(String)
    pan_number = Column(String)
    
    # Address (stored as JSON)
    billing_address = Column(JSON)
    shipping_address = Column(JSON)
    
    # Status
    is_active = Column(Boolean, default=True)
    customer_type = Column(String, default="regular")  # regular, premium, etc.
    
    # Notes
    notes = Column(String)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Customer {self.name}>"
