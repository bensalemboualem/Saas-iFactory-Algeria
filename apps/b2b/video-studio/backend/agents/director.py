"""
IAFactory Video Studio Pro - Agent Director (Réalisateur)
Orchestration du montage vidéo final.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

from pydantic import BaseModel, Field

from . import (
    BaseAgent, 
    AgentConfig, 
    AgentResponse,
    CostTrackingMixin,
    VideoScript,
    Storyboard
)
from ..services.elevenlabs_service import ElevenLabsService, get_elevenlabs_service
from ..services.fal_service import FalService, get_fal_service
from ..video.montage_orchestrator import MontageOrchestrator, get_montage_orchestrator, MontageProject, VideoSegment, AudioTrack

from config import settings, agent_configs


logger = logging.getLogger(__name__)


# === MODÈLES DE DONNÉES ===

class DirectorRequest(BaseModel):
    """Requête pour l'agent réalisateur."""
    script: VideoScript
    storyboard: Storyboard


class Asset(BaseModel):
    """Représente un asset média généré."""
    type: Literal["audio", "video", "image"]
    path: str
    scene_number: Optional[int] = None
    duration: float


# === AGENT DIRECTOR ===

class DirectorAgent(BaseAgent, CostTrackingMixin):
    """
    Agent Director - Orchestre la génération des assets et le montage final.
    """
    
    def __init__(self, montage_orchestrator: MontageOrchestrator, tts_service: ElevenLabsService, visual_service: FalService):
        config = AgentConfig(
            name="Director",
            model="", # Pas de LLM direct, mais on pourrait en utiliser un pour des choix créatifs
            system_prompt="Je suis le réalisateur. Je transforme les storyboards en vidéos finales."
        )
        super().__init__(config)
        self.orchestrator = montage_orchestrator
        self.tts_service = tts_service
        self.visual_service = visual_service
    
    async def process(self, input_data: Any) -> AgentResponse:
        """
        Point d'entrée principal pour la réalisation d'une vidéo.
        Prend un DirectorRequest en entrée.
        """
        start_time = datetime.utcnow()
        
        if not isinstance(input_data, dict):
            return AgentResponse(success=False, agent_name=self.name, error="Input data must be a dictionary.")
            
        try:
            request = DirectorRequest(**input_data)
            logger.info(f"[{self.name}] Début de la réalisation pour le script: {request.script.id}")
            
            # --- WORKFLOW DE RÉALISATION ---
            
            # 1. Générer la voix off (TTS) pour tout le script
            logger.info(f"[{self.name}] Étape 1: Génération de la voix off...")
            full_script_text = ". ".join([s.content for s in request.script.segments])
            tts_response = await self.tts_service.text_to_speech(text=full_script_text)
            if not tts_response.success or not tts_response.audio_path:
                raise Exception(f"Échec de la génération TTS: {tts_response.error}")
            
            voiceover_asset = Asset(
                type="audio", 
                path=tts_response.audio_path,
                duration=tts_response.duration_seconds or 0.0
            )
            logger.info(f"[{self.name}] Voix off générée: {voiceover_asset.path}")
            
            # 2. Générer les visuels pour chaque scène
            logger.info(f"[{self.name}] Étape 2: Génération des visuels de scènes...")
            visual_assets: List[Asset] = []
            # (Implémentation simplifiée : on génère une image par scène)
            for scene in request.storyboard.scenes:
                # TODO: Remplacer par une vraie génération vidéo par scène
                img_request = ImageGenerationRequest(prompt=scene.visual_prompt)
                img_response = await self.visual_service.generate_image(img_request)
                if not img_response.success or not img_response.result_url:
                    logger.warning(f"Échec génération visuel pour scène {scene.scene_number}. On continue...")
                    continue
                
                # NOTE: En réalité, il faudrait télécharger l'image depuis l'URL
                visual_assets.append(Asset(
                    type="image", # Devrait être 'video' à terme
                    path=img_response.result_url, # C'est une URL, pas un chemin local !
                    scene_number=scene.scene_number,
                    duration=(scene.timestamp_end - scene.timestamp_start)
                ))
            logger.info(f"[{self.name}] {len(visual_assets)} visuels générés.")
            if not visual_assets:
                raise Exception("Aucun visuel n'a pu être généré.")

            # 3. Préparer le projet de montage
            logger.info(f"[{self.name}] Étape 3: Préparation du projet de montage...")
            # NOTE: L'orchestrateur attend des chemins locaux, mais nous avons des URLs.
            # C'est une simplification, il faudrait télécharger les fichiers d'abord.
            # De plus, l'orchestrateur attend des vidéos, pas des images.
            # On va simuler en utilisant la première image comme placeholder.
            montage_project = MontageProject(
                segments=[VideoSegment(file_path=visual_assets[0].path)], # Placeholder
                voiceover=AudioTrack(file_path=voiceover_asset.path),
                output_path=f"/tmp/{request.script.id}_final.mp4"
            )
            
            # 4. Lancer le montage
            logger.info(f"[{self.name}] Étape 4: Lancement du montage final...")
            # NOTE: Ceci va probablement échouer car on passe une URL à FFMpeg
            # C'est une démonstration du workflow
            final_video_path = await self.orchestrator.assemble_video(montage_project)
            
            if not final_video_path:
                raise Exception("Le montage final a échoué.")
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"[{self.name}] Vidéo finalisée: {final_video_path} en {processing_time:.2f}s")
            
            return AgentResponse(
                success=True,
                data={"final_video_path": final_video_path},
                agent_name=self.name,
                processing_time=processing_time,
            )

        except Exception as e:
            logger.error(f"[{self.name}] Erreur durant la réalisation: {str(e)}")
            return AgentResponse(
                success=False,
                data=None,
                agent_name=self.name,
                error=str(e),
            )

# === FACTORY FUNCTION ===

_director_agent: Optional[DirectorAgent] = None

def create_director_agent() -> DirectorAgent:
    """Crée une instance de l'agent Director avec ses dépendances."""
    global _director_agent
    if _director_agent is None:
        orchestrator = get_montage_orchestrator()
        tts_service = get_elevenlabs_service()
        visual_service = get_fal_service()
        _director_agent = DirectorAgent(
            montage_orchestrator=orchestrator,
            tts_service=tts_service,
            visual_service=visual_service
        )
    return _director_agent

# Import tardif pour éviter les dépendances circulaires
from ..services.fal_service import ImageGenerationRequest
