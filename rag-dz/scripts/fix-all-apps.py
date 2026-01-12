#!/usr/bin/env python3
"""
FIX COMPLET - Ajoute tous les composants manquants aux apps
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

def fix_app(filepath, app_name):
    """Répare une app"""
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
            body_match = re.search(r'<body[^>]*>', content)
            if body_match:
                insert_pos = body_match.end()
                content = content[:insert_pos] + '\n' + TRILINGUE_CONTROLS + content[insert_pos:]
                fixes.append("Lang")
        
        # 5. Ajouter chatbot si manquant
        if "iaf-chatbot-btn" not in content and "IAFUnified.toggleChatbot" not in content:
            if '</body>' in content:
                content = content.replace('</body>', f'{CHATBOT_BTN}\n</body>')
                fixes.append("Chat")
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"🔧 FIXED {app_name}: {', '.join(fixes)}"
        
        return f"✅ OK: {app_name}"
    
    except Exception as e:
        return f"❌ ERROR {app_name}: {str(e)}"

def main():
    print("=" * 60)
    print("🔧 FIX COMPLET - IAFactory Trilingue")
    print("=" * 60)
    
    fixed = 0
    
    for app_dir in sorted(os.listdir(APPS_DIR)):
        if app_dir in ["shared", "landing", "node_modules", "school-erp"]:
            continue
        
        app_path = os.path.join(APPS_DIR, app_dir)
        if not os.path.isdir(app_path):
            continue
        
        index_path = os.path.join(app_path, "index.html")
        if os.path.exists(index_path):
            result = fix_app(index_path, app_dir)
            if "FIXED" in result:
                print(result)
                fixed += 1
    
    print("=" * 60)
    print(f"🔧 Apps réparées: {fixed}")
    print("=" * 60)

if __name__ == "__main__":
    main()
