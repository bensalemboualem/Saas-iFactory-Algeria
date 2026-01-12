/**
 * VoiceControls - Contrôles vocaux
 * =================================
 * Placeholder pour les contrôles vocaux (STT/TTS)
 * Sera complété lors de l'intégration voice complète
 */

import React, { useState } from "react";
import type { VoiceControlsProps } from "./types";

export const VoiceControls: React.FC<VoiceControlsProps> = ({
  disabled = true,
  isRecording = false,
  isPlaying = false,
  onStartRecording,
  onStopRecording,
  onPlayAudio,
  lastError,
  className = "",
}) => {
  const [showTooltip, setShowTooltip] = useState(false);

  // Mode placeholder (désactivé par défaut)
  if (disabled) {
    return (
      <div className={`relative ${className}`}>
        <button
          disabled
          className="
            flex items-center gap-2
            px-4 py-2
            bg-gray-200 dark:bg-gray-700
            text-gray-400 dark:text-gray-500
            rounded-xl
            cursor-not-allowed
            opacity-60
          "
          onMouseEnter={() => setShowTooltip(true)}
          onMouseLeave={() => setShowTooltip(false)}
        >
          <span className="text-xl">🎙️</span>
          <span className="text-sm hidden sm:inline">Agent Vocal</span>
        </button>
        
        {/* Tooltip */}
        {showTooltip && (
          <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg whitespace-nowrap shadow-lg z-10">
            🚧 Bientôt disponible
            <div className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-gray-900"></div>
          </div>
        )}
      </div>
    );
  }

  // Mode actif (futur)
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      {/* Bouton Microphone */}
      <button
        onClick={isRecording ? onStopRecording : onStartRecording}
        className={`
          relative
          flex items-center justify-center
          w-12 h-12
          rounded-full
          transition-all duration-300
          ${
            isRecording
              ? "bg-red-500 hover:bg-red-600 text-white animate-pulse"
              : "bg-blue-500 hover:bg-blue-600 text-white"
          }
          shadow-lg hover:shadow-xl
          focus:outline-none focus:ring-4 focus:ring-blue-300
        `}
        title={isRecording ? "Arrêter l'enregistrement" : "Commencer l'enregistrement"}
      >
        {isRecording ? (
          // Stop icon
          <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <rect x="6" y="6" width="12" height="12" rx="2" />
          </svg>
        ) : (
          // Mic icon
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
            />
          </svg>
        )}

        {/* Recording indicator */}
        {isRecording && (
          <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-400 rounded-full animate-ping"></span>
        )}
      </button>

      {/* Bouton lecture audio (si réponse audio disponible) */}
      {onPlayAudio && (
        <button
          onClick={onPlayAudio}
          disabled={isPlaying}
          className={`
            flex items-center justify-center
            w-10 h-10
            rounded-full
            ${
              isPlaying
                ? "bg-green-500 text-white animate-pulse"
                : "bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600"
            }
            transition-all
            focus:outline-none focus:ring-2 focus:ring-green-400
          `}
          title="Écouter la réponse"
        >
          {isPlaying ? (
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z" />
            </svg>
          ) : (
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M8 5v14l11-7z" />
            </svg>
          )}
        </button>
      )}

      {/* Indicateur d'état */}
      {isRecording && (
        <div className="flex items-center gap-2 text-sm text-red-500">
          <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
          <span>Enregistrement...</span>
        </div>
      )}

      {/* Erreur */}
      {lastError && (
        <div className="text-sm text-red-500 flex items-center gap-1">
          ⚠️ {lastError}
        </div>
      )}
    </div>
  );
};

/**
 * Composant de visualisation audio (waveform)
 * Placeholder pour futur
 */
export const AudioVisualizer: React.FC<{ isActive: boolean }> = ({ isActive }) => {
  if (!isActive) return null;

  return (
    <div className="flex items-center gap-0.5 h-8">
      {[...Array(5)].map((_, i) => (
        <div
          key={i}
          className="w-1 bg-blue-500 rounded-full animate-pulse"
          style={{
            height: `${Math.random() * 100}%`,
            animationDelay: `${i * 100}ms`,
          }}
        />
      ))}
    </div>
  );
};

export default VoiceControls;
