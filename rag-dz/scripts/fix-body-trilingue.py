#!/usr/bin/env python3
"""
FIX BODY TAG - Ajoute <body> aux apps qui n'en ont pas
et ajoute les contrôles trilingues
"""

import os
import re

APPS_DIR = "/opt/iafactory-rag-dz/apps"

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

def fix_body_and_lang(filepath, app_name):
    """Ajoute body et contrôles trilingues si manquants"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original = content
        fixes = []
        
        # Vérifier si contrôles trilingues manquants
        if "iaf-lang-dropdown" in content or "iaf-controls-floating" in content:
            return f"✅ OK: {app_name}"
        
        # Chercher </head> et ajouter <body> après
        if '</head>' in content and '<body' not in content.lower():
            # Ajouter <body> après </head>
            content = content.replace('</head>', '</head>\n<body>')
            fixes.append("BODY_OPEN")
        
        # Maintenant ajouter les contrôles après <body>
        body_match = re.search(r'<body[^>]*>', content, re.IGNORECASE)
        if body_match:
            insert_pos = body_match.end()
            content = content[:insert_pos] + '\n' + TRILINGUE_CONTROLS + content[insert_pos:]
            fixes.append("Lang")
        elif '</head>' in content:
            # Pas de body, ajouter après </head>
            content = content.replace('</head>', f'</head>\n<body>\n{TRILINGUE_CONTROLS}')
            fixes.append("Body+Lang")
        
        # Ajouter </body> avant </html> si manquant
        if '</body>' not in content and '</html>' in content:
            content = content.replace('</html>', '</body>\n</html>')
            fixes.append("BODY_CLOSE")
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"🔧 FIXED {app_name}: {', '.join(fixes)}"
        
        return f"⏭️  SKIP: {app_name}"
    
    except Exception as e:
        return f"❌ ERROR {app_name}: {str(e)}"

def main():
    print("=" * 60)
    print("🔧 FIX BODY + TRILINGUE")
    print("=" * 60)
    
    # Liste des apps problématiques
    problem_apps = [
        "agri-dz", "api-portal", "billing-panel", "chatbot-ia",
        "crm-ia-ui", "data-dz", "data-dz-dashboard", "dev-portal",
        "dzirvideo-ai", "fiscal-assistant", "legal-assistant", "med-dz",
        "pme-copilot-ui", "pmedz-sales", "pmedz-sales-ui", "prof-dz",
        "seo-dz", "seo-dz-boost", "startupdz-onboarding", "voice-assistant"
    ]
    
    fixed = 0
    
    for app_dir in problem_apps:
        app_path = os.path.join(APPS_DIR, app_dir)
        index_path = os.path.join(app_path, "index.html")
        
        if os.path.exists(index_path):
            result = fix_body_and_lang(index_path, app_dir)
            print(result)
            if "FIXED" in result:
                fixed += 1
    
    print("=" * 60)
    print(f"🔧 Apps réparées: {fixed}")
    print("=" * 60)

if __name__ == "__main__":
    main()
