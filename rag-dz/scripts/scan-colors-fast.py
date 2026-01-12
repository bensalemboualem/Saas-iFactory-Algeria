#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan rapide des couleurs incorrectes
"""

import os
import sys
from pathlib import Path

# Force UTF-8 for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Couleurs incorrectes
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

def scan_file(file_path):
    """Scan un fichier pour les couleurs incorrectes"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        issues = []
        for wrong, correct in WRONG_COLORS.items():
            if wrong in content:
                count = content.count(wrong)
                issues.append((wrong, correct, count))

        return issues
    except:
        return []

def scan_directory(dir_path, extensions=['.html', '.css', '.scss', '.js', '.jsx', '.ts', '.tsx']):
    """Scan un répertoire"""
    all_issues = {}

    for ext in extensions:
        for file_path in Path(dir_path).rglob(f'*{ext}'):
            # Skip node_modules, dist, build, .git
            if any(skip in str(file_path) for skip in ['node_modules', 'dist', 'build', '.git', '__pycache__']):
                continue

            issues = scan_file(file_path)
            if issues:
                all_issues[str(file_path)] = issues

    return all_issues

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 80)
    print("SCAN RAPIDE DES COULEURS INCORRECTES")
    print("=" * 80)
    print()

    # Priorités à scanner
    priority_apps = [
        ('apps/landing', 'Landing Page'),
        ('frontend/archon-ui-stable/archon-ui-main/src', 'Archon UI'),
        ('frontend/rag-ui/src', 'RAG UI'),
        ('apps/chatbot-ia', 'Chatbot IA'),
        ('apps/dashboard', 'Dashboard'),
    ]

    total_files = 0
    total_issues = 0

    for path, name in priority_apps:
        full_path = base_dir / path
        if not full_path.exists():
            print(f"[SKIP] {name}: Repertoire non trouve")
            continue

        print(f"[SCAN] {name}...")
        issues = scan_directory(full_path)

        if issues:
            print(f"  -> {len(issues)} fichiers avec problemes")
            for file, file_issues in list(issues.items())[:3]:  # Montrer 3 premiers
                rel_path = Path(file).relative_to(base_dir)
                print(f"     {rel_path}")
                for wrong, correct, count in file_issues[:2]:  # 2 premiers problèmes
                    print(f"       - {wrong} -> {correct} ({count}x)")
            if len(issues) > 3:
                print(f"     ... et {len(issues) - 3} autres fichiers")
            total_files += len(issues)
            total_issues += sum(sum(c for _, _, c in f) for f in issues.values())
        else:
            print(f"  -> OK - Aucun probleme")
        print()

    print("=" * 80)
    print(f"RESUME:")
    print(f"  Fichiers a corriger: {total_files}")
    print(f"  Total occurrences: {total_issues}")
    print("=" * 80)

if __name__ == '__main__':
    main()
