#!/usr/bin/env python3
"""
RÉPARATION COMPLÈTE IAFactory - Toutes les apps
Ajoute:
1. CSS unifié
2. JS unifié  
3. Contrôles trilingues (FR/AR/EN)
4. Chatbot
5. Footer
"""

import os
import re

APPS_DIR = "/opt/iafactory-rag-dz/apps"

CSS_LINK = '<link rel="stylesheet" href="/apps/shared/iafactory-unified.css">'
JS_LINK = '<script src="/apps/shared/iafactory-unified.js"></script>'

CHATBOT_BTN = '''<!-- IAFactory Chatbot -->
<button class="iaf-chatbot-btn" onclick="IAFUnified.toggleChatbot()" title="Aide" aria-label="Aide">💬</button>'''

TRILINGUE_CONTROLS = '''<!-- IAFactory Trilingue Controls -->
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
</div>'''

FOOTER_DIV = '<div data-iaf-footer></div>'

def fix_app_complete(filepath, app_name):
    """Répare complètement une app"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original = content
        fixes = []
        
        # 1. Ajouter CSS si manquant
        if "iafactory-unified.css" not in content:
            if '</head>' in content:
                content = content.replace('</head>', f'{CSS_LINK}\n</head>')
                fixes.append("CSS")
            elif '<head>' in content:
                content = content.replace('<head>', f'<head>\n{CSS_LINK}')
                fixes.append("CSS")
            elif '<html' in content.lower():
                # Ajouter après <html>
                html_match = re.search(r'<html[^>]*>', content, re.IGNORECASE)
                if html_match:
                    insert_pos = html_match.end()
                    content = content[:insert_pos] + f'\n<head>\n{CSS_LINK}\n</head>' + content[insert_pos:]
                    fixes.append("CSS+HEAD")
        
        # 2. S'assurer qu'il y a un </body>
        if '</body>' not in content and '</html>' in content:
            content = content.replace('</html>', '</body>\n</html>')
            fixes.append("BODY")
        
        # 3. Ajouter JS si manquant (avant </body>)
        if "iafactory-unified.js" not in content:
            if '</body>' in content:
                content = content.replace('</body>', f'{JS_LINK}\n</body>')
                fixes.append("JS")
        
        # 4. Ajouter contrôles trilingues si manquants
        if "iaf-lang-dropdown" not in content and "iaf-controls-floating" not in content:
            body_match = re.search(r'<body[^>]*>', content, re.IGNORECASE)
            if body_match:
                insert_pos = body_match.end()
                content = content[:insert_pos] + '\n' + TRILINGUE_CONTROLS + content[insert_pos:]
                fixes.append("Lang")
        
        # 5. Ajouter chatbot si manquant
        if "iaf-chatbot-btn" not in content and "IAFUnified.toggleChatbot" not in content:
            if '</body>' in content:
                content = content.replace('</body>', f'{CHATBOT_BTN}\n</body>')
                fixes.append("Chat")
        
        # 6. Ajouter footer si manquant
        if "data-iaf-footer" not in content and 'id="iaf-footer"' not in content:
            if '</body>' in content:
                content = content.replace('</body>', f'{FOOTER_DIV}\n</body>')
                fixes.append("Footer")
        
        # 7. Supprimer ancien chatbot
        if "toggleHelpWindow" in content and "IAFUnified" in content:
            # Supprimer les anciennes fonctions toggleHelpWindow non-IAF
            content = re.sub(
                r'\s*<button\s+class="help-btn"[^>]*onclick="toggleHelpWindow\(\)"[^>]*>[^<]*</button>\s*',
                '',
                content
            )
            content = re.sub(
                r'\s*function\s+toggleHelpWindow\s*\(\)\s*\{[^}]*\}\s*',
                '',
                content
            )
            fixes.append("CleanOld")
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"🔧 FIXED {app_name}: {', '.join(fixes)}"
        
        return f"✅ OK: {app_name}"
    
    except Exception as e:
        return f"❌ ERROR {app_name}: {str(e)}"

def main():
    print("=" * 70)
    print("🔧 RÉPARATION COMPLÈTE IAFactory - Toutes les Apps")
    print("=" * 70)
    
    fixed = 0
    ok = 0
    errors = 0
    skip_dirs = ["shared", "landing", "node_modules", "docs", "shared-components"]
    
    for app_dir in sorted(os.listdir(APPS_DIR)):
        if app_dir in skip_dirs:
            continue
        
        app_path = os.path.join(APPS_DIR, app_dir)
        if not os.path.isdir(app_path):
            continue
        
        index_path = os.path.join(app_path, "index.html")
        if os.path.exists(index_path):
            result = fix_app_complete(index_path, app_dir)
            
            if "FIXED" in result:
                print(result)
                fixed += 1
            elif "OK" in result:
                ok += 1
            else:
                print(result)
                errors += 1
    
    print("=" * 70)
    print(f"📊 Résultat: ✅ OK={ok} | 🔧 Réparé={fixed} | ❌ Erreur={errors}")
    print("=" * 70)

if __name__ == "__main__":
    main()
