#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corriger les erreurs HTML dans les 8 apps
"""
from pathlib import Path
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

APPS_TO_FIX = [
    "crm-ia-ui",
    "data-dz",
    "dev-portal",
    "developer",
    "fiscal-assistant",
    "legal-assistant",
    "pmedz-sales",
    "startupdz-onboarding-ui"
]

def fix_html(html_content):
    """Corriger les problèmes HTML"""

    # S'assurer que </body> existe
    if '<body' in html_content and '</body>' not in html_content:
        # Ajouter </body> avant </html>
        if '</html>' in html_content:
            html_content = html_content.replace('</html>', '</body>\n</html>')
        else:
            html_content += '\n</body>\n</html>'

    # S'assurer que </html> existe
    if '<html' in html_content and '</html>' not in html_content:
        html_content += '\n</html>'

    return html_content

def main():
    apps_dir = Path(r"d:\IAFactory\rag-dz\apps")

    print("="*80)
    print("CORRECTION DES ERREURS HTML")
    print("="*80)

    fixed_count = 0

    for app_name in APPS_TO_FIX:
        app_path = apps_dir / app_name
        index_path = app_path / "index.html"

        if not index_path.exists():
            print(f"\n[SKIP] {app_name} - index.html non trouvé")
            continue

        print(f"\n[FIX] {app_name}")

        try:
            # Lire le fichier
            with open(index_path, 'r', encoding='utf-8') as f:
                original = f.read()

            # Diagnostiquer le problème
            has_body_open = '<body' in original
            has_body_close = '</body>' in original
            has_html_close = '</html>' in original

            print(f"  <body>: {has_body_open}, </body>: {has_body_close}, </html>: {has_html_close}")

            # Corriger
            fixed = fix_html(original)

            # Vérifier que c'est corrigé
            if fixed != original:
                # Écrire le fichier corrigé
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(fixed)

                print(f"  ✅ Corrigé")
                fixed_count += 1
            else:
                print(f"  ℹ️  Aucune correction nécessaire")

        except Exception as e:
            print(f"  ❌ Erreur: {e}")

    print("\n" + "="*80)
    print(f"✅ {fixed_count}/{len(APPS_TO_FIX)} apps corrigées")
    print("="*80)

if __name__ == "__main__":
    main()
