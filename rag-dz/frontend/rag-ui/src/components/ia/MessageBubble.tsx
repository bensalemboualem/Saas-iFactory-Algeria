/**
 * MessageBubble - Bulle de message chat
 * ======================================
 * Affiche un message user ou assistant
 */

import React, { useState } from "react";
import type { MessageBubbleProps } from "./types";
import { getCountryEmoji } from "./types";

export const MessageBubble: React.FC<MessageBubbleProps> = ({
  message,
  isLatest = false,
  isLoading: propIsLoading,
  showMeta = true,
  onCopy,
  onRetry,
}) => {
  const [copied, setCopied] = useState(false);
  const isUser = message.role === "user";
  const isSystem = message.role === "system";
  const isAssistant = message.role === "assistant";
  const isLoading = propIsLoading ?? message.isLoading;

  const handleCopy = () => {
    if (onCopy) {
      onCopy(message.content);
    } else {
      navigator.clipboard.writeText(message.content);
    }
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Formatage du contenu avec markdown basique
  const formatContent = (content: string) => {
    // Remplacer les ** par du bold
    let formatted = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Remplacer les * par de l'italique
    formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
    // Remplacer les retours à la ligne
    formatted = formatted.replace(/\n/g, '<br/>');
    return formatted;
  };

  if (isSystem) {
    return (
      <div className="flex justify-center my-2">
        <div className="px-4 py-2 rounded-full text-sm" style={{ background: 'var(--card)', color: 'var(--iaf-text-secondary)' }}>
          ℹ️ {message.content}
        </div>
      </div>
    );
  }

  return (
    <div
      className={`flex w-full mb-4 ${isUser ? "justify-end" : "justify-start"}`}
    >
      <div
        className={`relative max-w-[80%] lg:max-w-[70%] rounded-2xl px-4 py-3 shadow-sm ${isLoading ? "animate-pulse" : ""}`}
        style={{
          background: isUser ? 'var(--iaf-green)' : 'var(--card)',
          color: isUser ? '#ffffff' : 'var(--text)',
          borderRadius: isUser ? '1rem 1rem 0.375rem 1rem' : '1rem 1rem 1rem 0.375rem',
          border: (message.error || message.isError) ? '2px solid var(--iaf-red)' : '1px solid var(--border)',
        }}
      >
        {/* Avatar/Icon */}
        <div
          className={`absolute -top-2 ${isUser ? "-right-2" : "-left-2"} w-8 h-8 rounded-full flex items-center justify-center text-lg shadow-md`}
          style={{ background: isUser ? 'var(--iaf-green)' : 'var(--bg)' }}
        >
          {isUser ? "👤" : "🤖"}
        </div>

        {/* Content */}
        <div className="pt-2">
          {isLoading ? (
            <div className="flex items-center gap-2">
              <div className="flex space-x-1">
                <div className="w-2 h-2 rounded-full animate-bounce" style={{ background: 'var(--iaf-text-secondary)', animationDelay: "0ms" }}></div>
                <div className="w-2 h-2 rounded-full animate-bounce" style={{ background: 'var(--iaf-text-secondary)', animationDelay: "150ms" }}></div>
                <div className="w-2 h-2 rounded-full animate-bounce" style={{ background: 'var(--iaf-text-secondary)', animationDelay: "300ms" }}></div>
              </div>
              <span className="text-sm opacity-70">Réflexion en cours...</span>
            </div>
          ) : (
            <div
              className="prose prose-sm max-w-none"
              style={{ color: 'inherit' }}
              dangerouslySetInnerHTML={{ __html: formatContent(message.content) }}
            />
          )}

          {/* Error */}
          {(message.error || message.isError) && (
            <div className="mt-2 text-sm flex items-center gap-1" style={{ color: 'var(--iaf-red)' }}>
              ⚠️ {message.error || "Une erreur est survenue"}
              {onRetry && (
                <button
                  onClick={() => onRetry()}
                  className="underline"
                  style={{ color: 'var(--iaf-red)' }}
                >
                  Réessayer
                </button>
              )}
            </div>
          )}
        </div>

        {/* Meta info */}
        {showMeta && message.meta && isAssistant && !isLoading && (
          <div className="mt-3 pt-2" style={{ borderTop: '1px solid var(--border)' }}>
            <div className="flex flex-wrap gap-2 text-xs" style={{ color: 'var(--iaf-text-secondary)' }}>
              {(message.meta.country_detected || message.meta.country) && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full" style={{ background: 'var(--bg)' }}>
                  {getCountryEmoji(message.meta.country_detected || message.meta.country || "GLOBAL")}
                  {message.meta.country_detected || message.meta.country}
                </span>
              )}
              {message.meta.language && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full" style={{ background: 'var(--bg)' }}>
                  🗣️ {message.meta.language.toUpperCase()}
                </span>
              )}
              {(message.meta.latency_ms || message.meta.latencyMs) && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full" style={{ background: 'var(--bg)' }}>
                  ⚡ {message.meta.latency_ms || message.meta.latencyMs}ms
                </span>
              )}
              {message.meta.mode && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full" style={{ background: 'rgba(0, 166, 81, 0.1)', color: 'var(--iaf-green)' }}>
                  {message.meta.mode === "bigrag" ? "📚" : message.meta.mode === "voice" ? "🎙️" : "🔀"} {message.meta.mode}
                </span>
              )}
            </div>
          </div>
        )}

        {/* Actions */}
        {isAssistant && !isLoading && (
          <div className="absolute bottom-2 right-2 flex gap-1 opacity-0 hover:opacity-100 transition-opacity">
            <button
              onClick={handleCopy}
              className="p-1.5 rounded-lg"
              style={{ background: 'var(--bg)', color: 'var(--iaf-text-secondary)' }}
              title="Copier"
            >
              {copied ? "✅" : "📋"}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;
