#!/usr/bin/env python3
"""
Script pour connecter toutes les apps à la landing page
et créer les apps manquantes avec la palette unifiée
"""

import os
import re

# Mapping des noms d'apps vers leurs chemins
APP_PATHS = {
    'Business DZ': 'apps/business-dz/index.html',
    'RAG École': 'frontend/rag-ui/index.html',
    'RAG Islam': 'frontend/rag-ui/index.html?mode=islam',
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

def add_link_to_app_card(card_html, app_name):
    """Ajoute un lien cliquable à une app card"""
    if app_name not in APP_PATHS:
        print(f"⚠️  App '{app_name}' not in path mapping")
        return card_html

    path = APP_PATHS[app_name]

    # Ajouter onclick et cursor
    if 'onclick=' not in card_html:
        card_html = card_html.replace(
            '<article class="app-card">',
            f'<article class="app-card" onclick="window.location.href=\'{path}\'" style="cursor: pointer;">'
        )

    return card_html

def main():
    landing_page = 'D:/IAFactory/rag-dz/landing-page.html'

    with open(landing_page, 'r', encoding='utf-8') as f:
        content = f.read()

    # Trouver toutes les app cards
    pattern = r'(<article class="app-card".*?</article>)'
    cards = re.findall(pattern, content, re.DOTALL)

    print(f"📊 Found {len(cards)} app cards")

    # Traiter chaque card
    for card in cards:
        # Extraire le titre
        title_match = re.search(r'<h3 class="app-title">(.*?)</h3>', card)
        if title_match:
            app_name = title_match.group(1)
            updated_card = add_link_to_app_card(card, app_name)
            content = content.replace(card, updated_card)
            print(f"✅ Added link for '{app_name}'")

    # Sauvegarder
    with open(landing_page, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Updated {landing_page}")

if __name__ == '__main__':
    main()
