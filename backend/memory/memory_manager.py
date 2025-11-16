"""
Memory Manager - Production-grade memory system with DB persistence
"""

import json
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

from models.memory import ConversationMemory, BusinessContext, UserPreferences

class MemoryManager:
    """
    Manages user conversation context and business insights
    Uses PostgreSQL for persistence with session-based organization
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    # ===== CONVERSATION MEMORY =====
    
    def save_conversation(
        self,
        user_id: str,
        session_id: str,
        query: str,
        response: str,
        intent: Optional[str] = None,
        entities: Optional[Dict] = None,
        meta_info: Optional[Dict] = None
    ) -> ConversationMemory:
        """Save a conversation turn to memory"""
        conversation = ConversationMemory(
            user_id=uuid.UUID(user_id),
            session_id=session_id,
            query=query,
            response=response,
            intent=intent,
            entities=entities or {},
            meta_info=meta_info or {}
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation
    
    def get_session_history(
        self,
        user_id: str,
        session_id: str,
        limit: int = 20
    ) -> List[ConversationMemory]:
        """Get conversation history for a session"""
        return (
            self.db.query(ConversationMemory)
            .filter(
                ConversationMemory.user_id == uuid.UUID(user_id),
                ConversationMemory.session_id == session_id
            )
            .order_by(desc(ConversationMemory.created_at))
            .limit(limit)
            .all()
        )
    
    def get_recent_conversations(
        self,
        user_id: str,
        limit: int = 10,
        days: int = 7
    ) -> List[ConversationMemory]:
        """Get recent conversations across all sessions"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        return (
            self.db.query(ConversationMemory)
            .filter(
                ConversationMemory.user_id == uuid.UUID(user_id),
                ConversationMemory.created_at >= cutoff
            )
            .order_by(desc(ConversationMemory.created_at))
            .limit(limit)
            .all()
        )
    
    def search_conversations(
        self,
        user_id: str,
        keyword: str,
        intent: Optional[str] = None,
        limit: int = 20
    ) -> List[ConversationMemory]:
        """Search conversations by keyword and optional intent"""
        query = self.db.query(ConversationMemory).filter(
            ConversationMemory.user_id == uuid.UUID(user_id)
        )
        
        if intent:
            query = query.filter(ConversationMemory.intent == intent)
        
        # Simple text search (upgrade to full-text search for production)
        query = query.filter(
            ConversationMemory.query.ilike(f"%{keyword}%") |
            ConversationMemory.response.ilike(f"%{keyword}%")
        )
        
        return query.order_by(desc(ConversationMemory.created_at)).limit(limit).all()
    
    # ===== BUSINESS CONTEXT =====
    
    def save_business_context(
        self,
        user_id: str,
        context_type: str,
        context_key: str,
        data: Dict,
        summary: Optional[str] = None,
        confidence_score: int = 100,
        expires_in_days: Optional[int] = None
    ) -> BusinessContext:
        """Save or update business context/insights"""
        # Check if exists
        existing = (
            self.db.query(BusinessContext)
            .filter(
                BusinessContext.user_id == uuid.UUID(user_id),
                BusinessContext.context_type == context_type,
                BusinessContext.context_key == context_key
            )
            .first()
        )
        
        if existing:
            existing.data = data
            existing.summary = summary
            existing.confidence_score = confidence_score
            existing.updated_at = datetime.utcnow()
            if expires_in_days:
                existing.expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
            self.db.commit()
            self.db.refresh(existing)
            return existing
        
        expires_at = None
        if expires_in_days:
            expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        
        context = BusinessContext(
            user_id=uuid.UUID(user_id),
            context_type=context_type,
            context_key=context_key,
            data=data,
            summary=summary,
            confidence_score=confidence_score,
            expires_at=expires_at
        )
        self.db.add(context)
        self.db.commit()
        self.db.refresh(context)
        return context
    
    def get_business_context(
        self,
        user_id: str,
        context_type: str,
        context_key: Optional[str] = None
    ) -> Optional[BusinessContext]:
        """Get specific business context"""
        query = self.db.query(BusinessContext).filter(
            BusinessContext.user_id == uuid.UUID(user_id),
            BusinessContext.context_type == context_type
        )
        
        # Filter out expired contexts
        query = query.filter(
            (BusinessContext.expires_at.is_(None)) |
            (BusinessContext.expires_at > datetime.utcnow())
        )
        
        if context_key:
            query = query.filter(BusinessContext.context_key == context_key)
            return query.first()
        
        return query.order_by(desc(BusinessContext.updated_at)).first()
    
    def get_all_contexts(
        self,
        user_id: str,
        context_type: Optional[str] = None
    ) -> List[BusinessContext]:
        """Get all business contexts for a user"""
        query = self.db.query(BusinessContext).filter(
            BusinessContext.user_id == uuid.UUID(user_id)
        )
        
        if context_type:
            query = query.filter(BusinessContext.context_type == context_type)
        
        # Filter out expired
        query = query.filter(
            (BusinessContext.expires_at.is_(None)) |
            (BusinessContext.expires_at > datetime.utcnow())
        )
        
        return query.order_by(desc(BusinessContext.updated_at)).all()
    
    # ===== USER PREFERENCES =====
    
    def get_preferences(self, user_id: str) -> UserPreferences:
        """Get or create user preferences"""
        prefs = (
            self.db.query(UserPreferences)
            .filter(UserPreferences.user_id == uuid.UUID(user_id))
            .first()
        )
        
        if not prefs:
            prefs = UserPreferences(user_id=uuid.UUID(user_id))
            self.db.add(prefs)
            self.db.commit()
            self.db.refresh(prefs)
        
        return prefs
    
    def update_preferences(
        self,
        user_id: str,
        **kwargs
    ) -> UserPreferences:
        """Update user preferences"""
        prefs = self.get_preferences(user_id)
        
        for key, value in kwargs.items():
            if hasattr(prefs, key):
                setattr(prefs, key, value)
        
        prefs.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(prefs)
        return prefs
    
    def track_query_pattern(self, user_id: str, query: str, intent: str):
        """Track user query patterns for learning preferences"""
        prefs = self.get_preferences(user_id)
        
        # Update frequent queries
        freq_queries = prefs.frequent_queries or []
        freq_queries.append({"query": query[:100], "intent": intent, "timestamp": datetime.utcnow().isoformat()})
        prefs.frequent_queries = freq_queries[-50:]  # Keep last 50
        
        # Update preferred topics
        topics = prefs.preferred_topics or []
        if intent and intent not in topics:
            topics.append(intent)
        prefs.preferred_topics = topics
        
        # Update active hours
        current_hour = datetime.utcnow().hour
        active_hours = prefs.active_hours or {}
        active_hours[str(current_hour)] = active_hours.get(str(current_hour), 0) + 1
        prefs.active_hours = active_hours
        
        prefs.updated_at = datetime.utcnow()
        self.db.commit()
    
    # ===== UTILITIES =====
    
    def cleanup_expired_contexts(self):
        """Remove expired business contexts"""
        self.db.query(BusinessContext).filter(
            BusinessContext.expires_at.isnot(None),
            BusinessContext.expires_at <= datetime.utcnow()
        ).delete()
        self.db.commit()
    
    def clear_user_memory(self, user_id: str, session_id: Optional[str] = None):
        """Clear conversation memory for user or session"""
        query = self.db.query(ConversationMemory).filter(
            ConversationMemory.user_id == uuid.UUID(user_id)
        )
        
        if session_id:
            query = query.filter(ConversationMemory.session_id == session_id)
        
        query.delete()
        self.db.commit()
    
    def get_context_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of user's memory state"""
        total_conversations = (
            self.db.query(ConversationMemory)
            .filter(ConversationMemory.user_id == uuid.UUID(user_id))
            .count()
        )
        
        recent_sessions = (
            self.db.query(ConversationMemory.session_id)
            .filter(ConversationMemory.user_id == uuid.UUID(user_id))
            .distinct()
            .limit(5)
            .all()
        )
        
        contexts = self.get_all_contexts(user_id)
        prefs = self.get_preferences(user_id)
        
        return {
            "total_conversations": total_conversations,
            "recent_sessions": [s[0] for s in recent_sessions],
            "active_contexts": len(contexts),
            "context_types": list(set(c.context_type for c in contexts)),
            "preferred_topics": prefs.preferred_topics or [],
            "default_language": prefs.default_language
        }


# Dependency for FastAPI
def get_memory_manager(db: Session) -> MemoryManager:
    """Dependency injection for memory manager"""
    return MemoryManager(db)
