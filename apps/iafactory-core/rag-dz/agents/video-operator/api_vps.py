"""
IA Factory Video Operator - FastAPI Backend
API REST pour le montage vidéo automatisé

Endpoints:
- POST /api/v1/edit          → Lance un job de montage
- GET  /api/v1/status/{id}   → Statut d'un job
- GET  /api/v1/download/{id} → Télécharge la vidéo finale
"""

import os
import uuid
import asyncio
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from video_operator import (
    VideoOperatorAgent, 
    VideoOperatorConfig, 
    Platform, 
    EditStyle
)

# ============================================================
# CONFIG
# ============================================================

UPLOAD_DIR = "/opt/iafactory-rag-dz/uploads/video-operator"
OUTPUT_DIR = "/opt/iafactory-rag-dz/outputs/video-operator"
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# In-memory job storage (use Redis in production)
jobs: Dict[str, Dict[str, Any]] = {}

# ============================================================
# MODELS
# ============================================================

class EditRequest(BaseModel):
    """Requête de montage vidéo"""
    target_duration: int = Field(default=15, ge=5, le=120)
    platforms: List[str] = Field(default=["instagram_reels"])
    style: str = Field(default="algerian_minimal")
    add_captions: bool = Field(default=True)
    add_music: bool = Field(default=False)
    language: str = Field(default="fr")  # fr, ar, en


class JobStatus(BaseModel):
    """Statut d'un job"""
    id: str
    status: str  # pending, processing, completed, failed
    progress: int = 0
    message: str = ""
    created_at: str
    completed_at: Optional[str] = None
    outputs: Optional[Dict[str, str]] = None
    error: Optional[str] = None
    video_url: Optional[str] = None


class EditResponse(BaseModel):
    """Réponse de création de job"""
    job_id: str
    status: str
    message: str


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="IA Factory Video Operator",
    description="API de montage vidéo automatisé - Trilingue (FR/AR/EN)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# BACKGROUND TASKS
# ============================================================

async def process_video_job(job_id: str, video_path: str, config: VideoOperatorConfig):
    """Traite un job de montage en background"""
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["message"] = "Analyse de la vidéo..."
        jobs[job_id]["progress"] = 10
        
        agent = VideoOperatorAgent(config)
        
        # Update progress during processing
        jobs[job_id]["progress"] = 30
        jobs[job_id]["message"] = "Détection des scènes..."
        
        await asyncio.sleep(1)  # Allow progress update
        
        jobs[job_id]["progress"] = 50
        jobs[job_id]["message"] = "Montage en cours..."
        
        # Process video
        outputs = await agent.process_video(video_path, f"edited_{job_id}")
        
        jobs[job_id]["progress"] = 90
        jobs[job_id]["message"] = "Export final..."
        
        await asyncio.sleep(0.5)
        
        # Complete
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["message"] = "Montage terminé!"
        jobs[job_id]["outputs"] = outputs
        jobs[job_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["message"] = f"Erreur: {str(e)}"
    
    finally:
        # Cleanup uploaded file
        try:
            if os.path.exists(video_path):
                os.unlink(video_path)
        except:
            pass


# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    active_jobs = len([j for j in jobs.values() if j.get("status") == "processing"])
    return {
        "status": "healthy",
        "service": "video-operator-v1",
        "version": "1.0.0",
        "jobs_active": active_jobs,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "IA Factory Video Operator",
        "status": "online",
        "version": "1.0.0",
        "languages": ["fr", "ar", "en"]
    }


@app.post("/api/v1/edit", response_model=EditResponse)
async def create_edit_job(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...),
    target_duration: int = Form(default=15),
    platforms: str = Form(default="instagram_reels"),
    style: str = Form(default="algerian_minimal"),
    add_captions: bool = Form(default=True),
    language: str = Form(default="fr")
):
    """
    Lance un job de montage vidéo automatisé.
    
    - **video**: Fichier vidéo (MP4, MOV, AVI)
    - **target_duration**: Durée cible en secondes (5-120)
    - **platforms**: Plateformes cibles (instagram_reels, tiktok, youtube_shorts)
    - **style**: Style de montage
    - **add_captions**: Ajouter des sous-titres
    - **language**: Langue (fr, ar, en)
    """
    
    # Validate file type
    allowed_types = ["video/mp4", "video/quicktime", "video/x-msvideo", "video/webm"]
    if video.content_type not in allowed_types:
        raise HTTPException(400, f"Type de fichier non supporté: {video.content_type}")
    
    # Generate job ID
    job_id = str(uuid.uuid4())[:8]
    
    # Save uploaded file
    video_path = os.path.join(UPLOAD_DIR, f"{job_id}_{video.filename}")
    
    with open(video_path, "wb") as f:
        content = await video.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(400, "Fichier trop volumineux (max 500MB)")
        f.write(content)
    
    # Parse platforms
    platform_map = {
        "instagram_reels": Platform.INSTAGRAM_REELS,
        "tiktok": Platform.TIKTOK,
        "youtube_shorts": Platform.YOUTUBE_SHORTS,
        "square": Platform.SQUARE
    }
    
    platform_list = [
        platform_map.get(p.strip(), Platform.INSTAGRAM_REELS)
        for p in platforms.split(",")
    ]
    
    # Create config
    config = VideoOperatorConfig(
        target_duration=min(max(target_duration, 5), 120),
        platforms=platform_list,
        add_captions=add_captions,
        output_dir=OUTPUT_DIR
    )
    
    # Create job record
    jobs[job_id] = {
        "id": job_id,
        "status": "pending",
        "progress": 0,
        "message": "En attente de traitement...",
        "created_at": datetime.now().isoformat(),
        "language": language,
        "config": {
            "target_duration": target_duration,
            "platforms": platforms,
            "style": style
        }
    }
    
    # Start background processing
    background_tasks.add_task(process_video_job, job_id, video_path, config)
    
    return EditResponse(
        job_id=job_id,
        status="pending",
        message="Job créé. Traitement en cours..."
    )


@app.get("/api/v1/status/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Récupère le statut d'un job de montage"""
    
    if job_id not in jobs:
        raise HTTPException(404, "Job non trouvé")
    
    job = jobs[job_id]
    
    return JobStatus(
        id=job["id"],
        status=job["status"],
        progress=job.get("progress", 0),
        message=job.get("message", ""),
        created_at=job["created_at"],
        completed_at=job.get("completed_at"),
        outputs=job.get("outputs"),
        error=job.get("error"),
        video_url=job.get("video_url")
    )


@app.get("/api/v1/download/{job_id}/{platform}")
async def download_video(job_id: str, platform: str):
    """Télécharge la vidéo montée pour une plateforme"""
    
    if job_id not in jobs:
        raise HTTPException(404, "Job non trouvé")
    
    job = jobs[job_id]
    
    if job["status"] != "completed":
        raise HTTPException(400, "Le montage n'est pas terminé")
    
    outputs = job.get("outputs", {})
    
    if platform not in outputs:
        raise HTTPException(404, f"Pas de vidéo pour la plateforme: {platform}")
    
    video_path = outputs[platform]
    
    if not os.path.exists(video_path):
        raise HTTPException(404, "Fichier vidéo introuvable")
    
    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=f"edited_{job_id}_{platform}.mp4"
    )


@app.get("/api/v1/jobs")
async def list_jobs(limit: int = 10):
    """Liste les derniers jobs"""
    
    sorted_jobs = sorted(
        jobs.values(),
        key=lambda j: j["created_at"],
        reverse=True
    )[:limit]
    
    return {
        "jobs": [
            {
                "id": j["id"],
                "status": j["status"],
                "progress": j.get("progress", 0),
                "created_at": j["created_at"]
            }
            for j in sorted_jobs
        ]
    }


@app.delete("/api/v1/jobs/{job_id}")
async def delete_job(job_id: str):
    """Supprime un job et ses fichiers"""
    
    if job_id not in jobs:
        raise HTTPException(404, "Job non trouvé")
    
    job = jobs[job_id]
    
    # Delete output files
    if "outputs" in job:
        for path in job["outputs"].values():
            try:
                if os.path.exists(path):
                    os.unlink(path)
            except:
                pass
    
    del jobs[job_id]
    
    return {"message": "Job supprimé"}


# ============================================================
# TEMPLATES ENDPOINTS
# ============================================================

@app.get("/api/v1/templates")
async def list_templates():
    """Liste les templates de montage disponibles"""
    
    return {
        "templates": [
            {
                "id": "algerian_minimal",
                "name": "Algérien Minimaliste",
                "name_ar": "الجزائري البسيط",
                "description": "Style épuré avec couleurs algériennes",
                "icon": "🇩🇿"
            },
            {
                "id": "product_demo",
                "name": "Démo Produit",
                "name_ar": "عرض المنتج",
                "description": "Idéal pour présenter un produit",
                "icon": "📦"
            },
            {
                "id": "food_promo",
                "name": "Promo Restaurant",
                "name_ar": "ترويج المطعم",
                "description": "Pour restaurants et food",
                "icon": "🍽️"
            },
            {
                "id": "cinematic",
                "name": "Cinématique",
                "name_ar": "سينمائي",
                "description": "Style film professionnel",
                "icon": "🎬"
            },
            {
                "id": "energetic",
                "name": "Énergique",
                "name_ar": "نشيط",
                "description": "Rythme rapide, dynamique",
                "icon": "⚡"
            }
        ]
    }


@app.get("/api/v1/platforms")
async def list_platforms():
    """Liste les plateformes supportées"""
    
    return {
        "platforms": [
            {
                "id": "instagram_reels",
                "name": "Instagram Reels",
                "aspect_ratio": "9:16",
                "max_duration": 90
            },
            {
                "id": "tiktok",
                "name": "TikTok",
                "aspect_ratio": "9:16",
                "max_duration": 180
            },
            {
                "id": "youtube_shorts",
                "name": "YouTube Shorts",
                "aspect_ratio": "9:16",
                "max_duration": 60
            },
            {
                "id": "square",
                "name": "Square (Feed)",
                "aspect_ratio": "1:1",
                "max_duration": 60
            }
        ]
    }


# ============================================================
# MAIN
# ============================================================



# ============================================================
# JSON ENDPOINT - Pour le frontend dzirvideo-ai
# ============================================================

from pydantic import BaseModel as BaseModelGen

class GenerateRequest(BaseModelGen):
    prompt: str
    duration: int = 15
    voiceover: Optional[str] = None
    voiceover_lang: str = "fr"
    style: str = "cinematic"


@app.post("/api/v1/generate")
async def generate_video_from_text(
    request: GenerateRequest,
    background_tasks: BackgroundTasks
):
    job_id = str(uuid.uuid4())[:8]
    
    jobs[job_id] = {
        "id": job_id,
        "status": "processing",
        "progress": 10,
        "message": "Generation IA en cours...",
        "created_at": datetime.now().isoformat(),
        "type": "text-to-video"
    }
    
    background_tasks.add_task(
        generate_video_task, 
        job_id, 
        request.prompt, 
        request.duration, 
        request.voiceover, 
        request.voiceover_lang
    )
    
    return {"job_id": job_id, "status": "processing", "message": "Generation lancee"}


async def generate_video_task(job_id: str, prompt: str, duration: int, voiceover: str, voiceover_lang: str):
    """REAL video generation using Replicate Minimax"""
    try:
        import replicate
        from dotenv import load_dotenv
        load_dotenv("/opt/iafactory-rag-dz/agents/video-operator/.env")
        
        REPLICATE_TOKEN = os.getenv("REPLICATE_API_TOKEN")
        if not REPLICATE_TOKEN:
            raise Exception("REPLICATE_API_TOKEN not configured")
        
        jobs[job_id]["progress"] = 10
        jobs[job_id]["message"] = "Connexion Replicate IA..."
        
        client = replicate.Client(api_token=REPLICATE_TOKEN)
        
        jobs[job_id]["progress"] = 20
        jobs[job_id]["message"] = "Lancement generation Minimax video-01..."
        
        # Create real prediction with Minimax
        prediction = client.predictions.create(
            model="minimax/video-01",
            input={"prompt": prompt, "prompt_optimizer": True}
        )
        
        jobs[job_id]["prediction_id"] = prediction.id
        jobs[job_id]["progress"] = 30
        jobs[job_id]["message"] = "Generation IA en cours..."
        
        # Poll for completion (up to 5 minutes)
        max_wait = 300
        waited = 0
        while waited < max_wait:
            await asyncio.sleep(5)
            waited += 5
            
            p = client.predictions.get(prediction.id)
            progress = min(30 + int(waited / max_wait * 60), 90)
            jobs[job_id]["progress"] = progress
            
            if p.status == "succeeded":
                jobs[job_id]["status"] = "completed"
                jobs[job_id]["progress"] = 100
                jobs[job_id]["message"] = "Video generee avec succes!"
                jobs[job_id]["video_url"] = p.output
                return
                
            elif p.status == "failed":
                raise Exception(p.error or "Generation failed on Replicate")
                
            jobs[job_id]["message"] = f"Generation IA Minimax... ({waited}s)"
        
        raise Exception("Timeout - generation trop longue")
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["message"] = "Erreur: " + str(e)
