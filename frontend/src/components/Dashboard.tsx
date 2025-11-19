import React, { useState, useEffect, useRef } from 'react';
import { chatAPI } from '../services/api';
import { ChatMessage } from '../types';
import { Send, Bot, User, Loader2 } from 'lucide-react';

const Dashboard: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || loading) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await chatAPI.sendQuery(inputMessage);
      console.log('Chat API Response:', response);
      console.log('Response content:', response.response);
      
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.response || response.reply || 'No response received',
        timestamp: new Date().toISOString(),
      };
      console.log('Assistant message:', assistantMessage);
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error: any) {
      console.error('Chat error:', error);
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${error.response?.data?.detail || error.message || 'Please try again.'}`,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-full flex flex-col">
      <div className="glass-card rounded-2xl p-6 flex-1 flex flex-col">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            AI Business Copilot
          </h1>
          <p className="text-gray-600 mt-2">
            Ask me anything about your business - invoices, GST, expenses, and more!
          </p>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto mb-6 space-y-4">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <Bot size={64} className="mx-auto text-blue-500 mb-4" />
                <h3 className="text-xl font-semibold text-gray-700 mb-2">
                  Welcome to SmartBiz AI
                </h3>
                <p className="text-gray-500">
                  Start a conversation by asking a question below
                </p>
                <div className="mt-6 space-y-2 text-left max-w-md mx-auto">
                  <p className="text-sm text-gray-600">Try asking:</p>
                  <ul className="text-sm text-gray-500 space-y-1">
                    <li>• "Create an invoice for ABC Corp worth ₹5000"</li>
                    <li>• "Show me all my invoices"</li>
                    <li>• "Verify GST number 29ABCDE1234F1Z5"</li>
                    <li>• "What's my total revenue this month?"</li>
                  </ul>
                </div>
              </div>
            </div>
          ) : (
            messages.map((message, index) => (
              <div
                key={index}
                className={`flex gap-3 ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                {message.role === 'assistant' && (
                  <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-indigo-600 flex items-center justify-center flex-shrink-0">
                    <Bot size={20} className="text-white" />
                  </div>
                )}
                <div
                  className={`max-w-[70%] rounded-2xl px-4 py-3 ${
                    message.role === 'user'
                      ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white'
                      : 'bg-white/50 backdrop-blur-sm border border-gray-200/50 text-gray-800'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{message.content}</p>
                </div>
                {message.role === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center flex-shrink-0">
                    <User size={20} className="text-gray-700" />
                  </div>
                )}
              </div>
            ))
          )}
          {loading && (
            <div className="flex gap-3 justify-start">
              <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-indigo-600 flex items-center justify-center flex-shrink-0">
                <Bot size={20} className="text-white" />
              </div>
              <div className="bg-white/50 backdrop-blur-sm border border-gray-200/50 rounded-2xl px-4 py-3">
                <Loader2 size={20} className="animate-spin text-blue-500" />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Form */}
        <form onSubmit={handleSendMessage} className="flex gap-3">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message..."
            className="glass-input flex-1"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !inputMessage.trim()}
            className="glass-button px-6 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  );
};

export default Dashboard;
