// frontend/src/components/TaskManager/TaskList.tsx

import React, { useState, useEffect } from 'react';
import TaskService, { Task } from '../../services/taskService';
import TaskItem from './TaskItem';
import TaskForm from './TaskForm';
import { toast } from 'react-toastify';

interface TaskListProps {
  userId: string;
}

const TaskList: React.FC<TaskListProps> = ({ userId }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchTasks();
  }, [userId]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const tasksData = await TaskService.getTasks(userId);
      setTasks(tasksData);
    } catch (err) {
      toast.error('Failed to load tasks. Please try again.', {
        position: "top-center",
        autoClose: 3000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        theme: "colored",
        style: {
          backgroundColor: '#ef4444', // Red background
          color: 'white',             // White text
          borderRadius: '8px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
        }
      });
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskCreated = (newTask: Task) => {
    setTasks([...tasks, newTask]);
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDeleted = (taskId: string) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  const handleToggleCompletion = async (taskId: string) => {
    try {
      const updatedTask = await TaskService.toggleTaskCompletion(userId, taskId);
      setTasks(tasks.map(task => task.id === taskId ? updatedTask : task));
      toast.info(`"${updatedTask.title}" ${updatedTask.completed ? 'completed' : 'marked as pending'}!`, {
        position: "top-center",
        autoClose: 2000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        theme: "colored",
        style: {
          backgroundColor: '#8b5cf6', // Purple background
          color: 'white',             // White text
          borderRadius: '8px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
        }
      });
    } catch (err) {
      toast.error('Failed to update task. Please try again.', {
        position: "top-center",
        autoClose: 3000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        theme: "colored",
        style: {
          backgroundColor: '#ef4444', // Red background
          color: 'white',             // White text
          borderRadius: '8px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
        }
      });
      console.error(err);
    }
  };

  // Calculate summary statistics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.completed).length;
  const pendingTasks = totalTasks - completedTasks;

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900">
        <div className="text-2xl font-semibold text-white">Loading tasks...</div>
      </div>
    );
  }


  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900 p-4 md:p-6">
      <div className="max-w-7xl mx-auto">
        {/* Welcome Header */}
        <header className="mb-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-blue-400 mb-2">Welcome to Your Task Dashboard</h1>
          <p className="text-xl text-indigo-300">Manage your tasks efficiently and boost your productivity</p>
        </header>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6 shadow-lg">
            <h3 className="text-gray-400 text-sm uppercase tracking-wider">Total Tasks</h3>
            <p className="text-3xl font-bold text-white mt-2">{totalTasks}</p>
          </div>

          <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6 shadow-lg">
            <h3 className="text-gray-400 text-sm uppercase tracking-wider">Completed</h3>
            <p className="text-3xl font-bold text-green-400 mt-2">{completedTasks}</p>
          </div>

          <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6 shadow-lg">
            <h3 className="text-gray-400 text-sm uppercase tracking-wider">Pending</h3>
            <p className="text-3xl font-bold text-blue-400 mt-2">{pendingTasks}</p>
          </div>
        </div>

        {/* Main Content Split Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left: My Tasks List - taking 8 out of 12 columns (2/3 of the space) */}
          <div className="bg-gray-800/30 backdrop-blur-sm border border-gray-700/50 rounded-2xl p-6 shadow-xl lg:col-span-8">
            <h2 className="text-2xl font-bold text-white mb-6">My Tasks</h2>

            {tasks.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <div className="bg-gray-700/50 p-6 rounded-full mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-white">No tasks yet</h3>
                <p className="text-gray-400 mt-2">Create your first task to get started</p>
              </div>
            ) : (
              <div className="space-y-4 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
                {tasks.map(task => (
                  <TaskItem
                    key={task.id}
                    task={task}
                    userId={userId}
                    onTaskUpdated={handleTaskUpdated}
                    onTaskDeleted={handleTaskDeleted}
                    onToggleCompletion={handleToggleCompletion}
                  />
                ))}
              </div>
            )}
          </div>

          {/* Right: Create New Task Form - taking 4 out of 12 columns (1/3 of the space) */}
          <div className="bg-gray-800/30 backdrop-blur-sm border border-gray-700/50 rounded-2xl p-6 shadow-xl lg:col-span-4">
            <h2 className="text-2xl font-bold text-white mb-6">Create New Task</h2>
            <TaskForm userId={userId} onTaskCreated={handleTaskCreated} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskList;