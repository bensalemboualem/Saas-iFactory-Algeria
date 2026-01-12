#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour améliorer les 26 apps stubs avec du contenu professionnel
"""
from pathlib import Path
import re

# Liste des 26 stubs à améliorer
STUBS_TO_UPGRADE = [
    "agri-dz", "agroalimentaire-dz", "bmad", "btp-dz", "clinique-dz",
    "commerce-dz", "creative-studio", "dashboard", "data-dz", "data-dz-dashboard",
    "dev-portal", "developer", "douanes-dz", "ecommerce-dz", "expert-comptable-dz",
    "fiscal-assistant", "formation-pro-dz", "industrie-dz", "irrigation-dz", "islam-dz",
    "ithy", "landing", "legal-assistant", "pharma-dz", "transport-dz", "universite-dz"
]

def extract_app_info(html_content):
    """Extraire les infos de l'app depuis le HTML existant"""
    title_match = re.search(r'<title>(.+?)</title>', html_content)
    title = title_match.group(1) if title_match else "Application"

    # Extraire l'icône
    icon_match = re.search(r'([🌾🏭🏛️🎨📊🔧👨‍💻📦🛒💼🏦📚🏗️💧🕌🧠📄💊🚚🎓])', title)
    icon = icon_match.group(1) if icon_match else "🚀"

    return {"title": title, "icon": icon}

def enhance_html(original_html, app_info):
    """Améliorer le HTML avec du contenu professionnel"""

    # Ajouter du JavaScript professionnel
    js_code = """
    <script>
        // Configuration
        const APP_CONFIG = {
            name: document.title,
            version: '1.0.0',
            apiUrl: window.location.origin + '/api'
        };

        // Initialisation
        document.addEventListener('DOMContentLoaded', function() {
            console.log(`✅ ${APP_CONFIG.name} - Application initialisée`);
            initializeApp();
        });

        // Fonction d'initialisation
        function initializeApp() {
            // Vérifier la connexion API
            checkAPIHealth();

            // Initialiser les événements
            initializeEvents();

            // Charger les données
            loadInitialData();
        }

        // Vérification santé API
        async function checkAPIHealth() {
            try {
                const response = await fetch('/api/health');
                if (response.ok) {
                    updateStatus('Connecté', 'success');
                }
            } catch (error) {
                updateStatus('Hors ligne', 'error');
            }
        }

        // Initialiser les événements
        function initializeEvents() {
            // Boutons d'action
            document.querySelectorAll('.action-btn').forEach(btn => {
                btn.addEventListener('click', handleAction);
            });

            // Theme toggle
            const themeToggle = document.querySelector('[data-theme-toggle]');
            if (themeToggle) {
                themeToggle.addEventListener('click', toggleTheme);
            }
        }

        // Gestionnaire d'actions
        function handleAction(e) {
            const action = e.target.dataset.action;
            console.log('Action:', action);
            showNotification(`Action: ${action}`, 'info');
        }

        // Toggle theme
        function toggleTheme() {
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        }

        // Charger les données initiales
        async function loadInitialData() {
            // TODO: Implémenter le chargement des données
            console.log('Chargement des données...');
        }

        // Mettre à jour le statut
        function updateStatus(message, type) {
            const statusEl = document.querySelector('.status-indicator');
            if (statusEl) {
                statusEl.textContent = message;
                statusEl.className = `status-indicator status-${type}`;
            }
        }

        // Afficher une notification
        function showNotification(message, type = 'info') {
            console.log(`[${type.toUpperCase()}] ${message}`);
            // TODO: Implémenter un système de notifications visuelles
        }

        // Utilitaires
        const utils = {
            formatDate: (date) => new Date(date).toLocaleDateString('fr-DZ'),
            formatNumber: (num) => new Intl.NumberFormat('fr-DZ').format(num),
            debounce: (func, wait) => {
                let timeout;
                return function executedFunction(...args) {
                    const later = () => {
                        clearTimeout(timeout);
                        func(...args);
                    };
                    clearTimeout(timeout);
                    timeout = setTimeout(later, wait);
                };
            }
        };
    </script>"""

    # Ajouter du CSS amélioré
    css_additions = """
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .fade-in {
            animation: fadeIn 0.5s ease-out;
        }

        /* Status Indicator */
        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 2rem;
            font-size: 0.875rem;
            font-weight: 500;
        }

        .status-success {
            background: rgba(16, 185, 129, 0.1);
            color: #10b981;
        }

        .status-success::before {
            content: '●';
            animation: pulse 2s infinite;
        }

        .status-error {
            background: rgba(239, 68, 68, 0.1);
            color: #ef4444;
        }

        .status-info {
            background: rgba(59, 130, 246, 0.1);
            color: #3b82f6;
        }

        /* Action Buttons */
        .action-btn {
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            border: none;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }

        .action-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }

        /* Loading */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: var(--primary);
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Responsive improvements */
        @media (max-width: 640px) {
            .header { padding: 1rem; }
            .container { padding: 1rem; }
        }
    """

    # Insérer le CSS avant </style>
    enhanced_html = original_html.replace('</style>', css_additions + '\n    </style>')

    # Insérer le JS avant </body>
    enhanced_html = enhanced_html.replace('</body>', js_code + '\n</body>')

    # Ajouter un indicateur de statut dans le header si pas présent
    if 'status-indicator' not in enhanced_html and '.header' in enhanced_html:
        status_html = '<div class="status-indicator status-success">Service actif</div>'
        # Trouver la fermeture du header et ajouter le status
        enhanced_html = re.sub(
            r'(</header>)',
            status_html + r'\n    \1',
            enhanced_html,
            count=1
        )

    return enhanced_html

def main():
    """Fonction principale"""
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    apps_dir = Path(r"d:\IAFactory\rag-dz\apps")

    print("="*80)
    print("AMELIORATION DES 26 APPS STUBS")
    print("="*80)

    upgraded_count = 0

    for app_name in STUBS_TO_UPGRADE:
        app_path = apps_dir / app_name
        index_path = app_path / "index.html"

        if not index_path.exists():
            print(f"\n[SKIP] {app_name} - index.html non trouve")
            continue

        print(f"\n[UPGRADE] {app_name}")

        # Lire le HTML existant
        with open(index_path, 'r', encoding='utf-8') as f:
            original_html = f.read()

        # Extraire les infos
        app_info = extract_app_info(original_html)
        print(f"  Titre: {app_info['title']}")
        print(f"  Icone: {app_info['icon']}")

        # Améliorer le HTML
        enhanced_html = enhance_html(original_html, app_info)

        # Écrire le fichier amélioré
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_html)

        print(f"  [OK] Ameliore avec succes")
        upgraded_count += 1

    print("\n" + "="*80)
    print(f"[OK] {upgraded_count} applications ameliorees!")
    print("="*80)

if __name__ == "__main__":
    main()
