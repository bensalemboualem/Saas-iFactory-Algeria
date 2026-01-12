"""
IAFactory Video Studio Pro - Agent Coordinateur de Scripts (ScriptCoordinator)
Orchestre le travail des autres agents et prépare le script final
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
import json
import logging
import asyncio

from pydantic import BaseModel, Field

from . import (
    BaseAgent, 
    AgentConfig, 
    AgentResponse,
    JSONOutputMixin,
    MultilingualMixin,
    CostTrackingMixin
)
from .idea_researcher import IdeaResearcherAgent, ContentIdea, IdeaResearchRequest
from .trend_analyzer import TrendAnalyzerAgent, TrendAnalysisRequest, SocialTrend
from .scriptwriter import ScriptwriterAgent, VideoScript
from config import settings


logger = logging.getLogger(__name__)


# === ENUMS ===

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RESEARCHING = "researching"
    ANALYZING_TRENDS = "analyzing_trends"
    GENERATING_IDEAS = "generating_ideas"
    WRITING_SCRIPT = "writing_script"
    REVIEWING = "reviewing"
    COMPLETED = "completed"
    FAILED = "failed"


class ContentFormat(str, Enum):
    YOUTUBE_LONG = "youtube_long"  # 10-60 min
    YOUTUBE_SHORT = "youtube_short"  # < 60s
    TIKTOK = "tiktok"  # 15-60s
    INSTAGRAM_REEL = "instagram_reel"  # 15-90s
    PODCAST = "podcast"  # Audio long format


# === MODÈLES DE DONNÉES ===

class CoordinationRequest(BaseModel):
    """Requête de coordination multi-agents."""
    project_name: str
    niche: str
    target_market: str = "dz"
    language: str = "fr"
    content_format: ContentFormat = ContentFormat.TIKTOK
    target_duration: int = 60  # secondes
    platforms: List[str] = ["tiktok", "instagram", "youtube"]
    
    # Options
    use_trends: bool = True  # Intégrer les tendances
    auto_select_idea: bool = True  # Sélection auto de la meilleure idée
    num_ideas_to_generate: int = 5
    
    # Contexte additionnel
    brand_guidelines: Optional[str] = None
    topic_preference: Optional[str] = None
    avoid_topics: List[str] = []
    
    # Paramètres de sortie
    include_visuals: bool = True  # Suggestions visuelles
    include_voiceover: bool = True  # Script voix off
    include_music: bool = True  # Suggestions musicales


class WorkflowStep(BaseModel):
    """Étape du workflow."""
    step_id: int
    name: str
    status: WorkflowStatus
    agent: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class CoordinationResult(BaseModel):
    """Résultat de la coordination."""
    project_id: str
    project_name: str
    status: WorkflowStatus
    
    # Workflow
    steps: List[WorkflowStep]
    current_step: int
    
    # Outputs
    trends_report: Optional[Dict] = None
    ideas: List[ContentIdea] = []
    selected_idea: Optional[ContentIdea] = None
    script: Optional[VideoScript] = None
    
    # Metadata
    total_tokens_used: int = 0
    total_processing_time: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


# === AGENT COORDINATEUR ===

class ScriptCoordinatorAgent(BaseAgent, JSONOutputMixin, MultilingualMixin, CostTrackingMixin):
    """
    Agent Coordinateur - Orchestre le workflow multi-agents.
    
    Workflow:
    1. TrendAnalyzer → Analyse des tendances actuelles
    2. IdeaResearcher → Génération d'idées basées sur trends + niche
    3. Sélection de la meilleure idée
    4. ScriptWriter → Génération du script complet
    5. Révision et optimisation
    """
    
    DEFAULT_CONFIG = AgentConfig(
        name="ScriptCoordinator",
        model=settings.CLAUDE_MODEL_OPUS,  # Opus pour la coordination
        temperature=0.6,
        max_tokens=4000,
        system_prompt="""Tu es le coordinateur principal de l'usine à contenu IAFactory Video Studio.

RÔLE: Orchestrer les agents spécialisés pour produire du contenu viral optimal.

RESPONSABILITÉS:
1. Analyser les inputs du projet
2. Déléguer aux agents spécialisés
3. Synthétiser les résultats
4. Sélectionner les meilleures options
5. Assurer la cohérence du contenu final

AGENTS SOUS TA DIRECTION:
- TrendAnalyzer: Veille des tendances
- IdeaResearcher: Génération d'idées
- ScriptWriter: Rédaction de scripts
- QualityController: Contrôle qualité

OBJECTIF: Produire un script viral optimisé pour le marché cible."""
    )
    
    def __init__(self, config: Optional[AgentConfig] = None):
        super().__init__(config or self.DEFAULT_CONFIG)
        
        # Initialiser les agents subordonnés
        self.trend_analyzer = TrendAnalyzerAgent()
        self.idea_researcher = IdeaResearcherAgent()
        self.script_writer = ScriptwriterAgent()
    
    async def process(self, input_data: CoordinationRequest) -> AgentResponse:
        """
        Exécute le workflow complet de coordination.
        """
        start_time = datetime.utcnow()
        
        # Initialiser le résultat
        result = CoordinationResult(
            project_id=f"proj_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            project_name=input_data.project_name,
            status=WorkflowStatus.PENDING,
            steps=[
                WorkflowStep(step_id=1, name="Analyse des tendances", status=WorkflowStatus.PENDING, agent="TrendAnalyzer"),
                WorkflowStep(step_id=2, name="Génération d'idées", status=WorkflowStatus.PENDING, agent="IdeaResearcher"),
                WorkflowStep(step_id=3, name="Sélection de l'idée", status=WorkflowStatus.PENDING, agent="ScriptCoordinator"),
                WorkflowStep(step_id=4, name="Écriture du script", status=WorkflowStatus.PENDING, agent="ScriptWriter"),
                WorkflowStep(step_id=5, name="Révision finale", status=WorkflowStatus.PENDING, agent="ScriptCoordinator"),
            ],
            current_step=1
        )
        
        total_tokens = 0
        
        try:
            # === ÉTAPE 1: Analyse des tendances ===
            if input_data.use_trends:
                result.steps[0].status = WorkflowStatus.ANALYZING_TRENDS
                result.steps[0].started_at = datetime.utcnow()
                
                trend_request = TrendAnalysisRequest(
                    platforms=["tiktok", "instagram", "youtube"],
                    target_markets=[input_data.target_market],
                    niches=[input_data.niche],
                    language=input_data.language
                )
                
                trend_response = await self.trend_analyzer.process(trend_request)
                
                if trend_response.success:
                    result.trends_report = trend_response.data
                    result.steps[0].result = {"trends_count": len(trend_response.data.get("trends", []))}
                    total_tokens += trend_response.tokens_used
                
                result.steps[0].status = WorkflowStatus.COMPLETED
                result.steps[0].completed_at = datetime.utcnow()
            else:
                result.steps[0].status = WorkflowStatus.COMPLETED
                result.steps[0].result = {"skipped": True}
            
            result.current_step = 2
            
            # === ÉTAPE 2: Génération d'idées ===
            result.steps[1].status = WorkflowStatus.GENERATING_IDEAS
            result.steps[1].started_at = datetime.utcnow()
            
            # Construire le contexte avec les tendances
            trend_context = ""
            if result.trends_report:
                top_trends = result.trends_report.get("top_trending", [])[:3]
                trend_context = f"Tendances actuelles: {json.dumps(top_trends, ensure_ascii=False)}"
            
            idea_request = IdeaResearchRequest(
                niche=input_data.niche,
                target_market=input_data.target_market,
                language=input_data.language,
                target_platforms=input_data.platforms,
                num_ideas=input_data.num_ideas_to_generate,
                additional_context=f"{input_data.topic_preference or ''} {trend_context}".strip(),
                exclude_topics=input_data.avoid_topics
            )
            
            idea_response = await self.idea_researcher.process(idea_request)
            
            if idea_response.success:
                ideas_data = idea_response.data.get("ideas", [])
                result.ideas = [ContentIdea(**i) for i in ideas_data]
                result.steps[1].result = {"ideas_count": len(result.ideas)}
                total_tokens += idea_response.tokens_used
            
            result.steps[1].status = WorkflowStatus.COMPLETED
            result.steps[1].completed_at = datetime.utcnow()
            result.current_step = 3
            
            # === ÉTAPE 3: Sélection de l'idée ===
            result.steps[2].status = WorkflowStatus.REVIEWING
            result.steps[2].started_at = datetime.utcnow()
            
            if result.ideas:
                if input_data.auto_select_idea:
                    result.selected_idea = await self._select_best_idea(
                        result.ideas, 
                        input_data
                    )
                else:
                    # Prendre la première avec le meilleur score viral
                    result.selected_idea = max(result.ideas, key=lambda x: x.viral_potential)
                
                result.steps[2].result = {"selected_idea": result.selected_idea.title}
            
            result.steps[2].status = WorkflowStatus.COMPLETED
            result.steps[2].completed_at = datetime.utcnow()
            result.current_step = 4
            
            # === ÉTAPE 4: Écriture du script ===
            result.steps[3].status = WorkflowStatus.WRITING_SCRIPT
            result.steps[3].started_at = datetime.utcnow()
            
            if result.selected_idea:
                script_response = await self.script_writer.process({
                    "topic": result.selected_idea.title,
                    "description": result.selected_idea.description,
                    "hook": result.selected_idea.hook,
                    "target_audience": result.selected_idea.target_audience,
                    "platform": input_data.content_format.value,
                    "duration_target": input_data.target_duration,
                    "language": input_data.language,
                    "include_visuals": input_data.include_visuals,
                    "include_voiceover": input_data.include_voiceover,
                    "brand_guidelines": input_data.brand_guidelines
                })
                
                if script_response.success:
                    result.script = VideoScript(**script_response.data)
                    result.steps[3].result = {"script_id": result.script.id}
                    total_tokens += script_response.tokens_used
            
            result.steps[3].status = WorkflowStatus.COMPLETED
            result.steps[3].completed_at = datetime.utcnow()
            result.current_step = 5
            
            # === ÉTAPE 5: Révision finale ===
            result.steps[4].status = WorkflowStatus.REVIEWING
            result.steps[4].started_at = datetime.utcnow()
            
            # Optimisation finale du script
            if result.script:
                optimization = await self._optimize_script(result.script, input_data)
                result.steps[4].result = optimization
                total_tokens += optimization.get("tokens_used", 0)
            
            result.steps[4].status = WorkflowStatus.COMPLETED
            result.steps[4].completed_at = datetime.utcnow()
            
            # Finalisation
            result.status = WorkflowStatus.COMPLETED
            result.completed_at = datetime.utcnow()
            result.total_tokens_used = total_tokens
            result.total_processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return AgentResponse(
                success=True,
                data=result.model_dump(),
                tokens_used=total_tokens,
                processing_time=result.total_processing_time,
                agent_name=self.name
            )
            
        except Exception as e:
            logger.error(f"ScriptCoordinator error: {e}")
            result.status = WorkflowStatus.FAILED
            
            return AgentResponse(
                success=False,
                data=result.model_dump(),
                agent_name=self.name,
                error=str(e)
            )
    
    async def _select_best_idea(
        self, 
        ideas: List[ContentIdea], 
        request: CoordinationRequest
    ) -> ContentIdea:
        """
        Utilise l'IA pour sélectionner la meilleure idée.
        """
        ideas_json = json.dumps([i.model_dump() for i in ideas], ensure_ascii=False, indent=2)
        
        prompt = f"""
Analyse ces {len(ideas)} idées de contenu et sélectionne LA MEILLEURE pour ce projet:

## Critères du projet
- Niche: {request.niche}
- Marché: {request.target_market}
- Format: {request.content_format.value}
- Durée: {request.target_duration}s
- Plateformes: {', '.join(request.platforms)}

## Idées à évaluer
{ideas_json}

## Ta mission

Évalue chaque idée selon:
1. Potentiel viral (0-10)
2. Faisabilité avec génération vidéo IA (0-10)
3. Adéquation avec le marché cible (0-10)
4. Originalité (0-10)

Retourne l'ID de la meilleure idée avec justification.

Format JSON:
{{
    "selected_idea_id": "idea_X",
    "scores": {{
        "viral_potential": X,
        "feasibility": X,
        "market_fit": X,
        "originality": X,
        "total": X
    }},
    "justification": "...",
    "improvements": ["suggestion 1", "suggestion 2"]
}}
"""
        
        response = await self.call_llm(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        
        selection = self.parse_json_output(response["content"], dict)
        selected_id = selection.get("selected_idea_id", ideas[0].id)
        
        # Trouver l'idée sélectionnée
        for idea in ideas:
            if idea.id == selected_id:
                return idea
        
        return ideas[0]
    
    async def _optimize_script(
        self, 
        script: VideoScript, 
        request: CoordinationRequest
    ) -> Dict:
        """
        Optimise le script final.
        """
        prompt = f"""
Révise et optimise ce script pour maximiser son impact viral:

## Script actuel
- Titre: {script.title}
- Hook: {script.hook}
- Durée cible: {script.duration_target}s
- Plateforme: {script.platform}

## Script complet
{json.dumps(script.model_dump(), ensure_ascii=False, indent=2)}

## Optimisations demandées

1. **Hook** - Le hook est-il assez percutant pour les 3 premières secondes?
2. **Rythme** - Le pacing est-il adapté à la plateforme?
3. **CTA** - L'appel à l'action est-il clair et engageant?
4. **Viralité** - Y a-t-il des éléments partageables?

Retourne les optimisations suggérées:

```json
{{
    "optimizations_applied": ["...", "..."],
    "improved_hook": "...",
    "improved_cta": "...",
    "viral_elements_added": ["...", "..."],
    "final_score": 8.5,
    "ready_for_production": true
}}
```
"""
        
        response = await self.call_llm(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        
        result = self.parse_json_output(response["content"], dict)
        result["tokens_used"] = response.get("tokens_used", 0)
        
        return result

    async def quick_script(
        self,
        topic: str,
        niche: str,
        duration: int = 60,
        language: str = "fr",
        market: str = "dz"
    ) -> VideoScript:
        """
        Génération rapide d'un script sans workflow complet.
        Méthode utilitaire pour les cas simples.
        """
        request = CoordinationRequest(
            project_name=f"Quick Script - {topic}",
            niche=niche,
            target_market=market,
            language=language,
            target_duration=duration,
            use_trends=False,
            num_ideas_to_generate=1
        )
        
        result = await self.process(request)
        
        if result.success and result.data.get("script"):
            return VideoScript(**result.data["script"])
        
        raise Exception("Failed to generate quick script")
