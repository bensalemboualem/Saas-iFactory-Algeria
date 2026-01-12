# 📚 RÉFÉRENCE COMPLÈTE - Composants IAFactory Algeria
**Version source** : Landing Page du 3 décembre 2025 (commit d7de375)
**Dernière mise à jour** : 14 décembre 2025

---

## 🎨 1. VARIABLES CSS (Design System)

### 1.1 Couleurs Dark Theme (par défaut)
```css
:root {
    --bg: #020617;           /* Background principal */
    --bg-alt: #020617;       /* Background alternatif */
    --card: #020617;         /* Background des cartes */
    --border: rgba(255, 255, 255, 0.12);  /* Bordures */
    --primary: #00a651;      /* Vert Algérie (couleur principale) */
    --primary-dark: #008c45; /* Vert Algérie foncé (hover) */
    --text: #f8fafc;         /* Texte principal */
    --muted: rgba(248, 250, 252, 0.75);  /* Texte secondaire */
    --shadow: 0 20px 60px rgba(0, 0, 0, 0.55);  /* Ombres */
}
```

### 1.2 Couleurs Light Theme
```css
[data-theme="light"] {
    --bg: #f7f5f0;
    --bg-alt: #f7f5f0;
    --card: #f7f5f0;
    --border: rgba(0, 0, 0, 0.08);
    --text: #0f172a;
    --muted: rgba(15, 23, 42, 0.7);
    --shadow: 0 20px 60px rgba(15, 23, 42, 0.25);
}
```

### 1.3 Polices
```css
body {
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}
```

---

## 📄 2. HEADER COMPLET

### 2.1 HTML Header
```html
<header>
    <div class="header-container">
        <!-- Logo -->
        <a href="/" class="header-logo">
            <img src="https://flagcdn.com/w40/dz.png" alt="Algérie" class="logo-flag">
            <span class="logo-text">
                <span class="highlight">IA</span>Factory
                Alger<span class="highlight">ia</span>
            </span>
        </a>

        <!-- Navigation principale -->
        <nav class="header-nav">
            <a class="nav-link" href="/apps.html">📱 Applications</a>
            <a class="nav-link" href="/docs/tarifs.html">Tarifs</a>
            <a class="nav-link" href="/docs/documentation.html">Documentation</a>
        </nav>

        <!-- Actions header -->
        <div class="header-actions">
            <!-- Toggle User/Dev -->
            <div class="profile-toggle">
                <button class="profile-btn active" data-profile="user">👤 Utilisateur</button>
                <button class="profile-btn" data-profile="dev">👨‍💻 Développeur</button>
            </div>

            <!-- Boutons auth -->
            <a href="/docs/login.html" class="btn-login">Log in</a>
            <a href="/docs/getstarted.html" class="btn-get-started">Get Started</a>

            <!-- Toggle theme -->
            <button class="theme-toggle" onclick="toggleTheme()">
                <span class="theme-icon-sun">☀️</span>
                <span class="theme-icon-moon" style="display: none;">🌙</span>
            </button>
        </div>
    </div>
</header>
```

### 2.2 CSS Header
```css
/* ========== HEADER ========== */
header {
    position: sticky;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
    backdrop-filter: blur(14px);
    border-bottom: 1px solid var(--border);
    background: rgba(2, 6, 23, 0.85);
}

[data-theme="light"] header {
    background: rgba(247, 245, 240, 0.95);
}

.header-container {
    max-width: 1400px;
    margin: 0 auto;
    height: 70px;
    padding: 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
}

.header-logo {
    display: flex;
    align-items: center;
    gap: 10px;
}

.logo-flag {
    width: 32px;
}

.logo-text {
    font-size: 18px;
    font-weight: 700;
}

.highlight {
    color: var(--primary);
}

.header-nav {
    display: flex;
    gap: 28px;
}

.nav-link {
    font-size: 15px;
    font-weight: 500;
    text-decoration: none;
    color: var(--muted);
    transition: color 0.3s ease;
}

.nav-link:hover {
    color: var(--primary);
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 12px;
}

.profile-toggle {
    display: flex;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 999px;
    padding: 4px;
    gap: 4px;
}

[data-theme="light"] .profile-toggle {
    background: rgba(0, 0, 0, 0.05);
}

.profile-btn {
    padding: 8px 16px;
    background: transparent;
    border: none;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 500;
    color: var(--muted);
    cursor: pointer;
    transition: all 0.3s ease;
}

.profile-btn.active {
    color: var(--primary);
    background: rgba(0, 166, 81, 0.15);
}

.btn-login {
    padding: 8px 20px;
    border-radius: 8px;
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text);
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.btn-login:hover {
    border-color: var(--primary);
    color: var(--primary);
}

.btn-get-started {
    padding: 8px 20px;
    border-radius: 8px;
    border: none;
    background: var(--primary);
    color: #021014;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-get-started:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 166, 81, 0.3);
}

.theme-toggle {
    border-radius: 8px;
    border: none;
    padding: 8px 12px;
    background: rgba(255, 255, 255, 0.05);
    color: var(--text);
    cursor: pointer;
    font-size: 16px;
    transition: all 0.3s ease;
}

[data-theme="light"] .theme-toggle {
    background: rgba(0, 0, 0, 0.05);
}

.theme-toggle:hover {
    background: rgba(255, 255, 255, 0.1);
}

[data-theme="light"] .theme-toggle:hover {
    background: rgba(0, 0, 0, 0.1);
}
```

---

## 📦 3. FOOTER COMPLET

### 3.1 HTML Footer
```html
<footer>
    <div class="footer-grid">
        <!-- Colonne 1 : Info + Réseaux sociaux -->
        <div class="footer-col">
            <h4>IAFactory Algeria</h4>
            <p>Plateforme IA souveraine pour institutions algériennes, public et privé.</p>
            <p style="margin-top: 0.5rem;">
                <i class="fas fa-map-marker-alt"></i> Alger, Algérie
            </p>

            <!-- Réseaux Sociaux (9 icônes SVG) -->
            <div class="social-links">
                <!-- TikTok -->
                <a href="#" class="social-link" aria-label="TikTok">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/>
                    </svg>
                </a>
                <!-- Répéter pour YouTube, Instagram, Facebook, LinkedIn, X, Discord, Reddit, Telegram -->
                <!-- ... (voir extraction complète ci-dessus) -->
            </div>
        </div>

        <!-- Colonne 2 : Produits -->
        <div class="footer-col">
            <h4>Produits</h4>
            <ul>
                <li><a href="docs/rag-assistants.html">RAG Assistants</a></li>
                <li><a href="docs/business-apps.html">Business Apps</a></li>
                <li><a href="docs/developer-tools.html">Developer Tools</a></li>
            </ul>
        </div>

        <!-- Colonne 3 : Directory IA -->
        <div class="footer-col">
            <h4>Directory IA</h4>
            <ul>
                <li><a href="docs/directory/ia-tools.html">🔧 Outils IA</a></li>
                <li><a href="docs/directory/agents.html">🤖 Agents IA</a></li>
                <li><a href="docs/directory/workflows.html">⚡ Workflows</a></li>
                <li><a href="docs/directory/daily-news.html">📰 Daily News</a></li>
            </ul>
        </div>

        <!-- Colonne 4 : Entreprise -->
        <div class="footer-col">
            <h4>Entreprise</h4>
            <ul>
                <li><a href="docs/a-propos.html">À propos</a></li>
                <li><a href="docs/blog.html">Blog</a></li>
                <li><a href="docs/contact.html">Contact</a></li>
            </ul>
        </div>

        <!-- Colonne 5 : Legal -->
        <div class="footer-col">
            <h4>Legal</h4>
            <ul>
                <li><a href="docs/confidentialite.html">Confidentialité</a></li>
                <li><a href="docs/conditions.html">Conditions</a></li>
                <li><a href="docs/mentions.html">Mentions</a></li>
            </ul>
        </div>
    </div>

    <div class="footer-bottom">
        © 2025 IAFactory Algeria. Tous droits réservés.
    </div>
</footer>
```

### 3.2 CSS Footer
```css
/* ========== FOOTER ========== */
footer {
    padding: 3rem 2rem;
    background: var(--card);
    border-top: 1px solid var(--border);
}

.footer-grid {
    max-width: 1400px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
    gap: 2rem;
}

.footer-col {
    min-width: 0;
}

.footer-col h4 {
    margin-bottom: 0.75rem;
    font-size: 0.95rem;
}

.footer-col p {
    color: var(--muted);
    font-size: 0.85rem;
    margin: 0;
}

.footer-col ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
}

.footer-col a {
    color: var(--muted);
    font-size: 0.85rem;
    transition: color 0.2s ease;
    text-decoration: none;
}

.footer-col a:hover {
    color: var(--primary);
}

.footer-bottom {
    max-width: 1200px;
    margin: 2rem auto 0;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
    text-align: center;
    color: var(--muted);
    font-size: 0.85rem;
}

/* Social Links */
.social-links {
    display: flex;
    gap: 8px;
    flex-wrap: nowrap;
    margin-top: 1rem;
    max-width: 100%;
}

.social-link {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 50%;
    color: var(--muted);
    transition: all 0.2s ease;
}

.social-link:hover {
    background: var(--primary);
    color: #021014;
    transform: translateY(-2px);
}

/* Responsive */
@media (max-width: 768px) {
    .footer-grid {
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }
}
```

---

## 🔲 4. SIDEBAR + CHATBOT IA (Composant qui fonctionne!)

### 4.1 HTML Sidebar
```html
<!-- Zone hover sidebar gauche -->
<div class="sidebar-hover-zone"></div>

<!-- Sidebar -->
<div class="sidebar" id="sidebar">
    <div class="sidebar-header">
        <div class="sidebar-logo">
            <img src="https://flagcdn.com/w40/dz.png" alt="DZ">
            <span>IAFactory Algeria</span>
        </div>
        <button class="btn-new-chat" onclick="nouvelleConversation()">
            <i class="fas fa-plus"></i> Nouvelle conversation
        </button>
    </div>

    <div class="sidebar-nav">
        <button class="nav-item active" onclick="navChatIA()">
            <i class="fas fa-comment-dots"></i> Chat IA
        </button>
        <button class="nav-item" onclick="toggleAppsPanel()">
            <i class="fas fa-th"></i> Applications
        </button>
        <button class="nav-item" onclick="navRAGSearch()">
            <i class="fas fa-search"></i> Recherche RAG
        </button>
        <button class="nav-item" onclick="navParametres()">
            <i class="fas fa-cog"></i> Paramètres
        </button>
    </div>

    <!-- Liste conversations récentes (exemples) -->
    <div class="sidebar-chats">
        <button class="chat-item" onclick="loadConversation(1)">
            <i class="fas fa-comment"></i> Conversation 1
        </button>
        <button class="chat-item" onclick="loadConversation(2)">
            <i class="fas fa-comment"></i> Conversation 2
        </button>
    </div>

    <div class="sidebar-footer">
        <p style="font-size: 0.8rem; color: var(--muted);">
            © 2025 IAFactory
        </p>
    </div>
</div>
```

### 4.2 CSS Sidebar
```css
/* ========== SIDEBAR ========== */
.sidebar-hover-zone {
    position: fixed;
    top: 70px;
    left: 0;
    width: 280px;
    height: calc(100vh - 70px);
    z-index: 89;
}

.sidebar {
    position: fixed;
    top: 70px;
    left: 0;
    width: 280px;
    height: calc(100vh - 70px);
    background: var(--card);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    z-index: 90;
    transition: transform 0.3s ease;
    transform: translateX(0);
}

.sidebar.hidden {
    transform: translateX(-100%);
}

.sidebar-header {
    padding: 16px;
    border-bottom: 1px solid var(--border);
}

.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
}

.sidebar-logo img {
    width: 24px;
}

.sidebar-logo span {
    font-weight: 700;
    font-size: 14px;
}

.btn-new-chat {
    width: 100%;
    padding: 10px 16px;
    background: var(--primary);
    color: #021014;
    border: none;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: all 0.2s ease;
}

.btn-new-chat:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 166, 81, 0.3);
}

.sidebar-nav {
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border-radius: 10px;
    border: none;
    background: transparent;
    color: var(--muted);
    cursor: pointer;
    font-size: 14px;
    text-align: left;
    width: 100%;
    transition: all 0.2s ease;
}

.nav-item:hover {
    background: rgba(255, 255, 255, 0.05);
    color: var(--text);
}

.nav-item.active {
    background: rgba(0, 166, 81, 0.15);
    color: var(--primary);
}

.sidebar-chats {
    flex: 1;
    overflow-y: auto;
    padding: 12px;
}

.chat-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border-radius: 8px;
    border: none;
    background: transparent;
    color: var(--muted);
    cursor: pointer;
    font-size: 13px;
    text-align: left;
    width: 100%;
    margin-bottom: 4px;
    transition: all 0.2s ease;
}

.chat-item:hover {
    background: rgba(255, 255, 255, 0.05);
    color: var(--text);
}

.sidebar-footer {
    padding: 16px;
    border-top: 1px solid var(--border);
    text-align: center;
}
```

---

## 💬 5. CHATBOT HELP FLOTTANT (Bouton d'aide)

### 5.1 HTML Chatbot Help
```html
<!-- ========== CHATBOT HELP FLOTTANT ========== -->
<div class="help-bubble" id="helpBubble">
    <span class="help-label">Dzir IA - Aide</span>
    <button class="help-btn" onclick="toggleHelpWindow()">💬</button>

    <div class="help-window" id="helpWindow">
        <div class="help-header">
            <h3>🤖 Dzir IA</h3>
            <button class="close-help-btn" onclick="toggleHelpWindow()">×</button>
        </div>

        <!-- 3 MODES : Chat IA / Recherche RAG / Support -->
        <div class="help-modes">
            <button class="help-mode-btn active" id="chatModeBtn" onclick="setHelpMode('chat')">
                💬 Chat IA
            </button>
            <button class="help-mode-btn" id="ragModeBtn" onclick="setHelpMode('rag')">
                🔍 Recherche RAG
            </button>
            <button class="help-mode-btn" id="supportModeBtn" onclick="setHelpMode('support')">
                📞 Support
            </button>
        </div>

        <!-- SÉLECTEUR RAG (affiché en mode Recherche) -->
        <div class="help-rag-selector" id="helpRagSelector" style="display: none;">
            <select id="helpRagSelect">
                <option value="DZ">🇩🇿 Business DZ (Algérie)</option>
                <option value="CH">🎓 École (Suisse)</option>
                <option value="GLOBAL">🕌 Islam (Global)</option>
                <option value="ALL">🌍 Tous les RAG</option>
            </select>
        </div>

        <!-- BANNER SUPPORT (affiché en mode Support) -->
        <div class="help-support-banner" id="helpSupportBanner" style="display: none;">
            ⚠️ Mode support humain activé
            <br>
            <button class="back-to-ai-btn" onclick="setHelpMode('chat')">
                🤖 Revenir au mode IA
            </button>
        </div>

        <!-- MESSAGES -->
        <div class="help-messages" id="helpMessages">
            <div class="help-message help-bot">
                <div class="help-avatar">
                    <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #00843D 0%, #2ecc71 100%); color: white; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 11px; box-shadow: 0 2px 8px rgba(0,132,61,0.3);">
                        DZ
                    </div>
                </div>
                <div class="help-bubble-msg">
                    👋 Bonjour ! Je suis <strong>Dzir IA</strong>, votre assistant IAFactory Algeria.
                    Comment puis-je vous aider ?
                </div>
            </div>
        </div>

        <!-- INPUT -->
        <div class="help-input-area">
            <button class="help-attach-btn">📎</button>
            <input
                type="text"
                class="help-input"
                placeholder="Posez votre question..."
                onkeypress="if(event.key === 'Enter') sendHelpMessage()"
            />
            <button class="help-send-btn" onclick="sendHelpMessage()">
                <i class="fas fa-paper-plane"></i>
            </button>
        </div>
    </div>
</div>
```

### 5.2 CSS Chatbot Help
```css
/* ========== CHATBOT HELP FLOTTANT ========== */
.help-bubble {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 999;
    display: flex;
    align-items: center;
    gap: 12px;
}

.help-label {
    background: var(--card);
    color: var(--text);
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 500;
    border: 1px solid var(--border);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.help-btn {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    border: none;
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
    font-size: 24px;
    cursor: pointer;
    box-shadow: 0 4px 16px rgba(0, 166, 81, 0.4);
    transition: all 0.3s ease;
}

.help-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 20px rgba(0, 166, 81, 0.6);
}

.help-window {
    position: fixed;
    bottom: 90px;
    right: 24px;
    width: 380px;
    height: 550px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    display: none;
    flex-direction: column;
    overflow: hidden;
}

.help-window.show {
    display: flex;
}

.help-header {
    padding: 16px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
}

.help-header h3 {
    margin: 0;
    font-size: 16px;
}

.close-help-btn {
    background: transparent;
    border: none;
    color: white;
    font-size: 24px;
    cursor: pointer;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background 0.2s ease;
}

.close-help-btn:hover {
    background: rgba(255, 255, 255, 0.2);
}

.help-modes {
    display: flex;
    gap: 8px;
    padding: 12px;
    border-bottom: 1px solid var(--border);
}

.help-mode-btn {
    flex: 1;
    padding: 8px 12px;
    background: transparent;
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--muted);
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.help-mode-btn:hover {
    background: rgba(255, 255, 255, 0.05);
}

.help-mode-btn.active {
    background: rgba(0, 166, 81, 0.15);
    color: var(--primary);
    border-color: var(--primary);
}

.help-messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.help-message {
    display: flex;
    gap: 10px;
    align-items: flex-start;
}

.help-avatar {
    flex-shrink: 0;
}

.help-bubble-msg {
    background: rgba(255, 255, 255, 0.05);
    padding: 12px 16px;
    border-radius: 12px;
    font-size: 14px;
    line-height: 1.5;
    max-width: 80%;
}

.help-input-area {
    padding: 12px;
    border-top: 1px solid var(--border);
    display: flex;
    gap: 8px;
    align-items: center;
}

.help-attach-btn {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: transparent;
    color: var(--muted);
    font-size: 16px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.help-attach-btn:hover {
    background: rgba(255, 255, 255, 0.05);
}

.help-input {
    flex: 1;
    padding: 10px 14px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text);
    font-size: 14px;
    outline: none;
}

.help-input:focus {
    border-color: var(--primary);
}

.help-send-btn {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    border: none;
    background: var(--primary);
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
}

.help-send-btn:hover {
    background: var(--primary-dark);
    transform: translateY(-1px);
}
```

---

## ⚡ 6. FONCTIONS JAVASCRIPT GLOBALES

### 6.1 Fonction Toggle Theme
```javascript
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);

    // Update theme icons
    const sunIcon = document.querySelector('.theme-icon-sun');
    const moonIcon = document.querySelector('.theme-icon-moon');

    if (newTheme === 'light') {
        sunIcon.style.display = 'none';
        moonIcon.style.display = 'inline';
    } else {
        sunIcon.style.display = 'inline';
        moonIcon.style.display = 'none';
    }
}

// Load theme from localStorage on page load
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);

    const sunIcon = document.querySelector('.theme-icon-sun');
    const moonIcon = document.querySelector('.theme-icon-moon');

    if (savedTheme === 'light') {
        sunIcon.style.display = 'none';
        moonIcon.style.display = 'inline';
    }
});
```

### 6.2 Fonction Sidebar
```javascript
function nouvelleConversation() {
    // Créer nouvelle conversation
    console.log('Nouvelle conversation créée');
    // TODO: Appel API pour créer nouvelle conversation
}

function navChatIA() {
    // Navigation vers Chat IA
    console.log('Navigation Chat IA');
}

function toggleAppsPanel() {
    const appsPanel = document.getElementById('appsPanel');
    appsPanel.classList.toggle('show');
}

function navRAGSearch() {
    console.log('Navigation Recherche RAG');
}

function navParametres() {
    console.log('Navigation Paramètres');
}

function loadConversation(id) {
    console.log('Chargement conversation:', id);
}

// Open/close sidebar on hover
const sidebarHoverZone = document.querySelector('.sidebar-hover-zone');
const sidebar = document.getElementById('sidebar');

function openSidebar() {
    sidebar.classList.remove('hidden');
}

function closeSidebar() {
    sidebar.classList.add('hidden');
}

sidebarHoverZone.addEventListener('mouseenter', openSidebar);
sidebar.addEventListener('mouseleave', closeSidebar);
```

### 6.3 Fonction Chatbot Help
```javascript
function toggleHelpWindow() {
    const helpWindow = document.getElementById('helpWindow');
    helpWindow.classList.toggle('show');
}

function setHelpMode(mode) {
    // Update active button
    document.querySelectorAll('.help-mode-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    const buttons = {
        'chat': 'chatModeBtn',
        'rag': 'ragModeBtn',
        'support': 'supportModeBtn'
    };

    document.getElementById(buttons[mode]).classList.add('active');

    // Show/hide mode-specific elements
    const ragSelector = document.getElementById('helpRagSelector');
    const supportBanner = document.getElementById('helpSupportBanner');

    ragSelector.style.display = mode === 'rag' ? 'block' : 'none';
    supportBanner.style.display = mode === 'support' ? 'block' : 'none';
}

function sendHelpMessage() {
    const input = document.querySelector('.help-input');
    const message = input.value.trim();

    if (!message) return;

    // Add user message to chat
    const messagesContainer = document.getElementById('helpMessages');
    const userMsg = document.createElement('div');
    userMsg.className = 'help-message help-user';
    userMsg.innerHTML = `
        <div class="help-bubble-msg">${message}</div>
    `;
    messagesContainer.appendChild(userMsg);

    // Clear input
    input.value = '';

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    // TODO: Send to AI API
}
```

---

## 📋 7. CHECKLIST D'INTÉGRATION

### Pour appliquer ces composants à une nouvelle page :

1. **CSS Variables** : Copier le `:root` et `[data-theme="light"]` dans le `<style>`
2. **Header** : Copier HTML + CSS header
3. **Footer** : Copier HTML + CSS footer
4. **Sidebar** (optionnel) : Copier HTML + CSS + JS sidebar
5. **Chatbot Help** (optionnel) : Copier HTML + CSS + JS chatbot
6. **JavaScript** : Copier les fonctions globales dans `<script>`
7. **Font Awesome** : Ajouter `<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">`

---

## 🎯 8. URLS & LIENS IMPORTANTS

### Liens Header
- Applications : `/apps.html`
- Tarifs : `/docs/tarifs.html`
- Documentation : `/docs/documentation.html`
- Login : `/docs/login.html`
- Get Started : `/docs/getstarted.html`

### Liens Footer Produits
- RAG Assistants : `docs/rag-assistants.html`
- Business Apps : `docs/business-apps.html`
- Developer Tools : `docs/developer-tools.html`

### Liens Footer Directory
- Outils IA : `docs/directory/ia-tools.html`
- Agents IA : `docs/directory/agents.html`
- Workflows : `docs/directory/workflows.html`
- Daily News : `docs/directory/daily-news.html`

### Liens Footer Entreprise
- À propos : `docs/a-propos.html`
- Blog : `docs/blog.html`
- Contact : `docs/contact.html`

### Liens Footer Legal
- Confidentialité : `docs/confidentialite.html`
- Conditions : `docs/conditions.html`
- Mentions : `docs/mentions.html`

---

## 🔧 9. RESPONSIVE BREAKPOINTS

```css
/* Mobile */
@media (max-width: 768px) {
    .header-nav {
        display: none;
    }

    .footer-grid {
        grid-template-columns: 1fr;
    }

    .sidebar {
        width: 100%;
    }
}

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) {
    .header-container {
        padding: 0 16px;
    }
}
```

---

## ✅ NEXT STEPS

1. ✅ **PHASE 1 TERMINÉE** : Document de référence créé
2. 🔄 **PHASE 2** : Créer les fichiers composants partagés individuels
3. 🔄 **PHASE 3** : Tester sur 3 pages pilotes
4. 🔄 **PHASE 4** : Harmoniser toutes les pages
5. 🔄 **PHASE 5** : Vérification finale

---

**Document créé le** : 14 décembre 2025
**Version** : 1.0
**Mainteneur** : IAFactory Team
