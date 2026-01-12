#!/usr/bin/env python3
"""
===================================================================
AUTOMATISATION - INTÉGRATION I18N DANS LES 18 AGENTS STREAMLIT
Rend tous les agents trilingues: Français | English | العربية
===================================================================
"""

import os
import re
import shutil
from pathlib import Path

# ========== CONFIGURATION ==========

AGENTS_CONFIG = [
    # Phase 1 - Premium HTTPS
    {
        "name": "ai-consultant",
        "path": "ai-agents/ai_consultant_agent",
        "main_file": "consultant_ui.py",
        "agent_type": "consultant",
        "port": 9101
    },
    {
        "name": "customer-support",
        "path": "ai-agents/ai_customer_support_agent",
        "main_file": "customer_support_agent.py",
        "agent_type": "support",
        "port": 9102
    },
    {
        "name": "data-analyst",
        "path": "ai-agents/data-analyst-agent",
        "main_file": "data_analyst_agent.py",
        "agent_type": "data_analysis",
        "port": 9103
    },
    {
        "name": "rag-as-service",
        "path": "ai-agents/rag-apps/rag_as_service",
        "main_file": "rag_as_service_agent.py",
        "agent_type": "rag",
        "port": 9110
    },
    {
        "name": "investment",
        "path": "ai-agents/finance-startups/investment_agent",
        "main_file": "investment_agent.py",
        "agent_type": "investment",
        "port": 9114
    },

    # Phase 2 - Business
    {
        "name": "xai-finance",
        "path": "ai-agents/xai_finance",
        "main_file": "xai_finance_agent.py",
        "agent_type": "finance",
        "port": 9104
    },
    {
        "name": "meeting-prep",
        "path": "ai-agents/meeting-prep-agent",
        "main_file": "meeting_prep_agent.py",
        "agent_type": "common",
        "port": 9105
    },
    {
        "name": "news-journalist",
        "path": "ai-agents/news-journalist-agent",
        "main_file": "news_journalist_agent.py",
        "agent_type": "common",
        "port": 9106
    },
    {
        "name": "web-scraping",
        "path": "ai-agents/web-scraping-agent",
        "main_file": "web_scraping_agent.py",
        "agent_type": "common",
        "port": 9107
    },
    {
        "name": "product-launch",
        "path": "ai-agents/product-launch-agent",
        "main_file": "product_launch_agent.py",
        "agent_type": "common",
        "port": 9108
    },

    # Phase 3 - RAG Apps
    {
        "name": "local-rag",
        "path": "ai-agents/rag-apps/local_rag_agent",
        "main_file": "local_rag_agent.py",
        "agent_type": "rag",
        "port": 9109
    },
    {
        "name": "agentic-rag",
        "path": "ai-agents/rag-apps/agentic_rag_with_reasoning",
        "main_file": "agentic_rag_agent.py",
        "agent_type": "rag",
        "port": 9111
    },
    {
        "name": "hybrid-search",
        "path": "ai-agents/rag-apps/hybrid_search_agent",
        "main_file": "hybrid_search_agent.py",
        "agent_type": "rag",
        "port": 9112
    },
    {
        "name": "autonomous-rag",
        "path": "ai-agents/rag-apps/autonomous_rag",
        "main_file": "autonomous_rag_agent.py",
        "agent_type": "rag",
        "port": 9113
    },

    # Phase 4 - Finance & Startups
    {
        "name": "financial-coach",
        "path": "ai-agents/finance-startups/ai_financial_coach_agent",
        "main_file": "financial_coach_agent.py",
        "agent_type": "finance",
        "port": 9115
    },
    {
        "name": "startup-trends",
        "path": "ai-agents/finance-startups/ai_startup_trend_analysis_agent",
        "main_file": "startup_trends_agent.py",
        "agent_type": "common",
        "port": 9116
    },
    {
        "name": "system-architect",
        "path": "ai-agents/software-dev/ai_system_architect_agent",
        "main_file": "system_architect_agent.py",
        "agent_type": "common",
        "port": 9117
    },
    {
        "name": "deep-research",
        "path": "ai-agents/ai-research-agents/deep_research_agent",
        "main_file": "deep_research_agent.py",
        "agent_type": "common",
        "port": 9118
    }
]

# Template d'imports i18n
I18N_IMPORTS_TEMPLATE = """import sys
sys.path.append('/app/shared')

from streamlit_i18n import get_i18n, render_header, inject_custom_css
"""

# ========== FONCTIONS ==========

def copy_i18n_module_to_agent(agent_path: str) -> bool:
    """Copier le module i18n dans le dossier shared de l'agent"""
    try:
        agent_dir = Path(agent_path)
        if not agent_dir.exists():
            print(f"  [!!] Chemin introuvable: {agent_path}")
            return False

        # Creer dossier shared
        shared_dir = agent_dir / "shared"
        shared_dir.mkdir(exist_ok=True)

        # Copier streamlit_i18n.py
        source = Path("shared/streamlit_i18n.py")
        destination = shared_dir / "streamlit_i18n.py"

        if not source.exists():
            print(f"  [XX] Module source introuvable: {source}")
            return False

        shutil.copy(source, destination)
        print(f"  [OK] Module i18n copie dans {shared_dir}")
        return True

    except Exception as e:
        print(f"  [XX] Erreur copie module: {e}")
        return False


def integrate_i18n_in_agent_file(agent_config: dict) -> bool:
    """Intégrer i18n dans le fichier principal de l'agent"""
    try:
        agent_dir = Path(agent_config["path"])
        main_file = agent_dir / agent_config["main_file"]

        if not main_file.exists():
            print(f"  [!!]  Fichier principal introuvable: {main_file}")
            return False

        # Lire le contenu
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Vérifier si déjà intégré
        if 'streamlit_i18n' in content:
            print(f"  [i]  Déjà intégré: {main_file}")
            return True

        # Ajouter imports i18n après les imports streamlit
        if 'import streamlit as st' in content:
            # Trouver la ligne import streamlit
            lines = content.split('\n')
            import_idx = -1

            for i, line in enumerate(lines):
                if line.strip().startswith('import streamlit as st'):
                    import_idx = i
                    break

            if import_idx >= 0:
                # Insérer les imports i18n après
                lines.insert(import_idx + 1, I18N_IMPORTS_TEMPLATE)
                content = '\n'.join(lines)
        else:
            # Ajouter au début si pas d'import streamlit trouvé
            content = I18N_IMPORTS_TEMPLATE + "\n" + content

        # Modifier st.set_page_config pour ajouter flag algérien
        content = re.sub(
            r'st\.set_page_config\s*\([^)]+\)',
            lambda m: m.group(0).replace('page_icon="', 'page_icon="DZ", ') if 'page_icon' in m.group(0)
                      else m.group(0).replace(')', ', page_icon="DZ")'),
            content
        )

        # Ajouter render_header après set_page_config si pas déjà présent
        if 'render_header' not in content and 'st.set_page_config' in content:
            agent_type = agent_config["agent_type"]
            header_code = f"""
# i18n Setup
i18n = get_i18n()
render_header("{agent_type}")
"""
            # Insérer après set_page_config
            content = re.sub(
                r'(st\.set_page_config\([^)]+\))',
                r'\1' + header_code,
                content
            )

        # Sauvegarder avec backup
        backup_file = main_file.with_suffix('.py.backup')
        shutil.copy(main_file, backup_file)

        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  [OK] Fichier modifié: {main_file}")
        print(f"     [save] Backup: {backup_file}")
        return True

    except Exception as e:
        print(f"  [XX] Erreur intégration fichier: {e}")
        return False


def update_dockerfile(agent_path: str) -> bool:
    """Mettre à jour le Dockerfile pour inclure le dossier shared"""
    try:
        dockerfile = Path(agent_path) / "Dockerfile"

        if not dockerfile.exists():
            print(f"  [!!]  Dockerfile introuvable: {dockerfile}")
            return False

        with open(dockerfile, 'r', encoding='utf-8') as f:
            content = f.read()

        # Vérifier si déjà configuré
        if '/app/shared' in content:
            print(f"  [i]  Dockerfile déjà configuré")
            return True

        # Ajouter mkdir shared si pas présent
        if 'mkdir -p /app/shared' not in content:
            # Insérer avant EXPOSE
            content = re.sub(
                r'(EXPOSE \d+)',
                r'# Create shared directory for i18n\nRUN mkdir -p /app/shared\n\n\1',
                content
            )

        # Backup et sauvegarde
        backup = dockerfile.with_suffix('.backup')
        shutil.copy(dockerfile, backup)

        with open(dockerfile, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  [OK] Dockerfile mis à jour")
        return True

    except Exception as e:
        print(f"  [XX] Erreur Dockerfile: {e}")
        return False


def integrate_agent(agent_config: dict) -> dict:
    """Integrer i18n dans un agent complet"""
    name = agent_config["name"]
    print(f"\n{'='*60}")
    print(f"[>] Agent: {name} (Port {agent_config['port']})")
    print(f"{'='*60}")

    results = {
        "name": name,
        "module_copied": False,
        "file_modified": False,
        "dockerfile_updated": False,
        "success": False
    }

    # 1. Copier module i18n
    results["module_copied"] = copy_i18n_module_to_agent(agent_config["path"])

    # 2. Modifier fichier principal
    results["file_modified"] = integrate_i18n_in_agent_file(agent_config)

    # 3. Mettre à jour Dockerfile
    results["dockerfile_updated"] = update_dockerfile(agent_config["path"])

    # Succès si au moins 2/3 tâches réussies
    success_count = sum([
        results["module_copied"],
        results["file_modified"],
        results["dockerfile_updated"]
    ])

    results["success"] = success_count >= 2

    if results["success"]:
        print(f"\n[OK] {name} - INTÉGRÉ AVEC SUCCÈS")
    else:
        print(f"\n[!!]  {name} - INTÉGRATION PARTIELLE ({success_count}/3)")

    return results


# ========== MAIN ==========

def main():
    print("""
================================================================
  INTEGRATION I18N - 18 AGENTS STREAMLIT
  Francais | English | Arabe
  IAFactory Algeria - Systeme Trilingue Automatique
================================================================
""")

    # Verifier que le module i18n source existe
    if not Path("shared/streamlit_i18n.py").exists():
        print("[XX] ERREUR: Module shared/streamlit_i18n.py introuvable!")
        print("   Assurez-vous d'etre dans le dossier racine du projet.")
        return

    results = []
    success_count = 0
    partial_count = 0
    failed_count = 0

    # Intégrer chaque agent
    for agent_config in AGENTS_CONFIG:
        result = integrate_agent(agent_config)
        results.append(result)

        if result["success"]:
            success_count += 1
        elif result["module_copied"] or result["file_modified"]:
            partial_count += 1
        else:
            failed_count += 1

    # Résumé
    print(f"""
================================================================
  RESUME DE L'INTEGRATION
================================================================

OK Agents integres avec succes:  {success_count}/18
!! Agents partiellement integres: {partial_count}/18
XX Agents echoues:                {failed_count}/18

{'='*60}
DETAILS PAR AGENT:
{'='*60}
""")

    for result in results:
        status = "[OK]" if result["success"] else ("[!!]" if result["module_copied"] or result["file_modified"] else "[XX]")
        print(f"{status} {result['name']}")
        print(f"   - Module copie:      {'+' if result['module_copied'] else '-'}")
        print(f"   - Fichier modifie:   {'+' if result['file_modified'] else '-'}")
        print(f"   - Dockerfile MAJ:    {'+' if result['dockerfile_updated'] else '-'}")
        print()

    print(f"""
{'='*60}
PROCHAINES ÉTAPES:
{'='*60}

1. Vérifier les backups créés (.backup)
2. Tester localement un agent:
   cd ai-agents/ai_consultant_agent
   streamlit run consultant_ui.py

3. Rebuild les conteneurs sur le VPS:
   docker-compose -f docker-compose-ai-agents.yml build
   docker-compose -f docker-compose-ai-agents.yml up -d

4. Acceder aux agents:
   https://ai-agents.iafactoryalgeria.com/consultant (9101)
   https://ai-agents.iafactoryalgeria.com/support (9102)
   etc.

IAFactory Algeria - Plateforme Trilingue Complete!
""")


if __name__ == "__main__":
    main()
