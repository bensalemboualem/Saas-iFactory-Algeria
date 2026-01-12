#!/usr/bin/env python3
"""
Script de mise à niveau complète de la landing page IAFactory Algeria
- Ajoute section 18 AI Agents avant les applications
- Active le toggle Dev/User existant pour filtrer apps/agents
- Supprime tous les numéros de ports des boutons
- Ajoute effet 3D aux cartes
- Harmonise les couleurs avec la landing page
"""

import re
import os

LANDING_PATH = r"d:\IAFactory\rag-dz\apps\landing\index.html"
BACKUP_PATH = r"d:\IAFactory\rag-dz\apps\landing\index.html.backup"

# Liste des 18 agents IA avec leurs infos
AI_AGENTS = [
    {"name": "AI Consultant", "emoji": "💼", "port": "9101", "desc": "Expert business consulting avec Google Gemini AI", "category": "business", "audience": "user"},
    {"name": "Customer Support", "emoji": "🎧", "port": "9102", "desc": "Support client intelligent 24/7", "category": "business", "audience": "user"},
    {"name": "Data Analysis", "emoji": "📊", "port": "9103", "desc": "Analyse de données avancée avec visualisations", "category": "business", "audience": "dev"},
    {"name": "XAI Finance", "emoji": "💰", "port": "9104", "desc": "Analyse financière avec IA explicable", "category": "finance", "audience": "user"},
    {"name": "Meeting Agent", "emoji": "📅", "port": "9105", "desc": "Assistant de réunions avec transcription", "category": "business", "audience": "user"},
    {"name": "Journalist", "emoji": "📰", "port": "9106", "desc": "Rédaction d'articles professionnels", "category": "business", "audience": "user"},
    {"name": "Web Scraping", "emoji": "🕷️", "port": "9107", "desc": "Extraction intelligente de données web", "category": "developer", "audience": "dev"},
    {"name": "Product Launch", "emoji": "🚀", "port": "9108", "desc": "Planification de lancements produits", "category": "business", "audience": "user"},
    {"name": "Local RAG", "emoji": "📚", "port": "9109", "desc": "RAG local avec Ollama et Qdrant", "category": "ia", "audience": "dev"},
    {"name": "RAG as a Service", "emoji": "☁️", "port": "9110", "desc": "RAG service cloud multi-modèles", "category": "ia", "audience": "dev"},
    {"name": "Agentic RAG", "emoji": "🤖", "port": "9111", "desc": "RAG avec agents autonomes", "category": "ia", "audience": "dev"},
    {"name": "Autonomous RAG", "emoji": "🧠", "port": "9112", "desc": "RAG autonome auto-optimisé", "category": "ia", "audience": "dev"},
    {"name": "Hybrid Search RAG", "emoji": "🔍", "port": "9113", "desc": "RAG avec recherche hybride", "category": "ia", "audience": "dev"},
    {"name": "Investment Agent", "emoji": "💼", "port": "9114", "desc": "Conseil en investissement intelligent", "category": "finance", "audience": "user"},
    {"name": "Financial Coach", "emoji": "💳", "port": "9115", "desc": "Coach financier personnel IA", "category": "finance", "audience": "user"},
    {"name": "Startup Trends", "emoji": "📈", "port": "9116", "desc": "Analyse tendances startups", "category": "finance", "audience": "user"},
    {"name": "System Architect", "emoji": "🏗️", "port": "9117", "desc": "Architecture système avec DeepSeek R1", "category": "developer", "audience": "dev"},
    {"name": "Deep Research", "emoji": "🔬", "port": "9118", "desc": "Recherche approfondie multi-sources", "category": "business", "audience": "dev"},
]

def create_agents_section():
    """Crée la section HTML des 18 agents IA"""
    agents_cards = []

    for agent in AI_AGENTS:
        card = f'''                <article class="agent-card" data-category="{agent['category']}" data-audience="{agent['audience']}">
                    <h5>{agent['emoji']} {agent['name']}</h5>
                    <div class="badge">{agent['category'].capitalize()}</div>
                    <p>{agent['desc']}</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/{agent['port']}', '_blank')">Ouvrir</button>
                </article>'''
        agents_cards.append(card)

    section = f'''
        <!-- AI AGENTS SECTION -->
        <section id="agents" class="section">
            <h2 class="section-title">🤖 18 AI Agents - Production Ready</h2>
            <p class="section-description">Agents IA autonomes et spécialisés pour automatiser vos tâches business, développement et analyses.</p>

            <div class="agents-grid">
{chr(10).join(agents_cards)}
            </div>
        </section>
'''
    return section

def add_3d_effect_css():
    """Ajoute le CSS pour l'effet 3D aux cartes"""
    return """
        /* ========== EFFET 3D CARTES ========== */
        .app-card, .agent-card {
            transform-style: preserve-3d;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .app-card:hover, .agent-card:hover {
            transform: translateY(-12px) rotateX(5deg) scale(1.02);
            box-shadow:
                0 25px 50px -12px rgba(0, 166, 81, 0.25),
                0 0 0 1px rgba(0, 166, 81, 0.1),
                inset 0 1px 0 0 rgba(255, 255, 255, 0.05);
        }

        [data-theme="light"] .app-card:hover,
        [data-theme="light"] .agent-card:hover {
            box-shadow:
                0 25px 50px -12px rgba(0, 166, 81, 0.15),
                0 0 0 1px rgba(0, 166, 81, 0.1),
                inset 0 1px 0 0 rgba(255, 255, 255, 0.8);
        }

        .agents-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 24px;
            margin-top: 32px;
        }

        .agent-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            position: relative;
            overflow: hidden;
        }

        .agent-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), #00d66a);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .agent-card:hover::before {
            opacity: 1;
        }
"""

def add_toggle_functionality_js():
    """Ajoute le JavaScript pour le toggle Dev/User"""
    return """
        // ========== TOGGLE DEV/USER FUNCTIONALITY ==========
        const profileButtons = document.querySelectorAll('.profile-btn');
        let currentAudience = 'user'; // Par défaut: mode utilisateur

        profileButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                // Retirer active de tous les boutons
                profileButtons.forEach(b => b.classList.remove('active'));

                // Activer le bouton cliqué
                this.classList.add('active');

                // Déterminer l'audience
                if (this.textContent.toLowerCase().includes('dev')) {
                    currentAudience = 'dev';
                } else {
                    currentAudience = 'user';
                }

                // Filtrer les cartes
                filterByAudience(currentAudience);
            });
        });

        function filterByAudience(audience) {
            const allCards = document.querySelectorAll('[data-audience]');

            allCards.forEach(card => {
                const cardAudience = card.getAttribute('data-audience');

                if (cardAudience === audience || cardAudience === 'both') {
                    card.style.display = '';
                    // Animation d'apparition
                    card.style.animation = 'fadeInUp 0.4s ease forwards';
                } else {
                    card.style.display = 'none';
                }
            });
        }

        // Animation CSS
        const styleSheet = document.createElement('style');
        styleSheet.textContent = `
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        `;
        document.head.appendChild(styleSheet);

        // Initialiser le filtre au chargement
        filterByAudience(currentAudience);
"""

def remove_port_numbers(html_content):
    """Supprime tous les numéros de ports des boutons"""
    # Pattern: :8XXX ou :9XXX dans les boutons
    html_content = re.sub(r'(Ouvrir|Open)\s*:\d{4,5}', r'\1', html_content)
    return html_content

def harmonize_colors_in_agents():
    """Retourne le CSS pour harmoniser les couleurs des agents avec la landing page"""
    return """
        /* ========== HARMONISATION COULEURS AGENTS ========== */
        /* À injecter dans chaque agent Streamlit */
        :root {
            --bg: #020617;
            --card: #020617;
            --border: rgba(255, 255, 255, 0.12);
            --primary: #00a651;
            --primary-dark: #008c45;
            --text: #f8fafc;
            --muted: rgba(248, 250, 252, 0.75);
            --shadow: 0 20px 60px rgba(0, 0, 0, 0.55);
        }

        [data-theme="light"] {
            --bg: #f7f5f0;
            --card: #f7f5f0;
            --border: rgba(0, 0, 0, 0.08);
            --text: #0f172a;
            --muted: rgba(15, 23, 42, 0.7);
            --shadow: 0 20px 60px rgba(15, 23, 42, 0.25);
        }

        /* Streamlit overrides */
        .stApp {
            background-color: var(--bg) !important;
            color: var(--text) !important;
        }

        .stButton > button {
            background-color: var(--primary) !important;
            color: #021014 !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(0, 166, 81, 0.3) !important;
        }
"""

def main():
    print("=" * 70)
    print("MISE À NIVEAU LANDING PAGE - IAFactory Algeria")
    print("=" * 70)
    print()

    # 1. Backup du fichier original
    print("[1/8] Création du backup...")
    if os.path.exists(LANDING_PATH):
        with open(LANDING_PATH, 'r', encoding='utf-8') as f:
            original_content = f.read()

        with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"    [OK] Backup cree: {BACKUP_PATH}")
    else:
        print(f"    ❌ Fichier non trouvé: {LANDING_PATH}")
        return

    # 2. Ajouter la section des agents
    print("[2/8] Ajout de la section '18 AI Agents'...")
    agents_section = create_agents_section()

    # Insérer AVANT la section <!-- APPS -->
    content = original_content.replace(
        '        <!-- APPS -->',
        agents_section + '        <!-- APPS -->'
    )
    print("    ✅ Section agents ajoutée")

    # 3. Supprimer les numéros de ports
    print("[3/8] Suppression des numéros de ports...")
    content = remove_port_numbers(content)
    print("    ✅ Ports supprimés")

    # 4. Ajouter l'effet 3D CSS
    print("[4/8] Ajout de l'effet 3D aux cartes...")
    css_3d = add_3d_effect_css()

    # Insérer avant la fermeture de </style>
    content = content.replace('    </style>', css_3d + '    </style>')
    print("    ✅ Effet 3D ajouté")

    # 5. Ajouter le JavaScript pour le toggle
    print("[5/8] Activation du toggle Dev/User...")
    js_toggle = add_toggle_functionality_js()

    # Insérer avant la fermeture de </script> principal
    content = content.replace('    </script>\n</body>', js_toggle + '\n    </script>\n</body>')
    print("    ✅ Toggle Dev/User activé")

    # 6. Sauvegarder le fichier modifié
    print("[6/8] Sauvegarde des modifications...")
    with open(LANDING_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print("    ✅ Fichier sauvegardé")

    # 7. Créer le CSS d'harmonisation pour les agents
    print("[7/8] Création du CSS d'harmonisation des agents...")
    colors_css = harmonize_colors_in_agents()

    colors_file = r"d:\IAFactory\rag-dz\shared\agent-colors-harmonization.css"
    with open(colors_file, 'w', encoding='utf-8') as f:
        f.write(colors_css)
    print(f"    ✅ CSS créé: {colors_file}")

    # 8. Résumé
    print("[8/8] Résumé des modifications")
    print("=" * 70)
    print("✅ Section '18 AI Agents' ajoutée AVANT les applications")
    print("✅ Toggle Dev/User activé dans le header")
    print("✅ Tous les ports supprimés des boutons")
    print("✅ Effet 3D ajouté aux cartes")
    print("✅ CSS d'harmonisation créé pour les agents")
    print()
    print("📋 PROCHAINES ÉTAPES:")
    print("   1. Vérifier la page: file:///d:/IAFactory/rag-dz/apps/landing/index.html")
    print("   2. Tester le toggle Dev/User")
    print("   3. Appliquer le CSS d'harmonisation à chaque agent Streamlit")
    print("   4. Vérifier le chatbot help dans chaque agent")
    print("   5. Tester la connexion back-front")
    print()
    print("🔄 Pour restaurer la version originale:")
    print(f"   copy {BACKUP_PATH} {LANDING_PATH}")
    print("=" * 70)

if __name__ == "__main__":
    main()
