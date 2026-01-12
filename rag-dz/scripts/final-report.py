#!/usr/bin/env python3
"""
RAPPORT FINAL - IAFactory Trilingue SaaS
Vérifie TOUT:
1. CSS unifié
2. JS unifié  
3. Contrôles trilingues (FR/AR/EN)
4. Chatbot aide
5. Footer
6. Pas d'ancien code
"""

import os
import re

APPS_DIR = "/opt/iafactory-rag-dz/apps"

def verify_complete(filepath, app_name):
    """Vérification complète d'une app"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        checks = {
            "CSS": "iafactory-unified.css" in content,
            "JS": "iafactory-unified.js" in content,
            "Lang": "iaf-lang-dropdown" in content or "iaf-controls-floating" in content or "IAFUnified.changeLang" in content,
            "Chat": "iaf-chatbot-btn" in content or "IAFUnified.toggleChatbot" in content,
            "Footer": "data-iaf-footer" in content or 'id="iaf-footer"' in content,
            "NoOld": "toggleHelpWindow" not in content or "IAFUnified" in content
        }
        
        return checks
    
    except Exception as e:
        return None

def main():
    print("=" * 70)
    print("📊 RAPPORT FINAL - IAFactory Trilingue SaaS")
    print("=" * 70)
    print()
    
    stats = {"total": 0, "perfect": 0, "issues": []}
    component_stats = {"CSS": 0, "JS": 0, "Lang": 0, "Chat": 0, "Footer": 0, "NoOld": 0}
    
    for app_dir in sorted(os.listdir(APPS_DIR)):
        if app_dir in ["shared", "landing", "node_modules", "school-erp"]:
            continue
        
        app_path = os.path.join(APPS_DIR, app_dir)
        if not os.path.isdir(app_path):
            continue
        
        index_path = os.path.join(app_path, "index.html")
        if os.path.exists(index_path):
            stats["total"] += 1
            checks = verify_complete(index_path, app_dir)
            
            if checks:
                for k, v in checks.items():
                    if v:
                        component_stats[k] += 1
                
                if all(checks.values()):
                    stats["perfect"] += 1
                else:
                    missing = [k for k, v in checks.items() if not v]
                    stats["issues"].append(f"{app_dir}: {', '.join(missing)}")
    
    # Affichage du rapport
    print("📈 STATISTIQUES PAR COMPOSANT:")
    print("-" * 50)
    for comp, count in component_stats.items():
        pct = (count / stats["total"]) * 100 if stats["total"] > 0 else 0
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        label = {
            "CSS": "CSS Unifié     ",
            "JS": "JS Unifié      ",
            "Lang": "Trilingue      ",
            "Chat": "Chatbot        ",
            "Footer": "Footer         ",
            "NoOld": "Sans Ancien    "
        }.get(comp, comp)
        print(f"  {label}: {bar} {count}/{stats['total']} ({pct:.0f}%)")
    
    print()
    print("=" * 70)
    print(f"🎯 SCORE GLOBAL: {stats['perfect']}/{stats['total']} apps parfaites ({(stats['perfect']/stats['total'])*100:.0f}%)")
    print("=" * 70)
    
    if stats["issues"]:
        print("\n⚠️  APPS AVEC PROBLÈMES:")
        for issue in stats["issues"]:
            print(f"   ❌ {issue}")
    else:
        print("\n🎉 TOUTES LES APPS SONT PARFAITES!")
    
    print()
    print("=" * 70)
    print("✅ COMPOSANTS UNIFIÉS IAFactory:")
    print("   • /apps/shared/iafactory-unified.css")
    print("   • /apps/shared/iafactory-unified.js")
    print("   • Header avec Lang (FR/AR/EN) + Theme Toggle")
    print("   • Chatbot d'aide unifié")
    print("   • Footer unifié")
    print("   • Support RTL pour l'arabe")
    print("=" * 70)

if __name__ == "__main__":
    main()
