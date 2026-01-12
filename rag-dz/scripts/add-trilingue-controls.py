#!/usr/bin/env python3
"""
Vérifie et ajoute les contrôles trilingues (lang dropdown + theme toggle) aux apps
"""

import re
import os

APPS_DIR = "/opt/iafactory-rag-dz/apps"

# Contrôles trilingues à ajouter si absents
TRILINGUE_CONTROLS = '''
<!-- IAFactory Trilingue Controls -->
<div class="iaf-controls-floating" style="position:fixed;top:20px;right:20px;z-index:9998;display:flex;gap:10px;align-items:center;">
    <div class="iaf-lang-dropdown" style="position:relative;">
        <button class="iaf-lang-btn" onclick="IAFUnified.toggleLangMenu()" 
            style="background:#667eea;color:white;border:none;padding:8px 15px;border-radius:8px;cursor:pointer;font-size:14px;display:flex;align-items:center;gap:5px;">
            🌐 <span id="current-lang-label">FR</span> ▼
        </button>
        <div class="iaf-lang-menu" id="lang-menu" 
            style="display:none;position:absolute;top:100%;right:0;background:white;border-radius:8px;box-shadow:0 4px 20px rgba(0,0,0,0.15);min-width:150px;margin-top:5px;overflow:hidden;">
            <button onclick="IAFUnified.changeLang('fr')" style="width:100%;padding:10px 15px;border:none;background:none;text-align:left;cursor:pointer;">🇫🇷 Français</button>
            <button onclick="IAFUnified.changeLang('ar')" style="width:100%;padding:10px 15px;border:none;background:none;text-align:left;cursor:pointer;">🇩🇿 العربية</button>
            <button onclick="IAFUnified.changeLang('en')" style="width:100%;padding:10px 15px;border:none;background:none;text-align:left;cursor:pointer;">🇬🇧 English</button>
        </div>
    </div>
    <button class="iaf-theme-toggle" onclick="IAFUnified.toggleTheme()" 
        style="background:#667eea;color:white;border:none;padding:8px 12px;border-radius:8px;cursor:pointer;font-size:16px;" 
        title="Toggle theme">🌓</button>
</div>
'''

def ensure_trilingue(filepath):
    """Ajoute les contrôles trilingues si absents"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Skip si déjà présent (dans header ou flottant)
        if 'iaf-lang-dropdown' in content or 'iaf-controls-floating' in content:
            return f"✅ OK: {os.path.basename(os.path.dirname(filepath))}"
        
        # Vérifier si iafactory-unified.js est inclus
        if 'iafactory-unified.js' not in content:
            return f"⚠️  NO JS: {os.path.basename(os.path.dirname(filepath))}"
        
        # Ajouter après <body> ou au début du body
        if '<body' in content:
            # Trouver la fin du tag body
            body_match = re.search(r'<body[^>]*>', content)
            if body_match:
                insert_pos = body_match.end()
                content = content[:insert_pos] + '\n' + TRILINGUE_CONTROLS + content[insert_pos:]
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"🔧 ADDED: {os.path.basename(os.path.dirname(filepath))}"
        
        return f"❌ NO BODY: {os.path.basename(os.path.dirname(filepath))}"
    
    except Exception as e:
        return f"❌ ERROR: {os.path.basename(os.path.dirname(filepath))} - {str(e)}"

def main():
    print("=" * 60)
    print("🌐 IAFactory - Ajout Contrôles Trilingues")
    print("=" * 60)
    
    results = {"ok": 0, "added": 0, "no_js": 0, "error": 0}
    added_apps = []
    
    for app_dir in sorted(os.listdir(APPS_DIR)):
        if app_dir in ["shared", "landing", "node_modules", "school-erp"]:
            continue
        
        app_path = os.path.join(APPS_DIR, app_dir)
        if not os.path.isdir(app_path):
            continue
        
        index_path = os.path.join(app_path, "index.html")
        if os.path.exists(index_path):
            result = ensure_trilingue(index_path)
            
            if "ADDED" in result:
                print(result)
                results["added"] += 1
                added_apps.append(app_dir)
            elif "OK" in result:
                results["ok"] += 1
            elif "NO JS" in result:
                results["no_js"] += 1
            else:
                results["error"] += 1
                print(result)
    
    print("=" * 60)
    print(f"🌐 Résultats: OK={results['ok']} | Ajouté={results['added']} | Sans JS={results['no_js']} | Erreur={results['error']}")
    if added_apps:
        print(f"   Apps modifiées: {', '.join(added_apps)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
