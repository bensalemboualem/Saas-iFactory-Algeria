"""
API routes for AI Agents - Video Studio Pro
Endpoints pour les agents IA: Trends, Ideas, Coordination, Quality Control
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import logging

# Import agents
import sys
sys.path.insert(0, '..')
from agents import (
    IdeaResearcherAgent,
    TrendAnalyzerAgent,
    ScriptCoordinatorAgent,
    QualityControllerAgent,
    IdeaResearchRequest,
    TrendAnalysisRequest,
    CoordinationRequest,
    QualityCheckRequest,
    ContentIdea,
    SocialTrend,
    VideoScript,
)

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize agents (singleton pattern)
_agents = {}

def get_idea_researcher() -> IdeaResearcherAgent:
    if "idea_researcher" not in _agents:
        _agents["idea_researcher"] = IdeaResearcherAgent()
    return _agents["idea_researcher"]

def get_trend_analyzer() -> TrendAnalyzerAgent:
    if "trend_analyzer" not in _agents:
        _agents["trend_analyzer"] = TrendAnalyzerAgent()
    return _agents["trend_analyzer"]

def get_script_coordinator() -> ScriptCoordinatorAgent:
    if "script_coordinator" not in _agents:
        _agents["script_coordinator"] = ScriptCoordinatorAgent()
    return _agents["script_coordinator"]

def get_quality_controller() -> QualityControllerAgent:
    if "quality_controller" not in _agents:
        _agents["quality_controller"] = QualityControllerAgent()
    return _agents["quality_controller"]


# ============================================
# SCHEMAS
# ============================================

class ContentFormat(str, Enum):
    YOUTUBE_LONG = "youtube_long"
    YOUTUBE_SHORT = "youtube_short"
    TIKTOK = "tiktok"
    INSTAGRAM_REEL = "instagram_reel"
    PODCAST = "podcast"


class TrendPlatform(str, Enum):
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    TWITTER = "twitter"


class IdeasRequest(BaseModel):
    """Requête pour générer des idées de contenu."""
    niche: str = Field(..., min_length=2, description="Niche du contenu (ex: cuisine, tech, sport)")
    target_market: str = Field("dz", description="Marché cible: dz, fr, ch, mena")
    language: str = Field("fr", description="Langue: fr, ar, darija, en")
    platforms: List[str] = Field(["tiktok", "instagram", "youtube"], description="Plateformes cibles")
    num_ideas: int = Field(5, ge=1, le=10, description="Nombre d'idées à générer")
    include_trends: bool = Field(True, description="Inclure les tendances actuelles")
    topic_hint: Optional[str] = Field(None, description="Sujet spécifique à explorer")
    avoid_topics: List[str] = Field([], description="Sujets à éviter")


class IdeasResponse(BaseModel):
    """Réponse avec les idées générées."""
    success: bool
    ideas: List[Dict[str, Any]]
    market_insights: Optional[str] = None
    recommended_posting_times: Optional[Dict[str, str]] = None
    tokens_used: int = 0
    processing_time: float = 0.0


class TrendsRequest(BaseModel):
    """Requête pour analyser les tendances."""
    platforms: List[TrendPlatform] = Field([TrendPlatform.TIKTOK, TrendPlatform.INSTAGRAM])
    markets: List[str] = Field(["dz", "fr"])
    niches: List[str] = Field([])
    time_range: str = Field("24h", description="Période: 24h, 7d, 30d")
    include_predictions: bool = Field(True)


class TrendsResponse(BaseModel):
    """Réponse avec les tendances."""
    success: bool
    trends: List[Dict[str, Any]]
    top_trending: List[Dict[str, Any]]
    emerging_trends: List[Dict[str, Any]]
    predictions: Optional[Dict[str, Any]] = None
    market_summary: Optional[Dict[str, str]] = None
    tokens_used: int = 0
    processing_time: float = 0.0


class CoordinateRequest(BaseModel):
    """Requête pour orchestrer le workflow complet."""
    project_name: str = Field(..., min_length=3)
    niche: str = Field(...)
    target_market: str = Field("dz")
    language: str = Field("fr")
    content_format: ContentFormat = Field(ContentFormat.TIKTOK)
    target_duration: int = Field(60, ge=15, le=600)
    platforms: List[str] = Field(["tiktok", "instagram", "youtube"])
    
    # Options workflow
    use_trends: bool = Field(True)
    auto_select_idea: bool = Field(True)
    num_ideas: int = Field(5, ge=1, le=10)
    
    # Contexte
    brand_guidelines: Optional[str] = None
    topic_preference: Optional[str] = None
    avoid_topics: List[str] = Field([])
    
    # Output options
    include_visuals: bool = Field(True)
    include_voiceover: bool = Field(True)
    include_music: bool = Field(True)


class CoordinateResponse(BaseModel):
    """Réponse du workflow de coordination."""
    success: bool
    project_id: str
    status: str
    current_step: int
    total_steps: int
    
    # Results
    trends_summary: Optional[Dict[str, Any]] = None
    ideas: List[Dict[str, Any]] = []
    selected_idea: Optional[Dict[str, Any]] = None
    script: Optional[Dict[str, Any]] = None
    quality_report: Optional[Dict[str, Any]] = None
    
    # Metadata
    tokens_used: int = 0
    processing_time: float = 0.0
    completed_at: Optional[datetime] = None


class QualityCheckRequest(BaseModel):
    """Requête de contrôle qualité."""
    script: Dict[str, Any]
    target_market: str = Field("dz")
    platform: str = Field("tiktok")
    strict_mode: bool = Field(False)
    auto_fix: bool = Field(True)


class QualityCheckResponse(BaseModel):
    """Réponse du contrôle qualité."""
    success: bool
    approved: bool
    overall_score: float
    overall_level: str
    issues_count: int
    critical_issues: int
    recommendations: List[str]
    viral_potential: float
    tokens_used: int = 0


# ============================================
# ENDPOINTS - TREND ANALYSIS
# ============================================

@router.post("/trends/analyze", response_model=TrendsResponse, tags=["Agents - Trends"])
async def analyze_trends(request: TrendsRequest):
    """
    Analyse les tendances sur les réseaux sociaux.
    
    Retourne les tendances actuelles, émergentes et des prédictions.
    """
    try:
        agent = get_trend_analyzer()
        
        # Convertir en format agent
        from agents.trend_analyzer import Platform
        platforms = [Platform(p.value) for p in request.platforms]
        
        agent_request = TrendAnalysisRequest(
            platforms=platforms,
            target_markets=request.markets,
            niches=request.niches,
            time_range=request.time_range,
            include_predictions=request.include_predictions
        )
        
        result = await agent.process(agent_request)
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)
        
        data = result.data
        return TrendsResponse(
            success=True,
            trends=data.get("trends", []),
            top_trending=data.get("top_trending", []),
            emerging_trends=data.get("emerging_trends", []),
            predictions=data.get("predictions"),
            market_summary=data.get("market_summary"),
            tokens_used=result.tokens_used,
            processing_time=result.processing_time
        )
        
    except Exception as e:
        logger.error(f"Trend analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends/quick", tags=["Agents - Trends"])
async def get_quick_trends(
    platform: str = "tiktok",
    market: str = "dz",
    limit: int = 5
):
    """
    Récupère rapidement les tendances principales.
    """
    try:
        agent = get_trend_analyzer()
        trends = await agent.get_trending_topics(
            platforms=[platform],
            market=market,
            limit=limit
        )
        
        return {
            "success": True,
            "platform": platform,
            "market": market,
            "trends": [t.model_dump() for t in trends]
        }
        
    except Exception as e:
        logger.error(f"Quick trends error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# ENDPOINTS - IDEA GENERATION
# ============================================

@router.post("/ideas/generate", response_model=IdeasResponse, tags=["Agents - Ideas"])
async def generate_ideas(request: IdeasRequest):
    """
    Génère des idées de contenu viral basées sur la niche et les tendances.
    """
    try:
        agent = get_idea_researcher()
        
        # Contexte avec tendances si demandé
        additional_context = request.topic_hint or ""
        
        if request.include_trends:
            trend_agent = get_trend_analyzer()
            trends = await trend_agent.get_trending_topics(
                platforms=request.platforms,
                market=request.target_market,
                limit=3
            )
            if trends:
                trend_names = [t.name for t in trends]
                additional_context += f" Tendances actuelles: {', '.join(trend_names)}"
        
        agent_request = IdeaResearchRequest(
            niche=request.niche,
            target_market=request.target_market,
            language=request.language,
            target_platforms=request.platforms,
            num_ideas=request.num_ideas,
            additional_context=additional_context.strip() if additional_context else None,
            exclude_topics=request.avoid_topics
        )
        
        result = await agent.process(agent_request)
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)
        
        data = result.data
        return IdeasResponse(
            success=True,
            ideas=data.get("ideas", []),
            market_insights=data.get("market_insights"),
            recommended_posting_times=data.get("recommended_posting_times"),
            tokens_used=result.tokens_used,
            processing_time=result.processing_time
        )
        
    except Exception as e:
        logger.error(f"Idea generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ideas/for-trend", tags=["Agents - Ideas"])
async def get_ideas_for_trend(
    trend: str,
    niche: str,
    language: str = "fr",
    count: int = 3
):
    """
    Génère des idées basées sur une tendance spécifique.
    """
    try:
        agent = get_idea_researcher()
        ideas = await agent.generate_ideas_for_trend(
            trend_topic=trend,
            niche=niche,
            language=language
        )
        
        return {
            "success": True,
            "trend": trend,
            "niche": niche,
            "ideas": [i.model_dump() for i in ideas[:count]]
        }
        
    except Exception as e:
        logger.error(f"Ideas for trend error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# ENDPOINTS - SCRIPT COORDINATION
# ============================================

@router.post("/coordinate", response_model=CoordinateResponse, tags=["Agents - Coordination"])
async def coordinate_workflow(request: CoordinateRequest):
    """
    Orchestre le workflow complet multi-agents:
    1. Analyse des tendances
    2. Génération d'idées
    3. Sélection de la meilleure idée
    4. Écriture du script
    5. Contrôle qualité
    
    Retourne le script finalisé prêt pour la production.
    """
    try:
        agent = get_script_coordinator()
        
        # Convertir en format agent
        from agents.script_coordinator import ContentFormat as AgentContentFormat
        
        agent_request = CoordinationRequest(
            project_name=request.project_name,
            niche=request.niche,
            target_market=request.target_market,
            language=request.language,
            content_format=AgentContentFormat(request.content_format.value),
            target_duration=request.target_duration,
            platforms=request.platforms,
            use_trends=request.use_trends,
            auto_select_idea=request.auto_select_idea,
            num_ideas_to_generate=request.num_ideas,
            brand_guidelines=request.brand_guidelines,
            topic_preference=request.topic_preference,
            avoid_topics=request.avoid_topics,
            include_visuals=request.include_visuals,
            include_voiceover=request.include_voiceover,
            include_music=request.include_music
        )
        
        result = await agent.process(agent_request)
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)
        
        data = result.data
        
        # Contrôle qualité si script généré
        quality_report = None
        if data.get("script"):
            qc_agent = get_quality_controller()
            qc_result = await qc_agent.quick_check(
                VideoScript(**data["script"]),
                market=request.target_market
            )
            quality_report = qc_result
        
        return CoordinateResponse(
            success=True,
            project_id=data.get("project_id", ""),
            status=data.get("status", "unknown"),
            current_step=data.get("current_step", 0),
            total_steps=len(data.get("steps", [])),
            trends_summary=data.get("trends_report"),
            ideas=[i for i in data.get("ideas", [])],
            selected_idea=data.get("selected_idea"),
            script=data.get("script"),
            quality_report=quality_report,
            tokens_used=result.tokens_used,
            processing_time=result.processing_time,
            completed_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Coordination error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/coordinate/quick-script", tags=["Agents - Coordination"])
async def quick_script(
    topic: str,
    niche: str,
    duration: int = 60,
    language: str = "fr",
    market: str = "dz"
):
    """
    Génère rapidement un script sans workflow complet.
    Idéal pour les cas simples.
    """
    try:
        agent = get_script_coordinator()
        script = await agent.quick_script(
            topic=topic,
            niche=niche,
            duration=duration,
            language=language,
            market=market
        )
        
        return {
            "success": True,
            "script": script.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Quick script error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# ENDPOINTS - QUALITY CONTROL
# ============================================

@router.post("/quality/check", response_model=QualityCheckResponse, tags=["Agents - Quality"])
async def check_quality(request: QualityCheckRequest):
    """
    Effectue un contrôle qualité complet sur un script.
    """
    try:
        agent = get_quality_controller()
        
        # Convertir le script
        script = VideoScript(**request.script)
        
        from agents.quality_controller import QualityCheckRequest as AgentQCRequest
        
        agent_request = AgentQCRequest(
            script=script,
            target_market=request.target_market,
            platform=request.platform,
            strict_mode=request.strict_mode,
            auto_fix=request.auto_fix
        )
        
        result = await agent.process(agent_request)
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)
        
        data = result.data
        return QualityCheckResponse(
            success=True,
            approved=data.get("approved", False),
            overall_score=data.get("overall_score", 0),
            overall_level=data.get("overall_level", "unknown"),
            issues_count=len(data.get("issues", [])),
            critical_issues=data.get("critical_issues", 0),
            recommendations=data.get("recommendations", []),
            viral_potential=data.get("viral_potential_score", 0),
            tokens_used=result.tokens_used
        )
        
    except Exception as e:
        logger.error(f"Quality check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/quality/cultural-check", tags=["Agents - Quality"])
async def check_cultural_sensitivity(
    content: str,
    market: str = "dz"
):
    """
    Vérifie la sensibilité culturelle d'un contenu.
    """
    try:
        agent = get_quality_controller()
        result = await agent.check_cultural_sensitivity(content, market)
        
        return {
            "success": True,
            "market": market,
            **result
        }
        
    except Exception as e:
        logger.error(f"Cultural check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# ENDPOINTS - AGENT STATUS
# ============================================

@router.get("/status", tags=["Agents - System"])
async def get_agents_status():
    """
    Retourne le statut de tous les agents.
    """
    agents_info = {}
    
    for name, agent in _agents.items():
        agents_info[name] = agent.get_stats()
    
    return {
        "agents_loaded": len(_agents),
        "agents": agents_info,
        "available_agents": [
            "idea_researcher",
            "trend_analyzer", 
            "script_coordinator",
            "quality_controller"
        ]
    }


@router.post("/reset-stats", tags=["Agents - System"])
async def reset_agent_stats():
    """
    Réinitialise les statistiques de tous les agents.
    """
    for agent in _agents.values():
        agent.reset_stats()
    
    return {"success": True, "message": "Stats reset for all agents"}
