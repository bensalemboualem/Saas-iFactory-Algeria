/**
 * IAFactory Theme System
 * Dark/Light mode with smooth transitions
 */

export type Theme = 'dark' | 'light'

// Get stored theme
export function getStoredTheme(): Theme {
  if (typeof window === 'undefined') return 'dark'
  const stored = localStorage.getItem('iafactory_theme')
  if (stored === 'light' || stored === 'dark') {
    return stored
  }
  // Check system preference
  if (window.matchMedia('(prefers-color-scheme: light)').matches) {
    return 'light'
  }
  return 'dark'
}

// Set theme
export function setTheme(theme: Theme): void {
  if (typeof window === 'undefined') return
  localStorage.setItem('iafactory_theme', theme)
  document.documentElement.setAttribute('data-theme', theme)
  // Dispatch event for other components
  window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }))
}

// Toggle theme
export function toggleTheme(): Theme {
  const current = getStoredTheme()
  const next: Theme = current === 'dark' ? 'light' : 'dark'
  setTheme(next)
  return next
}

// Initialize theme on load
export function initTheme(): void {
  if (typeof window === 'undefined') return
  const theme = getStoredTheme()
  document.documentElement.setAttribute('data-theme', theme)
}
