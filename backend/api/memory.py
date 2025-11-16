"""
Memory API - Manage conversation context and business insights
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

from core.database import get_db
# from core.security import get_current_user  # Auth not required for memory endpoints (testing)
from memory.memory_manager import MemoryManager

router = APIRouter()


# ===== REQUEST/RESPONSE MODELS =====

class ConversationRequest(BaseModel):
    session_id: str
    query: str
    response: str
    user_id: Optional[str] = None  # Optional for testing without auth
    intent: Optional[str] = None
    entities: Optional[Dict[str, Any]] = None
    meta_info: Optional[Dict[str, Any]] = None


class BusinessContextRequest(BaseModel):
    context_type: str  # invoice_insights, gst_summary, customer_pattern
    context_key: str
    data: Dict[str, Any]
    summary: Optional[str] = None
    confidence_score: int = 100
    expires_in_days: Optional[int] = None


class PreferencesUpdate(BaseModel):
    default_language: Optional[str] = None
    notification_settings: Optional[Dict[str, Any]] = None
    dashboard_layout: Optional[Dict[str, Any]] = None
    ai_settings: Optional[Dict[str, Any]] = None


class ConversationResponse(BaseModel):
    id: str
    query: str
    response: str
    intent: Optional[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class BusinessContextResponse(BaseModel):
    id: str
    context_type: str
    context_key: str
    data: Dict[str, Any]
    summary: Optional[str]
    confidence_score: int
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ===== CONVERSATION ENDPOINTS =====

@router.post("/conversation")
async def save_conversation(
    request: ConversationRequest,
    db: Session = Depends(get_db)
):
    """Save a conversation turn (auth optional for testing)"""
    try:
        memory = MemoryManager(db)
        
        # Get or create test user if user_id not provided
        if not request.user_id:
            from models.user import User
            user = db.query(User).first()
            if not user:
                # Create test user
                from core.security import hash_password
                user = User(
                    email="test@smartbiz.ai",
                    hashed_password=hash_password("test123"),
                    full_name="Test User"
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            user_id = str(user.id)
        else:
            # Validate UUID format
            import uuid
            try:
                uuid.UUID(request.user_id)
                user_id = request.user_id
            except ValueError:
                # Invalid UUID, get first user
                from models.user import User
                user = db.query(User).first()
                if not user:
                    raise HTTPException(status_code=400, detail="No users found. Please create a user first.")
                user_id = str(user.id)
        
        conversation = memory.save_conversation(
            user_id=user_id,
            session_id=request.session_id,
            query=request.query,
            response=request.response,
            intent=request.intent or "",
            entities=request.entities or {},
            meta_info=request.meta_info or {}
        )
        
        # Track pattern
        if request.intent:
            memory.track_query_pattern(
                user_id=user_id,
                query=request.query,
                intent=request.intent
            )
        
        return {
            "id": str(conversation.id),
            "session_id": conversation.session_id,
            "user_id": user_id,
            "message": "✅ Conversation saved successfully!",
            "created_at": conversation.created_at.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving conversation: {str(e)}")


@router.get("/conversation/session/{session_id}")
async def get_session_history(
    session_id: str,
    limit: int = 20,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get conversation history for a session (auth optional)"""
    memory = MemoryManager(db)
    
    # Get user_id from query param or use first user
    if not user_id:
        from models.user import User
        user = db.query(User).first()
        if not user:
            raise HTTPException(status_code=404, detail="No users found")
        user_id = str(user.id)
    
    conversations = memory.get_session_history(
        user_id=user_id,
        session_id=session_id,
        limit=limit
    )
    
    return {
        "message": f"✅ Retrieved {len(conversations)} conversation(s) from session {session_id}",
        "session_id": session_id,
        "count": len(conversations),
        "conversations": [
            {
                "id": str(c.id),
                "query": c.query,
                "response": c.response,
                "intent": c.intent,
                "created_at": c.created_at.isoformat()
            }
            for c in reversed(conversations)
        ]
    }


@router.get("/conversation/recent")
async def get_recent_conversations(
    limit: int = 10,
    days: int = 7,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get recent conversations across all sessions (auth optional)"""
    memory = MemoryManager(db)
    
    # Get user_id from query param or use first user
    if not user_id:
        from models.user import User
        user = db.query(User).first()
        if not user:
            raise HTTPException(status_code=404, detail="No users found")
        user_id = str(user.id)
    
    conversations = memory.get_recent_conversations(
        user_id=user_id,
        limit=limit,
        days=days
    )
    
    return {
        "message": f"✅ Retrieved {len(conversations)} recent conversation(s) from last {days} days",
        "count": len(conversations),
        "conversations": [
            {
                "id": str(c.id),
                "session_id": c.session_id,
                "query": c.query,
                "response": c.response,
                "intent": c.intent,
                "created_at": c.created_at.isoformat()
            }
            for c in conversations
        ]
    }


@router.get("/conversation/search")
async def search_conversations(
    keyword: str,
    intent: Optional[str] = None,
    limit: int = 20,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Search conversations by keyword (auth optional)"""
    memory = MemoryManager(db)
    
    # Get user_id from query param or use first user
    if not user_id:
        from models.user import User
        user = db.query(User).first()
        if not user:
            raise HTTPException(status_code=404, detail="No users found")
        user_id = str(user.id)
    
    conversations = memory.search_conversations(
        user_id=user_id,
        keyword=keyword,
        intent=intent,
        limit=limit
    )
    
    return {
        "message": f"✅ Found {len(conversations)} conversation(s) matching '{keyword}'",
        "keyword": keyword,
        "intent": intent,
        "count": len(conversations),
        "results": [
            {
                "id": str(c.id),
                "session_id": c.session_id,
                "query": c.query,
                "response": c.response[:200],  # Truncate
                "intent": c.intent,
                "created_at": c.created_at.isoformat()
            }
            for c in conversations
        ]
    }


# ===== BUSINESS CONTEXT ENDPOINTS =====

@router.post("/context")
async def save_business_context(
    request: BusinessContextRequest,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Save or update business context/insights (auth optional)"""
    memory = MemoryManager(db)
    
    # Resolve user_id
    if not user_id:
        from models.user import User
        user = db.query(User).first()
        if not user:
            raise HTTPException(status_code=404, detail="No users found")
        user_id = str(user.id)
    
    context = memory.save_business_context(
        user_id=user_id,
        context_type=request.context_type,
        context_key=request.context_key,
        data=request.data,
        summary=request.summary,
        confidence_score=request.confidence_score,
        expires_in_days=request.expires_in_days
    )
    
    return {
        "message": f"✅ Business context '{request.context_type}' saved successfully!",
        "id": str(context.id),
        "context_type": context.context_type,
        "context_key": context.context_key,
        "updated_at": context.updated_at.isoformat()
    }


@router.get("/context/{context_type}")
async def get_business_context(
    context_type: str,
    context_key: Optional[str] = None,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get specific business context (auth optional)"""
    memory = MemoryManager(db)
    
    if not user_id:
        from models.user import User
        user = db.query(User).first()
        if not user:
            raise HTTPException(status_code=404, detail="No users found")
        user_id = str(user.id)
    
    context = memory.get_business_context(
        user_id=user_id,
        context_type=context_type,
        context_key=context_key
    )
    
    if not context:
        raise HTTPException(status_code=404, detail="Context not found")
    
    return {
        "message": f"✅ Retrieved business context '{context_type}'",
        "id": str(context.id),
        "context_type": context.context_type,
        "context_key": context.context_key,
        "data": context.data,
        "summary": context.summary,
        "confidence_score": context.confidence_score,
        "updated_at": context.updated_at.isoformat()
    }


@router.get("/context")
async def get_all_contexts(
    context_type: Optional[str] = None,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all business contexts (auth optional)"""
    memory = MemoryManager(db)
    
    if not user_id:
        from models.user import User
        user = db.query(User).first()
        if not user:
            raise HTTPException(status_code=404, detail="No users found")
        user_id = str(user.id)
    
    contexts = memory.get_all_contexts(
        user_id=user_id,
        context_type=context_type
    )
    
    return {
        "message": f"✅ Retrieved {len(contexts)} business context(s)",
        "count": len(contexts),
        "contexts": [
            {
                "id": str(c.id),
                "context_type": c.context_type,
                "context_key": c.context_key,
                "summary": c.summary,
                "confidence_score": c.confidence_score,
                "updated_at": c.updated_at.isoformat()
            }
            for c in contexts
        ]
    }


# ===== PREFERENCES ENDPOINTS =====

@router.get("/preferences")
async def get_preferences(
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get user preferences (auth optional)"""
    memory = MemoryManager(db)
    if not user_id:
        from models.user import User
        user = db.query(User).first()
        if not user:
            raise HTTPException(status_code=404, detail="No users found")
        user_id = str(user.id)
    prefs = memory.get_preferences(user_id)
    
    return {
        "message": "✅ User preferences retrieved successfully!",
        "default_language": prefs.default_language,
        "notification_settings": prefs.notification_settings,
        "dashboard_layout": prefs.dashboard_layout,
        "ai_settings": prefs.ai_settings,
        "frequent_queries": prefs.frequent_queries[-10:] if prefs.frequent_queries else [],
        "preferred_topics": prefs.preferred_topics,
        "active_hours": prefs.active_hours
    }


@router.put("/preferences")
async def update_preferences(
    request: PreferencesUpdate,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Update user preferences (auth optional)"""
    memory = MemoryManager(db)
    if not user_id:
        from models.user import User
        user = db.query(User).first()
        if not user:
            raise HTTPException(status_code=404, detail="No users found")
        user_id = str(user.id)
    
    update_data = request.dict(exclude_unset=True)
    prefs = memory.update_preferences(user_id, **update_data)
    
    return {
        "message": "✅ Preferences updated successfully!",
        "default_language": prefs.default_language,
        "updated_at": prefs.updated_at.isoformat()
    }


# ===== UTILITY ENDPOINTS =====

@router.get("/summary")
async def get_memory_summary(
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get summary of user's memory state (auth optional)"""
    memory = MemoryManager(db)
    if not user_id:
        from models.user import User
        user = db.query(User).first()
        if not user:
            raise HTTPException(status_code=404, detail="No users found")
        user_id = str(user.id)
    summary = memory.get_context_summary(user_id)
    return {
        "message": "✅ Memory summary generated successfully!",
        **summary
    }


@router.delete("/conversation/session/{session_id}")
async def clear_session(
    session_id: str,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Clear conversation memory for a session (auth optional)"""
    memory = MemoryManager(db)
    if not user_id:
        from models.user import User
        user = db.query(User).first()
        if not user:
            raise HTTPException(status_code=404, detail="No users found")
        user_id = str(user.id)
    memory.clear_user_memory(
        user_id=user_id,
        session_id=session_id
    )
    return {"message": f"✅ Session {session_id} cleared successfully!"}


@router.delete("/conversation/all")
async def clear_all_conversations(
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Clear all conversation memory (auth optional)"""
    memory = MemoryManager(db)
    if not user_id:
        from models.user import User
        user = db.query(User).first()
        if not user:
            raise HTTPException(status_code=404, detail="No users found")
        user_id = str(user.id)
    memory.clear_user_memory(user_id=user_id)
    return {"message": "✅ All conversations cleared successfully!"}


@router.post("/cleanup")
async def cleanup_expired(
    db: Session = Depends(get_db)
):
    """Cleanup expired contexts (admin/scheduled task)"""
    memory = MemoryManager(db)
    memory.cleanup_expired_contexts()
    return {"message": "✅ Expired contexts cleaned up successfully!"}
