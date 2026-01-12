#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour harmoniser les couleurs de toutes les apps avec la landing page
Couleurs de référence:
- Light mode: bg=#f7f5f0, primary=#00a651
- Dark mode: bg=#020617, primary=#00a651
"""

import os
import re
import sys
from pathlib import Path

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Couleurs de référence
REF_COLORS = {
    'light_bg': '#f7f5f0',  # beige
    'dark_bg': '#020617',   # bleu foncé
    'primary': '#00a651',   # vert IAFactory
}

# Variantes HSL
REF_COLORS_HSL = {
    'light_bg_hsl': '40 22% 95%',
    'dark_bg_hsl': '222 84% 5%',
    'primary_hsl': '143 100% 33%',
}

# Couleurs incorrectes à remplacer
WRONG_COLORS = {
    # Blancs purs
    '#ffffff': REF_COLORS['light_bg'],
    '#fff': REF_COLORS['light_bg'],
    '0 0% 100%': REF_COLORS_HSL['light_bg_hsl'],
    '0 0% 98%': REF_COLORS_HSL['light_bg_hsl'],

    # Noirs purs
    '#000000': REF_COLORS['dark_bg'],
    '#000': REF_COLORS['dark_bg'],
    '0 0% 0%': REF_COLORS_HSL['dark_bg_hsl'],
    '0 0% 5%': REF_COLORS_HSL['dark_bg_hsl'],

    # Violets (anciennes couleurs Archon)
    '#a855f7': REF_COLORS['primary'],
    '271 91% 65%': REF_COLORS_HSL['primary_hsl'],
}

def find_color_files(base_dir):
    """Trouve tous les fichiers HTML, CSS, JS avec des couleurs"""
    files = []
    for ext in ['*.html', '*.css', '*.scss', '*.jsx', '*.tsx', '*.ts', '*.js']:
        files.extend(Path(base_dir).rglob(ext))
    return files

def detect_wrong_colors(file_path):
    """Détecte les couleurs incorrectes dans un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        issues = []
        for wrong, correct in WRONG_COLORS.items():
            if wrong in content:
                count = content.count(wrong)
                issues.append({
                    'file': str(file_path),
                    'wrong': wrong,
                    'correct': correct,
                    'count': count
                })

        return issues
    except Exception as e:
        print(f"Erreur lecture {file_path}: {e}")
        return []

def fix_colors(file_path, dry_run=True):
    """Corrige les couleurs dans un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        for wrong, correct in WRONG_COLORS.items():
            content = content.replace(wrong, correct)

        if content != original:
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            else:
                print(f"  [DRY RUN] Corrections dans: {file_path}")
                return True
        return False
    except Exception as e:
        print(f"Erreur correction {file_path}: {e}")
        return False

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 80)
    print("HARMONISATION DES COULEURS - TOUTES LES APPS")
    print("=" * 80)
    print(f"\nRéférence Landing Page:")
    print(f"  Light bg : {REF_COLORS['light_bg']} ({REF_COLORS_HSL['light_bg_hsl']})")
    print(f"  Dark bg  : {REF_COLORS['dark_bg']} ({REF_COLORS_HSL['dark_bg_hsl']})")
    print(f"  Primary  : {REF_COLORS['primary']} ({REF_COLORS_HSL['primary_hsl']})")
    print()

    # Scanner les apps
    apps_dir = base_dir / 'apps'
    frontend_dir = base_dir / 'frontend'

    all_issues = []

    print("[SCAN] SCAN DES APPLICATIONS...")
    print()

    # Scanner apps/
    for app_dir in sorted(apps_dir.iterdir()):
        if app_dir.is_dir():
            files = find_color_files(app_dir)
            for file_path in files:
                issues = detect_wrong_colors(file_path)
                if issues:
                    all_issues.extend(issues)

    # Scanner frontend/
    for frontend_app in sorted(frontend_dir.iterdir()):
        if frontend_app.is_dir():
            files = find_color_files(frontend_app)
            for file_path in files:
                issues = detect_wrong_colors(file_path)
                if issues:
                    all_issues.extend(issues)

    # Afficher résumé
    print(f"\n[RESUME] RESUME:")
    print(f"  Total fichiers avec couleurs incorrectes: {len(set(i['file'] for i in all_issues))}")
    print(f"  Total occurrences a corriger: {sum(i['count'] for i in all_issues)}")
    print()

    if all_issues:
        # Grouper par fichier
        files_dict = {}
        for issue in all_issues:
            if issue['file'] not in files_dict:
                files_dict[issue['file']] = []
            files_dict[issue['file']].append(issue)

        print("[DETAILS] DETAILS PAR FICHIER:")
        for i, (file, issues) in enumerate(sorted(files_dict.items())[:10], 1):
            print(f"\n{i}. {Path(file).relative_to(base_dir)}")
            for issue in issues:
                print(f"   - {issue['wrong']} → {issue['correct']} ({issue['count']}×)")

        if len(files_dict) > 10:
            print(f"\n... et {len(files_dict) - 10} fichiers supplémentaires")

        print("\n" + "=" * 80)
        print("Pour corriger automatiquement, lance:")
        print(f"  python {sys.argv[0]} --fix")
        print("=" * 80)
    else:
        print("[OK] Aucune couleur incorrecte detectee!")

if __name__ == '__main__':
    if '--fix' in sys.argv:
        print("[FIX] MODE CORRECTION ACTIVE")
        # TODO: implémenter correction
    else:
        main()
