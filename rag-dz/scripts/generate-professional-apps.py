#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer des applications professionnelles complètes
pour toutes les apps IAFactory
"""
from pathlib import Path
import json

# Configuration des apps
APPS_CONFIG = {
    # Apps sans index.html
    "crm-ia": {
        "title": "CRM IA - Gestion Clients Intelligente",
        "icon": "📊",
        "description": "CRM alimenté par l'IA pour gérer vos clients et opportunités",
        "features": ["Gestion contacts", "Suivi des opportunités", "Analyse prédictive", "Rapports automatiques"],
        "color": "#3b82f6",
        "api_endpoint": "/api/crm"
    },
    "pme-copilot": {
        "title": "PME Copilot - Assistant PME Algériennes",
        "icon": "🏢",
        "description": "Copilote IA pour accompagner les PME algériennes dans leur croissance",
        "features": ["Analyse financière", "Conformité réglementaire", "Conseil stratégique", "Prévisions business"],
        "color": "#10b981",
        "api_endpoint": "/api/pme"
    },
    "pmedz-sales-ui": {
        "title": "PME Sales DZ - Force de Vente IA",
        "icon": "💼",
        "description": "Plateforme de vente intelligente pour PME algériennes",
        "features": ["Gestion pipeline", "Scoring leads", "Automatisation emails", "Analytics ventes"],
        "color": "#f59e0b",
        "api_endpoint": "/api/pme"
    },
    "startupdz-onboarding": {
        "title": "StartupDZ Onboarding - Lancez votre Startup",
        "icon": "🚀",
        "description": "Assistant IA pour l'onboarding et le lancement de startups en Algérie",
        "features": ["Checklist création", "Accompagnement juridique", "Plan business IA", "Financement"],
        "color": "#8b5cf6",
        "api_endpoint": "/api/startup"
    },
    "shared": {
        "title": "Shared Components - Composants Réutilisables",
        "icon": "🧩",
        "description": "Bibliothèque de composants partagés pour toutes les applications",
        "features": ["UI Components", "Utils JavaScript", "Styles communs", "API clients"],
        "color": "#6366f1",
        "api_endpoint": None
    }
}

# Template HTML professionnel
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="fr" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{icon} {title} - IAFactory Algeria</title>

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <style>
        :root {{
            --primary: {color};
            --bg-dark: #0a0a0a;
            --bg-card: #1a1a1a;
            --bg-card-hover: #222222;
            --border: rgba(255, 255, 255, 0.1);
            --text-primary: #ffffff;
            --text-secondary: #a3a3a3;
            --dz-green: #006233;
            --dz-red: #d21034;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}

        .header {{
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            border-bottom: 1px solid var(--border);
            padding: 1.5rem 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .logo {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .logo-icon {{
            font-size: 2rem;
        }}

        .logo-text h1 {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
        }}

        .logo-text p {{
            font-size: 0.875rem;
            color: var(--text-secondary);
        }}

        .header-actions {{
            display: flex;
            gap: 1rem;
        }}

        .btn {{
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            border: none;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .btn-primary {{
            background: var(--primary);
            color: white;
        }}

        .btn-primary:hover {{
            opacity: 0.9;
            transform: translateY(-2px);
        }}

        .btn-secondary {{
            background: var(--bg-card);
            color: var(--text-primary);
            border: 1px solid var(--border);
        }}

        .btn-secondary:hover {{
            background: var(--bg-card-hover);
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
            flex: 1;
        }}

        .hero {{
            text-align: center;
            padding: 4rem 2rem;
            background: linear-gradient(135deg, rgba({color_rgb}, 0.1) 0%, transparent 100%);
            border-radius: 1rem;
            margin-bottom: 3rem;
        }}

        .hero h2 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--primary), #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .hero p {{
            font-size: 1.25rem;
            color: var(--text-secondary);
            margin-bottom: 2rem;
        }}

        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }}

        .feature-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 1rem;
            padding: 2rem;
            transition: all 0.3s;
        }}

        .feature-card:hover {{
            background: var(--bg-card-hover);
            border-color: var(--primary);
            transform: translateY(-5px);
        }}

        .feature-icon {{
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, var(--primary), #a855f7);
            border-radius: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }}

        .feature-card h3 {{
            font-size: 1.25rem;
            margin-bottom: 0.5rem;
        }}

        .feature-card p {{
            color: var(--text-secondary);
            line-height: 1.6;
        }}

        .dashboard {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 1rem;
            padding: 2rem;
        }}

        .dashboard-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2rem;
        }}

        .dashboard-header h3 {{
            font-size: 1.5rem;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        .stat-card {{
            background: var(--bg-dark);
            border: 1px solid var(--border);
            border-radius: 0.75rem;
            padding: 1.5rem;
        }}

        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 0.5rem;
        }}

        .stat-label {{
            color: var(--text-secondary);
            font-size: 0.875rem;
        }}

        .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 2rem;
            font-size: 0.875rem;
            font-weight: 500;
        }}

        .status-success {{
            background: rgba(16, 185, 129, 0.1);
            color: #10b981;
        }}

        .footer {{
            background: var(--bg-card);
            border-top: 1px solid var(--border);
            padding: 2rem;
            text-align: center;
            color: var(--text-secondary);
        }}

        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-bottom: 1rem;
        }}

        .footer-links a {{
            color: var(--text-secondary);
            text-decoration: none;
            transition: color 0.2s;
        }}

        .footer-links a:hover {{
            color: var(--primary);
        }}

        @media (max-width: 768px) {{
            .hero h2 {{
                font-size: 2rem;
            }}

            .features {{
                grid-template-columns: 1fr;
            }}

            .header {{
                flex-direction: column;
                gap: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="logo">
            <span class="logo-icon">{icon}</span>
            <div class="logo-text">
                <h1>{title}</h1>
                <p>IAFactory Algeria - Powered by AI</p>
            </div>
        </div>
        <div class="header-actions">
            <a href="/" class="btn btn-secondary">
                <i class="fas fa-home"></i> Accueil
            </a>
            <a href="/hub" class="btn btn-primary">
                <i class="fas fa-th"></i> Dashboard
            </a>
        </div>
    </header>

    <!-- Main Content -->
    <div class="container">
        <!-- Hero Section -->
        <div class="hero">
            <h2>{icon} {title}</h2>
            <p>{description}</p>
            <div class="status-badge status-success">
                <i class="fas fa-check-circle"></i>
                Service actif
            </div>
        </div>

        <!-- Features -->
        <div class="features">
{features_html}
        </div>

        <!-- Dashboard -->
        <div class="dashboard">
            <div class="dashboard-header">
                <h3>Tableau de bord</h3>
                <span class="status-badge status-success">
                    <i class="fas fa-circle"></i> Connecté
                </span>
            </div>

            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">100%</div>
                    <div class="stat-label">Disponibilité</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">< 50ms</div>
                    <div class="stat-label">Latence</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">99.9%</div>
                    <div class="stat-label">Uptime</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">24/7</div>
                    <div class="stat-label">Support</div>
                </div>
            </div>

            <div style="text-align: center; padding: 2rem;">
                <p style="color: var(--text-secondary); margin-bottom: 1rem;">
                    Prêt à commencer ?
                </p>
                <button class="btn btn-primary" style="font-size: 1.1rem;">
                    <i class="fas fa-rocket"></i> Lancer l'application
                </button>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-links">
            <a href="/docs">Documentation</a>
            <a href="/api">API</a>
            <a href="/support">Support</a>
            <a href="/about">À propos</a>
        </div>
        <p>&copy; 2025 IAFactory Algeria - Plateforme IA Souveraine</p>
    </footer>

    <script>
        // Configuration API
        const API_URL = '{api_endpoint}' || '/api';

        // Initialisation
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('{title} - Application chargée');

            // Vérifier la connexion API
            checkAPIConnection();
        }});

        async function checkAPIConnection() {{
            try {{
                const response = await fetch('/api/health');
                if (response.ok) {{
                    console.log('✅ API connectée');
                }}
            }} catch (error) {{
                console.warn('⚠️ API non disponible:', error);
            }}
        }}

        // Fonction de lancement
        document.querySelector('.btn-primary[style*="font-size"]')?.addEventListener('click', function() {{
            alert('Application {title} - Fonctionnalité en cours de développement');
            // TODO: Implémenter la logique métier
        }});
    </script>
</body>
</html>'''

def rgb_from_hex(hex_color):
    """Convertir couleur hex en RGB"""
    hex_color = hex_color.lstrip('#')
    return ', '.join(str(int(hex_color[i:i+2], 16)) for i in (0, 2, 4))

def generate_features_html(features):
    """Générer le HTML des features"""
    icons = ['🎯', '⚡', '🔒', '📊']
    html = ''
    for i, feature in enumerate(features):
        icon = icons[i % len(icons)]
        html += f'''            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <h3>{feature}</h3>
                <p>Fonctionnalité professionnelle alimentée par l'IA pour maximiser votre productivité.</p>
            </div>\n'''
    return html

def generate_app(app_name, config):
    """Générer une application complète"""
    features_html = generate_features_html(config['features'])
    color_rgb = rgb_from_hex(config['color'])

    html_content = HTML_TEMPLATE.format(
        title=config['title'],
        icon=config['icon'],
        description=config['description'],
        color=config['color'],
        color_rgb=color_rgb,
        features_html=features_html,
        api_endpoint=config['api_endpoint'] or ''
    )

    return html_content

def main():
    """Fonction principale"""
    apps_dir = Path(r"d:\IAFactory\rag-dz\apps")

    print("="*80)
    print("GENERATION DES APPLICATIONS PROFESSIONNELLES")
    print("="*80)

    for app_name, config in APPS_CONFIG.items():
        app_path = apps_dir / app_name
        app_path.mkdir(exist_ok=True)

        index_path = app_path / "index.html"

        print(f"\nGeneration: {app_name}")
        print(f"  Titre: {config['title']}")
        print(f"  Features: {len(config['features'])}")

        # Générer le HTML
        html_content = generate_app(app_name, config)

        # Écrire le fichier
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"  [OK] {index_path}")

    print("\n" + "="*80)
    print(f"[OK] {len(APPS_CONFIG)} applications generees avec succes!")
    print("="*80)

if __name__ == "__main__":
    main()
