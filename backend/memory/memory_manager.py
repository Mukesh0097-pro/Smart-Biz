"""
Memory Manager - Handles contextual memory using OpenMemory concept
"""

import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
from core.config import settings

class MemoryManager:
    """
    Manages user conversation context and memory
    Implements a simple file-based memory system (can be upgraded to OpenMemory)
    """
    
    def __init__(self, storage_path: str = None):
        self.storage_path = Path(storage_path or settings.MEMORY_STORE_PATH)
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def _get_user_memory_file(self, user_id: str) -> Path:
        """Get the memory file path for a user"""
        return self.storage_path / f"{user_id}.json"
    
    def get_context(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve conversation context for a user
        """
        memory_file = self._get_user_memory_file(user_id)
        
        if not memory_file.exists():
            return {
                "user_id": user_id,
                "conversations": [],
                "preferences": {},
                "last_updated": None
            }
        
        try:
            with open(memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading memory: {e}")
            return {
                "user_id": user_id,
                "conversations": [],
                "preferences": {},
                "last_updated": None
            }
    
    def update_context(
        self,
        user_id: str,
        query: str,
        response: str,
        metadata: Optional[Dict] = None
    ):
        """
        Update conversation context with new interaction
        """
        context = self.get_context(user_id)
        
        # Add new conversation entry
        conversation_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "response": response,
            "metadata": metadata or {}
        }
        
        context["conversations"].append(conversation_entry)
        
        # Keep only last 50 conversations to manage memory size
        if len(context["conversations"]) > 50:
            context["conversations"] = context["conversations"][-50:]
        
        context["last_updated"] = datetime.utcnow().isoformat()
        
        # Save to file
        self._save_context(user_id, context)
    
    def _save_context(self, user_id: str, context: Dict[str, Any]):
        """Save context to file"""
        memory_file = self._get_user_memory_file(user_id)
        
        try:
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(context, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def clear_context(self, user_id: str):
        """Clear all context for a user"""
        memory_file = self._get_user_memory_file(user_id)
        
        if memory_file.exists():
            memory_file.unlink()
    
    def get_recent_conversations(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get recent conversations"""
        context = self.get_context(user_id)
        conversations = context.get("conversations", [])
        return conversations[-limit:] if conversations else []
    
    def update_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Update user preferences in memory"""
        context = self.get_context(user_id)
        context["preferences"].update(preferences)
        context["last_updated"] = datetime.utcnow().isoformat()
        self._save_context(user_id, context)
    
    def get_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences from memory"""
        context = self.get_context(user_id)
        return context.get("preferences", {})
    
    def search_conversations(self, user_id: str, keyword: str) -> List[Dict]:
        """Search conversations by keyword"""
        context = self.get_context(user_id)
        conversations = context.get("conversations", [])
        
        results = []
        for conv in conversations:
            if keyword.lower() in conv["query"].lower() or keyword.lower() in conv["response"].lower():
                results.append(conv)
        
        return results
