"""
AI Orchestrator - Routes queries to appropriate handlers
"""

from typing import Dict, Any, Optional
import logging
from openai import OpenAI
from core.config import settings

logger = logging.getLogger(__name__)

class AIOrchestrator:
    """
    Main AI orchestration layer
    Classifies intent and routes to appropriate service
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        
        # Intent classification mapping
        self.intent_handlers = {
            "invoice": self._handle_invoice_query,
            "gst": self._handle_gst_query,
            "customer": self._handle_customer_query,
            "analytics": self._handle_analytics_query,
            "general": self._handle_general_query
        }
    
    async def process_query(
        self,
        user_id: str,
        query: str,
        context: Optional[Dict] = None,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Process user query and return appropriate response
        """
        try:
            # Classify intent
            intent = await self._classify_intent(query)
            logger.info(f"Classified intent: {intent} for query: {query}")
            
            # Get handler
            handler = self.intent_handlers.get(intent, self._handle_general_query)
            
            # Process query
            response = await handler(user_id, query, context, language)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in AI orchestrator: {str(e)}")
            return {
                "reply": "I apologize, but I encountered an error processing your request. Please try again.",
                "error": str(e)
            }
    
    async def _classify_intent(self, query: str) -> str:
        """
        Classify user intent from query
        """
        query_lower = query.lower()
        
        # Simple keyword-based classification
        if any(word in query_lower for word in ["invoice", "bill", "billing"]):
            return "invoice"
        elif any(word in query_lower for word in ["gst", "tax", "filing"]):
            return "gst"
        elif any(word in query_lower for word in ["customer", "client", "vendor"]):
            return "customer"
        elif any(word in query_lower for word in ["revenue", "analytics", "insight", "report"]):
            return "analytics"
        else:
            return "general"
    
    async def _handle_invoice_query(
        self,
        user_id: str,
        query: str,
        context: Optional[Dict],
        language: str
    ) -> Dict[str, Any]:
        """Handle invoice-related queries"""
        return {
            "reply": "I can help you with invoices. You can create, view, or manage your invoices. What would you like to do?",
            "suggestions": [
                "Create a new invoice",
                "View recent invoices",
                "Check pending invoices"
            ]
        }
    
    async def _handle_gst_query(
        self,
        user_id: str,
        query: str,
        context: Optional[Dict],
        language: str
    ) -> Dict[str, Any]:
        """Handle GST-related queries"""
        return {
            "reply": "I can assist you with GST filing and compliance. What specific information do you need?",
            "suggestions": [
                "Show GST summary",
                "File GST return",
                "Check compliance status"
            ]
        }
    
    async def _handle_customer_query(
        self,
        user_id: str,
        query: str,
        context: Optional[Dict],
        language: str
    ) -> Dict[str, Any]:
        """Handle customer-related queries"""
        return {
            "reply": "I can help you manage your customers and vendors. What would you like to do?",
            "suggestions": [
                "Add a new customer",
                "View customer list",
                "Update customer details"
            ]
        }
    
    async def _handle_analytics_query(
        self,
        user_id: str,
        query: str,
        context: Optional[Dict],
        language: str
    ) -> Dict[str, Any]:
        """Handle analytics and insights queries"""
        return {
            "reply": "I can provide business insights and analytics. Here's what I found:",
            "suggestions": [
                "Show revenue trends",
                "Top customers",
                "Payment analysis"
            ]
        }
    
    async def _handle_general_query(
        self,
        user_id: str,
        query: str,
        context: Optional[Dict],
        language: str
    ) -> Dict[str, Any]:
        """Handle general queries"""
        
        if not self.client:
            return {
                "reply": "I'm here to help you manage your business! You can ask me about invoices, GST filing, customers, and business insights.",
                "suggestions": [
                    "Create an invoice",
                    "File GST",
                    "Show my dashboard"
                ]
            }
        
        # Use OpenAI for general conversation
        try:
            prompt = f"Context: {context}\nUser Query: {query}\nRespond as a helpful MSME business assistant."
            
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are SmartBiz AI, a helpful assistant for Indian MSME businesses. Help with invoicing, GST, compliance, and business insights."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            
            reply = response.choices[0].message.content
            
            return {
                "reply": reply,
                "suggestions": [
                    "Tell me more",
                    "Show me an example",
                    "What else can you do?"
                ]
            }
            
        except Exception as e:
            logger.error(f"OpenAI error: {str(e)}")
            return {
                "reply": "I'm SmartBiz AI, your business co-pilot. I can help with invoices, GST filing, customer management, and business insights. How can I assist you today?",
                "suggestions": [
                    "Create an invoice",
                    "View dashboard",
                    "File GST"
                ]
            }
