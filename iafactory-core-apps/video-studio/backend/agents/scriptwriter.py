"""
IAFactory Video Studio Pro - Agent Scénariste (Scriptwriter)
Génération de scripts optimisés pour le contenu viral
"""

from typing import Any, Dict, List, Literal, Optional
from datetime import datetime
import json
import logging

from pydantic import BaseModel, Field

from . import (
    BaseAgent, 
    AgentConfig, 
    AgentResponse,
    JSONOutputMixin,
    MultilingualMixin,
    CostTrackingMixin
)
from config import settings, agent_configs


logger = logging.getLogger(__name__)


# === MODÈLES DE DONNÉES ===

class ScriptSegment(BaseModel):
    """Segment de script avec timestamps."""
    timestamp_start: float
    timestamp_end: float
    content: str
    speaker: Optional[str] = "host"
    visual_direction: str
    b_roll_suggestion: Optional[str] = None
    is_viral_moment: bool = False


class ViralMoment(BaseModel):
    """Moment identifié comme potentiellement viral."""
    timestamp: float
    content: str
    reason: str
    short_title: str


class VideoScript(BaseModel):
    """Script vidéo complet."""
    id: str = Field(default_factory=lambda: f"script_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    title: str
    topic: str
    target_audience: str
    platform: Literal["youtube", "tiktok", "instagram", "all"]
    duration_target: int  # en secondes
    language: str
    
    # Structure du script
    hook: str
    intro: str
    segments: List[ScriptSegment]
    outro: str
    cta: str
    
    # Optimisation virale
    viral_moments: List[ViralMoment] = []
    viral_score: float = 0.0
    suggested_titles: List[str] = []
    suggested_hashtags: List[str] = []
    seo_description: str = ""
    
    # Metadata
    word_count: int = 0
    estimated_duration: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: Literal["draft", "approved", "in_production", "completed"] = "draft"


class ShortScript(BaseModel):
    """Script court pour TikTok/Reels."""
    id: str
    parent_script_id: str
    title: str
    hook: str
    content: str
    cta: str
    duration: int  # secondes
    platform: str
    hashtags: List[str]
    viral_score: float


# === AGENT SCRIPTWRITER ===

class ScriptwriterAgent(BaseAgent, JSONOutputMixin, MultilingualMixin, CostTrackingMixin):
    """
    Agent Scénariste - Génère des scripts optimisés pour le contenu viral.
    
    Utilise Claude Opus 4 pour la créativité et la qualité.
    """
    
    SYSTEM_PROMPT = """Tu es un scénariste expert en création de contenu viral pour les réseaux sociaux.

## Ton expertise:
- Création de hooks captivants (les 3 premières secondes sont cruciales)
- Scripts optimisés pour YouTube, TikTok et Instagram Reels
- Storytelling émotionnel et engageant
- Connaissance des tendances actuelles et des algorithmes
- Maîtrise du français, arabe et dialecte algérien (Darija)

## Règles de création:
1. Le HOOK doit immédiatement capturer l'attention
2. Chaque phrase doit pouvoir être visualisée
3. Varier le rythme (tension/relâchement)
4. Inclure des questions rhétoriques pour l'engagement
5. Terminer par un CTA clair

## Pour le contenu algérien:
- Intégrer des expressions locales authentiques
- Référencer des situations reconnaissables
- Utiliser l'humour local quand approprié

## Format de sortie:
Tu dois TOUJOURS retourner un JSON valide avec la structure spécifiée."""

    def __init__(self):
        config = AgentConfig(
            name="Scriptwriter",
            model=agent_configs.SCRIPTWRITER["model"],
            temperature=agent_configs.SCRIPTWRITER["temperature"],
            max_tokens=agent_configs.SCRIPTWRITER["max_tokens"],
            retry_attempts=agent_configs.SCRIPTWRITER["retry_attempts"],
            timeout=agent_configs.SCRIPTWRITER["timeout"],
            system_prompt=self.SYSTEM_PROMPT
        )
        super().__init__(config)
    
    async def process(self, input_data: Any) -> AgentResponse:
        """Point d'entrée principal pour la génération de script."""
        return await self.generate_script(**input_data)
    
    async def generate_script(
        self,
        topic: str,
        target_audience: str,
        platform: Literal["youtube", "tiktok", "instagram", "all"] = "youtube",
        duration: int = 300,  # 5 minutes par défaut
        language: str = "fr",
        tone: str = "engaging",
        context: Optional[str] = None,
    ) -> AgentResponse:
        """
        Génère un script complet optimisé pour la plateforme cible.
        
        Args:
            topic: Sujet de la vidéo
            target_audience: Audience cible
            platform: Plateforme de diffusion
            duration: Durée cible en secondes
            language: Langue du script
            tone: Ton souhaité (engaging, educational, entertaining, etc.)
            context: Contexte additionnel (optionnel)
        """
        start_time = datetime.utcnow()
        
        # Construire le prompt
        lang_instruction = self.get_language_instruction(language)
        
        prompt = f"""Crée un script vidéo complet sur le sujet suivant:

## SUJET
{topic}

## PARAMÈTRES
- Audience cible: {target_audience}
- Plateforme: {platform}
- Durée cible: {duration} secondes ({duration // 60} minutes)
- Langue: {language}
- Ton: {tone}
{"- Contexte: " + context if context else ""}

{lang_instruction}

## FORMAT DE SORTIE (JSON)
Retourne UNIQUEMENT un JSON valide avec cette structure:

{{
    "title": "Titre accrocheur de la vidéo",
    "hook": "Les 3 premières secondes - phrase d'accroche puissante",
    "intro": "Introduction (10-20 secondes)",
    "segments": [
        {{
            "timestamp_start": 0.0,
            "timestamp_end": 30.0,
            "content": "Contenu du segment",
            "speaker": "host",
            "visual_direction": "Description visuelle pour ce segment",
            "b_roll_suggestion": "Suggestion de B-roll",
            "is_viral_moment": false
        }}
    ],
    "outro": "Conclusion",
    "cta": "Appel à l'action",
    "viral_moments": [
        {{
            "timestamp": 45.0,
            "content": "Extrait du moment",
            "reason": "Pourquoi c'est viral",
            "short_title": "Titre pour le Short"
        }}
    ],
    "viral_score": 75,
    "suggested_titles": ["Titre 1", "Titre 2", "Titre 3", "Titre 4", "Titre 5"],
    "suggested_hashtags": ["#hashtag1", "#hashtag2"],
    "seo_description": "Description SEO optimisée"
}}

IMPORTANT: 
- Identifie 3 à 5 moments viraux potentiels pour créer des Shorts
- Le hook doit être provocant/intrigant
- Chaque segment doit avoir une direction visuelle claire
"""

        try:
            # Appel au LLM
            response = await self.call_llm(
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parser la réponse JSON
            script_data = await self.parse_json_response(response["content"])
            
            if "error" in script_data:
                return AgentResponse(
                    success=False,
                    data=None,
                    agent_name=self.name,
                    error=f"Erreur parsing JSON: {script_data.get('raw', 'Unknown')[:200]}",
                    tokens_used=response["tokens_used"],
                    processing_time=response["processing_time"],
                )
            
            # Construire l'objet VideoScript
            script = VideoScript(
                title=script_data.get("title", "Sans titre"),
                topic=topic,
                target_audience=target_audience,
                platform=platform,
                duration_target=duration,
                language=language,
                hook=script_data.get("hook", ""),
                intro=script_data.get("intro", ""),
                segments=[
                    ScriptSegment(**seg) 
                    for seg in script_data.get("segments", [])
                ],
                outro=script_data.get("outro", ""),
                cta=script_data.get("cta", ""),
                viral_moments=[
                    ViralMoment(**vm) 
                    for vm in script_data.get("viral_moments", [])
                ],
                viral_score=script_data.get("viral_score", 0),
                suggested_titles=script_data.get("suggested_titles", []),
                suggested_hashtags=script_data.get("suggested_hashtags", []),
                seo_description=script_data.get("seo_description", ""),
                word_count=self._count_words(script_data),
                estimated_duration=self._estimate_duration(script_data),
            )
            
            # Calculer le coût
            word_count = script.word_count
            token_cost = self.calculate_token_cost(
                "script_claude_opus", 
                word_count / 1000
            )
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            logger.info(
                f"[{self.name}] Script généré: '{script.title}' - "
                f"{word_count} mots - Score viral: {script.viral_score}"
            )
            
            return AgentResponse(
                success=True,
                data=script.model_dump(),
                agent_name=self.name,
                tokens_used=response["tokens_used"],
                processing_time=processing_time,
            )
            
        except Exception as e:
            logger.error(f"[{self.name}] Erreur génération script: {str(e)}")
            return AgentResponse(
                success=False,
                data=None,
                agent_name=self.name,
                error=str(e),
            )
    
    async def generate_hook_variations(
        self,
        topic: str,
        count: int = 5,
        language: str = "fr"
    ) -> AgentResponse:
        """
        Génère plusieurs variations de hooks pour A/B testing.
        """
        prompt = f"""Génère {count} variations de hooks accrocheurs pour une vidéo sur:
"{topic}"

Chaque hook doit:
- Durer maximum 3 secondes à lire
- Créer une tension ou curiosité
- Être différent des autres (angle unique)

Retourne un JSON:
{{
    "hooks": [
        {{"text": "Hook 1", "style": "question", "emotion": "curiosity"}},
        {{"text": "Hook 2", "style": "statement", "emotion": "shock"}}
    ]
}}
"""
        
        response = await self.call_llm(
            messages=[{"role": "user", "content": prompt}]
        )
        
        data = await self.parse_json_response(response["content"])
        
        return AgentResponse(
            success=True,
            data=data,
            agent_name=self.name,
            tokens_used=response["tokens_used"],
            processing_time=response["processing_time"],
        )
    
    async def extract_shorts(
        self,
        script: VideoScript,
        count: int = 3
    ) -> AgentResponse:
        """
        Extrait les meilleurs moments pour des Shorts viraux.
        """
        # Utiliser les moments viraux identifiés
        viral_moments = script.viral_moments[:count]
        
        shorts = []
        for i, moment in enumerate(viral_moments):
            short = ShortScript(
                id=f"{script.id}_short_{i+1}",
                parent_script_id=script.id,
                title=moment.short_title,
                hook=moment.content[:100],
                content=moment.content,
                cta=script.cta,
                duration=min(60, 30),  # 30-60 secondes
                platform="tiktok",
                hashtags=script.suggested_hashtags[:5],
                viral_score=script.viral_score,
            )
            shorts.append(short.model_dump())
        
        return AgentResponse(
            success=True,
            data={"shorts": shorts, "count": len(shorts)},
            agent_name=self.name,
        )
    
    async def localize_script(
        self,
        script: VideoScript,
        target_language: str,
        cultural_context: Optional[str] = None
    ) -> AgentResponse:
        """
        Adapte le script à une autre langue/culture.
        """
        prompt = f"""Adapte ce script à la langue "{target_language}":

Script original:
- Titre: {script.title}
- Hook: {script.hook}
- Intro: {script.intro}
- Segments: {json.dumps([s.model_dump() for s in script.segments], ensure_ascii=False)}
- Outro: {script.outro}
- CTA: {script.cta}

{"Contexte culturel: " + cultural_context if cultural_context else ""}

Adapte le contenu pour qu'il résonne avec l'audience locale.
Retourne le script adapté au même format JSON."""

        response = await self.call_llm(
            messages=[{"role": "user", "content": prompt}]
        )
        
        data = await self.parse_json_response(response["content"])
        
        return AgentResponse(
            success=True,
            data=data,
            agent_name=self.name,
            tokens_used=response["tokens_used"],
            processing_time=response["processing_time"],
        )
    
    def _count_words(self, script_data: Dict) -> int:
        """Compte le nombre de mots dans le script."""
        text = ""
        text += script_data.get("hook", "")
        text += " " + script_data.get("intro", "")
        for seg in script_data.get("segments", []):
            text += " " + seg.get("content", "")
        text += " " + script_data.get("outro", "")
        text += " " + script_data.get("cta", "")
        
        return len(text.split())
    
    def _estimate_duration(self, script_data: Dict) -> float:
        """Estime la durée du script (150 mots/minute)."""
        word_count = self._count_words(script_data)
        return (word_count / 150) * 60  # secondes


# === FACTORY FUNCTION ===

def create_scriptwriter_agent() -> ScriptwriterAgent:
    """Crée une instance de l'agent Scriptwriter."""
    return ScriptwriterAgent()
