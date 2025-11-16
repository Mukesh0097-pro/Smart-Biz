"""
Invoice PDF Generator Service
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
from typing import Dict, Any
import os
from pathlib import Path

class InvoiceGenerator:
    """Generate professional invoice PDFs"""
    
    def __init__(self):
        self.output_dir = Path("./invoices")
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_pdf(self, invoice_data: Dict[str, Any], user_data: Dict[str, Any], customer_data: Dict[str, Any]) -> str:
        """
        Generate invoice PDF
        
        Args:
            invoice_data: Invoice details (number, items, amounts, dates)
            user_data: Business/user details (name, address, GST, email)
            customer_data: Customer details (name, address, GST, email)
        
        Returns:
            Path to generated PDF file
        """
        # Create PDF filename
        invoice_number = invoice_data.get('invoice_number', 'INV-0001')
        filename = f"{invoice_number}.pdf"
        filepath = self.output_dir / filename
        
        # Create PDF
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        # Container for PDF elements
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        
        normal_style = styles['Normal']
        normal_style.fontSize = 10
        
        # Title
        elements.append(Paragraph("TAX INVOICE", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Invoice Info and Business Details (side by side)
        invoice_info_data = [
            ['Invoice Number:', invoice_data.get('invoice_number', 'N/A')],
            ['Invoice Date:', invoice_data.get('created_at', datetime.now().strftime('%d-%b-%Y'))],
            ['Due Date:', invoice_data.get('due_date', 'N/A')],
            ['Status:', invoice_data.get('status', 'DRAFT')]
        ]
        
        business_info = user_data.get('business_name') or user_data.get('full_name') or 'Your Business'
        business_details = [
            [Paragraph('<b>From:</b>', normal_style)],
            [Paragraph(f'<b>{business_info}</b>', normal_style)],
            [Paragraph(user_data.get('email') or '', normal_style)],
            [Paragraph(user_data.get('phone') or '', normal_style)],
            [Paragraph(f"GSTIN: {user_data.get('gst_number') or 'N/A'}", normal_style)]
        ]
        
        # Create two-column layout
        header_data = [
            [
                Table(business_details, colWidths=[3*inch]),
                Table(invoice_info_data, colWidths=[1.2*inch, 1.8*inch])
            ]
        ]
        
        header_table = Table(header_data, colWidths=[3*inch, 3*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ]))
        
        elements.append(header_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Customer Details
        elements.append(Paragraph("Bill To:", heading_style))
        
        customer_info = [
            [Paragraph(f"<b>{customer_data.get('name') or 'Customer'}</b>", normal_style)],
            [Paragraph(customer_data.get('email') or '', normal_style)],
            [Paragraph(customer_data.get('phone') or '', normal_style)],
        ]
        
        if customer_data.get('gst_number'):
            customer_info.append([Paragraph(f"GSTIN: {customer_data['gst_number']}", normal_style)])
        
        if customer_data.get('billing_address'):
            addr = customer_data['billing_address']
            if isinstance(addr, dict):
                address_text = f"{addr.get('street', '')}, {addr.get('city', '')}, {addr.get('state', '')} - {addr.get('pincode', '')}"
                customer_info.append([Paragraph(address_text, normal_style)])
        
        customer_table = Table(customer_info, colWidths=[6*inch])
        elements.append(customer_table)
        elements.append(Spacer(1, 0.4*inch))
        
        # Items Table
        elements.append(Paragraph("Items:", heading_style))
        
        # Table header
        items_data = [
            ['#', 'Description', 'Qty', 'Rate (₹)', 'Amount (₹)']
        ]
        
        # Add items
        items = invoice_data.get('items', [])
        if not items:
            items = [{'name': 'Service/Product', 'quantity': 1, 'rate': 0, 'amount': 0}]
        
        for idx, item in enumerate(items, 1):
            # Get item details - handle both 'name' and 'description' fields
            item_name = item.get('name') or item.get('description') or 'Item'
            item_qty = item.get('quantity', 1)
            item_rate = float(item.get('rate', 0))
            item_amount = float(item.get('amount', item_qty * item_rate))
            
            items_data.append([
                str(idx),
                item_name,
                str(item_qty),
                f"{item_rate:,.2f}",
                f"{item_amount:,.2f}"
            ])
        
        # Subtotal, Tax, Total
        subtotal = float(invoice_data.get('subtotal', 0))
        tax_rate = float(invoice_data.get('gst_rate', 18))
        tax_amount = float(invoice_data.get('tax_amount', 0))
        total = float(invoice_data.get('total_amount', 0))
        
        # Add separator row
        items_data.append(['', '', '', '', ''])
        
        # Add totals
        items_data.append(['', '', '', 'Subtotal:', f"{subtotal:,.2f}"])
        items_data.append(['', '', '', f'GST ({tax_rate:.0f}%):', f"{tax_amount:,.2f}"])
        items_data.append(['', '', '', Paragraph('<b>Total:</b>', normal_style), Paragraph(f"<b>{total:,.2f}</b>", normal_style)])
        
        # Create items table
        items_table = Table(items_data, colWidths=[0.5*inch, 2.8*inch, 0.6*inch, 1.2*inch, 1.4*inch])
        items_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            
            # Items rows - only apply grid to rows with actual data
            ('ALIGN', (0, 1), (0, -5), 'CENTER'),
            ('ALIGN', (2, 1), (2, -5), 'CENTER'),
            ('ALIGN', (3, 1), (-1, -5), 'RIGHT'),
            ('FONTNAME', (0, 1), (-1, -5), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -5), 10),
            ('GRID', (0, 0), (-1, -5), 0.5, colors.HexColor('#d1d5db')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -5), [colors.white, colors.HexColor('#f9fafb')]),
            ('TOPPADDING', (0, 1), (-1, -5), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -5), 8),
            
            # Totals section
            ('LINEABOVE', (3, -3), (-1, -3), 1.5, colors.HexColor('#d1d5db')),
            ('ALIGN', (3, -3), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, -3), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, -3), (-1, -2), 10),
            ('TOPPADDING', (0, -3), (-1, -1), 8),
            ('BOTTOMPADDING', (0, -3), (-1, -1), 8),
            
            # Total row (bold)
            ('LINEABOVE', (3, -1), (-1, -1), 2, colors.HexColor('#1e40af')),
            ('FONTNAME', (3, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (3, -1), (-1, -1), 12),
            ('BACKGROUND', (3, -1), (-1, -1), colors.HexColor('#eff6ff')),
            ('TEXTCOLOR', (3, -1), (-1, -1), colors.HexColor('#1e40af')),
        ]))
        
        elements.append(items_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Notes
        if invoice_data.get('notes'):
            elements.append(Paragraph("Notes:", heading_style))
            elements.append(Paragraph(invoice_data['notes'], normal_style))
            elements.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("Thank you for your business!", footer_style))
        elements.append(Paragraph(f"Generated by SmartBiz AI on {datetime.now().strftime('%d %B %Y')}", footer_style))
        
        # Build PDF
        doc.build(elements)
        
        return str(filepath)
