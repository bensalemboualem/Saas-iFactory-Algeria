#!/usr/bin/env python3
"""
Script pour intégrer automatiquement:
1. Le theme CSS unifié (shared/theme.css)
2. Le theme JS (shared/theme.js)
3. Un bouton retour vers landing-page.html
Dans toutes les apps qui ne les ont pas encore
"""

import os
import re
from pathlib import Path

BASE_DIR = Path('D:/IAFactory/rag-dz')

# Apps à traiter
APPS_TO_FIX = [
    'frontend/rag-ui/index.html',
    'apps/pme-copilot-ui/index.html',
    'apps/pmedz-sales/index.html',
    'apps/crm-ia-ui/index.html',
    'apps/fiscal-assistant/index.html',
    'apps/legal-assistant/index.html',
    'apps/billing-panel/index.html',
    'apps/bmad/index.html',
    'apps/api-portal/frontend/index.html',
    'apps/dev-portal/index.html',
    'apps/data-dz/index.html',
    'apps/data-dz-dashboard/index.html',
    'apps/creative-studio/index.html',
    'apps/startup-dz/index.html',
    'apps/ithy/index.html',
    'apps/dashboard/index.html',
    'frontend/archon-ui/index.html',
    'apps/landing/index.html',
    'apps/landing-pro/index.html',
]

def calculate_relative_path(app_path):
    """Calcule le chemin relatif vers shared/ depuis l'app"""
    depth = app_path.count('/')
    if 'frontend/' in app_path:
        return '../shared/'
    elif 'api-portal/frontend' in app_path:
        return '../../../shared/'
    else:
        return '../../shared/'

def integrate_theme(app_path):
    """Intègre le theme dans une app"""
    full_path = BASE_DIR / app_path
    if not full_path.exists():
        print(f"  [SKIP] Fichier n'existe pas: {app_path}")
        return False

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        print(f"  [ERROR] Impossible de lire: {app_path}")
        return False

    modified = False
    relative_path = calculate_relative_path(app_path)

    # 1. Ajouter theme.css dans <head> si absent
    if 'shared/theme.css' not in content:
        # Trouver </head>
        if '</head>' in content:
            theme_link = f'\n  <!-- Theme CSS Global -->\n  <link rel="stylesheet" href="{relative_path}theme.css">\n'
            content = content.replace('</head>', theme_link + '</head>')
            modified = True
            print(f"  [+] Ajoute theme.css")

    # 2. Ajouter theme.js avant </body> si absent
    if 'shared/theme.js' not in content:
        if '</body>' in content:
            theme_script = f'\n  <!-- Theme Manager -->\n  <script src="{relative_path}theme.js"></script>\n'
            content = content.replace('</body>', theme_script + '</body>')
            modified = True
            print(f"  [+] Ajoute theme.js")

    # 3. Ajouter bouton retour si absent
    if 'landing-page.html' not in content and 'Retour' not in content:
        # Ajouter un bouton retour basique dans le header ou en haut du body
        if '<body>' in content:
            # Calculer le chemin de retour
            if 'frontend/' in app_path:
                back_path = '../landing-page.html'
            elif 'api-portal/frontend' in app_path:
                back_path = '../../../landing-page.html'
            else:
                back_path = '../../landing-page.html'

            back_button = f'''
  <!-- Back Button -->
  <div style="position: fixed; top: 20px; right: 20px; z-index: 1000;">
    <a href="{back_path}" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: var(--bg-card); border: 1px solid var(--border-primary); border-radius: var(--radius-md); color: var(--text-primary); text-decoration: none; transition: all 0.2s;">
      ← Retour
    </a>
  </div>
'''
            content = content.replace('<body>', '<body>' + back_button)
            modified = True
            print(f"  [+] Ajoute bouton retour")

    # Sauvegarder si modifié
    if modified:
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [OK] Fichier mis a jour")
            return True
        except:
            print(f"  [ERROR] Impossible d'ecrire: {app_path}")
            return False
    else:
        print(f"  [SKIP] Deja a jour")
        return False

def main():
    print("=" * 70)
    print("INTEGRATION DU THEME UNIFIE DANS TOUTES LES APPS")
    print("=" * 70)
    print()

    total = len(APPS_TO_FIX)
    updated = 0

    for app_path in APPS_TO_FIX:
        print(f"\n{app_path}")
        print("-" * 50)
        if integrate_theme(app_path):
            updated += 1

    print("\n" + "=" * 70)
    print("RAPPORT FINAL")
    print("=" * 70)
    print(f"Total apps traitees: {total}")
    print(f"Apps mises a jour: {updated}")
    print(f"Apps deja a jour: {total - updated}")
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
