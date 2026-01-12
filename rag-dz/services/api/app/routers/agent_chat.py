"""
Agent Chat Router - Compatibilité avec Archon-UI

Ce router fournit l'API /api/agent-chat utilisée par l'Archon-UI
et redirige vers les agents BMAD avec support multi-provider LLM.
"""

import os
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/agent-chat", tags=["agent-chat"])

# Storage in-memory (TODO: utiliser Redis ou PostgreSQL en prod)
sessions: Dict[str, dict] = {}
messages_store: Dict[str, List[dict]] = {}


# ===================== Models =====================

class CreateSessionRequest(BaseModel):
    agent_type: Optional[str] = "rag"
    project_id: Optional[str] = None


class CreateSessionResponse(BaseModel):
    session_id: str
    agent_type: str
    created_at: str


class SendMessageRequest(BaseModel):
    message: str
    project_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ChatMessage(BaseModel):
    id: str
    content: str
    sender: str  # 'user' or 'agent'
    timestamp: str
    agent_type: Optional[str] = None


# ===================== LLM Multi-Provider =====================

async def call_llm(system_prompt: str, user_message: str, history: List[dict] = None) -> str:
    """Appelle le LLM avec fallback entre providers (Groq → OpenAI → Anthropic)"""

    # Construire les messages
    messages = [{"role": "system", "content": system_prompt}]
    if history:
        for msg in history[-10:]:  # Garder les 10 derniers messages
            messages.append({
                "role": "user" if msg.get("sender") == "user" else "assistant",
                "content": msg.get("content", "")
            })
    messages.append({"role": "user", "content": user_message})

    # Groq (gratuit et rapide)
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {groq_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": messages,
                        "max_tokens": 2048,
                        "temperature": 0.7
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.warning(f"Groq failed: {e}")

    # OpenAI fallback
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {openai_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4o-mini",
                        "messages": messages,
                        "max_tokens": 2048,
                        "temperature": 0.7
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.warning(f"OpenAI failed: {e}")

    # Anthropic fallback
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": anthropic_key,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "claude-3-5-sonnet-20241022",
                        "max_tokens": 2048,
                        "system": system_prompt,
                        "messages": [{"role": m["role"], "content": m["content"]}
                                    for m in messages if m["role"] != "system"]
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                return data["content"][0]["text"]
        except Exception as e:
            logger.warning(f"Anthropic failed: {e}")

    raise HTTPException(
        status_code=503,
        detail="Aucun provider LLM disponible. Configurez GROQ_API_KEY, OPENAI_API_KEY ou ANTHROPIC_API_KEY."
    )


def get_agent_system_prompt(agent_type: str) -> str:
    """Retourne le prompt système selon le type d'agent

    Pour les agents BMAD (bmm-*, bmb-*, cis-*), charge la personnalité depuis les fichiers YAML.
    """
    # Check if it's a BMAD agent
    if agent_type.startswith(("bmm-", "bmb-", "bmgd-", "cis-", "orchestrator-")):
        try:
            from app.routers.bmad_chat import load_agent_personality
            return load_agent_personality(agent_type)
        except Exception as e:
            logger.warning(f"Failed to load BMAD personality for {agent_type}: {e}")
            # Fall back to generic BMAD prompt
            return f"""Tu es un agent BMAD ({agent_type}).
Tu fais partie de l'écosystème BMAD (Build More, Architect Dreams).
Réponds en français de manière professionnelle et aide l'utilisateur avec son projet."""

    prompts = {
        "rag": """Tu es l'Assistant Knowledge Base de RAG.dz.

Tu aides les utilisateurs à rechercher et comprendre les informations dans leur base de connaissances.

**Tes capacités:**
- Rechercher des documents pertinents
- Résumer des informations
- Répondre aux questions sur le contenu indexé
- Suggérer des documents connexes

**Ton style:**
- Concis et direct
- Cite toujours tes sources quand possible
- Pose des questions pour clarifier
- Réponds en français par défaut

Commence par une salutation amicale.""",

        "bmad": """Tu es un agent BMAD (Build More, Architect Dreams).

Tu suis la philosophie C.O.R.E.:
- **C**ollaboration: Travail humain-AI
- **O**ptimized: Processus optimisés
- **R**eflection: Questions stratégiques
- **E**ngine: Orchestration d'agents

**Ton rôle:**
Guider l'utilisateur dans son projet de développement logiciel.

**Instructions:**
1. Pose des questions pour comprendre le besoin
2. Propose des solutions structurées
3. Suggère les bons agents BMAD pour chaque tâche
4. Reste pratique et pragmatique

Réponds toujours en français.""",

        "bolt": """Tu es l'assistant Bolt.DIY pour la génération de code.

**Tes capacités:**
- Générer du code à partir de descriptions
- Expliquer des architectures
- Suggérer des améliorations
- Déboguer des problèmes

**Ton style:**
- Code propre et documenté
- Explications claires
- Exemples concrets
- Best practices modernes

Réponds en français.""",

        "planning": """Tu es l'Assistant Planning de IA Factory.

**Ton rôle:**
Tu gères les rendez-vous et le planning via conversation naturelle.
Tu peux consulter, créer, modifier et annuler des rendez-vous.

**Tes capacités:**
- Consulter les rendez-vous du jour, de la semaine
- Créer de nouveaux rendez-vous
- Modifier les horaires (reporter)
- Annuler des rendez-vous
- Vérifier les disponibilités
- Envoyer des rappels

**Instructions importantes:**
1. CONFIRME TOUJOURS avant de modifier ou annuler un rendez-vous
2. Demande les informations manquantes (nom, date, heure, motif)
3. Propose des créneaux disponibles quand on te demande de réserver
4. Résume les modifications effectuées
5. Sois précis sur les dates et heures

**Fonctions disponibles:**
- fetchAppointments() : Liste les rendez-vous
- createAppointment(data) : Crée un RDV
- rescheduleAppointment(id, newTime) : Reporte un RDV
- cancelAppointment(id) : Annule un RDV
- fetchAvailableSlots(date) : Créneaux libres

**Format de réponse:**
Quand tu effectues une action, indique clairement:
- ✅ Action réussie avec détails
- ⚠️ Action nécessitant confirmation
- ❌ Action impossible avec raison

Réponds toujours en français de manière professionnelle et efficace."""
    }

    return prompts.get(agent_type, prompts["rag"])


# ===================== Endpoints =====================

@router.get("/status")
async def get_status():
    """Vérifie le statut du service chat"""
    # Vérifier quel provider est disponible
    providers = []
    if os.getenv("GROQ_API_KEY"):
        providers.append("groq")
    if os.getenv("OPENAI_API_KEY"):
        providers.append("openai")
    if os.getenv("ANTHROPIC_API_KEY"):
        providers.append("anthropic")

    return {
        "status": "online" if providers else "degraded",
        "providers": providers,
        "active_sessions": len(sessions),
        "message": "Chat service ready" if providers else "No LLM provider configured"
    }


@router.post("/sessions", response_model=CreateSessionResponse)
async def create_session(request: CreateSessionRequest):
    """Crée une nouvelle session de chat"""
    session_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    sessions[session_id] = {
        "session_id": session_id,
        "agent_type": request.agent_type or "rag",
        "project_id": request.project_id,
        "created_at": now
    }

    messages_store[session_id] = []

    logger.info(f"Created chat session {session_id} with agent_type={request.agent_type}")

    return CreateSessionResponse(
        session_id=session_id,
        agent_type=request.agent_type or "rag",
        created_at=now
    )


@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Récupère les informations d'une session"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]


@router.post("/sessions/{session_id}/send")
async def send_message(session_id: str, request: SendMessageRequest):
    """Envoie un message et reçoit une réponse de l'agent"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    agent_type = session.get("agent_type", "rag")

    # Créer le message utilisateur
    user_msg_id = str(uuid.uuid4())
    user_msg = {
        "id": user_msg_id,
        "content": request.message,
        "sender": "user",
        "timestamp": datetime.utcnow().isoformat(),
        "agent_type": agent_type
    }
    messages_store[session_id].append(user_msg)

    # Obtenir la réponse de l'agent
    try:
        system_prompt = get_agent_system_prompt(agent_type)
        history = messages_store[session_id]

        response_content = await call_llm(system_prompt, request.message, history)

        # Créer le message de réponse
        agent_msg_id = str(uuid.uuid4())
        agent_msg = {
            "id": agent_msg_id,
            "content": response_content,
            "sender": "agent",
            "timestamp": datetime.utcnow().isoformat(),
            "agent_type": agent_type
        }
        messages_store[session_id].append(agent_msg)

        logger.info(f"Chat response generated for session {session_id}")

        return ChatMessage(**agent_msg)

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}/messages")
async def get_messages(session_id: str, after: Optional[str] = None):
    """Récupère les messages d'une session"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = messages_store.get(session_id, [])

    # Si 'after' est spécifié, ne retourner que les nouveaux messages
    if after:
        found = False
        filtered = []
        for msg in messages:
            if found:
                filtered.append(msg)
            if msg["id"] == after:
                found = True
        return [ChatMessage(**m) for m in filtered]

    return [ChatMessage(**m) for m in messages]


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Supprime une session de chat"""
    if session_id in sessions:
        del sessions[session_id]
    if session_id in messages_store:
        del messages_store[session_id]

    return {"status": "deleted", "session_id": session_id}
