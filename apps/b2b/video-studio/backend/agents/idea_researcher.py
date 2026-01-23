"""
IAFactory Video Studio Pro - Agent Chercheur d'Idées (IdeaResearcher)
Recherche des idées de contenu virales basées sur le contexte et la niche
"""

from typing import Any, Dict, List, Optional
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
from config import settings


logger = logging.getLogger(__name__)


# === MODÈLES DE DONNÉES ===

class ContentIdea(BaseModel):
    """Une idée de contenu."""
    id: str = Field(default_factory=lambda: f"idea_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    title: str
    description: str
    hook: str  # Accroche principale
    target_audience: str
    estimated_engagement: float  # Score 0-10
    keywords: List[str] = []
    hashtags: List[str] = []
    format_suggestions: List[str] = []  # youtube, tiktok, instagram
    duration_suggestion: int  # en secondes
    viral_potential: float  # Score 0-10
    reasons: List[str] = []  # Pourquoi cette idée peut marcher
    similar_successful_content: List[str] = []  # Exemples de succès similaires


class IdeaResearchRequest(BaseModel):
    """Requête de recherche d'idées."""
    niche: str  # ex: "cuisine algérienne", "tech", "sport"
    target_market: str = "dz"  # dz, fr, ch, mena
    language: str = "fr"  # fr, ar, darija, en
    content_type: str = "video"  # video, short, podcast
    target_platforms: List[str] = ["youtube", "tiktok", "instagram"]
    exclude_topics: List[str] = []
    num_ideas: int = 5
    focus_on_trends: bool = True
    additional_context: Optional[str] = None


class IdeaResearchResult(BaseModel):
    """Résultat de la recherche d'idées."""
    request_id: str
    ideas: List[ContentIdea]
    market_insights: str
    recommended_posting_times: Dict[str, str]
    competitor_analysis: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


# === AGENT IDEA RESEARCHER ===

class IdeaResearcherAgent(BaseAgent, JSONOutputMixin, MultilingualMixin, CostTrackingMixin):
    """
    Agent Chercheur d'Idées - Génère des idées de contenu virales.
    
    Utilise:
    - Analyse du marché cible
    - Compréhension des tendances
    - Patterns de viralité
    """
    
    DEFAULT_CONFIG = AgentConfig(
        name="IdeaResearcher",
        model=settings.CLAUDE_MODEL_SONNET,
        temperature=0.8,  # Plus créatif
        max_tokens=4000,
        system_prompt="""Tu es un expert en création de contenu viral pour le marché algérien et francophone.

MISSION: Générer des idées de contenu originales et engageantes qui ont un fort potentiel viral.

EXPERTISE:
- Compréhension profonde de la culture algérienne et MENA
- Connaissance des tendances réseaux sociaux (TikTok, Instagram, YouTube)
- Maîtrise du storytelling viral
- Expertise en SEO vidéo et hashtags

LANGUES: Français, Arabe classique, Darija algérienne

RÈGLES:
1. Les idées doivent être réalisables avec de la génération vidéo IA
2. Privilégier les sujets qui résonnent émotionnellement
3. Toujours inclure un hook puissant (3 premières secondes)
4. Considérer les spécificités culturelles du marché cible

OUTPUT: Toujours répondre en JSON structuré."""
    )
    
    def __init__(self, config: Optional[AgentConfig] = None):
        super().__init__(config or self.DEFAULT_CONFIG)
    
    async def process(self, input_data: IdeaResearchRequest) -> AgentResponse:
        """
        Génère des idées de contenu basées sur la requête.
        """
        start_time = datetime.utcnow()
        
        try:
            prompt = self._build_research_prompt(input_data)
            
            response = await self.call_llm(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8
            )
            
            # Parser la réponse JSON
            result = self.parse_json_output(response["content"], IdeaResearchResult)
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return AgentResponse(
                success=True,
                data=result.model_dump(),
                tokens_used=response.get("tokens_used", 0),
                processing_time=processing_time,
                agent_name=self.name
            )
            
        except Exception as e:
            logger.error(f"IdeaResearcher error: {e}")
            return AgentResponse(
                success=False,
                data=None,
                agent_name=self.name,
                error=str(e)
            )
    
    def _build_research_prompt(self, request: IdeaResearchRequest) -> str:
        """Construit le prompt de recherche d'idées."""
        
        market_context = {
            "dz": "Algérie - Culture locale, humour algérien, actualités nationales, Darija",
            "fr": "France - Marché francophone européen, tendances urbaines",
            "ch": "Suisse - Multilingue (FR/DE/IT), qualité premium, lifestyle",
            "mena": "Moyen-Orient & Afrique du Nord - Arabe, culture musulmane, diversité régionale"
        }
        
        platforms_context = ", ".join(request.target_platforms)
        
        prompt = f"""
RECHERCHE D'IDÉES DE CONTENU VIRAL

## Contexte
- **Niche**: {request.niche}
- **Marché cible**: {request.target_market} - {market_context.get(request.target_market, "International")}
- **Langue principale**: {request.language}
- **Type de contenu**: {request.content_type}
- **Plateformes**: {platforms_context}
- **Nombre d'idées demandées**: {request.num_ideas}

{f"**Contexte additionnel**: {request.additional_context}" if request.additional_context else ""}
{f"**Sujets à éviter**: {', '.join(request.exclude_topics)}" if request.exclude_topics else ""}

## Ta mission

Génère {request.num_ideas} idées de contenu uniques et virales pour cette niche.

Pour chaque idée, fournis:
1. Un titre accrocheur
2. Une description détaillée
3. Un hook puissant (pour les 3 premières secondes)
4. L'audience cible précise
5. Score d'engagement estimé (0-10)
6. Mots-clés et hashtags optimisés
7. Formats suggérés (durée, plateforme)
8. Potentiel viral et pourquoi
9. Exemples de contenu similaire qui a marché

## Format de réponse (JSON)

```json
{{
    "request_id": "idea_req_YYYYMMDDHHMMSS",
    "ideas": [
        {{
            "id": "idea_1",
            "title": "...",
            "description": "...",
            "hook": "...",
            "target_audience": "...",
            "estimated_engagement": 8.5,
            "keywords": ["...", "..."],
            "hashtags": ["#...", "#..."],
            "format_suggestions": ["youtube_short", "tiktok"],
            "duration_suggestion": 60,
            "viral_potential": 8.0,
            "reasons": ["...", "..."],
            "similar_successful_content": ["...", "..."]
        }}
    ],
    "market_insights": "Analyse du marché...",
    "recommended_posting_times": {{
        "youtube": "18h-20h",
        "tiktok": "12h-14h, 20h-22h",
        "instagram": "11h-13h, 19h-21h"
    }},
    "competitor_analysis": "Les principaux créateurs dans cette niche..."
}}
```

Génère maintenant les idées en JSON:
"""
        
        return prompt

    async def generate_ideas_for_trend(
        self, 
        trend_topic: str, 
        niche: str,
        language: str = "fr"
    ) -> List[ContentIdea]:
        """
        Génère des idées basées sur une tendance spécifique.
        Méthode utilitaire pour l'intégration avec TrendAnalyzer.
        """
        request = IdeaResearchRequest(
            niche=niche,
            language=language,
            additional_context=f"Tendance actuelle à exploiter: {trend_topic}",
            num_ideas=3,
            focus_on_trends=True
        )
        
        result = await self.process(request)
        
        if result.success and result.data:
            return [ContentIdea(**idea) for idea in result.data.get("ideas", [])]
        
        return []
