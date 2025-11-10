"""
Dashboard analytics and insights API routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from core.database import get_db
from core.security import get_current_user
from models.invoice import Invoice, InvoiceStatus

router = APIRouter()

@router.get("/overview")
async def get_dashboard_overview(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard overview with key metrics"""
    user_id = current_user["user_id"]
    
    # Total revenue (all paid invoices)
    total_revenue = db.query(func.sum(Invoice.total_amount)).filter(
        Invoice.user_id == user_id,
        Invoice.status == InvoiceStatus.PAID
    ).scalar() or 0.0
    
    # Pending invoices
    pending_invoices = db.query(func.count(Invoice.id)).filter(
        Invoice.user_id == user_id,
        Invoice.status.in_([InvoiceStatus.SENT, InvoiceStatus.OVERDUE])
    ).scalar() or 0
    
    # Pending amount
    pending_amount = db.query(func.sum(Invoice.total_amount)).filter(
        Invoice.user_id == user_id,
        Invoice.status.in_([InvoiceStatus.SENT, InvoiceStatus.OVERDUE])
    ).scalar() or 0.0
    
    # This month's revenue
    first_day_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0)
    monthly_revenue = db.query(func.sum(Invoice.total_amount)).filter(
        Invoice.user_id == user_id,
        Invoice.status == InvoiceStatus.PAID,
        Invoice.paid_at >= first_day_of_month
    ).scalar() or 0.0
    
    return {
        "total_revenue": total_revenue,
        "pending_invoices": pending_invoices,
        "pending_amount": pending_amount,
        "monthly_revenue": monthly_revenue,
        "total_invoices": db.query(func.count(Invoice.id)).filter(
            Invoice.user_id == user_id
        ).scalar() or 0
    }

@router.get("/insights")
async def get_ai_insights(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-generated business insights"""
    # Placeholder for AI-powered insights
    insights = [
        {
            "type": "revenue",
            "message": "Your revenue increased by 20% this month",
            "icon": "trending_up"
        },
        {
            "type": "payment",
            "message": "3 invoices are overdue - consider sending reminders",
            "icon": "warning"
        },
        {
            "type": "customer",
            "message": "Customer ABC Corp is your top client this quarter",
            "icon": "star"
        }
    ]
    
    return {"insights": insights}

@router.get("/charts/revenue")
async def get_revenue_chart_data(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: int = 30
):
    """Get revenue chart data for last N days"""
    # Placeholder - implement actual data aggregation
    data = []
    for i in range(days):
        date = datetime.now() - timedelta(days=days-i-1)
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "revenue": 0  # Calculate actual revenue
        })
    
    return {"data": data}
