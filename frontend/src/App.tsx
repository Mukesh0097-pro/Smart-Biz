import React, { useState, useEffect } from 'react';
import { Screen } from './types';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import DashboardAnalytics from './components/DashboardAnalytics';
import SupplierFinder from './components/SupplierFinder';
import Login from './components/Login';
import Register from './components/Register';
import Invoices from './components/Invoices';
import GSTCompliance from './components/GSTCompliance';

const App: React.FC = () => {
  const [activeScreen, setActiveScreen] = useState<Screen>(Screen.AI_COPILOT);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [showRegister, setShowRegister] = useState<boolean>(false);

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = (token: string) => {
    localStorage.setItem('token', token);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setActiveScreen(Screen.AI_COPILOT);
  };

  const renderScreen = () => {
    switch (activeScreen) {
      case Screen.AI_COPILOT:
        return <Dashboard />;
      case Screen.DASHBOARD:
        return <DashboardAnalytics />;
      case Screen.INVOICES:
        return <Invoices />;
      case Screen.GST:
        return <GSTCompliance />;
      case Screen.SUPPLIER_FINDER:
        return <SupplierFinder />;
      default:
        return (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <h1 className="text-3xl font-bold text-slate-800">
                {activeScreen}
              </h1>
              <p className="mt-2 text-slate-500">Feature coming soon.</p>
            </div>
          </div>
        );
    }
  };

  if (!isAuthenticated) {
    return showRegister ? (
      <Register 
        onRegister={handleLogin} 
        onSwitchToLogin={() => setShowRegister(false)} 
      />
    ) : (
      <Login 
        onLogin={handleLogin} 
        onSwitchToRegister={() => setShowRegister(true)} 
      />
    );
  }

  return (
    <div className="flex h-screen w-full bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <Sidebar 
        activeScreen={activeScreen} 
        setActiveScreen={setActiveScreen}
        onLogout={handleLogout}
      />
      <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
        {renderScreen()}
      </main>
    </div>
  );
};

export default App;
