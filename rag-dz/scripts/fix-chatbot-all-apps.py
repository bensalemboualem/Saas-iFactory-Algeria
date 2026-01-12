#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger le chatbot dans toutes les apps
Remplace l'iframe chatbot-ia par l'URL correcte
"""

import sys
import os
from pathlib import Path

# Apps à corriger (exclure school et archon)
APPS_TO_FIX = [
    'bmad',
    'creative-studio',
    'dzirvideo-ai',
    'prompt-creator',
    'pme-copilot',
    'growth-grid',
    'islam-dz',
    'prof-dz',
    'med-dz'
]

# Ancien chatbot iframe (chemin relatif incorrect)
OLD_CHATBOT = '<iframe src="../chatbot-ia/index.html" style="width: 100%; height: 100%; border: none;"></iframe>'

# Nouveau chatbot iframe (URL absolue correcte)
NEW_CHATBOT = '<iframe src="https://www.iafactoryalgeria.com/apps/chatbot-ia/" style="width: 100%; height: 100%; border: none;"></iframe>'

def fix_chatbot_in_file(file_path):
    """Corrige le chatbot dans un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        if OLD_CHATBOT in content:
            content = content.replace(OLD_CHATBOT, NEW_CHATBOT)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True
        return False
    except Exception as e:
        print(f"Erreur avec {file_path}: {e}")
        return False

def main():
    base_dir = Path(__file__).parent.parent
    apps_dir = base_dir / 'apps'

    print("=" * 80)
    print("CORRECTION DU CHATBOT DANS TOUTES LES APPS")
    print("=" * 80)
    print()

    fixed_count = 0

    for app_name in APPS_TO_FIX:
        app_path = apps_dir / app_name / 'index.html'

        if not app_path.exists():
            print(f"[SKIP] {app_name}: Fichier non trouvé")
            continue

        if fix_chatbot_in_file(app_path):
            print(f"[OK] {app_name}: Chatbot corrigé")
            fixed_count += 1
        else:
            print(f"[SKIP] {app_name}: Pas de chatbot à corriger")

    print()
    print("=" * 80)
    print(f"RÉSULTAT: {fixed_count} apps corrigées")
    print("=" * 80)

if __name__ == '__main__':
    main()
