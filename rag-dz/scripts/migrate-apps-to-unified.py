#!/usr/bin/env python3
"""
IAFactory - Migration Script: Unified Components
Migre toutes les apps vers les composants unifiés (header, footer, chatbot)
Supprime le code dupliqué et les clés API exposées
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

# Configuration
APPS_DIR = Path(__file__).parent.parent / "apps"
EXCLUDE_DIRS = {"shared", "landing", "landing-pro", "marketing"}
BACKUP_SUFFIX = ".backup"

# Template pour les apps migrées
APP_TEMPLATE = '''<!DOCTYPE html>
<html lang="fr" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{icon} {title} - IAFactory Algeria</title>

    <!-- IAFactory Unified Components -->
    <link rel="stylesheet" href="/apps/shared/iafactory-unified.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <style>
        /* App-specific styles */
        body {{
            padding-top: var(--iaf-header-height);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            font-family: var(--iaf-font-primary);
            background: var(--iaf-bg);
            color: var(--iaf-text);
            margin: 0;
        }}

        .container {{
            max-width: var(--iaf-container-max);
            margin: 0 auto;
            padding: 2rem;
            flex: 1;
        }}

        .hero {{
            text-align: center;
            padding: 4rem 2rem;
            background: linear-gradient(135deg, rgba(0, 166, 81, 0.1) 0%, transparent 100%);
            border-radius: 1rem;
            margin-bottom: 3rem;
        }}

        .hero h2 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--iaf-primary), #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .hero p {{
            font-size: 1.25rem;
            color: var(--iaf-text-secondary);
            margin-bottom: 2rem;
        }}

        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }}

        .feature-card {{
            background: var(--iaf-bg-card);
            border: 1px solid var(--iaf-border);
            border-radius: 1rem;
            padding: 2rem;
            transition: all 0.3s;
        }}

        .feature-card:hover {{
            border-color: var(--iaf-primary);
            transform: translateY(-5px);
        }}

        .feature-icon {{
            width: 60px;
            height: 60px;
            background: var(--iaf-gradient);
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
            color: var(--iaf-text-primary);
        }}

        .feature-card p {{
            color: var(--iaf-text-secondary);
            line-height: 1.6;
        }}

        .dashboard {{
            background: var(--iaf-bg-card);
            border: 1px solid var(--iaf-border);
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
            color: var(--iaf-text-primary);
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        .stat-card {{
            background: var(--iaf-bg);
            border: 1px solid var(--iaf-border);
            border-radius: 0.75rem;
            padding: 1.5rem;
        }}

        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--iaf-primary);
            margin-bottom: 0.5rem;
        }}

        .stat-label {{
            color: var(--iaf-text-secondary);
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
            background: rgba(0, 166, 81, 0.1);
            color: var(--iaf-primary);
        }}

        .btn {{
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            border: none;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .btn-primary {{
            background: var(--iaf-gradient);
            color: white;
            box-shadow: 0 4px 12px rgba(0, 166, 81, 0.3);
        }}

        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 166, 81, 0.4);
        }}

        @media (max-width: 768px) {{
            .hero h2 {{ font-size: 1.75rem; }}
            .features {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body data-iaf-auto-init>
    <!-- Header (auto-injected) -->
    <div id="iaf-header" data-iaf-header></div>

    <!-- Main Content -->
    <div class="container">
        <!-- Hero Section -->
        <div class="hero">
            <h2>{icon} {title}</h2>
            <p>{description}</p>
            <div class="status-badge">
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
                <span class="status-badge">
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
                <p style="color: var(--iaf-text-secondary); margin-bottom: 1rem;">
                    Prêt à commencer ?
                </p>
                <button class="btn btn-primary" id="launchBtn">
                    <i class="fas fa-rocket"></i> Lancer l'application
                </button>
            </div>
        </div>
    </div>

    <!-- Footer (auto-injected) -->
    <div id="iaf-footer" data-iaf-footer></div>

    <!-- IAFactory Unified JS -->
    <script src="/apps/shared/iafactory-unified.js"></script>

    <script>
        // Configuration API
        const API_URL = '{api_endpoint}';

        // Initialisation
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('{title} - Application chargée');
            checkAPIConnection();
        }});

        async function checkAPIConnection() {{
            try {{
                const response = await fetch('/api/health');
                if (response.ok) console.log('✅ API connectée');
            }} catch (error) {{
                console.warn('⚠️ API non disponible:', error);
            }}
        }}

        // Lancement
        document.getElementById('launchBtn')?.addEventListener('click', function() {{
            alert('{title} - Fonctionnalité en cours de développement');
        }});
    </script>
</body>
</html>
'''

def extract_app_info(html_content: str) -> dict:
    """Extrait les informations de l'app depuis le HTML existant"""
    info = {
        "title": "Application",
        "description": "Application IAFactory Algeria",
        "icon": "🚀",
        "features": [],
        "api_endpoint": "/api"
    }

    # Extraire le titre
    title_match = re.search(r'<title>([^<]+)</title>', html_content)
    if title_match:
        full_title = title_match.group(1)
        # Extraire l'emoji et le titre
        emoji_match = re.search(r'^([^\w\s]+)\s*', full_title)
        if emoji_match:
            info["icon"] = emoji_match.group(1).strip()
            full_title = full_title[len(emoji_match.group(0)):]

        # Nettoyer le titre
        info["title"] = re.sub(r'\s*-\s*IAFactory.*$', '', full_title).strip()

    # Extraire la description
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html_content)
    if desc_match:
        info["description"] = desc_match.group(1)

    # Extraire les features
    feature_pattern = r'<div class="feature-card">\s*<div class="feature-icon">([^<]+)</div>\s*<h3>([^<]+)</h3>\s*<p>([^<]+)</p>'
    features = re.findall(feature_pattern, html_content)
    for icon, title, desc in features:
        info["features"].append({
            "icon": icon.strip(),
            "title": title.strip(),
            "desc": desc.strip()
        })

    # Extraire l'endpoint API
    api_match = re.search(r"const API_URL = '([^']+)'", html_content)
    if api_match:
        info["api_endpoint"] = api_match.group(1)

    return info


def generate_features_html(features: List[dict]) -> str:
    """Génère le HTML des features"""
    if not features:
        features = [
            {"icon": "🎯", "title": "Fonctionnalité 1", "desc": "Description de la fonctionnalité."},
            {"icon": "⚡", "title": "Fonctionnalité 2", "desc": "Description de la fonctionnalité."},
            {"icon": "🔒", "title": "Fonctionnalité 3", "desc": "Description de la fonctionnalité."},
            {"icon": "📊", "title": "Fonctionnalité 4", "desc": "Description de la fonctionnalité."},
        ]

    html_parts = []
    for f in features:
        html_parts.append(f'''            <div class="feature-card">
                <div class="feature-icon">{f["icon"]}</div>
                <h3>{f["title"]}</h3>
                <p>{f["desc"]}</p>
            </div>''')

    return "\n".join(html_parts)


def migrate_app(app_dir: Path, dry_run: bool = False) -> Tuple[bool, str]:
    """Migre une app vers les composants unifiés"""
    index_file = app_dir / "index.html"

    if not index_file.exists():
        return False, f"Pas de index.html dans {app_dir.name}"

    # Lire le contenu actuel
    try:
        content = index_file.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Erreur lecture {app_dir.name}: {e}"

    # Vérifier si déjà migré
    if "iafactory-unified.css" in content:
        return False, f"{app_dir.name} déjà migré"

    # Extraire les infos
    info = extract_app_info(content)
    features_html = generate_features_html(info["features"])

    # Générer le nouveau HTML
    new_content = APP_TEMPLATE.format(
        icon=info["icon"],
        title=info["title"],
        description=info["description"],
        features_html=features_html,
        api_endpoint=info["api_endpoint"]
    )

    if dry_run:
        return True, f"[DRY RUN] {app_dir.name} serait migré"

    # Backup
    backup_file = index_file.with_suffix(index_file.suffix + BACKUP_SUFFIX)
    try:
        backup_file.write_text(content, encoding="utf-8")
    except Exception as e:
        return False, f"Erreur backup {app_dir.name}: {e}"

    # Écrire le nouveau fichier
    try:
        index_file.write_text(new_content, encoding="utf-8")
    except Exception as e:
        return False, f"Erreur écriture {app_dir.name}: {e}"

    return True, f"✅ {app_dir.name} migré avec succès"


def find_apps_to_migrate() -> List[Path]:
    """Trouve toutes les apps à migrer"""
    apps = []

    if not APPS_DIR.exists():
        print(f"❌ Répertoire apps non trouvé: {APPS_DIR}")
        return apps

    for item in APPS_DIR.iterdir():
        if item.is_dir() and item.name not in EXCLUDE_DIRS:
            index_file = item / "index.html"
            if index_file.exists():
                apps.append(item)

    return sorted(apps, key=lambda x: x.name)


def main():
    import argparse
    import sys

    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(description="Migre les apps vers les composants unifies")
    parser.add_argument("--dry-run", action="store_true", help="Affiche les changements sans les appliquer")
    parser.add_argument("--app", type=str, help="Migrer une app specifique")
    parser.add_argument("--list", action="store_true", help="Lister les apps a migrer")
    args = parser.parse_args()

    print("=" * 60)
    print("IAFactory - Migration vers Composants Unifies")
    print("=" * 60)

    apps = find_apps_to_migrate()

    if args.list:
        print(f"\n[DIR] {len(apps)} apps a migrer:")
        for app in apps:
            print(f"  - {app.name}")
        return

    if args.app:
        app_path = APPS_DIR / args.app
        if not app_path.exists():
            print(f"❌ App non trouvée: {args.app}")
            return
        apps = [app_path]

    print(f"\n🔄 Migration de {len(apps)} apps...")
    if args.dry_run:
        print("⚠️  Mode DRY RUN - aucune modification ne sera effectuée\n")

    success_count = 0
    skip_count = 0
    error_count = 0

    for app in apps:
        success, message = migrate_app(app, dry_run=args.dry_run)
        print(message)

        if success:
            success_count += 1
        elif "déjà migré" in message:
            skip_count += 1
        else:
            error_count += 1

    print("\n" + "=" * 60)
    print(f"✅ Succès: {success_count}")
    print(f"⏭️  Ignorés: {skip_count}")
    print(f"❌ Erreurs: {error_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
