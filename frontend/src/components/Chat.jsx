import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import config from '../config'; // Import the config

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [attachment, setAttachment] = useState(null);
  const [conversationContext, setConversationContext] = useState({
    logs: [],
    analyses: [],
    currentTopic: null
  });
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setAttachment(file);
      setInput(`Analyze logs from ${file.name}`);
    }
  };

  const handleSend = async () => {
    if ((!input.trim() && !attachment) || isLoading) return;

    setIsLoading(true);
    const userMessage = input.trim();
    setInput('');

    try {
      // Read file content if present (so we can store locally)
      let fileContent = '';
      if (attachment) {
        fileContent = await attachment.text();
      }

      setMessages(prev => [...prev, {
        role: 'user',
        content: userMessage + (attachment ? ` (with file: ${attachment.name})` : '')
      }]);

      let response;

      if (attachment) {
        const formData = new FormData();
        formData.append("file", attachment);

        response = await axios.post(`${config.API_BASE}/analyze-logs-upload`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });

        // update conversation context
        setConversationContext(prev => ({
          ...prev,
          logs: [...prev.logs, { filename: attachment.name, content: fileContent }],
          analyses: [...prev.analyses, response.data.result],
          currentTopic: attachment.name
        }));

        setAttachment(null);
        if (fileInputRef.current) fileInputRef.current.value = '';
      } else {
        response = await axios.post(`${config.API_BASE}/copilot-chat`, {
          message: userMessage,
          context: conversationContext
        });
      }

      const assistantText = response?.data?.result || response?.data?.analysis || response?.data?.response || 'No response received';

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: assistantText,
        type: response?.data?.type || 'info'
      }]);

    } catch (error) {
      console.error('Error details:', error.response || error);
      const errMsg = error.response?.data?.detail || error.response?.data?.result || error.message || 'Unknown error occurred';
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Error: ${errMsg}`,
        type: 'error'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center p-6">
      <div className="flex flex-col w-full max-w-2xl h-[640px] bg-gray-800 rounded-xl shadow-lg">
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-3 ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700 text-white'
                }`}
              >
                <div className="prose prose-invert prose-p:my-1 prose-li:my-0 prose-ul:my-1 max-w-none">
                  <ReactMarkdown
                    components={{
                      p: ({ children }) => <p className="my-1">{children}</p>,
                      ul: ({ children }) => <ul className="my-1 space-y-1">{children}</ul>,
                      li: ({ children }) => <li className="my-0">{children}</li>,
                    }}
                  >
                    {message.content}
                  </ReactMarkdown>
                </div>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div className="p-4 border-t border-gray-700">
          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileUpload}
                className="hidden"
                accept=".txt,.log"
              />
              <button
                onClick={() => fileInputRef.current?.click()}
                className="px-3 py-1 bg-gray-700 text-white rounded hover:bg-gray-600"
              >
                {attachment ? '📎 ' + attachment.name : '📎 Attach Log'}
              </button>
              {attachment && (
                <button
                  onClick={() => {
                    setAttachment(null);
                    if (fileInputRef.current) fileInputRef.current.value = '';
                  }}
                  className="px-2 py-1 text-gray-400 hover:text-white"
                >
                  ✕
                </button>
              )}
            </div>
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                className="flex-1 p-2 bg-gray-700 text-white rounded-lg border border-gray-600"
                placeholder="Ask me anything... (e.g., 'deploy nginx:latest' or 'analyze auth logs')"
                disabled={isLoading}
              />
              <button
                onClick={handleSend}
                disabled={isLoading}
                className={`px-4 py-2 bg-blue-600 text-white rounded-lg ${isLoading ? 'opacity-50' : 'hover:bg-blue-700'}`}
              > 
                {isLoading ? 'Sending...' : 'Send'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}