'use client';

import { useChat } from 'ai/react';
import FormulaLibrary from './components/FormulaLibrary';
import LevelSelector from './components/LevelSelector';
import { useUsageLimit } from '../motivation/hooks/useUsageLimit';
import UsageLimitBanner from '../motivation/components/UsageLimitBanner';
import LeadCaptureModal from '../motivation/components/LeadCaptureModal';
import TypingIndicator from '../motivation/components/TypingIndicator';

export default function TuteurMathsPage() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat/tuteur-maths',
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

  const SUGGESTED_QUESTIONS = [
    "Comment résoudre une équation du 1er degré?",
    "Explique-moi le théorème de Pythagore",
    "Comment calculer l'aire d'un triangle?",
    "C'est quoi une dérivée?",
  ];

  const handleSuggestionClick = (question: string) => {
    if (!canSendMessage()) {
      showLeadCapture();
      return;
    }

    const syntheticEvent = {
      preventDefault: () => {},
    } as React.FormEvent;

    handleInputChange({
      target: { value: question },
    } as React.ChangeEvent<HTMLInputElement>);

    setTimeout(() => {
      handleSubmit(syntheticEvent);
      incrementUsage();
    }, 100);
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      {/* Header */}
      <header className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <span>📐</span>
                <span>Prof. Karim</span>
              </h1>
              <p className="text-sm text-slate-600 dark:text-slate-400">
                Ton tuteur de mathématiques personnel
              </p>
            </div>
            <a
              href="/"
              className="text-sm text-purple-600 dark:text-purple-400 hover:underline"
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
          {/* Left Sidebar - Formulas Library */}
          <div className="lg:col-span-1">
            <div className="sticky top-24 h-[calc(100vh-200px)] overflow-hidden card">
              <FormulaLibrary />
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
                    <div className="text-6xl mb-4">📐</div>
                    <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
                      Salut! Je suis Prof. Karim
                    </h2>
                    <p className="text-slate-600 dark:text-slate-400 mb-6 max-w-md mx-auto">
                      Ton tuteur de maths personnel. Pose tes questions, envoie un exercice, ou demande une explication. Je suis là pour t'aider à réussir!
                    </p>

                    {/* Suggested Questions */}
                    <div className="space-y-2 max-w-lg mx-auto">
                      <p className="text-sm text-slate-500 dark:text-slate-400 mb-3">
                        Questions fréquentes:
                      </p>
                      {SUGGESTED_QUESTIONS.map((question, index) => (
                        <button
                          key={index}
                          onClick={() => handleSuggestionClick(question)}
                          className="w-full text-left px-4 py-3 bg-purple-50 dark:bg-purple-900/20 hover:bg-purple-100 dark:hover:bg-purple-900/30 rounded-lg transition-colors text-sm text-slate-700 dark:text-slate-300"
                        >
                          💬 {question}
                        </button>
                      ))}
                    </div>

                    <div className="grid grid-cols-2 gap-3 max-w-lg mx-auto text-sm mt-6">
                      <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg text-left">
                        <span className="font-semibold text-blue-700 dark:text-blue-300">🎯 BEM/BAC</span>
                        <p className="text-slate-600 dark:text-slate-400 text-xs mt-1">Préparation examens</p>
                      </div>
                      <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg text-left">
                        <span className="font-semibold text-green-700 dark:text-green-300">✍️ Étape par étape</span>
                        <p className="text-slate-600 dark:text-slate-400 text-xs mt-1">Explications détaillées</p>
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
                          ? 'bg-purple-500 text-white'
                          : 'bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700'
                      }`}
                    >
                      <div className="flex items-start space-x-2">
                        <span className="text-2xl">
                          {message.role === 'user' ? '👤' : '📐'}
                        </span>
                        <div className="flex-1 whitespace-pre-wrap font-mono text-sm">
                          {message.content}
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
                        ? "Pose ta question ou colle ton exercice..."
                        : "Limite atteinte - Passe à Premium pour continuer"
                    }
                    disabled={!canSendMessage() || isLoading}
                    rows={3}
                    className="input-field flex-1 disabled:opacity-50 disabled:cursor-not-allowed resize-none font-mono text-sm"
                  />
                  <button
                    type="submit"
                    disabled={!input.trim() || !canSendMessage() || isLoading}
                    className="btn-primary px-6 disabled:opacity-50 disabled:cursor-not-allowed self-end"
                  >
                    {isLoading ? '...' : 'Envoyer'}
                  </button>
                </div>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-2 text-center">
                  💡 Prof. Karim t'explique étape par étape
                </p>
              </form>
            </div>
          </div>

          {/* Right Sidebar - Level Selector */}
          <div className="lg:col-span-1 space-y-6">
            <LevelSelector />

            {/* Tips Card */}
            <div className="card p-4">
              <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-3">
                💡 Conseils
              </h3>
              <div className="space-y-3 text-sm text-slate-600 dark:text-slate-400">
                <div className="flex items-start space-x-2">
                  <span>✓</span>
                  <p>Copie ton exercice complet</p>
                </div>
                <div className="flex items-start space-x-2">
                  <span>✓</span>
                  <p>Demande des explications étape par étape</p>
                </div>
                <div className="flex items-start space-x-2">
                  <span>✓</span>
                  <p>N'hésite pas à poser des questions</p>
                </div>
                <div className="flex items-start space-x-2">
                  <span>✓</span>
                  <p>Toujours vérifier le résultat!</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Lead Capture Modal */}
      <LeadCaptureModal isOpen={showModal} onClose={hideModal} />
    </div>
  );
}
