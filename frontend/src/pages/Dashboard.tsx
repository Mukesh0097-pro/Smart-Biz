import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { dashboardService, authService } from '../services/api';
import Navbar from '../components/Navbar';

const Dashboard: React.FC = () => {
  const [overview, setOverview] = useState<any>(null);
  const [insights, setInsights] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [overviewData, insightsData] = await Promise.all([
        dashboardService.getOverview(),
        dashboardService.getInsights(),
      ]);
      setOverview(overviewData);
      setInsights(insightsData.insights || []);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-1">
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Revenue
                  </dt>
                  <dd className="mt-1 text-3xl font-semibold text-gray-900">
                    ₹{overview?.total_revenue?.toLocaleString() || 0}
                  </dd>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-1">
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Monthly Revenue
                  </dt>
                  <dd className="mt-1 text-3xl font-semibold text-gray-900">
                    ₹{overview?.monthly_revenue?.toLocaleString() || 0}
                  </dd>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-1">
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Pending Invoices
                  </dt>
                  <dd className="mt-1 text-3xl font-semibold text-gray-900">
                    {overview?.pending_invoices || 0}
                  </dd>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-1">
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Pending Amount
                  </dt>
                  <dd className="mt-1 text-3xl font-semibold text-gray-900">
                    ₹{overview?.pending_amount?.toLocaleString() || 0}
                  </dd>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* AI Insights */}
        <div className="bg-white shadow rounded-lg p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">AI Insights</h2>
          <div className="space-y-4">
            {insights.map((insight, index) => (
              <div
                key={index}
                className="flex items-start p-4 bg-blue-50 rounded-lg"
              >
                <div className="flex-1">
                  <p className="text-sm text-gray-900">{insight.message}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
          <button
            onClick={() => navigate('/invoices')}
            className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow"
          >
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Create Invoice
            </h3>
            <p className="text-sm text-gray-500">
              Generate a new invoice for your customers
            </p>
          </button>

          <button
            onClick={() => navigate('/chat')}
            className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow"
          >
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Ask AI Assistant
            </h3>
            <p className="text-sm text-gray-500">
              Get help with business queries
            </p>
          </button>

          <button className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow">
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              File GST
            </h3>
            <p className="text-sm text-gray-500">
              Automate your GST filing process
            </p>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
