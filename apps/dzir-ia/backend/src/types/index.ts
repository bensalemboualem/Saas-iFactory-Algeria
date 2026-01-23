import { z } from 'zod';

// ============ Auth Types ============
export interface JWTPayload {
  sub: string; // user ID
  email: string;
  plan: 'free' | 'pro' | 'enterprise';
  iat: number;
  exp: number;
}

export interface AuthContext {
  userId: string;
  email: string;
  plan: string;
}

// ============ Credits Types ============
export interface CreditsResponse {
  available: number;
  used: number;
  limit: number;
}

// ============ Collection Types ============
export const CollectionSchema = z.object({
  id: z.string(),
  name: z.string().min(1).max(100),
  description: z.string().optional(),
  color: z.string().optional(),
  icon: z.string().optional(),
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime(),
});

export type Collection = z.infer<typeof CollectionSchema>;

// ============ Document Types ============
export const DocumentSchema = z.object({
  id: z.string(),
  collectionId: z.string(),
  title: z.string(),
  sourceType: z.enum(['url', 'pdf', 'text', 'image', 'audio']),
  sourceUrl: z.string().optional(),
  content: z.string(),
  summary: z.string().optional(),
  metadata: z.record(z.unknown()).optional(),
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime(),
});

export type Document = z.infer<typeof DocumentSchema>;

// ============ Chunk Types ============
export const ChunkSchema = z.object({
  id: z.string(),
  documentId: z.string(),
  content: z.string(),
  embedding: z.array(z.number()).optional(),
  position: z.number(),
  metadata: z.record(z.unknown()).optional(),
});

export type Chunk = z.infer<typeof ChunkSchema>;

// ============ Search Types ============
export const SearchRequestSchema = z.object({
  query: z.string().min(1),
  collectionIds: z.array(z.string()).optional(),
  limit: z.number().min(1).max(50).default(10),
  threshold: z.number().min(0).max(1).default(0.7),
});

// For GET requests, query params are strings - use coerce
export const SearchQuerySchema = z.object({
  query: z.string().min(1),
  collectionIds: z.string().transform((s) => s.split(',')).optional(),
  limit: z.coerce.number().min(1).max(50).default(10),
  threshold: z.coerce.number().min(0).max(1).default(0.7),
});

export type SearchRequest = z.infer<typeof SearchRequestSchema>;

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

// ============ Ask Types ============
export const AskRequestSchema = z.object({
  query: z.string().min(1),
  collectionIds: z.array(z.string()).optional(),
  model: z.string().default('gpt-4o-mini'),
  systemPrompt: z.string().optional(),
  maxTokens: z.number().min(100).max(4096).default(2048).optional(),
});

export type AskRequest = z.infer<typeof AskRequestSchema>;

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
export const CaptureRequestSchema = z.object({
  collectionId: z.string(),
  sourceType: z.enum(['url', 'pdf', 'text']),
  sourceUrl: z.string().url().optional(),
  content: z.string().optional(),
  title: z.string().optional(),
  // For PDF: base64-encoded PDF content
  pdfBase64: z.string().optional(),
  // Original filename (for PDFs)
  filename: z.string().optional(),
});

export type CaptureRequest = z.infer<typeof CaptureRequestSchema>;

// ============ Sync Types ============
export const SyncItemSchema = z.object({
  id: z.string(),
  type: z.enum(['collection', 'document', 'chunk']),
  action: z.enum(['create', 'update', 'delete']),
  data: z.record(z.unknown()),
  timestamp: z.string().datetime(),
  clientId: z.string(),
});

export type SyncItem = z.infer<typeof SyncItemSchema>;

export const SyncRequestSchema = z.object({
  items: z.array(SyncItemSchema),
  lastSyncTimestamp: z.string().datetime().optional(),
});

export type SyncRequest = z.infer<typeof SyncRequestSchema>;
