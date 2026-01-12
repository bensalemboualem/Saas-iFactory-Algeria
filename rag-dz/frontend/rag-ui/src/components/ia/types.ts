/**
 * Types pour BigRAG + Voice Agent
 * ================================
 * Types TypeScript pour l'interface IA iaFactory
 */

// ============================================
// ENUMS
// ============================================

export type Country = "DZ" | "CH" | "GLOBAL" | "AUTO";
export type MessageRole = "user" | "assistant" | "system";
export type ChatMode = "bigrag" | "voice" | "hybrid";
export type Language = "ar" | "fr" | "en" | "de" | "it" | "ar-dz";

// ============================================
// API RESPONSE TYPES
// ============================================

/**
 * Source document retourné par BIG RAG
 */
export interface RAGSource {
  id?: string;
  title?: string;
  content?: string;
  snippet?: string;
  text?: string;
  source_name?: string;
  source?: string;
  source_url?: string;
  url?: string;
  display_name?: string;
  country?: Country;
  date?: string;
  theme?: string;
  score?: number;
  is_official?: boolean;
  tags?: string[];
}

/**
 * Contexte utilisé pour la génération
 */
export interface RAGContext {
  id?: string;
  text: string;
  source: string;
  country: string;
  score: number;
  theme?: string;
  url?: string;
}

/**
 * Réponse de l'API BIG RAG /api/rag/multi/query
 */
export interface BigRAGApiResponse {
  // Réponse principale
  answer: string;
  
  // Résultats de recherche
  results?: Array<{
    id?: string;
    title?: string;
    content: string;
    score?: number;
    country?: string;
    theme?: string;
    tags?: string[];
    source_url?: string;
    display_name?: string;
    date?: string;
  }>;
  
  // Détection pays
  detected_country?: Country;
  country_detected?: Country;
  country_emoji?: string;
  country_confidence?: number;
  
  // Langue
  language?: Language;
  language_detected?: Language;
  
  // Sources et contextes
  sources?: RAGSource[];
  contexts_used?: RAGContext[];
  
  // Métadonnées
  meta?: {
    latency_ms?: number;
    model_used?: string;
    search_time_ms?: number;
    llm_time_ms?: number;
    total_sources?: number;
  };
  
  // Pour compatibilité
  confidence?: number;
  search_mode?: string;
}

/**
 * Réponse de l'API Voice Agent /api/voice/agent/text
 */
export interface VoiceAgentApiResponse {
  // Réponse
  response?: string;
  text?: string;
  response_text?: string;
  response_audio_b64?: string;
  
  // Intent
  intent?: {
    type: string;
    confidence: number;
    entities?: Record<string, string>;
  };
  
  // Conversation
  conversation_id?: string;
  turn_id?: string;
  
  // Pays & langue
  country_detected?: Country;
  language?: Language;
  
  // TTS
  tts_backend?: string;
  voice_used?: string;
  
  // Timing
  latency_ms?: number;
  stt_time_ms?: number;
  nlp_time_ms?: number;
  llm_time_ms?: number;
  tts_time_ms?: number;
}

// ============================================
// CHAT MESSAGE TYPES
// ============================================

/**
 * Métadonnées d'un message
 */
export interface MessageMeta {
  country?: Country;
  country_detected?: Country;
  country_emoji?: string;
  language?: Language;
  latency_ms?: number;
  latencyMs?: number;
  sources?: RAGSource[];
  contexts?: RAGContext[];
  model_used?: string;
  intent?: {
    type: string;
    confidence: number;
  };
  mode?: ChatMode;
}

/**
 * Message dans le chat
 */
export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: Date;
  meta?: MessageMeta;
  sources?: RAGSource[];
  isLoading?: boolean;
  isError?: boolean;
  error?: string;
}

// ============================================
// COMPONENT PROPS
// ============================================

/**
 * Props pour BigRAGChat
 */
export interface BigRAGChatProps {
  /** Pays par défaut */
  defaultCountry?: Country;
  /** Activer les contrôles vocaux */
  enableVoice?: boolean;
  /** Historique max des messages */
  maxHistory?: number;
  /** Mode par défaut */
  defaultMode?: ChatMode;
  /** Titre personnalisé */
  title?: string;
  /** Sous-titre personnalisé */
  subtitle?: string;
  /** Message de bienvenue */
  welcomeMessage?: string;
  /** Classe CSS additionnelle */
  className?: string;
  /** Afficher les sources */
  showSources?: boolean;
  /** Afficher les métadonnées */
  showMeta?: boolean;
  /** Callback après envoi de message */
  onMessageSent?: (userMessage: ChatMessage, assistantMessage: ChatMessage) => void;
  /** Callback en cas d'erreur */
  onError?: (error: Error) => void;
}

/**
 * Props pour CountrySelector
 */
export interface CountrySelectorProps {
  value?: Country;
  selectedCountry?: Country;
  onChange?: (country: Country) => void;
  onCountryChange?: (country: Country) => void;
  disabled?: boolean;
  size?: "sm" | "md" | "lg";
  showFlags?: boolean;
  className?: string;
}

/**
 * Props pour MessageBubble
 */
export interface MessageBubbleProps {
  message: ChatMessage;
  isLatest?: boolean;
  isLoading?: boolean;
  showMeta?: boolean;
  onCopy?: (content: string) => void;
  onRetry?: () => void;
}

/**
 * Props pour SourceList
 */
export interface SourceListProps {
  sources: RAGSource[];
  maxItems?: number;
  maxVisible?: number;
  collapsed?: boolean;
  collapsedByDefault?: boolean;
  onToggle?: () => void;
  className?: string;
}

/**
 * Props pour VoiceControls
 */
export interface VoiceControlsProps {
  disabled?: boolean;
  isRecording?: boolean;
  isPlaying?: boolean;
  onStartRecording?: () => void;
  onStopRecording?: () => void;
  onPlayAudio?: () => void;
  lastError?: string;
  className?: string;
}

// ============================================
// API REQUEST TYPES
// ============================================

/**
 * Requête pour BIG RAG
 */
export interface BigRAGRequest {
  query: string;
  top_k?: number;
  country_hint?: Country | null;
  language_hint?: Language | null;
  use_reranker?: boolean;
  include_global?: boolean;
}

/**
 * Requête pour Voice Agent (texte)
 */
export interface VoiceAgentTextRequest {
  text: string;
  language?: Language;
  country_hint?: Country;
  conversation_id?: string;
  mode?: string;
  enable_tts?: boolean;
}

// ============================================
// UTILITY TYPES
// ============================================

/**
 * État du chat
 */
export interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  selectedCountry: Country;
  mode: ChatMode;
  lastSources: RAGSource[];
  error?: string;
  conversationId?: string;
}

/**
 * Options pour les pays
 */
export interface CountryOption {
  value: Country;
  label: string;
  emoji: string;
  languages: Language[];
}

export const COUNTRY_OPTIONS: CountryOption[] = [
  { value: "AUTO", label: "Détection auto", emoji: "🔍", languages: ["fr", "ar"] },
  { value: "DZ", label: "Business DZ", emoji: "💼", languages: ["ar", "fr", "ar-dz"] },
  { value: "CH", label: "RAG École", emoji: "🎓", languages: ["fr", "ar"] },
  { value: "GLOBAL", label: "RAG Islam", emoji: "☪️", languages: ["ar", "fr", "en"] },
];

/**
 * Génère un ID unique
 */
export function generateId(): string {
  return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Obtient l'emoji du pays
 */
export function getCountryEmoji(country: Country): string {
  const option = COUNTRY_OPTIONS.find(o => o.value === country);
  return option?.emoji || "🌍";
}

/**
 * Obtient le label du pays
 */
export function getCountryLabel(country: Country): string {
  const option = COUNTRY_OPTIONS.find(o => o.value === country);
  return option?.label || country;
}
