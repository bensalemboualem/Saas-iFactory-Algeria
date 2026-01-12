import React, { useState, useEffect } from 'react';

export function Sidebar() {
  const [expanded, setExpanded] = useState(false);
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [activeSection, setActiveSection] = useState('general');

  useEffect(() => {
    const savedTheme = localStorage.getItem('iafactory_theme') as 'dark' | 'light' || 'dark';
    setTheme(savedTheme);
    applyTheme(savedTheme);
  }, []);

  const applyTheme = (newTheme: 'dark' | 'light') => {
    document.body.setAttribute('data-theme', newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
    if (newTheme === 'dark') {
      document.body.classList.add('dark');
      document.documentElement.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
      document.documentElement.classList.remove('dark');
    }
  };

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('iafactory_theme', newTheme);
    applyTheme(newTheme);
  };

  const createNewChat = () => {
    console.log('New Chat');
  };

  const openSettings = () => {
    setSettingsOpen(true);
  };

  const closeSettings = () => {
    setSettingsOpen(false);
  };

  const openUserMenu = () => {
    console.log('User menu');
  };

  return (
    <>
      <aside
        className={`iaf-sidebar ${expanded ? 'expanded' : ''}`}
        id="iafSidebar"
        role="complementary"
        aria-label="Sidebar principale"
        onMouseEnter={() => setExpanded(true)}
        onMouseLeave={() => setExpanded(false)}
      >
        <div className="iaf-sidebar-content">
          {/* Logo Section (Top) */}
          <a href="https://www.iafactoryalgeria.com" className="iaf-sidebar-logo" aria-label="IAFactory Algeria" dir="ltr">
            <img src="https://flagcdn.com/w40/dz.png" alt="Algerie" className="sidebar-logo-flag" />
            <span className="sidebar-logo-text">
              <span className="letter i-drop" style={{ color: '#00a651', animationDelay: '0s' }}>
                <span className="i-stem">i</span>
                <span className="i-dot">.</span>
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
                <span className="i-stem">i</span>
                <span className="i-dot">.</span>
              </span>
              <span className="letter" style={{ color: '#00a651', animationDelay: '1.5s' }}>a</span>
            </span>
          </a>

          {/* Main Actions (Top) */}
          <nav className="iaf-sidebar-main" role="navigation" aria-label="Navigation principale">
            {/* New Chat */}
            <button className="iaf-sidebar-item" onClick={createNewChat}>
              <i className="fa-solid fa-plus iaf-sidebar-icon"></i>
              <span className="iaf-sidebar-label">Nouveau Chat</span>
            </button>

            {/* Projects */}
            <a href="#projects" className="iaf-sidebar-item">
              <i className="fa-solid fa-folder iaf-sidebar-icon"></i>
              <span className="iaf-sidebar-label">Projets</span>
            </a>

            {/* Archive / History */}
            <a href="#archive" className="iaf-sidebar-item">
              <i className="fa-solid fa-clock-rotate-left iaf-sidebar-icon"></i>
              <span className="iaf-sidebar-label">Historique</span>
            </a>
          </nav>

          {/* Bottom Section */}
          <div className="iaf-sidebar-bottom">
            {/* Settings + Theme (Horizontal) */}
            <div className="iaf-sidebar-actions">
              {/* Settings Button */}
              <button className="iaf-sidebar-btn" onClick={openSettings} title="Parametres">
                <span style={{ fontSize: '18px' }}>⚙️</span>
              </button>

              {/* Theme Toggle */}
              <button className="iaf-sidebar-btn" onClick={toggleTheme} title="Changer le theme">
                <span id="themeIcon" style={{ fontSize: '18px' }}>{theme === 'dark' ? '☀️' : '🌙'}</span>
              </button>
            </div>

            {/* User Info Button */}
            <button className="iaf-sidebar-user" onClick={openUserMenu}>
              <div className="iaf-user-avatar" id="userAvatar">AB</div>
              <div className="iaf-user-info">
                <div className="iaf-user-name" id="userName">Ahmed Benali</div>
                <div className="iaf-user-meta">
                  <span className="iaf-user-profile" id="userProfile">Utilisateur</span>
                  <span className="iaf-user-separator">•</span>
                  <span className="iaf-user-tokens" id="userTokens">
                    <span className="tokens-count">2,500</span> <span>tokens</span>
                  </span>
                </div>
              </div>
              <i className="fa-solid fa-ellipsis-vertical iaf-user-menu-icon"></i>
            </button>
          </div>
        </div>
      </aside>

      {/* Settings Modal */}
      {settingsOpen && (
        <div className="settings-modal" style={{ display: 'flex' }}>
          <div className="settings-overlay" onClick={closeSettings}></div>
          <div className="settings-container">
            <div className="settings-header">
              <h2>⚙️ Parametres</h2>
              <button className="settings-close" onClick={closeSettings}>✕</button>
            </div>
            <div className="settings-body">
              {/* Sidebar Navigation */}
              <div className="settings-sidebar">
                <button
                  className={`settings-nav-item ${activeSection === 'general' ? 'active' : ''}`}
                  onClick={() => setActiveSection('general')}
                >
                  <i className="fas fa-sliders-h"></i> General
                </button>
                <button
                  className={`settings-nav-item ${activeSection === 'appearance' ? 'active' : ''}`}
                  onClick={() => setActiveSection('appearance')}
                >
                  <i className="fas fa-palette"></i> Apparence
                </button>
                <button
                  className={`settings-nav-item ${activeSection === 'providers' ? 'active' : ''}`}
                  onClick={() => setActiveSection('providers')}
                >
                  <i className="fas fa-cloud"></i> Providers IA
                </button>
                <button
                  className={`settings-nav-item ${activeSection === 'apikeys' ? 'active' : ''}`}
                  onClick={() => setActiveSection('apikeys')}
                >
                  <i className="fas fa-key"></i> Cles API
                </button>
                <button
                  className={`settings-nav-item ${activeSection === 'data' ? 'active' : ''}`}
                  onClick={() => setActiveSection('data')}
                >
                  <i className="fas fa-database"></i> Donnees
                </button>
                <button
                  className={`settings-nav-item ${activeSection === 'about' ? 'active' : ''}`}
                  onClick={() => setActiveSection('about')}
                >
                  <i className="fas fa-info-circle"></i> A propos
                </button>
              </div>

              {/* Content Sections */}
              <div className="settings-content">
                {/* General */}
                <div className={`settings-section ${activeSection === 'general' ? 'active' : ''}`}>
                  <h3>Parametres generaux</h3>
                  <div className="settings-group">
                    <label>Langue de l'interface</label>
                    <select defaultValue="fr">
                      <option value="fr">🇫🇷 Francais</option>
                      <option value="en">🇬🇧 English</option>
                      <option value="ar">🇩🇿 العربية</option>
                    </select>
                  </div>
                  <div className="settings-group">
                    <label>Profil par defaut</label>
                    <select defaultValue="user">
                      <option value="user">👤 Utilisateur</option>
                      <option value="dev">👨‍💻 Developpeur</option>
                    </select>
                  </div>
                </div>

                {/* Appearance */}
                <div className={`settings-section ${activeSection === 'appearance' ? 'active' : ''}`}>
                  <h3>Apparence</h3>
                  <div className="settings-group">
                    <label>Theme</label>
                    <div className="theme-options">
                      <button
                        className={`theme-option ${theme === 'dark' ? 'active' : ''}`}
                        onClick={() => { setTheme('dark'); localStorage.setItem('iafactory_theme', 'dark'); applyTheme('dark'); }}
                      >
                        🌙 Sombre
                      </button>
                      <button
                        className={`theme-option ${theme === 'light' ? 'active' : ''}`}
                        onClick={() => { setTheme('light'); localStorage.setItem('iafactory_theme', 'light'); applyTheme('light'); }}
                      >
                        ☀️ Clair
                      </button>
                    </div>
                  </div>
                </div>

                {/* Providers */}
                <div className={`settings-section ${activeSection === 'providers' ? 'active' : ''}`}>
                  <h3>Providers IA</h3>
                  <div className="settings-group">
                    <label>Provider par defaut</label>
                    <select defaultValue="groq">
                      <optgroup label="☁️ Cloud">
                        <option value="groq">Groq (Rapide &amp; Gratuit)</option>
                        <option value="openai">OpenAI</option>
                        <option value="anthropic">Anthropic</option>
                      </optgroup>
                      <optgroup label="🖥️ Local">
                        <option value="ollama">Ollama</option>
                      </optgroup>
                    </select>
                  </div>
                </div>

                {/* API Keys */}
                <div className={`settings-section ${activeSection === 'apikeys' ? 'active' : ''}`}>
                  <h3>Cles API</h3>
                  <p className="settings-info">Vos cles sont stockees localement.</p>
                  <div className="api-keys-list">
                    <div className="api-key-item">
                      <div className="api-key-header">
                        <span className="api-key-name">🟢 Groq</span>
                        <span className="api-key-status">✅ Configuree</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Data */}
                <div className={`settings-section ${activeSection === 'data' ? 'active' : ''}`}>
                  <h3>Donnees &amp; Confidentialite</h3>
                  <div className="settings-group">
                    <button className="btn-settings">📥 Exporter les conversations</button>
                    <button className="btn-settings btn-danger">🗑️ Effacer l'historique</button>
                  </div>
                </div>

                {/* About */}
                <div className={`settings-section ${activeSection === 'about' ? 'active' : ''}`}>
                  <h3>A propos</h3>
                  <div className="about-info">
                    <div className="about-logo">🇩🇿 IAFactory Algeria</div>
                    <p><strong>Version:</strong> 2.0.0</p>
                    <p>Plateforme IA 100% algerienne.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default Sidebar;
