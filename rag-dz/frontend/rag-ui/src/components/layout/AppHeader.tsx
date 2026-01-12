import { useState, useEffect } from 'react'

export function Header() {
  const [profile, setProfile] = useState<'user' | 'dev'>('user')
  const [langMenuOpen, setLangMenuOpen] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [currentLang, setCurrentLang] = useState('fr')
  const [scrolled, setScrolled] = useState(false)

  // Handle scroll
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  // Close menus on outside click
  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (!(e.target as Element).closest('.iaf-language-selector')) {
        setLangMenuOpen(false)
      }
    }
    document.addEventListener('click', handleClick)
    return () => document.removeEventListener('click', handleClick)
  }, [])

  // Close mobile menu on escape
  useEffect(() => {
    const handleKeydown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && mobileMenuOpen) {
        setMobileMenuOpen(false)
      }
    }
    document.addEventListener('keydown', handleKeydown)
    return () => document.removeEventListener('keydown', handleKeydown)
  }, [mobileMenuOpen])

  const switchProfile = (newProfile: 'user' | 'dev') => {
    setProfile(newProfile)
    window.dispatchEvent(new CustomEvent('profileChanged', { detail: { profile: newProfile } }))
  }

  const changeLanguage = (lang: string) => {
    setCurrentLang(lang)
    setLangMenuOpen(false)
    localStorage.setItem('iafactory_lang', lang)
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr'
  }

  const toggleLangMenu = (e: React.MouseEvent) => {
    e.stopPropagation()
    setLangMenuOpen(!langMenuOpen)
  }

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen)
    document.body.style.overflow = !mobileMenuOpen ? 'hidden' : ''
  }

  const langLabels: Record<string, string> = { fr: 'FR', en: 'EN', ar: 'AR' }

  return (
    <header className={`iaf-header ${scrolled ? 'scrolled' : ''}`} role="banner">
      <div className="iaf-header-container">
        {/* Logo Section (EXACT COPY from landing) */}
        <div className="header-logo" dir="ltr">
          <img src="https://flagcdn.com/w40/dz.png" alt="Algerie" className="logo-flag" />
          <span className="logo-text">
            <span className="letter i-drop" style={{ color: '#00a651', animationDelay: '0s' }}>
              <span className="i-stem">ı</span>
              <span className="i-dot">•</span>
            </span>
            <span className="letter" style={{ color: '#00a651', animationDelay: '0.1s' }}>A</span>
            <span className="letter" style={{ color: 'var(--text)', animationDelay: '0.2s' }}>F</span>
            <span className="letter" style={{ color: 'var(--text)', animationDelay: '0.3s' }}>a</span>
            <span className="letter" style={{ color: 'var(--text)', animationDelay: '0.4s' }}>c</span>
            <span className="letter" style={{ color: 'var(--text)', animationDelay: '0.5s' }}>t</span>
            <span className="letter" style={{ color: 'var(--text)', animationDelay: '0.6s' }}>o</span>
            <span className="letter" style={{ color: '#ef4444', animationDelay: '0.7s' }}>r</span>
            <span className="letter" style={{ color: '#ef4444', animationDelay: '0.8s' }}>y</span>
            {' '}
            <span className="letter" style={{ color: 'var(--text)', animationDelay: '0.9s' }}>A</span>
            <span className="letter" style={{ color: 'var(--text)', animationDelay: '1s' }}>l</span>
            <span className="letter" style={{ color: 'var(--text)', animationDelay: '1.1s' }}>g</span>
            <span className="letter" style={{ color: 'var(--text)', animationDelay: '1.2s' }}>e</span>
            <span className="letter" style={{ color: 'var(--text)', animationDelay: '1.3s' }}>r</span>
            <span className="letter i-drop" style={{ color: '#00a651', animationDelay: '1.4s' }}>
              <span className="i-stem">ı</span>
              <span className="i-dot">•</span>
            </span>
            <span className="letter" style={{ color: '#00a651', animationDelay: '1.5s' }}>a</span>
          </span>
        </div>

        {/* Main Navigation */}
        <nav className="iaf-nav" role="navigation" aria-label="Navigation principale">
          <a href="https://www.iafactoryalgeria.com/docs/tarifs.html" className="iaf-nav-link">
            <i className="fa-solid fa-tags iaf-nav-icon"></i>
            <span>Tarifs</span>
          </a>
          <a href="https://www.iafactoryalgeria.com/apps.html" className="iaf-nav-link">
            <i className="fa-solid fa-th iaf-nav-icon"></i>
            <span>Applications</span>
          </a>
          <a href="https://www.iafactoryalgeria.com/docs/directory/agents.html" className="iaf-nav-link">
            <i className="fa-solid fa-robot iaf-nav-icon"></i>
            <span>Agents IA</span>
          </a>
          <a href="https://www.iafactoryalgeria.com/docs/directory/workflows.html" className="iaf-nav-link">
            <i className="fa-solid fa-diagram-project iaf-nav-icon"></i>
            <span>Workflows</span>
          </a>
        </nav>

        {/* Header Actions */}
        <div className="iaf-header-actions">
          {/* User/Dev Profile Toggle */}
          <div className="iaf-profile-toggle" role="tablist" aria-label="Type de profil">
            <button
              className={`iaf-profile-btn ${profile === 'user' ? 'active' : ''}`}
              data-profile="user"
              role="tab"
              aria-selected={profile === 'user'}
              onClick={() => switchProfile('user')}
            >
              <i className="fa-solid fa-user iaf-profile-icon"></i>
              <span>Utilisateur</span>
            </button>
            <button
              className={`iaf-profile-btn ${profile === 'dev' ? 'active' : ''}`}
              data-profile="dev"
              role="tab"
              aria-selected={profile === 'dev'}
              onClick={() => switchProfile('dev')}
            >
              <i className="fa-solid fa-code iaf-profile-icon"></i>
              <span>Developpeur</span>
            </button>
          </div>

          {/* Language Selector */}
          <div className="iaf-language-selector">
            <button
              className="iaf-lang-btn"
              onClick={toggleLangMenu}
              aria-label="Changer la langue"
              aria-haspopup="true"
              aria-expanded={langMenuOpen}
            >
              <i className="fa-solid fa-globe iaf-lang-icon"></i>
              <span className="iaf-lang-label">{langLabels[currentLang]}</span>
              <i className="fa-solid fa-chevron-down iaf-lang-chevron"></i>
            </button>
            <div className={`iaf-lang-menu ${langMenuOpen ? 'show' : ''}`} role="menu">
              <button className={`iaf-lang-option ${currentLang === 'fr' ? 'active' : ''}`} onClick={() => changeLanguage('fr')} role="menuitem">
                <span className="iaf-lang-flag">🇫🇷</span>
                <span>Francais</span>
                <i className="fa-solid fa-check iaf-lang-check"></i>
              </button>
              <button className={`iaf-lang-option ${currentLang === 'en' ? 'active' : ''}`} onClick={() => changeLanguage('en')} role="menuitem">
                <span className="iaf-lang-flag">🇬🇧</span>
                <span>English</span>
                <i className="fa-solid fa-check iaf-lang-check"></i>
              </button>
              <button className={`iaf-lang-option ${currentLang === 'ar' ? 'active' : ''}`} onClick={() => changeLanguage('ar')} role="menuitem" dir="rtl">
                <span className="iaf-lang-flag">🇩🇿</span>
                <span>العربية</span>
                <i className="fa-solid fa-check iaf-lang-check"></i>
              </button>
            </div>
          </div>

          {/* Social Links (GitHub, Hugging Face) */}
          <div className="iaf-social-links">
            <a href="https://github.com/IAFactory-Algeria" className="iaf-social-link" target="_blank" rel="noopener noreferrer" aria-label="GitHub" title="GitHub">
              <i className="fa-brands fa-github"></i>
            </a>
            <a href="https://huggingface.co/IAFactory-Algeria" className="iaf-social-link" target="_blank" rel="noopener noreferrer" aria-label="Hugging Face" title="Hugging Face">
              <span className="hf-icon">🤗</span>
            </a>
          </div>

          {/* Auth Buttons */}
          <div className="iaf-auth-buttons">
            <a href="https://www.iafactoryalgeria.com/docs/login.html" className="iaf-btn iaf-btn-secondary">
              <i className="fa-solid fa-arrow-right-to-bracket iaf-btn-icon"></i>
              <span>Log in</span>
            </a>
            <a href="https://www.iafactoryalgeria.com/docs/getstarted.html" className="iaf-btn iaf-btn-primary">
              <i className="fa-solid fa-rocket iaf-btn-icon"></i>
              <span>Get Started</span>
            </a>
          </div>

          {/* Mobile Menu Button */}
          <button className={`iaf-mobile-menu-btn ${mobileMenuOpen ? 'active' : ''}`} onClick={toggleMobileMenu} aria-label="Menu mobile" aria-expanded={mobileMenuOpen}>
            <span className="iaf-burger-line"></span>
            <span className="iaf-burger-line"></span>
            <span className="iaf-burger-line"></span>
          </button>
        </div>
      </div>

      {/* Mobile Menu Overlay */}
      <div className={`iaf-mobile-menu ${mobileMenuOpen ? 'open' : ''}`} id="mobileMenu" role="dialog" aria-modal="true">
        <div className="iaf-mobile-menu-header">
          <div className="iaf-mobile-logo">
            <img src="https://flagcdn.com/w40/dz.png" alt="Algeria" width="28" height="21" />
            <span>IAFactory DZ</span>
          </div>
          <button className="iaf-mobile-close" onClick={toggleMobileMenu} aria-label="Fermer le menu">
            <span>✕</span>
          </button>
        </div>
        <nav className="iaf-mobile-nav" role="navigation">
          <a href="https://www.iafactoryalgeria.com/docs/tarifs.html" className="iaf-mobile-link" onClick={toggleMobileMenu}>
            <span className="iaf-mobile-icon">💰</span>
            <span>Tarifs</span>
          </a>
          <a href="https://www.iafactoryalgeria.com/apps.html" className="iaf-mobile-link" onClick={toggleMobileMenu}>
            <span className="iaf-mobile-icon">📱</span>
            <span>Applications</span>
          </a>
          <a href="https://www.iafactoryalgeria.com/docs/directory/agents.html" className="iaf-mobile-link" onClick={toggleMobileMenu}>
            <span className="iaf-mobile-icon">🤖</span>
            <span>Agents IA</span>
          </a>
          <a href="https://www.iafactoryalgeria.com/docs/directory/workflows.html" className="iaf-mobile-link" onClick={toggleMobileMenu}>
            <span className="iaf-mobile-icon">⚡</span>
            <span>Workflows</span>
          </a>
          <div className="iaf-mobile-divider"></div>
          <a href="https://github.com/IAFactory-Algeria" target="_blank" rel="noopener noreferrer" className="iaf-mobile-link">
            <span className="iaf-mobile-icon"><i className="fa-brands fa-github"></i></span>
            <span>GitHub</span>
          </a>
          <a href="https://huggingface.co/IAFactory-Algeria" target="_blank" rel="noopener noreferrer" className="iaf-mobile-link">
            <span className="iaf-mobile-icon">🤗</span>
            <span>Hugging Face</span>
          </a>
          <div className="iaf-mobile-divider"></div>
          <a href="https://www.iafactoryalgeria.com/docs/login.html" className="iaf-mobile-link iaf-mobile-link-auth" onClick={toggleMobileMenu}>
            <span className="iaf-mobile-icon">🔑</span>
            <span>Log in</span>
          </a>
          <a href="https://www.iafactoryalgeria.com/docs/getstarted.html" className="iaf-mobile-link iaf-mobile-link-primary" onClick={toggleMobileMenu}>
            <span className="iaf-mobile-icon">🚀</span>
            <span>Get Started</span>
          </a>
        </nav>
      </div>
    </header>
  )
}

// Export both names for compatibility
export { Header as AppHeader }
export default Header
