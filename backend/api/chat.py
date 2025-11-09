"""
AI Chat API routes - Main AI Co-Pilot Interface
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.core.security import get_current_user, sanitize_input
from backend.orchestrator.ai_orchestrator import AIOrchestrator
from backend.memory.memory_manager import MemoryManager

router = APIRouter()

class ChatQuery(BaseModel):
    query: str
    session_id: Optional[str] = None
    language: Optional[str] = "en"

class ChatResponse(BaseModel):
    reply: str
    context: Optional[dict] = None
    suggestions: Optional[list] = None

# Initialize AI components
ai_orchestrator = AIOrchestrator()
memory_manager = MemoryManager()

@router.post("/query", response_model=ChatResponse)
async def handle_chat_query(
    chat_query: ChatQuery,
    current_user: dict = Depends(get_current_user)
):
    """
    Main AI chat endpoint
    Processes natural language queries and routes to appropriate services
    """
    try:
        user_id = current_user["user_id"]
        query = sanitize_input(chat_query.query)
        
        # Get user context from memory
        context = memory_manager.get_context(user_id)
        
        # Classify intent and route to appropriate handler
        response = await ai_orchestrator.process_query(
            user_id=user_id,
            query=query,
            context=context,
            language=chat_query.language
        )
        
        # Update memory with new interaction
        memory_manager.update_context(
            user_id=user_id,
            query=query,
            response=response["reply"]
        )
        
        return ChatResponse(
            reply=response["reply"],
            context=response.get("context"),
            suggestions=response.get("suggestions")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.post("/clear-context")
async def clear_context(current_user: dict = Depends(get_current_user)):
    """Clear user's conversation context"""
    user_id = current_user["user_id"]
    memory_manager.clear_context(user_id)
    return {"message": "Context cleared successfully"}

@router.get("/suggestions")
async def get_suggestions(current_user: dict = Depends(get_current_user)):
    """Get contextual suggestions for user"""
    user_id = current_user["user_id"]
    context = memory_manager.get_context(user_id)
    
    suggestions = [
        "Show me my invoices for this month",
        "Create a new invoice",
        "What's my total revenue?",
        "Help me file GST",
        "Add a new customer",
        "Show pending payments"
    ]
    
    return {"suggestions": suggestions}
