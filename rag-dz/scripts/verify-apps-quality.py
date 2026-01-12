#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vérification de la qualité des applications
Vérifie que chaque app a un contenu professionnel complet
"""
from pathlib import Path
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_app_quality(html_content):
    """Vérifier la qualité d'une application"""
    checks = {
        'has_css': '<style>' in html_content and len(html_content) > 5000,
        'has_js': '<script>' in html_content,
        'has_responsive': '@media' in html_content,
        'has_animations': 'animation' in html_content or 'transition' in html_content,
        'has_api_integration': 'fetch(' in html_content or 'API' in html_content,
        'has_event_handlers': 'addEventListener' in html_content,
        'has_status_indicator': 'status' in html_content.lower(),
        'professional_design': 'gradient' in html_content or 'box-shadow' in html_content
    }

    score = sum(checks.values())
    total = len(checks)
    percentage = (score / total) * 100

    return {
        'score': score,
        'total': total,
        'percentage': percentage,
        'checks': checks,
        'size': len(html_content),
        'is_professional': percentage >= 75  # Au moins 75% des critères
    }

def main():
    apps_dir = Path(r"d:\IAFactory\rag-dz\apps")

    print("="*80)
    print("VERIFICATION DE LA QUALITE DES APPLICATIONS")
    print("="*80)

    professional_apps = []
    basic_apps = []
    missing_index = []

    for app_path in sorted(apps_dir.iterdir()):
        if not app_path.is_dir():
            continue

        app_name = app_path.name
        index_path = app_path / "index.html"

        # Vérifier si index.html existe (à la racine ou dans un sous-dossier)
        index_files = list(app_path.rglob("index.html"))

        if not index_files:
            missing_index.append(app_name)
            continue

        # Utiliser le premier index.html trouvé
        index_path = index_files[0]

        # Lire et analyser le contenu
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            quality = check_app_quality(html_content)

            if quality['is_professional']:
                professional_apps.append((app_name, quality))
            else:
                basic_apps.append((app_name, quality))
        except Exception as e:
            print(f"\n[ERROR] {app_name}: {e}")
            basic_apps.append((app_name, {'percentage': 0, 'size': 0}))

    # Afficher les résultats
    print(f"\n✅ APPS PROFESSIONNELLES: {len(professional_apps)}/{len(professional_apps) + len(basic_apps)}")
    for app_name, quality in professional_apps:
        print(f"  ✅ {app_name:<40} ({quality['percentage']:.0f}% qualité, {quality['size']:,} caractères)")

    if basic_apps:
        print(f"\n⚠️  APPS BASIQUES (< 75% qualité): {len(basic_apps)}")
        for app_name, quality in basic_apps:
            print(f"  ⚠️  {app_name:<40} ({quality.get('percentage', 0):.0f}% qualité)")

    if missing_index:
        print(f"\n❌ APPS SANS INDEX.HTML: {len(missing_index)}")
        for app_name in missing_index:
            print(f"  ❌ {app_name}")

    print("\n" + "="*80)
    print(f"RÉSUMÉ:")
    print(f"  Apps professionnelles:  {len(professional_apps)}")
    print(f"  Apps basiques:          {len(basic_apps)}")
    print(f"  Apps sans index:        {len(missing_index)}")
    print(f"  TOTAL:                  {len(professional_apps) + len(basic_apps) + len(missing_index)}")
    print(f"  Taux de qualité:        {len(professional_apps)/(len(professional_apps)+len(basic_apps))*100:.1f}%")
    print("="*80)

    if len(professional_apps) == (len(professional_apps) + len(basic_apps) + len(missing_index)):
        print("\n✅ TOUTES LES APPS SONT PROFESSIONNELLES !")
        print("✅ PRÊT POUR LE DÉPLOIEMENT VPS !")
    elif len(missing_index) == 0 and len(basic_apps) == 0:
        print("\n✅ TOUTES LES APPS ONT UN INDEX.HTML PROFESSIONNEL !")
        print("✅ PRÊT POUR LE DÉPLOIEMENT VPS !")
    else:
        print("\n⚠️  Il reste des apps à améliorer")

if __name__ == "__main__":
    main()
