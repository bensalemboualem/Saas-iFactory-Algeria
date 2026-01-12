#!/usr/bin/env python3
"""
===================================================================
SCRIPT D'INTÉGRATION i18n AUTOMATIQUE
Intègre le système trilingue dans TOUTES les applications
===================================================================
"""

import os
import re
from pathlib import Path

# Chemins
RAG_DZ_ROOT = Path(__file__).parent.parent
APPS_DIR = RAG_DZ_ROOT / "apps"
SHARED_DIR = RAG_DZ_ROOT / "shared"

# Fichiers partagés
I18N_JS = SHARED_DIR / "i18n.js"
THEME_CSS = SHARED_DIR / "iafactory-theme.css"
LANG_SWITCHER_JS = SHARED_DIR / "language-switcher.js"

# Template HTML pour intégrer i18n
I18N_INTEGRATION_TEMPLATE = """
<!-- IAFactory i18n System - TRILINGUE -->
<link rel="stylesheet" href="/shared/iafactory-theme.css">
<script src="/shared/i18n.js"></script>
<script src="/shared/language-switcher.js"></script>
"""

LANG_SWITCHER_HTML = """
<!-- Language Switcher -->
<div data-language-switcher></div>
"""


def find_all_html_files():
    """Trouve tous les fichiers HTML dans les apps"""
    html_files = []
    for app_dir in APPS_DIR.iterdir():
        if app_dir.is_dir():
            for html_file in app_dir.rglob("*.html"):
                html_files.append(html_file)
    return html_files


def integrate_i18n_in_html(html_file):
    """Intègre le système i18n dans un fichier HTML"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Vérifier si déjà intégré
        if 'iafactory-theme.css' in content or 'i18n.js' in content:
            print(f"  ⏭️  Déjà intégré: {html_file.relative_to(RAG_DZ_ROOT)}")
            return False

        modified = False

        # 1. Ajouter les fichiers partagés dans <head>
        if '</head>' in content:
            content = content.replace('</head>', f'{I18N_INTEGRATION_TEMPLATE}\n</head>')
            modified = True

        # 2. Ajouter le language switcher dans le header
        # Chercher le header/navbar
        header_patterns = [
            (r'(<header[^>]*>.*?<div[^>]*class[^>]*header-container[^>]*>)',
             r'\1\n{switcher}'),
            (r'(<nav[^>]*>.*?<div[^>]*class[^>]*nav[^>]*>)',
             r'\1\n{switcher}'),
            (r'(<div[^>]*class[^>]*header[^>]*>)',
             r'\1\n{switcher}'),
        ]

        for pattern, replacement in header_patterns:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(
                    pattern,
                    replacement.format(switcher=LANG_SWITCHER_HTML),
                    content,
                    count=1,
                    flags=re.DOTALL
                )
                modified = True
                break

        if modified:
            # Écrire le fichier modifié
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Intégré: {html_file.relative_to(RAG_DZ_ROOT)}")
            return True
        else:
            print(f"  ⚠️  Pas de header trouvé: {html_file.relative_to(RAG_DZ_ROOT)}")
            return False

    except Exception as e:
        print(f"  ❌ Erreur avec {html_file.relative_to(RAG_DZ_ROOT)}: {e}")
        return False


def main():
    print("=" * 70)
    print("INTÉGRATION i18n TRILINGUE - TOUTES LES APPLICATIONS")
    print("=" * 70)
    print()

    # Vérifier que les fichiers partagés existent
    if not I18N_JS.exists():
        print(f"❌ Fichier manquant: {I18N_JS}")
        return

    if not THEME_CSS.exists():
        print(f"❌ Fichier manquant: {THEME_CSS}")
        return

    if not LANG_SWITCHER_JS.exists():
        print(f"❌ Fichier manquant: {LANG_SWITCHER_JS}")
        return

    print(f"✅ Fichiers partagés trouvés:")
    print(f"   - {I18N_JS.name}")
    print(f"   - {THEME_CSS.name}")
    print(f"   - {LANG_SWITCHER_JS.name}")
    print()

    # Trouver tous les fichiers HTML
    html_files = find_all_html_files()
    print(f"🔍 {len(html_files)} fichiers HTML trouvés")
    print()

    # Intégrer i18n dans chaque fichier
    success_count = 0
    skip_count = 0
    error_count = 0

    for html_file in html_files:
        result = integrate_i18n_in_html(html_file)
        if result is True:
            success_count += 1
        elif result is False:
            skip_count += 1
        else:
            error_count += 1

    print()
    print("=" * 70)
    print("RÉSULTATS")
    print("=" * 70)
    print(f"✅ Intégrés avec succès: {success_count}")
    print(f"⏭️  Déjà intégrés: {skip_count}")
    print(f"❌ Erreurs: {error_count}")
    print()
    print("🎉 Intégration terminée!")
    print()
    print("PROCHAINES ÉTAPES:")
    print("1. Tester les pages en changeant de langue")
    print("2. Ajouter data-i18n attributes aux éléments à traduire")
    print("3. Exemple: <h1 data-i18n=\"hero.title\">Titre</h1>")
    print()


if __name__ == '__main__':
    main()
