import { useState } from "react";
import axios from "axios";
import Chat from './components/Chat';
import config from './config'; // Import the config

export default function App() {
  return (
    <div className="min-h-screen bg-gray-900 p-4 md:p-8">
      <h1 className="text-3xl md:text-4xl font-bold text-center mb-6 md:mb-10 text-white flex items-center justify-center gap-3">
        <span>⚡</span> AIOps Copilot
        {config.ENV !== "production" && (
          <span className="text-sm bg-yellow-500 text-black px-2 py-1 rounded">
            {config.ENV}
          </span>
        )}
      </h1>
      <div className="max-w-4xl mx-auto h-[calc(100vh-120px)]">
        <Chat />
      </div>
    </div>
  );
}