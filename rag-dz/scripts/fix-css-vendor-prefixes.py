#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corriger les vendor prefixes CSS manquants dans les fichiers Directory
"""
from pathlib import Path
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def fix_vendor_prefixes(css_content):
    """Ajouter les propriétés standard après les vendor prefixes"""
    fixes_made = []

    # Fix 1: -webkit-line-clamp
    # Chercher les occurrences de -webkit-line-clamp sans line-clamp qui suit
    pattern1 = r'(-webkit-line-clamp:\s*\d+;)(?!\s*line-clamp:)'

    def replace_line_clamp(match):
        webkit_prop = match.group(1)
        value = re.search(r'\d+', webkit_prop).group()
        fixes_made.append(f'-webkit-line-clamp -> +line-clamp: {value}')
        return f'{webkit_prop}\n            line-clamp: {value};'

    css_content = re.sub(pattern1, replace_line_clamp, css_content)

    # Fix 2: -webkit-background-clip
    # Chercher les occurrences de -webkit-background-clip sans background-clip qui suit
    pattern2 = r'(-webkit-background-clip:\s*text;)(?!\s*background-clip:)'

    def replace_bg_clip(match):
        webkit_prop = match.group(1)
        fixes_made.append('-webkit-background-clip -> +background-clip: text')
        return f'{webkit_prop}\n            background-clip: text;'

    css_content = re.sub(pattern2, replace_bg_clip, css_content)

    return css_content, fixes_made

def fix_file(file_path):
    """Corriger un fichier HTML"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        fixed_content, fixes = fix_vendor_prefixes(content)

        if fixes:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True, fixes
        else:
            return False, []

    except Exception as e:
        return False, [f'Erreur: {e}']

def main():
    directory_path = Path(r'd:\IAFactory\rag-dz\docs\directory')

    print('='*80)
    print('CORRECTION DES VENDOR PREFIXES CSS - DIRECTORY')
    print('='*80)
    print()

    files_to_fix = [
        'agents.html',
        'daily-news.html',
        'ia-tools.html',
        'workflows.html'
    ]

    total_fixed = 0
    total_changes = 0

    for filename in files_to_fix:
        file_path = directory_path / filename

        if not file_path.exists():
            print(f'⚠️  {filename:<25} [NON TROUVÉ]')
            continue

        print(f'🔧 {filename:<25}', end=' ')

        fixed, changes = fix_file(file_path)

        if fixed:
            print(f'✅ {len(changes)} corrections')
            for change in changes:
                print(f'    • {change}')
            total_fixed += 1
            total_changes += len(changes)
        else:
            print('✓ Aucune correction nécessaire')

    print()
    print('='*80)
    print(f'✅ {total_fixed}/{len(files_to_fix)} fichiers corrigés')
    print(f'✅ {total_changes} propriétés standard ajoutées')
    print('='*80)
    print()
    print('📝 Corrections appliquées:')
    print('  • -webkit-line-clamp → ajout de line-clamp')
    print('  • -webkit-background-clip → ajout de background-clip')
    print()
    print('✅ Les problèmes CSS sont corrigés!')
    print('='*80)

if __name__ == '__main__':
    main()
