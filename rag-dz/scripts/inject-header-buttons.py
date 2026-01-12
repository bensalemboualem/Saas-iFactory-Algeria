#!/usr/bin/env python3
"""
Script pour ajouter les boutons langue/thème dans les headers existants
des applications IAFactory.
"""

import os
import re

APPS_DIR = "/opt/iafactory-rag-dz/apps"
SKIP_DIRS = ["shared", "landing", "node_modules", "school-erp", "api-packages"]

# Boutons à injecter dans le header
LANG_THEME_BUTTONS = '''
                <!-- IAF Unified Controls -->
                <div class="iaf-header-actions" style="display:flex;align-items:center;gap:0.5rem;margin-left:auto;">
                    <div class="iaf-lang-dropdown" style="position:relative;">
                        <button class="iaf-lang-btn" onclick="IAFactory.toggleLangMenu()" style="display:flex;align-items:center;gap:0.5rem;padding:0.5rem 0.75rem;border-radius:8px;border:1px solid rgba(255,255,255,0.1);background:transparent;color:inherit;cursor:pointer;font-size:0.85rem;">
                            🌐 <span id="iaf-current-lang">FR</span>
                        </button>
                        <div class="iaf-lang-menu" id="iaf-lang-menu" style="position:absolute;top:100%;right:0;margin-top:4px;background:var(--bg-card,#1a1a2e);border:1px solid rgba(255,255,255,0.1);border-radius:12px;box-shadow:0 15px 30px rgba(0,0,0,0.3);display:none;min-width:150px;z-index:1001;overflow:hidden;">
                            <button class="iaf-lang-option" onclick="IAFactory.setLanguage('fr')" style="display:flex;align-items:center;gap:0.5rem;width:100%;padding:0.75rem 1rem;border:none;background:transparent;color:inherit;cursor:pointer;text-align:left;">🇫🇷 Français</button>
                            <button class="iaf-lang-option" onclick="IAFactory.setLanguage('en')" style="display:flex;align-items:center;gap:0.5rem;width:100%;padding:0.75rem 1rem;border:none;background:transparent;color:inherit;cursor:pointer;text-align:left;">🇬🇧 English</button>
                            <button class="iaf-lang-option" onclick="IAFactory.setLanguage('ar')" style="display:flex;align-items:center;gap:0.5rem;width:100%;padding:0.75rem 1rem;border:none;background:transparent;color:inherit;cursor:pointer;text-align:left;">🇩🇿 العربية</button>
                        </div>
                    </div>
                    <button class="iaf-theme-btn" onclick="IAFactory.toggleTheme()" id="iaf-theme-btn" style="width:40px;height:40px;border-radius:10px;border:1px solid rgba(255,255,255,0.1);background:transparent;color:inherit;cursor:pointer;font-size:1.1rem;">☀️</button>
                </div>
'''

# Chatbot HTML
CHATBOT_HTML = '''
    <!-- IAF Chatbot Help -->
    <div class="iaf-chatbot" style="position:fixed;bottom:24px;right:24px;z-index:9999;">
        <button class="iaf-chatbot-btn" onclick="IAFactory.toggleChatbot()" style="width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,#00a651,#00d66a);border:none;cursor:pointer;color:white;font-size:24px;box-shadow:0 4px 20px rgba(0,166,81,0.4);">💬</button>
    </div>
    <div class="iaf-chatbot-window" id="iaf-chatbot-window" style="position:fixed;bottom:100px;right:24px;width:380px;height:520px;background:var(--bg-card,#1a1a2e);border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,0.4);display:none;flex-direction:column;z-index:9998;overflow:hidden;border:1px solid rgba(255,255,255,0.1);">
        <div style="padding:16px;background:linear-gradient(135deg,#00a651,#00d66a);color:white;display:flex;justify-content:space-between;align-items:center;">
            <h3 style="margin:0;font-size:16px;">🤖 <span data-i18n="chatbotTitle">Dzir IA</span></h3>
            <button onclick="IAFactory.toggleChatbot()" style="background:rgba(255,255,255,0.2);border:none;color:white;width:28px;height:28px;border-radius:50%;cursor:pointer;font-size:18px;">×</button>
        </div>
        <div style="display:flex;padding:8px;gap:4px;background:rgba(0,0,0,0.2);">
            <button class="iaf-chatbot-mode active" id="iaf-mode-chat" onclick="IAFactory.setChatMode('chat')" style="flex:1;padding:8px;border:none;background:var(--accent,#00a651);color:white;cursor:pointer;border-radius:8px;font-size:12px;" data-i18n="chatbotModeChat">Chat IA</button>
            <button class="iaf-chatbot-mode" id="iaf-mode-rag" onclick="IAFactory.setChatMode('rag')" style="flex:1;padding:8px;border:none;background:transparent;color:inherit;cursor:pointer;border-radius:8px;font-size:12px;opacity:0.6;" data-i18n="chatbotModeRag">Recherche</button>
            <button class="iaf-chatbot-mode" id="iaf-mode-support" onclick="IAFactory.setChatMode('support')" style="flex:1;padding:8px;border:none;background:transparent;color:inherit;cursor:pointer;border-radius:8px;font-size:12px;opacity:0.6;" data-i18n="chatbotModeSupport">Support</button>
        </div>
        <div class="iaf-chatbot-messages" id="iaf-chatbot-messages" style="flex:1;overflow-y:auto;padding:16px;">
            <div style="display:flex;gap:8px;margin-bottom:12px;">
                <div style="width:32px;height:32px;background:linear-gradient(135deg,#00a651,#00d66a);color:white;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:11px;flex-shrink:0;">DZ</div>
                <div style="background:rgba(0,0,0,0.2);padding:10px 14px;border-radius:12px;max-width:80%;font-size:14px;line-height:1.4;" data-i18n="chatbotWelcome" data-i18n-html>👋 Bonjour ! Je suis <strong>Dzir IA</strong>. Comment puis-je vous aider ?</div>
            </div>
        </div>
        <div style="display:flex;padding:12px;gap:8px;border-top:1px solid rgba(255,255,255,0.1);">
            <input type="text" id="iaf-chatbot-input" placeholder="Tapez votre message..." data-i18n-placeholder="chatbotPlaceholder" onkeypress="if(event.key==='Enter')IAFactory.sendChatMessage()" style="flex:1;padding:10px 14px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;background:rgba(0,0,0,0.2);color:inherit;outline:none;font-size:14px;">
            <button onclick="IAFactory.sendChatMessage()" style="width:40px;height:40px;border-radius:50%;border:none;background:#00a651;color:white;cursor:pointer;font-size:16px;">➤</button>
        </div>
    </div>
'''

def inject_into_header(filepath):
    """Injecte les boutons langue/thème dans le header existant"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Skip si pas de header
        if '<header' not in content.lower():
            return f"⏭️  SKIP (pas de header): {filepath}"
        
        # Skip si déjà les boutons
        if 'iaf-lang-dropdown' in content:
            return f"⏭️  SKIP (déjà fait): {filepath}"
        
        original = content
        
        # Trouver la position juste avant </header>
        # Injecter les boutons langue/thème
        content = re.sub(
            r'(</header>)',
            LANG_THEME_BUTTONS + r'\n            \1',
            content,
            count=1,
            flags=re.IGNORECASE
        )
        
        # Ajouter le chatbot avant </body> si pas déjà présent
        if 'iaf-chatbot-btn' not in content and 'iaf-chatbot' not in content:
            content = re.sub(
                r'(</body>)',
                CHATBOT_HTML + r'\n\1',
                content,
                count=1,
                flags=re.IGNORECASE
            )
        
        if content == original:
            return f"⏭️  SKIP (pas de modif): {filepath}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"✅ UPDATED: {filepath}"
    
    except Exception as e:
        return f"❌ ERROR: {filepath} - {str(e)}"

def main():
    print("=" * 60)
    print("🚀 IAFactory - Injection Boutons Langue/Thème dans Headers")
    print("=" * 60)
    
    updated = 0
    skipped = 0
    errors = 0
    
    for app_dir in sorted(os.listdir(APPS_DIR)):
        if app_dir in SKIP_DIRS:
            continue
        
        app_path = os.path.join(APPS_DIR, app_dir)
        if not os.path.isdir(app_path):
            continue
        
        index_path = os.path.join(app_path, "index.html")
        if os.path.exists(index_path):
            result = inject_into_header(index_path)
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
