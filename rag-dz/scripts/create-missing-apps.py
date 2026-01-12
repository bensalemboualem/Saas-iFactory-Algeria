#!/usr/bin/env python3
"""
Script pour créer toutes les apps manquantes avec le template unifié
"""

import os
import shutil

# Liste des apps à créer
APPS_TO_CREATE = [
    {
        'name': 'Business DZ',
        'folder': 'business-dz',
        'description': 'Assistant IA expert en fiscalité, juridique et réglementations administratives algériennes'
    },
    {
        'name': 'SEO DZ Boost',
        'folder': 'seo-dz',
        'description': 'SEO optimisé pour le marché algérien avec mots-clés locaux'
    },
    {
        'name': 'StartupDZ Onboarding',
        'folder': 'startup-dz',
        'description': 'Accompagnement inscription CNRC, business plan et formalités'
    },
    {
        'name': 'Voice Assistant',
        'folder': 'voice-assistant',
        'description': 'Assistant vocal multilingue FR/AR pour commander IAFactory'
    },
    {
        'name': 'Shared Components',
        'folder': 'shared-components',
        'description': 'Bibliothèque de composants réutilisables pour toutes les apps'
    },
    {
        'name': 'MedDZ Assistant',
        'folder': 'med-dz',
        'description': 'Assistant IA pour cliniques et cabinets médicaux algériens'
    },
]

BASE_DIR = 'D:/IAFactory/rag-dz'
APPS_DIR = os.path.join(BASE_DIR, 'apps')
TEMPLATE_FILE = os.path.join(BASE_DIR, 'shared', 'app-template.html')

def create_app(app_info):
    """Créer une nouvelle app à partir du template"""
    app_folder = os.path.join(APPS_DIR, app_info['folder'])

    # Créer le dossier si nécessaire
    os.makedirs(app_folder, exist_ok=True)

    # Lire le template
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template = f.read()

    # Remplacer les placeholders
    content = template.replace('{{APP_NAME}}', app_info['name'])
    content = content.replace('{{APP_DESCRIPTION}}', app_info['description'])

    # Écrire le fichier index.html
    index_path = os.path.join(app_folder, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Created: {app_info['name']} -> {index_path}")

    # Créer un README
    readme_content = f"""# {app_info['name']}

{app_info['description']}

## 🚀 Lancement

Ouvrez simplement `index.html` dans votre navigateur.

## 🎨 Thème

L'app utilise automatiquement le thème global IAFactory Algeria avec support dark/light mode.

## 🔗 Retour

Bouton "Retour" pour revenir à la landing page principale.
"""

    readme_path = os.path.join(app_folder, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

def main():
    print("Creation des apps manquantes...\n")

    for app in APPS_TO_CREATE:
        create_app(app)

    print(f"\n{len(APPS_TO_CREATE)} apps creees avec succes!")
    print("\nToutes les apps utilisent:")
    print("   - shared/theme.css (couleurs unifiees)")
    print("   - shared/theme.js (dark/light mode)")
    print("   - Couleurs algeriennes")

if __name__ == '__main__':
    main()
