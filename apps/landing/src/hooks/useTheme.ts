import { useEffect, useState, useCallback } from 'react';

export type Theme = 'dark' | 'light';

// Couleurs centralisées - Source unique de vérité
export const themeColors = {
  dark: {
    bgPrimary: '#1a1a1a',
    bgSecondary: '#0d0d0d',
    bgCard: '#262626',
    textPrimary: '#f0f0f0',
    textSecondary: '#B0B0B0',
    textMuted: '#A3A3A3',
    borderColor: 'rgba(255, 255, 255, 0.12)',
    inputBg: '#1f1f1f',
  },
  light: {
    bgPrimary: '#FAF9F7',
    bgSecondary: '#f5f5f5',
    bgCard: '#ffffff',
    textPrimary: '#1F1F1F',
    textSecondary: '#4A4A4A',
    textMuted: '#5D5D5D',
    borderColor: 'rgba(0, 0, 0, 0.08)',
    inputBg: '#ffffff',
  },
} as const;

// Couleurs d'accent (vert Algérie)
export const accentColors = {
  primary: '#00A86B',
  secondary: '#2ECC71',
  dark: '#008B5E',
  light: '#58D68D',
  gradient: 'linear-gradient(135deg, #00A86B, #2ECC71)',
  gradientDark: 'linear-gradient(135deg, #008B5E, #00A86B)',
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
