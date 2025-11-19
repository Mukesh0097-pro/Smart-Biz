import React, { useState, useEffect } from 'react';
import { invoiceAPI } from '../services/api';
import { Invoice } from '../types';
import { FileText, Download, Trash2, Plus, Loader2 } from 'lucide-react';

const Invoices: React.FC = () => {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadInvoices();
  }, []);

  const loadInvoices = async () => {
    try {
      setLoading(true);
      const response = await invoiceAPI.list();
      // Backend returns { invoices: [...] }
      setInvoices(response.invoices || []);
    } catch (err: any) {
      console.error('Error loading invoices:', err);
      setError(err.response?.data?.detail || 'Failed to load invoices');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (invoiceId: string, invoiceNumber: string) => {
    try {
      await invoiceAPI.downloadPDF(invoiceId, invoiceNumber);
    } catch (err: any) {
      console.error('Error downloading invoice:', err);
      alert(err.response?.data?.detail || 'Failed to download invoice');
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this invoice?')) return;

    try {
      await invoiceAPI.delete(id);
      setInvoices(invoices.filter((inv) => inv.id !== id));
    } catch (err: any) {
      console.error('Error deleting invoice:', err);
      alert(err.response?.data?.detail || 'Failed to delete invoice');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'paid':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'overdue':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="h-full">
      <div className="glass-card rounded-2xl p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              Invoices
            </h1>
            <p className="text-gray-600 mt-2">Manage your business invoices</p>
          </div>
          <button
            onClick={() => alert('Use AI Copilot to create invoices: "Create an invoice for ABC Corp worth ₹5000"')}
            className="glass-button flex items-center gap-2"
          >
            <Plus size={20} />
            Create Invoice
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Loading State */}
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <Loader2 size={48} className="animate-spin text-blue-500" />
          </div>
        ) : invoices.length === 0 ? (
          <div className="text-center py-12">
            <FileText size={64} className="mx-auto text-gray-400 mb-4" />
            <h3 className="text-xl font-semibold text-gray-700 mb-2">
              No invoices yet
            </h3>
            <p className="text-gray-500">
              Use the AI Copilot to create your first invoice
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">
                    Invoice #
                  </th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">
                    Customer
                  </th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">
                    Issue Date
                  </th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">
                    Due Date
                  </th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">
                    Amount
                  </th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">
                    Status
                  </th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                {invoices.map((invoice) => (
                  <tr
                    key={invoice.id}
                    className="border-b border-gray-100 hover:bg-gray-50/50"
                  >
                    <td className="py-4 px-4 font-medium text-gray-900">
                      {invoice.invoice_number}
                    </td>
                    <td className="py-4 px-4 text-gray-700">
                      {invoice.customer_id || 'N/A'}
                    </td>
                    <td className="py-4 px-4 text-gray-600">
                      {new Date(invoice.created_at).toLocaleDateString()}
                    </td>
                    <td className="py-4 px-4 text-gray-600">
                      {new Date(invoice.due_date).toLocaleDateString()}
                    </td>
                    <td className="py-4 px-4 font-semibold text-gray-900">
                      ₹{invoice.total_amount.toLocaleString()}
                    </td>
                    <td className="py-4 px-4">
                      <span
                        className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(
                          invoice.status
                        )}`}
                      >
                        {invoice.status}
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleDownload(invoice.id, invoice.invoice_number)}
                          className="p-2 hover:bg-blue-50 rounded-lg transition-colors"
                          title="Download PDF"
                        >
                          <Download size={18} className="text-blue-600" />
                        </button>
                        <button
                          onClick={() => handleDelete(invoice.id)}
                          className="p-2 hover:bg-red-50 rounded-lg transition-colors"
                          title="Delete Invoice"
                        >
                          <Trash2 size={18} className="text-red-600" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Invoices;
