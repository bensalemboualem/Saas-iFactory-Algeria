#!/usr/bin/env python3
"""
Script de migration des apps vers theme.css unifié
IAFactory Algeria - 18/12/2025
"""

import os
import re
from pathlib import Path

APPS_DIR = Path(__file__).parent.parent / "apps"
THEME_CSS_LINK = '<link rel="stylesheet" href="../../shared/theme.css">'

# Apps avec styles inline à migrer
APPS_TO_MIGRATE = [
    "agri-dz", "agroalimentaire-dz", "btp-dz", "clinique-dz", 
    "commerce-dz", "council", "douanes-dz", "ecommerce-dz",
    "expert-comptable-dz", "formation-pro-dz", "industrie-dz", 
    "irrigation-dz", "pharma-dz", "transport-dz", "universite-dz",
    "developer"
]

def migrate_app(app_name: str) -> dict:
    """Migre une app vers theme.css"""
    app_path = APPS_DIR / app_name / "index.html"
    result = {"app": app_name, "status": "skipped", "changes": []}
    
    if not app_path.exists():
        result["status"] = "no_index"
        return result
    
    content = app_path.read_text(encoding="utf-8")
    original = content
    
    # 1. Vérifier si déjà migré
    if "../../shared/theme.css" in content:
        result["status"] = "already_migrated"
        return result
    
    # 2. Ajouter le lien vers theme.css après la balise title
    if THEME_CSS_LINK not in content:
        content = re.sub(
            r'(</title>)',
            f'\\1\n    {THEME_CSS_LINK}',
            content
        )
        result["changes"].append("Added theme.css link")
    
    # 3. Remplacer data-theme="dark" par class sur body (ou supprimer)
    content = re.sub(r'<html([^>]*) data-theme="dark"', '<html\\1', content)
    content = re.sub(r'<html([^>]*) data-theme="light"', '<html\\1', content)
    
    # 4. Commenter les variables CSS inline (ne pas supprimer pour backup)
    # Trouver et commenter le bloc :root inline
    pattern = r'(:root,?\s*\[data-theme="dark"\]\s*\{[^}]+\})'
    if re.search(pattern, content):
        content = re.sub(pattern, '/* MIGRATED TO theme.css - \\1 */', content)
        result["changes"].append("Commented :root dark mode variables")
    
    pattern = r'(\[data-theme="light"\]\s*\{[^}]+\})'
    if re.search(pattern, content):
        content = re.sub(pattern, '/* MIGRATED TO theme.css - \\1 */', content)
        result["changes"].append("Commented light mode variables")
    
    # 5. Mettre à jour le toggle theme JS
    old_toggle = 'document.documentElement.getAttribute("data-theme")'
    new_toggle = 'document.body.classList.contains("light-theme")'
    if old_toggle in content:
        content = content.replace(old_toggle, new_toggle)
        result["changes"].append("Updated theme toggle check")
    
    old_set = 'document.documentElement.setAttribute("data-theme"'
    if old_set in content:
        # Remplacer par classList.toggle
        content = re.sub(
            r'document\.documentElement\.setAttribute\("data-theme",\s*"dark"\)',
            'document.body.classList.remove("light-theme")',
            content
        )
        content = re.sub(
            r'document\.documentElement\.setAttribute\("data-theme",\s*"light"\)',
            'document.body.classList.add("light-theme")',
            content
        )
        result["changes"].append("Updated theme toggle setter")
    
    # 6. Sauvegarder si modifié
    if content != original:
        app_path.write_text(content, encoding="utf-8")
        result["status"] = "migrated"
    else:
        result["status"] = "no_changes"
    
    return result

def main():
    print("=" * 60)
    print("🔄 Migration des apps vers theme.css unifié")
    print("=" * 60)
    
    results = {"migrated": 0, "skipped": 0, "errors": 0}
    
    for app in APPS_TO_MIGRATE:
        result = migrate_app(app)
        
        if result["status"] == "migrated":
            print(f"✅ {app}: Migré ({', '.join(result['changes'])})")
            results["migrated"] += 1
        elif result["status"] == "already_migrated":
            print(f"⏭️  {app}: Déjà migré")
            results["skipped"] += 1
        elif result["status"] == "no_index":
            print(f"❌ {app}: Pas de index.html")
            results["errors"] += 1
        else:
            print(f"⚠️  {app}: {result['status']}")
    
    print("\n" + "=" * 60)
    print(f"📊 Résultats: {results['migrated']} migrés, {results['skipped']} déjà OK, {results['errors']} erreurs")
    print("=" * 60)

if __name__ == "__main__":
    main()
