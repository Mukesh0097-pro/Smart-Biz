import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authService = {
  async login(email: string, password: string) {
    const response = await apiClient.post('/auth/login', { email, password });
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  async register(email: string, password: string, full_name: string) {
    const response = await apiClient.post('/auth/register', {
      email,
      password,
      full_name,
    });
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  },

  getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },
};

export const chatService = {
  async sendQuery(query: string) {
    const response = await apiClient.post('/chat/query', { query });
    return response.data;
  },

  async getSuggestions() {
    const response = await apiClient.get('/chat/suggestions');
    return response.data;
  },
};

export const invoiceService = {
  async getInvoices(status?: string) {
    const response = await apiClient.get('/invoices/list', {
      params: { status },
    });
    return response.data;
  },

  async createInvoice(invoiceData: any) {
    const response = await apiClient.post('/invoices/create', invoiceData);
    return response.data;
  },

  async getInvoice(invoiceId: string) {
    const response = await apiClient.get(`/invoices/${invoiceId}`);
    return response.data;
  },
};

export const dashboardService = {
  async getOverview() {
    const response = await apiClient.get('/dashboard/overview');
    return response.data;
  },

  async getInsights() {
    const response = await apiClient.get('/dashboard/insights');
    return response.data;
  },
};

export default apiClient;
