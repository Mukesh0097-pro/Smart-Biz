"""
Memory models for conversation context and business insights
"""

from sqlalchemy import Column, String, DateTime, JSON, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from core.database import Base

class ConversationMemory(Base):
    __tablename__ = "conversation_memory"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(String, nullable=False, index=True)  # Group related conversations
    
    # Conversation data
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    intent = Column(String)  # invoice, gst, insights, general
    entities = Column(JSON)  # Extracted entities from query
    
    # Context
    meta_info = Column(JSON)  # Additional context (language, source, etc)
    embedding = Column(JSON)  # Vector embedding for semantic search (future)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<ConversationMemory {self.id} - {self.intent}>"


class BusinessContext(Base):
    __tablename__ = "business_context"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Context type: invoice_insights, gst_summary, customer_pattern, etc
    context_type = Column(String, nullable=False, index=True)
    context_key = Column(String, nullable=False)  # Unique identifier for this context
    
    # Data
    data = Column(JSON, nullable=False)  # Structured insights/patterns
    summary = Column(Text)  # Human-readable summary
    
    # Metadata
    confidence_score = Column(Integer, default=100)  # 0-100
    expires_at = Column(DateTime)  # Auto-expire stale insights
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<BusinessContext {self.context_type} - {self.context_key}>"


class UserPreferences(Base):
    __tablename__ = "user_preferences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    
    # Preferences
    default_language = Column(String, default="en")
    notification_settings = Column(JSON, default={})  # Email, SMS preferences
    dashboard_layout = Column(JSON, default={})  # Customized dashboard
    ai_settings = Column(JSON, default={})  # AI response style, verbosity
    
    # Usage patterns (learned)
    frequent_queries = Column(JSON, default=[])  # Most asked questions
    preferred_topics = Column(JSON, default=[])  # invoice, gst, insights
    active_hours = Column(JSON, default={})  # When user is most active
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserPreferences {self.user_id}>"
