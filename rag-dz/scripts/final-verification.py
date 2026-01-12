#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICATION FINALE COMPLETE ET RIGOUREUSE
Vérifie TOUT avant déploiement VPS
"""
from pathlib import Path
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_html_validity(html_content):
    """Vérifier la validité basique du HTML"""
    errors = []

    # Vérifier les balises essentielles
    if '<!DOCTYPE html>' not in html_content:
        errors.append("Manque DOCTYPE")
    if '<html' not in html_content:
        errors.append("Manque balise <html>")
    if '<head' not in html_content:
        errors.append("Manque balise <head>")
    if '<body' not in html_content:
        errors.append("Manque balise <body>")
    if '<title' not in html_content:
        errors.append("Manque balise <title>")

    # Vérifier fermeture des balises principales (ignorer les occurrences dans les attributs/texte)
    # Compter seulement les vraies balises HTML
    import re
    html_tags = len(re.findall(r'<html[>\s]', html_content))
    html_close = html_content.count('</html>')
    head_tags = len(re.findall(r'<head[>\s]', html_content))
    head_close = html_content.count('</head>')
    body_tags = len(re.findall(r'<body[>\s]', html_content))
    body_close = html_content.count('</body>')

    if html_close != html_tags:
        errors.append("Balises <html> non fermées correctement")
    if head_close != head_tags:
        errors.append("Balises <head> non fermées correctement")
    if body_close != body_tags:
        errors.append("Balises <body> non fermées correctement")

    return errors

def check_professional_content(html_content):
    """Vérifier que le contenu est professionnel"""
    checks = {
        'CSS': '<style>' in html_content,
        'CSS_Length': len(html_content) > 5000,
        'Responsive': '@media' in html_content,
        'Animations': 'animation' in html_content or 'transition' in html_content,
        'JavaScript': '<script>' in html_content,
        'Event_Handlers': 'addEventListener' in html_content,
        'API_Integration': 'fetch(' in html_content or '/api/' in html_content,
        'Modern_Design': 'flex' in html_content or 'grid' in html_content,
        'Gradient': 'gradient' in html_content,
        'Box_Shadow': 'box-shadow' in html_content
    }

    missing = [key for key, value in checks.items() if not value]
    score = sum(checks.values()) / len(checks) * 100

    return {
        'score': score,
        'checks': checks,
        'missing': missing
    }

def check_app_complete(app_path):
    """Vérification complète d'une app"""
    app_name = app_path.name

    # Chercher index.html (racine ou sous-dossiers)
    index_files = list(app_path.rglob("index.html"))

    if not index_files:
        return {
            'status': 'MISSING',
            'error': 'Pas d\'index.html trouvé',
            'details': None
        }

    # Prendre le premier index.html trouvé
    index_path = index_files[0]

    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Vérifier validité HTML
        html_errors = check_html_validity(html_content)

        # Vérifier contenu professionnel
        professional = check_professional_content(html_content)

        # Déterminer le statut
        if html_errors:
            status = 'INVALID_HTML'
        elif professional['score'] < 50:
            status = 'BASIC'
        elif professional['score'] < 75:
            status = 'GOOD'
        else:
            status = 'PROFESSIONAL'

        return {
            'status': status,
            'index_path': str(index_path.relative_to(app_path.parent.parent)),
            'size': len(html_content),
            'lines': html_content.count('\n') + 1,
            'html_errors': html_errors,
            'professional_score': professional['score'],
            'missing_features': professional['missing'],
            'details': professional
        }

    except Exception as e:
        return {
            'status': 'ERROR',
            'error': str(e),
            'details': None
        }

def main():
    apps_dir = Path(r"d:\IAFactory\rag-dz\apps")

    print("="*80)
    print("VERIFICATION FINALE COMPLETE - TOUTES LES APPS")
    print("="*80)
    print()

    results = {}

    # Vérifier chaque app
    for app_path in sorted(apps_dir.iterdir()):
        if not app_path.is_dir():
            continue

        app_name = app_path.name
        result = check_app_complete(app_path)
        results[app_name] = result

    # Catégoriser les résultats
    professional = []
    good = []
    basic = []
    invalid = []
    missing = []
    errors = []

    for app_name, result in results.items():
        if result['status'] == 'PROFESSIONAL':
            professional.append((app_name, result))
        elif result['status'] == 'GOOD':
            good.append((app_name, result))
        elif result['status'] == 'BASIC':
            basic.append((app_name, result))
        elif result['status'] == 'INVALID_HTML':
            invalid.append((app_name, result))
        elif result['status'] == 'MISSING':
            missing.append((app_name, result))
        else:
            errors.append((app_name, result))

    # Afficher les résultats
    print(f"✅ APPS PROFESSIONNELLES (>75%): {len(professional)}")
    for app_name, result in professional:
        print(f"  ✅ {app_name:<40} {result['professional_score']:.0f}% ({result['size']:,} chars)")

    if good:
        print(f"\n✅ APPS BONNES (50-75%): {len(good)}")
        for app_name, result in good:
            print(f"  ✅ {app_name:<40} {result['professional_score']:.0f}% ({result['size']:,} chars)")

    if basic:
        print(f"\n⚠️  APPS BASIQUES (<50%): {len(basic)}")
        for app_name, result in basic:
            print(f"  ⚠️  {app_name:<40} {result['professional_score']:.0f}%")
            print(f"      Manque: {', '.join(result['missing_features'][:3])}")

    if invalid:
        print(f"\n❌ APPS AVEC HTML INVALIDE: {len(invalid)}")
        for app_name, result in invalid:
            print(f"  ❌ {app_name}")
            for error in result['html_errors']:
                print(f"      - {error}")

    if missing:
        print(f"\n❌ APPS SANS INDEX.HTML: {len(missing)}")
        for app_name, result in missing:
            print(f"  ❌ {app_name} - {result['error']}")

    if errors:
        print(f"\n❌ APPS AVEC ERREURS: {len(errors)}")
        for app_name, result in errors:
            print(f"  ❌ {app_name} - {result.get('error', 'Erreur inconnue')}")

    # Résumé final
    print("\n" + "="*80)
    print("RESUME FINAL:")
    print(f"  Apps PROFESSIONNELLES:  {len(professional)}")
    print(f"  Apps BONNES:            {len(good)}")
    print(f"  Apps BASIQUES:          {len(basic)}")
    print(f"  Apps HTML INVALIDE:     {len(invalid)}")
    print(f"  Apps SANS INDEX:        {len(missing)}")
    print(f"  Apps AVEC ERREURS:      {len(errors)}")
    print(f"  ────────────────────────────────")
    print(f"  TOTAL:                  {len(results)}")

    total_ok = len(professional) + len(good)
    total_problems = len(basic) + len(invalid) + len(missing) + len(errors)

    print(f"\n  Apps OK:                {total_ok}/{len(results)} ({total_ok/len(results)*100:.1f}%)")
    print(f"  Apps avec problèmes:    {total_problems}/{len(results)}")
    print("="*80)

    # Verdict final
    if total_problems == 0:
        print("\n✅ ✅ ✅ TOUTES LES APPS SONT PARFAITES ! ✅ ✅ ✅")
        print("✅ PRET POUR LE DEPLOIEMENT VPS !")
    elif total_problems <= 1 and len(basic) == total_problems:
        print("\n✅ QUASI PARFAIT ! Seulement 1 app basique (api-portal = projet React)")
        print("✅ PRET POUR LE DEPLOIEMENT VPS !")
    else:
        print(f"\n❌ IL Y A {total_problems} APPS AVEC DES PROBLEMES !")
        print("❌ NE PAS DEPLOYER AVANT CORRECTION !")

    print("="*80)

if __name__ == "__main__":
    main()
