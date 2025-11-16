"""
SmartBiz AI Orchestrator - MSME Automation Assistant
Handles intent classification, entity extraction, tool routing, and memory management
"""

from typing import Dict, Any, Optional, List
import logging
import re
from datetime import datetime
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    Groq = None
from core.config import settings

logger = logging.getLogger(__name__)

class AIOrchestrator:
    """
    SmartBiz AI - MSME Automation Assistant
    
    Core responsibilities:
    1. Understand query → classify intent + extract entities
    2. Decide pipeline → chat, GST, invoicing, government APIs, insights
    3. Call tools only when necessary
    4. Generate final structured response
    """
    
    def __init__(self):
        # Initialize Groq client for Llama 3.1 8B
        if GROQ_AVAILABLE and settings.GROQ_API_KEY:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            self.model = settings.GROQ_MODEL
            logger.info(f"✅ Groq client initialized with model: {self.model}")
        else:
            self.client = None
            self.model = None
            logger.warning("⚠️ Groq not available. Install with: pip install groq")
        
        # Intent categories
        self.intents = {
            "chat.general": ["hello", "hi", "help", "how", "what", "explain", "tell me"],
            "invoice.create": ["create invoice", "new invoice", "generate invoice", "make invoice", "bill"],
            "invoice.view": ["show invoice", "view invoice", "get invoice", "invoice details", "invoice status"],
            "gst.verify": ["check gst", "verify gst", "gst details", "gst number", "validate gst"],
            "gst.return": ["gst return", "file gst", "gst filing", "gst summary", "tax return"],
            "gov.udyam": ["udyam", "msme certificate", "udyam number", "udyam registration"],
            "gov.egov": ["digilocker", "certificate", "document", "pan", "aadhaar"],
            "business.summary": ["summary", "report", "analytics", "insights", "dashboard", "revenue", "sales"],
            "task.update": ["update", "change", "set", "preference", "language", "profile"]
        }
        
        # Tool mapping
        self.tool_routes = {
            "gst.verify": "gst_service.verify",
            "gst.return": "gst_service.filing",
            "invoice.create": "invoice_service.create",
            "invoice.view": "invoice_service.fetch",
            "gov.udyam": "udyam_service.verify",
            "gov.egov": "digilocker_service.fetch",
            "business.summary": "analytics_service.generate"
        }
    
    async def process_query(
        self,
        user_id: str,
        query: str,
        context: Optional[Dict] = None,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Main orchestration pipeline
        
        Steps:
        1. Classify intent
        2. Extract entities
        3. Check memory for relevant info
        4. Decide pipeline
        5. Execute tools if needed
        6. Generate final response
        7. Propose memory entries
        8. Return structured JSON
        """
        try:
            # Step 1: Classify intent
            intent = await self._classify_intent(query)
            logger.info(f"🎯 Intent: {intent} | Query: {query}")
            
            # Step 2: Extract entities
            entities = await self._extract_entities(query, intent)
            logger.info(f"🧩 Entities: {entities}")
            
            # Step 3: Check memory for context (placeholder - integrate with MemoryManager)
            memory_context = await self._fetch_relevant_memory(user_id, intent, entities)
            
            # Step 4: Decide pipeline and execute
            tools_used = []
            tool_results = {}
            
            if intent in self.tool_routes:
                # Execute tool
                tool_name = self.tool_routes[intent]
                tool_results = await self._execute_tool(tool_name, entities, user_id)
                tools_used.append(tool_name)
                logger.info(f"⚙️ Tool executed: {tool_name}")
            
            # Step 5: Generate final answer
            answer = await self._generate_answer(query, intent, entities, tool_results, memory_context, language)
            
            # Step 6: Propose memory entries
            memory_to_save = await self._propose_memory(intent, entities, tool_results)
            
            # Step 7: Return structured response
            response = {
                "answer": answer,
                "intent": intent,
                "entities": entities,
                "tools_used": tools_used,
                "memory_to_save": memory_to_save
            }
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Error in AI orchestrator: {str(e)}")
            return {
                "answer": "I apologize, but I encountered an error processing your request. Please try again.",
                "intent": "unknown",
                "entities": {},
                "tools_used": [],
                "memory_to_save": [],
                "error": str(e)
            }
    
    
    async def _classify_intent(self, query: str) -> str:
        """
        Classify user intent using keyword matching
        
        Returns one of:
        - chat.general, invoice.create, invoice.view
        - gst.verify, gst.return
        - gov.udyam, gov.egov
        - business.summary, task.update
        - unknown
        """
        query_lower = query.lower()
        
        # Match against intent keywords
        for intent, keywords in self.intents.items():
            if any(keyword in query_lower for keyword in keywords):
                return intent
        
        return "unknown"
    
    async def _extract_entities(self, query: str, intent: str) -> Dict[str, Any]:
        """
        Extract structured entities from query
        
        Never hallucinate - extract ONLY what is present:
        - GST number (15 chars: 2 digits + 5 letters + 4 digits + 1 letter + 1 alphanumeric + Z + 1 alphanumeric)
        - Invoice fields (buyer, items, amount, GST %, date)
        - Business name
        - Udyam number
        - Document types
        - Date ranges
        - Language preference
        """
        entities = {}
        query_lower = query.lower()
        
        # Extract GST number (pattern: 29ABCDE1234F1Z5)
        gst_pattern = r'\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z0-9]{1}Z[A-Z0-9]{1}\b'
        gst_match = re.search(gst_pattern, query.upper())
        if gst_match:
            entities["gst_number"] = gst_match.group(0)
        
        # Extract Udyam number (pattern: UDYAM-XX-00-0000000)
        udyam_pattern = r'UDYAM-[A-Z]{2}-\d{2}-\d{7}'
        udyam_match = re.search(udyam_pattern, query.upper())
        if udyam_match:
            entities["udyam_number"] = udyam_match.group(0)
        
        # Extract invoice ID (pattern: INV-12345 or #12345)
        invoice_pattern = r'(?:INV-|#)(\d+)'
        invoice_match = re.search(invoice_pattern, query.upper())
        if invoice_match:
            entities["invoice_id"] = invoice_match.group(1)
        
        # Extract amount (₹5000 or Rs. 5000 or 5000 rupees)
        amount_pattern = r'(?:₹|Rs\.?|INR)\s*(\d+(?:,\d+)*(?:\.\d+)?)'
        amount_match = re.search(amount_pattern, query, re.IGNORECASE)
        if amount_match:
            entities["amount"] = float(amount_match.group(1).replace(',', ''))
        elif re.search(r'(\d+(?:,\d+)*(?:\.\d+)?)\s*rupees?', query_lower):
            amt_match = re.search(r'(\d+(?:,\d+)*(?:\.\d+)?)\s*rupees?', query_lower)
            entities["amount"] = float(amt_match.group(1).replace(',', ''))
        
        # Extract customer/buyer name (after "for" or "to")
        if " for " in query_lower or " to " in query_lower:
            name_pattern = r'(?:for|to)\s+([A-Z][a-zA-Z\s]{2,30})(?:\s|$|,|\.|;)'
            name_match = re.search(name_pattern, query, re.IGNORECASE)
            if name_match:
                entities["customer_name"] = name_match.group(1).strip()
        
        # Extract business name (after "company" or "business")
        business_pattern = r'(?:company|business|firm)\s+(?:name\s+)?(?:is\s+)?([A-Z][a-zA-Z\s&]{2,50})'
        business_match = re.search(business_pattern, query, re.IGNORECASE)
        if business_match:
            entities["business_name"] = business_match.group(1).strip()
        
        # Extract months
        months = ["january", "february", "march", "april", "may", "june",
                  "july", "august", "september", "october", "november", "december"]
        for month in months:
            if month in query_lower:
                entities["month"] = month.capitalize()
                break
        
        # Extract date (DD/MM/YYYY or DD-MM-YYYY or YYYY-MM-DD)
        date_pattern = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b'
        date_match = re.search(date_pattern, query)
        if date_match:
            entities["date"] = date_match.group(1)
        
        # Extract language preference
        languages = ["english", "hindi", "tamil", "telugu", "kannada", "malayalam", "bengali", "marathi", "gujarati"]
        for lang in languages:
            if lang in query_lower:
                entities["language"] = lang.capitalize()
                break
        
        # Extract document types
        doc_types = ["pan", "aadhaar", "gst certificate", "udyam certificate", "msme certificate"]
        for doc in doc_types:
            if doc in query_lower:
                entities["document_type"] = doc.upper() if len(doc) <= 4 else doc.title()
                break
        
        return entities
    
    async def _fetch_relevant_memory(self, user_id: str, intent: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch relevant memory context for the query
        
        TODO: Integrate with MemoryManager
        - Previous conversations
        - User preferences (language, business name, formats)
        - Previous invoices or GST checks
        - Known entities about user context
        """
        # Placeholder - will integrate with memory/memory_manager.py
        return {
            "previous_context": None,
            "user_preferences": {},
            "business_data": {}
        }
    
    async def _execute_tool(self, tool_name: str, entities: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Execute the appropriate tool based on routing
        
        Tools:
        - gst_service.verify → GST API
        - invoice_service.create → Invoicing API
        - invoice_service.fetch → Get invoices
        - udyam_service.verify → Udyam API
        - digilocker_service.fetch → DigiLocker API
        - analytics_service.generate → Business insights
        
        Returns tool result or error
        """
        from models.invoice import Invoice
        from models.customer import Customer
        from datetime import datetime, timedelta
        from core.database import SessionLocal
        
        logger.info(f"🔧 Executing tool: {tool_name} with entities: {entities}")
        
        db = SessionLocal()
        
        try:
            # Invoice creation - ACTUALLY CREATE THE INVOICE
            if tool_name == "invoice_service.create":
                customer_name = entities.get("customer_name")
                amount = entities.get("amount", 0)
                
                if not customer_name or not amount:
                    return {
                        "status": "error",
                        "message": "Please provide customer name and amount. Example: 'Create invoice for ABC Corp worth ₹5000'"
                    }
                
                # Find or create customer
                customer = db.query(Customer).filter(
                    Customer.user_id == user_id,
                    Customer.name.ilike(f"%{customer_name}%")
                ).first()
                
                if not customer:
                    # Create new customer
                    customer = Customer(
                        user_id=user_id,
                        name=customer_name,
                        customer_type="regular"
                    )
                    db.add(customer)
                    db.commit()
                    db.refresh(customer)
                
                # Generate invoice number
                invoice_count = db.query(Invoice).filter(Invoice.user_id == user_id).count()
                invoice_number = f"INV-{datetime.now().year}-{invoice_count + 1:04d}"
                
                # Create invoice with single item
                invoice = Invoice(
                    invoice_number=invoice_number,
                    user_id=user_id,
                    customer_id=customer.id,
                    due_date=datetime.now() + timedelta(days=30),
                    items=[{
                        "name": "Service/Product",
                        "quantity": 1,
                        "rate": float(amount),
                        "amount": float(amount)
                    }],
                    subtotal=float(amount),
                    tax_amount=float(amount) * 0.18,  # 18% GST
                    total_amount=float(amount) * 1.18,
                    gst_rate=18.0,
                    status="DRAFT"
                )
                
                db.add(invoice)
                db.commit()
                db.refresh(invoice)
                
                # Generate PDF
                pdf_path = None
                try:
                    from services.invoice_generator import InvoiceGenerator
                    from models.user import User
                    
                    # Get user details
                    user = db.query(User).filter(User.id == user_id).first()
                    
                    # Prepare data for PDF
                    invoice_data = {
                        'invoice_number': invoice.invoice_number,
                        'created_at': invoice.created_at.strftime('%d-%b-%Y'),
                        'due_date': invoice.due_date.strftime('%d-%b-%Y'),
                        'status': invoice.status,
                        'items': invoice.items,
                        'subtotal': invoice.subtotal,
                        'tax_amount': invoice.tax_amount,
                        'total_amount': invoice.total_amount,
                        'gst_rate': invoice.gst_rate,
                        'notes': invoice.notes or 'Payment terms: Net 30 days'
                    }
                    
                    user_data = {
                        'full_name': user.full_name if user else 'Your Business',
                        'email': user.email if user else '',
                        'business_name': user.full_name if user else 'Your Business'
                    }
                    
                    customer_data = {
                        'name': customer.name,
                        'email': customer.email or '',
                        'phone': customer.phone or '',
                        'gst_number': customer.gst_number,
                        'billing_address': customer.billing_address
                    }
                    
                    # Generate PDF
                    generator = InvoiceGenerator()
                    pdf_path = generator.generate_pdf(invoice_data, user_data, customer_data)
                    logger.info(f"📄 PDF generated: {pdf_path}")
                    
                except Exception as pdf_error:
                    logger.error(f"PDF generation error: {str(pdf_error)}")
                    # Continue without PDF if generation fails
                
                return {
                    "status": "success",
                    "message": f"Invoice {invoice_number} created successfully!",
                    "data": {
                        "invoice_id": str(invoice.id),
                        "invoice_number": invoice_number,
                        "customer_name": customer.name,
                        "amount": float(amount),
                        "total_with_tax": float(amount) * 1.18,
                        "due_date": invoice.due_date.strftime("%Y-%m-%d"),
                        "pdf_path": pdf_path
                    }
                }
            
            # Invoice fetch - GET ACTUAL INVOICES FROM DB
            elif tool_name == "invoice_service.fetch":
                invoice_id = entities.get("invoice_id")
                month = entities.get("month")
                
                query = db.query(Invoice).filter(Invoice.user_id == user_id)
                
                # Filter by month if provided
                if month:
                    month_num = {
                        "january": 1, "february": 2, "march": 3, "april": 4,
                        "may": 5, "june": 6, "july": 7, "august": 8,
                        "september": 9, "october": 10, "november": 11, "december": 12
                    }.get(month.lower())
                    
                    if month_num:
                        from sqlalchemy import extract
                        query = query.filter(extract('month', Invoice.created_at) == month_num)
                
                # Filter by invoice_id if provided
                if invoice_id:
                    query = query.filter(Invoice.id == invoice_id)
                
                invoices = query.order_by(Invoice.created_at.desc()).limit(10).all()
                
                invoice_list = []
                total_amount = 0
                
                for inv in invoices:
                    invoice_list.append({
                        "invoice_number": inv.invoice_number,
                        "amount": inv.total_amount,
                        "status": inv.status,
                        "date": inv.created_at.strftime("%Y-%m-%d")
                    })
                    total_amount += inv.total_amount
                
                return {
                    "status": "success",
                    "message": f"Found {len(invoices)} invoice(s)",
                    "data": {
                        "count": len(invoices),
                        "invoices": invoice_list,
                        "total_amount": total_amount,
                        "month": month
                    }
                }
            
            # GST verification
            elif tool_name == "gst_service.verify":
                gst_number = entities.get("gst_number")
                
                if not gst_number:
                    return {
                        "status": "error",
                        "message": "Please provide a valid GST number (15 characters). Example: 29ABCDE1234F1Z5"
                    }
                
                return {
                    "status": "success",
                    "message": f"GST verification initiated for {gst_number}",
                    "data": {
                        "gst_number": gst_number,
                        "note": "GST API integration pending - will verify with government database"
                    }
                }
            
            # GST filing
            elif tool_name == "gst_service.filing":
                month = entities.get("month")
                
                # Get invoices for GST calculation
                query = db.query(Invoice).filter(Invoice.user_id == user_id)
                
                if month:
                    month_num = {
                        "january": 1, "february": 2, "march": 3, "april": 4,
                        "may": 5, "june": 6, "july": 7, "august": 8,
                        "september": 9, "october": 10, "november": 11, "december": 12
                    }.get(month.lower())
                    
                    if month_num:
                        from sqlalchemy import extract
                        query = query.filter(extract('month', Invoice.created_at) == month_num)
                
                invoices = query.all()
                total_sales = sum(inv.subtotal for inv in invoices)
                total_gst = sum(inv.tax_amount for inv in invoices)
                
                return {
                    "status": "success",
                    "message": f"GST summary prepared{' for ' + month if month else ''}",
                    "data": {
                        "month": month,
                        "total_invoices": len(invoices),
                        "total_sales": total_sales,
                        "total_gst_collected": total_gst,
                        "note": "GST filing API integration pending"
                    }
                }
            
            # Udyam verification
            elif tool_name == "udyam_service.verify":
                udyam_number = entities.get("udyam_number")
                
                if not udyam_number:
                    return {
                        "status": "error",
                        "message": "Please provide Udyam number. Format: UDYAM-XX-00-0000000"
                    }
                
                return {
                    "status": "success",
                    "message": f"Verifying Udyam number: {udyam_number}",
                    "data": {
                        "udyam_number": udyam_number,
                        "note": "Udyam API integration pending"
                    }
                }
            
            # Analytics - REAL DATA FROM DB
            elif tool_name == "analytics_service.generate":
                month = entities.get("month")
                
                # Get invoices
                query = db.query(Invoice).filter(Invoice.user_id == user_id)
                
                if month:
                    month_num = {
                        "january": 1, "february": 2, "march": 3, "april": 4,
                        "may": 5, "june": 6, "july": 7, "august": 8,
                        "september": 9, "october": 10, "november": 11, "december": 12
                    }.get(month.lower())
                    
                    if month_num:
                        from sqlalchemy import extract
                        query = query.filter(extract('month', Invoice.created_at) == month_num)
                
                invoices = query.all()
                
                # Calculate metrics
                total_revenue = sum(inv.total_amount for inv in invoices)
                total_invoices = len(invoices)
                paid_invoices = len([inv for inv in invoices if inv.status == "PAID"])
                pending_invoices = len([inv for inv in invoices if inv.status in ["DRAFT", "SENT"]])
                
                # Get customer count
                customer_count = db.query(Customer).filter(Customer.user_id == user_id).count()
                
                return {
                    "status": "success",
                    "message": f"Business analytics generated{' for ' + month if month else ''}",
                    "data": {
                        "month": month or "all time",
                        "total_revenue": total_revenue,
                        "total_invoices": total_invoices,
                        "paid_invoices": paid_invoices,
                        "pending_invoices": pending_invoices,
                        "total_customers": customer_count
                    }
                }
            
            # DigiLocker
            elif tool_name == "digilocker_service.fetch":
                doc_type = entities.get("document_type", "document")
                
                return {
                    "status": "success",
                    "message": f"Fetching {doc_type} from DigiLocker",
                    "data": {
                        "document_type": doc_type,
                        "note": "DigiLocker API integration pending"
                    }
                }
            
            else:
                return {
                    "status": "pending",
                    "message": f"Service {tool_name} is being implemented. Feature coming soon!",
                    "data": {}
                }
                
        except Exception as e:
            logger.error(f"Tool execution error: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "message": f"Error executing tool: {str(e)}",
                "data": {}
            }
        finally:
            db.close()
    
    async def _generate_answer(
        self,
        query: str,
        intent: str,
        entities: Dict[str, Any],
        tool_results: Dict[str, Any],
        memory_context: Dict[str, Any],
        language: str
    ) -> str:
        """
        Generate final user-friendly answer
        
        Rules:
        - Simple, business-friendly, confident
        - Use bullet points when possible
        - Avoid long paragraphs
        - Give next steps if relevant
        - Never hallucinate data
        - If tool failed, say so gracefully
        """
        
        # If tool was used, summarize its result
        if tool_results and tool_results.get("status") == "success":
            result_message = tool_results.get("message", "")
            result_data = tool_results.get("data", {})
            
            if intent == "gst.verify":
                gst_num = entities.get('gst_number', 'N/A')
                note = result_data.get("note", "")
                return f"✅ **GST Verification Request**\n\n**GST Number:** {gst_num}\n\n{note}\n\n**What happens next:**\n• Verification with government database\n• Business details retrieval\n• Compliance status check\n\nNote: Full GST API integration coming soon!"
            
            elif intent == "invoice.create":
                invoice_num = result_data.get('invoice_number', 'N/A')
                customer = result_data.get('customer_name', 'customer')
                amount = result_data.get('amount', 0)
                total = result_data.get('total_with_tax', 0)
                due_date = result_data.get('due_date', 'N/A')
                pdf_path = result_data.get('pdf_path')
                
                pdf_info = f"\n**PDF Generated:** ✅ {pdf_path}" if pdf_path else "\n**PDF:** Available in invoices folder"
                
                return f"✅ **Invoice Created Successfully!**\n\n**Invoice Number:** {invoice_num}\n**Customer:** {customer}\n**Amount:** ₹{amount:,.2f}\n**GST (18%):** ₹{(total - amount):,.2f}\n**Total:** ₹{total:,.2f}\n**Due Date:** {due_date}{pdf_info}\n\n**Next steps:**\n• Download PDF from invoices folder\n• Send to customer via email\n• Track payment status\n• View in Invoices page"
            
            elif intent == "invoice.view":
                count = result_data.get('count', 0)
                invoices = result_data.get('invoices', [])
                total_amt = result_data.get('total_amount', 0)
                month = result_data.get('month')
                
                if count == 0:
                    return f"📄 **No Invoices Found**\n\n{f'No invoices found for {month}.' if month else 'You havent created any invoices yet.'}\n\n**Get started:**\n• Create your first invoice\n• Import existing invoices\n• Set up customers"
                
                invoice_list = "\n".join([f"• {inv['invoice_number']} - ₹{inv['amount']:,.2f} ({inv['status']}) - {inv['date']}" for inv in invoices[:5]])
                
                return f"📄 **Invoice Summary{' - ' + month.title() if month else ''}**\n\n**Total Invoices:** {count}\n**Total Amount:** ₹{total_amt:,.2f}\n\n**Recent Invoices:**\n{invoice_list}\n\n{f'View all {count} invoices in the Invoices page.' if count > 5 else ''}"
            
            elif intent == "gst.return":
                month = result_data.get('month', 'this period')
                total_invoices = result_data.get('total_invoices', 0)
                total_sales = result_data.get('total_sales', 0)
                total_gst = result_data.get('total_gst_collected', 0)
                
                return f"📝 **GST Return Summary{' - ' + month.title() if month else ''}**\n\n**Total Invoices:** {total_invoices}\n**Total Sales:** ₹{total_sales:,.2f}\n**GST Collected:** ₹{total_gst:,.2f}\n\n**Filing process:**\n1. Review all invoices ✅\n2. Calculate tax liability ✅\n3. Prepare GSTR forms (pending)\n4. Submit to GSTN (pending)\n\nNote: GST filing API integration in progress!"
            
            elif intent == "business.summary":
                month = result_data.get('month', 'all time')
                revenue = result_data.get('total_revenue', 0)
                total_inv = result_data.get('total_invoices', 0)
                paid = result_data.get('paid_invoices', 0)
                pending = result_data.get('pending_invoices', 0)
                customers = result_data.get('total_customers', 0)
                
                return f"📊 **Business Analytics - {month.title()}**\n\n**Revenue:** ₹{revenue:,.2f}\n**Invoices:** {total_inv} total\n• Paid: {paid}\n• Pending: {pending}\n**Customers:** {customers}\n\n**Insights:**\n• Payment rate: {(paid/total_inv*100 if total_inv > 0 else 0):.1f}%\n• Avg invoice value: ₹{(revenue/total_inv if total_inv > 0 else 0):,.2f}\n\nView detailed analytics in Dashboard!"
            
            elif intent == "gov.udyam":
                udyam_num = result_data.get('udyam_number', 'N/A')
                note = result_data.get('note', '')
                return f"🏢 **Udyam Verification**\n\n**Udyam Number:** {udyam_num}\n\n{note}\n\n**Verification includes:**\n• MSME certificate validity\n• Business classification\n• Enterprise type\n• Registration status\n\nFull integration coming soon!"
            
            elif intent == "gov.egov":
                doc_type = result_data.get('document_type', 'document')
                note = result_data.get('note', '')
                return f"📁 **DigiLocker Document Fetch**\n\n**Document:** {doc_type}\n\n{note}\n\n**Available documents:**\n• PAN Card\n• Aadhaar\n• GST Certificate\n• MSME/Udyam Certificate\n• Driving License\n\nDigiLocker integration in development!"
        
        # Handle error responses from tools
        if tool_results and tool_results.get("status") == "error":
            error_msg = tool_results.get("message", "An error occurred")
            return f"❌ **Error**\n\n{error_msg}\n\nPlease check your input and try again."
        
        # Intent-based responses when no tool is used
        if intent == "chat.general":
            return self._get_general_response(query, language)
        
        elif intent == "gst.return":
            return "📝 GST Return Filing\n\nI can help you file your GST return. Please provide:\n• Filing period (month/quarter)\n• Confirm your GSTIN\n• Review transactions\n\nShould I proceed?"
        
        elif intent == "gov.udyam":
            if entities.get("udyam_number"):
                return f"🔍 Verifying Udyam number: {entities['udyam_number']}\n\nPlease wait while I fetch your MSME certificate details..."
            else:
                return "🏢 Udyam Registration\n\nI can help you:\n• Verify existing Udyam number\n• Check MSME certificate status\n• Understand registration benefits\n\nPlease share your Udyam number or ask a specific question."
        
        elif intent == "gov.egov":
            doc_type = entities.get("document_type", "document")
            return f"📁 DigiLocker Integration\n\nFetching your {doc_type} from DigiLocker...\n\nSupported documents:\n• PAN Card\n• Aadhaar\n• GST Certificate\n• MSME Certificate"
        
        elif intent == "task.update":
            return "⚙️ Profile Update\n\nWhat would you like to update?\n• Business details\n• Language preference\n• Notification settings\n• Default invoice format\n\nPlease specify what you'd like to change."
        
        elif intent == "unknown":
            return "I'm not sure I understood that. I can help you with:\n\n• Invoice creation and management\n• GST verification and filing\n• Udyam registration details\n• Business analytics and reports\n• DigiLocker document access\n\nWhat would you like to do?"
        
        else:
            return "I'm SmartBiz AI, your MSME business assistant. How can I help you today?"
    
    def _get_general_response(self, query: str, language: str) -> str:
        """
        Handle general chat queries
        """
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["hello", "hi", "hey"]):
            return "Hello! I'm SmartBiz AI, your MSME business co-pilot. 👋\n\nI can help you with:\n• Invoice management\n• GST filing and verification\n• Business analytics\n• Government scheme information\n• Document automation\n\nWhat would you like to do today?"
        
        elif any(word in query_lower for word in ["help", "what can you do"]):
            return "I'm here to simplify your business operations! 🚀\n\n**I can help you:**\n• Create and manage invoices\n• Verify GST numbers\n• File GST returns\n• Check Udyam registration\n• Generate business reports\n• Access DigiLocker documents\n• Provide business insights\n\nJust ask me what you need!"
        
        else:
            # For other general queries, use Groq Llama 3.1 8B if available
            if self.client:
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": "You are SmartBiz AI, a helpful assistant for Indian MSME businesses. Be concise, professional, and helpful. Answer in 2-3 short paragraphs."},
                            {"role": "user", "content": query}
                        ],
                        max_tokens=300,
                        temperature=0.7
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    logger.error(f"Groq LLM error: {str(e)}")
            
            return "I'm SmartBiz AI. I specialize in helping MSME businesses with invoicing, GST, compliance, and analytics. How can I assist you?"
    
    async def _propose_memory(self, intent: str, entities: Dict[str, Any], tool_results: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Propose memory entries to save
        
        Save ONLY when:
        - User gives stable data (business name, GST, Udyam, address)
        - User expresses preferences (language, formats, rules)
        - Important business actions occur (invoice created, GST verified)
        
        Do NOT save:
        - Temporary info
        - Random chat
        - Mistakes
        - Model-generated content
        """
        memory_entries = []
        
        # Save GST number if verified
        if intent == "gst.verify" and entities.get("gst_number") and tool_results.get("status") == "success":
            memory_entries.append({
                "type": "fact",
                "key": "gst_number",
                "value": entities["gst_number"]
            })
        
        # Save business name if provided
        if entities.get("business_name"):
            memory_entries.append({
                "type": "fact",
                "key": "business_name",
                "value": entities["business_name"]
            })
        
        # Save Udyam number if verified
        if intent == "gov.udyam" and entities.get("udyam_number") and tool_results.get("status") == "success":
            memory_entries.append({
                "type": "fact",
                "key": "udyam_number",
                "value": entities["udyam_number"]
            })
        
        # Save language preference if explicitly stated
        if intent == "task.update" and entities.get("language"):
            memory_entries.append({
                "type": "preference",
                "key": "language",
                "value": entities["language"]
            })
        
        # Save invoice creation action
        if intent == "invoice.create" and tool_results.get("status") == "success":
            memory_entries.append({
                "type": "action",
                "key": "last_invoice",
                "value": f"Created for {entities.get('customer_name', 'N/A')} - ₹{entities.get('amount', 0)}"
            })
        
        return memory_entries
