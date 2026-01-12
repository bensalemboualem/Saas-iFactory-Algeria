"""
Studio Creatif - Generation Video (Wan 2.1 via Hugging Face)
Router pour la generation de videos IA avec Agent Scenariste local + Rendu GPU cloud
"""
import json
import logging
import httpx
import os
import base64
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..services.user_key_service import debit_key, get_key
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# --- CONFIGURATION ---
# API Keys
HF_API_TOKEN = os.getenv("HF_API_TOKEN", os.getenv("HUGGINGFACE_API_KEY", ""))
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")
PIAPI_KEY = os.getenv("PIAPI_KEY", "")  # Pour Wan 2.5 avec audio

# Couts par type de generation
VIDEO_COST_USD = 0.00  # GRATUIT (free tier)
IMAGE_COST_USD = 0.00  # GRATUIT

router = APIRouter(prefix="/api/studio", tags=["Creative Studio"])


class VideoGenerationRequest(BaseModel):
    user_prompt: str
    user_id: str
    key_code: Optional[str] = None
    duration: int = 5  # Duree en secondes (Wan 2.1 supporte 5-10s)
    aspect_ratio: str = "16:9"
    style: str = "photorealistic"


class ImageGenerationRequest(BaseModel):
    user_prompt: str
    user_id: str
    key_code: Optional[str] = None
    aspect_ratio: str = "1:1"
    style: str = "photorealistic"


class PresentationGenerationRequest(BaseModel):
    user_prompt: str
    user_id: str
    key_code: Optional[str] = None
    num_slides: int = 5
    theme: str = "dark"


async def call_local_llm(prompt: str, model: str = "qwen:7b") -> dict:
    """
    Appel au LLM local (Ollama/Qwen) pour le scripting intelligent.
    """
    ollama_url = os.getenv("OLLAMA_API_BASE_URL", "http://localhost:11434")

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                }
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "content": result.get("response", ""),
                    "technical_prompt": result.get("response", "")[:500]
                }
            else:
                logger.warning(f"Ollama returned status {response.status_code}")
                return {"success": False, "error": "LLM local indisponible"}

    except Exception as e:
        logger.error(f"Erreur appel LLM local: {e}")
        return {
            "success": True,
            "content": prompt,
            "technical_prompt": prompt,
            "fallback": True
        }


async def call_groq_llm(prompt: str) -> dict:
    """
    Fallback vers Groq si Ollama indisponible.
    """
    groq_api_key = os.getenv("GROQ_API_KEY", "")

    if not groq_api_key:
        return {"success": False, "error": "Groq API key not configured"}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {groq_api_key}"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 500
                }
            )

            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                return {
                    "success": True,
                    "content": content,
                    "technical_prompt": content[:500]
                }
            else:
                return {"success": False, "error": f"Groq error: {response.status_code}"}

    except Exception as e:
        logger.error(f"Erreur appel Groq: {e}")
        return {"success": False, "error": str(e)}


async def generate_video_replicate(prompt: str, duration: int = 5) -> dict:
    """
    Generation video via Replicate (Wan 2.1 ou autre modele)
    """
    if not REPLICATE_API_TOKEN:
        return {"success": False, "error": "REPLICATE_API_TOKEN non configure"}

    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            # Lancer la prediction
            response = await client.post(
                "https://api.replicate.com/v1/predictions",
                headers={
                    "Authorization": f"Bearer {REPLICATE_API_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "version": "alibaba-pai/wan2.1-t2v-14b",  # Wan 2.1 Text-to-Video
                    "input": {
                        "prompt": prompt,
                        "num_frames": duration * 8,  # ~8 fps
                        "guidance_scale": 7.5,
                        "num_inference_steps": 30
                    }
                }
            )

            if response.status_code == 201:
                prediction = response.json()
                prediction_id = prediction.get("id")

                # Polling pour attendre le resultat (max 5 minutes)
                for _ in range(60):
                    await asyncio.sleep(5)

                    status_response = await client.get(
                        f"https://api.replicate.com/v1/predictions/{prediction_id}",
                        headers={"Authorization": f"Bearer {REPLICATE_API_TOKEN}"}
                    )

                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data.get("status")

                        if status == "succeeded":
                            output = status_data.get("output")
                            video_url = output if isinstance(output, str) else output[0] if output else None
                            return {
                                "success": True,
                                "video_url": video_url,
                                "prediction_id": prediction_id
                            }
                        elif status == "failed":
                            return {"success": False, "error": status_data.get("error", "Generation failed")}

                return {"success": False, "error": "Timeout - generation trop longue"}
            else:
                logger.error(f"Replicate error: {response.status_code} - {response.text}")
                return {"success": False, "error": f"Replicate error: {response.status_code}"}

    except Exception as e:
        logger.error(f"Erreur Replicate: {e}")
        return {"success": False, "error": str(e)}


@router.post("/generate-video")
async def generate_video(request: VideoGenerationRequest):
    """
    Generation de video IA avec workflow Wan 2.1:
    1. Agent Scenariste (Qwen/Groq) - Optimisation du prompt
    2. Debit Wallet - Securite economique
    3. Wan 2.1 via Replicate - Generation video
    """

    # Etape 1: Agent Scenariste (Scripting Intelligent)
    scripter_prompt = f"""Optimise ce prompt pour la generation video IA (Wan 2.1):

CONCEPT: "{request.user_prompt}"

Genere un prompt technique en anglais, detaille et cinematographique.
Inclus: mouvements de camera, eclairage, style visuel, atmosphere.
Maximum 200 mots. Style: {request.style}

Reponds UNIQUEMENT avec le prompt optimise, sans explication."""

    llm_response = await call_local_llm(scripter_prompt)
    if not llm_response.get("success"):
        llm_response = await call_groq_llm(scripter_prompt)

    if llm_response.get("success"):
        optimized_prompt = llm_response.get("content", request.user_prompt)[:500]
    else:
        optimized_prompt = f"Cinematic {request.style} video of {request.user_prompt}, smooth camera movement, professional lighting, high quality, 4K"

    # Etape 2: Debit Wallet (si cle fournie)
    if request.key_code:
        debit_result = await debit_key(
            request.key_code,
            VIDEO_COST_USD,
            f"Wan 2.1 Video Generation - {request.duration}s"
        )
        if not debit_result.success:
            raise HTTPException(status_code=402, detail=f"Solde insuffisant: {debit_result.message}")

    # Etape 3: Generation video via PiAPI (Wan 2.2 - meilleure qualite)
    if PIAPI_KEY:
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.piapi.ai/api/v1/task",
                    headers={
                        "x-api-key": PIAPI_KEY,
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "Qubico/wanx",
                        "task_type": "wan22-txt2video-14b",
                        "input": {
                            "prompt": optimized_prompt,
                            "aspect_ratio": request.aspect_ratio
                        }
                    }
                )

                if response.status_code in [200, 201]:
                    result = response.json()
                    task_id = result.get("data", {}).get("task_id") or result.get("task_id")

                    return {
                        "status": "processing",
                        "prediction_id": task_id,
                        "provider": "piapi",
                        "prompt": optimized_prompt,
                        "engine": "Wan 2.2 14B (PiAPI)",
                        "message": "Video Wan 2.2 lancee! Generation en cours (~2-3 min)..."
                    }
                else:
                    logger.warning(f"PiAPI error: {response.status_code} - {response.text[:200]}")
                    # Fallback to Replicate
        except Exception as e:
            logger.warning(f"PiAPI failed, fallback to Replicate: {e}")

    # Fallback: Replicate (sans son)
    if not REPLICATE_API_TOKEN:
        return {
            "status": "demo",
            "message": "Configurez PIAPI_KEY ou REPLICATE_API_TOKEN",
            "prompt": optimized_prompt,
            "video_url": None,
            "engine": "Demo Mode"
        }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.replicate.com/v1/models/minimax/video-01/predictions",
                headers={
                    "Authorization": f"Bearer {REPLICATE_API_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "input": {
                        "prompt": optimized_prompt,
                        "prompt_optimizer": True
                    }
                }
            )

            if response.status_code in [200, 201]:
                result = response.json()
                prediction_id = result.get("id")

                return {
                    "status": "processing",
                    "prediction_id": prediction_id,
                    "provider": "replicate",
                    "prompt": optimized_prompt,
                    "engine": "MiniMax Video-01 (sans son)",
                    "message": "Video lancee! Generation en cours (~2-3 min)..."
                }
            else:
                error_text = response.text[:300]
                logger.error(f"Replicate error: {response.status_code} - {error_text}")
                raise HTTPException(status_code=503, detail=f"Replicate: {error_text}")

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout - la generation prend du temps, reessayez")
    except Exception as e:
        logger.error(f"Erreur generation video: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/video-status/{prediction_id}")
async def get_video_status(prediction_id: str, provider: str = "replicate"):
    """
    Verifier le statut d'une generation video en cours.
    provider: "piapi" ou "replicate"
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # PiAPI (Wan 2.2)
            if provider == "piapi" and PIAPI_KEY:
                response = await client.get(
                    f"https://api.piapi.ai/api/v1/task/{prediction_id}",
                    headers={"x-api-key": PIAPI_KEY}
                )

                if response.status_code == 200:
                    data = response.json()
                    task_data = data.get("data", data)
                    status = task_data.get("status", "unknown")

                    result = {
                        "prediction_id": prediction_id,
                        "status": status,
                        "provider": "piapi",
                        "engine": "Wan 2.2 14B (PiAPI)"
                    }

                    if status == "completed":
                        works = task_data.get("output", {}).get("works", [])
                        if works:
                            resource = works[0].get("resource", {})
                            result["video_url"] = resource.get("resourceWithoutWatermark") or resource.get("resource")
                        result["status"] = "succeeded"
                        result["message"] = "Video generee avec succes!"
                    elif status == "failed":
                        result["error"] = task_data.get("error", "Generation echouee")
                    elif status in ["pending", "processing"]:
                        result["status"] = "processing"
                        result["message"] = "Generation en cours..."

                    return result
                else:
                    logger.warning(f"PiAPI status error: {response.status_code}")

            # Replicate (fallback)
            if REPLICATE_API_TOKEN:
                response = await client.get(
                    f"https://api.replicate.com/v1/predictions/{prediction_id}",
                    headers={"Authorization": f"Bearer {REPLICATE_API_TOKEN}"}
                )

                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status")

                    result = {
                        "prediction_id": prediction_id,
                        "status": status,
                        "created_at": data.get("created_at"),
                        "provider": "replicate",
                        "engine": "MiniMax Video-01"
                    }

                    if status == "succeeded":
                        output = data.get("output")
                        result["video_url"] = output if isinstance(output, str) else (output[0] if output else None)
                        result["message"] = "Video generee avec succes!"
                    elif status == "failed":
                        result["error"] = data.get("error", "Generation echouee")
                    elif status == "processing":
                        result["message"] = "Generation en cours..."
                        result["logs"] = data.get("logs", "")[-500:]

                    return result

            raise HTTPException(status_code=404, detail="Prediction non trouvee")

    except Exception as e:
        logger.error(f"Erreur status video: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-image")
async def generate_image(request: ImageGenerationRequest):
    """
    Generation d'image IA via Replicate (Flux)
    """
    enhanced_prompt = f"{request.style}, {request.user_prompt}, high quality, detailed"

    if request.key_code:
        debit_result = await debit_key(request.key_code, IMAGE_COST_USD, "Image Generation")
        if not debit_result.success:
            raise HTTPException(status_code=402, detail=debit_result.message)

    if not REPLICATE_API_TOKEN:
        return {
            "status": "demo",
            "message": "Mode demo - REPLICATE_API_TOKEN requis",
            "prompt": enhanced_prompt,
            "estimated_cost": IMAGE_COST_USD,
            "image_url": None
        }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.replicate.com/v1/predictions",
                headers={
                    "Authorization": f"Bearer {REPLICATE_API_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "version": "black-forest-labs/flux-schnell",
                    "input": {
                        "prompt": enhanced_prompt,
                        "aspect_ratio": request.aspect_ratio,
                        "output_format": "webp"
                    }
                }
            )

            if response.status_code == 201:
                prediction = response.json()
                return {
                    "status": "processing",
                    "prediction_id": prediction.get("id"),
                    "poll_url": prediction.get("urls", {}).get("get"),
                    "prompt": enhanced_prompt,
                    "estimated_cost": IMAGE_COST_USD
                }
            else:
                raise HTTPException(status_code=503, detail="Service indisponible")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-presentation")
async def generate_presentation(request: PresentationGenerationRequest):
    """
    Generation de presentation Reveal.js (Gamma-Killer)
    """
    presentation_prompt = f"""Cree une presentation de {request.num_slides} slides sur: "{request.user_prompt}"

FORMAT: Markdown avec separateurs (---)
THEME: {request.theme}

Pour chaque slide:
- Titre (## )
- 3-4 points cles
- Suggestion visuelle

Commence directement avec le Markdown."""

    llm_response = await call_local_llm(presentation_prompt)
    if not llm_response.get("success"):
        llm_response = await call_groq_llm(presentation_prompt)

    if not llm_response.get("success"):
        raise HTTPException(status_code=503, detail="Service LLM indisponible")

    content = llm_response.get("content", "")
    slides = content.split("---")

    return {
        "status": "success",
        "num_slides": len(slides),
        "theme": request.theme,
        "markdown_content": content,
        "slides": [{"index": i, "content": slide.strip()} for i, slide in enumerate(slides)],
        "cost_usd": 0.001,
        "message": "Presentation generee avec succes"
    }


@router.get("/pricing")
async def get_studio_pricing():
    """
    Grille tarifaire du Studio Creatif
    """
    hf_configured = bool(HF_API_TOKEN)

    return {
        "video": {
            "cost_usd": VIDEO_COST_USD,
            "description": "Video 3-5s Wan 2.1",
            "provider": "Hugging Face (Wan 2.1 - GRATUIT)",
            "available": hf_configured
        },
        "image": {
            "cost_usd": IMAGE_COST_USD,
            "description": "Image haute qualite",
            "provider": "Hugging Face (Flux - GRATUIT)",
            "available": hf_configured
        },
        "presentation": {
            "cost_usd": 0.001,
            "description": "Presentation Reveal.js",
            "provider": "LLM (Qwen/Groq)",
            "available": True
        },
        "currency": "USD",
        "hf_configured": hf_configured
    }
