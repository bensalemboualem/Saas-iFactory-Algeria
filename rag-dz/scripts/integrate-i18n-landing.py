#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'intégration automatique du système multilingue (FR/AR/EN)
dans la landing page IAFactory

Usage:
    python scripts/integrate-i18n-landing.py

Modifications appliquées:
1. Ajout script i18n dans <head>
2. Ajout language switcher dans header
3. Insertion section PRO entre #apps et #cta
"""

import os
import re
from pathlib import Path


def read_file(filepath):
    """Lit un fichier avec encodage UTF-8"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(filepath, content):
    """Écrit un fichier avec encodage UTF-8"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def extract_component(source_file, start_marker, end_marker):
    """Extrait un composant entre deux marqueurs"""
    content = read_file(source_file)

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        raise ValueError(f"Marqueurs non trouvés: {start_marker} ... {end_marker}")

    return content[start_idx:end_idx + len(end_marker)]


def integrate_i18n():
    """Intègre le système i18n dans la landing page"""

    # Chemins
    base_dir = Path(__file__).parent.parent
    landing_file = base_dir / 'apps' / 'landing' / 'index.html'
    i18n_file = base_dir / 'apps' / 'landing' / 'iafactory-i18n-complete.html'
    output_file = base_dir / 'apps' / 'landing' / 'index-i18n.html'

    print("🚀 Intégration système multilingue IAFactory...")
    print(f"   Source: {landing_file}")
    print(f"   i18n: {i18n_file}")
    print(f"   Output: {output_file}")
    print()

    # Lire landing page
    landing_content = read_file(landing_file)
    i18n_content = read_file(i18n_file)

    # ===== ÉTAPE 1: Extraire et insérer le script i18n =====
    print("📝 Étape 1/3: Extraction script i18n...")

    # Extraire le script du fichier i18n
    script_start = i18n_content.find('<script>')
    script_end = i18n_content.find('</script>', script_start) + len('</script>')
    i18n_script = i18n_content[script_start:script_end]

    # Insérer avant </head>
    landing_content = landing_content.replace(
        '    <style>',
        f'{i18n_script}\n\n    <style>'
    )
    print("   ✅ Script i18n ajouté dans <head>")

    # ===== ÉTAPE 2: Extraire et insérer le language switcher =====
    print("📝 Étape 2/3: Extraction language switcher...")

    # Extraire le switcher
    switcher_start = i18n_content.find('<div class="language-switcher">')
    switcher_end = i18n_content.find('</div>', switcher_start) + len('</div>')
    language_switcher = i18n_content[switcher_start:switcher_end]

    # Extraire le CSS du switcher
    css_start = i18n_content.find('/* Language Switcher */')
    css_end = i18n_content.find('</style>', css_start)
    language_css = i18n_content[css_start:css_end].strip()

    # Insérer le switcher après le theme toggle
    # Rechercher la structure du theme toggle
    theme_toggle_pattern = r'(<button[^>]*class="theme-toggle"[^>]*>.*?</button>)'
    match = re.search(theme_toggle_pattern, landing_content, re.DOTALL)

    if match:
        theme_toggle_html = match.group(1)
        landing_content = landing_content.replace(
            theme_toggle_html,
            f'{theme_toggle_html}\n\n            {language_switcher}'
        )
        print("   ✅ Language switcher ajouté dans header")
    else:
        print("   ⚠️  Theme toggle non trouvé, switcher non inséré")

    # Insérer le CSS avant la fermeture de </style>
    landing_content = landing_content.replace(
        '    </style>',
        f'\n{language_css}\n    </style>'
    )
    print("   ✅ CSS language switcher ajouté")

    # ===== ÉTAPE 3: Extraire et insérer la section PRO =====
    print("📝 Étape 3/3: Extraction section PRO...")

    # Extraire la section PRO
    pro_start = i18n_content.find('<section id="pro-solutions"')
    pro_end = i18n_content.find('</section>', pro_start) + len('</section>')
    pro_section = i18n_content[pro_start:pro_end]

    # Trouver le point d'insertion (entre #apps et #cta)
    # Rechercher la fin de la section apps et le début de la section CTA
    cta_section_pattern = r'(</section>\s*<!-- CTA -->\s*<section id="cta")'
    match = re.search(cta_section_pattern, landing_content, re.DOTALL)

    if match:
        original_text = match.group(1)
        replacement = f'</section>\n\n        {pro_section}\n\n        <!-- CTA -->\n        <section id="cta"'
        landing_content = landing_content.replace(original_text, replacement)
        print("   ✅ Section PRO insérée entre #apps et #cta")
    else:
        print("   ⚠️  Point d'insertion #cta non trouvé, section PRO non insérée")

    # ===== Sauvegarder le résultat =====
    print()
    print("💾 Sauvegarde du fichier modifié...")
    write_file(output_file, landing_content)

    # Statistiques
    original_lines = len(read_file(landing_file).split('\n'))
    new_lines = len(landing_content.split('\n'))
    added_lines = new_lines - original_lines

    print(f"   ✅ Fichier sauvegardé: {output_file}")
    print()
    print("📊 Statistiques:")
    print(f"   Lignes originales: {original_lines}")
    print(f"   Lignes finales: {new_lines}")
    print(f"   Lignes ajoutées: +{added_lines}")
    print()
    print("✅ Intégration terminée!")
    print()
    print("🚀 Prochaines étapes:")
    print("   1. Vérifier: d:/IAFactory/rag-dz/apps/landing/index-i18n.html")
    print("   2. Tester en local (ouvrir dans navigateur)")
    print("   3. Si OK, renommer: index-i18n.html → index.html")
    print("   4. Déployer: scp index.html root@46.224.3.125:/opt/iafactory-rag-dz/apps/landing/")
    print()


if __name__ == '__main__':
    try:
        integrate_i18n()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
