import axios from 'axios';
import type {
  LoginResponse,
  ChatQueryRequest,
  ChatQueryResponse,
  Invoice,
  GSTVerificationResponse,
  Customer,
} from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  login: async (email: string, password: string): Promise<LoginResponse> => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await axios.post(`${API_BASE_URL}/auth/login`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  register: async (email: string, password: string, businessName?: string): Promise<LoginResponse> => {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, {
      email,
      password,
      business_name: businessName,
    });
    return response.data;
  },
};

// Chat API
export const chatAPI = {
  sendQuery: async (query: string): Promise<ChatQueryResponse> => {
    const response = await api.post('/chat/query', { query });
    return response.data;
  },
};

// Invoice API
export const invoiceAPI = {
  list: async (): Promise<Invoice[]> => {
    const response = await api.get('/invoices/list');
    return response.data;
  },

  get: async (id: number): Promise<Invoice> => {
    const response = await api.get(`/invoices/${id}`);
    return response.data;
  },

  create: async (invoiceData: Partial<Invoice>): Promise<Invoice> => {
    const response = await api.post('/invoices/create', invoiceData);
    return response.data;
  },

  downloadPDF: async (id: number): Promise<void> => {
    const response = await api.get(`/invoices/${id}/download`, {
      responseType: 'blob',
    });
    
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `invoice_${id}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/invoices/${id}`);
  },
};

// GST API
export const gstAPI = {
  verify: async (gstin: string): Promise<GSTVerificationResponse> => {
    const response = await api.get(`/gst/verify?gstin=${gstin}`);
    return response.data;
  },
};

// Customer API
export const customerAPI = {
  list: async (): Promise<Customer[]> => {
    const response = await api.get('/customers/list');
    return response.data;
  },

  create: async (customerData: Partial<Customer>): Promise<Customer> => {
    const response = await api.post('/customers/create', customerData);
    return response.data;
  },
};

// Dashboard API
export const dashboardAPI = {
  getStats: async (): Promise<any> => {
    const response = await api.get('/dashboard/stats');
    return response.data;
  },
};

export default api;
