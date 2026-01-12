"IAFactory Video Studio Pro - Agent Storyboarder
Découpage visuel et génération de prompts pour les scènes.

"

from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

from pydantic import BaseModel, Field

from . import (
    BaseAgent, 
    AgentConfig, 
    AgentResponse,
    JSONOutputMixin,
    CostTrackingMixin,
    VideoScript # Importé pour le typage
)
from config import settings, agent_configs


logger = logging.getLogger(__name__)


# === MODÈLES DE DONNÉES ===

class Scene(BaseModel):
    """Représente une scène visuelle du storyboard."""
    scene_number: int
    timestamp_start: float
    timestamp_end: float
    description: str  # Description de ce qui se passe
    visual_prompt: str # Prompt pour générer l'image/vidéo de cette scène
    b_roll_suggestion: Optional[str] = None


class Storyboard(BaseModel):
    """Représente un storyboard complet pour un script."""
    id: str = Field(default_factory=lambda: f"storyboard_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    script_id: str
    scenes: List[Scene]
    thumbnail_prompt: str # Prompt optimisé pour la miniature (thumbnail)
    status: Literal["draft", "completed"] = "draft"


# === AGENT STORYBOARDER ===

class StoryboarderAgent(BaseAgent, JSONOutputMixin, CostTrackingMixin):
    """
    Agent Storyboarder - Découpe un script en scènes visuelles.
    
    Utilise Claude Sonnet 4 pour la rapidité et la précision.
    """
    
    SYSTEM_PROMPT = """Tu es un réalisateur et un expert en storyboard. Ton rôle est de transformer un script textuel en une séquence de scènes visuelles claires et réalisables.

## Ta mission:
1.  **Décomposer le script** en scènes logiques, en se basant sur les segments fournis.
2.  **Générer un prompt visuel** pour chaque scène. Ce prompt doit être détaillé et direct, prêt à être utilisé par une IA de génération d'images/vidéos (style Midjourney, DALL-E, Luma, Kling).
3.  **Suggérer du B-roll** pour enrichir la narration visuelle.
4.  **Créer un prompt pour la miniature (thumbnail)** qui est captivant, optimisé pour le clic (CTR), et qui résume l'essence de la vidéo.

## Règles pour les prompts visuels:
- Style: Cinématique, photoréaliste, haute définition.
- Format: "Un plan [type de plan] de [sujet], [action], [éclairage], [détails de l'environnement]. --ar 16:9 --style raw"
- Exemple: "Un gros plan d'un visage d'homme algérien de 30 ans, air surpris, regardant directement la caméra. Éclairage dramatique venant du côté, fond flou d'un bureau moderne. --ar 16:9 --style raw"

## Format de sortie:
Tu dois TOUJOURS retourner un JSON valide avec la structure spécifiée."""

    def __init__(self):
        config = AgentConfig(
            name="Storyboarder",
            model=agent_configs.STORYBOARDER["model"],
            temperature=agent_configs.STORYBOARDER["temperature"],
            max_tokens=agent_configs.STORYBOARDER["max_tokens"],
            retry_attempts=agent_configs.STORYBOARDER["retry_attempts"],
            timeout=agent_configs.STORYBOARDER["timeout"],
            system_prompt=self.SYSTEM_PROMPT
        )
        super().__init__(config)
    
    async def process(self, input_data: Any) -> AgentResponse:
        """Point d'entrée principal pour la création du storyboard."""
        if not isinstance(input_data, dict):
            return AgentResponse(success=False, agent_name=self.name, error="Input data must be a dictionary.")
            
        script_obj = VideoScript(**input_data)
        return await self.decompose_script(script_obj)
    
    async def decompose_script(self, script: VideoScript) -> AgentResponse:
        """
        Décompose un script en scènes et génère les prompts visuels.
        """
        start_time = datetime.utcnow()
        
        script_content_for_prompt = "\n".join(
            [f"- Segment {i+1} ({s.timestamp_start}s - {s.timestamp_end}s): {s.content}" 
             for i, s in enumerate(script.segments)]
        )
        
        prompt = f"""Décompose le script suivant en scènes visuelles et génère les prompts correspondants.

## Script
- Titre: {script.title}
- Hook: {script.hook}
- Intro: {script.intro}
- Segments:
{script_content_for_prompt}
- Outro: {script.outro}

## FORMAT DE SORTIE (JSON)
Retourne UNIQUEMENT un JSON valide avec cette structure:

{{
    "scenes": [
        {{
            "scene_number": 1,
            "timestamp_start": 0.0,
            "timestamp_end": 3.0,
            "description": "Description de la scène du hook.",
            "visual_prompt": "Prompt visuel pour le hook (style cinématique). --ar 16:9",
            "b_roll_suggestion": "Suggestion de B-roll si pertinent"
        }},
        {{
            "scene_number": 2,
            "timestamp_start": 3.1,
            "timestamp_end": 15.0,
            "description": "Description de la scène de l'intro.",
            "visual_prompt": "Prompt visuel pour l'intro. --ar 16:9",
            "b_roll_suggestion": "Plan d'illustration."
        }}
    ],
    "thumbnail_prompt": "Prompt très détaillé pour une miniature YouTube hyper-réaliste et intrigante, liée au coeur du sujet."
}}
"""
        try:
            # Appel au LLM
            response = await self.call_llm(
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parser la réponse JSON
            storyboard_data = await self.parse_json_response(response["content"])
            
            if "error" in storyboard_data:
                return AgentResponse(
                    success=False,
                    agent_name=self.name,
                    error=f"Erreur parsing JSON: {storyboard_data.get('raw', 'Unknown')[:200]}",
                    tokens_used=response["tokens_used"],
                    processing_time=response["processing_time"],
                )
            
            # Construire l'objet Storyboard
            storyboard = Storyboard(
                script_id=script.id,
                scenes=[Scene(**s) for s in storyboard_data.get("scenes", [])],
                thumbnail_prompt=storyboard_data.get("thumbnail_prompt", "Générer une miniature par défaut.")
            )
            
            token_cost = self.calculate_token_cost(
                "storyboard_claude_sonnet", 
                response["tokens_used"] / 1000
            )
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            logger.info(
                f"[{self.name}] Storyboard créé pour le script '{script.id}' avec {len(storyboard.scenes)} scènes."
            )
            
            return AgentResponse(
                success=True,
                data=storyboard.model_dump(),
                agent_name=self.name,
                tokens_used=response["tokens_used"],
                processing_time=processing_time,
            )

        except Exception as e:
            logger.error(f"[{self.name}] Erreur décomposition script: {str(e)}")
            return AgentResponse(
                success=False,
                data=None,
                agent_name=self.name,
                error=str(e),
            )

# === FACTORY FUNCTION ===

def create_storyboarder_agent() -> StoryboarderAgent:
    """Crée une instance de l'agent Storyboarder."""
    return StoryboarderAgent()
