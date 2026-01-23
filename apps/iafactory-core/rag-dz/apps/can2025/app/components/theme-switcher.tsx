
'use client'

import * as React from 'react'
import { useTheme } from 'next-themes'
import { Sun, Moon } from 'lucide-react'

export function ThemeSwitcher() {
  const { theme, setTheme } = useTheme()

  return (
    <button
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      className="p-2 rounded-full bg-white/10 hover:bg-white/20 transition-colors"
      aria-label="Toggle theme"
    >
      <Sun className="h-6 w-6 text-white dark:hidden" />
      <Moon className="h-6 w-6 text-white hidden dark:block" />
    </button>
  )
}
