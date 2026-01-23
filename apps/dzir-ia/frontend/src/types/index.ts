// ============ Collection Types ============
export interface Collection {
  id: string;
  name: string;
  description?: string;
  color?: string;
  icon?: string;
  createdAt: string;
  updatedAt: string;
  documentsCount?: number;
}

// ============ Document Types ============
export interface Document {
  id: string;
  collectionId: string;
  title: string;
  sourceType: 'url' | 'pdf' | 'text' | 'image' | 'audio';
  sourceUrl?: string;
  content: string;
  summary?: string;
  metadata?: Record<string, unknown>;
  createdAt: string;
  updatedAt: string;
}

// ============ Search Types ============
export interface SearchResult {
  documentId: string;
  chunkId: string;
  content: string;
  score: number;
  document: {
    title: string;
    sourceType: string;
    sourceUrl?: string;
  };
}

export interface SearchResponse {
  results: SearchResult[];
  count: number;
  query: string;
}

// ============ Ask Types ============
export interface AskSource {
  index: number;
  documentId: string;
  chunkId: string;
  title: string;
  snippet: string;
  position: number;
  score: number;
  sourceUrl?: string;
}

export interface AskResponse {
  answer: string;
  sources: AskSource[];
  model: string;
  tokensUsed: {
    prompt: number;
    completion: number;
    total: number;
  };
}

// ============ Capture Types ============
export interface CaptureRequest {
  collectionId: string;
  sourceType: 'url' | 'pdf' | 'text';
  sourceUrl?: string;
  content?: string;
  title?: string;
  pdfBase64?: string;
  filename?: string;
}

// ============ API Error Types ============
export interface ApiErrorDetails {
  error: string;
  message?: string;
  required?: number;
  balance?: number;
  bucket?: string;
  limit?: number;
  resetAt?: number;
  retryAfter?: number;
}

// ============ Sync Types ============
export interface SyncItem {
  id: string;
  type: 'collection' | 'document' | 'chunk';
  action: 'create' | 'update' | 'delete';
  data: Record<string, unknown>;
  timestamp: string;
  clientId: string;
}

// ============ Timeline Types ============
export interface TimelineEvent {
  id: string;
  type: 'capture' | 'search' | 'ask' | 'sync';
  title: string;
  description?: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

// ============ UI State Types ============
export interface UIState {
  sidebarOpen: boolean;
  askPanelExpanded: boolean;
  currentView: 'collections' | 'timeline' | 'graph' | 'search';
  selectedCollectionId: string | null;
}
