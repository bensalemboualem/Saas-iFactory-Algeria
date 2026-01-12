#!/usr/bin/env python3
"""
===================================================================
PIPELINE AUTOMATISÉ: BMAD → ARCHON → BOLT
IAFactory Algeria - Automation Complete Workflow
===================================================================

Ce script automatise le workflow complet:
1. BMAD: Création des specs (PRD, Architecture, User Stories)
2. ARCHON: Création de la knowledge base avec les specs
3. BOLT: Génération automatique du code

Usage:
    python bmad-to-archon-to-bolt.py --project "Mon E-commerce"
"""

import os
import sys
import json
import time
import requests
import subprocess
from pathlib import Path
from typing import Dict, Any, List

# ========== CONFIGURATION ==========
BMAD_PATH = "/opt/iafactory-rag-dz/bmad"
ARCHON_API = "http://localhost:3737/api"
BOLT_API = "http://localhost:5173/api"
PROJECTS_DIR = "/opt/iafactory-rag-dz/projects"

# Ports des services
ARCHON_PORT = 3737
BOLT_PORT = 5173
BACKEND_PORT = 8000


class BmadToArchonToBolt:
    """Orchestrateur du pipeline complet"""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_slug = project_name.lower().replace(" ", "-")
        self.project_dir = Path(PROJECTS_DIR) / self.project_slug

        # Chemins des outputs
        self.bmad_output_dir = self.project_dir / "bmad-output"
        self.archon_kb_id = None
        self.bolt_project_id = None

    def step1_run_bmad_workflow(self) -> Dict[str, Any]:
        """
        Étape 1: Exécuter BMAD pour créer les specs

        Returns:
            Dict contenant PRD, Architecture, Stories
        """
        print("\n" + "="*60)
        print("ÉTAPE 1: BMAD - Création des Spécifications")
        print("="*60)

        # Créer le dossier du projet
        self.project_dir.mkdir(parents=True, exist_ok=True)
        self.bmad_output_dir.mkdir(exist_ok=True)

        print(f"\n📁 Projet créé: {self.project_dir}")

        # Initialiser BMAD dans le dossier projet
        os.chdir(self.project_dir)

        print("\n🎯 Installation BMAD dans le projet...")
        subprocess.run([
            "npx", "bmad-method@alpha", "install",
            "--modules", "bmm",
            "--name", self.project_name
        ], check=True)

        print("\n📋 Workflows BMAD à exécuter:")
        print("   1. workflow-init (Initialisation)")
        print("   2. brainstorm-project (Brainstorming)")
        print("   3. prd (Product Requirements Document)")
        print("   4. architecture (Architecture)")
        print("   5. dev-stories (User Stories)")

        # Paths des outputs BMAD
        bmad_folder = self.project_dir / ".bmad"
        docs_folder = bmad_folder / "docs"

        workflows_to_run = [
            ("workflow-init", "Initialisation du projet"),
            ("brainstorm-project", "Brainstorming guidé"),
            ("prd", "Product Requirements Document"),
            ("architecture", "Décisions d'architecture"),
            ("create-stories", "Création des user stories")
        ]

        print("\n⚠️  ATTENTION: Les workflows BMAD sont INTERACTIFS")
        print("    Vous devez les exécuter manuellement dans votre IDE")
        print(f"\n    Dossier: {self.project_dir}")
        print("\n    Commandes à exécuter:")
        for workflow, desc in workflows_to_run:
            print(f"      /bmad:bmm:workflows:{workflow}  # {desc}")

        input("\n✋ Appuyez sur ENTER quand tous les workflows BMAD sont terminés...")

        # Lire les outputs BMAD
        bmad_outputs = {
            "prd": None,
            "architecture": None,
            "stories": []
        }

        # Chercher le PRD
        prd_files = list(docs_folder.glob("**/prd*.md"))
        if prd_files:
            with open(prd_files[0], 'r', encoding='utf-8') as f:
                bmad_outputs["prd"] = f.read()
            print(f"✅ PRD trouvé: {prd_files[0]}")

        # Chercher l'architecture
        arch_files = list(docs_folder.glob("**/architecture*.md"))
        if arch_files:
            with open(arch_files[0], 'r', encoding='utf-8') as f:
                bmad_outputs["architecture"] = f.read()
            print(f"✅ Architecture trouvée: {arch_files[0]}")

        # Chercher les stories
        story_files = list(docs_folder.glob("**/story-*.md"))
        for story_file in story_files:
            with open(story_file, 'r', encoding='utf-8') as f:
                bmad_outputs["stories"].append({
                    "file": str(story_file),
                    "content": f.read()
                })
        print(f"✅ {len(bmad_outputs['stories'])} stories trouvées")

        # Sauvegarder les outputs pour ARCHON
        outputs_json = self.bmad_output_dir / "bmad-outputs.json"
        with open(outputs_json, 'w', encoding='utf-8') as f:
            json.dump(bmad_outputs, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Outputs BMAD sauvegardés: {outputs_json}")

        return bmad_outputs

    def step2_create_archon_knowledge_base(self, bmad_outputs: Dict[str, Any]) -> str:
        """
        Étape 2: Créer la knowledge base ARCHON avec les specs BMAD

        Args:
            bmad_outputs: Outputs de BMAD (PRD, Architecture, Stories)

        Returns:
            ID de la knowledge base créée
        """
        print("\n" + "="*60)
        print("ÉTAPE 2: ARCHON - Création de la Knowledge Base")
        print("="*60)

        # Vérifier qu'ARCHON est accessible
        try:
            response = requests.get(f"{ARCHON_API}/health", timeout=5)
            response.raise_for_status()
            print("✅ ARCHON est accessible")
        except Exception as e:
            print(f"❌ ARCHON non accessible: {e}")
            print(f"   Démarrer ARCHON: docker-compose up -d iaf-archon-prod")
            sys.exit(1)

        # Créer une nouvelle knowledge base
        kb_data = {
            "name": f"{self.project_name} - Knowledge Base",
            "description": f"Base de connaissances générée depuis BMAD pour {self.project_name}",
            "type": "project_specs",
            "metadata": {
                "source": "bmad-pipeline",
                "project_name": self.project_name,
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }

        print(f"\n📚 Création de la knowledge base: {kb_data['name']}")

        response = requests.post(
            f"{ARCHON_API}/knowledge",
            json=kb_data,
            timeout=30
        )
        response.raise_for_status()
        kb_result = response.json()
        self.archon_kb_id = kb_result["id"]

        print(f"✅ Knowledge base créée: {self.archon_kb_id}")

        # Uploader les documents BMAD
        documents_to_upload = []

        # 1. PRD
        if bmad_outputs["prd"]:
            documents_to_upload.append({
                "name": "Product Requirements Document",
                "type": "prd",
                "content": bmad_outputs["prd"],
                "metadata": {"phase": "planning"}
            })

        # 2. Architecture
        if bmad_outputs["architecture"]:
            documents_to_upload.append({
                "name": "Architecture Document",
                "type": "architecture",
                "content": bmad_outputs["architecture"],
                "metadata": {"phase": "design"}
            })

        # 3. User Stories
        for i, story in enumerate(bmad_outputs["stories"], 1):
            documents_to_upload.append({
                "name": f"User Story {i}",
                "type": "user_story",
                "content": story["content"],
                "metadata": {"phase": "implementation", "story_number": i}
            })

        print(f"\n📤 Upload de {len(documents_to_upload)} documents...")

        for doc in documents_to_upload:
            print(f"   Uploading: {doc['name']}...")
            response = requests.post(
                f"{ARCHON_API}/knowledge/{self.archon_kb_id}/documents",
                json=doc,
                timeout=60
            )
            response.raise_for_status()
            print(f"   ✅ {doc['name']}")

        # Lancer l'indexation (embeddings)
        print("\n🔄 Indexation des documents (création des embeddings)...")
        response = requests.post(
            f"{ARCHON_API}/knowledge/{self.archon_kb_id}/index",
            timeout=300
        )
        response.raise_for_status()

        print("✅ Indexation terminée!")
        print(f"\n📊 Knowledge Base Stats:")

        # Récupérer les stats
        response = requests.get(f"{ARCHON_API}/knowledge/{self.archon_kb_id}/stats")
        stats = response.json()
        print(f"   - Documents: {stats.get('documents_count', 0)}")
        print(f"   - Chunks: {stats.get('chunks_count', 0)}")
        print(f"   - Vector embeddings: {stats.get('embeddings_count', 0)}")

        return self.archon_kb_id

    def step3_launch_bolt_project(self, kb_id: str) -> str:
        """
        Étape 3: Lancer BOLT pour générer le code

        Args:
            kb_id: ID de la knowledge base ARCHON

        Returns:
            ID du projet BOLT créé
        """
        print("\n" + "="*60)
        print("ÉTAPE 3: BOLT - Génération du Code")
        print("="*60)

        # Vérifier que BOLT est accessible
        try:
            response = requests.get(f"{BOLT_API}/health", timeout=5)
            print("✅ BOLT est accessible")
        except Exception as e:
            print(f"❌ BOLT non accessible: {e}")
            print(f"   Démarrer BOLT: cd /opt/iafactory-rag-dz/bolt-diy && pnpm run dev")
            sys.exit(1)

        # Créer un nouveau projet BOLT
        bolt_project_data = {
            "name": self.project_name,
            "description": f"Projet généré automatiquement depuis BMAD",
            "knowledge_base_id": kb_id,
            "template": "auto",  # BOLT détecte automatiquement le type
            "metadata": {
                "source": "bmad-archon-pipeline",
                "bmad_project": self.project_slug
            }
        }

        print(f"\n🚀 Création du projet BOLT: {self.project_name}")

        response = requests.post(
            f"{BOLT_API}/projects",
            json=bolt_project_data,
            timeout=30
        )
        response.raise_for_status()
        bolt_result = response.json()
        self.bolt_project_id = bolt_result["id"]

        print(f"✅ Projet BOLT créé: {self.bolt_project_id}")

        # Lancer la génération automatique
        print("\n⚡ Lancement de la génération de code...")
        print("   BOLT va utiliser la knowledge base ARCHON pour:")
        print("   - Analyser le PRD et l'architecture")
        print("   - Générer la structure du projet")
        print("   - Créer les composants de base")
        print("   - Implémenter les user stories")

        response = requests.post(
            f"{BOLT_API}/projects/{self.bolt_project_id}/generate",
            json={
                "mode": "auto",
                "use_rag": True,
                "knowledge_base_id": kb_id
            },
            timeout=600  # 10 minutes max
        )
        response.raise_for_status()
        generation_result = response.json()

        print("\n✅ Génération terminée!")
        print(f"\n📁 Code généré dans: {generation_result.get('output_dir')}")
        print(f"🌐 URL du projet: http://localhost:{BOLT_PORT}/projects/{self.bolt_project_id}")

        return self.bolt_project_id

    def run_complete_pipeline(self):
        """Exécuter le pipeline complet: BMAD → ARCHON → BOLT"""
        print("\n" + "="*70)
        print("🚀 PIPELINE AUTOMATISÉ: BMAD → ARCHON → BOLT")
        print("   IAFactory Algeria - Complete Automation Workflow")
        print("="*70)

        print(f"\n📦 Projet: {self.project_name}")
        print(f"📁 Dossier: {self.project_dir}")

        try:
            # Étape 1: BMAD
            bmad_outputs = self.step1_run_bmad_workflow()

            # Étape 2: ARCHON
            kb_id = self.step2_create_archon_knowledge_base(bmad_outputs)

            # Étape 3: BOLT
            project_id = self.step3_launch_bolt_project(kb_id)

            # Résumé final
            print("\n" + "="*70)
            print("✅ PIPELINE TERMINÉ AVEC SUCCÈS!")
            print("="*70)

            print(f"\n📊 Résumé:")
            print(f"   1. BMAD:")
            print(f"      - PRD: {'✅' if bmad_outputs['prd'] else '❌'}")
            print(f"      - Architecture: {'✅' if bmad_outputs['architecture'] else '❌'}")
            print(f"      - Stories: {len(bmad_outputs['stories'])}")
            print(f"\n   2. ARCHON:")
            print(f"      - Knowledge Base ID: {kb_id}")
            print(f"      - URL: http://localhost:{ARCHON_PORT}/knowledge/{kb_id}")
            print(f"\n   3. BOLT:")
            print(f"      - Project ID: {project_id}")
            print(f"      - URL: http://localhost:{BOLT_PORT}/projects/{project_id}")

            print(f"\n🎯 Prochaines étapes:")
            print(f"   1. Ouvrir BOLT: http://localhost:{BOLT_PORT}/projects/{project_id}")
            print(f"   2. Vérifier le code généré")
            print(f"   3. Tester l'application")
            print(f"   4. Déployer!")

            # Sauvegarder le résumé
            summary_file = self.project_dir / "pipeline-summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "project_name": self.project_name,
                    "project_slug": self.project_slug,
                    "bmad_outputs": {
                        "prd_exists": bool(bmad_outputs["prd"]),
                        "architecture_exists": bool(bmad_outputs["architecture"]),
                        "stories_count": len(bmad_outputs["stories"])
                    },
                    "archon_kb_id": kb_id,
                    "bolt_project_id": project_id,
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }, f, indent=2)

            print(f"\n💾 Résumé sauvegardé: {summary_file}")

        except Exception as e:
            print(f"\n❌ ERREUR: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    """Point d'entrée du script"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Pipeline automatisé: BMAD → ARCHON → BOLT"
    )
    parser.add_argument(
        "--project",
        required=True,
        help="Nom du projet à créer"
    )

    args = parser.parse_args()

    # Créer et lancer le pipeline
    pipeline = BmadToArchonToBolt(args.project)
    pipeline.run_complete_pipeline()


if __name__ == "__main__":
    main()
