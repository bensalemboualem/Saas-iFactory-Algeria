'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import {
  Video,
  Menu,
  X,
  Sun,
  Moon,
  Globe,
  ChevronDown,
  Tag,
  Grid,
  Bot,
  GitBranch,
  User,
  Code,
  LogIn,
  Rocket,
  Play
} from 'lucide-react'
import { Language, languageInfo, t, getStoredLanguage, setStoredLanguage } from '@/lib/i18n'
import { Theme, getStoredTheme, toggleTheme } from '@/lib/theme'

interface HeaderProps {
  onLanguageChange?: (lang: Language) => void
  onThemeChange?: (theme: Theme) => void
}

export default function Header({ onLanguageChange, onThemeChange }: HeaderProps) {
  const [language, setLanguage] = useState<Language>('fr')
  const [theme, setThemeState] = useState<Theme>('dark')
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [langMenuOpen, setLangMenuOpen] = useState(false)
  const [profileMode, setProfileMode] = useState<'user' | 'dev'>('user')

  useEffect(() => {
    setLanguage(getStoredLanguage())
    setThemeState(getStoredTheme())

    // Listen for changes
    const handleLangChange = (e: CustomEvent) => setLanguage(e.detail.lang)
    const handleThemeChange = (e: CustomEvent) => setThemeState(e.detail.theme)

    window.addEventListener('languageChanged', handleLangChange as EventListener)
    window.addEventListener('themeChanged', handleThemeChange as EventListener)

    return () => {
      window.removeEventListener('languageChanged', handleLangChange as EventListener)
      window.removeEventListener('themeChanged', handleThemeChange as EventListener)
    }
  }, [])

  const handleLanguageChange = (lang: Language) => {
    setStoredLanguage(lang)
    setLanguage(lang)
    setLangMenuOpen(false)
    onLanguageChange?.(lang)
  }

  const handleThemeToggle = () => {
    const newTheme = toggleTheme()
    setThemeState(newTheme)
    onThemeChange?.(newTheme)
  }

  const isRTL = languageInfo[language].dir === 'rtl'

  return (
    <header
      className="iaf-header"
      dir={isRTL ? 'rtl' : 'ltr'}
    >
      <div className="iaf-header-container">
        {/* Logo */}
        <Link href="/" className="header-logo">
          <div className="w-10 h-10 bg-gradient-to-br from-[#00a651] to-[#00c761] rounded-lg flex items-center justify-center">
            <Video className="w-6 h-6 text-white" />
          </div>
          <span className="logo-text text-lg font-bold">
            <span className="text-[var(--iaf-text-primary)]">IA</span>
            <span className="text-[#00a651]">Factory</span>
            <span className="text-[var(--iaf-text-primary)]"> Video</span>
          </span>
        </Link>

        {/* Main Navigation */}
        <nav className="iaf-nav">
          <Link href="/docs/tarifs" className="iaf-nav-link">
            <Tag className="w-4 h-4" />
            <span>{t('pricing', language)}</span>
          </Link>
          <Link href="/apps" className="iaf-nav-link">
            <Grid className="w-4 h-4" />
            <span>{t('apps', language)}</span>
          </Link>
          <Link href="/agents" className="iaf-nav-link">
            <Bot className="w-4 h-4" />
            <span>{t('ai_agents', language)}</span>
          </Link>
          <Link href="/workflows" className="iaf-nav-link">
            <GitBranch className="w-4 h-4" />
            <span>{t('workflows', language)}</span>
          </Link>
        </nav>

        {/* Header Actions */}
        <div className="iaf-header-actions">
          {/* Profile Toggle */}
          <div className="iaf-profile-toggle">
            <button
              className={`iaf-profile-btn ${profileMode === 'user' ? 'active' : ''}`}
              onClick={() => setProfileMode('user')}
            >
              <User className="w-4 h-4" />
              <span>{t('user', language)}</span>
            </button>
            <button
              className={`iaf-profile-btn ${profileMode === 'dev' ? 'active' : ''}`}
              onClick={() => setProfileMode('dev')}
            >
              <Code className="w-4 h-4" />
              <span>{t('developer', language)}</span>
            </button>
          </div>

          {/* Theme Toggle */}
          <button
            className="iaf-theme-btn"
            onClick={handleThemeToggle}
            aria-label={theme === 'dark' ? t('light_mode', language) : t('dark_mode', language)}
          >
            {theme === 'dark' ? (
              <Sun className="w-5 h-5" />
            ) : (
              <Moon className="w-5 h-5" />
            )}
          </button>

          {/* Language Selector */}
          <div className="iaf-language-selector">
            <button
              className="iaf-lang-btn"
              onClick={() => setLangMenuOpen(!langMenuOpen)}
              aria-expanded={langMenuOpen}
            >
              <Globe className="w-4 h-4" />
              <span className="iaf-lang-label">{language.toUpperCase()}</span>
              <ChevronDown className={`w-3 h-3 transition-transform ${langMenuOpen ? 'rotate-180' : ''}`} />
            </button>

            {langMenuOpen && (
              <div className="iaf-lang-menu show">
                {(Object.keys(languageInfo) as Language[]).map((lang) => (
                  <button
                    key={lang}
                    className={`iaf-lang-option ${language === lang ? 'active' : ''}`}
                    onClick={() => handleLanguageChange(lang)}
                    dir={languageInfo[lang].dir}
                  >
                    <span className="iaf-lang-flag">{languageInfo[lang].flag}</span>
                    <span>{languageInfo[lang].nativeName}</span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Auth Buttons */}
          <div className="iaf-auth-buttons">
            <Link href="/login" className="iaf-btn iaf-btn-secondary">
              <LogIn className="w-4 h-4" />
              <span>{t('login', language)}</span>
            </Link>
            <Link href="/getstarted" className="iaf-btn iaf-btn-primary">
              <Rocket className="w-4 h-4" />
              <span>{t('get_started', language)}</span>
            </Link>
            <Link href="/getstarted" className="iaf-btn iaf-btn-primary iaf-btn-try">
              <Play className="w-4 h-4" />
              <span>{t('try_free', language)}</span>
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="iaf-mobile-menu-btn"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Menu"
          >
            {mobileMenuOpen ? (
              <X className="w-6 h-6" />
            ) : (
              <Menu className="w-6 h-6" />
            )}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="iaf-mobile-menu open">
          <div className="iaf-mobile-menu-header">
            <div className="iaf-mobile-logo">
              <span className="text-2xl">🇩🇿</span>
              <span>IAFactory DZ</span>
            </div>
            <button
              className="iaf-mobile-close"
              onClick={() => setMobileMenuOpen(false)}
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <nav className="iaf-mobile-nav">
            <Link href="/docs/tarifs" className="iaf-mobile-link" onClick={() => setMobileMenuOpen(false)}>
              <Tag className="w-5 h-5" />
              <span>{t('pricing', language)}</span>
            </Link>
            <Link href="/apps" className="iaf-mobile-link" onClick={() => setMobileMenuOpen(false)}>
              <Grid className="w-5 h-5" />
              <span>{t('apps', language)}</span>
            </Link>
            <Link href="/agents" className="iaf-mobile-link" onClick={() => setMobileMenuOpen(false)}>
              <Bot className="w-5 h-5" />
              <span>{t('ai_agents', language)}</span>
            </Link>
            <Link href="/workflows" className="iaf-mobile-link" onClick={() => setMobileMenuOpen(false)}>
              <GitBranch className="w-5 h-5" />
              <span>{t('workflows', language)}</span>
            </Link>

            <div className="iaf-mobile-divider" />

            {/* Mobile Language Options */}
            <div className="px-4 py-2">
              <p className="text-sm text-[var(--iaf-text-muted)] mb-2">Language</p>
              <div className="flex flex-wrap gap-2">
                {(Object.keys(languageInfo) as Language[]).map((lang) => (
                  <button
                    key={lang}
                    className={`px-3 py-1 rounded-lg text-sm ${
                      language === lang
                        ? 'bg-[#00a651] text-white'
                        : 'bg-[var(--iaf-bg-glass)] text-[var(--iaf-text-secondary)]'
                    }`}
                    onClick={() => handleLanguageChange(lang)}
                  >
                    {languageInfo[lang].flag} {lang.toUpperCase()}
                  </button>
                ))}
              </div>
            </div>

            {/* Mobile Theme Toggle */}
            <div className="px-4 py-2">
              <button
                className="flex items-center gap-2 text-[var(--iaf-text-secondary)]"
                onClick={handleThemeToggle}
              >
                {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
                <span>{theme === 'dark' ? t('light_mode', language) : t('dark_mode', language)}</span>
              </button>
            </div>

            <div className="iaf-mobile-divider" />

            <Link href="/login" className="iaf-mobile-link iaf-mobile-link-auth" onClick={() => setMobileMenuOpen(false)}>
              <LogIn className="w-5 h-5" />
              <span>{t('login', language)}</span>
            </Link>
            <Link href="/getstarted" className="iaf-mobile-link iaf-mobile-link-primary" onClick={() => setMobileMenuOpen(false)}>
              <Rocket className="w-5 h-5" />
              <span>{t('get_started', language)}</span>
            </Link>
          </nav>
        </div>
      )}
    </header>
  )
}
