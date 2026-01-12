"""
IAFactory Video Studio Pro - Agent Analyseur de Tendances (TrendAnalyzer)
Surveille et analyse les tendances sur les réseaux sociaux
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
import json
import logging
import asyncio
import aiohttp

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


# === ENUMS ===

class Platform(str, Enum):
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    TWITTER = "twitter"
    FACEBOOK = "facebook"


class TrendCategory(str, Enum):
    HASHTAG = "hashtag"
    AUDIO = "audio"
    CHALLENGE = "challenge"
    FORMAT = "format"
    TOPIC = "topic"
    MEME = "meme"


# === MODÈLES DE DONNÉES ===

class SocialTrend(BaseModel):
    """Une tendance détectée sur les réseaux sociaux."""
    id: str = Field(default_factory=lambda: f"trend_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    platform: Platform
    category: TrendCategory
    name: str  # Nom du trend (hashtag, son, challenge...)
    description: str
    engagement_score: float  # Score 0-100
    velocity: float  # Vitesse de croissance (0-10)
    lifespan_estimate: str  # "1-2 days", "1 week", etc.
    geographic_reach: List[str]  # ["dz", "fr", "worldwide"]
    related_hashtags: List[str] = []
    example_content: List[str] = []  # URLs ou descriptions
    virality_score: float  # Score 0-10
    relevance_score: float  # Pertinence pour le marché cible
    detected_at: datetime = Field(default_factory=datetime.utcnow)


class TrendAnalysisRequest(BaseModel):
    """Requête d'analyse de tendances."""
    platforms: List[Platform] = [Platform.TIKTOK, Platform.INSTAGRAM, Platform.YOUTUBE]
    target_markets: List[str] = ["dz", "fr"]
    niches: List[str] = []  # Niches spécifiques à surveiller
    language: str = "fr"
    time_range: str = "24h"  # 24h, 7d, 30d
    min_engagement_score: float = 50.0
    include_predictions: bool = True


class TrendReport(BaseModel):
    """Rapport complet des tendances."""
    report_id: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    trends: List[SocialTrend]
    top_trending: List[SocialTrend]  # Top 5
    emerging_trends: List[SocialTrend]  # Nouvelles tendances
    declining_trends: List[str]  # Tendances en baisse
    predictions: Dict[str, Any]  # Prédictions pour les prochains jours
    market_summary: Dict[str, str]  # Résumé par marché
    recommended_actions: List[str]  # Actions recommandées


# === SERVICE DE COLLECTE (APIs externes simulées) ===

class TrendDataCollector:
    """
    Collecteur de données de tendances.
    Utilise des APIs externes et web scraping.
    """
    
    @staticmethod
    async def fetch_tiktok_trends(market: str = "dz") -> List[Dict]:
        """
        Récupère les tendances TikTok.
        En production: utiliser TikTok Research API ou scraping.
        """
        # Simulation - En prod, appeler l'API TikTok
        mock_trends = [
            {"name": "#DiscoverAlgeria", "views": 15000000, "category": "travel"},
            {"name": "#DarijaHumor", "views": 8500000, "category": "comedy"},
            {"name": "#AlgerianFood", "views": 6200000, "category": "food"},
            {"name": "#RamadanRecipes", "views": 12000000, "category": "food"},
            {"name": "#CAN2025", "views": 25000000, "category": "sport"},
        ]
        return mock_trends
    
    @staticmethod
    async def fetch_youtube_trends(market: str = "dz") -> List[Dict]:
        """
        Récupère les tendances YouTube.
        Utilise YouTube Data API.
        """
        mock_trends = [
            {"title": "Les meilleurs spots de Alger", "views": 500000, "category": "travel"},
            {"title": "Recette Couscous traditionnel", "views": 350000, "category": "food"},
            {"title": "Match Algérie CAN 2025", "views": 1200000, "category": "sport"},
        ]
        return mock_trends
    
    @staticmethod
    async def fetch_instagram_trends(market: str = "dz") -> List[Dict]:
        """
        Récupère les tendances Instagram.
        """
        mock_trends = [
            {"hashtag": "#TeamDZ", "posts": 850000, "growth": "+15%"},
            {"hashtag": "#AlgerieMonAmour", "posts": 620000, "growth": "+8%"},
            {"hashtag": "#123VivaLAlgerie", "posts": 1500000, "growth": "+25%"},
        ]
        return mock_trends


# === AGENT TREND ANALYZER ===

class TrendAnalyzerAgent(BaseAgent, JSONOutputMixin, MultilingualMixin, CostTrackingMixin):
    """
    Agent Analyseur de Tendances - Détecte et analyse les tendances virales.
    
    Fonctionnalités:
    - Collecte multi-plateformes
    - Analyse de viralité
    - Prédictions de tendances
    - Recommandations personnalisées
    """
    
    DEFAULT_CONFIG = AgentConfig(
        name="TrendAnalyzer",
        model=settings.CLAUDE_MODEL_SONNET,
        temperature=0.5,  # Plus analytique
        max_tokens=4000,
        system_prompt="""Tu es un expert en analyse de tendances réseaux sociaux spécialisé dans le marché algérien et MENA.

MISSION: Analyser les tendances actuelles et prédire les prochains trends viraux.

EXPERTISE:
- Analyse de données sociales multi-plateformes
- Compréhension des algorithmes TikTok, Instagram, YouTube
- Connaissance approfondie de la culture algérienne
- Prédiction de viralité

CAPACITÉS:
1. Identifier les tendances émergentes avant qu'elles explosent
2. Évaluer la durée de vie d'une tendance
3. Mesurer la pertinence pour une niche spécifique
4. Recommander le timing optimal de publication

OUTPUT: Toujours répondre en JSON structuré avec des métriques précises."""
    )
    
    def __init__(self, config: Optional[AgentConfig] = None):
        super().__init__(config or self.DEFAULT_CONFIG)
        self.collector = TrendDataCollector()
    
    async def process(self, input_data: TrendAnalysisRequest) -> AgentResponse:
        """
        Analyse les tendances selon la requête.
        """
        start_time = datetime.utcnow()
        
        try:
            # 1. Collecter les données brutes
            raw_data = await self._collect_trend_data(input_data)
            
            # 2. Analyser avec l'IA
            prompt = self._build_analysis_prompt(input_data, raw_data)
            
            response = await self.call_llm(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )
            
            # 3. Parser et enrichir le rapport
            report = self.parse_json_output(response["content"], TrendReport)
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return AgentResponse(
                success=True,
                data=report.model_dump(),
                tokens_used=response.get("tokens_used", 0),
                processing_time=processing_time,
                agent_name=self.name
            )
            
        except Exception as e:
            logger.error(f"TrendAnalyzer error: {e}")
            return AgentResponse(
                success=False,
                data=None,
                agent_name=self.name,
                error=str(e)
            )
    
    async def _collect_trend_data(self, request: TrendAnalysisRequest) -> Dict[str, Any]:
        """Collecte les données de toutes les plateformes demandées."""
        data = {}
        
        tasks = []
        for platform in request.platforms:
            for market in request.target_markets:
                if platform == Platform.TIKTOK:
                    tasks.append(("tiktok", market, self.collector.fetch_tiktok_trends(market)))
                elif platform == Platform.YOUTUBE:
                    tasks.append(("youtube", market, self.collector.fetch_youtube_trends(market)))
                elif platform == Platform.INSTAGRAM:
                    tasks.append(("instagram", market, self.collector.fetch_instagram_trends(market)))
        
        results = await asyncio.gather(*[t[2] for t in tasks], return_exceptions=True)
        
        for i, (platform, market, _) in enumerate(tasks):
            key = f"{platform}_{market}"
            if not isinstance(results[i], Exception):
                data[key] = results[i]
            else:
                logger.warning(f"Failed to fetch {key}: {results[i]}")
                data[key] = []
        
        return data
    
    def _build_analysis_prompt(self, request: TrendAnalysisRequest, raw_data: Dict) -> str:
        """Construit le prompt d'analyse."""
        
        prompt = f"""
ANALYSE DES TENDANCES RÉSEAUX SOCIAUX

## Paramètres
- **Plateformes**: {", ".join([p.value for p in request.platforms])}
- **Marchés cibles**: {", ".join(request.target_markets)}
- **Période**: {request.time_range}
- **Langue**: {request.language}
{f"**Niches spécifiques**: {', '.join(request.niches)}" if request.niches else ""}

## Données collectées

```json
{json.dumps(raw_data, indent=2, ensure_ascii=False)}
```

## Ta mission

Analyse ces données et génère un rapport complet:

1. **Tendances principales** - Les 10 tendances les plus importantes
2. **Tendances émergentes** - Nouvelles tendances à fort potentiel
3. **Tendances en déclin** - À éviter
4. **Prédictions** - Ce qui va exploser dans les prochains jours
5. **Recommandations** - Actions concrètes pour un créateur de contenu

## Format de réponse (JSON)

```json
{{
    "report_id": "trend_report_YYYYMMDDHHMMSS",
    "trends": [
        {{
            "id": "trend_1",
            "platform": "tiktok",
            "category": "hashtag",
            "name": "#Example",
            "description": "...",
            "engagement_score": 85.0,
            "velocity": 8.5,
            "lifespan_estimate": "1 week",
            "geographic_reach": ["dz", "fr"],
            "related_hashtags": ["#...", "#..."],
            "virality_score": 8.0,
            "relevance_score": 9.0
        }}
    ],
    "top_trending": [...],
    "emerging_trends": [...],
    "declining_trends": ["#OldTrend", ...],
    "predictions": {{
        "next_week": ["Prédiction 1", "..."],
        "confidence": 0.75
    }},
    "market_summary": {{
        "dz": "Résumé marché algérien...",
        "fr": "Résumé marché français..."
    }},
    "recommended_actions": [
        "Action 1: ...",
        "Action 2: ..."
    ]
}}
```

Génère le rapport maintenant:
"""
        
        return prompt

    async def get_trending_topics(
        self, 
        platforms: List[str] = ["tiktok", "instagram"],
        market: str = "dz",
        limit: int = 5
    ) -> List[SocialTrend]:
        """
        Récupère rapidement les sujets tendances.
        Méthode utilitaire pour l'intégration rapide.
        """
        request = TrendAnalysisRequest(
            platforms=[Platform(p) for p in platforms],
            target_markets=[market],
            time_range="24h"
        )
        
        result = await self.process(request)
        
        if result.success and result.data:
            trends = result.data.get("top_trending", [])[:limit]
            return [SocialTrend(**t) for t in trends]
        
        return []

    async def analyze_specific_trend(self, trend_name: str, platform: str = "tiktok") -> Dict:
        """
        Analyse approfondie d'une tendance spécifique.
        """
        prompt = f"""
Analyse approfondie de la tendance "{trend_name}" sur {platform}.

Fournis:
1. Origine de la tendance
2. Pourquoi elle est virale
3. Durée de vie estimée
4. Comment l'exploiter pour du contenu original
5. Risques à éviter

Format JSON:
{{
    "trend_name": "{trend_name}",
    "platform": "{platform}",
    "origin": "...",
    "viral_factors": ["...", "..."],
    "lifespan": "...",
    "content_opportunities": ["...", "..."],
    "risks": ["...", "..."],
    "recommendation": "..."
}}
"""
        
        response = await self.call_llm(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        
        return self.parse_json_output(response["content"], dict)
