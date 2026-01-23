// D:\iafactorychatgpt\dzir-ia\frontend\src\api\client.ts
import type {
  Collection,
  Document,
  SearchResponse,
  AskResponse,
  CaptureRequest,
  SyncItem,
  ApiErrorDetails,
} from "../types";

// ===== API BASE =====
// DEV: always use same-origin proxy (/api) to avoid CORS issues.
// PROD: use VITE_API_URL if set, otherwise /api (reverse proxy).
export const API_BASE: string = import.meta.env.DEV
  ? "/api"
  : (import.meta.env.VITE_API_URL || "/api");

// Health origin (optional)
export const API_ORIGIN: string = import.meta.env.DEV
  ? ""
  : (import.meta.env.VITE_API_ORIGIN || "");

/**
 * Custom API Error with typed details for handling 402/429/503
 */
class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public details?: ApiErrorDetails
  ) {
    super(message);
    this.name = "ApiError";
  }

  isInsufficientCredits(): boolean {
    return this.status === 402 && this.details?.error === "INSUFFICIENT_CREDITS";
  }

  isRateLimited(): boolean {
    return this.status === 429 && this.details?.error === "RATE_LIMITED";
  }

  isServiceUnavailable(): boolean {
    return this.status === 503;
  }

  getRetryAfter(): number | null {
    if (this.isRateLimited() && this.details?.retryAfter) return this.details.retryAfter;
    return null;
  }

  getRequiredCredits(): number | null {
    if (this.isInsufficientCredits() && this.details?.required) return this.details.required;
    return null;
  }

  getBalance(): number | null {
    if (this.isInsufficientCredits() && this.details?.balance !== undefined) return this.details.balance;
    return null;
  }
}

// ===== Auth token =====
// In dev, backend requires "Bearer ..." even with AUTH_BYPASS.
// If no token is stored, fallback to "dev".
function getAuthToken(): string | null {
  const stored = localStorage.getItem("token");
  if (stored && stored.trim()) return stored.trim();
  return import.meta.env.DEV ? "dev" : null;
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = getAuthToken();

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  // Some endpoints may return empty body
  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new ApiError(res.status, data?.error || data?.message || "Request failed", data);
  }

  return data as T;
}

// ============ Collections API ============
export const collectionsApi = {
  create: (data: { color?: string; description?: string; icon?: string, name: string; }) =>
    request<{ collection: Collection }>("/collections", {
      body: JSON.stringify(data),
      method: "POST",
    }),

  delete: (id: string) =>
    request<{ success: boolean }>(`/collections/${id}`, { method: "DELETE" }),

  get: (id: string) =>
    request<{ collection: Collection; documentsCount: number }>(`/collections/${id}`),

  list: () => request<{ collections: Collection[]; count: number }>("/collections"),
};

// ============ Documents API ============
export const documentsApi = {
  delete: (id: string) => request<{ success: boolean }>(`/documents/${id}`, { method: "DELETE" }),

  get: (id: string) => request<{ document: Document }>(`/documents/${id}`),

  list: (collectionId?: string) => {
    const params = collectionId ? `?collectionId=${encodeURIComponent(collectionId)}` : "";
    return request<{ count: number, documents: Document[]; }>(`/documents${params}`);
  },
};

// ============ Capture API ============
export const captureApi = {
  capture: (data: CaptureRequest) =>
    request<{
      chunksCount: number;
      document: Document;
      embeddingsTokensUsed: number;
      message: string;
      vectorIndexDisabled: boolean;
      vectorIndexed: boolean;
    }>("/capture", {
      body: JSON.stringify(data),
      method: "POST",
    }),
};

// ============ Search API ============
export const searchApi = {
  search: (query: string, collectionIds?: string[], limit?: number, threshold?: number) =>
    request<SearchResponse>("/search", {
      body: JSON.stringify({ collectionIds, limit, query, threshold }),
      method: "POST",
    }),
};

// ============ Ask API ============
export const askApi = {
  ask: (query: string, collectionIds?: string[], model?: string, systemPrompt?: string) =>
    request<AskResponse>("/ask", {
      body: JSON.stringify({ collectionIds, model, query, systemPrompt }),
      method: "POST",
    }),
};

// ============ Sync API ============
export const syncApi = {
  status: () =>
    request<{
      lastSyncTimestamp: string | null;
      totalSyncedItems: number;
      userId: string;
    }>("/sync/status"),

  sync: (items: SyncItem[], lastSyncTimestamp?: string) =>
    request<{
      results: Array<{ id: string; message?: string, status: string; }>;
      serverChanges: SyncItem[];
      syncTimestamp: string;
    }>("/sync", {
      body: JSON.stringify({ items, lastSyncTimestamp }),
      method: "POST",
    }),
};

// ============ Health API ============
export const healthApi = {
  check: async () => {
    try {
      const url = API_ORIGIN ? `${API_ORIGIN}/health` : "/health";
      const res = await fetch(url);
      return res.json();
    } catch {
      return { status: "offline" };
    }
  },
};

export { ApiError };
