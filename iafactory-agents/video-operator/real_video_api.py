"""
IA Factory Video Operator - REAL Video Generation
Kling AI + Voix-off + Musique + Montage FFmpeg
"""

import os
import uuid
import asyncio
import subprocess
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv("/opt/iafactory-rag-dz/agents/video-operator/.env")

# ============================================================
# CONFIG
# ============================================================

OUTPUT_DIR = "/opt/iafactory-rag-dz/outputs/video-operator"
MUSIC_DIR = "/opt/iafactory-rag-dz/assets/music"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)

jobs: Dict[str, Dict[str, Any]] = {}

# ============================================================
# MODELS
# ============================================================

class GenerateRequest(BaseModel):
    prompt: str
    duration: int = 10
    voiceover: Optional[str] = None
    voiceover_lang: str = "fr"
    style: str = "professional"
    add_music: bool = True
    model: str = "kling"  # kling, wan, minimax, veo
import httpx

# ============================================================
# VIDEO GENERATION - Google Veo (Gemini API)
# ============================================================

async def generate_with_veo(prompt: str, duration: int = 8, aspect_ratio: str = "16:9", resolution: str = "1080p") -> dict:
    """Generate video with Google Veo (Gemini API)"""
    api_key = os.getenv("GOOGLE_GENAI_API_KEY")
    if not api_key:
        raise Exception("Clé API Gemini (GOOGLE_GENAI_API_KEY) manquante dans .env")
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/veo-3.1:generateVideo"
    headers = {"Content-Type": "application/json"}
    params = {"key": api_key}
    payload = {
        "prompt": {"text": prompt},
        "aspectRatio": aspect_ratio,
        "resolution": resolution,
        "durationSeconds": duration
    }
    async with httpx.AsyncClient(timeout=180) as client:
        # Lancement de la génération
        r = await client.post(endpoint, headers=headers, params=params, json=payload)
        if r.status_code != 200:
            raise Exception(f"Erreur API Veo: {r.text}")
        op = r.json()
        operation_id = op.get("name")
        if not operation_id:
            raise Exception("Réponse API Veo invalide: pas d'ID d'opération")
        # Polling jusqu'à ce que done = true
        poll_url = f"https://generativelanguage.googleapis.com/v1beta/{operation_id}"
        for _ in range(60):  # Jusqu'à 5 min
            await asyncio.sleep(5)
            poll = await client.get(poll_url, params=params)
            if poll.status_code != 200:
                continue
            poll_data = poll.json()
            if poll_data.get("done"):
                # Cherche l'URL de la vidéo générée
                try:
                    video_url = poll_data["response"]["generatedVideos"][0]["videoUri"]
                    return {"url": video_url, "duration": duration}
                except Exception:
                    raise Exception(f"Réponse finale Veo inattendue: {poll_data}")
        raise Exception("Timeout Veo: vidéo non générée après 5 minutes")

class JobStatus(BaseModel):
    id: str
    status: str
    progress: int = 0
    message: str = ""
    created_at: str
    video_url: Optional[str] = None
    error: Optional[str] = None

# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="IA Factory Video Operator - PRO",
    description="Generation video IA avec Kling + Voix-off + Montage",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# VIDEO GENERATION - Replicate Minimax
# ============================================================

async def generate_with_kling(prompt: str, duration: int = 10) -> dict:
    """Generate video with Minimax via Replicate (fallback since FAL exhausted)"""
    import replicate
    
    token = os.getenv("REPLICATE_API_TOKEN")
    client = replicate.Client(api_token=token)
    
    prediction = client.predictions.create(
        model="minimax/video-01",
        input={
            "prompt": prompt,
            "prompt_optimizer": True
        }
    )
    
    # Wait for completion
    max_wait = 300
    waited = 0
    while waited < max_wait:
        await asyncio.sleep(5)
        waited += 5
        p = client.predictions.get(prediction.id)
        
        if p.status == "succeeded":
            return {"url": p.output, "duration": 5}
        elif p.status == "failed":
            raise Exception(p.error or "Generation failed")
    
    raise Exception("Timeout")

async def generate_with_wan(prompt: str, duration: int = 5) -> dict:
    """Same as kling for now - uses Minimax"""
    return await generate_with_kling(prompt, duration)

# ============================================================
# VOIX-OFF - Google TTS (gratuit)
# ============================================================

async def generate_voiceover(text: str, lang: str = "fr", output_path: str = None) -> str:
    """Generate voiceover using Google TTS (free, reliable)"""
    from gtts import gTTS
    
    lang_codes = {
        "fr": "fr",
        "ar": "ar", 
        "en": "en"
    }
    
    lang_code = lang_codes.get(lang, "fr")
    output_path = output_path or f"/tmp/voiceover_{uuid.uuid4().hex[:8]}.mp3"
    
    tts = gTTS(text, lang=lang_code)
    tts.save(output_path)
    
    return output_path

# ============================================================
# MONTAGE FFMPEG
# ============================================================

def merge_video_audio(video_path: str, audio_path: str, output_path: str, music_path: str = None) -> str:
    """Merge video with voiceover and optional background music"""
    
    if music_path and os.path.exists(music_path):
        # Video + Voiceover + Music
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-i", music_path,
            "-filter_complex",
            "[1:a]volume=1.0[voice];[2:a]volume=0.3[music];[voice][music]amix=inputs=2:duration=first[aout]",
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path
        ]
    else:
        # Video + Voiceover only
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-map", "0:v",
            "-map", "1:a",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path
        ]
    
    subprocess.run(cmd, capture_output=True)
    return output_path

def concat_videos(video_paths: list, output_path: str) -> str:
    """Concatenate multiple video clips"""
    
    list_file = f"/tmp/concat_{uuid.uuid4().hex[:8]}.txt"
    with open(list_file, "w") as f:
        for vp in video_paths:
            f.write(f"file '{vp}'\n")
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        output_path
    ]
    
    subprocess.run(cmd, capture_output=True)
    os.remove(list_file)
    return output_path

def download_video(url: str, output_path: str) -> str:
    """Download video from URL"""
    import httpx
    
    with httpx.Client(timeout=120) as client:
        response = client.get(url)
        with open(output_path, "wb") as f:
            f.write(response.content)
    
    return output_path

# ============================================================
# MAIN GENERATION TASK
# ============================================================

async def generate_video_task(job_id: str, request: GenerateRequest):
    """Complete video generation pipeline"""
    try:
        jobs[job_id]["progress"] = 5
        jobs[job_id]["message"] = "Initialisation..."
        
        video_clips = []
        total_duration = request.duration
        clip_duration = 10 if request.model == "kling" else 5
        num_clips = max(1, (total_duration + clip_duration - 1) // clip_duration)
        
        # Generate video clips
        for i in range(num_clips):
            jobs[job_id]["progress"] = 10 + (i * 30 // num_clips)
            jobs[job_id]["message"] = f"Generation clip {i+1}/{num_clips} avec {request.model.upper()}..."
            if request.model == "kling":
                result = await generate_with_kling(request.prompt, clip_duration)
            elif request.model == "wan":
                result = await generate_with_wan(request.prompt, clip_duration)
            elif request.model == "veo":
                result = await generate_with_veo(request.prompt, duration=clip_duration)
            else:
                raise Exception(f"Modèle inconnu: {request.model}")
            # Vérification de l'URL du clip
            clip_url = result.get("url")
            if not clip_url:
                raise Exception(f"Aucune URL vidéo retournée par le modèle {request.model} pour le clip {i+1}")
            clip_path = f"/tmp/clip_{job_id}_{i}.mp4"
            download_video(clip_url, clip_path)
            video_clips.append(clip_path)
        
        jobs[job_id]["progress"] = 50
        
        # Vérification des clips générés
        if not video_clips or not all(os.path.exists(clip) for clip in video_clips):
            raise Exception("Aucun clip vidéo généré ou téléchargé. Vérifiez le modèle et l'API.")
        # Concatenate if multiple clips
        if len(video_clips) > 1:
            jobs[job_id]["message"] = "Assemblage des clips..."
            video_path = f"/tmp/video_{job_id}.mp4"
            concat_videos(video_clips, video_path)
        else:
            video_path = video_clips[0]
        
        jobs[job_id]["progress"] = 60
        
        # Generate voiceover if provided
        audio_path = None
        if request.voiceover:
            jobs[job_id]["message"] = "Generation voix-off..."
            audio_path = await generate_voiceover(
                request.voiceover, 
                request.voiceover_lang
            )
            jobs[job_id]["progress"] = 75
        
        # Final output
        output_filename = f"video_{job_id}.mp4"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        if audio_path:
            jobs[job_id]["message"] = "Montage final avec voix-off..."
            # Check for background music
            music_path = os.path.join(MUSIC_DIR, f"{request.style}.mp3")
            if not os.path.exists(music_path):
                music_path = None
            
            merge_video_audio(video_path, audio_path, output_path, music_path)
        else:
            # Just copy the video
            import shutil
            shutil.copy(video_path, output_path)
        
        jobs[job_id]["progress"] = 95
        jobs[job_id]["message"] = "Finalisation..."
        
        # Cleanup temp files
        for clip in video_clips:
            if os.path.exists(clip):
                os.remove(clip)
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
        
        # Set final URL
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["message"] = "Video generee avec succes!"
        jobs[job_id]["video_url"] = f"/outputs/{output_filename}"
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["message"] = f"Erreur: {str(e)}"

# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "video-operator-v2-PRO",
        "version": "2.0.0",
        "features": ["kling", "wan", "voiceover", "montage"],
        "jobs_active": len([j for j in jobs.values() if j.get("status") == "processing"])
    }

@app.post("/api/v1/generate")
async def generate_video(request: GenerateRequest, background_tasks: BackgroundTasks):
    job_id = uuid.uuid4().hex[:8]
    
    jobs[job_id] = {
        "id": job_id,
        "status": "processing",
        "progress": 0,
        "message": "Demarrage...",
        "created_at": datetime.now().isoformat(),
        "video_url": None,
        "error": None
    }
    
    background_tasks.add_task(generate_video_task, job_id, request)
    
    return {"job_id": job_id, "status": "processing", "message": "Generation lancee"}

@app.get("/api/v1/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")
    
    job = jobs[job_id]
    return JobStatus(
        id=job["id"],
        status=job["status"],
        progress=job.get("progress", 0),
        message=job.get("message", ""),
        created_at=job["created_at"],
        video_url=job.get("video_url"),
        error=job.get("error")
    )

@app.get("/outputs/{filename}")
async def download_output(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found")
    return FileResponse(file_path, media_type="video/mp4", filename=filename)

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8085)
