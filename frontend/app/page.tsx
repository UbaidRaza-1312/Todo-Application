'use client';

import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  const handleStartClick = () => {
    router.push('/auth/login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900 flex flex-col">
      <div className="flex-grow flex items-center justify-center px-4 py-12">
        <div className="max-w-4xl w-full text-center">
          <h1 className="text-5xl md:text-7xl font-bold text-blue-400 mb-6">
            Todo App
          </h1>

          <p className="text-xl md:text-2xl text-indigo-200 mb-10 max-w-2xl mx-auto">
            Organize your life, boost your productivity, and achieve your goals with our intuitive task management solution.
          </p>

          <button
            onClick={handleStartClick}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-8 rounded-full text-lg transition-all duration-300 transform hover:scale-105 shadow-lg shadow-indigo-500/30"
          >
            Get Started
          </button>
        </div>
      </div>

      <div className="py-16 px-4 bg-black/20">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-white mb-12">Powerful Features for Maximum Productivity</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6 shadow-lg">
              <div className="text-indigo-400 mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Task Management</h3>
              <p className="text-gray-300">Create, organize, and prioritize your tasks with ease. Track your progress and stay on top of your goals.</p>
            </div>

            <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6 shadow-lg">
              <div className="text-indigo-400 mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Time Tracking</h3>
              <p className="text-gray-300">Monitor how much time you spend on each task. Optimize your schedule and improve your efficiency.</p>
            </div>

            <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6 shadow-lg">
              <div className="text-indigo-400 mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Secure & Private</h3>
              <p className="text-gray-300">Your data is protected with industry-standard encryption. Rest assured that your tasks remain private.</p>
            </div>
          </div>
        </div>
      </div>

      <div className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-white mb-12">Why Choose Our Todo App?</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-10 items-center">
            <div>
              <h3 className="text-2xl font-bold text-indigo-300 mb-4">Boost Your Productivity</h3>
              <p className="text-gray-300 mb-4">
                Our intuitive interface helps you organize tasks efficiently, set priorities, and track your progress.
                With smart notifications and deadline reminders, you'll never miss an important task again.
              </p>
              <p className="text-gray-300">
                Collaborate seamlessly with team members, share tasks, and monitor project progress in real-time.
                Increase your productivity by up to 40% with our streamlined workflow.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-5 shadow-lg">
                <div className="text-green-400 text-3xl font-bold mb-2">99.9%</div>
                <div className="text-gray-300 text-sm">Uptime Guarantee</div>
              </div>

              <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-5 shadow-lg">
                <div className="text-blue-400 text-3xl font-bold mb-2">24/7</div>
                <div className="text-gray-300 text-sm">Customer Support</div>
              </div>

              <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-5 shadow-lg">
                <div className="text-purple-400 text-3xl font-bold mb-2">Free</div>
                <div className="text-gray-300 text-sm">Forever Plan</div>
              </div>

              <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-5 shadow-lg">
                <div className="text-yellow-400 text-3xl font-bold mb-2">Sync</div>
                <div className="text-gray-300 text-sm">Across Devices</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <footer className="py-6 text-center text-gray-400 bg-gray-800/80 backdrop-blur-md border-t border-gray-700/50">
        <p>© {new Date().getFullYear()} Todo App. All rights reserved.</p>
      </footer>
    </div>
  );
}