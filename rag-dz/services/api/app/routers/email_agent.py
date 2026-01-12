"""
Email Agent Router
API endpoints for email assistance
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from ..services.email_agent_service import (
    improve_email,
    summarize_email,
    draft_reply,
    analyze_email_for_appointment,
    formalize_email,
    translate_email,
    EmailAssistRequest,
    EmailAnalysisRequest,
    EmailAssistResponse,
    EMAIL_AGENT_CONFIG,
)

router = APIRouter(prefix="/api/agent", tags=["email-agent"])


class EmailAssistAPIRequest(BaseModel):
    draft: str
    context: Optional[str] = None
    action: str = "improve"  # improve, summarize, reply, formalize, translate
    target_language: Optional[str] = None
    original_email: Optional[str] = None
    reply_intent: Optional[str] = None


class EmailAnalyzeAPIRequest(BaseModel):
    content: str
    from_email: str
    subject: str
    task: str = "analyze_email_for_appointment"


@router.post("/email-assist")
async def assist_email(request: EmailAssistAPIRequest):
    """
    Email assistance endpoint
    Actions: improve, summarize, reply, formalize, translate
    """
    try:
        if request.action == "improve":
            result = await improve_email(request.draft, request.context)
            return {"improved_text": result}

        elif request.action == "summarize":
            result = await summarize_email(request.draft)
            return {"summary": result}

        elif request.action == "reply":
            if not request.original_email or not request.reply_intent:
                raise HTTPException(
                    status_code=400,
                    detail="original_email and reply_intent required for reply action"
                )
            result = await draft_reply(request.original_email, request.reply_intent)
            return {"improved_text": result}

        elif request.action == "formalize":
            result = await formalize_email(request.draft)
            return {"improved_text": result}

        elif request.action == "translate":
            target = request.target_language or "en"
            result = await translate_email(request.draft, target)
            return {"improved_text": result}

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown action: {request.action}"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze", response_model=EmailAssistResponse)
async def analyze_email(request: EmailAnalyzeAPIRequest):
    """
    Analyze email for automated processing
    Used by n8n workflows for auto-reply decisions
    """
    try:
        if request.task == "analyze_email_for_appointment":
            result = await analyze_email_for_appointment(
                content=request.content,
                from_email=request.from_email,
                subject=request.subject,
            )
            return result

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown task: {request.task}"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/email-agent/info")
async def get_agent_info():
    """Get Email Agent configuration"""
    return EMAIL_AGENT_CONFIG


@router.get("/agents")
async def list_agents():
    """List all available agents including Email Agent"""
    agents = [
        {
            "id": "email",
            "name": "Assistant Email",
            "icon": "Mail",
            "description": "Lire, résumer, et rédiger des emails professionnels",
            "color": "#EA4335",
            "capabilities": [
                "Lecture et résumé d'emails",
                "Rédaction de réponses",
                "Amélioration du style",
                "Traduction",
                "Analyse pour auto-réponse"
            ]
        },
        {
            "id": "calendar",
            "name": "Assistant Agenda",
            "icon": "Calendar",
            "description": "Gérer les rendez-vous et événements",
            "color": "#4285F4",
            "capabilities": [
                "Création d'événements",
                "Rappels de RDV",
                "Gestion des disponibilités"
            ]
        },
        {
            "id": "rag",
            "name": "Assistant Documents",
            "icon": "FileText",
            "description": "Recherche dans la base de connaissances",
            "color": "#34A853",
            "capabilities": [
                "Recherche sémantique",
                "Résumé de documents",
                "Questions-réponses"
            ]
        },
        {
            "id": "bmad",
            "name": "BMAD Orchestrator",
            "icon": "Workflow",
            "description": "Orchestration de projets",
            "color": "#9C27B0",
            "capabilities": [
                "Création de projets",
                "Coordination d'agents",
                "Export vers Bolt"
            ]
        },
        {
            "id": "code",
            "name": "Assistant Code",
            "icon": "Code",
            "description": "Aide au développement",
            "color": "#FF9800",
            "capabilities": [
                "Génération de code",
                "Review et suggestions",
                "Documentation"
            ]
        },
        {
            "id": "general",
            "name": "Assistant Général",
            "icon": "Bot",
            "description": "Assistant polyvalent",
            "color": "#607D8B",
            "capabilities": [
                "Questions générales",
                "Rédaction",
                "Analyse"
            ]
        }
    ]
    return {"agents": agents}
