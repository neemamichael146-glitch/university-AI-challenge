'use client';

import { useState, useEffect } from 'react';

export default function Home() {
  const [apiStatus, setApiStatus] = useState<'checking' | 'connected' | 'error'>('checking');

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/health`)
      .then((res) => res.ok && setApiStatus('connected'))
      .catch(() => setApiStatus('error'));
  }, []);

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8">
      <div className="max-w-2xl w-full text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">ChuoAI</h1>
        <p className="text-xl text-gray-600 mb-8">
          University Admissions Assistant for Tanzanian Students
        </p>

        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">API Status</h2>
          <div className="flex items-center justify-center gap-2">
            <span
              className={`w-3 h-3 rounded-full ${
                apiStatus === 'connected'
                  ? 'bg-green-500'
                  : apiStatus === 'error'
                  ? 'bg-red-500'
                  : 'bg-yellow-500 animate-pulse'
              }`}
            />
            <span className="text-gray-700 capitalize">{apiStatus}</span>
          </div>
          <p className="text-sm text-gray-500 mt-2">
            Backend: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <a
            href="/chat"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Start Chat
          </a>
          <a
            href="/universities"
            className="bg-gray-100 text-gray-900 px-6 py-3 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Browse Universities
          </a>
        </div>
      </div>
    </main>
  );
}