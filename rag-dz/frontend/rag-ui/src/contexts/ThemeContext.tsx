import React, { useEffect, useState, createContext, useContext } from 'react';
type Theme = 'dark' | 'light';
interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
}
const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Apply theme to DOM - sync with IAFactory landing page
const applyTheme = (newTheme: Theme) => {
  // Apply to both body and html for consistency with landing page
  document.body.setAttribute('data-theme', newTheme);
  document.documentElement.setAttribute('data-theme', newTheme);
  // Also toggle .dark class for Tailwind
  if (newTheme === 'dark') {
    document.body.classList.add('dark');
    document.documentElement.classList.add('dark');
  } else {
    document.body.classList.remove('dark');
    document.documentElement.classList.remove('dark');
  }
};

export const ThemeProvider: React.FC<{
  children: React.ReactNode;
}> = ({ children }) => {
  // Read from localStorage immediately to avoid flash (use iafactory_theme key)
  const [theme, setTheme] = useState<Theme>(() => {
    const savedTheme = localStorage.getItem('iafactory_theme') as Theme | null;
    return savedTheme || 'dark';
  });
  useEffect(() => {
    // Apply theme to DOM
    applyTheme(theme);

    // Save to localStorage with iafactory_theme key for consistency
    localStorage.setItem('iafactory_theme', theme);
  }, [theme]);
  return <ThemeContext.Provider value={{
    theme,
    setTheme
  }}>
      {children}
    </ThemeContext.Provider>;
};
export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};