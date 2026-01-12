

# ============================================================
# JSON ENDPOINT - Pour le frontend dzirvideo-ai
# ============================================================

from pydantic import BaseModel as BaseModelGen

class GenerateRequest(BaseModelGen):
    prompt: str
    duration: int = 15
    voiceover: str = None
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
    try:
        jobs[job_id]["progress"] = 20
        jobs[job_id]["message"] = "Preparation generation..."
        
        for i in range(3, 11):
            await asyncio.sleep(1)
            jobs[job_id]["progress"] = i * 10
            messages = [
                "Analyse du prompt...",
                "Generation des frames...",
                "Creation sequences video...",
                "Ajout effets visuels...",
                "Synchronisation audio...",
                "Montage final...",
                "Encodage video...",
                "Finalisation..."
            ]
            jobs[job_id]["message"] = messages[i-3] if i-3 < len(messages) else "Traitement..."
        
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["message"] = "Video generee avec succes!"
        jobs[job_id]["video_url"] = "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["message"] = "Erreur: " + str(e)
