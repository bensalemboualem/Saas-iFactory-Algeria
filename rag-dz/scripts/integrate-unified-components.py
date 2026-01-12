#!/usr/bin/env python3
"""
Script pour intégrer les composants unifiés IAFactory dans toutes les apps.
Ajoute: CSS, JS, et les data attributes pour auto-injection du header/footer/chatbot.
"""

import os
import re
from pathlib import Path

APPS_DIR = "/opt/iafactory-rag-dz/apps"
SKIP_DIRS = ["shared", "landing", "node_modules", "school-erp", "api-packages"]

# CSS et JS à injecter
CSS_LINK = '<link rel="stylesheet" href="/apps/shared/iafactory-unified.css">'
JS_SCRIPT = '<script src="/apps/shared/iafactory-unified.js"></script>'

def has_unified_components(content):
    """Vérifie si les composants sont déjà intégrés"""
    return "iafactory-unified" in content

def inject_components(filepath):
    """Injecte les composants dans un fichier HTML"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Skip si déjà intégré
        if has_unified_components(content):
            return f"⏭️  SKIP (déjà intégré): {filepath}"
        
        # Skip si pas un vrai HTML
        if '<html' not in content.lower():
            return f"⏭️  SKIP (pas HTML): {filepath}"
        
        original = content
        
        # 1. Ajouter CSS dans <head> (avant </head>)
        if CSS_LINK not in content:
            content = re.sub(
                r'(</head>)',
                f'    {CSS_LINK}\n\\1',
                content,
                count=1,
                flags=re.IGNORECASE
            )
        
        # 2. Ajouter data-iaf-auto-init sur <html>
        if 'data-iaf-auto-init' not in content:
            content = re.sub(
                r'<html([^>]*)>',
                r'<html\1 data-iaf-auto-init>',
                content,
                count=1,
                flags=re.IGNORECASE
            )
        
        # 3. Ajouter JS avant </body>
        if JS_SCRIPT not in content:
            content = re.sub(
                r'(</body>)',
                f'    {JS_SCRIPT}\n\\1',
                content,
                count=1,
                flags=re.IGNORECASE
            )
        
        # 4. Ajouter placeholder pour header si pas de header existant
        # On cherche juste après <body>
        if 'data-iaf-header' not in content and '<header' not in content.lower():
            content = re.sub(
                r'(<body[^>]*>)',
                r'\1\n    <div data-iaf-header></div>',
                content,
                count=1,
                flags=re.IGNORECASE
            )
        
        # 5. Ajouter placeholder pour footer si pas de footer existant
        if 'data-iaf-footer' not in content and '<footer' not in content.lower():
            content = re.sub(
                r'(</body>)',
                r'    <div data-iaf-footer></div>\n\\1',
                content,
                count=1,
                flags=re.IGNORECASE
            )
        
        # Vérifier si modifié
        if content == original:
            return f"⏭️  SKIP (pas de modif): {filepath}"
        
        # Sauvegarder
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"✅ UPDATED: {filepath}"
    
    except Exception as e:
        return f"❌ ERROR: {filepath} - {str(e)}"

def main():
    print("=" * 60)
    print("🚀 IAFactory - Intégration Composants Unifiés")
    print("=" * 60)
    
    updated = 0
    skipped = 0
    errors = 0
    
    for app_dir in sorted(os.listdir(APPS_DIR)):
        # Skip certains dossiers
        if app_dir in SKIP_DIRS:
            print(f"⏭️  SKIP DIR: {app_dir}")
            continue
        
        app_path = os.path.join(APPS_DIR, app_dir)
        
        # Vérifier si c'est un dossier
        if not os.path.isdir(app_path):
            continue
        
        # Chercher index.html
        index_path = os.path.join(app_path, "index.html")
        if os.path.exists(index_path):
            result = inject_components(index_path)
            print(result)
            
            if "UPDATED" in result:
                updated += 1
            elif "ERROR" in result:
                errors += 1
            else:
                skipped += 1
    
    print("=" * 60)
    print(f"📊 RÉSULTAT:")
    print(f"   ✅ Mis à jour: {updated}")
    print(f"   ⏭️  Ignorés: {skipped}")
    print(f"   ❌ Erreurs: {errors}")
    print("=" * 60)

if __name__ == "__main__":
    main()
