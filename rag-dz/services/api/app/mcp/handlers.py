"""
MCP Handlers - Agent-specific message handlers
Implements the business logic for each agent in the MCP ecosystem
"""
import asyncio
import logging
from typing import Dict, Any, Optional
import uuid

from app.mcp.server import (
    mcp_server,
    MCPMessage,
    MCPMessageType,
    MCPAgent,
    MCPContext
)
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class BMADHandler:
    """
    BMAD Agent Handler
    Manages PM, Architect, Developer, Analyst, Tester agents
    """

    AGENT_PERSONAS = {
        MCPAgent.BMAD_PM: {
            "name": "John (PM)",
            "role": "Product Manager",
            "system_prompt": """Tu es John, Product Manager expert.
Tu excelles dans:
- La définition des besoins utilisateurs
- La priorisation des features
- La gestion du backlog
- La communication avec les stakeholders

Réponds toujours de manière structurée avec des user stories et des critères d'acceptation."""
        },
        MCPAgent.BMAD_ARCHITECT: {
            "name": "Winston (Architect)",
            "role": "System Architect",
            "system_prompt": """Tu es Winston, Architecte Système senior.
Tu excelles dans:
- La conception d'architectures scalables
- Les choix technologiques
- Les patterns de design
- La documentation technique

Fournis toujours des diagrammes en ASCII et des justifications techniques."""
        },
        MCPAgent.BMAD_DEVELOPER: {
            "name": "Amelia (Developer)",
            "role": "Senior Developer",
            "system_prompt": """Tu es Amelia, Développeuse Full-Stack senior.
Tu excelles dans:
- L'implémentation de code propre
- Les best practices
- Les tests unitaires
- Le refactoring

Fournis toujours du code fonctionnel et bien commenté."""
        },
        MCPAgent.BMAD_ANALYST: {
            "name": "Mary (Analyst)",
            "role": "Business Analyst",
            "system_prompt": """Tu es Mary, Business Analyst experte.
Tu excelles dans:
- L'analyse des processus métier
- La documentation fonctionnelle
- Les spécifications détaillées
- La validation des requirements

Fournis toujours des analyses structurées avec des métriques."""
        },
        MCPAgent.BMAD_TESTER: {
            "name": "Murat (Tester)",
            "role": "Test Architect",
            "system_prompt": """Tu es Murat, Architecte QA senior.
Tu excelles dans:
- Les stratégies de test
- L'automatisation des tests
- La couverture de code
- Les tests de performance

Fournis toujours des plans de test détaillés et des cas de test."""
        }
    }

    async def handle(self, message: MCPMessage) -> MCPMessage:
        """Handle BMAD agent messages"""
        tool = message.payload.get("tool")
        params = message.payload.get("parameters", {})
        session_id = message.payload.get("session_id")

        try:
            if tool == "bmad_brainstorm":
                result = await self._brainstorm(params, session_id)
            elif tool == "bmad_plan":
                result = await self._create_plan(params, session_id)
            elif tool == "bmad_review":
                result = await self._review(params, message.target)
            else:
                result = await self._generic_chat(params, message.target)

            return MCPMessage(
                id=str(uuid.uuid4()),
                type=MCPMessageType.TOOL_RESULT,
                source=message.target,
                target=message.source,
                payload={"success": True, "result": result},
                correlation_id=message.id
            )

        except Exception as e:
            logger.error(f"BMAD handler error: {e}")
            return MCPMessage(
                id=str(uuid.uuid4()),
                type=MCPMessageType.ERROR,
                source=message.target,
                target=message.source,
                payload={"success": False, "error": str(e)},
                correlation_id=message.id
            )

    async def _brainstorm(self, params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Run brainstorming session"""
        from app.services.bmad_orchestrator import bmad_orchestrator

        project_name = params.get("project_name")
        description = params.get("description")

        # Get PM perspective
        pm_result = await bmad_orchestrator.chat(
            agent="pm",
            message=f"Analyse ce projet et propose des user stories:\nNom: {project_name}\nDescription: {description}",
            session_id=session_id
        )

        # Get Architect perspective
        architect_result = await bmad_orchestrator.chat(
            agent="architect",
            message=f"Propose une architecture pour ce projet:\n{pm_result}",
            session_id=session_id
        )

        # Update MCP context
        mcp_server.update_context(session_id, {
            "project_name": project_name,
            "project_description": description,
            "brainstorm_result": f"## PM Analysis\n{pm_result}\n\n## Architecture\n{architect_result}",
            "current_stage": "brainstorm_complete"
        })

        return {
            "pm_analysis": pm_result,
            "architecture_proposal": architect_result,
            "session_id": session_id
        }

    async def _create_plan(self, params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Create detailed project plan"""
        from app.services.bmad_orchestrator import bmad_orchestrator

        brainstorm = params.get("brainstorm_result")

        # Developer input
        dev_result = await bmad_orchestrator.chat(
            agent="developer",
            message=f"Crée un plan d'implémentation technique basé sur:\n{brainstorm}",
            session_id=session_id
        )

        # Tester input
        test_result = await bmad_orchestrator.chat(
            agent="tester",
            message=f"Crée une stratégie de test pour ce projet:\n{brainstorm}",
            session_id=session_id
        )

        project_plan = f"""# Plan Projet

## Plan d'Implémentation
{dev_result}

## Stratégie de Test
{test_result}
"""

        # Update context
        mcp_server.update_context(session_id, {
            "project_plan": project_plan,
            "current_stage": "planning_complete"
        })

        return {
            "implementation_plan": dev_result,
            "test_strategy": test_result,
            "full_plan": project_plan
        }

    async def _review(self, params: Dict[str, Any], agent: MCPAgent) -> Dict[str, Any]:
        """Review content with specified agent"""
        from app.services.bmad_orchestrator import bmad_orchestrator

        content = params.get("content")
        review_type = params.get("review_type", "general")

        agent_name = agent.value.replace("bmad_", "")
        result = await bmad_orchestrator.chat(
            agent=agent_name,
            message=f"Review this {review_type}:\n{content}"
        )

        return {"review": result, "agent": agent_name}

    async def _generic_chat(self, params: Dict[str, Any], agent: MCPAgent) -> Dict[str, Any]:
        """Generic chat with BMAD agent"""
        from app.services.bmad_orchestrator import bmad_orchestrator

        message = params.get("message", "")
        agent_name = agent.value.replace("bmad_", "")

        result = await bmad_orchestrator.chat(
            agent=agent_name,
            message=message
        )

        return {"response": result, "agent": agent_name}


class ArchonHandler:
    """
    Archon Agent Handler
    Manages knowledge base operations
    """

    async def handle(self, message: MCPMessage) -> MCPMessage:
        """Handle Archon messages"""
        tool = message.payload.get("tool")
        params = message.payload.get("parameters", {})
        session_id = message.payload.get("session_id")

        try:
            if tool == "archon_create_kb":
                result = await self._create_knowledge_base(params, session_id)
            elif tool == "archon_query":
                result = await self._query(params)
            elif tool == "archon_index":
                result = await self._index_content(params)
            else:
                result = {"error": f"Unknown tool: {tool}"}

            return MCPMessage(
                id=str(uuid.uuid4()),
                type=MCPMessageType.TOOL_RESULT,
                source=MCPAgent.ARCHON,
                target=message.source,
                payload={"success": True, "result": result},
                correlation_id=message.id
            )

        except Exception as e:
            logger.error(f"Archon handler error: {e}")
            return MCPMessage(
                id=str(uuid.uuid4()),
                type=MCPMessageType.ERROR,
                source=MCPAgent.ARCHON,
                target=message.source,
                payload={"success": False, "error": str(e)},
                correlation_id=message.id
            )

    async def _create_knowledge_base(self, params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Create a new knowledge base for the project"""
        project_name = params.get("project_name")
        documents = params.get("documents", [])

        # Get context for project info
        context = mcp_server.get_context(session_id)

        # Create KB content from project artifacts
        kb_content = []
        if context:
            if context.brainstorm_result:
                kb_content.append({
                    "content": context.brainstorm_result,
                    "metadata": {"type": "brainstorm", "project": project_name}
                })
            if context.project_plan:
                kb_content.append({
                    "content": context.project_plan,
                    "metadata": {"type": "plan", "project": project_name}
                })

        # Index in Archon (via BigRAG)
        from app.bigrag import bigrag_service

        kb_id = f"project_{session_id}"
        for doc in kb_content:
            await bigrag_service.index(
                content=doc["content"],
                metadata=doc["metadata"],
                collection=kb_id
            )

        # Update context
        mcp_server.update_context(session_id, {
            "knowledge_base_id": kb_id,
            "current_stage": "kb_created"
        })

        return {
            "kb_id": kb_id,
            "documents_indexed": len(kb_content),
            "project": project_name
        }

    async def _query(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Query the knowledge base"""
        from app.services.advanced_rag import advanced_rag

        query = params.get("query")
        kb_id = params.get("kb_id", "default")
        limit = params.get("limit", 5)

        result = await advanced_rag.retrieve(
            query=query,
            collection=kb_id,
            limit=limit,
            use_reranking=True
        )

        return {
            "query": query,
            "results": result.get("results", []),
            "total": result.get("total", 0)
        }

    async def _index_content(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Index new content"""
        from app.bigrag import bigrag_service

        content = params.get("content")
        metadata = params.get("metadata", {})
        kb_id = params.get("kb_id", "default")

        await bigrag_service.index(
            content=content,
            metadata=metadata,
            collection=kb_id
        )

        return {"indexed": True, "kb_id": kb_id}


class BoltHandler:
    """
    Bolt Agent Handler
    Manages code generation and deployment
    """

    async def handle(self, message: MCPMessage) -> MCPMessage:
        """Handle Bolt messages"""
        tool = message.payload.get("tool")
        params = message.payload.get("parameters", {})
        session_id = message.payload.get("session_id")

        try:
            if tool == "bolt_generate":
                result = await self._generate(params, session_id)
            elif tool == "bolt_preview":
                result = await self._preview(params, session_id)
            elif tool == "bolt_deploy":
                result = await self._deploy(params, session_id)
            else:
                result = {"error": f"Unknown tool: {tool}"}

            return MCPMessage(
                id=str(uuid.uuid4()),
                type=MCPMessageType.TOOL_RESULT,
                source=MCPAgent.BOLT,
                target=message.source,
                payload={"success": True, "result": result},
                correlation_id=message.id
            )

        except Exception as e:
            logger.error(f"Bolt handler error: {e}")
            return MCPMessage(
                id=str(uuid.uuid4()),
                type=MCPMessageType.ERROR,
                source=MCPAgent.BOLT,
                target=message.source,
                payload={"success": False, "error": str(e)},
                correlation_id=message.id
            )

    async def _generate(self, params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Generate code with Bolt"""
        prompt = params.get("prompt")
        template = params.get("template", "react")
        model = params.get("model", "claude-3-5-sonnet")

        # Get context for additional info
        context = mcp_server.get_context(session_id)

        # Enhance prompt with context
        enhanced_prompt = prompt
        if context:
            if context.rag_context:
                enhanced_prompt = f"{prompt}\n\nContexte RAG:\n{context.rag_context}"
            if context.architecture:
                enhanced_prompt = f"{enhanced_prompt}\n\nArchitecture:\n{context.architecture}"

        # Update context
        mcp_server.update_context(session_id, {
            "generated_prompt": enhanced_prompt,
            "bolt_session_id": f"bolt_{session_id}",
            "current_stage": "prompt_generated"
        })

        return {
            "prompt": enhanced_prompt,
            "template": template,
            "model": model,
            "bolt_session_id": f"bolt_{session_id}",
            "ready": True
        }

    async def _preview(self, params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Get preview URL for Bolt project"""
        context = mcp_server.get_context(session_id)

        return {
            "session_id": session_id,
            "preview_url": f"http://localhost:5173/preview/{session_id}",
            "status": "ready" if context else "not_started"
        }

    async def _deploy(self, params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Deploy project from Bolt"""
        target = params.get("target", "vercel")

        # Update context
        mcp_server.update_context(session_id, {
            "current_stage": "deployed"
        })

        return {
            "session_id": session_id,
            "target": target,
            "status": "deployment_initiated",
            "message": f"Déploiement vers {target} en cours..."
        }


class OrchestratorHandler:
    """
    Orchestrator Handler
    Manages the full workflow pipeline
    """

    async def handle(self, message: MCPMessage) -> MCPMessage:
        """Handle Orchestrator messages"""
        tool = message.payload.get("tool")
        params = message.payload.get("parameters", {})

        try:
            if tool == "workflow_start":
                result = await self._start_workflow(params)
            else:
                result = {"error": f"Unknown tool: {tool}"}

            return MCPMessage(
                id=str(uuid.uuid4()),
                type=MCPMessageType.TOOL_RESULT,
                source=MCPAgent.ORCHESTRATOR,
                target=message.source,
                payload={"success": True, "result": result},
                correlation_id=message.id
            )

        except Exception as e:
            logger.error(f"Orchestrator handler error: {e}")
            return MCPMessage(
                id=str(uuid.uuid4()),
                type=MCPMessageType.ERROR,
                source=MCPAgent.ORCHESTRATOR,
                target=message.source,
                payload={"success": False, "error": str(e)},
                correlation_id=message.id
            )

    async def _start_workflow(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Start the full BMAD → Archon → Bolt workflow"""
        project_name = params.get("project_name")
        description = params.get("description")

        # Create session
        session_id = str(uuid.uuid4())[:8]
        context = mcp_server.create_context(session_id)
        context.project_name = project_name
        context.project_description = description

        # Step 1: BMAD Brainstorm
        brainstorm_result = await mcp_server.call_tool(
            "bmad_brainstorm",
            {"project_name": project_name, "description": description},
            MCPAgent.ORCHESTRATOR,
            session_id
        )

        # Step 2: BMAD Planning
        plan_result = await mcp_server.call_tool(
            "bmad_plan",
            {"session_id": session_id, "brainstorm_result": brainstorm_result.get("result", {}).get("pm_analysis", "")},
            MCPAgent.ORCHESTRATOR,
            session_id
        )

        # Step 3: Archon KB
        kb_result = await mcp_server.call_tool(
            "archon_create_kb",
            {"session_id": session_id, "project_name": project_name},
            MCPAgent.ORCHESTRATOR,
            session_id
        )

        # Step 4: Generate Bolt Prompt
        context = mcp_server.get_context(session_id)
        bolt_prompt = f"""# Projet: {project_name}

## Description
{description}

## Plan d'Implémentation
{context.project_plan if context else 'N/A'}

## Instructions
Génère une application complète basée sur ce plan.
Inclus tous les fichiers nécessaires avec une structure claire.
"""

        bolt_result = await mcp_server.call_tool(
            "bolt_generate",
            {"prompt": bolt_prompt, "session_id": session_id},
            MCPAgent.ORCHESTRATOR,
            session_id
        )

        return {
            "session_id": session_id,
            "stages_completed": ["brainstorm", "planning", "kb_creation", "prompt_generation"],
            "brainstorm": brainstorm_result,
            "plan": plan_result,
            "knowledge_base": kb_result,
            "bolt": bolt_result,
            "status": "workflow_complete"
        }


# Initialize handlers
bmad_handler = BMADHandler()
archon_handler = ArchonHandler()
bolt_handler = BoltHandler()
orchestrator_handler = OrchestratorHandler()


def register_handlers():
    """Register all handlers with MCP server"""
    # BMAD agents
    for agent in [MCPAgent.BMAD_PM, MCPAgent.BMAD_ARCHITECT, MCPAgent.BMAD_DEVELOPER,
                  MCPAgent.BMAD_ANALYST, MCPAgent.BMAD_TESTER]:
        mcp_server.register_agent_handler(agent, bmad_handler.handle)

    # Archon
    mcp_server.register_agent_handler(MCPAgent.ARCHON, archon_handler.handle)

    # Bolt
    mcp_server.register_agent_handler(MCPAgent.BOLT, bolt_handler.handle)

    # Orchestrator
    mcp_server.register_agent_handler(MCPAgent.ORCHESTRATOR, orchestrator_handler.handle)

    logger.info("All MCP handlers registered")


# Auto-register on import
register_handlers()
