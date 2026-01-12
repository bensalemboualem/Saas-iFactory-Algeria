"""
IAFactory Video Studio Pro - Agent Growth Hacker
Optimisation virale du contenu vidéo.
"""

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
    VideoScript
)
from config import settings, agent_configs


logger = logging.getLogger(__name__)


# === MODÈLES DE DONNÉES ===

class ViralAnalysisReport(BaseModel):
    """Rapport d'analyse du potentiel viral."""
    viral_score: int = Field(..., description="Score de 0 à 100")
    strengths: List[str] = Field(..., description="Points forts du script")
    weaknesses: List[str] = Field(..., description="Points faibles à améliorer")
    suggestions: List[str] = Field(..., description="Suggestions concrètes d'amélioration")
    peak_moment: str = Field(..., description="Le moment le plus fort du script")


class TitleVariations(BaseModel):
    """Variations de titres optimisés."""
    titles: List[Dict[str, str]] # Ex: [{"text": "Titre 1", "style": "Question"}, ...]


class OptimizedHashtags(BaseModel):
    """Hashtags optimisés par plateforme."""
    hashtags: List[str]
    strategy: str # Ex: "Mix de hashtags populaires et de niche"


# === AGENT GROWTH HACKER ===

class GrowthHackerAgent(BaseAgent, JSONOutputMixin, CostTrackingMixin):
    """
    Agent Growth Hacker - Analyse et optimise le contenu pour la viralité.
    
    Utilise un modèle rapide (comme Grok ou Claude Sonnet) pour l'analyse de tendances.
    """
    
    SYSTEM_PROMPT = """Tu es un expert en growth hacking et en stratégies de contenu viral sur les réseaux sociaux (YouTube, TikTok, Instagram).

## Ta mission:
Analyser un script ou un sujet et fournir des recommandations concrètes pour maximiser sa portée et son engagement.

## Facteurs d'analyse:
- **Hook (Accroche):** Est-ce que les 3 premières secondes sont percutantes ?
- **Émotion:** Le script suscite-t-il une émotion forte (curiosité, choc, humour, etc.) ?
- **Rythme:** Y a-t-il une bonne dynamique ?
- **Sujet:** Le sujet est-il tendance ou pertinent pour l'audience cible ?
- **Rétention:** Quels sont les points où l'audience risque de décrocher ?

## Format de sortie:
Tu dois TOUJOURS retourner un JSON valide et concis avec la structure demandée."""

    def __init__(self):
        config = AgentConfig(
            name="GrowthHacker",
            model=agent_configs.GROWTH_HACKER["model"],
            temperature=agent_configs.GROWTH_HACKER["temperature"],
            max_tokens=agent_configs.GROWTH_HACKER["max_tokens"],
            retry_attempts=agent_configs.GROWTH_HACKER["retry_attempts"],
            timeout=agent_configs.GROWTH_HACKER["timeout"],
            system_prompt=self.SYSTEM_PROMPT
        )
        super().__init__(config)
    
    async def process(self, input_data: Any) -> AgentResponse:
        """Point d'entrée principal. L'action est déterminée par le contenu de l'input."""
        action = input_data.get("action")
        payload = input_data.get("payload")

        if action == "analyze_script":
            script = VideoScript(**payload)
            return await self.analyze_viral_potential(script)
        elif action == "generate_titles":
            return await self.generate_title_variations(**payload)
        elif action == "optimize_hashtags":
            return await self.optimize_hashtags(**payload)
        else:
            return AgentResponse(success=False, agent_name=self.name, error=f"Action inconnue: {action}")

    async def analyze_viral_potential(self, script: VideoScript) -> AgentResponse:
        """Analyse le potentiel viral d'un script complet."""
        
        prompt = f"""Analyse le potentiel viral de ce script vidéo.

## Script
- Titre: {script.title}
- Hook: {script.hook}
- Contenu: {" ".join([s.content for s in script.segments])}
- CTA: {script.cta}

## FORMAT DE SORTIE (JSON)
Retourne UNIQUEMENT un JSON valide avec cette structure:

{{
    "viral_score": 85,
    "strengths": ["Excellent hook", "Sujet tendance"],
    "weaknesses": ["Le milieu du script est un peu lent"],
    "suggestions": ["Ajouter un son populaire en fond", "Raccourcir le segment 3"],
    "peak_moment": "Le moment où le secret est révélé à 2:30."
}}
"""
        try:
            response = await self.call_llm(messages=[{"role": "user", "content": prompt}])
            report_data = await self.parse_json_response(response["content"])

            if "error" in report_data:
                return AgentResponse(success=False, agent_name=self.name, error="Erreur parsing JSON")

            report = ViralAnalysisReport(**report_data)
            return AgentResponse(success=True, data=report.model_dump(), agent_name=self.name)
        
        except Exception as e:
            logger.error(f"[{self.name}] Erreur analyse virale: {e}")
            return AgentResponse(success=False, agent_name=self.name, error=str(e))

    async def generate_title_variations(self, topic: str, count: int = 5) -> AgentResponse:
        """Génère des variations de titres optimisés pour le clic."""
        
        prompt = f"""Génère {count} titres ultra-optimisés pour le clic (CTR) pour une vidéo sur le sujet: "{topic}".

Varie les styles: question, affirmation choc, liste, etc.

## FORMAT DE SORTIE (JSON)
{{
    "titles": [
        {{"text": "Pourquoi vous ratez TOUS cet investissement.", "style": "Question provocante"}},
        {{"text": "Les 3 MEILLEURS placements de 2025.", "style": "Liste"}},
        {{"text": "J'ai testé l'investissement secret des millionnaires.", "style": "Storytelling"}}
    ]
}}
"""
        try:
            response = await self.call_llm(messages=[{"role": "user", "content": prompt}])
            titles_data = await self.parse_json_response(response["content"])
            
            if "error" in titles_data:
                return AgentResponse(success=False, agent_name=self.name, error="Erreur parsing JSON")

            titles = TitleVariations(**titles_data)
            return AgentResponse(success=True, data=titles.model_dump(), agent_name=self.name)

        except Exception as e:
            logger.error(f"[{self.name}] Erreur génération titres: {e}")
            return AgentResponse(success=False, agent_name=self.name, error=str(e))

    async def optimize_hashtags(self, topic: str, platform: Literal["youtube", "tiktok", "instagram"]) -> AgentResponse:
        """Génère une liste de hashtags optimisés."""

        prompt = f"""Génère une liste de hashtags optimisés pour la plateforme "{platform}" sur le sujet: "{topic}".

Combine des hashtags populaires, de niche, et spécifiques au sujet.

## FORMAT DE SORTIE (JSON)
{{
    "hashtags": ["#conseil", "#finance", "#investissementdz", "#bourse2025"],
    "strategy": "Un mix de hashtags larges pour la portée, et de niche ('#investissementdz') pour cibler une audience qualifiée."
}}
"""
        try:
            response = await self.call_llm(messages=[{"role": "user", "content": prompt}])
            hashtags_data = await self.parse_json_response(response["content"])

            if "error" in hashtags_data:
                return AgentResponse(success=False, agent_name=self.name, error="Erreur parsing JSON")

            hashtags = OptimizedHashtags(**hashtags_data)
            return AgentResponse(success=True, data=hashtags.model_dump(), agent_name=self.name)

        except Exception as e:
            logger.error(f"[{self.name}] Erreur optimisation hashtags: {e}")
            return AgentResponse(success=False, agent_name=self.name, error=str(e))


# === FACTORY FUNCTION ===

def create_growth_hacker_agent() -> GrowthHackerAgent:
    """Crée une instance de l'agent GrowthHacker."""
    return GrowthHackerAgent()
