/**
 * BigRAGChat - Composant principal de chat BIG RAG
 * ================================================
 * Chat professionnel style Perplexity/ChatGPT
 * Connecté à /api/rag/multi/query et /api/voice/agent/text
 */

import React, { useState, useRef, useEffect, useCallback } from "react";
import type {
  BigRAGChatProps,
  ChatMessage,
  ChatState,
  ChatMode,
  Country,
  RAGSource,
  BigRAGApiResponse,
  VoiceAgentApiResponse,
} from "./types";
import { generateId, COUNTRY_OPTIONS } from "./types";
import { CountrySelector } from "./CountrySelector";
import { MessageBubble } from "./MessageBubble";
import { SourceList } from "./SourceList";
import { VoiceControls } from "./VoiceControls";

// Configuration API
const API_BASE_URL = "/api";

export const BigRAGChat: React.FC<BigRAGChatProps> = ({
  defaultCountry = "DZ",
  enableVoice = false,
  maxHistory = 50,
  defaultMode = "bigrag",
  className = "",
  welcomeMessage,
  onMessageSent,
  onError,
}) => {
  // ========== STATE ==========
  const [state, setState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    selectedCountry: defaultCountry,
    mode: defaultMode,
    lastSources: [],
    error: undefined,
  });
  
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // ========== HELPERS ==========
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [state.messages, scrollToBottom]);

  // Auto-resize textarea
  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    // Auto-resize
    e.target.style.height = "auto";
    e.target.style.height = Math.min(e.target.scrollHeight, 200) + "px";
  };

  // ========== API CALLS ==========
  const callBigRAGAPI = async (
    query: string,
    country: Country
  ): Promise<BigRAGApiResponse> => {
    const response = await fetch(`${API_BASE_URL}/rag/multi/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query,
        country: country === "AUTO" ? undefined : country,
        limit: 5,
        threshold: 0.3,
      }),
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  };

  const callVoiceAgentAPI = async (
    text: string,
    country: Country
  ): Promise<VoiceAgentApiResponse> => {
    const response = await fetch(`${API_BASE_URL}/voice/agent/text`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text,
        country: country === "AUTO" ? "DZ" : country,
        language: "fr",
      }),
    });

    if (!response.ok) {
      throw new Error(`Voice API Error: ${response.status}`);
    }

    return response.json();
  };

  // ========== SEND MESSAGE ==========
  const sendMessage = async () => {
    const trimmedInput = input.trim();
    if (!trimmedInput || state.isLoading) return;

    const startTime = Date.now();
    const userMessage: ChatMessage = {
      id: generateId(),
      role: "user",
      content: trimmedInput,
      timestamp: new Date(),
      meta: {
        country: state.selectedCountry,
        language: "fr",
        mode: state.mode,
      },
    };

    // Add user message and clear input
    setState((prev) => ({
      ...prev,
      messages: [...prev.messages.slice(-maxHistory + 1), userMessage],
      isLoading: true,
      error: undefined,
    }));
    setInput("");
    if (inputRef.current) {
      inputRef.current.style.height = "auto";
    }

    try {
      let assistantContent = "";
      let sources: RAGSource[] = [];
      let detectedCountry = state.selectedCountry;

      if (state.mode === "bigrag" || state.mode === "hybrid") {
        // Call BIG RAG API
        const ragResponse = await callBigRAGAPI(trimmedInput, state.selectedCountry);
        
        // Extract answer from response
        if (ragResponse.answer) {
          assistantContent = ragResponse.answer;
        } else if (ragResponse.results && ragResponse.results.length > 0) {
          // Build answer from results
          assistantContent = ragResponse.results
            .map((r, i) => `**${i + 1}.** ${r.content}`)
            .join("\n\n");
        }

        // Extract sources
        sources = (ragResponse.results || []).map((r) => ({
          id: r.id || generateId(),
          title: r.title || "Document",
          content: r.content,
          snippet: r.content.slice(0, 200) + (r.content.length > 200 ? "..." : ""),
          score: r.score,
          country: (r.country as Country) || state.selectedCountry,
          theme: r.theme,
          tags: r.tags,
          source_url: r.source_url,
          display_name: r.display_name,
          date: r.date,
        }));

        detectedCountry = ragResponse.detected_country || state.selectedCountry;
      }

      if (state.mode === "voice" || state.mode === "hybrid") {
        // Call Voice Agent API
        const voiceResponse = await callVoiceAgentAPI(trimmedInput, state.selectedCountry);
        
        if (state.mode === "voice") {
          assistantContent = voiceResponse.response || voiceResponse.text || "";
        } else {
          // Hybrid: append voice response
          if (voiceResponse.response) {
            assistantContent += `\n\n---\n\n**🎙️ Agent Vocal:**\n${voiceResponse.response}`;
          }
        }
      }

      const latencyMs = Date.now() - startTime;

      const assistantMessage: ChatMessage = {
        id: generateId(),
        role: "assistant",
        content: assistantContent || "Désolé, je n'ai pas trouvé d'information pertinente.",
        timestamp: new Date(),
        sources,
        meta: {
          country: detectedCountry,
          language: "fr",
          mode: state.mode,
          latencyMs,
        },
      };

      setState((prev) => ({
        ...prev,
        messages: [...prev.messages, assistantMessage],
        isLoading: false,
        lastSources: sources,
        selectedCountry: detectedCountry !== "AUTO" ? detectedCountry : prev.selectedCountry,
      }));

      onMessageSent?.(userMessage, assistantMessage);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Erreur inconnue";
      
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
        messages: [
          ...prev.messages,
          {
            id: generateId(),
            role: "assistant",
            content: `❌ Erreur: ${errorMessage}`,
            timestamp: new Date(),
            isError: true,
            meta: { country: state.selectedCountry, language: "fr", mode: state.mode },
          },
        ],
      }));

      onError?.(error instanceof Error ? error : new Error(errorMessage));
    }
  };

  // ========== KEY HANDLERS ==========
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // ========== MODE TOGGLE ==========
  const toggleMode = (newMode: ChatMode) => {
    setState((prev) => ({ ...prev, mode: newMode }));
  };

  // ========== CLEAR CHAT ==========
  const clearChat = () => {
    setState((prev) => ({
      ...prev,
      messages: [],
      lastSources: [],
      error: undefined,
    }));
  };

  // ========== RENDER ==========
  return (
    <div
      className={`flex flex-col h-full rounded-2xl shadow-xl overflow-hidden ${className}`}
      style={{ background: 'var(--card)', color: 'var(--text)' }}
    >
      {/* ===== HEADER ===== */}
      <div
        className="flex items-center justify-between px-4 py-3"
        style={{ background: 'var(--card)', borderBottom: '1px solid var(--border)' }}
      >
        <div className="flex items-center gap-3">
          {/* Mode selector */}
          <div className="flex rounded-lg p-1" style={{ background: 'var(--bg)' }}>
            <button
              onClick={() => toggleMode("bigrag")}
              className="px-3 py-1 text-sm rounded-md transition-all"
              style={{
                background: state.mode === "bigrag" ? 'var(--card)' : 'transparent',
                color: state.mode === "bigrag" ? 'var(--iaf-green)' : 'var(--iaf-text-secondary)',
              }}
            >
              📚 RAG
            </button>
            <button
              onClick={() => toggleMode("voice")}
              className="px-3 py-1 text-sm rounded-md transition-all"
              style={{
                background: state.mode === "voice" ? 'var(--card)' : 'transparent',
                color: state.mode === "voice" ? 'var(--iaf-green)' : 'var(--iaf-text-secondary)',
              }}
            >
              🎙️ Agent
            </button>
            <button
              onClick={() => toggleMode("hybrid")}
              className="px-3 py-1 text-sm rounded-md transition-all"
              style={{
                background: state.mode === "hybrid" ? 'var(--card)' : 'transparent',
                color: state.mode === "hybrid" ? 'var(--iaf-green)' : 'var(--iaf-text-secondary)',
              }}
            >
              🔀 Hybride
            </button>
          </div>

          {/* Country selector */}
          <CountrySelector
            selectedCountry={state.selectedCountry}
            onCountryChange={(country) => setState((prev) => ({ ...prev, selectedCountry: country }))}
            size="sm"
          />
        </div>

        <div className="flex items-center gap-2">
          {/* Voice controls (placeholder) */}
          {enableVoice && <VoiceControls disabled={!enableVoice} />}

          {/* Clear button */}
          {state.messages.length > 0 && (
            <button
              onClick={clearChat}
              className="p-2 rounded-lg transition-all"
              style={{ color: 'var(--iaf-text-secondary)' }}
              title="Effacer la conversation"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </button>
          )}
        </div>
      </div>

      {/* ===== MESSAGES ===== */}
      <div className="flex-1 p-4 space-y-4" style={{ background: '#020617', overflowY: 'auto', scrollbarWidth: 'none', msOverflowStyle: 'none' }}>
        {/* Welcome message */}
        {state.messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center p-8">
            <div className="text-6xl mb-4">🤖</div>
            <h2 className="text-2xl font-bold mb-2" style={{ color: 'var(--text)' }}>
              {welcomeMessage || "Assistant IA iaFactory"}
            </h2>
            <p className="max-w-md" style={{ color: 'var(--iaf-text-secondary)' }}>
              Posez vos questions sur la fiscalité, le juridique ou l'administratif
              en Algérie 🇩🇿 ou en Suisse 🇨🇭
            </p>

            {/* Quick prompts */}
            <div className="flex flex-wrap justify-center gap-2 mt-6">
              {[
                "Quels sont les impôts en Algérie ?",
                "Comment créer une SARL en Suisse ?",
                "Quel est le SMIG algérien ?",
              ].map((prompt) => (
                <button
                  key={prompt}
                  onClick={() => {
                    setInput(prompt);
                    inputRef.current?.focus();
                  }}
                  className="px-4 py-2 text-sm rounded-xl transition-all"
                  style={{ background: 'var(--card)', color: 'var(--iaf-text-secondary)', border: '1px solid var(--border)' }}
                >
                  {prompt}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Message list */}
        {state.messages.map((message, index) => (
          <div key={message.id}>
            <MessageBubble
              message={message}
              isLatest={index === state.messages.length - 1}
              showMeta
              onRetry={
                message.isError
                  ? () => {
                      // Retry last user message
                      const lastUserMessage = state.messages
                        .slice()
                        .reverse()
                        .find((m) => m.role === "user");
                      if (lastUserMessage) {
                        setInput(lastUserMessage.content);
                        sendMessage();
                      }
                    }
                  : undefined
              }
            />
            
            {/* Show sources after assistant message */}
            {message.role === "assistant" && message.sources && message.sources.length > 0 && (
              <div className="ml-0 mt-2">
                <SourceList
                  sources={message.sources}
                  maxVisible={3}
                  collapsedByDefault
                />
              </div>
            )}
          </div>
        ))}

        {/* Loading indicator */}
        {state.isLoading && (
          <MessageBubble
            message={{
              id: "loading",
              role: "assistant",
              content: "",
              timestamp: new Date(),
            }}
            isLoading
          />
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* ===== INPUT ===== */}
      <div className="p-4" style={{ background: 'var(--card)', borderTop: '1px solid var(--border)' }}>
        {/* Error display */}
        {state.error && (
          <div className="mb-3 p-3 rounded-lg text-sm flex items-center gap-2" style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--iaf-red)', color: 'var(--iaf-red)' }}>
            <span>⚠️</span>
            <span>{state.error}</span>
            <button
              onClick={() => setState((prev) => ({ ...prev, error: undefined }))}
              className="ml-auto"
              style={{ color: 'var(--iaf-red)' }}
            >
              ✕
            </button>
          </div>
        )}

        <div className="flex items-end gap-3">
          <textarea
            ref={inputRef}
            value={input}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder={`Posez votre question (${COUNTRY_OPTIONS.find((c) => c.value === state.selectedCountry)?.label || "Global"})...`}
            disabled={state.isLoading}
            rows={1}
            className="flex-1 px-4 py-3 rounded-xl resize-none focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed"
            style={{
              background: '#1e293b',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              color: '#f8fafc',
            }}
          />

          <button
            onClick={sendMessage}
            disabled={!input.trim() || state.isLoading}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '48px',
              height: '48px',
              borderRadius: '12px',
              background: '#00a651',
              border: 'none',
              cursor: (!input.trim() || state.isLoading) ? 'not-allowed' : 'pointer',
              opacity: (!input.trim() || state.isLoading) ? 0.6 : 1,
            }}
          >
            {state.isLoading ? (
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style={{ animation: 'spin 1s linear infinite' }}>
                <circle cx="12" cy="12" r="10" stroke="#ffffff" strokeWidth="4" opacity="0.3" />
                <path fill="#ffffff" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
            ) : (
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M22 2L11 13" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            )}
          </button>
        </div>

        {/* Mode indicator */}
        <div className="mt-2 flex items-center justify-between text-xs" style={{ color: 'var(--iaf-text-muted)' }}>
          <span>
            Mode:{" "}
            <span className="font-medium" style={{ color: 'var(--iaf-green)' }}>
              {state.mode === "bigrag" && "📚 BIG RAG"}
              {state.mode === "voice" && "🎙️ Agent Vocal"}
              {state.mode === "hybrid" && "🔀 Hybride"}
            </span>
          </span>
          <span>Entrée pour envoyer, Shift+Entrée pour nouvelle ligne</span>
        </div>
      </div>
    </div>
  );
};

export default BigRAGChat;
