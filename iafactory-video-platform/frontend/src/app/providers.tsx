'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState, useEffect, createContext, useContext } from 'react'
import { Language, getStoredLanguage, setStoredLanguage, getDirection } from '@/lib/i18n'
import { Theme, getStoredTheme, setTheme, initTheme } from '@/lib/theme'

// Context for language
interface LanguageContextType {
  language: Language
  setLanguage: (lang: Language) => void
  dir: 'ltr' | 'rtl'
}

const LanguageContext = createContext<LanguageContextType>({
  language: 'fr',
  setLanguage: () => {},
  dir: 'ltr'
})

export const useLanguage = () => useContext(LanguageContext)

// Context for theme
interface ThemeContextType {
  theme: Theme
  setTheme: (theme: Theme) => void
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContextType>({
  theme: 'dark',
  setTheme: () => {},
  toggleTheme: () => {}
})

export const useTheme = () => useContext(ThemeContext)

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,
            refetchOnWindowFocus: false,
          },
        },
      })
  )

  const [language, setLanguageState] = useState<Language>('fr')
  const [theme, setThemeState] = useState<Theme>('dark')
  const [mounted, setMounted] = useState(false)

  // Initialize on mount
  useEffect(() => {
    setMounted(true)

    // Initialize theme
    initTheme()
    setThemeState(getStoredTheme())

    // Initialize language
    setLanguageState(getStoredLanguage())

    // Listen for changes
    const handleThemeChange = (e: CustomEvent) => setThemeState(e.detail.theme)
    const handleLangChange = (e: CustomEvent) => setLanguageState(e.detail.lang)

    window.addEventListener('themeChanged', handleThemeChange as EventListener)
    window.addEventListener('languageChanged', handleLangChange as EventListener)

    return () => {
      window.removeEventListener('themeChanged', handleThemeChange as EventListener)
      window.removeEventListener('languageChanged', handleLangChange as EventListener)
    }
  }, [])

  // Update document when language changes
  useEffect(() => {
    if (mounted) {
      const dir = getDirection(language)
      document.documentElement.setAttribute('dir', dir)
      document.documentElement.setAttribute('lang', language)
    }
  }, [language, mounted])

  const handleSetLanguage = (lang: Language) => {
    setStoredLanguage(lang)
    setLanguageState(lang)
  }

  const handleSetTheme = (newTheme: Theme) => {
    setTheme(newTheme)
    setThemeState(newTheme)
  }

  const handleToggleTheme = () => {
    const newTheme: Theme = theme === 'dark' ? 'light' : 'dark'
    handleSetTheme(newTheme)
  }

  // Prevent hydration mismatch
  if (!mounted) {
    return (
      <QueryClientProvider client={queryClient}>
        <div style={{ visibility: 'hidden' }}>{children}</div>
      </QueryClientProvider>
    )
  }

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeContext.Provider value={{ theme, setTheme: handleSetTheme, toggleTheme: handleToggleTheme }}>
        <LanguageContext.Provider value={{ language, setLanguage: handleSetLanguage, dir: getDirection(language) }}>
          {children}
        </LanguageContext.Provider>
      </ThemeContext.Provider>
    </QueryClientProvider>
  )
}
