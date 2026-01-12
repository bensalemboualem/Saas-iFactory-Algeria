#!/usr/bin/env python3
"""
Ajoute les composants trilingues IAFactory aux pages docs
"""

import os
import re

DOCS_DIR = "/opt/iafactory-rag-dz/docs"

CSS_LINK = '<link rel="stylesheet" href="/apps/shared/iafactory-unified.css">'
JS_LINK = '<script src="/apps/shared/iafactory-unified.js"></script>'

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
</div>
'''

CHATBOT_BTN = '''<!-- IAFactory Chatbot -->
<button class="iaf-chatbot-btn" onclick="IAFUnified.toggleChatbot()" title="Aide" aria-label="Aide">💬</button>'''

FOOTER_DIV = '<div data-iaf-footer></div>'

def fix_doc(filepath):
    """Ajoute les composants trilingues à un doc HTML"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original = content
        fixes = []
        name = os.path.basename(filepath)
        
        # Skip si déjà trilingue
        if "iafactory-unified.js" in content and "iaf-lang" in content:
            return f"✅ OK: {name}"
        
        # 1. Ajouter CSS si manquant
        if "iafactory-unified.css" not in content:
            if '</head>' in content:
                content = content.replace('</head>', f'{CSS_LINK}\n</head>')
                fixes.append("CSS")
        
        # 2. Ajouter </body> si manquant
        if '</body>' not in content and '</html>' in content:
            content = content.replace('</html>', '</body>\n</html>')
            fixes.append("BODY")
        
        # 3. Ajouter JS si manquant
        if "iafactory-unified.js" not in content:
            if '</body>' in content:
                content = content.replace('</body>', f'{JS_LINK}\n</body>')
                fixes.append("JS")
            elif '</html>' in content:
                content = content.replace('</html>', f'{JS_LINK}\n</html>')
                fixes.append("JS")
        
        # 4. Ajouter contrôles trilingues
        if "iaf-lang-dropdown" not in content and "iaf-controls-floating" not in content:
            body_match = re.search(r'<body[^>]*>', content, re.IGNORECASE)
            if body_match:
                insert_pos = body_match.end()
                content = content[:insert_pos] + '\n' + TRILINGUE_CONTROLS + content[insert_pos:]
                fixes.append("Lang")
            elif '</head>' in content:
                # Ajouter après </head> avec body
                content = content.replace('</head>', f'</head>\n<body>\n{TRILINGUE_CONTROLS}')
                fixes.append("Body+Lang")
        
        # 5. Ajouter chatbot
        if "iaf-chatbot-btn" not in content:
            if '</body>' in content:
                content = content.replace('</body>', f'{CHATBOT_BTN}\n</body>')
                fixes.append("Chat")
        
        # 6. Ajouter footer
        if "data-iaf-footer" not in content:
            if '</body>' in content:
                content = content.replace('</body>', f'{FOOTER_DIV}\n</body>')
                fixes.append("Footer")
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"🔧 FIXED {name}: {', '.join(fixes)}"
        
        return f"⏭️  SKIP: {name}"
    
    except Exception as e:
        return f"❌ ERROR {os.path.basename(filepath)}: {str(e)}"

def main():
    print("=" * 60)
    print("📚 FIX DOCS TRILINGUE")
    print("=" * 60)
    
    fixed = 0
    
    for filename in sorted(os.listdir(DOCS_DIR)):
        if filename.endswith('.html'):
            filepath = os.path.join(DOCS_DIR, filename)
            result = fix_doc(filepath)
            print(result)
            if "FIXED" in result:
                fixed += 1
    
    print("=" * 60)
    print(f"📚 Docs réparés: {fixed}")
    print("=" * 60)

if __name__ == "__main__":
    main()
