"""
IAFactory Video Studio Pro - API Routes pour la Vidéo

Intégré avec le système de crédits IAFactory:
- Vérifie le plan Pro+ pour la génération vidéo
- Déduit les crédits dynamiques selon durée/résolution
- Renvoie 402 si crédits insuffisants
"""

from typing import List, Optional, Literal
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Header
import logging

from ...services.minimax_service import MiniMaxService, get_minimax_service, VideoGenerationStatus as MiniMaxStatus
from ...services.fal_service import FalService, get_fal_service, FalGenerationResponse as FalStatus
from ...services.elevenlabs_service import ElevenLabsService, get_elevenlabs_service, TTSRequest
from ...services.credits_proxy import credits_proxy
from ...agents.director import DirectorAgent, create_director_agent, DirectorRequest
from ...agents import AgentResponse, VideoScript, Storyboard

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/video",
    tags=["Video"],
)


# === MODÈLES DE REQUÊTES & RÉPONSES ===

class VideoClipGenerationRequest(BaseModel):
    """Requête pour générer un clip vidéo."""
    provider: Literal["minimax", "fal", "kling", "runway", "sora"] = "fal"
    prompt: str = Field(..., example="Un plan cinématique d'Alger la nuit.")
    duration_seconds: int = Field(4, gt=0, le=15)
    aspect_ratio: Literal["16:9", "9:16", "1:1"] = "16:9"
    resolution: Literal["480p", "720p", "1080p", "4k"] = "720p"
    tenant_id: Optional[str] = None  # ID du tenant pour vérification crédits


class JobStatusResponse(BaseModel):
    """Réponse unifiée pour le statut d'une tâche."""
    provider: str
    job_id: str
    status: str
    progress: Optional[int] = None
    result_url: Optional[str] = None
    error: Optional[str] = None


class FinalRenderRequest(BaseModel):
    """Requête pour lancer le rendu final d'une vidéo."""
    script_id: str
    storyboard_id: str


# === DÉPENDANCES ===

async def get_minimax() -> MiniMaxService:
    return get_minimax_service()

async def get_fal() -> FalService:
    return get_fal_service()

async def get_director() -> DirectorAgent:
    return create_director_agent()


# === ROUTES ===

@router.post("/generate-clip", response_model=JobStatusResponse, status_code=status.HTTP_202_ACCEPTED)
async def generate_video_clip(
    request: VideoClipGenerationRequest,
    authorization: Optional[str] = Header(None),
    minimax_service: MiniMaxService = Depends(get_minimax),
    fal_service: FalService = Depends(get_fal)
):
    """
    Lance la génération asynchrone d'un clip vidéo via un fournisseur spécifié.

    Crédits:
    - Vérifie que le tenant a un plan Pro+ (vidéo requise)
    - Calcule le coût dynamique selon durée/résolution
    - Déduit les crédits avant génération
    - Renvoie 402 si crédits insuffisants
    """
    logger.info(f"API: Demande de génération de clip via {request.provider} avec le prompt: '{request.prompt[:30]}...'")

    # === VÉRIFICATION DES CRÉDITS ===
    tenant_id = request.tenant_id
    token = authorization.replace("Bearer ", "") if authorization else ""

    if tenant_id:
        # 1. Vérifier que le plan permet la vidéo (Pro+)
        await credits_proxy.require_video_plan(tenant_id, token)

        # 2. Mapper le provider au nom de service pour les crédits
        service_map = {
            "minimax": "minimax-video",
            "fal": "lumalabs",
            "kling": "kling-ai",
            "runway": "runway-gen3",
            "sora": "sora-2"
        }
        service_name = service_map.get(request.provider, "minimax-video")

        # 3. Calculer le coût dynamique
        cost = await credits_proxy.get_dynamic_cost(
            service=service_name,
            duration_seconds=request.duration_seconds,
            resolution=request.resolution,
            token=token
        )

        logger.info(f"Coût estimé: {cost} crédits pour {service_name} ({request.duration_seconds}s, {request.resolution})")

        # 4. Déduire les crédits (lève 402 si insuffisant)
        deduction = await credits_proxy.deduct_credits(
            tenant_id=tenant_id,
            service=service_name,
            token=token,
            metadata={
                "provider": request.provider,
                "duration_seconds": request.duration_seconds,
                "resolution": request.resolution,
                "prompt": request.prompt[:100]
            }
        )

        logger.info(f"Crédits déduits: {deduction.get('deducted', 0)}, reste: {deduction.get('remaining', 0)}")

    status_response: Optional[MiniMaxStatus | FalStatus] = None

    if request.provider == "minimax":
        from ...services.minimax_service import VideoGenerationRequest as MiniMaxRequest
        minimax_request = MiniMaxRequest(
            prompt=request.prompt, 
            duration_seconds=request.duration_seconds, 
            aspect_ratio=request.aspect_ratio
        )
        status_response = await minimax_service.text_to_video(minimax_request)
        
    elif request.provider == "fal":
        from ...services.fal_service import FalVideoGenerationRequest
        fal_request = FalVideoGenerationRequest(
            prompt=request.prompt,
            duration_seconds=request.duration_seconds
        )
        status_response = await fal_service.text_to_video(fal_request)
        
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fournisseur de vidéo non supporté.")

    if not status_response or not status_response.success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Échec du lancement de la tâche de génération vidéo: {status_response.error if status_response else 'Erreur inconnue'}"
        )
        
    return JobStatusResponse(
        provider=request.provider,
        job_id=status_response.job_id,
        status=status_response.status,
    )


@router.get("/jobs/{provider}/{job_id}/status", response_model=JobStatusResponse)
async def get_job_status(
    provider: str,
    job_id: str,
    minimax_service: MiniMaxService = Depends(get_minimax),
    fal_service: FalService = Depends(get_fal)
):
    """
    Vérifie le statut d'une tâche de génération de clip vidéo.
    """
    logger.info(f"API: Vérification du statut pour la tâche {job_id} chez {provider}")
    
    status_response: Optional[MiniMaxStatus | FalStatus] = None
    
    if provider == "minimax":
        status_response = await minimax_service.get_generation_status(job_id)
    elif provider == "fal":
        status_response = await fal_service.get_job_status(job_id)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fournisseur de vidéo non supporté.")

    if not status_response or not status_response.success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tâche {job_id} non trouvée ou erreur: {status_response.error if status_response else 'Erreur inconnue'}"
        )
    
    return JobStatusResponse(
        provider=provider,
        job_id=job_id,
        status=status_response.status,
        progress=getattr(status_response, 'progress', None),
        result_url=getattr(status_response, 'video_url', getattr(status_response, 'result_url', None)),
        error=status_response.error,
    )


@router.post("/render-final", status_code=status.HTTP_202_ACCEPTED)
async def render_final_video(
    request: FinalRenderRequest,
    background_tasks: BackgroundTasks,
    director: DirectorAgent = Depends(get_director)
):
    """
    Lance le rendu final d'une vidéo en tâche de fond.
    (Implémentation fictive car nécessite une DB pour récupérer script & storyboard)
    """
    logger.info(f"API: Lancement du rendu final pour le script {request.script_id}")

    # Récupération fictive du script et du storyboard
    if request.script_id != "dummy_script_id" or request.storyboard_id != "dummy_storyboard_id":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Script ou Storyboard non trouvé.")

    dummy_script = VideoScript(
        id="dummy_script_id", title="Titre Fictif", topic="Sujet Fictif",
        target_audience="Audience Fictive", platform="youtube", duration_target=30,
        language="fr", hook="Hook", intro="Intro", segments=[], outro="Outro", cta="CTA"
    )
    dummy_storyboard = Storyboard(
        id="dummy_storyboard_id", script_id="dummy_script_id", scenes=[],
        thumbnail_prompt="Prompt miniature"
    )
    
    director_request = DirectorRequest(script=dummy_script, storyboard=dummy_storyboard)
    
    # Lancement de la tâche de fond
    background_tasks.add_task(director.process, director_request.model_dump())
    
    return {"message": "Le rendu final a été lancé en tâche de fond.", "script_id": request.script_id}


@router.get("/preview/{video_id}")
async def get_video_preview(video_id: str):
    """
    Retourne une URL de prévisualisation pour un clip ou une vidéo finale.
    (Implémentation fictive)
    """
    logger.info(f"API: Demande de prévisualisation pour la vidéo {video_id}")
    # En réalité, on retournerait une URL signée S3 ou un lien vers un fichier local/servi
    return {"preview_url": f"https://cdn.iafactory.ai/previews/{video_id}.mp4"}
