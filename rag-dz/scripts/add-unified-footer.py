#!/usr/bin/env python3
"""
Ajoute le footer unifié IAFactory aux apps qui n'en ont pas
"""

import os
import re

APPS_DIR = "/opt/iafactory-rag-dz/apps"

FOOTER_DIV = '<div data-iaf-footer></div>'

def add_footer(filepath, app_name):
    """Ajoute le footer si manquant"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Skip si déjà présent
        if 'data-iaf-footer' in content or 'id="iaf-footer"' in content:
            return f"✅ OK: {app_name}"
        
        # Ajouter avant </body>
        if '</body>' in content:
            # Trouver le </body> et ajouter le footer juste avant
            content = content.replace('</body>', f'{FOOTER_DIV}\n</body>')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"🔧 ADDED: {app_name}"
        
        return f"⚠️  NO BODY: {app_name}"
    
    except Exception as e:
        return f"❌ ERROR: {app_name} - {str(e)}"

def main():
    print("=" * 60)
    print("📄 IAFactory - Ajout Footer Unifié")
    print("=" * 60)
    
    added = 0
    ok = 0
    
    for app_dir in sorted(os.listdir(APPS_DIR)):
        if app_dir in ["shared", "landing", "node_modules", "school-erp"]:
            continue
        
        app_path = os.path.join(APPS_DIR, app_dir)
        if not os.path.isdir(app_path):
            continue
        
        index_path = os.path.join(app_path, "index.html")
        if os.path.exists(index_path):
            result = add_footer(index_path, app_dir)
            if "ADDED" in result:
                print(result)
                added += 1
            elif "OK" in result:
                ok += 1
            else:
                print(result)
    
    print("=" * 60)
    print(f"📄 Résultat: OK={ok} | Ajouté={added}")
    print("=" * 60)

if __name__ == "__main__":
    main()
