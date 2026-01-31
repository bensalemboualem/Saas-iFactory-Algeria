import { useEffect, useState, useCallback } from 'react';

export type Theme = 'dark' | 'light';

// Couleurs centralisées - Synchronisées avec Home.tsx CSS vars
export const themeColors = {
  dark: {
    bgPrimary: '#0A0F1A',
    bgSecondary: '#111827',
    bgCard: 'rgba(255,255,255,0.06)',
    textPrimary: '#F8FAFC',
    textSecondary: 'rgba(248,250,252,0.80)',
    textMuted: 'rgba(248,250,252,0.65)',
    borderColor: 'rgba(255,255,255,0.10)',
    inputBg: '#111827',
  },
  light: {
    bgPrimary: '#F6F3EE',
    bgSecondary: '#FBF8F3',
    bgCard: '#EDE9E3',
    textPrimary: '#141414',
    textSecondary: 'rgba(20,20,20,0.80)',
    textMuted: 'rgba(20,20,20,0.62)',
    borderColor: 'rgba(20,20,20,0.10)',
    inputBg: '#EDE9E3',
  },
} as const;

// Couleurs d'accent (vert Algérie)
export const accentColors = {
  primary: '#1C7A5F',
  secondary: '#22C55E',
  dark: '#006233',
  light: '#2ECC71',
  gradient: 'linear-gradient(135deg, #1C7A5F, #22C55E)',
  gradientDark: 'linear-gradient(135deg, #006233, #1C7A5F)',
} as const;

// Type pour les couleurs (union des deux thèmes)
export type ThemeColors = typeof themeColors.dark | typeof themeColors.light;

interface UseThemeReturn {
  theme: Theme;
  isDark: boolean;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
  colors: ThemeColors;
  accent: typeof accentColors;
}

export function useTheme(): UseThemeReturn {
  const [theme, setThemeState] = useState<Theme>(() => {
    // Initialisation côté client uniquement
    if (typeof window !== 'undefined') {
      return (localStorage.getItem('theme') as Theme) || 'dark';
    }
    return 'dark';
  });

  // Synchroniser avec le DOM au montage
  useEffect(() => {
    const savedTheme = (localStorage.getItem('theme') as Theme) || 'dark';
    setThemeState(savedTheme);
    document.documentElement.dataset.theme = savedTheme;
  }, []);

  // Écouter les changements de thème externes (autres composants/onglets)
  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'theme' && e.newValue) {
        const newTheme = e.newValue as Theme;
        setThemeState(newTheme);
        document.documentElement.dataset.theme = newTheme;
      }
    };

    // Observer pour les changements dans le même onglet
    const observer = new MutationObserver(() => {
      const currentTheme = document.documentElement.dataset.theme as Theme;
      if (currentTheme && currentTheme !== theme) {
        setThemeState(currentTheme);
      }
    });

    window.addEventListener('storage', handleStorageChange);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-theme'],
    });

    return () => {
      window.removeEventListener('storage', handleStorageChange);
      observer.disconnect();
    };
  }, [theme]);

  const setTheme = useCallback((newTheme: Theme) => {
    setThemeState(newTheme);
    document.documentElement.dataset.theme = newTheme;
    localStorage.setItem('theme', newTheme);
  }, []);

  const toggleTheme = useCallback(() => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
  }, [theme, setTheme]);

  const isDark = theme === 'dark';
  const colors = isDark ? themeColors.dark : themeColors.light;

  return {
    theme,
    isDark,
    toggleTheme,
    setTheme,
    colors,
    accent: accentColors,
  };
}

export default useTheme;
