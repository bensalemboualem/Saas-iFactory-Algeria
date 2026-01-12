import { create } from "zustand";
import { persist } from "zustand/middleware";
import { Locale } from "./i18n";

interface User {
  id: string;
  email: string;
  name: string;
  credits: number;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setUser: (user: User | null) => void;
  setToken: (token: string | null) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      setUser: (user) => set({ user, isAuthenticated: !!user }),
      setToken: (token) => set({ token }),
      logout: () => set({ user: null, token: null, isAuthenticated: false }),
    }),
    {
      name: "auth-storage",
    }
  )
);

// Credits store
interface CreditsState {
  balance: number;
  setBalance: (balance: number) => void;
  deductCredits: (amount: number) => void;
  addCredits: (amount: number) => void;
}

export const useCreditsStore = create<CreditsState>((set) => ({
  balance: 0,
  setBalance: (balance) => set({ balance }),
  deductCredits: (amount) => set((state) => ({ balance: state.balance - amount })),
  addCredits: (amount) => set((state) => ({ balance: state.balance + amount })),
}));

// Generation store
interface GenerationTask {
  id: string;
  status: "pending" | "processing" | "completed" | "failed";
  progress: number;
  prompt: string;
  mode: "text-to-video" | "image-to-video";
  videoUrl?: string;
  error?: string;
  createdAt: Date;
}

interface GenerationState {
  tasks: GenerationTask[];
  currentTask: GenerationTask | null;
  addTask: (task: GenerationTask) => void;
  updateTask: (id: string, updates: Partial<GenerationTask>) => void;
  setCurrentTask: (task: GenerationTask | null) => void;
  removeTask: (id: string) => void;
}

export const useGenerationStore = create<GenerationState>((set) => ({
  tasks: [],
  currentTask: null,
  addTask: (task) => set((state) => ({ tasks: [...state.tasks, task] })),
  updateTask: (id, updates) =>
    set((state) => ({
      tasks: state.tasks.map((t) => (t.id === id ? { ...t, ...updates } : t)),
      currentTask:
        state.currentTask?.id === id
          ? { ...state.currentTask, ...updates }
          : state.currentTask,
    })),
  setCurrentTask: (task) => set({ currentTask: task }),
  removeTask: (id) =>
    set((state) => ({ tasks: state.tasks.filter((t) => t.id !== id) })),
}));

// Theme store
interface ThemeStore {
  theme: "dark" | "light";
  setTheme: (theme: "dark" | "light") => void;
  toggleTheme: () => void;
}

export const useThemeStore = create<ThemeStore>()(
  persist(
    (set) => ({
      theme: "dark",
      setTheme: (theme) => set({ theme }),
      toggleTheme: () => set((state) => ({ theme: state.theme === "dark" ? "light" : "dark" })),
    }),
    { name: "iaf-theme" }
  )
);

// Locale store
interface LocaleStore {
  locale: Locale;
  setLocale: (locale: Locale) => void;
}

export const useLocaleStore = create<LocaleStore>()(
  persist(
    (set) => ({
      locale: "fr",
      setLocale: (locale) => set({ locale }),
    }),
    { name: "iaf-locale" }
  )
);

// Settings panel store
interface SettingsStore {
  isOpen: boolean;
  open: () => void;
  close: () => void;
  toggle: () => void;
}

export const useSettingsStore = create<SettingsStore>((set) => ({
  isOpen: false,
  open: () => set({ isOpen: true }),
  close: () => set({ isOpen: false }),
  toggle: () => set((state) => ({ isOpen: !state.isOpen })),
}));

// Chat help store
interface ChatStore {
  isOpen: boolean;
  messages: { role: "user" | "assistant"; content: string }[];
  open: () => void;
  close: () => void;
  toggle: () => void;
  addMessage: (role: "user" | "assistant", content: string) => void;
  clearMessages: () => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  isOpen: false,
  messages: [],
  open: () => set({ isOpen: true }),
  close: () => set({ isOpen: false }),
  toggle: () => set((state) => ({ isOpen: !state.isOpen })),
  addMessage: (role, content) =>
    set((state) => ({ messages: [...state.messages, { role, content }] })),
  clearMessages: () => set({ messages: [] }),
}));

// Sidebar store
interface SidebarStore {
  isCollapsed: boolean;
  toggle: () => void;
  setCollapsed: (collapsed: boolean) => void;
}

export const useSidebarStore = create<SidebarStore>()(
  persist(
    (set) => ({
      isCollapsed: false,
      toggle: () => set((state) => ({ isCollapsed: !state.isCollapsed })),
      setCollapsed: (collapsed) => set({ isCollapsed: collapsed }),
    }),
    { name: "iaf-sidebar" }
  )
);
