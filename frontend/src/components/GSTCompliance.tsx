import React, { useState } from 'react';
import { gstAPI } from '../services/api';
import { GSTVerificationResponse } from '../types';
import { Shield, CheckCircle, XCircle, Loader2 } from 'lucide-react';

const GSTCompliance: React.FC = () => {
  const [gstin, setGstin] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<GSTVerificationResponse | null>(null);
  const [error, setError] = useState('');

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!gstin.trim()) return;

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await gstAPI.verify(gstin);
      setResult(response);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to verify GST number');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-full">
      <div className="glass-card rounded-2xl p-6">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            GST Compliance
          </h1>
          <p className="text-gray-600 mt-2">
            Verify GST numbers and manage compliance
          </p>
        </div>

        {/* Verification Form */}
        <form onSubmit={handleVerify} className="mb-8">
          <div className="flex gap-3">
            <input
              type="text"
              value={gstin}
              onChange={(e) => setGstin(e.target.value.toUpperCase())}
              placeholder="Enter GST Number (e.g., 29ABCDE1234F1Z5)"
              className="glass-input flex-1"
              maxLength={15}
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !gstin.trim()}
              className="glass-button px-8 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {loading && <Loader2 size={20} className="animate-spin" />}
              {loading ? 'Verifying...' : 'Verify'}
            </button>
          </div>
          <p className="text-sm text-gray-500 mt-2">
            Enter a 15-character GST Identification Number
          </p>
        </form>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6 flex items-center gap-2">
            <XCircle size={20} />
            {error}
          </div>
        )}

        {/* Verification Result */}
        {result && (
          <div className="glass-card rounded-xl p-6 border-2 border-green-200">
            <div className="flex items-center gap-3 mb-6">
              {result.verified ? (
                <>
                  <CheckCircle size={32} className="text-green-600" />
                  <div>
                    <h3 className="text-xl font-semibold text-green-800">
                      GST Number Verified
                    </h3>
                    <p className="text-green-600">Valid and Active</p>
                  </div>
                </>
              ) : (
                <>
                  <XCircle size={32} className="text-red-600" />
                  <div>
                    <h3 className="text-xl font-semibold text-red-800">
                      Verification Failed
                    </h3>
                    <p className="text-red-600">Invalid GST Number</p>
                  </div>
                </>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-white/50 rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-1">GSTIN</p>
                <p className="font-semibold text-gray-900">{result.gstin}</p>
              </div>

              <div className="bg-white/50 rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-1">Legal Name</p>
                <p className="font-semibold text-gray-900">{result.legal_name}</p>
              </div>

              {result.trade_name && (
                <div className="bg-white/50 rounded-lg p-4">
                  <p className="text-sm text-gray-600 mb-1">Trade Name</p>
                  <p className="font-semibold text-gray-900">{result.trade_name}</p>
                </div>
              )}

              <div className="bg-white/50 rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-1">Status</p>
                <p className="font-semibold text-gray-900">{result.status}</p>
              </div>

              <div className="bg-white/50 rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-1">State</p>
                <p className="font-semibold text-gray-900">{result.state}</p>
              </div>

              {result.address && (
                <div className="bg-white/50 rounded-lg p-4 md:col-span-2">
                  <p className="text-sm text-gray-600 mb-1">Address</p>
                  <p className="font-semibold text-gray-900">{result.address}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Help Section */}
        {!result && !loading && (
          <div className="mt-8 glass-card rounded-xl p-6 bg-blue-50/50">
            <div className="flex items-start gap-3">
              <Shield size={24} className="text-blue-600 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">
                  About GST Verification
                </h3>
                <ul className="text-sm text-gray-700 space-y-2">
                  <li>
                    • Verify the authenticity of GST numbers before business
                    transactions
                  </li>
                  <li>
                    • Get real-time information about registered businesses
                  </li>
                  <li>
                    • Ensure compliance with GST regulations
                  </li>
                  <li>
                    • Access legal name, trade name, and registered address
                  </li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default GSTCompliance;
