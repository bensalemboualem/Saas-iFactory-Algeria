"""
API Routes pour l'Agent Orchestrateur #20
Endpoints pour analyser, synthétiser et ordonner la production
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime, timezone

from app.services.orchestrator_service import orchestrator_service
from app.routers.coordination import create_project_from_conversation

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/orchestrator", tags=["orchestrator"])


# ============================================
# REQUEST/RESPONSE MODELS
# ============================================

class Message(BaseModel):
    role: str
    content: str
    agent: Optional[str] = None


class AnalyzeRequest(BaseModel):
    messages: List[Message]
    agents_used: List[str]


class SynthesizeRequest(BaseModel):
    messages: List[Message]
    agents_used: List[str]


class ProductionRequest(BaseModel):
    project_id: str
    project_name: str
    tech_stack: List[str]
    knowledge_base_id: str


class CompleteOrchestrationRequest(BaseModel):
    """Orchestration complète: Analyse → Création Projet → Production"""
    messages: List[Message]
    agents_used: List[str]
    auto_produce: bool = True


# ============================================
# ENDPOINTS
# ============================================

@router.get("/health")
async def health_check():
    """Health check de l'orchestrateur"""
    return {
        "status": "healthy",
        "agent": "Orchestrator #20",
        "description": "Agent d'orchestration principal RAG.dz"
    }


@router.post("/analyze-readiness")
async def analyze_project_readiness(request: AnalyzeRequest):
    """
    Analyse si le projet est prêt pour la production

    Vérifie:
    - Architecture définie
    - Requirements clairs
    - Tech stack choisi
    - UX/UI spécifié
    - Tests planifiés

    Returns confidence_score (0-100%) et project_ready (bool)
    """
    try:
        messages_dict = [msg.dict() for msg in request.messages]

        analysis = orchestrator_service.analyze_project_readiness(
            messages=messages_dict,
            agents_used=request.agents_used
        )

        logger.info(f"🎯 Orchestrator Analysis: {analysis['confidence_score']}% ready")

        return {
            "success": True,
            "analysis": analysis
        }

    except Exception as e:
        logger.error(f"Error analyzing project readiness: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/synthesize-knowledge")
async def synthesize_knowledge(request: SynthesizeRequest):
    """
    Synthétise toute la connaissance des agents BMAD
    en un document de knowledge base structuré

    Retourne un document markdown complet avec:
    - Vue d'ensemble
    - Architecture
    - Requirements
    - Tech stack
    - UX/UI
    - Tests
    - Contributions des agents
    """
    try:
        messages_dict = [msg.dict() for msg in request.messages]

        knowledge_doc = orchestrator_service.synthesize_knowledge(
            messages=messages_dict,
            agents_used=request.agents_used
        )

        logger.info(f"📚 Knowledge synthesized: {len(knowledge_doc)} characters")

        return {
            "success": True,
            "knowledge_document": knowledge_doc,
            "agents_consulted": len(request.agents_used),
            "message_count": len(request.messages)
        }

    except Exception as e:
        logger.error(f"Error synthesizing knowledge: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/order-production")
async def order_production(request: ProductionRequest):
    """
    Ordonne à Bolt.DIY de produire le projet final

    Génère une commande de production complète avec:
    - Instructions de génération
    - URL Bolt avec paramètres
    - Référence à la knowledge base
    """
    try:
        production_command = orchestrator_service.order_bolt_production(
            project_id=request.project_id,
            project_name=request.project_name,
            tech_stack=request.tech_stack,
            knowledge_base_id=request.knowledge_base_id
        )

        logger.info(f"🚀 Production ordered for project: {request.project_name}")

        return {
            "success": True,
            "production_command": production_command
        }

    except Exception as e:
        logger.error(f"Error ordering production: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/complete-orchestration")
async def complete_orchestration(request: CompleteOrchestrationRequest):
    """
    Orchestration complète end-to-end:

    1. Analyse de préparation du projet
    2. Si prêt (>80%) → Création projet Archon + KB
    3. Synthèse de la connaissance
    4. Ordre de production à Bolt.DIY

    C'est l'endpoint principal de l'Agent Orchestrateur #20
    """
    try:
        messages_dict = [msg.dict() for msg in request.messages]

        # Étape 1: Analyser si le projet est prêt
        logger.info("🎯 Step 1: Analyzing project readiness...")
        analysis = orchestrator_service.analyze_project_readiness(
            messages=messages_dict,
            agents_used=request.agents_used
        )

        if not analysis["project_ready"]:
            return {
                "success": False,
                "message": "Projet pas encore prêt pour la production",
                "analysis": analysis,
                "next_steps": [
                    f"Complétez: {', '.join(analysis['missing_elements'])}"
                ]
            }

        # Étape 2: Synthétiser la connaissance
        logger.info("📚 Step 2: Synthesizing knowledge...")
        knowledge_doc = orchestrator_service.synthesize_knowledge(
            messages=messages_dict,
            agents_used=request.agents_used
        )

        # Étape 3: Créer le projet dans Archon
        logger.info("🏗️ Step 3: Creating Archon project...")

        # Utiliser l'endpoint de coordination existant
        from app.routers.coordination import CreateProjectRequest
        create_request = CreateProjectRequest(
            messages=[Message(**msg) for msg in messages_dict],
            agents_used=request.agents_used,
            auto_create_project=True
        )
        project_result = await create_project_from_conversation(create_request)

        if not project_result["success"]:
            raise Exception(f"Failed to create project: {project_result.get('error')}")

        # Étape 4: Ordonner la production (si demandé)
        production_command = None
        if request.auto_produce:
            logger.info("🚀 Step 4: Ordering production...")

            # Extraire tech stack depuis l'analyse
            tech_stack = project_result["analysis"].get("technologies", [])

            production_command = orchestrator_service.order_bolt_production(
                project_id=project_result["project_id"],
                project_name=project_result["analysis"].get("project_name", "Untitled"),
                tech_stack=tech_stack,
                knowledge_base_id=project_result["knowledge_source_id"]
            )

        # Résultat final
        return {
            "success": True,
            "orchestration_complete": True,
            "analysis": analysis,
            "project": {
                "project_id": project_result["project_id"],
                "knowledge_base_id": project_result["knowledge_source_id"],
                "archon_url": project_result.get("archon_project_url"),
            },
            "production_command": production_command,
            "bolt_production_url": production_command["bolt_url"] if production_command else None,
            "message": f"✅ Projet créé avec succès! Confidence: {analysis['confidence_score']}%"
        }

    except Exception as e:
        logger.error(f"Error in complete orchestration: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bolt-workflow")
async def create_bolt_workflow(
    task: str,
    description: str,
    target: str = "bolt"
):
    """
    Workflow Bolt.DIY → BMAD → Archon → Bolt

    Permet à Bolt d'envoyer un projet aux agents BMAD,
    qui analysent, créent la KB dans Archon, et retournent
    des instructions pour Bolt
    """
    try:
        import uuid
        workflow_id = str(uuid.uuid4())

        logger.info(f"🚀 Starting Bolt workflow {workflow_id}: {task}")

        # Construire les messages pour l'orchestration
        messages = [
            {"role": "user", "content": f"Task: {task}"},
            {"role": "user", "content": f"Description: {description}"}
        ]

        # Utiliser l'orchestration complète
        from app.routers.orchestrator import CompleteOrchestrationRequest, Message

        orchestration_request = CompleteOrchestrationRequest(
            messages=[Message(**msg) for msg in messages],
            agents_used=["architect", "backend", "frontend", "devops"],
            auto_produce=True
        )

        result = await complete_orchestration(orchestration_request)

        if not result["success"]:
            raise Exception("Orchestration failed")

        return {
            "workflow_id": workflow_id,
            "status": "completed",
            "project_id": result["project"]["project_id"],
            "archon_url": result["project"]["archon_url"],
            "bolt_url": result.get("bolt_production_url"),
            "instructions": result.get("production_command", {}).get("instructions"),
            "message": "✅ Workflow Bolt → BMAD → Archon completed"
        }

    except Exception as e:
        logger.error(f"Bolt workflow failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{project_id}")
async def get_project_status(project_id: int):
    """
    Récupère le status d'un projet orchestré depuis la base de données

    Args:
        project_id: ID du projet

    Returns:
        État d'orchestration complet du projet
    """
    try:
        import psycopg2
        from app.config import settings

        # Connexion à la base de données
        conn = psycopg2.connect(settings.DATABASE_URL)
        cur = conn.cursor()

        # Récupérer l'état d'orchestration
        cur.execute("""
            SELECT
                id, project_id, agents_consulted, messages_count,
                architecture_defined, requirements_clear, tech_stack_chosen,
                ux_specified, tests_planned, confidence_score, project_ready,
                knowledge_base_id, knowledge_doc_path, production_ordered,
                production_command, bolt_url, status, metadata, created_at, updated_at
            FROM orchestrator_state
            WHERE project_id = %s
        """, (project_id,))

        row = cur.fetchone()

        if not row:
            cur.close()
            conn.close()
            return {
                "success": True,
                "project_id": project_id,
                "status": "not_found",
                "message": "No orchestration state found for this project"
            }

        # Construire la réponse
        state = {
            "id": row[0],
            "project_id": row[1],
            "agents_consulted": row[2],
            "messages_count": row[3],
            "signals": {
                "architecture_defined": row[4],
                "requirements_clear": row[5],
                "tech_stack_chosen": row[6],
                "ux_specified": row[7],
                "tests_planned": row[8]
            },
            "confidence_score": row[9],
            "project_ready": row[10],
            "knowledge_base_id": row[11],
            "knowledge_doc_path": row[12],
            "production_ordered": row[13],
            "production_command": row[14],
            "bolt_url": row[15],
            "status": row[16],
            "metadata": row[17],
            "created_at": row[18].isoformat() if row[18] else None,
            "updated_at": row[19].isoformat() if row[19] else None
        }

        # Récupérer les workflows BMAD associés
        cur.execute("""
            SELECT id, workflow_name, workflow_type, status, started_at, completed_at
            FROM bmad_workflows
            WHERE project_id = %s
            ORDER BY created_at DESC
        """, (project_id,))

        workflows = []
        for w_row in cur.fetchall():
            workflows.append({
                "id": w_row[0],
                "workflow_name": w_row[1],
                "workflow_type": w_row[2],
                "status": w_row[3],
                "started_at": w_row[4].isoformat() if w_row[4] else None,
                "completed_at": w_row[5].isoformat() if w_row[5] else None
            })

        cur.close()
        conn.close()

        return {
            "success": True,
            "project_id": project_id,
            "orchestrator_state": state,
            "bmad_workflows": workflows,
            "message": f"Project orchestration status: {state['status']}"
        }

    except Exception as e:
        logger.error(f"Error fetching project status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _compute_missing_signals(row: Dict[str, Any]) -> List[str]:
    """Retourne les signaux manquants basés sur les booléens stockés."""
    signal_map = {
        "architecture_defined": "Architecture",
        "requirements_clear": "Exigences",
        "tech_stack_chosen": "Stack technique",
        "ux_specified": "UX/UI",
        "tests_planned": "Tests",
    }
    missing = [
        label for key, label in signal_map.items()
        if not row.get(key, False)
    ]
    return missing


@router.get("/pending-workflows")
async def get_pending_workflows(limit: int = 10):
    """
    Retourne la liste des orchestrations encore en cours ou en échec.

    Utilisé par n8n pour supervision automatique.
    """
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        from app.config import settings

        conn = psycopg2.connect(settings.DATABASE_URL)
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(
            """
            SELECT
                id,
                project_id,
                agents_consulted,
                messages_count,
                architecture_defined,
                requirements_clear,
                tech_stack_chosen,
                ux_specified,
                tests_planned,
                confidence_score,
                project_ready,
                production_ordered,
                status,
                metadata,
                created_at,
                updated_at
            FROM orchestrator_state
            WHERE status != 'completed'
            ORDER BY created_at ASC
            LIMIT %s
            """,
            (limit,)
        )

        rows = cur.fetchall()
        cur.close()
        conn.close()

        pending = []
        now = datetime.now(timezone.utc)

        for row in rows:
            created_at = row.get("created_at")
            age_minutes = None
            if created_at:
                if created_at.tzinfo is None:
                    created_at = created_at.replace(tzinfo=timezone.utc)
                age_minutes = round((now - created_at).total_seconds() / 60, 2)

            row_dict = dict(row)
            row_dict["missing_signals"] = _compute_missing_signals(row_dict)
            row_dict["age_minutes"] = age_minutes
            pending.append(row_dict)

        return {
            "success": True,
            "count": len(pending),
            "pending": pending,
        }

    except Exception as e:
        logger.error("Error while fetching pending orchestrations", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pending-workflows/{state_id}/recover")
async def recover_pending_workflow(state_id: int):
    """
    Ré-initialise une orchestration en échec afin qu'elle soit retraitée.

    Utilisé par l'orchestrateur n8n pour automatiser les relances.
    """
    try:
        import psycopg2
        from app.config import settings

        conn = psycopg2.connect(settings.DATABASE_URL)
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE orchestrator_state
            SET status = 'analyzing',
                production_ordered = FALSE,
                updated_at = CURRENT_TIMESTAMP,
                metadata = COALESCE(metadata, '{}'::jsonb) || jsonb_build_object(
                    'last_recovery_at', CURRENT_TIMESTAMP
                )
            WHERE id = %s
            RETURNING project_id
            """,
            (state_id,)
        )

        result = cur.fetchone()

        if not result:
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Orchestrator state not found")

        conn.commit()
        cur.close()
        conn.close()

        return {
            "success": True,
            "state_id": state_id,
            "project_id": result[0],
            "message": "Orchestrator state reset to analyzing"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to recover orchestrator state", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
