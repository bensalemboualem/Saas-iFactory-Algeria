'use client';

import { useState } from 'react';
import { useChat } from 'ai/react';
import SnippetsLibrary from './components/SnippetsLibrary';
import QuickActions from './components/QuickActions';
import DevStatsWidget from './components/DevStatsWidget';
import CodeBlock from './components/CodeBlock';
import { useUsageLimit } from '../motivation/hooks/useUsageLimit';
import UsageLimitBanner from '../motivation/components/UsageLimitBanner';
import LeadCaptureModal from '../motivation/components/LeadCaptureModal';
import TypingIndicator from '../motivation/components/TypingIndicator';

export default function DevHelperPage() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat/dev-helper',
    onError: (error) => {
      console.error('Chat error:', error);
    },
  });

  const {
    messagesUsedToday,
    canSendMessage,
    incrementUsage,
    showLeadCapture,
    showModal,
    hideModal,
  } = useUsageLimit();

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!canSendMessage()) {
      showLeadCapture();
      return;
    }

    if (input.trim()) {
      handleSubmit(e);
      incrementUsage();
    }
  };

  const handleQuickAction = (prompt: string) => {
    if (!canSendMessage()) {
      showLeadCapture();
      return;
    }

    const syntheticEvent = {
      preventDefault: () => {},
    } as React.FormEvent;

    const inputEvent = {
      target: { value: prompt },
    } as React.ChangeEvent<HTMLInputElement>;

    handleInputChange(inputEvent);

    setTimeout(() => {
      handleSubmit(syntheticEvent);
      incrementUsage();
    }, 100);
  };

  // Extract code blocks from message content
  const renderMessage = (content: string) => {
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = codeBlockRegex.exec(content)) !== null) {
      // Add text before code block
      if (match.index > lastIndex) {
        parts.push(
          <p key={`text-${lastIndex}`} className="whitespace-pre-wrap">
            {content.slice(lastIndex, match.index)}
          </p>
        );
      }

      // Add code block
      const language = match[1] || 'text';
      const code = match[2].trim();
      parts.push(<CodeBlock key={`code-${match.index}`} code={code} language={language} />);

      lastIndex = match.index + match[0].length;
    }

    // Add remaining text
    if (lastIndex < content.length) {
      parts.push(
        <p key={`text-${lastIndex}`} className="whitespace-pre-wrap">
          {content.slice(lastIndex)}
        </p>
      );
    }

    return parts.length > 0 ? parts : <p className="whitespace-pre-wrap">{content}</p>;
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      {/* Header */}
      <header className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <span>💻</span>
                <span>DevBot</span>
              </h1>
              <p className="text-sm text-slate-600 dark:text-slate-400">
                Ton assistant développeur personnel
              </p>
            </div>
            <a
              href="/"
              className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
            >
              ← Tous les agents
            </a>
          </div>
        </div>
      </header>

      {/* Usage Limit Banner */}
      <UsageLimitBanner messagesUsed={messagesUsedToday} />

      {/* Main Content - 3 columns */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Left Sidebar - Snippets Library */}
          <div className="lg:col-span-1">
            <div className="sticky top-24 h-[calc(100vh-200px)] overflow-hidden card">
              <SnippetsLibrary />
            </div>
          </div>

          {/* Center - Chat Interface */}
          <div className="lg:col-span-2">
            <div className="card h-[calc(100vh-200px)] flex flex-col">
              {/* Messages Container */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {/* Welcome Message */}
                {messages.length === 0 && (
                  <div className="text-center py-8">
                    <div className="text-6xl mb-4">💻</div>
                    <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
                      Salut! Je suis DevBot
                    </h2>
                    <p className="text-slate-600 dark:text-slate-400 mb-6 max-w-md mx-auto">
                      Ton senior dev personnel. Colle ton code, explique ton bug, ou demande des conseils. Je suis là pour t'aider!
                    </p>
                    <div className="grid grid-cols-2 gap-3 max-w-lg mx-auto text-sm">
                      <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg text-left">
                        <span className="font-semibold text-blue-700 dark:text-blue-300">🐛 Debug</span>
                        <p className="text-slate-600 dark:text-slate-400 text-xs mt-1">Résous tes bugs rapidement</p>
                      </div>
                      <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg text-left">
                        <span className="font-semibold text-green-700 dark:text-green-300">📖 Explique</span>
                        <p className="text-slate-600 dark:text-slate-400 text-xs mt-1">Comprends ton code profondément</p>
                      </div>
                      <div className="p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg text-left">
                        <span className="font-semibold text-yellow-700 dark:text-yellow-300">⚡ Optimise</span>
                        <p className="text-slate-600 dark:text-slate-400 text-xs mt-1">Code plus performant</p>
                      </div>
                      <div className="p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg text-left">
                        <span className="font-semibold text-purple-700 dark:text-purple-300">💡 Snippets</span>
                        <p className="text-slate-600 dark:text-slate-400 text-xs mt-1">Code prêt à copier</p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Messages */}
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-lg p-4 ${
                        message.role === 'user'
                          ? 'bg-blue-500 text-white'
                          : 'bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700'
                      }`}
                    >
                      <div className="flex items-start space-x-2">
                        <span className="text-2xl">
                          {message.role === 'user' ? '👤' : '💻'}
                        </span>
                        <div className="flex-1 overflow-x-auto">
                          {renderMessage(message.content)}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}

                {/* Typing Indicator */}
                {isLoading && <TypingIndicator />}
              </div>

              {/* Input Form */}
              <form onSubmit={handleFormSubmit} className="p-4 border-t border-slate-200 dark:border-slate-800">
                <div className="flex space-x-2">
                  <textarea
                    value={input}
                    onChange={handleInputChange}
                    placeholder={
                      canSendMessage()
                        ? "Colle ton code ou décris ton problème..."
                        : "Limite atteinte - Passe à Premium pour continuer"
                    }
                    disabled={!canSendMessage() || isLoading}
                    rows={3}
                    className="input-field flex-1 disabled:opacity-50 disabled:cursor-not-allowed resize-none"
                  />
                  <button
                    type="submit"
                    disabled={!input.trim() || !canSendMessage() || isLoading}
                    className="btn-primary px-6 disabled:opacity-50 disabled:cursor-not-allowed self-end"
                  >
                    {isLoading ? '...' : 'Send'}
                  </button>
                </div>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-2 text-center">
                  💡 DevBot t'aide à coder mieux et plus vite
                </p>
              </form>
            </div>
          </div>

          {/* Right Sidebar - Quick Actions + Stats */}
          <div className="lg:col-span-1 space-y-6">
            <QuickActions onActionClick={handleQuickAction} />
            <DevStatsWidget />
          </div>
        </div>
      </div>

      {/* Lead Capture Modal */}
      <LeadCaptureModal isOpen={showModal} onClose={hideModal} />
    </div>
  );
}
