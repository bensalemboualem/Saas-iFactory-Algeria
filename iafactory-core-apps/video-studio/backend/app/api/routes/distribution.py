"""
Distribution API Routes - Publication multi-plateforme
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime, timedelta
import uuid
import structlog

from app.agents import AgentTask, AgentRole, AgentStatus, GrowthHackerAgent

router = APIRouter()
logger = structlog.get_logger()

# In-memory storage
distributions_db: dict = {}
productions_db: dict = {}  # Reference


class Platform(str, Enum):
    YOUTUBE = "youtube"
    YOUTUBE_SHORTS = "youtube_shorts"
    TIKTOK = "tiktok"
    INSTAGRAM_REELS = "instagram_reels"
    INSTAGRAM_POST = "instagram_post"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    FACEBOOK = "facebook"


class DistributionStatus(str, Enum):
    PENDING = "pending"
    OPTIMIZING = "optimizing"
    SCHEDULED = "scheduled"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    ERROR = "error"


class PlatformConfig(BaseModel):
    platform: Platform
    enabled: bool = True
    custom_title: Optional[str] = None
    custom_description: Optional[str] = None
    custom_hashtags: Optional[List[str]] = None
    scheduled_time: Optional[datetime] = None


class OptimizeRequest(BaseModel):
    video_id: Optional[str] = None
    title: str = Field(..., min_length=5)
    description: str = Field(..., min_length=10)
    topic: str
    platforms: List[Platform] = [Platform.YOUTUBE]
    target_audience: Optional[str] = "18-35 ans"
    language: str = "fr"


class DistributeRequest(BaseModel):
    production_id: str
    platforms: List[PlatformConfig]
    auto_schedule: bool = True
    use_optimization: bool = True


class OptimizationResult(BaseModel):
    platform: str
    title: str
    description: str
    hashtags: List[str]
    best_posting_time: Optional[str] = None
    viral_score: float = 0
    thumbnail_prompt: Optional[str] = None


class OptimizeResponse(BaseModel):
    id: str
    status: str
    optimizations: List[OptimizationResult] = []
    tokens_used: int = 0
    error: Optional[str] = None


class PlatformPublication(BaseModel):
    platform: str
    status: str
    scheduled_time: Optional[datetime] = None
    published_url: Optional[str] = None
    error: Optional[str] = None


class DistributionResponse(BaseModel):
    id: str
    status: str
    production_id: str
    publications: List[PlatformPublication] = []
    analytics: Optional[dict] = None
    error: Optional[str] = None


async def optimize_task(optimization_id: str, request: OptimizeRequest):
    """Background task pour optimiser le contenu."""
    try:
        growth_hacker = GrowthHackerAgent()
        
        task = AgentTask(
            task_id=optimization_id,
            role=AgentRole.GROWTH_HACKER,
            input_data={
                "title": request.title,
                "description": request.description,
                "topic": request.topic,
                "platforms": [p.value for p in request.platforms],
                "target_audience": request.target_audience,
                "language": request.language
            }
        )
        
        result = await growth_hacker.execute(task)
        
        if result.status == AgentStatus.COMPLETED:
            distributions_db[optimization_id] = {
                "id": optimization_id,
                "status": "completed",
                "data": result.output,
                "tokens_used": result.tokens_used
            }
        else:
            distributions_db[optimization_id] = {
                "id": optimization_id,
                "status": "error",
                "error": result.error
            }
            
    except Exception as e:
        logger.error("Optimization error", optimization_id=optimization_id, error=str(e))
        distributions_db[optimization_id] = {
            "id": optimization_id,
            "status": "error",
            "error": str(e)
        }


@router.post("/optimize", response_model=OptimizeResponse)
async def optimize_content(
    request: OptimizeRequest,
    background_tasks: BackgroundTasks
):
    """
    Optimise le contenu pour maximiser l'engagement.
    
    - Génère des titres accrocheurs par plateforme
    - Optimise les descriptions et hashtags
    - Suggère les meilleurs horaires de publication
    - Calcule un score de viralité
    """
    optimization_id = str(uuid.uuid4())[:8]
    
    distributions_db[optimization_id] = {
        "id": optimization_id,
        "status": "optimizing",
        "type": "optimization"
    }
    
    background_tasks.add_task(optimize_task, optimization_id, request)
    
    logger.info(
        "Optimization started",
        optimization_id=optimization_id,
        platforms=[p.value for p in request.platforms]
    )
    
    return OptimizeResponse(
        id=optimization_id,
        status="optimizing"
    )


@router.get("/optimize/{optimization_id}", response_model=OptimizeResponse)
async def get_optimization(optimization_id: str):
    """Récupère le résultat d'une optimisation."""
    opt = distributions_db.get(optimization_id)
    
    if not opt:
        raise HTTPException(status_code=404, detail="Optimization not found")
    
    if opt["status"] == "completed":
        data = opt.get("data", {})
        optimizations = data.get("platform_optimizations", [])
        
        return OptimizeResponse(
            id=optimization_id,
            status="completed",
            optimizations=[OptimizationResult(**o) for o in optimizations],
            tokens_used=opt.get("tokens_used", 0)
        )
    elif opt["status"] == "error":
        return OptimizeResponse(
            id=optimization_id,
            status="error",
            error=opt.get("error")
        )
    else:
        return OptimizeResponse(
            id=optimization_id,
            status=opt["status"]
        )


async def distribute_task(distribution_id: str, request: DistributeRequest):
    """Background task pour distribuer le contenu."""
    try:
        publications = []
        
        for platform_config in request.platforms:
            if not platform_config.enabled:
                continue
            
            # Simuler la publication (intégrer les APIs réelles)
            scheduled_time = platform_config.scheduled_time
            if request.auto_schedule and not scheduled_time:
                # Calculer le meilleur horaire
                best_times = {
                    Platform.YOUTUBE: 14,  # 14h
                    Platform.TIKTOK: 19,  # 19h
                    Platform.INSTAGRAM_REELS: 12,  # 12h
                    Platform.LINKEDIN: 9,  # 9h
                }
                hour = best_times.get(platform_config.platform, 12)
                scheduled_time = datetime.now() + timedelta(hours=max(0, hour - datetime.now().hour))
            
            publications.append({
                "platform": platform_config.platform.value,
                "status": "scheduled" if scheduled_time else "pending",
                "scheduled_time": scheduled_time.isoformat() if scheduled_time else None,
                "published_url": None
            })
        
        distributions_db[distribution_id] = {
            "id": distribution_id,
            "status": DistributionStatus.SCHEDULED.value,
            "production_id": request.production_id,
            "publications": publications
        }
        
    except Exception as e:
        logger.error("Distribution error", distribution_id=distribution_id, error=str(e))
        distributions_db[distribution_id] = {
            "id": distribution_id,
            "status": DistributionStatus.ERROR.value,
            "error": str(e)
        }


@router.post("/distribute", response_model=DistributionResponse)
async def distribute_content(
    request: DistributeRequest,
    background_tasks: BackgroundTasks
):
    """
    Lance la distribution multi-plateforme.
    
    - Programme la publication sur chaque plateforme
    - Adapte le format selon la plateforme
    - Optimise les métadonnées automatiquement
    """
    distribution_id = str(uuid.uuid4())[:8]
    
    # Vérifier la production
    production = productions_db.get(request.production_id)
    if not production:
        # Accepter quand même pour le test
        logger.warning("Production not found, proceeding anyway", production_id=request.production_id)
    
    distributions_db[distribution_id] = {
        "id": distribution_id,
        "status": DistributionStatus.PENDING.value,
        "production_id": request.production_id
    }
    
    background_tasks.add_task(distribute_task, distribution_id, request)
    
    logger.info(
        "Distribution started",
        distribution_id=distribution_id,
        production_id=request.production_id,
        platforms=[p.platform.value for p in request.platforms]
    )
    
    return DistributionResponse(
        id=distribution_id,
        status=DistributionStatus.PENDING.value,
        production_id=request.production_id
    )


@router.get("/distribute/{distribution_id}", response_model=DistributionResponse)
async def get_distribution(distribution_id: str):
    """Récupère le statut d'une distribution."""
    dist = distributions_db.get(distribution_id)
    
    if not dist:
        raise HTTPException(status_code=404, detail="Distribution not found")
    
    return DistributionResponse(
        id=distribution_id,
        status=dist.get("status", "unknown"),
        production_id=dist.get("production_id", ""),
        publications=[PlatformPublication(**p) for p in dist.get("publications", [])],
        analytics=dist.get("analytics"),
        error=dist.get("error")
    )


@router.get("/platforms")
async def get_platforms():
    """Liste toutes les plateformes supportées."""
    return {
        "platforms": [
            {
                "id": "youtube",
                "name": "YouTube",
                "icon": "youtube",
                "formats": ["16:9", "9:16"],
                "max_duration": 43200,  # 12h
                "features": ["thumbnails", "cards", "end_screens", "chapters"]
            },
            {
                "id": "youtube_shorts",
                "name": "YouTube Shorts",
                "icon": "youtube",
                "formats": ["9:16"],
                "max_duration": 60,
                "features": ["music", "text"]
            },
            {
                "id": "tiktok",
                "name": "TikTok",
                "icon": "tiktok",
                "formats": ["9:16"],
                "max_duration": 180,
                "features": ["music", "effects", "duets"]
            },
            {
                "id": "instagram_reels",
                "name": "Instagram Reels",
                "icon": "instagram",
                "formats": ["9:16"],
                "max_duration": 90,
                "features": ["music", "effects", "collab"]
            },
            {
                "id": "instagram_post",
                "name": "Instagram Post",
                "icon": "instagram",
                "formats": ["1:1", "4:5"],
                "max_duration": 60,
                "features": ["carousel", "tags"]
            },
            {
                "id": "linkedin",
                "name": "LinkedIn",
                "icon": "linkedin",
                "formats": ["16:9", "1:1"],
                "max_duration": 600,
                "features": ["captions", "articles"]
            },
            {
                "id": "twitter",
                "name": "X (Twitter)",
                "icon": "twitter",
                "formats": ["16:9", "1:1"],
                "max_duration": 140,
                "features": ["threads", "spaces"]
            },
            {
                "id": "facebook",
                "name": "Facebook",
                "icon": "facebook",
                "formats": ["16:9", "9:16", "1:1"],
                "max_duration": 14400,  # 4h
                "features": ["reels", "live", "stories"]
            }
        ]
    }


@router.get("/best-times")
async def get_best_posting_times(platform: Optional[str] = None):
    """Retourne les meilleurs horaires de publication."""
    times = {
        "youtube": {
            "weekday": ["14:00", "17:00", "20:00"],
            "weekend": ["10:00", "14:00", "18:00"],
            "peak_days": ["saturday", "sunday"]
        },
        "tiktok": {
            "weekday": ["12:00", "19:00", "21:00"],
            "weekend": ["11:00", "19:00", "22:00"],
            "peak_days": ["tuesday", "thursday"]
        },
        "instagram": {
            "weekday": ["11:00", "13:00", "17:00"],
            "weekend": ["10:00", "14:00"],
            "peak_days": ["wednesday", "friday"]
        },
        "linkedin": {
            "weekday": ["07:30", "12:00", "17:00"],
            "weekend": ["10:00"],
            "peak_days": ["tuesday", "wednesday", "thursday"]
        },
        "twitter": {
            "weekday": ["08:00", "12:00", "17:00"],
            "weekend": ["12:00", "18:00"],
            "peak_days": ["wednesday"]
        }
    }
    
    if platform:
        return times.get(platform, {"error": "Platform not found"})
    
    return {"best_times": times}


@router.get("/hashtag-suggestions")
async def get_hashtag_suggestions(
    topic: str,
    platform: Platform = Platform.INSTAGRAM_REELS,
    count: int = 10
):
    """Suggère des hashtags basés sur le sujet."""
    # En production, utiliser un service de recherche de hashtags
    base_hashtags = {
        "tech": ["#tech", "#technology", "#innovation", "#digital", "#ai"],
        "business": ["#business", "#entrepreneur", "#startup", "#success", "#motivation"],
        "algeria": ["#algeria", "#dz", "#algerie", "#dzair", "#alger"],
        "video": ["#video", "#content", "#creator", "#youtube", "#viral"],
    }
    
    suggestions = []
    topic_lower = topic.lower()
    
    for category, tags in base_hashtags.items():
        if category in topic_lower or topic_lower in category:
            suggestions.extend(tags)
    
    # Ajouter des hashtags génériques
    suggestions.extend(["#fyp", "#trending", "#explore", "#follow"])
    
    # Limiter au nombre demandé
    unique_tags = list(set(suggestions))[:count]
    
    return {
        "topic": topic,
        "platform": platform.value,
        "hashtags": unique_tags
    }


@router.get("/")
async def list_distributions(
    status: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    """Liste toutes les distributions."""
    dists = [d for d in distributions_db.values() if d.get("type") != "optimization"]
    
    if status:
        dists = [d for d in dists if d.get("status") == status]
    
    return {
        "total": len(dists),
        "distributions": dists[offset:offset + limit]
    }
