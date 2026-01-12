"""
Service d'orchestration pour les workflows Bolt SuperPower
Gère l'exécution séquentielle des agents BMAD et la génération finale
"""
import logging
import asyncio
import time
import json
from typing import Dict, Any, List, Optional
import asyncpg
import os
import httpx

from app.models.bolt_workflow import (
    BMADWorkflowRequest,
    WorkflowStatus,
    AgentStatus,
    AgentResult,
    ProjectSynthesis
)
from app.services.bolt_workflow_service import BoltWorkflowService
from app.services.bolt_zip_service import BoltZipService
from app.services.bmad_orchestrator import BMADOrchestrator
from app.services.archon_integration_service import ArchonIntegrationService

logger = logging.getLogger(__name__)


class BoltOrchestrationService:
    """Service d'orchestration des workflows Bolt"""

    def __init__(self, db_pool: asyncpg.Pool):
        self.db_pool = db_pool
        self.workflow_service = BoltWorkflowService(db_pool)
        self.zip_service = BoltZipService(db_pool)
        self.bmad_orchestrator = BMADOrchestrator()
        self.archon_service = ArchonIntegrationService(db_pool)

        # Configuration LLM - utiliser Groq par défaut (gratuit)
        self.llm_provider = os.getenv("LLM_PROVIDER", "groq")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

        if not self.groq_api_key:
            logger.warning("GROQ_API_KEY not set - LLM calls may fail")

    # ==================== Mode Direct ====================

    async def run_direct_mode(
        self,
        workflow_id: str,
        prompt: str,
        tech_stack: Optional[List[str]],
        save_to_archon: bool
    ):
        """
        Exécute le mode direct: génération immédiate à partir d'un prompt

        Steps:
        1. Mettre statut à GENERATING
        2. Générer le code via Claude
        3. Sauvegarder dans Archon (optionnel)
        4. Créer le ZIP
        5. Mettre statut à COMPLETED
        """
        try:
            logger.info(f"Starting direct mode for workflow {workflow_id}")

            # Étape 1: Statut GENERATING
            await self.workflow_service.update_workflow_status(
                workflow_id,
                WorkflowStatus.GENERATING
            )

            # Étape 2: Génération du code
            generated_code = await self.generate_code_from_prompt(
                prompt=prompt,
                tech_stack=tech_stack
            )

            # Étape 3: Sauvegarder dans Archon (si demandé)
            archon_project_id = None
            knowledge_source_id = None

            if save_to_archon:
                archon_project_id, knowledge_source_id = await self.save_to_archon(
                    workflow_id=workflow_id,
                    project_name=self._extract_project_name(prompt),
                    content=generated_code,
                    tech_stack=tech_stack
                )

                await self.workflow_service.set_archon_project(
                    workflow_id,
                    archon_project_id,
                    knowledge_source_id
                )

            # Étape 4: Créer le ZIP
            zip_path = await self.zip_service.create_project_zip(
                workflow_id=workflow_id,
                generated_code=generated_code,
                include_docs=True,
                include_tests=True,
                include_deployment=True
            )

            await self.workflow_service.set_zip_file_path(workflow_id, zip_path)

            # Étape 5: Statut COMPLETED
            await self.workflow_service.update_workflow_status(
                workflow_id,
                WorkflowStatus.COMPLETED
            )

            logger.info(f"Direct mode completed for workflow {workflow_id}")

        except Exception as e:
            logger.error(f"Error in direct mode for workflow {workflow_id}: {e}", exc_info=True)
            await self.workflow_service.update_workflow_status(
                workflow_id,
                WorkflowStatus.FAILED
            )

    # ==================== Mode BMAD ====================

    async def run_bmad_orchestration(
        self,
        workflow_id: str,
        request: BMADWorkflowRequest
    ):
        """
        Exécute l'orchestration BMAD complète

        Steps:
        1. Mettre statut à ORCHESTRATING
        2. Exécuter chaque agent séquentiellement
        3. Synthétiser les résultats
        4. Créer projet dans Archon
        5. Mettre statut à GENERATING
        6. Générer le code final
        7. Créer le ZIP
        8. Mettre statut à COMPLETED
        """
        try:
            logger.info(f"Starting BMAD orchestration for workflow {workflow_id}")

            # Étape 1: Statut ORCHESTRATING
            await self.workflow_service.update_workflow_status(
                workflow_id,
                WorkflowStatus.ORCHESTRATING
            )

            # Étape 2: Exécuter les agents séquentiellement
            agent_results = {}
            previous_context = {
                "user_description": request.user_description,
                "constraints": request.constraints.dict(),
                "preferences": request.preferences.dict()
            }

            for agent_id in request.agents_to_use:
                logger.info(f"Executing agent {agent_id} for workflow {workflow_id}")

                # Mettre à jour le current_agent
                await self.workflow_service.update_workflow_status(
                    workflow_id,
                    WorkflowStatus.ORCHESTRATING,
                    current_agent=agent_id
                )

                # Exécuter l'agent
                result = await self.execute_agent(
                    workflow_id=workflow_id,
                    agent_id=agent_id,
                    context=previous_context,
                    previous_results=agent_results
                )

                agent_results[agent_id] = result

                # Ajouter l'agent aux agents complétés
                await self.workflow_service.add_completed_agent(workflow_id, agent_id)

                # Enrichir le contexte pour le prochain agent
                previous_context[agent_id] = result.output

            # Étape 3: Synthétiser tous les résultats
            logger.info(f"Synthesizing results for workflow {workflow_id}")
            synthesis = await self.synthesize_agents_results(
                user_description=request.user_description,
                agent_results=agent_results,
                constraints=request.constraints,
                preferences=request.preferences
            )

            # Étape 4: Créer projet dans Archon
            logger.info(f"Creating Archon project for workflow {workflow_id}")
            archon_project_id, knowledge_source_id = await self.create_archon_project(
                workflow_id=workflow_id,
                synthesis=synthesis
            )

            await self.workflow_service.set_archon_project(
                workflow_id,
                archon_project_id,
                knowledge_source_id
            )

            # Étape 5: Statut GENERATING
            await self.workflow_service.update_workflow_status(
                workflow_id,
                WorkflowStatus.GENERATING,
                current_agent=None
            )

            # Étape 6: Générer le code final à partir de la synthèse
            logger.info(f"Generating final code for workflow {workflow_id}")
            generated_code = await self.generate_code_from_synthesis(synthesis)

            # Étape 7: Créer le ZIP
            logger.info(f"Creating ZIP for workflow {workflow_id}")
            zip_path = await self.zip_service.create_project_zip(
                workflow_id=workflow_id,
                generated_code=generated_code,
                synthesis=synthesis,
                agent_results=agent_results,
                include_docs=True,
                include_tests=True,
                include_deployment=True
            )

            await self.workflow_service.set_zip_file_path(workflow_id, zip_path)

            # Étape 8: Statut COMPLETED
            await self.workflow_service.update_workflow_status(
                workflow_id,
                WorkflowStatus.COMPLETED
            )

            logger.info(f"BMAD orchestration completed for workflow {workflow_id}")

        except Exception as e:
            logger.error(f"Error in BMAD orchestration for workflow {workflow_id}: {e}", exc_info=True)
            await self.workflow_service.update_workflow_status(
                workflow_id,
                WorkflowStatus.FAILED
            )

    # ==================== Agents Execution ====================

    async def execute_agent(
        self,
        workflow_id: str,
        agent_id: str,
        context: Dict[str, Any],
        previous_results: Dict[str, AgentResult]
    ) -> AgentResult:
        """
        Exécute un agent BMAD individuel

        Args:
            workflow_id: ID du workflow
            agent_id: ID de l'agent à exécuter
            context: Contexte de base
            previous_results: Résultats des agents précédents

        Returns:
            AgentResult avec la sortie de l'agent
        """
        start_time = time.time()

        try:
            # Récupérer l'exécution d'agent depuis la DB
            executions = await self.workflow_service.get_agent_executions(workflow_id)
            execution = next((e for e in executions if e["agent_id"] == agent_id), None)

            if not execution:
                raise ValueError(f"Agent execution not found for agent {agent_id}")

            execution_id = execution["id"]

            # Marquer comme démarré
            await self.workflow_service.start_agent_execution(execution_id)

            # Construire le prompt pour l'agent
            agent_prompt = self._build_agent_prompt(
                agent_id=agent_id,
                context=context,
                previous_results=previous_results
            )

            # Appeler l'agent via l'API Groq (gratuit) avec httpx
            logger.info(f"Calling agent {agent_id} with Groq API")

            if not self.groq_api_key:
                raise ValueError("GROQ_API_KEY not set")

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.groq_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": self._get_agent_system_prompt(agent_id)},
                            {"role": "user", "content": agent_prompt}
                        ],
                        "max_tokens": 4096,
                        "temperature": 0.7
                    },
                    timeout=120.0
                )
                response.raise_for_status()
                data = response.json()

            output = data["choices"][0]["message"]["content"]
            execution_time = int(time.time() - start_time)

            # Extraire un résumé (premiers 200 caractères)
            summary = output[:200] + "..." if len(output) > 200 else output

            # Marquer comme complété
            await self.workflow_service.complete_agent_execution(
                execution_id=execution_id,
                output_result=output,
                output_summary=summary,
                execution_time_seconds=execution_time
            )

            logger.info(f"Agent {agent_id} completed in {execution_time}s")

            return AgentResult(
                agent_id=agent_id,
                agent_name=execution["agent_name"],
                status=AgentStatus.COMPLETED,
                output=output,
                summary=summary,
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = int(time.time() - start_time)
            logger.error(f"Error executing agent {agent_id}: {e}", exc_info=True)

            # Marquer comme échoué
            if execution:
                await self.workflow_service.fail_agent_execution(
                    execution_id=execution_id,
                    error_message=str(e)
                )

            return AgentResult(
                agent_id=agent_id,
                agent_name=execution["agent_name"] if execution else f"{agent_id} Agent",
                status=AgentStatus.FAILED,
                execution_time=execution_time,
                error=str(e)
            )

    # ==================== Code Generation ====================

    async def generate_code_from_prompt(
        self,
        prompt: str,
        tech_stack: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Génère du code à partir d'un prompt direct - utilise Groq par défaut"""

        tech_stack_str = ", ".join(tech_stack) if tech_stack else "best modern stack"

        system_prompt = f"""You are an expert full-stack developer. Generate production-ready code based on the user's requirements.

Tech Stack: {tech_stack_str}

Return a complete project structure with:
- Source code files
- Configuration files
- Documentation
- Tests (if applicable)

Format your response as a structured JSON with file paths and contents."""

        # Utiliser Groq par défaut (gratuit et rapide)
        generated_content = await self._call_llm(system_prompt, prompt)

        return {
            "raw_output": generated_content,
            "tech_stack": tech_stack,
            "prompt": prompt
        }

    async def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Appel LLM avec fallback entre providers"""

        # Essayer Groq d'abord (gratuit)
        if self.groq_api_key:
            try:
                return await self._call_groq(system_prompt, user_prompt)
            except Exception as e:
                logger.warning(f"Groq failed: {e}, trying fallback...")

        # Fallback OpenAI
        if self.openai_api_key:
            try:
                return await self._call_openai(system_prompt, user_prompt)
            except Exception as e:
                logger.warning(f"OpenAI failed: {e}, trying fallback...")

        # Fallback Anthropic
        if self.anthropic_api_key:
            try:
                return await self._call_anthropic(system_prompt, user_prompt)
            except Exception as e:
                logger.error(f"All LLM providers failed: {e}")
                raise

        raise Exception("No LLM provider configured or all failed")

    async def _call_groq(self, system_prompt: str, user_prompt: str) -> str:
        """Appel à Groq API"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "max_tokens": 8000,
                    "temperature": 0.7
                },
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def _call_openai(self, system_prompt: str, user_prompt: str) -> str:
        """Appel à OpenAI API"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "max_tokens": 8000,
                    "temperature": 0.7
                },
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def _call_anthropic(self, system_prompt: str, user_prompt: str) -> str:
        """Appel à Anthropic API"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.anthropic_api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "claude-3-5-sonnet-20241022",
                    "max_tokens": 8000,
                    "system": system_prompt,
                    "messages": [
                        {"role": "user", "content": user_prompt}
                    ]
                },
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()
            return data["content"][0]["text"]

    async def generate_code_from_synthesis(
        self,
        synthesis: ProjectSynthesis
    ) -> Dict[str, Any]:
        """Génère du code final à partir de la synthèse BMAD"""

        system_prompt = """You are an expert full-stack developer. Generate production-ready code based on the comprehensive project synthesis from multiple specialized agents.

Generate a complete, working application with:
- All source code files
- Configuration files
- Tests
- Documentation
- Deployment configs

Format your response as structured code files."""

        user_prompt = f"""# Project Synthesis

**Project Name**: {synthesis.project_name}

**Description**: {synthesis.description}

**Tech Stack**: {', '.join(synthesis.tech_stack)}

## Architecture
{synthesis.architecture or 'N/A'}

## Requirements
{synthesis.requirements or 'N/A'}

## API Design
{synthesis.api_design or 'N/A'}

## UI Components
{synthesis.ui_components or 'N/A'}

## Deployment Strategy
{synthesis.deployment_strategy or 'N/A'}

## Test Plan
{synthesis.test_plan or 'N/A'}

---

Based on this comprehensive synthesis, generate the complete project code."""

        # Utiliser le système multi-provider
        generated_content = await self._call_llm(system_prompt, user_prompt)

        return {
            "raw_output": generated_content,
            "synthesis": synthesis.dict(),
            "tech_stack": synthesis.tech_stack
        }

    # ==================== Synthesis ====================

    async def synthesize_agents_results(
        self,
        user_description: str,
        agent_results: Dict[str, AgentResult],
        constraints: Any,
        preferences: Any
    ) -> ProjectSynthesis:
        """Synthétise les résultats de tous les agents en un projet cohérent"""

        # Extraire les informations de chaque agent
        architecture = agent_results.get("architect", AgentResult(agent_id="architect", agent_name="Architect", status=AgentStatus.FAILED)).output
        requirements = agent_results.get("pm", AgentResult(agent_id="pm", agent_name="PM", status=AgentStatus.FAILED)).output
        api_design = agent_results.get("backend", AgentResult(agent_id="backend", agent_name="Backend", status=AgentStatus.FAILED)).output
        ui_components = agent_results.get("frontend", AgentResult(agent_id="frontend", agent_name="Frontend", status=AgentStatus.FAILED)).output
        deployment_strategy = agent_results.get("devops", AgentResult(agent_id="devops", agent_name="DevOps", status=AgentStatus.FAILED)).output
        test_plan = agent_results.get("qa", AgentResult(agent_id="qa", agent_name="QA", status=AgentStatus.FAILED)).output

        # Détecter le tech stack depuis l'architecture
        tech_stack = self._extract_tech_stack(architecture or "")

        # Construire la documentation complète
        full_documentation = f"""# {user_description}

## Architecture
{architecture or 'Not defined'}

## Requirements
{requirements or 'Not defined'}

## API Design
{api_design or 'Not defined'}

## UI Components
{ui_components or 'Not defined'}

## Deployment Strategy
{deployment_strategy or 'Not defined'}

## Test Plan
{test_plan or 'Not defined'}
"""

        # Contributions des agents
        agents_contributions = {
            result.agent_id: result.output or ""
            for result in agent_results.values()
        }

        return ProjectSynthesis(
            project_name=self._extract_project_name(user_description),
            description=user_description,
            tech_stack=tech_stack,
            architecture=architecture,
            requirements=requirements,
            api_design=api_design,
            ui_components=ui_components,
            deployment_strategy=deployment_strategy,
            test_plan=test_plan,
            full_documentation=full_documentation,
            agents_contributions=agents_contributions
        )

    # ==================== Archon Integration ====================

    async def save_to_archon(
        self,
        workflow_id: str,
        project_name: str,
        content: Dict[str, Any],
        tech_stack: Optional[List[str]]
    ) -> tuple[int, str]:
        """Sauvegarde dans Archon (mode direct)"""
        try:
            # S'assurer que les tables existent
            await self.archon_service.ensure_archon_tables_exist()

            # Créer la source de connaissance
            knowledge_content = f"""# {project_name}

## Generated Code

```
{content.get('raw_output', 'No output')}
```

## Tech Stack
{', '.join(tech_stack) if tech_stack else 'N/A'}

## Prompt
{content.get('prompt', 'N/A')}

---
Generated by Bolt SuperPower (Direct Mode)
Workflow ID: {workflow_id}
"""

            knowledge_id = await self.archon_service.create_knowledge_source(
                name=f"Bolt Direct: {project_name}",
                source_type="bolt_direct",
                content=knowledge_content,
                metadata={
                    "workflow_id": workflow_id,
                    "tech_stack": tech_stack,
                    "mode": "direct"
                }
            )

            # Créer le projet Archon
            project_id = await self.archon_service.create_project(
                name=project_name,
                description=f"Generated via Bolt Direct Mode\nWorkflow: {workflow_id}",
                knowledge_source_id=knowledge_id,
                features=tech_stack or [],
                metadata={
                    "workflow_id": workflow_id,
                    "mode": "direct"
                }
            )

            logger.info(f"Saved to Archon: project_id={project_id}, knowledge_id={knowledge_id}")
            return (project_id, knowledge_id)

        except Exception as e:
            logger.error(f"Error saving to Archon: {e}", exc_info=True)
            return (0, "error")

    async def create_archon_project(
        self,
        workflow_id: str,
        synthesis: ProjectSynthesis
    ) -> tuple[int, str]:
        """Crée un projet complet dans Archon (mode BMAD)"""
        try:
            # S'assurer que les tables existent
            await self.archon_service.ensure_archon_tables_exist()

            # Créer la source de connaissance avec la documentation complète
            knowledge_id = await self.archon_service.create_knowledge_source(
                name=f"Bolt BMAD: {synthesis.project_name}",
                source_type="bolt_bmad",
                content=synthesis.full_documentation,
                metadata={
                    "workflow_id": workflow_id,
                    "tech_stack": synthesis.tech_stack,
                    "mode": "bmad",
                    "agents_contributions": list(synthesis.agents_contributions.keys())
                }
            )

            # Créer le projet Archon
            project_id = await self.archon_service.create_project(
                name=synthesis.project_name,
                description=synthesis.description,
                knowledge_source_id=knowledge_id,
                features=synthesis.tech_stack,
                metadata={
                    "workflow_id": workflow_id,
                    "mode": "bmad",
                    "agents_used": list(synthesis.agents_contributions.keys())
                }
            )

            # Ajouter les documents par agent
            for agent_id, contribution in synthesis.agents_contributions.items():
                doc_name = f"{agent_id.upper()}_OUTPUT.md"
                await self.archon_service.add_project_document(
                    project_id=project_id,
                    doc_name=doc_name,
                    doc_type="agent_output",
                    content=contribution
                )

            # Ajouter les documents de synthèse
            if synthesis.architecture:
                await self.archon_service.add_project_document(
                    project_id=project_id,
                    doc_name="ARCHITECTURE.md",
                    doc_type="documentation",
                    content=synthesis.architecture
                )

            if synthesis.requirements:
                await self.archon_service.add_project_document(
                    project_id=project_id,
                    doc_name="REQUIREMENTS.md",
                    doc_type="documentation",
                    content=synthesis.requirements
                )

            if synthesis.api_design:
                await self.archon_service.add_project_document(
                    project_id=project_id,
                    doc_name="API_DESIGN.md",
                    doc_type="documentation",
                    content=synthesis.api_design
                )

            logger.info(f"Created Archon project {project_id} with {len(synthesis.agents_contributions)} agent documents")

            return (project_id, knowledge_id)

        except Exception as e:
            logger.error(f"Error creating Archon project: {e}", exc_info=True)
            return (0, "error")

    # ==================== Helper Methods ====================

    def _build_agent_prompt(
        self,
        agent_id: str,
        context: Dict[str, Any],
        previous_results: Dict[str, AgentResult]
    ) -> str:
        """Construit le prompt pour un agent"""

        base_context = f"""User Project Description:
{context.get('user_description', 'N/A')}

Constraints:
- Budget: {context.get('constraints', {}).get('budget', 'N/A')}
- Timeline: {context.get('constraints', {}).get('timeline', 'N/A')}
- Team Size: {context.get('constraints', {}).get('team_size', 'N/A')}

Preferences:
- Tech Stack: {context.get('preferences', {}).get('tech_stack', 'N/A')}
- Deployment: {context.get('preferences', {}).get('deployment', 'N/A')}
"""

        if previous_results:
            base_context += "\n\nPrevious Agents Results:\n"
            for agent_id_prev, result in previous_results.items():
                base_context += f"\n### {result.agent_name}\n{result.summary}\n"

        return base_context

    def _get_agent_system_prompt(self, agent_id: str) -> str:
        """Retourne le system prompt pour un agent"""

        prompts = {
            "architect": "You are Winston, a senior software architect. Analyze the project requirements and propose a robust, scalable architecture. Define the tech stack, patterns, and system design.",
            "pm": "You are John, an experienced project manager. Create user stories, define MVP features, and prioritize requirements. Break down the project into manageable tasks.",
            "backend": "You are Amelia, a backend development expert. Design the API endpoints, database schema, authentication, and business logic.",
            "frontend": "You are Sara, a frontend development expert. Design UI/UX wireframes, component architecture, and state management strategy.",
            "devops": "You are Carlos, a DevOps engineer. Define CI/CD pipeline, infrastructure as code, deployment strategy, and monitoring.",
            "qa": "You are Murat, a QA engineer. Create a comprehensive test plan with unit, integration, and e2e test strategies."
        }

        return prompts.get(agent_id, f"You are a specialized {agent_id} agent. Provide expert analysis for this project.")

    def _extract_project_name(self, description: str) -> str:
        """Extrait un nom de projet depuis la description"""
        # Simple heuristique: prendre les 5 premiers mots
        words = description.split()[:5]
        return " ".join(words).title()

    def _extract_tech_stack(self, architecture_text: str) -> List[str]:
        """Extrait le tech stack depuis le texte d'architecture"""
        # Heuristique simple: chercher des technologies communes
        common_techs = [
            "React", "Vue", "Angular", "Next.js", "TypeScript", "JavaScript",
            "Python", "FastAPI", "Django", "Flask", "Node.js", "Express",
            "PostgreSQL", "MongoDB", "Redis", "MySQL",
            "Docker", "Kubernetes", "AWS", "Vercel", "Netlify",
            "TailwindCSS", "Material-UI", "Bootstrap"
        ]

        found_techs = []
        for tech in common_techs:
            if tech.lower() in architecture_text.lower():
                found_techs.append(tech)

        return found_techs if found_techs else ["React", "FastAPI", "PostgreSQL"]
