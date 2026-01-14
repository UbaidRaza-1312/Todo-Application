// app/page.tsx
'use client';

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Layout from '../src/components/Layout';
import AuthService from '../src/services/authService';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated
    const token = AuthService.getToken();
    if (token) {
      // If authenticated, redirect to tasks page
      router.push('/tasks');
    } else {
      // If not authenticated, redirect to login page
      router.push('/auth/login');
    }
  }, [router]);

  return (
    <Layout title="Todo App">
      <div className="flex flex-col items-center justify-center min-h-[calc(100vh-200px)]">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-800 mb-4">Todo App</h1>
          <p className="text-gray-600">Redirecting...</p>
        </div>
      </div>
    </Layout>
  );
}