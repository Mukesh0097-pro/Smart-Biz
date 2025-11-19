import React from 'react';
import { Screen } from '../types';
import {
  LayoutDashboard,
  FileText,
  Receipt,
  Package,
  TrendingUp,
  FileSpreadsheet,
  Bot,
  LogOut,
  Menu,
  X,
} from 'lucide-react';

interface SidebarProps {
  activeScreen: Screen;
  setActiveScreen: (screen: Screen) => void;
  onLogout: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeScreen, setActiveScreen, onLogout }) => {
  const [isOpen, setIsOpen] = React.useState(false);

  const menuItems = [
    { screen: Screen.AI_COPILOT, icon: Bot, label: 'AI Copilot' },
    { screen: Screen.DASHBOARD, icon: LayoutDashboard, label: 'Dashboard' },
    { screen: Screen.INVOICES, icon: FileText, label: 'Invoices' },
    { screen: Screen.GST, icon: Receipt, label: 'GST Compliance' },
    { screen: Screen.SUPPLIER_FINDER, icon: Package, label: 'Supplier Finder' },
    { screen: Screen.EXPENSE_TRACKER, icon: TrendingUp, label: 'Expense Tracker' },
    { screen: Screen.INVENTORY, icon: Package, label: 'Inventory' },
    { screen: Screen.REPORTS, icon: FileSpreadsheet, label: 'Reports' },
  ];

  return (
    <>
      {/* Mobile Menu Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 rounded-lg glass-card"
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Sidebar */}
      <aside
        className={`
          fixed lg:static inset-y-0 left-0 z-40
          w-64 bg-white/80 backdrop-blur-md border-r border-white/20 shadow-xl
          transform transition-transform duration-300 ease-in-out
          ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
      >
        <div className="flex flex-col h-full p-4">
          {/* Logo */}
          <div className="mb-8 pt-12 lg:pt-0">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              SmartBiz AI
            </h1>
            <p className="text-sm text-gray-500 mt-1">Your Business Copilot</p>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-2">
            {menuItems.map(({ screen, icon: Icon, label }) => (
              <button
                key={screen}
                onClick={() => {
                  setActiveScreen(screen);
                  setIsOpen(false);
                }}
                className={`
                  w-full flex items-center gap-3 px-4 py-3 rounded-lg
                  transition-all duration-200
                  ${
                    activeScreen === screen
                      ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-lg'
                      : 'text-gray-700 hover:bg-gray-100/50'
                  }
                `}
              >
                <Icon size={20} />
                <span className="font-medium">{label}</span>
              </button>
            ))}
          </nav>

          {/* Logout Button */}
          <button
            onClick={onLogout}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-red-600 hover:bg-red-50 transition-all"
          >
            <LogOut size={20} />
            <span className="font-medium">Logout</span>
          </button>
        </div>
      </aside>

      {/* Overlay for mobile */}
      {isOpen && (
        <div
          onClick={() => setIsOpen(false)}
          className="lg:hidden fixed inset-0 bg-black/20 backdrop-blur-sm z-30"
        />
      )}
    </>
  );
};

export default Sidebar;
