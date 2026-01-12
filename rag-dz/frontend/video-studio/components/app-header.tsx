"use client"

import * as React from "react"
import Link from "next/link"

export function AppHeader() {
  const [theme, setTheme] = React.useState("dark")
  const [profileMode, setProfileMode] = React.useState("user")
  const [langMenuOpen, setLangMenuOpen] = React.useState(false)
  const [currentLang, setCurrentLang] = React.useState("fr")
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false)
  const [settingsOpen, setSettingsOpen] = React.useState(false)
  const [activeSection, setActiveSection] = React.useState("general")

  // Apply theme to DOM
  const applyTheme = (newTheme: string) => {
    // Apply to both body and html for consistency with landing page
    document.body.setAttribute('data-theme', newTheme)
    document.documentElement.setAttribute('data-theme', newTheme)
    // Also toggle .dark class for Tailwind
    if (newTheme === 'dark') {
      document.body.classList.add('dark')
      document.documentElement.classList.add('dark')
    } else {
      document.body.classList.remove('dark')
      document.documentElement.classList.remove('dark')
    }
  }

  React.useEffect(() => {
    const savedTheme = localStorage.getItem("iafactory_theme") || "dark"
    setTheme(savedTheme)
    applyTheme(savedTheme)
  }, [])

  const toggleTheme = () => {
    const newTheme = theme === "light" ? "dark" : "light"
    setTheme(newTheme)
    localStorage.setItem("iafactory_theme", newTheme)
    applyTheme(newTheme)
  }

  const toggleLangMenu = (e: React.MouseEvent) => {
    e.stopPropagation()
    setLangMenuOpen(!langMenuOpen)
  }

  const changeLanguage = (lang: string) => {
    setCurrentLang(lang)
    setLangMenuOpen(false)
    localStorage.setItem("iafactory_lang", lang)
  }

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen)
  }

  const closeMobileMenu = () => {
    setMobileMenuOpen(false)
  }

  // Close lang menu when clicking outside
  React.useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      const target = e.target as HTMLElement
      if (!target.closest(".language-dropdown")) {
        setLangMenuOpen(false)
      }
    }
    document.addEventListener("click", handleClick)
    return () => document.removeEventListener("click", handleClick)
  }, [])

  const langLabels = { fr: "🌐 FR", en: "🌐 EN", ar: "🌐 AR" }

  return (
    <>
      <header>
        <div className="header-container">
          {/* Logo */}
          <Link href="/" className="header-logo">
            <img src="https://flagcdn.com/w40/dz.png" alt="Algérie" className="logo-flag" />
            <span className="logo-text">
              <span className="highlight">IA</span>Factory Alger<span className="highlight">ia</span>
            </span>
          </Link>

          {/* Navigation */}
          <nav className="header-nav">
            <Link href="/" className="nav-link">
              Accueil
            </Link>
            <Link href="/studio" className="nav-link">
              Studio
            </Link>
            <Link href="/library" className="nav-link">
              Bibliothèque
            </Link>
            <Link href="/templates" className="nav-link">
              Templates
            </Link>
            <Link href="/analytics" className="nav-link">
              Analytics
            </Link>
          </nav>

          {/* Actions */}
          <div className="header-actions">
            {/* Profile Toggle */}
            <div className="profile-toggle">
              <button
                className={`profile-btn ${profileMode === "user" ? "active" : ""}`}
                onClick={() => setProfileMode("user")}
              >
                👤 Utilisateur
              </button>
              <button
                className={`profile-btn ${profileMode === "developer" ? "active" : ""}`}
                onClick={() => setProfileMode("developer")}
              >
                👨‍💻 Développeur
              </button>
            </div>

            {/* Login Button */}
            <Link href="/login" className="btn-login">
              Log in
            </Link>

            {/* Get Started Button */}
            <Link href="/studio" className="btn-get-started">
              Get Started
            </Link>

            {/* Language Dropdown */}
            <div className="language-dropdown">
              <button className="lang-btn" onClick={toggleLangMenu}>
                {langLabels[currentLang as keyof typeof langLabels]}
              </button>
              <div className={`lang-menu ${langMenuOpen ? "show" : ""}`}>
                <button className="lang-option" onClick={() => changeLanguage("fr")}>
                  🇫🇷 Français
                </button>
                <button className="lang-option" onClick={() => changeLanguage("en")}>
                  🇬🇧 English
                </button>
                <button className="lang-option" onClick={() => changeLanguage("ar")}>
                  🇩🇿 العربية
                </button>
              </div>
            </div>

            {/* Settings Button */}
            <button className="settings-btn" onClick={() => setSettingsOpen(true)} aria-label="Settings">
              ⚙️
            </button>

            {/* Theme Toggle */}
            <button className="theme-toggle" onClick={toggleTheme} aria-label="Toggle theme">
              {theme === "light" ? "🌙" : "☀️"}
            </button>

            {/* Mobile Menu Button */}
            <button
              className="mobile-menu-btn"
              aria-label="Menu"
              onClick={toggleMobileMenu}
            >
              <span></span>
              <span></span>
              <span></span>
            </button>
          </div>
        </div>
      </header>

      {/* Mobile Menu */}
      <div className={`mobile-menu ${mobileMenuOpen ? "open" : ""}`}>
        <nav className="mobile-menu-nav">
          <Link href="/" className="mobile-nav-link" onClick={closeMobileMenu}>
            🏠 Accueil
          </Link>
          <Link href="/studio" className="mobile-nav-link" onClick={closeMobileMenu}>
            🎬 Studio
          </Link>
          <Link href="/library" className="mobile-nav-link" onClick={closeMobileMenu}>
            📚 Bibliothèque
          </Link>
          <Link href="/templates" className="mobile-nav-link" onClick={closeMobileMenu}>
            📋 Templates
          </Link>
          <Link href="/analytics" className="mobile-nav-link" onClick={closeMobileMenu}>
            📊 Analytics
          </Link>
          <hr style={{ borderColor: "var(--border)", margin: "16px 0" }} />
          <Link href="/login" className="mobile-nav-link login-btn-mobile" onClick={closeMobileMenu}>
            🔑 Log in
          </Link>
          <Link href="/studio" className="mobile-nav-link getstarted-btn-mobile" onClick={closeMobileMenu}>
            🚀 Get Started
          </Link>
        </nav>
      </div>

      {/* Settings Modal */}
      {settingsOpen && (
        <div className="settings-modal">
          <div className="settings-overlay" onClick={() => setSettingsOpen(false)}></div>
          <div className="settings-container">
            <div className="settings-header">
              <h2>⚙️ Paramètres</h2>
              <button className="settings-close" onClick={() => setSettingsOpen(false)}>✕</button>
            </div>
            <div className="settings-body">
              {/* Sidebar Navigation */}
              <div className="settings-sidebar">
                <button
                  className={`settings-nav-item ${activeSection === "general" ? "active" : ""}`}
                  onClick={() => setActiveSection("general")}
                >
                  <i className="fas fa-sliders-h"></i> Général
                </button>
                <button
                  className={`settings-nav-item ${activeSection === "appearance" ? "active" : ""}`}
                  onClick={() => setActiveSection("appearance")}
                >
                  <i className="fas fa-palette"></i> Apparence
                </button>
                <button
                  className={`settings-nav-item ${activeSection === "providers" ? "active" : ""}`}
                  onClick={() => setActiveSection("providers")}
                >
                  <i className="fas fa-cloud"></i> Providers IA
                </button>
                <button
                  className={`settings-nav-item ${activeSection === "apikeys" ? "active" : ""}`}
                  onClick={() => setActiveSection("apikeys")}
                >
                  <i className="fas fa-key"></i> Clés API
                </button>
                <button
                  className={`settings-nav-item ${activeSection === "data" ? "active" : ""}`}
                  onClick={() => setActiveSection("data")}
                >
                  <i className="fas fa-database"></i> Données
                </button>
                <button
                  className={`settings-nav-item ${activeSection === "about" ? "active" : ""}`}
                  onClick={() => setActiveSection("about")}
                >
                  <i className="fas fa-info-circle"></i> À propos
                </button>
              </div>

              {/* Content Sections */}
              <div className="settings-content">
                {/* General */}
                <div className={`settings-section ${activeSection === "general" ? "active" : ""}`}>
                  <h3>Paramètres généraux</h3>
                  <div className="settings-group">
                    <label>Langue de l'interface</label>
                    <select defaultValue={currentLang} onChange={(e) => changeLanguage(e.target.value)}>
                      <option value="fr">🇫🇷 Français</option>
                      <option value="en">🇬🇧 English</option>
                      <option value="ar">🇩🇿 العربية</option>
                    </select>
                  </div>
                  <div className="settings-group">
                    <label>Profil par défaut</label>
                    <select defaultValue={profileMode} onChange={(e) => setProfileMode(e.target.value)}>
                      <option value="user">👤 Utilisateur</option>
                      <option value="developer">👨‍💻 Développeur</option>
                    </select>
                  </div>
                  <div className="settings-group">
                    <label>
                      <input type="checkbox" defaultChecked />
                      Sauvegarder les conversations automatiquement
                    </label>
                  </div>
                  <div className="settings-group">
                    <label>
                      <input type="checkbox" />
                      Sons de notification
                    </label>
                  </div>
                </div>

                {/* Appearance */}
                <div className={`settings-section ${activeSection === "appearance" ? "active" : ""}`}>
                  <h3>Apparence</h3>
                  <div className="settings-group">
                    <label>Thème</label>
                    <div className="theme-options">
                      <button
                        className={`theme-option ${theme === "dark" ? "active" : ""}`}
                        onClick={() => { setTheme("dark"); localStorage.setItem("iafactory_theme", "dark"); applyTheme("dark"); }}
                      >
                        🌙 Sombre
                      </button>
                      <button
                        className={`theme-option ${theme === "light" ? "active" : ""}`}
                        onClick={() => { setTheme("light"); localStorage.setItem("iafactory_theme", "light"); applyTheme("light"); }}
                      >
                        ☀️ Clair
                      </button>
                    </div>
                  </div>
                  <div className="settings-group">
                    <label>Taille de police</label>
                    <select defaultValue="medium">
                      <option value="small">Petite</option>
                      <option value="medium">Moyenne</option>
                      <option value="large">Grande</option>
                    </select>
                  </div>
                  <div className="settings-group">
                    <label>
                      <input type="checkbox" />
                      Mode compact
                    </label>
                  </div>
                </div>

                {/* Providers */}
                <div className={`settings-section ${activeSection === "providers" ? "active" : ""}`}>
                  <h3>Providers IA</h3>
                  <div className="settings-group">
                    <label>Provider par défaut</label>
                    <select defaultValue="groq">
                      <optgroup label="☁️ Cloud">
                        <option value="groq">Groq (Rapide & Gratuit)</option>
                        <option value="openai">OpenAI</option>
                        <option value="anthropic">Anthropic</option>
                        <option value="google">Google AI</option>
                        <option value="deepseek">DeepSeek</option>
                        <option value="mistral">Mistral</option>
                      </optgroup>
                      <optgroup label="🖥️ Local">
                        <option value="ollama">Ollama</option>
                        <option value="lmstudio">LM Studio</option>
                      </optgroup>
                    </select>
                  </div>
                  <div className="settings-group">
                    <label>Modèle par défaut</label>
                    <select defaultValue="auto">
                      <option value="auto">Automatique (selon provider)</option>
                    </select>
                  </div>
                  <div className="settings-group">
                    <label>Température (créativité)</label>
                    <input type="range" min="0" max="100" defaultValue="70" />
                    <span>0.7</span>
                  </div>
                  <div className="settings-group">
                    <label>Max tokens (longueur réponse)</label>
                    <select defaultValue="2048">
                      <option value="256">Court (256)</option>
                      <option value="1024">Moyen (1024)</option>
                      <option value="2048">Long (2048)</option>
                      <option value="4096">Très long (4096)</option>
                    </select>
                  </div>
                </div>

                {/* API Keys */}
                <div className={`settings-section ${activeSection === "apikeys" ? "active" : ""}`}>
                  <h3>Clés API</h3>
                  <p className="settings-info">Vos clés sont stockées localement dans votre navigateur et ne sont jamais envoyées à nos serveurs.</p>
                  <div className="api-keys-list">
                    <div className="api-key-item">
                      <div className="api-key-header">
                        <span className="api-key-name">🟢 Groq</span>
                        <span className="api-key-status">✅ Configurée</span>
                      </div>
                      <div className="api-key-actions">
                        <input type="password" placeholder="gsk_..." className="api-key-input" />
                        <button className="btn-save-key">Sauver</button>
                        <a href="https://console.groq.com/keys" target="_blank" rel="noopener noreferrer" className="btn-get-key">Obtenir</a>
                      </div>
                    </div>
                    <div className="api-key-item">
                      <div className="api-key-header">
                        <span className="api-key-name">🔵 OpenAI</span>
                        <span className="api-key-status">❌ Non configurée</span>
                      </div>
                      <div className="api-key-actions">
                        <input type="password" placeholder="sk-..." className="api-key-input" />
                        <button className="btn-save-key">Sauver</button>
                        <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer" className="btn-get-key">Obtenir</a>
                      </div>
                    </div>
                    <div className="api-key-item">
                      <div className="api-key-header">
                        <span className="api-key-name">🟤 Anthropic</span>
                        <span className="api-key-status">❌ Non configurée</span>
                      </div>
                      <div className="api-key-actions">
                        <input type="password" placeholder="sk-ant-..." className="api-key-input" />
                        <button className="btn-save-key">Sauver</button>
                        <a href="https://console.anthropic.com/settings/keys" target="_blank" rel="noopener noreferrer" className="btn-get-key">Obtenir</a>
                      </div>
                    </div>
                    <div className="api-key-item">
                      <div className="api-key-header">
                        <span className="api-key-name">🔷 DeepSeek</span>
                        <span className="api-key-status">❌ Non configurée</span>
                      </div>
                      <div className="api-key-actions">
                        <input type="password" placeholder="sk-..." className="api-key-input" />
                        <button className="btn-save-key">Sauver</button>
                        <a href="https://platform.deepseek.com/api_keys" target="_blank" rel="noopener noreferrer" className="btn-get-key">Obtenir</a>
                      </div>
                    </div>
                    <div className="api-key-item">
                      <div className="api-key-header">
                        <span className="api-key-name">🟡 Google AI</span>
                        <span className="api-key-status">❌ Non configurée</span>
                      </div>
                      <div className="api-key-actions">
                        <input type="password" placeholder="AIza..." className="api-key-input" />
                        <button className="btn-save-key">Sauver</button>
                        <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener noreferrer" className="btn-get-key">Obtenir</a>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Data */}
                <div className={`settings-section ${activeSection === "data" ? "active" : ""}`}>
                  <h3>Données & Confidentialité</h3>
                  <div className="settings-group">
                    <label>Historique des conversations</label>
                    <p className="settings-info">Vos conversations sont stockées localement.</p>
                    <button className="btn-settings">📥 Exporter les conversations</button>
                    <button className="btn-settings btn-danger">🗑️ Effacer l'historique</button>
                  </div>
                  <div className="settings-group">
                    <label>Réinitialisation</label>
                    <button className="btn-settings btn-danger">🔄 Réinitialiser tous les paramètres</button>
                  </div>
                </div>

                {/* About */}
                <div className={`settings-section ${activeSection === "about" ? "active" : ""}`}>
                  <h3>À propos</h3>
                  <div className="about-info">
                    <div className="about-logo">🇩🇿 IAFactory Algeria</div>
                    <p><strong>Version:</strong> 2.0.0</p>
                    <p><strong>Build:</strong> 2025.12.09</p>
                    <p>Plateforme IA 100% algérienne avec support trilingue (Français, Arabe incluant darija et amazigh, Anglais).</p>
                    <div className="about-links">
                      <a href="https://www.iafactoryalgeria.com" target="_blank" rel="noopener noreferrer">🌐 Site web</a>
                      <a href="/docs/documentation.html" target="_blank" rel="noopener noreferrer">📚 Documentation</a>
                      <a href="mailto:contact@iafactoryalgeria.com">📧 Contact</a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
