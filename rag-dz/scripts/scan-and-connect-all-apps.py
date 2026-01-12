#!/usr/bin/env python3
"""
Script pour scanner toutes les apps, vérifier leur état
et les connecter à la landing page
"""

import os
import re
from pathlib import Path

BASE_DIR = Path('D:/IAFactory/rag-dz')

# Toutes les apps connues avec leurs chemins
ALL_APPS = {
    'Business DZ': 'apps/business-dz/index.html',
    'RAG École': 'frontend/rag-ui/index.html',
    'RAG Islam': 'frontend/rag-ui/index.html',
    'PME Copilot': 'apps/pme-copilot-ui/index.html',
    'PMEDZ Sales': 'apps/pmedz-sales/index.html',
    'CRM IA': 'apps/crm-ia-ui/index.html',
    'Fiscal Assistant': 'apps/fiscal-assistant/index.html',
    'Legal Assistant': 'apps/legal-assistant/index.html',
    'Billing Panel': 'apps/billing-panel/index.html',
    'SEO DZ Boost': 'apps/seo-dz/index.html',
    'BMAD': 'apps/bmad/index.html',
    'API Portal': 'apps/api-portal/frontend/index.html',
    'Developer Portal': 'apps/dev-portal/index.html',
    'Data DZ': 'apps/data-dz/index.html',
    'Data DZ Dashboard': 'apps/data-dz-dashboard/index.html',
    'Creative Studio': 'apps/creative-studio/index.html',
    'StartupDZ Onboarding': 'apps/startup-dz/index.html',
    'Ithy': 'apps/ithy/index.html',
    'Dashboard Central': 'apps/dashboard/index.html',
    'Archon Hub': 'frontend/archon-ui/index.html',
    'RAG UI': 'frontend/rag-ui/index.html',
    'Voice Assistant': 'apps/voice-assistant/index.html',
    'Landing Home': 'apps/landing/index.html',
    'Landing Pro': 'apps/landing-pro/index.html',
    'Shared Components': 'apps/shared-components/index.html',
    'MedDZ Assistant': 'apps/med-dz/index.html',
}

def check_file_exists(filepath):
    """Vérifie si un fichier existe"""
    full_path = BASE_DIR / filepath
    return full_path.exists()

def check_has_theme_css(filepath):
    """Vérifie si l'app charge shared/theme.css"""
    full_path = BASE_DIR / filepath
    if not full_path.exists():
        return False

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return 'shared/theme.css' in content
    except:
        return False

def check_has_back_button(filepath):
    """Vérifie si l'app a un bouton retour vers landing"""
    full_path = BASE_DIR / filepath
    if not full_path.exists():
        return False

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return 'landing-page.html' in content or 'Retour' in content
    except:
        return False

def scan_all_apps():
    """Scan toutes les apps et génère un rapport"""
    print("=" * 70)
    print("SCAN DE TOUTES LES APPS - IAFactory Algeria")
    print("=" * 70)
    print()

    total = len(ALL_APPS)
    exists = 0
    has_theme = 0
    has_back = 0
    missing = []

    for app_name, app_path in ALL_APPS.items():
        print(f"\n{app_name}")
        print("-" * 50)

        file_exists = check_file_exists(app_path)
        theme_css = check_has_theme_css(app_path) if file_exists else False
        back_btn = check_has_back_button(app_path) if file_exists else False

        if file_exists:
            exists += 1
            print(f"  [OK] Fichier existe: {app_path}")
        else:
            print(f"  [MANQUANT] Fichier: {app_path}")
            missing.append((app_name, app_path))

        if theme_css:
            has_theme += 1
            print(f"  [OK] Theme CSS integre")
        else:
            print(f"  [A FAIRE] Ajouter shared/theme.css")

        if back_btn:
            has_back += 1
            print(f"  [OK] Bouton retour present")
        else:
            print(f"  [A FAIRE] Ajouter bouton retour")

    # Rapport final
    print("\n" + "=" * 70)
    print("RAPPORT FINAL")
    print("=" * 70)
    print(f"Total apps: {total}")
    print(f"Apps existantes: {exists}/{total} ({exists*100//total}%)")
    print(f"Apps avec theme CSS: {has_theme}/{total} ({has_theme*100//total}%)")
    print(f"Apps avec bouton retour: {has_back}/{total} ({has_back*100//total}%)")

    if missing:
        print(f"\n\nAPPS MANQUANTES ({len(missing)}):")
        for name, path in missing:
            print(f"  - {name}: {path}")

    print("\n" + "=" * 70)

def update_landing_page_links():
    """Met à jour landing-page.html avec tous les liens"""
    landing_page = BASE_DIR / 'landing-page.html'

    print("\n\nMise a jour des liens dans landing-page.html...")

    with open(landing_page, 'r', encoding='utf-8') as f:
        content = f.read()

    updated = 0
    for app_name, app_path in ALL_APPS.items():
        # Chercher la app card
        pattern = f'<h3 class="app-title">{re.escape(app_name)}</h3>'
        if pattern in content:
            # Vérifier si elle a déjà un onclick
            card_pattern = f'(<article class="app-card"[^>]*>.*?<h3 class="app-title">{re.escape(app_name)}</h3>)'
            match = re.search(card_pattern, content, re.DOTALL)

            if match and 'onclick=' not in match.group(1):
                # Ajouter onclick et cursor
                old_tag = '<article class="app-card"'
                new_tag = f'<article class="app-card" onclick="window.location.href=\'{app_path}\'" style="cursor: pointer;"'

                # Remplacer seulement pour cette card
                start = match.start()
                end = match.end()
                before = content[:start]
                card = content[start:end]
                after = content[end:]

                card = card.replace(old_tag, new_tag, 1)
                content = before + card + after
                updated += 1
                print(f"  [OK] Lien ajoute: {app_name}")

    # Sauvegarder
    with open(landing_page, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n{updated} liens ajoutes/mis a jour dans landing-page.html")

if __name__ == '__main__':
    scan_all_apps()
    update_landing_page_links()
