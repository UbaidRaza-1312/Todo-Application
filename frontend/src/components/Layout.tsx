// frontend/src/components/Layout.tsx

import React, { ReactNode, useEffect, useState } from 'react';
import Link from 'next/link';
import AuthService from '../services/authService';

interface LayoutProps {
  children: ReactNode;
  title?: string;
}

const Layout: React.FC<LayoutProps> = ({ children, title = 'Todo App' }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [checkedAuth, setCheckedAuth] = useState(false);

  useEffect(() => {
    // Check authentication status after component mounts
    setIsAuthenticated(AuthService.isAuthenticated());
    setCheckedAuth(true);
  }, []);

  const handleLogout = () => {
    AuthService.logout();
    window.location.href = '/auth/login';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-indigo-700 text-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link href="/" className="text-xl font-bold">
                Todo App
              </Link>
              <div className="ml-6 flex space-x-4">
                {checkedAuth ? (
                  isAuthenticated ? (
                    <Link href="/tasks" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-indigo-600">
                      Tasks
                    </Link>
                  ) : (
                    <>
                      <Link href="/auth/login" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-indigo-600">
                        Login
                      </Link>
                      <Link href="/auth/register" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-indigo-600">
                        Register
                      </Link>
                    </>
                  )
                ) : (
                  // Placeholder to maintain layout during hydration
                  <div className="px-3 py-2 rounded-md text-sm font-medium">
                    Loading...
                  </div>
                )}
              </div>
            </div>
            {checkedAuth && isAuthenticated && (
              <div className="flex items-center">
                <button
                  onClick={handleLogout}
                  className="px-3 py-2 rounded-md text-sm font-medium hover:bg-indigo-600"
                >
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </nav>

      <main>
        {children}
      </main>

      <footer className="bg-gray-800/80 backdrop-blur-md border-t border-gray-700/50 mt-8 py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-400 text-sm">
          © {new Date().getFullYear()} Todo App. All rights reserved.
        </div>
      </footer>
    </div>
  );
};

export default Layout;