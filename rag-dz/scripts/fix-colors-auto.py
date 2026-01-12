#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction automatique des couleurs
"""

import os
import sys
from pathlib import Path
import shutil

# Force UTF-8 for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Couleurs incorrectes à remplacer
WRONG_COLORS = {
    '#ffffff': '#f7f5f0',
    '#fff': '#f7f5f0',
    '0 0% 100%': '40 22% 95%',
    '#000000': '#020617',
    '#000': '#020617',
    '0 0% 0%': '222 84% 5%',
    '#a855f7': '#00a651',
    '271 91% 65%': '143 100% 33%',
}

def fix_file(file_path, dry_run=False):
    """Corrige les couleurs dans un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        original = content
        changes = []

        for wrong, correct in WRONG_COLORS.items():
            if wrong in content:
                count = content.count(wrong)
                content = content.replace(wrong, correct)
                changes.append((wrong, correct, count))

        if content != original:
            if not dry_run:
                # Backup
                backup_path = str(file_path) + '.backup'
                shutil.copy2(file_path, backup_path)

                # Write corrected content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

            return changes
        return []
    except Exception as e:
        print(f"  [ERREUR] {file_path}: {e}")
        return []

def fix_directory(dir_path, extensions=['.html', '.css', '.scss', '.js', '.jsx', '.ts', '.tsx'], dry_run=False):
    """Corrige tous les fichiers d'un répertoire"""
    fixed_files = []

    for ext in extensions:
        for file_path in Path(dir_path).rglob(f'*{ext}'):
            # Skip node_modules, dist, build, .git
            if any(skip in str(file_path) for skip in ['node_modules', 'dist', 'build', '.git', '__pycache__']):
                continue

            changes = fix_file(file_path, dry_run=dry_run)
            if changes:
                fixed_files.append((file_path, changes))

    return fixed_files

def main():
    base_dir = Path(__file__).parent.parent

    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv

    print("=" * 80)
    if dry_run:
        print("CORRECTION DES COULEURS - MODE DRY RUN (SIMULATION)")
    else:
        print("CORRECTION DES COULEURS - MODE ACTIF")
    print("=" * 80)
    print()

    # Priorités à corriger
    priority_apps = [
        ('apps/landing', 'Landing Page'),
        ('frontend/archon-ui-stable/archon-ui-main/src', 'Archon UI'),
        ('frontend/rag-ui/src', 'RAG UI'),
        ('apps/chatbot-ia', 'Chatbot IA'),
    ]

    total_files = 0
    total_changes = 0

    for path, name in priority_apps:
        full_path = base_dir / path
        if not full_path.exists():
            print(f"[SKIP] {name}: Repertoire non trouve")
            continue

        print(f"[FIX] {name}...")
        fixed = fix_directory(full_path, dry_run=dry_run)

        if fixed:
            action = "seront corriges" if dry_run else "corriges"
            print(f"  -> {len(fixed)} fichiers {action}")
            for file_path, changes in fixed[:3]:  # Montrer 3 premiers
                rel_path = Path(file_path).relative_to(base_dir)
                print(f"     {rel_path}")
                for wrong, correct, count in changes[:2]:
                    print(f"       - {wrong} -> {correct} ({count}x)")
            if len(fixed) > 3:
                print(f"     ... et {len(fixed) - 3} autres fichiers")

            total_files += len(fixed)
            total_changes += sum(sum(c for _, _, c in changes) for _, changes in fixed)
        else:
            print(f"  -> OK - Aucune correction necessaire")
        print()

    print("=" * 80)
    if dry_run:
        print(f"SIMULATION COMPLETE:")
        print(f"  Fichiers a corriger: {total_files}")
        print(f"  Total modifications: {total_changes}")
        print()
        print("Pour appliquer les corrections, relancez sans --dry-run")
    else:
        print(f"CORRECTIONS APPLIQUEES:")
        print(f"  Fichiers corriges: {total_files}")
        print(f"  Total modifications: {total_changes}")
        print()
        print("Les fichiers originaux ont ete sauvegardes avec l'extension .backup")
    print("=" * 80)

if __name__ == '__main__':
    main()
