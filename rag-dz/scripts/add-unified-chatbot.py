#!/usr/bin/env python3
"""
Assure que toutes les apps ont le chatbot IAFactory unifié
Ajoute le bouton chatbot si absent
"""

import re
import os

APPS_DIR = "/opt/iafactory-rag-dz/apps"

CHATBOT_BTN = '''
<!-- IAFactory Unified Chatbot -->
<button class="iaf-chatbot-btn" onclick="IAFUnified.toggleChatbot()" title="Aide" aria-label="Aide">
    💬
</button>
'''

def ensure_chatbot(filepath):
    """Ajoute le bouton chatbot si absent"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Skip si déjà présent
        if 'iaf-chatbot-btn' in content or 'IAFUnified.toggleChatbot' in content:
            return f"✅ OK: {filepath}"
        
        # Vérifier si iafactory-unified.js est inclus
        if 'iafactory-unified.js' not in content:
            return f"⚠️  NO JS: {filepath}"
        
        # Ajouter avant </body>
        if '</body>' in content:
            content = content.replace('</body>', f'{CHATBOT_BTN}\n</body>')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"🔧 ADDED: {filepath}"
        
        return f"❌ NO BODY: {filepath}"
    
    except Exception as e:
        return f"❌ ERROR: {filepath} - {str(e)}"

def main():
    print("=" * 60)
    print("💬 IAFactory - Ajout Chatbot Unifié")
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
            result = ensure_chatbot(index_path)
            if "ADDED" in result:
                print(result)
                added += 1
            elif "OK" in result:
                ok += 1
    
    print("=" * 60)
    print(f"💬 OK: {ok} | Ajouté: {added}")
    print("=" * 60)

if __name__ == "__main__":
    main()
