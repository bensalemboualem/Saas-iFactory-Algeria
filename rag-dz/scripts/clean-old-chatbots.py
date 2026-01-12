#!/usr/bin/env python3
"""
Nettoie les anciens chatbots et garde seulement le chatbot unifié IAFactory
"""

import re
import os

APPS_DIR = "/opt/iafactory-rag-dz/apps"

def clean_old_chatbots(filepath):
    """Supprime les anciens chatbots non-unifiés"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original = content
        
        # Supprimer les anciens boutons help-btn avec toggleHelpWindow (pas IAFactory)
        # Mais garder les nouveaux iaf-chatbot-btn
        old_count = content.count('toggleHelpWindow')
        
        # Supprimer les <button class="help-btn" onclick="toggleHelpWindow()">
        content = re.sub(
            r'\s*<button\s+class="help-btn"[^>]*onclick="toggleHelpWindow\(\)"[^>]*>[^<]*</button>\s*',
            '',
            content
        )
        
        # Supprimer les div.help-window#helpWindow (anciens)
        content = re.sub(
            r'\s*<div\s+class="help-window"\s+id="helpWindow"[^>]*>.*?</div>\s*</div>\s*</div>',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Supprimer les fonctions toggleHelpWindow isolées (pas dans IAFactory)
        content = re.sub(
            r'\s*function\s+toggleHelpWindow\s*\(\)\s*\{[^}]*\}\s*',
            '',
            content
        )
        
        new_count = content.count('toggleHelpWindow')
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"✅ CLEANED: {filepath} (removed {old_count - new_count} old refs)"
        else:
            return f"⏭️  SKIP: {filepath}"
    
    except Exception as e:
        return f"❌ ERROR: {filepath} - {str(e)}"

def main():
    print("=" * 60)
    print("🧹 IAFactory - Nettoyage Anciens Chatbots")
    print("=" * 60)
    
    cleaned = 0
    
    for app_dir in sorted(os.listdir(APPS_DIR)):
        if app_dir in ["shared", "landing", "node_modules", "school-erp"]:
            continue
        
        app_path = os.path.join(APPS_DIR, app_dir)
        if not os.path.isdir(app_path):
            continue
        
        index_path = os.path.join(app_path, "index.html")
        if os.path.exists(index_path):
            result = clean_old_chatbots(index_path)
            if "CLEANED" in result:
                print(result)
                cleaned += 1
    
    print("=" * 60)
    print(f"🧹 Nettoyé: {cleaned} apps")
    print("=" * 60)

if __name__ == "__main__":
    main()
