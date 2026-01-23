'use client';

import { useChat } from 'ai/react';
import { useEffect, useRef, useState } from 'react';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';
import UsageLimitBanner from './UsageLimitBanner';
import LeadCaptureModal from './LeadCaptureModal';
import { useUsageLimit } from '../hooks/useUsageLimit';

const SUGGESTED_QUESTIONS = [
  "Comment gérer mon stress au travail ?",
  "J'ai du mal à me motiver, des conseils ?",
  "Comment améliorer ma productivité ?",
  "Je procrastine beaucoup, aide-moi !",
  "Comment fixer des objectifs réalistes ?",
];

export default function ChatInterface() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat/motivation',
    onError: (error) => {
      console.error('Chat error:', error);
    },
  });

  const { messagesUsedToday, canSendMessage, incrementUsage, showLeadCapture, showModal, hideModal } = useUsageLimit();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [showSuggestions, setShowSuggestions] = useState(true);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Hide suggestions after first message
  useEffect(() => {
    if (messages.length > 0) {
      setShowSuggestions(false);
    }
  }, [messages]);

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

  const handleSuggestionClick = (question: string) => {
    if (!canSendMessage()) {
      showLeadCapture();
      return;
    }

    // Create a synthetic event
    const syntheticEvent = {
      preventDefault: () => {},
    } as React.FormEvent;

    handleInputChange({
      target: { value: question },
    } as React.ChangeEvent<HTMLInputElement>);

    // Submit after a small delay to let input update
    setTimeout(() => {
      handleSubmit(syntheticEvent);
      incrementUsage();
    }, 100);
  };

  return (
    <div className="card h-[calc(100vh-240px)] flex flex-col">
      {/* Usage Limit Banner */}
      <UsageLimitBanner messagesUsed={messagesUsedToday} />

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Welcome Message */}
        {messages.length === 0 && (
          <div className="text-center py-8">
            <div className="text-6xl mb-4 animate-bounce">💪</div>
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
              Salut! Je suis Amine
            </h2>
            <p className="text-slate-600 dark:text-slate-400 mb-6 max-w-md mx-auto">
              Ton coach bien-être personnel. Je suis là pour t'accompagner dans ton développement personnel.
              Comment tu te sens aujourd'hui ?
            </p>

            {/* Suggested Questions */}
            {showSuggestions && (
              <div className="space-y-2 max-w-lg mx-auto">
                <p className="text-sm text-slate-500 dark:text-slate-400 mb-3">
                  Questions fréquentes:
                </p>
                {SUGGESTED_QUESTIONS.map((question, index) => (
                  <button
                    key={index}
                    onClick={() => handleSuggestionClick(question)}
                    className="w-full text-left px-4 py-3 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 rounded-lg transition-colors text-sm"
                  >
                    💬 {question}
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Messages */}
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}

        {/* Typing Indicator */}
        {isLoading && <TypingIndicator />}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form onSubmit={handleFormSubmit} className="p-4 border-t border-slate-200 dark:border-slate-800">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={handleInputChange}
            placeholder={
              canSendMessage()
                ? "Écris ton message ici..."
                : "Limite atteinte - Passe à Premium pour continuer"
            }
            disabled={!canSendMessage() || isLoading}
            className="input-field flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
          />
          <button
            type="submit"
            disabled={!input.trim() || !canSendMessage() || isLoading}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <span className="flex items-center space-x-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                    fill="none"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
              </span>
            ) : (
              <span>Envoyer</span>
            )}
          </button>
        </div>

        <p className="text-xs text-slate-500 dark:text-slate-400 mt-2 text-center">
          💡 Amine t'écoute et t'accompagne avec bienveillance
        </p>
      </form>

      {/* Lead Capture Modal */}
      <LeadCaptureModal isOpen={showModal} onClose={hideModal} />
    </div>
  );
}
