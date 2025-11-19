// Screen navigation types
export enum Screen {
  AI_COPILOT = 'AI Copilot',
  DASHBOARD = 'Dashboard',
  INVOICES = 'Invoices',
  GST = 'GST Compliance',
  SUPPLIER_FINDER = 'Supplier Finder',
  EXPENSE_TRACKER = 'Expense Tracker',
  INVENTORY = 'Inventory',
  REPORTS = 'Reports',
}

// User types
export interface User {
  id: number;
  email: string;
  business_name?: string;
  gstin?: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

// Invoice types
export interface Invoice {
  id: string;
  invoice_number: string;
  customer_id: string;
  customer_name?: string;
  created_at: string;
  due_date: string;
  total_amount: number;
  status: string;
  items?: InvoiceItem[];
}

export interface InvoiceItem {
  id?: number;
  invoice_id?: number;
  description: string;
  quantity: number;
  unit_price: number;
  tax_rate: number;
  amount: number;
}

// Chat types
export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

export interface ChatQueryRequest {
  query: string;
  user_id?: number;
}

export interface ChatQueryResponse {
  response: string;
  intent?: string;
  entities?: any;
}

// GST types
export interface GSTVerificationRequest {
  gstin: string;
}

export interface GSTVerificationResponse {
  gstin: string;
  legal_name: string;
  trade_name?: string;
  status: string;
  state: string;
  address?: string;
  verified: boolean;
}

// Customer types
export interface Customer {
  id: number;
  name: string;
  email?: string;
  phone?: string;
  gstin?: string;
  address?: string;
  user_id: number;
}
