"""
API Coordination BMAD → Archon → Bolt.DIY
Endpoints pour orchestration automatique de projets
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime
import logging

from app.services.project_coordinator import coordinator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/coordination", tags=["Coordination"])


class Message(BaseModel):
    role: str
    content: str
    agent: Optional[str] = None
    timestamp: Optional[str] = None


class ConversationRequest(BaseModel):
    messages: List[Message]
    agents_used: List[str]
    auto_create_project: bool = True


class ProjectCreationResponse(BaseModel):
    success: bool
    project_id: Optional[str] = None
    knowledge_source_id: Optional[str] = None
    bolt_url: Optional[str] = None
    archon_project_url: Optional[str] = None
    error: Optional[str] = None
    analysis: Optional[Dict[str, Any]] = None


@router.post("/analyze-conversation")
async def analyze_conversation(request: ConversationRequest):
    """
    Analyse une conversation multi-agents pour détecter un projet

    Retourne:
        - is_project: bool
        - project_name: str
        - description: str
        - technologies: List[str]
        - requirements: List[str]
    """
    try:
        messages_dict = [msg.dict() for msg in request.messages]

        analysis = await coordinator.analyze_conversation(
            messages=messages_dict,
            agents_used=request.agents_used
        )

        return {
            "success": True,
            "analysis": analysis
        }

    except Exception as e:
        logger.error(f"Error analyzing conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-project", response_model=ProjectCreationResponse)
async def create_project_from_conversation(request: ConversationRequest):
    """
    Crée automatiquement un projet Archon depuis une conversation BMAD

    Workflow:
    1. Analyse la conversation pour extraire infos projet
    2. Crée le projet dans Archon
    3. Convertit transcript en knowledge base
    4. Génère URL Bolt.DIY avec contexte

    Returns:
        - project_id: ID du projet Archon
        - knowledge_source_id: ID de la knowledge base
        - bolt_url: URL pour lancer Bolt.DIY avec contexte
        - archon_project_url: URL du projet dans Archon
    """
    try:
        messages_dict = [msg.dict() for msg in request.messages]

        # 1. Analyser la conversation
        logger.info(f"🔍 Analyse de {len(messages_dict)} messages avec {len(request.agents_used)} agents")

        analysis = await coordinator.analyze_conversation(
            messages=messages_dict,
            agents_used=request.agents_used
        )

        if not analysis.get("is_project"):
            return ProjectCreationResponse(
                success=False,
                error="La conversation ne semble pas définir un projet",
                analysis=analysis
            )

        logger.info(f"✅ Projet détecté: {analysis.get('project_name')}")

        # 2. Créer le projet si auto_create_project
        if request.auto_create_project:
            result = await coordinator.create_archon_project(
                project_data=analysis,
                conversation_transcript=messages_dict
            )

            return ProjectCreationResponse(
                success=result["success"],
                project_id=result.get("project_id"),
                knowledge_source_id=result.get("knowledge_source_id"),
                bolt_url=result.get("bolt_url"),
                archon_project_url=result.get("archon_project_url"),
                error=result.get("error"),
                analysis=analysis
            )

        else:
            # Retourner seulement l'analyse
            return ProjectCreationResponse(
                success=True,
                analysis=analysis
            )

    except Exception as e:
        logger.error(f"❌ Error creating project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/finalize-and-launch")
async def finalize_and_launch_bolt(
    project_id: str,
    knowledge_source_id: str
):
    """
    Finalise un projet et génère commande pour lancer Bolt.DIY

    Returns:
        - bolt_command: Commande shell pour lancer Bolt
        - bolt_url: URL directe
        - project_context: Contexte du projet
    """
    try:
        # Générer URL Bolt avec contexte
        bolt_url = coordinator._generate_bolt_url(project_id, knowledge_source_id)

        # Commande pour lancer Bolt.DIY avec contexte
        bolt_command = f"""
# Lancer Bolt.DIY avec contexte projet Archon
cd bolt-diy
npm run dev -- --project-id={project_id} --knowledge-source={knowledge_source_id}

# Ou ouvrir directement dans navigateur:
# {bolt_url}
"""

        return {
            "success": True,
            "bolt_url": bolt_url,
            "bolt_command": bolt_command.strip(),
            "project_id": project_id,
            "knowledge_source_id": knowledge_source_id,
            "instructions": [
                "1. Ouvre Bolt.DIY avec l'URL fournie",
                "2. Le contexte du projet Archon sera automatiquement chargé",
                "3. Les agents BMAD seront disponibles via MCP",
                "4. La knowledge base du projet sera accessible pour RAG"
            ]
        }

    except Exception as e:
        logger.error(f"Error finalizing project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def coordination_health():
    """Health check du service de coordination"""
    return {
        "status": "healthy",
        "service": "project_coordination",
        "archon_url": coordinator.archon_url,
        "bolt_url": coordinator.bolt_url
    }
