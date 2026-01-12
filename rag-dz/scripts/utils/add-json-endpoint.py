# Script à exécuter sur le VPS pour ajouter endpoint JSON
# Usage: python3 add-json-endpoint.py

endpoint_code = '''
# ============================================================
# JSON ENDPOINT - Pour le frontend dzirvideo-ai
# ============================================================

from pydantic import BaseModel

class GenerateRequest(BaseModel):
    """Requête de génération vidéo depuis prompt texte"""
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
    """
    Génère une vidéo à partir d'un prompt texte.
    Endpoint compatible avec le frontend dzirvideo-ai.
    """
    job_id = str(uuid.uuid4())[:8]
    
    jobs[job_id] = {
        "id": job_id,
        "status": "processing",
        "progress": 10,
        "message": "Génération IA en cours...",
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
    
    return {"job_id": job_id, "status": "processing", "message": "Génération lancée"}


async def generate_video_task(job_id: str, prompt: str, duration: int, voiceover: str, voiceover_lang: str):
    """Task de génération vidéo en background"""
    import aiohttp
    
    try:
        jobs[job_id]["progress"] = 20
        jobs[job_id]["message"] = "Préparation génération..."
        
        # Mode démo - simule la génération
        for i in range(3, 11):
            await asyncio.sleep(1)
            jobs[job_id]["progress"] = i * 10
            messages = [
                "Analyse du prompt...",
                "Génération des frames...",
                "Création séquences vidéo...",
                "Ajout effets visuels...",
                "Synchronisation audio...",
                "Montage final...",
                "Encodage vidéo...",
                "Finalisation..."
            ]
            jobs[job_id]["message"] = messages[i-3] if i-3 < len(messages) else "Traitement..."
        
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["message"] = "Vidéo générée avec succès!"
        jobs[job_id]["video_url"] = "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["message"] = f"Erreur: {str(e)}"
'''

# Ajoute au fichier api.py
with open('/opt/iafactory-rag-dz/agents/video-operator/api.py', 'a') as f:
    f.write(endpoint_code)

print("Endpoint ajouté!")
