#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vérifier que toutes les clés data-i18n ont une traduction arabe
"""

import re
import sys

# Lire le fichier index.html
with open('apps/landing/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 1. Extraire toutes les clés data-i18n utilisées dans le HTML
data_i18n_keys = set(re.findall(r'data-i18n="([^"]+)"', html_content))
print(f"=== CLÉS data-i18n UTILISÉES: {len(data_i18n_keys)} ===\n")

# 2. Extraire toutes les clés avec traduction AR du dictionnaire JavaScript
ar_translations = {}
pattern = r'"([^"]+)":\s*\{\s*fr:\s*"[^"]*",\s*ar:\s*"([^"]*)",\s*en:\s*"[^"]*"\s*\}'
for match in re.finditer(pattern, html_content):
    key = match.group(1)
    ar_text = match.group(2)
    ar_translations[key] = ar_text

print(f"=== CLÉS AVEC TRADUCTION AR: {len(ar_translations)} ===\n")

# 3. Vérifier les clés manquantes
missing_translations = []
for key in sorted(data_i18n_keys):
    if key not in ar_translations:
        missing_translations.append(key)
    elif not ar_translations[key] or ar_translations[key].isspace():
        missing_translations.append(f"{key} (vide)")

# 4. Résultats
if missing_translations:
    print(f"❌ TRADUCTIONS ARABES MANQUANTES: {len(missing_translations)}\n")
    for key in missing_translations:
        print(f"  - {key}")
    sys.exit(1)
else:
    print("✅ TOUTES LES CLÉS ONT UNE TRADUCTION ARABE!\n")

    # Afficher quelques exemples
    print("=== EXEMPLES DE TRADUCTIONS AR ===\n")
    sample_keys = ['user', 'developer', 'new_conversation', 'products', 'footer_description',
                   'title_archon_ui', 'badge_business', 'btn_open']
    for key in sample_keys:
        if key in ar_translations:
            print(f"{key:25} → {ar_translations[key]}")

    print(f"\n=== STATISTIQUES ===")
    print(f"Total clés utilisées: {len(data_i18n_keys)}")
    print(f"Total traductions AR: {len(ar_translations)}")
    print(f"Couverture: 100%")
    sys.exit(0)
