/**
 * Module IA - BigRAG + Voice
 * ==========================
 * Exports centralisés pour les composants IA
 */

// Types
export type {
  Country,
  ChatMode,
  MessageRole,
  Language,
  RAGSource,
  RAGContext,
  BigRAGApiResponse,
  VoiceAgentApiResponse,
  ChatMessage,
  MessageMeta,
  ChatState,
  BigRAGChatProps,
  CountrySelectorProps,
  MessageBubbleProps,
  SourceListProps,
  VoiceControlsProps,
  CountryOption,
} from "./types";

export { COUNTRY_OPTIONS, generateId, getCountryEmoji, getCountryLabel } from "./types";

// Components
export { CountrySelector, CountrySelectorDropdown } from "./CountrySelector";
export { MessageBubble } from "./MessageBubble";
export { SourceList } from "./SourceList";
export { VoiceControls, AudioVisualizer } from "./VoiceControls";
export { BigRAGChat } from "./BigRAGChat";
export { BigRAGPage, BigRAGStandalonePage } from "./BigRAGPage";

// Default export
export { BigRAGPage as default } from "./BigRAGPage";
