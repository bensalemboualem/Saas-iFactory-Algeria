/**
 * IAFACTORY DESIGN SYSTEM - UNIFIED HEADER COMPONENT
 * Version: 3.0 - Décembre 2025
 * Source: Landing Page iafactoryalgeria.com (Single Source of Truth)
 *
 * Usage:
 * import { IAFactoryHeader } from '@/shared/components/IAFactoryHeader';
 * <IAFactoryHeader />
 */

import React, { useState, useEffect, useCallback } from 'react';

// ===== TYPES =====
type Language = 'fr' | 'en' | 'ar';
type Theme = 'dark' | 'light';
type Region = 'dz' | 'ch';
type Profile = 'user' | 'dev';

interface IAFactoryHeaderProps {
  /** Override auto-detection of region */
  region?: Region;
  /** Show/hide profile toggle */
  showProfileToggle?: boolean;
  /** Show/hide social links */
  showSocialLinks?: boolean;
  /** Custom navigation items */
  navItems?: NavItem[];
  /** Callback when profile changes */
  onProfileChange?: (profile: Profile) => void;
  /** Callback when language changes */
  onLanguageChange?: (lang: Language) => void;
  /** Callback when theme changes */
  onThemeChange?: (theme: Theme) => void;
  /** Login URL */
  loginUrl?: string;
  /** Get Started URL */
  getStartedUrl?: string;
  /** Custom class name */
  className?: string;
}

interface NavItem {
  label: string;
  href: string;
  icon?: string;
  i18nKey?: string;
}

// ===== TRANSLATIONS =====
const translations = {
  pricing: { fr: 'Tarifs', en: 'Pricing', ar: 'الأسعار' },
  apps: { fr: 'Applications', en: 'Applications', ar: 'التطبيقات' },
  ai_agents: { fr: 'Agents IA', en: 'AI Agents', ar: 'وكلاء الذكاء' },
  workflows: { fr: 'Workflows', en: 'Workflows', ar: 'سير العمل' },
  user: { fr: 'Utilisateur', en: 'User', ar: 'مستخدم' },
  developer: { fr: 'Développeur', en: 'Developer', ar: 'مطور' },
  login: { fr: 'Connexion', en: 'Log in', ar: 'تسجيل الدخول' },
  get_started: { fr: 'Commencer', en: 'Get Started', ar: 'ابدأ الآن' },
} as const;

// ===== DEFAULT NAV ITEMS =====
const defaultNavItems: NavItem[] = [
  { label: 'Tarifs', href: '/docs/tarifs.html', icon: 'fa-tags', i18nKey: 'pricing' },
  { label: 'Applications', href: '/apps.html', icon: 'fa-th', i18nKey: 'apps' },
  { label: 'Agents IA', href: '/docs/directory/agents.html', icon: 'fa-robot', i18nKey: 'ai_agents' },
  { label: 'Workflows', href: '/docs/directory/workflows.html', icon: 'fa-diagram-project', i18nKey: 'workflows' },
];

// ===== REGION CONFIG =====
const regionConfig = {
  dz: {
    flag: 'https://flagcdn.com/w40/dz.png',
    name: 'Algeria',
    i18nName: { fr: 'Algérie', en: 'Algeria', ar: 'الجزائر' },
    github: 'https://github.com/IAFactory-Algeria',
    huggingface: 'https://huggingface.co/IAFactory-Algeria',
  },
  ch: {
    flag: 'https://flagcdn.com/w40/ch.png',
    name: 'Suisse',
    i18nName: { fr: 'Suisse', en: 'Switzerland', ar: 'سويسرا' },
    github: 'https://github.com/IAFactory',
    huggingface: 'https://huggingface.co/IAFactory',
  },
};

// ===== DETECT REGION FROM HOSTNAME =====
function detectRegion(): Region {
  if (typeof window === 'undefined') return 'dz';
  const hostname = window.location.hostname;
  if (hostname.includes('iafactory.ch') || hostname.includes('switzerland')) {
    return 'ch';
  }
  return 'dz'; // Default to Algeria
}

// ===== HEADER COMPONENT =====
export function IAFactoryHeader({
  region: propRegion,
  showProfileToggle = true,
  showSocialLinks = true,
  navItems = defaultNavItems,
  onProfileChange,
  onLanguageChange,
  onThemeChange,
  loginUrl = '/docs/login.html',
  getStartedUrl = '/docs/getstarted.html',
  className = '',
}: IAFactoryHeaderProps) {
  // State
  const [region, setRegion] = useState<Region>(propRegion || 'dz');
  const [language, setLanguage] = useState<Language>('fr');
  const [theme, setTheme] = useState<Theme>('dark');
  const [profile, setProfile] = useState<Profile>('user');
  const [langMenuOpen, setLangMenuOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  // Detect region on mount
  useEffect(() => {
    if (!propRegion) {
      setRegion(detectRegion());
    }
  }, [propRegion]);

  // Load saved preferences
  useEffect(() => {
    const savedLang = localStorage.getItem('iafactory_lang') as Language;
    const savedTheme = localStorage.getItem('iafactory_theme') as Theme;

    if (savedLang && ['fr', 'en', 'ar'].includes(savedLang)) {
      setLanguage(savedLang);
    }
    if (savedTheme && ['dark', 'light'].includes(savedTheme)) {
      setTheme(savedTheme);
    } else {
      // Check system preference
      if (window.matchMedia?.('(prefers-color-scheme: light)').matches) {
        setTheme('light');
      }
    }
  }, []);

  // Apply theme to document
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    document.documentElement.classList.remove('dark', 'light');
    document.documentElement.classList.add(theme);
    localStorage.setItem('iafactory_theme', theme);
    onThemeChange?.(theme);
  }, [theme, onThemeChange]);

  // Apply language to document
  useEffect(() => {
    document.documentElement.lang = language;
    document.documentElement.dir = language === 'ar' ? 'rtl' : 'ltr';
    localStorage.setItem('iafactory_lang', language);
    onLanguageChange?.(language);
  }, [language, onLanguageChange]);

  // Scroll effect
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Close menus on outside click
  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (!target.closest('.iaf-language-selector')) {
        setLangMenuOpen(false);
      }
    };
    document.addEventListener('click', handleClick);
    return () => document.removeEventListener('click', handleClick);
  }, []);

  // Close mobile menu on escape
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && mobileMenuOpen) {
        setMobileMenuOpen(false);
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [mobileMenuOpen]);

  // Prevent body scroll when mobile menu is open
  useEffect(() => {
    document.body.style.overflow = mobileMenuOpen ? 'hidden' : '';
    return () => { document.body.style.overflow = ''; };
  }, [mobileMenuOpen]);

  // Translation helper
  const t = useCallback((key: keyof typeof translations): string => {
    return translations[key]?.[language] || key;
  }, [language]);

  // Handlers
  const handleThemeToggle = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  const handleLanguageChange = (lang: Language) => {
    setLanguage(lang);
    setLangMenuOpen(false);
  };

  const handleProfileChange = (newProfile: Profile) => {
    setProfile(newProfile);
    onProfileChange?.(newProfile);
  };

  const config = regionConfig[region];

  return (
    <>
      {/* CSS Variables for Header */}
      <style>{`
        .iaf-header {
          --iaf-header-height: 60px;
          --iaf-green: #00a651;
          --iaf-red: #ef4444;
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          height: var(--iaf-header-height);
          background: ${theme === 'dark' ? '#020617' : '#f7f5f0'};
          backdrop-filter: blur(24px) saturate(180%);
          -webkit-backdrop-filter: blur(24px) saturate(180%);
          border-bottom: 1px solid ${theme === 'dark' ? 'rgba(255,255,255,0.12)' : 'rgba(0,0,0,0.08)'};
          z-index: 1000;
          transition: all 250ms cubic-bezier(0.4, 0, 0.2, 1);
        }
        .iaf-header.scrolled {
          box-shadow: 0 4px 16px ${theme === 'dark' ? 'rgba(0,0,0,0.25)' : 'rgba(0,0,0,0.1)'};
        }
        .iaf-header-container {
          max-width: 1400px;
          margin: 0 auto;
          height: 100%;
          padding: 0 24px;
          display: flex;
          align-items: center;
          gap: 24px;
        }
        .iaf-logo {
          display: flex;
          align-items: center;
          gap: 10px;
          flex-shrink: 0;
          text-decoration: none;
        }
        .iaf-logo-flag {
          width: 32px;
          height: auto;
          animation: flagWave 3s ease-in-out infinite;
          transform-origin: left center;
        }
        @keyframes flagWave {
          0%, 100% { transform: perspective(400px) rotateY(0deg) scale(1); }
          25% { transform: perspective(400px) rotateY(8deg) scale(1.05); }
          50% { transform: perspective(400px) rotateY(0deg) scale(1); }
          75% { transform: perspective(400px) rotateY(-8deg) scale(1.05); }
        }
        .iaf-logo-text {
          font-size: 18px;
          font-weight: 700;
          color: ${theme === 'dark' ? '#f8fafc' : '#0f172a'};
        }
        .iaf-logo-text .green { color: var(--iaf-green); }
        .iaf-logo-text .red { color: var(--iaf-red); }
        .iaf-nav {
          display: flex;
          align-items: center;
          gap: 4px;
          margin-left: auto;
        }
        .iaf-nav-link {
          display: flex;
          align-items: center;
          gap: 6px;
          padding: 6px 12px;
          font-size: 14px;
          font-weight: 500;
          color: ${theme === 'dark' ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.7)'};
          text-decoration: none;
          border-radius: 8px;
          transition: all 150ms;
        }
        .iaf-nav-link:hover {
          color: var(--iaf-green);
        }
        .iaf-header-actions {
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .iaf-profile-toggle {
          display: flex;
          gap: 6px;
        }
        .iaf-profile-btn {
          display: flex;
          align-items: center;
          gap: 5px;
          padding: 6px 12px;
          background: transparent;
          border: none;
          border-radius: 8px;
          font-size: 13px;
          font-weight: 500;
          color: ${theme === 'dark' ? 'rgba(255,255,255,0.5)' : 'rgba(0,0,0,0.5)'};
          cursor: pointer;
          transition: all 150ms;
        }
        .iaf-profile-btn:hover {
          color: ${theme === 'dark' ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.7)'};
        }
        .iaf-profile-btn.active {
          color: #ffffff;
          background: var(--iaf-green);
          box-shadow: 0 2px 8px rgba(0, 166, 81, 0.3);
        }
        .iaf-theme-btn {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 36px;
          height: 36px;
          background: ${theme === 'dark' ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.04)'};
          border: none;
          border-radius: 8px;
          color: ${theme === 'dark' ? '#f8fafc' : '#0f172a'};
          cursor: pointer;
          transition: all 150ms;
          font-size: 16px;
        }
        .iaf-theme-btn:hover {
          background: ${theme === 'dark' ? 'rgba(255,255,255,0.12)' : 'rgba(0,0,0,0.08)'};
        }
        .iaf-lang-selector {
          position: relative;
        }
        .iaf-lang-btn {
          display: flex;
          align-items: center;
          gap: 6px;
          padding: 6px 12px;
          background: transparent;
          border: none;
          border-radius: 8px;
          font-size: 13px;
          font-weight: 500;
          color: ${theme === 'dark' ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.7)'};
          cursor: pointer;
          transition: all 150ms;
        }
        .iaf-lang-btn:hover {
          color: var(--iaf-green);
        }
        .iaf-lang-menu {
          position: absolute;
          top: calc(100% + 8px);
          right: 0;
          min-width: 160px;
          background: ${theme === 'dark' ? '#020617' : '#ffffff'};
          border: 1px solid ${theme === 'dark' ? 'rgba(255,255,255,0.12)' : 'rgba(0,0,0,0.08)'};
          border-radius: 12px;
          padding: 6px;
          box-shadow: 0 8px 32px ${theme === 'dark' ? 'rgba(0,0,0,0.3)' : 'rgba(0,0,0,0.12)'};
          opacity: 0;
          visibility: hidden;
          transform: translateY(-10px);
          transition: all 200ms;
        }
        .iaf-lang-menu.open {
          opacity: 1;
          visibility: visible;
          transform: translateY(0);
        }
        .iaf-lang-option {
          display: flex;
          align-items: center;
          gap: 12px;
          width: 100%;
          padding: 10px 12px;
          background: transparent;
          border: none;
          border-radius: 8px;
          font-size: 14px;
          color: ${theme === 'dark' ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.7)'};
          cursor: pointer;
          transition: all 150ms;
          text-align: left;
        }
        .iaf-lang-option:hover {
          background: ${theme === 'dark' ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.04)'};
          color: ${theme === 'dark' ? '#f8fafc' : '#0f172a'};
        }
        .iaf-lang-option.active {
          background: rgba(0, 166, 81, 0.15);
          color: var(--iaf-green);
        }
        .iaf-social-links {
          display: flex;
          gap: 8px;
        }
        .iaf-social-link {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 36px;
          height: 36px;
          background: transparent;
          border: none;
          border-radius: 8px;
          color: ${theme === 'dark' ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.7)'};
          text-decoration: none;
          transition: all 150ms;
          font-size: 18px;
        }
        .iaf-social-link:hover {
          color: ${theme === 'dark' ? '#f8fafc' : '#0f172a'};
          transform: translateY(-2px);
        }
        .iaf-auth-buttons {
          display: flex;
          gap: 8px;
        }
        .iaf-btn {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          gap: 6px;
          padding: 7px 16px;
          font-size: 13px;
          font-weight: 600;
          text-decoration: none;
          border-radius: 8px;
          border: none;
          cursor: pointer;
          transition: all 150ms;
        }
        .iaf-btn-secondary {
          background: transparent;
          color: ${theme === 'dark' ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.7)'};
        }
        .iaf-btn-secondary:hover {
          color: var(--iaf-green);
        }
        .iaf-btn-primary {
          background: linear-gradient(135deg, var(--iaf-green) 0%, #00c761 100%);
          color: #ffffff;
          box-shadow: 0 2px 8px rgba(0, 166, 81, 0.25);
        }
        .iaf-btn-primary:hover {
          box-shadow: 0 4px 14px rgba(0, 166, 81, 0.35);
          transform: translateY(-1px);
        }
        .iaf-mobile-menu-btn {
          display: none;
          flex-direction: column;
          gap: 5px;
          padding: 8px;
          background: transparent;
          border: none;
          cursor: pointer;
        }
        .iaf-burger-line {
          width: 22px;
          height: 2px;
          background: ${theme === 'dark' ? '#f8fafc' : '#0f172a'};
          border-radius: 2px;
          transition: all 250ms;
        }
        .iaf-mobile-menu-btn.active .iaf-burger-line:nth-child(1) {
          transform: rotate(45deg) translate(7px, 7px);
        }
        .iaf-mobile-menu-btn.active .iaf-burger-line:nth-child(2) {
          opacity: 0;
        }
        .iaf-mobile-menu-btn.active .iaf-burger-line:nth-child(3) {
          transform: rotate(-45deg) translate(7px, -7px);
        }
        .iaf-mobile-menu {
          position: fixed;
          top: 0;
          right: 0;
          width: 100%;
          max-width: 380px;
          height: 100vh;
          background: ${theme === 'dark' ? '#020617' : '#f7f5f0'};
          border-left: 1px solid ${theme === 'dark' ? 'rgba(255,255,255,0.12)' : 'rgba(0,0,0,0.08)'};
          box-shadow: -8px 0 32px ${theme === 'dark' ? 'rgba(0,0,0,0.3)' : 'rgba(0,0,0,0.12)'};
          z-index: 1100;
          transform: translateX(100%);
          transition: transform 350ms cubic-bezier(0.4, 0, 0.2, 1);
          overflow-y: auto;
        }
        .iaf-mobile-menu.open {
          transform: translateX(0);
        }
        .iaf-mobile-menu-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 24px;
          border-bottom: 1px solid ${theme === 'dark' ? 'rgba(255,255,255,0.12)' : 'rgba(0,0,0,0.08)'};
        }
        .iaf-mobile-logo {
          display: flex;
          align-items: center;
          gap: 12px;
          font-size: 16px;
          font-weight: 700;
          color: ${theme === 'dark' ? '#f8fafc' : '#0f172a'};
        }
        .iaf-mobile-close {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 36px;
          height: 36px;
          background: ${theme === 'dark' ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.04)'};
          border: none;
          border-radius: 8px;
          font-size: 20px;
          color: ${theme === 'dark' ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.7)'};
          cursor: pointer;
          transition: all 150ms;
        }
        .iaf-mobile-close:hover {
          background: rgba(239, 68, 68, 0.2);
          color: var(--iaf-red);
        }
        .iaf-mobile-nav {
          padding: 24px;
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .iaf-mobile-link {
          display: flex;
          align-items: center;
          gap: 14px;
          padding: 14px 16px;
          background: ${theme === 'dark' ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.04)'};
          border: 1px solid ${theme === 'dark' ? 'rgba(255,255,255,0.12)' : 'rgba(0,0,0,0.08)'};
          border-radius: 12px;
          font-size: 15px;
          font-weight: 500;
          color: ${theme === 'dark' ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.7)'};
          text-decoration: none;
          transition: all 150ms;
        }
        .iaf-mobile-link:hover {
          background: ${theme === 'dark' ? 'rgba(255,255,255,0.12)' : 'rgba(0,0,0,0.08)'};
          color: ${theme === 'dark' ? '#f8fafc' : '#0f172a'};
          border-color: var(--iaf-green);
        }
        .iaf-mobile-link-primary {
          background: linear-gradient(135deg, var(--iaf-green) 0%, #00c761 100%);
          color: #ffffff !important;
          border: none;
          font-weight: 600;
          box-shadow: 0 4px 12px rgba(0, 166, 81, 0.3);
        }
        .iaf-mobile-divider {
          height: 1px;
          background: ${theme === 'dark' ? 'rgba(255,255,255,0.12)' : 'rgba(0,0,0,0.08)'};
          margin: 16px 0;
        }
        /* Responsive */
        @media (max-width: 1024px) {
          .iaf-nav, .iaf-profile-toggle, .iaf-social-links, .iaf-auth-buttons {
            display: none;
          }
          .iaf-mobile-menu-btn {
            display: flex;
          }
        }
        @media (max-width: 768px) {
          .iaf-header-container {
            padding: 0 16px;
          }
          .iaf-logo-text {
            display: none;
          }
          .iaf-mobile-menu {
            max-width: 100%;
          }
        }
        /* Content padding to account for sticky header */
        .iaf-header-spacer {
          height: var(--iaf-header-height, 60px);
        }
      `}</style>

      {/* Header */}
      <header className={`iaf-header ${isScrolled ? 'scrolled' : ''} ${className}`} role="banner">
        <div className="iaf-header-container">
          {/* Logo */}
          <a href="/" className="iaf-logo" dir="ltr">
            <img src={config.flag} alt={config.name} className="iaf-logo-flag" />
            <span className="iaf-logo-text">
              <span className="green">IA</span>Factory{' '}
              {region === 'dz' ? (
                <span>Alger<span className="green">ia</span></span>
              ) : (
                <span>Su<span className="red">is</span>se</span>
              )}
            </span>
          </a>

          {/* Navigation */}
          <nav className="iaf-nav" role="navigation">
            {navItems.map((item, index) => (
              <a key={index} href={item.href} className="iaf-nav-link">
                {item.icon && <i className={`fa-solid ${item.icon}`} />}
                <span>{item.i18nKey ? t(item.i18nKey as keyof typeof translations) : item.label}</span>
              </a>
            ))}
          </nav>

          {/* Header Actions */}
          <div className="iaf-header-actions">
            {/* Profile Toggle */}
            {showProfileToggle && (
              <div className="iaf-profile-toggle" role="tablist">
                <button
                  className={`iaf-profile-btn ${profile === 'user' ? 'active' : ''}`}
                  onClick={() => handleProfileChange('user')}
                  role="tab"
                  aria-selected={profile === 'user'}
                >
                  <i className="fa-solid fa-user" />
                  <span>{t('user')}</span>
                </button>
                <button
                  className={`iaf-profile-btn ${profile === 'dev' ? 'active' : ''}`}
                  onClick={() => handleProfileChange('dev')}
                  role="tab"
                  aria-selected={profile === 'dev'}
                >
                  <i className="fa-solid fa-code" />
                  <span>{t('developer')}</span>
                </button>
              </div>
            )}

            {/* Theme Toggle */}
            <button
              className="iaf-theme-btn"
              onClick={handleThemeToggle}
              aria-label={theme === 'dark' ? 'Activer le mode clair' : 'Activer le mode sombre'}
              title={theme === 'dark' ? 'Mode clair' : 'Mode sombre'}
            >
              {theme === 'dark' ? '☀️' : '🌙'}
            </button>

            {/* Language Selector */}
            <div className="iaf-lang-selector">
              <button
                className="iaf-lang-btn"
                onClick={(e) => { e.stopPropagation(); setLangMenuOpen(!langMenuOpen); }}
                aria-haspopup="true"
                aria-expanded={langMenuOpen}
              >
                <i className="fa-solid fa-globe" />
                <span>{language.toUpperCase()}</span>
                <i className={`fa-solid fa-chevron-down`} style={{ fontSize: 10, transition: 'transform 150ms', transform: langMenuOpen ? 'rotate(180deg)' : 'none' }} />
              </button>
              <div className={`iaf-lang-menu ${langMenuOpen ? 'open' : ''}`} role="menu">
                <button className={`iaf-lang-option ${language === 'fr' ? 'active' : ''}`} onClick={() => handleLanguageChange('fr')} role="menuitem">
                  <span>🇫🇷</span>
                  <span>Français</span>
                </button>
                <button className={`iaf-lang-option ${language === 'en' ? 'active' : ''}`} onClick={() => handleLanguageChange('en')} role="menuitem">
                  <span>🇬🇧</span>
                  <span>English</span>
                </button>
                <button className={`iaf-lang-option ${language === 'ar' ? 'active' : ''}`} onClick={() => handleLanguageChange('ar')} role="menuitem" dir="rtl">
                  <span>🇩🇿</span>
                  <span>العربية</span>
                </button>
              </div>
            </div>

            {/* Social Links */}
            {showSocialLinks && (
              <div className="iaf-social-links">
                <a href={config.github} className="iaf-social-link" target="_blank" rel="noopener noreferrer" title="GitHub">
                  <i className="fa-brands fa-github" />
                </a>
                <a href={config.huggingface} className="iaf-social-link" target="_blank" rel="noopener noreferrer" title="Hugging Face">
                  🤗
                </a>
              </div>
            )}

            {/* Auth Buttons */}
            <div className="iaf-auth-buttons">
              <a href={loginUrl} className="iaf-btn iaf-btn-secondary">
                <i className="fa-solid fa-arrow-right-to-bracket" />
                <span>{t('login')}</span>
              </a>
              <a href={getStartedUrl} className="iaf-btn iaf-btn-primary">
                <i className="fa-solid fa-rocket" />
                <span>{t('get_started')}</span>
              </a>
            </div>

            {/* Mobile Menu Button */}
            <button
              className={`iaf-mobile-menu-btn ${mobileMenuOpen ? 'active' : ''}`}
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label="Menu mobile"
              aria-expanded={mobileMenuOpen}
            >
              <span className="iaf-burger-line" />
              <span className="iaf-burger-line" />
              <span className="iaf-burger-line" />
            </button>
          </div>
        </div>
      </header>

      {/* Mobile Menu */}
      <div className={`iaf-mobile-menu ${mobileMenuOpen ? 'open' : ''}`} role="dialog" aria-modal="true">
        <div className="iaf-mobile-menu-header">
          <div className="iaf-mobile-logo">
            <img src={config.flag} alt={config.name} width="28" />
            <span>IAFactory {region === 'dz' ? 'DZ' : 'CH'}</span>
          </div>
          <button className="iaf-mobile-close" onClick={() => setMobileMenuOpen(false)} aria-label="Fermer">
            ✕
          </button>
        </div>
        <nav className="iaf-mobile-nav" role="navigation">
          {navItems.map((item, index) => (
            <a key={index} href={item.href} className="iaf-mobile-link" onClick={() => setMobileMenuOpen(false)}>
              <span>{item.icon && <i className={`fa-solid ${item.icon}`} />}</span>
              <span>{item.i18nKey ? t(item.i18nKey as keyof typeof translations) : item.label}</span>
            </a>
          ))}
          <div className="iaf-mobile-divider" />
          {/* Theme toggle in mobile */}
          <button className="iaf-mobile-link" onClick={handleThemeToggle}>
            <span>{theme === 'dark' ? '☀️' : '🌙'}</span>
            <span>{theme === 'dark' ? 'Mode clair' : 'Mode sombre'}</span>
          </button>
          <div className="iaf-mobile-divider" />
          <a href={loginUrl} className="iaf-mobile-link" onClick={() => setMobileMenuOpen(false)}>
            <span>🔑</span>
            <span>{t('login')}</span>
          </a>
          <a href={getStartedUrl} className="iaf-mobile-link iaf-mobile-link-primary" onClick={() => setMobileMenuOpen(false)}>
            <span>🚀</span>
            <span>{t('get_started')}</span>
          </a>
        </nav>
      </div>

      {/* Spacer for sticky header */}
      <div className="iaf-header-spacer" />
    </>
  );
}

// ===== HEADER SPACER COMPONENT =====
export function IAFactoryHeaderSpacer() {
  return <div style={{ height: 60 }} />;
}

export default IAFactoryHeader;
