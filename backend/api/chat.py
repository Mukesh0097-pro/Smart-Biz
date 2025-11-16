"""
AI Chat API routes - Main AI Co-Pilot Interface
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from core.database import get_db
from core.security import get_current_user, sanitize_input
from orchestrator.ai_orchestrator import AIOrchestrator
from memory.memory_manager import MemoryManager

router = APIRouter()

class ChatQuery(BaseModel):
    query: str
    session_id: Optional[str] = "default"
    language: Optional[str] = "en"

class ChatResponse(BaseModel):
    reply: str
    intent: Optional[str] = None
    entities: Optional[dict] = None
    context: Optional[dict] = None
    suggestions: Optional[list] = None
    tools_used: Optional[list] = None

# Initialize AI components
ai_orchestrator = AIOrchestrator()

@router.post("/query", response_model=ChatResponse)
async def handle_chat_query(
    chat_query: ChatQuery,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Main AI chat endpoint
    Processes natural language queries and routes to appropriate services
    """
    try:
        user_id = current_user["user_id"]
        query = sanitize_input(chat_query.query)
        
        # Initialize memory manager with db session
        memory = MemoryManager(db)
        
        # Get recent context
        recent = memory.get_recent_conversations(user_id, limit=5)
        context = {"recent_conversations": [{"query": c.query, "response": c.response} for c in recent]}
        
        # Classify intent and route to appropriate handler
        response = await ai_orchestrator.process_query(
            user_id=user_id,
            query=query,
            context=context,
            language=chat_query.language
        )
        
        # Extract answer from new response format
        answer = response.get("answer", "I'm sorry, I couldn't process that request.")
        intent = response.get("intent", "unknown")
        entities = response.get("entities", {})
        tools_used = response.get("tools_used", [])
        memory_to_save = response.get("memory_to_save", [])
        
        # Save conversation to memory
        memory.save_conversation(
            user_id=user_id,
            session_id=chat_query.session_id,
            query=query,
            response=answer,
            intent=intent,
            entities=entities
        )
        
        # Generate contextual suggestions based on intent
        suggestions = []
        if intent.startswith("invoice"):
            suggestions = ["Create a new invoice", "View recent invoices", "Check pending invoices"]
        elif intent.startswith("gst"):
            suggestions = ["Show GST summary", "File GST return", "Check compliance status"]
        elif intent.startswith("business"):
            suggestions = ["Show revenue trends", "Top customers", "Payment analysis"]
        else:
            suggestions = ["Create an invoice", "File GST", "Show my dashboard"]
        
        return ChatResponse(
            reply=answer,
            intent=intent,
            entities=entities,
            context={"memory_saved": len(memory_to_save) > 0},
            suggestions=suggestions,
            tools_used=tools_used
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.post("/clear-context")
async def clear_context(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clear user's conversation context"""
    user_id = current_user["user_id"]
    memory = MemoryManager(db)
    memory.clear_user_memory(user_id)
    return {"message": "Context cleared successfully"}

@router.get("/suggestions")
async def get_suggestions(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get contextual suggestions for user"""
    user_id = current_user["user_id"]
    memory = MemoryManager(db)
    prefs = memory.get_preferences(user_id)
    
    suggestions = [
        "Show me my invoices for this month",
        "Create a new invoice",
        "What's my total revenue?",
        "Help me file GST",
        "Add a new customer",
        "Show pending payments"
    ]
    
    return {"suggestions": suggestions, "preferred_topics": prefs.preferred_topics}
