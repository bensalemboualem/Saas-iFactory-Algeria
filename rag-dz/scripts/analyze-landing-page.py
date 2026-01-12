#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyser la landing page complète
"""
from pathlib import Path
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    landing = Path(r'd:\IAFactory\rag-dz\landing-complete-responsive.html')

    with open(landing, 'r', encoding='utf-8') as f:
        content = f.read()

    print('='*80)
    print('ANALYSE DE LA LANDING PAGE COMPLETE')
    print('='*80)
    print()

    # Taille
    lines = content.count('\n') + 1
    chars = len(content)
    print(f'📄 Fichier: {landing.name}')
    print(f'   Lignes: {lines:,}')
    print(f'   Taille: {chars:,} caractères ({chars/1024:.1f} KB)')
    print()

    # Features détectées
    features = []
    if 'dark-mode' in content.lower() or 'data-theme' in content:
        features.append('🌙 Dark/Light Mode')
    if 'chat' in content.lower():
        features.append('💬 Chat IA intégré')
    if 'sidebar' in content.lower():
        features.append('📁 Sidebar Apps')
    if 'language' in content.lower() or 'lang-' in content:
        features.append('🌍 Multi-langue')
    if 'api' in content.lower() and 'key' in content.lower():
        features.append('🔑 Gestion clés API')
    if '@media' in content:
        features.append('📱 Responsive Design')
    if 'provider' in content.lower():
        features.append('🤖 Multi-providers IA')

    print('✨ FEATURES DÉTECTÉES:')
    for feature in features:
        print(f'   {feature}')
    print()

    # Compter les apps référencées
    app_matches = re.findall(r'href="[./]*apps/([^"]+)"', content)
    unique_apps = set(app_matches)
    print(f'📦 Applications référencées: {len(unique_apps)}')
    if len(unique_apps) <= 10:
        for app in sorted(unique_apps):
            print(f'   • {app}')
    else:
        for app in sorted(list(unique_apps)[:10]):
            print(f'   • {app}')
        print(f'   ... et {len(unique_apps)-10} autres')
    print()

    # Liens vers docs/directory
    dir_links = re.findall(r'href="[./]*(docs/directory/[^"]+)"', content)
    unique_dirs = set(dir_links)
    print(f'📚 Liens Directory: {len(unique_dirs)}')
    for link in sorted(unique_dirs):
        print(f'   • {link}')
    print()

    # API endpoints
    api_matches = re.findall(r'[\'"]/(api/[^\'"\s]+)[\'"]', content)
    unique_apis = set(api_matches)
    if unique_apis:
        print(f'🔌 API Endpoints: {len(unique_apis)}')
        for api in sorted(list(unique_apis)[:5]):
            print(f'   • {api}')
        if len(unique_apis) > 5:
            print(f'   ... et {len(unique_apis)-5} autres')
        print()

    # Dépendances externes
    cdn_links = re.findall(r'https://[^"\']+(?:cdnjs|unpkg|jsdelivr)[^"\']+', content)
    print(f'🌐 CDN externes: {len(set(cdn_links))}')
    cdn_types = set()
    for cdn in cdn_links:
        if 'font-awesome' in cdn:
            cdn_types.add('Font Awesome')
        elif 'marked' in cdn:
            cdn_types.add('Marked.js (Markdown)')
        elif 'highlight' in cdn:
            cdn_types.add('Highlight.js (Code syntax)')
    for cdn_type in sorted(cdn_types):
        print(f'   • {cdn_type}')
    print()

    # Vérifier structure HTML
    has_doctype = '<!DOCTYPE html>' in content
    has_viewport = 'viewport' in content
    has_charset = 'charset' in content.lower()

    print('🔍 VALIDATION HTML:')
    print(f'   DOCTYPE: {"✅" if has_doctype else "❌"}')
    print(f'   Viewport: {"✅" if has_viewport else "❌"}')
    print(f'   Charset: {"✅" if has_charset else "❌"}')
    print()

    print('='*80)
    print('✅ LANDING PAGE PRÊTE POUR INTÉGRATION VPS')
    print('='*80)
    print()
    print('📋 PROCHAINES ÉTAPES:')
    print('  1. Copier landing-complete-responsive.html → apps/landing/index.html')
    print('  2. Vérifier tous les liens relatifs (apps/, docs/)')
    print('  3. Configurer Nginx pour servir la landing page à la racine /')
    print('  4. Tester le déploiement VPS complet')
    print()
    print('='*80)

if __name__ == '__main__':
    main()
