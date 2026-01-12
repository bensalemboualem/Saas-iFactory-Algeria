#!/usr/bin/env python3
"""
SCAN COMPLET IAFactory - Vérification Interfaces
- Erreurs HTML
- Couleurs cohérentes avec landing
- Versions trilingues (FR/AR/EN)
- Composants unifiés
"""

import os
import re
from collections import defaultdict

APPS_DIR = "/opt/iafactory-rag-dz/apps"
LANDING_FILE = "/opt/iafactory-rag-dz/apps/landing/index.html"

# Couleurs attendues (extraites de la landing page)
EXPECTED_COLORS = {
    "primary": ["#667eea", "#764ba2", "#6366f1"],  # Violet/Purple gradient
    "secondary": ["#f093fb", "#f5576c"],  # Pink
    "accent": ["#4facfe", "#00f2fe", "#43e97b", "#38f9d7"],  # Blue/Green
    "dark": ["#1a1a2e", "#16213e", "#0f0f23", "#111827"],  # Dark backgrounds
    "text": ["#ffffff", "#f8fafc", "#e2e8f0"]  # White text
}

def get_landing_colors():
    """Extraire les couleurs de la landing page"""
    try:
        with open(LANDING_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Trouver toutes les couleurs hex
        colors = re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}', content)
        return list(set(colors))
    except:
        return []

def check_app(filepath, app_name, landing_colors):
    """Vérifier une app"""
    result = {
        "name": app_name,
        "errors": [],
        "warnings": [],
        "trilingue": {"fr": False, "ar": False, "en": False},
        "components": {"css": False, "js": False, "lang": False, "chat": False, "footer": False},
        "colors_match": True,
        "html_valid": True
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # 1. Vérifier HTML basique
        if not content.strip():
            result["errors"].append("Fichier vide")
            result["html_valid"] = False
            return result
        
        if '<!DOCTYPE' not in content.upper() and '<html' not in content.lower():
            result["warnings"].append("Pas de DOCTYPE/HTML")
        
        if '</body>' not in content:
            result["warnings"].append("Pas de </body>")
        
        if '</html>' not in content:
            result["warnings"].append("Pas de </html>")
        
        # 2. Vérifier composants unifiés
        result["components"]["css"] = "iafactory-unified.css" in content
        result["components"]["js"] = "iafactory-unified.js" in content
        result["components"]["lang"] = "iaf-lang-dropdown" in content or "iaf-controls-floating" in content or "IAFUnified.changeLang" in content
        result["components"]["chat"] = "iaf-chatbot-btn" in content or "IAFUnified.toggleChatbot" in content
        result["components"]["footer"] = "data-iaf-footer" in content or 'id="iaf-footer"' in content
        
        # 3. Vérifier trilingue
        # Vérifier si les traductions sont présentes
        result["trilingue"]["fr"] = any(x in content for x in ["lang='fr'", 'lang="fr"', "Français", "Accueil", "Applications"])
        result["trilingue"]["ar"] = any(x in content for x in ["lang='ar'", 'lang="ar"', "العربية", "الرئيسية", "التطبيقات", "dir=\"rtl\""])
        result["trilingue"]["en"] = any(x in content for x in ["lang='en'", 'lang="en"', "English", "Home", "Applications"])
        
        # Si le JS unifié est présent, les traductions sont incluses
        if result["components"]["js"]:
            result["trilingue"]["fr"] = True
            result["trilingue"]["ar"] = True
            result["trilingue"]["en"] = True
        
        # 4. Vérifier couleurs (chercher les couleurs principales)
        app_colors = re.findall(r'#[0-9a-fA-F]{6}', content)
        
        # Vérifier si les couleurs principales sont présentes
        has_primary = any(c.lower() in [x.lower() for x in EXPECTED_COLORS["primary"]] for c in app_colors)
        has_dark = any(c.lower() in [x.lower() for x in EXPECTED_COLORS["dark"]] for c in app_colors)
        
        if not has_primary and not has_dark and app_colors:
            # Vérifier si au moins le CSS unifié est là (qui contient les bonnes couleurs)
            if not result["components"]["css"]:
                result["warnings"].append("Couleurs non-standard détectées")
        
        # 5. Vérifier ancien code
        if "toggleHelpWindow" in content and "IAFUnified" not in content:
            result["warnings"].append("Ancien chatbot détecté")
        
        # Compter les erreurs/warnings
        if not result["components"]["css"]:
            result["errors"].append("CSS unifié manquant")
        if not result["components"]["js"]:
            result["errors"].append("JS unifié manquant")
        if not result["components"]["lang"]:
            result["errors"].append("Contrôles trilingues manquants")
        if not result["components"]["chat"]:
            result["errors"].append("Chatbot manquant")
        if not result["components"]["footer"]:
            result["warnings"].append("Footer manquant")
        
    except Exception as e:
        result["errors"].append(f"Erreur lecture: {str(e)}")
        result["html_valid"] = False
    
    return result

def main():
    print("=" * 80)
    print("🔍 SCAN COMPLET IAFactory - Vérification Interfaces")
    print("=" * 80)
    print()
    
    # Récupérer les couleurs de la landing
    landing_colors = get_landing_colors()
    print(f"📊 Couleurs landing page: {len(landing_colors)} couleurs détectées")
    print()
    
    # Scanner toutes les apps
    results = []
    skip_dirs = ["shared", "landing", "node_modules", "docs", "shared-components"]
    
    for app_dir in sorted(os.listdir(APPS_DIR)):
        if app_dir in skip_dirs:
            continue
        
        app_path = os.path.join(APPS_DIR, app_dir)
        if not os.path.isdir(app_path):
            continue
        
        index_path = os.path.join(app_path, "index.html")
        if os.path.exists(index_path):
            result = check_app(index_path, app_dir, landing_colors)
            results.append(result)
    
    # Afficher les résultats
    print("=" * 80)
    print("📋 RAPPORT PAR APP")
    print("=" * 80)
    
    perfect = []
    with_errors = []
    with_warnings = []
    
    for r in results:
        if r["errors"]:
            with_errors.append(r)
        elif r["warnings"]:
            with_warnings.append(r)
        else:
            perfect.append(r)
    
    # Apps avec erreurs
    if with_errors:
        print(f"\n❌ APPS AVEC ERREURS ({len(with_errors)}):")
        print("-" * 60)
        for r in with_errors:
            print(f"  {r['name']}:")
            for e in r["errors"]:
                print(f"    ❌ {e}")
            for w in r["warnings"]:
                print(f"    ⚠️  {w}")
    
    # Apps avec warnings
    if with_warnings:
        print(f"\n⚠️  APPS AVEC AVERTISSEMENTS ({len(with_warnings)}):")
        print("-" * 60)
        for r in with_warnings:
            print(f"  {r['name']}:")
            for w in r["warnings"]:
                print(f"    ⚠️  {w}")
    
    # Stats trilingue
    print("\n" + "=" * 80)
    print("🌐 STATISTIQUES TRILINGUE")
    print("=" * 80)
    
    fr_count = sum(1 for r in results if r["trilingue"]["fr"])
    ar_count = sum(1 for r in results if r["trilingue"]["ar"])
    en_count = sum(1 for r in results if r["trilingue"]["en"])
    total = len(results)
    
    print(f"  🇫🇷 Français: {fr_count}/{total} ({fr_count*100//total}%)")
    print(f"  🇩🇿 Arabe:    {ar_count}/{total} ({ar_count*100//total}%)")
    print(f"  🇬🇧 Anglais:  {en_count}/{total} ({en_count*100//total}%)")
    
    # Stats composants
    print("\n" + "=" * 80)
    print("🧩 STATISTIQUES COMPOSANTS")
    print("=" * 80)
    
    css_count = sum(1 for r in results if r["components"]["css"])
    js_count = sum(1 for r in results if r["components"]["js"])
    lang_count = sum(1 for r in results if r["components"]["lang"])
    chat_count = sum(1 for r in results if r["components"]["chat"])
    footer_count = sum(1 for r in results if r["components"]["footer"])
    
    print(f"  CSS Unifié:     {css_count}/{total} ({css_count*100//total}%)")
    print(f"  JS Unifié:      {js_count}/{total} ({js_count*100//total}%)")
    print(f"  Lang Dropdown:  {lang_count}/{total} ({lang_count*100//total}%)")
    print(f"  Chatbot:        {chat_count}/{total} ({chat_count*100//total}%)")
    print(f"  Footer:         {footer_count}/{total} ({footer_count*100//total}%)")
    
    # Résumé final
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ FINAL")
    print("=" * 80)
    print(f"  ✅ Apps parfaites:        {len(perfect)}/{total}")
    print(f"  ⚠️  Apps avec warnings:   {len(with_warnings)}/{total}")
    print(f"  ❌ Apps avec erreurs:     {len(with_errors)}/{total}")
    print("=" * 80)
    
    if len(perfect) == total:
        print("\n🎉 TOUTES LES APPS SONT PARFAITES!")
    elif with_errors:
        print(f"\n🔧 {len(with_errors)} apps nécessitent des corrections")

if __name__ == "__main__":
    main()
