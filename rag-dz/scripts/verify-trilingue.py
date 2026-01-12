#!/usr/bin/env python3
"""
TRIPLE VÉRIFICATION - IAFactory Trilingue SaaS
Vérifie que toutes les apps ont:
1. iafactory-unified.css
2. iafactory-unified.js  
3. iaf-lang-dropdown (trilingue)
4. iaf-chatbot-btn (aide)
5. PAS d'ancien chatbot (toggleHelpWindow)
"""

import os
import re

APPS_DIR = "/opt/iafactory-rag-dz/apps"

def verify_app(filepath, app_name):
    """Vérifie une app"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        checks = {
            "CSS": "iafactory-unified.css" in content,
            "JS": "iafactory-unified.js" in content,
            "Lang": "iaf-lang-dropdown" in content or "iaf-controls-floating" in content,
            "Chat": "iaf-chatbot-btn" in content or "IAFUnified.toggleChatbot" in content,
            "NoOld": "toggleHelpWindow" not in content
        }
        
        all_ok = all(checks.values())
        
        if not all_ok:
            missing = [k for k, v in checks.items() if not v]
            return f"❌ {app_name}: MISSING {', '.join(missing)}"
        
        return f"✅ {app_name}: OK"
    
    except Exception as e:
        return f"⚠️  {app_name}: ERROR - {str(e)}"

def main():
    print("=" * 70)
    print("🔍 TRIPLE VÉRIFICATION - IAFactory Trilingue SaaS")
    print("=" * 70)
    print()
    
    ok_count = 0
    fail_count = 0
    apps_ko = []
    
    for app_dir in sorted(os.listdir(APPS_DIR)):
        if app_dir in ["shared", "landing", "node_modules", "school-erp"]:
            continue
        
        app_path = os.path.join(APPS_DIR, app_dir)
        if not os.path.isdir(app_path):
            continue
        
        index_path = os.path.join(app_path, "index.html")
        if os.path.exists(index_path):
            result = verify_app(index_path, app_dir)
            
            if "OK" in result:
                ok_count += 1
            else:
                fail_count += 1
                apps_ko.append(result)
                print(result)
    
    print()
    print("=" * 70)
    print(f"📊 RÉSULTAT: ✅ {ok_count} OK | ❌ {fail_count} KO")
    print("=" * 70)
    
    if apps_ko:
        print("\n🔧 APPS À CORRIGER:")
        for app in apps_ko:
            print(f"   {app}")
    else:
        print("\n🎉 TOUTES LES APPS SONT TRILINGUES ET COMPLÈTES!")
    
    print()
    
    # Vérification spécifique des 3 apps clés
    print("=" * 70)
    print("🔑 VÉRIFICATION DES 3 APPS CLÉS")
    print("=" * 70)
    
    key_apps = ["creative-studio", "council", "pme-copilot"]
    for app in key_apps:
        index_path = os.path.join(APPS_DIR, app, "index.html")
        if os.path.exists(index_path):
            result = verify_app(index_path, app)
            print(result)
        else:
            print(f"⚠️  {app}: NOT FOUND")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
