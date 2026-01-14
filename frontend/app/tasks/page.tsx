// app/tasks/page.tsx
'use client';

import React, { useState, useEffect } from 'react';
import TaskList from '../../src/components/TaskManager/TaskList';
import AuthService from '../../src/services/authService';

const TasksPage = () => {
  const [userId, setUserId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = AuthService.getToken();
    if (!token) {
      // Remove any stale cookies if token isn't in localStorage
      document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
      window.location.href = '/auth/login';
      return;
    }

    // Fetch user data from API
    AuthService.getCurrentUser()
      .then(user => {
        setUserId(user.id);
      })
      .catch(() => {
        // Remove invalid token from both localStorage and cookies
        localStorage.removeItem('access_token');
        document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        window.location.href = '/auth/login';
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900">
        <div className="text-2xl font-semibold text-white">Loading...</div>
      </div>
    );
  }

  if (!userId) {
    return null; // Redirect is happening in useEffect
  }

  return <TaskList userId={userId} />;
};

export default TasksPage;