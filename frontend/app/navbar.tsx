// frontend/app/navbar.tsx

'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function Navbar() {
  const pathname = usePathname();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [checkedAuth, setCheckedAuth] = useState(false);

  useEffect(() => {
    // Check if user is logged in by checking for token in localStorage
    const token = localStorage.getItem('access_token');
    setIsLoggedIn(!!token);
    setCheckedAuth(true);
  }, [pathname]); // Re-check when pathname changes

  const handleLogout = () => {
    // Remove both localStorage and cookie tokens
    localStorage.removeItem('access_token');
    document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    window.location.href = '/auth/login';
  };

  return (
    <nav className="bg-gray-800/80 backdrop-blur-md text-white shadow-lg border-b border-gray-700/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="text-xl font-bold text-white">
              Todo App
            </Link>
            <div className="ml-6 flex space-x-4">
              {!checkedAuth ? (
                // Placeholder to maintain layout during hydration
                <div className="px-3 py-2 rounded-md text-sm font-medium text-gray-300">
                  Loading...
                </div>
              ) : isLoggedIn ? (
                <>
                </>
              ) : (
                <>
                  <Link
                    href="/auth/login"
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      pathname === '/auth/login'
                        ? 'bg-gray-700/50 text-white'
                        : 'text-gray-300 hover:bg-gray-700/50 hover:text-white'
                    }`}
                  >
                    Login
                  </Link>
                  <Link
                    href="/auth/register"
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      pathname === '/auth/register'
                        ? 'bg-gray-700/50 text-white'
                        : 'text-gray-300 hover:bg-gray-700/50 hover:text-white'
                    }`}
                  >
                    Register
                  </Link>
                </>
              )}
            </div>
          </div>
          {checkedAuth && isLoggedIn && (
            <div className="flex items-center">
              <button
                onClick={handleLogout}
                className="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:bg-gray-700/50 hover:text-white transition-colors"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}