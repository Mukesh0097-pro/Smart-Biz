import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { TrendingUp, DollarSign, FileText, AlertCircle, Loader2 } from 'lucide-react';

interface DashboardStats {
  total_revenue: number;
  pending_invoices: number;
  pending_amount: number;
  monthly_revenue: number;
  total_invoices: number;
}

const DashboardAnalytics: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      console.log('Fetching dashboard overview...');
      
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/api/dashboard/overview', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      
      console.log('Dashboard data received:', response.data);
      setStats(response.data);
    } catch (err: any) {
      console.error('Error fetching dashboard data:', err);
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to load dashboard data';
      console.error('Error details:', errorMsg);
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <Loader2 className="animate-spin text-blue-500" size={48} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <AlertCircle className="mx-auto text-red-500 mb-4" size={48} />
          <h3 className="text-xl font-semibold text-gray-700 mb-2">Error Loading Dashboard</h3>
          <p className="text-gray-500">{error}</p>
          <button
            onClick={fetchDashboardData}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
          Dashboard Analytics
        </h1>
        <p className="text-gray-600 mt-2">
          Overview of your business performance
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Total Revenue */}
        <div className="glass-card rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center">
              <DollarSign className="text-green-600" size={24} />
            </div>
          </div>
          <h3 className="text-sm font-medium text-gray-600 mb-1">Total Revenue</h3>
          <p className="text-3xl font-bold text-gray-900">
            ₹{stats?.total_revenue.toLocaleString('en-IN') || '0'}
          </p>
        </div>

        {/* Monthly Revenue */}
        <div className="glass-card rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
              <TrendingUp className="text-blue-600" size={24} />
            </div>
          </div>
          <h3 className="text-sm font-medium text-gray-600 mb-1">This Month</h3>
          <p className="text-3xl font-bold text-gray-900">
            ₹{stats?.monthly_revenue.toLocaleString('en-IN') || '0'}
          </p>
        </div>

        {/* Pending Amount */}
        <div className="glass-card rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 rounded-full bg-yellow-100 flex items-center justify-center">
              <AlertCircle className="text-yellow-600" size={24} />
            </div>
          </div>
          <h3 className="text-sm font-medium text-gray-600 mb-1">Pending Amount</h3>
          <p className="text-3xl font-bold text-gray-900">
            ₹{stats?.pending_amount.toLocaleString('en-IN') || '0'}
          </p>
          <p className="text-sm text-gray-500 mt-1">
            {stats?.pending_invoices || 0} invoice{(stats?.pending_invoices || 0) !== 1 ? 's' : ''}
          </p>
        </div>

        {/* Total Invoices */}
        <div className="glass-card rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center">
              <FileText className="text-indigo-600" size={24} />
            </div>
          </div>
          <h3 className="text-sm font-medium text-gray-600 mb-1">Total Invoices</h3>
          <p className="text-3xl font-bold text-gray-900">
            {stats?.total_invoices || 0}
          </p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="glass-card rounded-2xl p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="px-4 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-lg hover:from-blue-600 hover:to-indigo-700 transition-all">
            Create Invoice
          </button>
          <button className="px-4 py-3 bg-white border-2 border-blue-500 text-blue-600 rounded-lg hover:bg-blue-50 transition-all">
            Verify GST Number
          </button>
          <button className="px-4 py-3 bg-white border-2 border-indigo-500 text-indigo-600 rounded-lg hover:bg-indigo-50 transition-all">
            View Reports
          </button>
        </div>
      </div>

      {/* Recent Activity Placeholder */}
      <div className="glass-card rounded-2xl p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Recent Activity</h2>
        <p className="text-gray-500 text-center py-8">
          Ask the AI Copilot to see your recent invoices and transactions
        </p>
      </div>
    </div>
  );
};

export default DashboardAnalytics;
