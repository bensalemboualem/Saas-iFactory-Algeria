import React, { useState, useRef, useEffect } from 'react';

// ============================================
// Types
// ============================================
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: ContextSource[];
  meta?: ResponseMeta;
}

interface ContextSource {
  title: string;
  snippet: string;
  source_name: string;
  source_url?: string;
  date?: string;
}

interface ResponseMeta {
  latency_ms: number;
  model: string;
}

interface RAGResponse {
  answer: string;
  sources: ContextSource[];
  processing_time?: number;
  confidence?: number;
}

interface MiniRAGChatProps {
  /** Nombre max de requêtes en mode démo (défaut: 3) */
  maxMessages?: number;
  /** URL de l'API (défaut: /api/rag/query) */
  apiUrl?: string;
  /** Pays pour les filtres (défaut: DZ) */
  country?: string;
  /** Placeholder du champ de saisie */
  placeholder?: string;
  /** Titre du chat */
  title?: string;
  /** Afficher les sources */
  showSources?: boolean;
  /** Mode compact */
  compact?: boolean;
  /** Callback quand limite atteinte */
  onLimitReached?: () => void;
}

// ============================================
// Composant Principal
// ============================================
export const MiniRAGChat: React.FC<MiniRAGChatProps> = ({
  maxMessages = 3,
  apiUrl = '/api/rag/query',
  country = 'DZ',
  placeholder = 'Posez votre question sur la réglementation algérienne...',
  title = '🤖 Assistant IA - Démo',
  showSources = true,
  compact = false,
  onLimitReached,
}) => {
  // State
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [remainingCount, setRemainingCount] = useState(maxMessages);
  
  // Refs
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll vers le bas
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Générer un ID unique
  const generateId = () => `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

  // Appel API RAG
  const callRAGAPI = async (query: string): Promise<RAGResponse> => {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        top_k: 5,
        filters: { country },
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Erreur ${response.status}`);
    }

    return response.json();
  };

  // Soumettre une question
  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();
    
    const query = input.trim();
    if (!query || isLoading || remainingCount <= 0) return;

    // Reset error
    setError(null);

    // Ajouter message utilisateur
    const userMessage: Message = {
      id: generateId(),
      role: 'user',
      content: query,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    // Appel API
    setIsLoading(true);
    try {
      const data = await callRAGAPI(query);

      // Ajouter réponse IA
      const assistantMessage: Message = {
        id: generateId(),
        role: 'assistant',
        content: data.answer,
        timestamp: new Date(),
        sources: data.sources,
        meta: data.processing_time ? { latency_ms: data.processing_time * 1000 } : undefined,
      };
      setMessages(prev => [...prev, assistantMessage]);

      // Décrémenter le compteur
      const newCount = remainingCount - 1;
      setRemainingCount(newCount);
      
      if (newCount <= 0 && onLimitReached) {
        onLimitReached();
      }

    } catch (err) {
      console.error('Erreur RAG:', err);
      setError(
        err instanceof Error 
          ? err.message 
          : 'Impossible de contacter l\'IA pour le moment.'
      );
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  // Gérer Enter pour soumettre
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  // Limite atteinte ?
  const isLimitReached = remainingCount <= 0;

  return (
    <div className={`
      bg-slate-900 border border-slate-700 rounded-2xl overflow-hidden
      shadow-xl shadow-black/20
      ${compact ? 'max-w-md' : 'max-w-2xl'} w-full
    `}>
      {/* Header */}
      <div className="bg-gradient-to-r from-emerald-600 to-purple-600 px-4 py-3 flex items-center justify-between">
        <h3 className="text-white font-semibold text-sm flex items-center gap-2">
          {title}
        </h3>
        <span className="text-white/80 text-xs bg-white/20 px-2 py-1 rounded-full">
          {remainingCount} essai{remainingCount !== 1 ? 's' : ''} restant{remainingCount !== 1 ? 's' : ''}
        </span>
      </div>

      {/* Messages */}
      <div className={`
        overflow-y-auto p-4 space-y-4 bg-slate-800/50
        ${compact ? 'h-64' : 'h-80'}
      `}>
        {messages.length === 0 && (
          <div className="text-center text-slate-400 py-8">
            <div className="text-4xl mb-3">💬</div>
            <p className="text-sm">Posez votre première question à l'IA</p>
            <p className="text-xs mt-1 text-slate-500">
              Exemples : fiscalité, droit du travail, import/export...
            </p>
          </div>
        )}

        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`
              max-w-[85%] rounded-2xl px-4 py-3
              ${msg.role === 'user' 
                ? 'bg-emerald-600 text-white rounded-br-md' 
                : 'bg-slate-700 text-slate-100 rounded-bl-md'}
            `}>
              {/* Contenu */}
              <p className="text-sm whitespace-pre-wrap leading-relaxed">
                {msg.content}
              </p>

              {/* Sources (pour les réponses IA) */}
              {showSources && msg.role === 'assistant' && msg.sources && msg.sources.length > 0 && (
                <div className="mt-3 pt-3 border-t border-slate-600">
                  <p className="text-xs text-slate-400 mb-2">📚 Sources :</p>
                  <div className="space-y-1">
                    {msg.sources.slice(0, 3).map((src, idx) => (
                      <div key={idx} className="text-xs text-slate-300 bg-slate-800/50 rounded px-2 py-1">
                        {src.source_url ? (
                          <a 
                            href={src.source_url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="text-emerald-400 hover:underline"
                          >
                            {src.source_name || src.title}
                          </a>
                        ) : (
                          <span>{src.source_name || src.title}</span>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Meta (latence) */}
              {msg.role === 'assistant' && msg.meta && (
                <p className="text-xs text-slate-500 mt-2">
                  ⚡ {msg.meta.latency_ms}ms • {msg.meta.model}
                </p>
              )}
            </div>
          </div>
        ))}

        {/* Loading */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-slate-700 text-slate-100 rounded-2xl rounded-bl-md px-4 py-3">
              <div className="flex items-center gap-2">
                <div className="flex space-x-1">
                  <span className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                  <span className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                  <span className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                </div>
                <span className="text-sm text-slate-400">L'IA réfléchit...</span>
              </div>
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="bg-red-900/30 border border-red-700 text-red-300 rounded-lg px-4 py-3 text-sm">
            ⚠️ {error}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 bg-slate-900 border-t border-slate-700">
        {isLimitReached ? (
          <div className="text-center py-4">
            <p className="text-amber-400 text-sm mb-3">
              🔒 Limite de démo atteinte
            </p>
            <a 
              href="/auth/register" 
              className="inline-block bg-gradient-to-r from-emerald-500 to-purple-500 text-white px-6 py-2 rounded-lg font-semibold text-sm hover:opacity-90 transition-opacity"
            >
              Créer un compte gratuit →
            </a>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="flex gap-3">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={placeholder}
              disabled={isLoading}
              rows={1}
              className="
                flex-1 bg-slate-800 border border-slate-600 rounded-xl px-4 py-3
                text-white placeholder-slate-400 text-sm
                focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500
                disabled:opacity-50 resize-none
              "
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="
                bg-gradient-to-r from-emerald-500 to-emerald-600 
                hover:from-emerald-400 hover:to-emerald-500
                text-white px-5 py-3 rounded-xl font-semibold text-sm
                disabled:opacity-50 disabled:cursor-not-allowed
                transition-all duration-200
                flex items-center gap-2
              "
            >
              {isLoading ? (
                <span className="animate-spin">⏳</span>
              ) : (
                <>
                  <span>Envoyer</span>
                  <span>→</span>
                </>
              )}
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

export default MiniRAGChat;
