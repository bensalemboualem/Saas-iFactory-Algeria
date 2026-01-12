#!/usr/bin/env python3
"""
Integration i18n dans les 18 agents Streamlit sur VPS
Structure adaptee a l'organisation reelle
"""

import os
import shutil
from pathlib import Path

# Agents par categorie
AGENTS_MAP = {
    "business-core": ["consultant", "customer-support", "data-analysis"],
    "finance-startups": ["ai_deep_research_agent", "ai_financial_coach_agent",
                         "ai_investment_agent", "ai_startup_trend_analysis_agent",
                         "ai_system_architect_r1"],
    "productivity": ["journalist", "meeting", "product-launch", "web-scraping", "xai-finance"],
    "rag-apps": ["agentic_rag_with_reasoning", "autonomous_rag",
                 "hybrid_search_rag", "local_rag_agent", "rag-as-a-service"]
}

def copy_i18n_module(agent_path):
    """Copier le module i18n dans agent/shared/"""
    try:
        shared_dir = agent_path / "shared"
        shared_dir.mkdir(exist_ok=True)

        source = Path("/opt/iafactory-rag-dz/shared/streamlit_i18n.py")
        dest = shared_dir / "streamlit_i18n.py"

        shutil.copy(source, dest)
        print(f"  [OK] Module i18n copie: {dest}")
        return True
    except Exception as e:
        print(f"  [XX] Erreur: {e}")
        return False

def integrate_i18n_in_python_file(py_file, agent_type="common"):
    """Ajouter imports i18n dans fichier Python"""
    try:
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'streamlit_i18n' in content:
            print(f"  [i] Deja integre: {py_file.name}")
            return True

        # Backup
        backup = py_file.with_suffix('.py.backup')
        shutil.copy(py_file, backup)

        # Ajouter imports apres "import streamlit as st"
        if 'import streamlit as st' in content:
            i18n_imports = """
import sys
sys.path.append('/app/shared')
from streamlit_i18n import get_i18n, render_header
"""
            content = content.replace(
                'import streamlit as st',
                'import streamlit as st' + i18n_imports
            )

        # Ajouter render_header apres set_page_config si present
        if 'st.set_page_config' in content and 'render_header' not in content:
            # Trouver position apres set_page_config
            lines = content.split('\n')
            new_lines = []
            in_page_config = False
            added_header = False

            for line in lines:
                new_lines.append(line)
                if 'st.set_page_config' in line:
                    in_page_config = True
                elif in_page_config and ')' in line:
                    in_page_config = False
                    if not added_header:
                        new_lines.append(f'''
# i18n Setup
i18n = get_i18n()
render_header("{agent_type}")
''')
                        added_header = True

            content = '\n'.join(new_lines)

        with open(py_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  [OK] Fichier modifie: {py_file.name}")
        return True
    except Exception as e:
        print(f"  [XX] Erreur: {e}")
        return False

def process_agent(category, agent_name):
    """Traiter un agent"""
    print(f"\n{'='*60}")
    print(f"[>] {category}/{agent_name}")
    print('='*60)

    agent_path = Path(f"/opt/iafactory-rag-dz/ai-agents/{category}/{agent_name}")

    if not agent_path.exists():
        print(f"  [XX] Chemin inexistant")
        return False

    # 1. Copier module i18n
    copy_i18n_module(agent_path)

    # 2. Trouver fichier Python principal
    py_files = list(agent_path.glob("*.py"))
    main_file = None

    for pf in py_files:
        if pf.name.startswith('ai_') or 'agent' in pf.name:
            main_file = pf
            break

    if not main_file and py_files:
        main_file = py_files[0]

    if main_file:
        agent_type = "consultant" if "consultant" in agent_name else "common"
        integrate_i18n_in_python_file(main_file, agent_type)

    print(f"[OK] {agent_name} traite")
    return True

def main():
    print("""
================================================================
  INTEGRATION I18N - 18 AGENTS STREAMLIT VPS
  Francais | English | Arabe
================================================================
""")

    total = 0
    success = 0

    for category, agents in AGENTS_MAP.items():
        print(f"\n{'#'*60}")
        print(f"# CATEGORIE: {category.upper()}")
        print('#'*60)

        for agent in agents:
            if process_agent(category, agent):
                success += 1
            total += 1

    print(f"""
================================================================
  RESUME
================================================================
Agents traites: {success}/{total}

PROCHAINES ETAPES:
1. Rebuild containers Docker:
   cd /opt/iafactory-rag-dz
   docker-compose -f docker-compose-ai-agents.yml build
   docker-compose -f docker-compose-ai-agents-phase2.yml build
   docker-compose -f docker-compose-ai-agents-phase3.yml build
   docker-compose -f docker-compose-ai-agents-phase4.yml build

2. Redemarrer les agents:
   docker-compose -f docker-compose-ai-agents.yml up -d
   docker-compose -f docker-compose-ai-agents-phase2.yml up -d
   docker-compose -f docker-compose-ai-agents-phase3.yml up -d
   docker-compose -f docker-compose-ai-agents-phase4.yml up -d

IAFactory Algeria - Plateforme Trilingue Complete!
================================================================
""")

if __name__ == "__main__":
    main()
