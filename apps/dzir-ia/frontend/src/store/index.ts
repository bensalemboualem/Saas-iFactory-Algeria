import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Collection, Document, TimelineEvent, UIState, SyncItem } from '../types';
import { nanoid } from 'nanoid';

// ============ Collections Store ============
interface CollectionsState {
  collections: Collection[];
  loading: boolean;
  error: string | null;
  setCollections: (collections: Collection[]) => void;
  addCollection: (collection: Collection) => void;
  removeCollection: (id: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useCollectionsStore = create<CollectionsState>((set) => ({
  collections: [],
  loading: false,
  error: null,
  setCollections: (collections) => set({ collections }),
  addCollection: (collection) =>
    set((state) => ({ collections: [collection, ...state.collections] })),
  removeCollection: (id) =>
    set((state) => ({
      collections: state.collections.filter((c) => c.id !== id),
    })),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}));

// ============ Documents Store ============
interface DocumentsState {
  documents: Document[];
  currentDocument: Document | null;
  loading: boolean;
  setDocuments: (documents: Document[]) => void;
  addDocument: (document: Document) => void;
  removeDocument: (id: string) => void;
  setCurrentDocument: (document: Document | null) => void;
  setLoading: (loading: boolean) => void;
}

export const useDocumentsStore = create<DocumentsState>((set) => ({
  documents: [],
  currentDocument: null,
  loading: false,
  setDocuments: (documents) => set({ documents }),
  addDocument: (document) =>
    set((state) => ({ documents: [document, ...state.documents] })),
  removeDocument: (id) =>
    set((state) => ({
      documents: state.documents.filter((d) => d.id !== id),
    })),
  setCurrentDocument: (document) => set({ currentDocument: document }),
  setLoading: (loading) => set({ loading }),
}));

// ============ Timeline Store ============
interface TimelineState {
  events: TimelineEvent[];
  addEvent: (event: Omit<TimelineEvent, 'id' | 'timestamp'>) => void;
  clearEvents: () => void;
}

export const useTimelineStore = create<TimelineState>()(
  persist(
    (set) => ({
      events: [],
      addEvent: (event) =>
        set((state) => ({
          events: [
            {
              ...event,
              id: nanoid(),
              timestamp: new Date().toISOString(),
            },
            ...state.events,
          ].slice(0, 100), // Keep last 100 events
        })),
      clearEvents: () => set({ events: [] }),
    }),
    {
      name: 'dzir-timeline',
    }
  )
);

// ============ Sync Queue Store ============
interface SyncQueueState {
  queue: SyncItem[];
  lastSyncTimestamp: string | null;
  isSyncing: boolean;
  clientId: string;
  addToQueue: (item: Omit<SyncItem, 'id' | 'timestamp' | 'clientId'>) => void;
  removeFromQueue: (id: string) => void;
  clearQueue: () => void;
  setLastSyncTimestamp: (timestamp: string) => void;
  setIsSyncing: (syncing: boolean) => void;
}

export const useSyncQueueStore = create<SyncQueueState>()(
  persist(
    (set, get) => ({
      queue: [],
      lastSyncTimestamp: null,
      isSyncing: false,
      clientId: nanoid(),
      addToQueue: (item) =>
        set((state) => ({
          queue: [
            ...state.queue,
            {
              ...item,
              id: nanoid(),
              timestamp: new Date().toISOString(),
              clientId: get().clientId,
            },
          ],
        })),
      removeFromQueue: (id) =>
        set((state) => ({
          queue: state.queue.filter((i) => i.id !== id),
        })),
      clearQueue: () => set({ queue: [] }),
      setLastSyncTimestamp: (timestamp) => set({ lastSyncTimestamp: timestamp }),
      setIsSyncing: (syncing) => set({ isSyncing: syncing }),
    }),
    {
      name: 'dzir-sync-queue',
    }
  )
);

// ============ UI Store ============
interface UIStore extends UIState {
  toggleSidebar: () => void;
  toggleAskPanel: () => void;
  setCurrentView: (view: UIState['currentView']) => void;
  setSelectedCollectionId: (id: string | null) => void;
}

export const useUIStore = create<UIStore>()(
  persist(
    (set) => ({
      sidebarOpen: true,
      askPanelExpanded: false,
      currentView: 'collections',
      selectedCollectionId: null,
      toggleSidebar: () =>
        set((state) => ({ sidebarOpen: !state.sidebarOpen })),
      toggleAskPanel: () =>
        set((state) => ({ askPanelExpanded: !state.askPanelExpanded })),
      setCurrentView: (view) => set({ currentView: view }),
      setSelectedCollectionId: (id) => set({ selectedCollectionId: id }),
    }),
    {
      name: 'dzir-ui',
    }
  )
);

// ============ Search Store ============
interface SearchState {
  query: string;
  results: import('../types').SearchResult[];
  loading: boolean;
  setQuery: (query: string) => void;
  setResults: (results: import('../types').SearchResult[]) => void;
  setLoading: (loading: boolean) => void;
  clearSearch: () => void;
}

export const useSearchStore = create<SearchState>((set) => ({
  query: '',
  results: [],
  loading: false,
  setQuery: (query) => set({ query }),
  setResults: (results) => set({ results }),
  setLoading: (loading) => set({ loading }),
  clearSearch: () => set({ query: '', results: [] }),
}));
