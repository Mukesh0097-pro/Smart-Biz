"""
Invoice management API routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from backend.core.database import get_db
from backend.core.security import get_current_user
from backend.models.invoice import Invoice, InvoiceStatus

router = APIRouter()

class InvoiceItem(BaseModel):
    name: str
    quantity: float
    rate: float
    amount: float

class InvoiceCreate(BaseModel):
    customer_id: str
    due_date: datetime
    items: List[InvoiceItem]
    notes: Optional[str] = None
    tax_rate: Optional[float] = 18.0

@router.post("/create")
async def create_invoice(
    invoice_data: InvoiceCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new invoice"""
    user_id = current_user["user_id"]
    
    # Calculate amounts
    subtotal = sum(item.amount for item in invoice_data.items)
    tax_amount = subtotal * (invoice_data.tax_rate / 100)
    total_amount = subtotal + tax_amount
    
    # Generate invoice number
    invoice_count = db.query(Invoice).filter(Invoice.user_id == user_id).count()
    invoice_number = f"INV-{datetime.now().year}-{invoice_count + 1:04d}"
    
    # Create invoice
    new_invoice = Invoice(
        invoice_number=invoice_number,
        user_id=user_id,
        customer_id=invoice_data.customer_id,
        due_date=invoice_data.due_date,
        items=[item.dict() for item in invoice_data.items],
        subtotal=subtotal,
        tax_amount=tax_amount,
        total_amount=total_amount,
        gst_rate=invoice_data.tax_rate,
        notes=invoice_data.notes,
        status=InvoiceStatus.DRAFT
    )
    
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    
    return {
        "message": "Invoice created successfully",
        "invoice_id": str(new_invoice.id),
        "invoice_number": new_invoice.invoice_number
    }

@router.get("/list")
async def list_invoices(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    status: Optional[str] = None,
    limit: int = 50
):
    """List user's invoices"""
    query = db.query(Invoice).filter(Invoice.user_id == current_user["user_id"])
    
    if status:
        query = query.filter(Invoice.status == status)
    
    invoices = query.order_by(Invoice.created_at.desc()).limit(limit).all()
    
    return {
        "invoices": [
            {
                "id": str(inv.id),
                "invoice_number": inv.invoice_number,
                "customer_id": str(inv.customer_id),
                "total_amount": inv.total_amount,
                "status": inv.status,
                "due_date": inv.due_date.isoformat(),
                "created_at": inv.created_at.isoformat()
            }
            for inv in invoices
        ]
    }

@router.get("/{invoice_id}")
async def get_invoice(
    invoice_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get invoice details"""
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.user_id == current_user["user_id"]
    ).first()
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    return {
        "id": str(invoice.id),
        "invoice_number": invoice.invoice_number,
        "customer_id": str(invoice.customer_id),
        "items": invoice.items,
        "subtotal": invoice.subtotal,
        "tax_amount": invoice.tax_amount,
        "total_amount": invoice.total_amount,
        "status": invoice.status,
        "due_date": invoice.due_date.isoformat(),
        "notes": invoice.notes
    }
