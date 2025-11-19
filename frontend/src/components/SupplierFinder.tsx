import React from 'react';
import { Package, Search } from 'lucide-react';

const SupplierFinder: React.FC = () => {
  return (
    <div className="h-full">
      <div className="glass-card rounded-2xl p-6">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            Supplier Finder
          </h1>
          <p className="text-gray-600 mt-2">
            Find and manage your business suppliers
          </p>
        </div>

        {/* Coming Soon */}
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <Package size={64} className="mx-auto text-gray-400 mb-4" />
            <h3 className="text-xl font-semibold text-gray-700 mb-2">
              Coming Soon
            </h3>
            <p className="text-gray-500 mb-6">
              This feature is under development
            </p>
            <div className="glass-card rounded-lg p-6 max-w-md mx-auto text-left">
              <h4 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <Search size={20} className="text-blue-600" />
                Planned Features
              </h4>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>• Search for suppliers by category and location</li>
                <li>• Compare prices and ratings</li>
                <li>• Manage supplier contacts and contracts</li>
                <li>• Track order history and performance</li>
                <li>• AI-powered supplier recommendations</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SupplierFinder;
