"""
Agent Orchestrateur #20 - Service
Coordonne tous les agents BMAD et déclenche la production automatique
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class OrchestratorService:
    """Service d'orchestration pour l'Agent #20"""

    def __init__(self):
        self.project_signals = {
            "architecture_defined": False,
            "requirements_clear": False,
            "tech_stack_chosen": False,
            "ux_specified": False,
            "tests_planned": False,
        }

    def analyze_project_readiness(
        self,
        messages: List[Dict[str, Any]],
        agents_used: List[str]
    ) -> Dict[str, Any]:
        """
        Analyse si le projet est prêt pour la production automatique

        Critères:
        - Architecture définie (Winston - bmm-architect)
        - Requirements clairs (John - bmm-pm)
        - Tech stack choisi (Winston + Amelia)
        - UX/UI spécifié (Sally - bmm-ux-designer)
        - Tests planifiés (Murat - bmm-tea)
        """
        signals = self._detect_project_signals(messages, agents_used)

        # Calculer le score de confiance
        total_signals = len(signals)
        validated_signals = sum(1 for v in signals.values() if v)
        confidence_score = int((validated_signals / total_signals) * 100)

        project_ready = confidence_score >= 80  # 80% minimum

        missing_elements = [
            key.replace("_", " ").title()
            for key, value in signals.items()
            if not value
        ]

        return {
            "project_ready": project_ready,
            "confidence_score": confidence_score,
            "signals": signals,
            "missing_elements": missing_elements,
            "agents_consulted": len(agents_used),
            "message_count": len(messages),
        }

    def _detect_project_signals(
        self,
        messages: List[Dict[str, Any]],
        agents_used: List[str]
    ) -> Dict[str, bool]:
        """Détecte les signaux de préparation du projet"""

        conversation_text = " ".join([
            msg.get("content", "").lower()
            for msg in messages
        ])

        signals = {}

        # Signal 1: Architecture définie
        architecture_keywords = [
            "architecture", "microservices", "monolithic", "backend", "frontend",
            "api", "database", "redis", "postgresql", "layers", "components"
        ]
        signals["architecture_defined"] = (
            "bmm-architect" in agents_used and
            any(kw in conversation_text for kw in architecture_keywords)
        )

        # Signal 2: Requirements clairs
        requirements_keywords = [
            "requirements", "features", "user stories", "epics", "prd",
            "fonctionnalités", "specifications", "scope"
        ]
        signals["requirements_clear"] = (
            "bmm-pm" in agents_used and
            any(kw in conversation_text for kw in requirements_keywords)
        )

        # Signal 3: Tech stack choisi
        tech_keywords = [
            "react", "vue", "angular", "python", "fastapi", "node",
            "typescript", "javascript", "next", "django", "flask"
        ]
        signals["tech_stack_chosen"] = (
            any(kw in conversation_text for kw in tech_keywords)
        )

        # Signal 4: UX/UI spécifié
        ux_keywords = [
            "ux", "ui", "design", "wireframe", "mockup", "prototype",
            "user experience", "interface", "responsive"
        ]
        signals["ux_specified"] = (
            "bmm-ux-designer" in agents_used or
            any(kw in conversation_text for kw in ux_keywords)
        )

        # Signal 5: Tests planifiés
        test_keywords = [
            "test", "testing", "qa", "quality", "unit test", "integration",
            "e2e", "coverage", "pytest", "jest"
        ]
        signals["tests_planned"] = (
            "bmm-tea" in agents_used or
            any(kw in conversation_text for kw in test_keywords)
        )

        return signals

    def synthesize_knowledge(
        self,
        messages: List[Dict[str, Any]],
        agents_used: List[str]
    ) -> str:
        """
        Synthétise toute la connaissance accumulée des agents BMAD
        en un document de knowledge base structuré
        """

        # Grouper les messages par agent
        agent_contributions = {}
        for msg in messages:
            agent = msg.get("agent", "unknown")
            if agent not in agent_contributions:
                agent_contributions[agent] = []
            if msg.get("role") == "assistant":
                agent_contributions[agent].append(msg.get("content", ""))

        # Générer le document de synthèse
        knowledge_doc = f"""# 📚 Knowledge Base - Projet RAG.dz

**Date de création**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Agents consultés**: {len(agents_used)}
**Messages analysés**: {len(messages)}

---

## 🎯 Vue d'Ensemble

{self._extract_project_overview(messages)}

---

## 🏗️ Architecture Technique

{self._extract_architecture(agent_contributions.get('bmm-architect', []))}

---

## 📋 Requirements Fonctionnels

{self._extract_requirements(agent_contributions.get('bmm-pm', []))}

---

## 💻 Stack Technologique

{self._extract_tech_stack(messages)}

---

## 🎨 UX/UI Design

{self._extract_ux_design(agent_contributions.get('bmm-ux-designer', []))}

---

## 🧪 Stratégie de Tests

{self._extract_test_strategy(agent_contributions.get('bmm-tea', []))}

---

## 👥 Contributions des Agents

{self._format_agent_contributions(agent_contributions)}

---

**Généré automatiquement par l'Agent Orchestrateur #20**
"""

        return knowledge_doc

    def _extract_project_overview(self, messages: List[Dict[str, Any]]) -> str:
        """Extrait la vue d'ensemble du projet"""
        first_user_message = next(
            (msg.get("content", "") for msg in messages if msg.get("role") == "user"),
            "Projet non spécifié"
        )
        return f"Le projet vise à: {first_user_message[:500]}..."

    def _extract_architecture(self, architect_messages: List[str]) -> str:
        """Extrait les décisions d'architecture"""
        if not architect_messages:
            return "Architecture non encore définie."

        return "\n\n".join([
            f"- {msg[:300]}..."
            for msg in architect_messages[:3]
        ])

    def _extract_requirements(self, pm_messages: List[str]) -> str:
        """Extrait les requirements du PM"""
        if not pm_messages:
            return "Requirements à définir."

        return "\n\n".join([
            f"- {msg[:300]}..."
            for msg in pm_messages[:3]
        ])

    def _extract_tech_stack(self, messages: List[Dict[str, Any]]) -> str:
        """Détecte et liste le stack technologique"""
        conversation_text = " ".join([
            msg.get("content", "").lower()
            for msg in messages
        ])

        tech_found = []
        tech_patterns = {
            "Frontend": ["react", "vue", "angular", "next", "svelte"],
            "Backend": ["fastapi", "django", "flask", "express", "nestjs"],
            "Database": ["postgresql", "mysql", "mongodb", "redis", "supabase"],
            "Language": ["python", "typescript", "javascript", "go", "rust"],
        }

        for category, technologies in tech_patterns.items():
            found = [tech for tech in technologies if tech in conversation_text]
            if found:
                tech_found.append(f"**{category}**: {', '.join(found)}")

        return "\n".join(tech_found) if tech_found else "Stack technologique à définir."

    def _extract_ux_design(self, ux_messages: List[str]) -> str:
        """Extrait les spécifications UX/UI"""
        if not ux_messages:
            return "Design UX/UI à définir."

        return "\n\n".join([
            f"- {msg[:300]}..."
            for msg in ux_messages[:2]
        ])

    def _extract_test_strategy(self, tea_messages: List[str]) -> str:
        """Extrait la stratégie de tests"""
        if not tea_messages:
            return "Stratégie de tests à définir."

        return "\n\n".join([
            f"- {msg[:300]}..."
            for msg in tea_messages[:2]
        ])

    def _format_agent_contributions(self, contributions: Dict[str, List[str]]) -> str:
        """Formate les contributions de chaque agent"""
        formatted = []

        agent_names = {
            "bmm-architect": "🏗️ Winston (Architect)",
            "bmm-pm": "📋 John (Product Manager)",
            "bmm-dev": "💻 Amelia (Developer)",
            "bmm-ux-designer": "🎨 Sally (UX Designer)",
            "bmm-tea": "🧪 Murat (Test Engineer)",
        }

        for agent_id, messages in contributions.items():
            if messages and agent_id != "unknown":
                name = agent_names.get(agent_id, agent_id)
                formatted.append(f"### {name}\n")
                formatted.append(f"Messages: {len(messages)}\n")

        return "\n".join(formatted) if formatted else "Aucune contribution enregistrée."

    def order_bolt_production(
        self,
        project_id: str,
        project_name: str,
        tech_stack: List[str],
        knowledge_base_id: str
    ) -> Dict[str, Any]:
        """
        Ordonne à Bolt.DIY de produire le projet final

        Returns:
            Commande de production avec instructions complètes
        """

        production_command = {
            "command": "PRODUCE_PROJECT",
            "project_id": project_id,
            "project_name": project_name,
            "tech_stack": tech_stack,
            "knowledge_base_id": knowledge_base_id,
            "instructions": [
                "1. Générer l'architecture complète de fichiers",
                "2. Créer tous les composants nécessaires",
                "3. Implémenter la logique métier",
                "4. Ajouter les tests unitaires et d'intégration",
                "5. Configurer le déploiement (Docker, CI/CD)",
                "6. Générer la documentation",
                "7. Produire le code final prêt à l'emploi",
            ],
            "bolt_url": f"http://localhost:5174?project_id={project_id}&knowledge_base={knowledge_base_id}&mode=production",
            "timestamp": datetime.now().isoformat(),
        }

        logger.info(f"🎯 Agent Orchestrateur ordonne production: {project_name}")

        return production_command


# Instance globale
orchestrator_service = OrchestratorService()
