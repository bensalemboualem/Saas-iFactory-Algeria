"""
DZ-VoiceAssistant Backend API
Assistant vocal pour iaFactory Algeria avec support FR + Darija

Endpoints:
- POST /api/voice/stt - Speech-to-Text (Whisper)
- POST /api/voice/route - Route vers assistants (RAG/Legal/Fiscal/Park)
- POST /api/voice/tts - Text-to-Speech
- GET /api/voice/health - Health check
"""

import os
import io
import base64
import tempfile
import logging
from typing import Optional, Literal
from datetime import datetime

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dz-voice-assistant")

# Environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
RAG_DZ_URL = os.getenv("RAG_DZ_URL", "http://iaf-rag-prod:3000")
LEGAL_API_URL = os.getenv("LEGAL_API_URL", "http://iaf-legal-assistant-prod:8197")
FISCAL_API_URL = os.getenv("FISCAL_API_URL", "http://iaf-fiscal-assistant-prod:8199")

# STT/TTS Provider config
STT_PROVIDER = os.getenv("STT_PROVIDER", "groq")  # groq, openai, local
TTS_PROVIDER = os.getenv("TTS_PROVIDER", "edge")  # edge, openai, local

app = FastAPI(
    title="DZ-VoiceAssistant API",
    description="Assistant vocal pour iaFactory Algeria - FR + Darija",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class STTResponse(BaseModel):
    text: str
    language_detected: str = "fr"
    duration_seconds: Optional[float] = None
    confidence: Optional[float] = None

class RouteRequest(BaseModel):
    text: str
    target: Literal["rag", "legal", "fiscal", "park"] = "rag"
    options: Optional[dict] = Field(default_factory=lambda: {
        "language": "auto",
        "return_audio": True
    })

class RouteResponse(BaseModel):
    text_answer: str
    audio_base64: Optional[str] = None
    source_module: str
    meta: dict = Field(default_factory=lambda: {"status": "ok", "details": ""})

class TTSRequest(BaseModel):
    text: str
    language: Literal["fr", "ar"] = "fr"
    voice: Literal["default", "female", "male"] = "default"

class TTSResponse(BaseModel):
    audio_base64: str
    format: str = "mp3"
    duration_estimate: Optional[float] = None

# ============================================================================
# STT (Speech-to-Text) FUNCTIONS
# ============================================================================

async def stt_groq(audio_bytes: bytes, language: str = "auto") -> STTResponse:
    """
    Transcription via GROQ Whisper API
    GROQ offre Whisper large-v3 gratuit et rapide
    """
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            # GROQ utilise l'endpoint audio/transcriptions compatible OpenAI
            files = {
                "file": ("audio.webm", audio_bytes, "audio/webm"),
                "model": (None, "whisper-large-v3"),
            }
            
            # Si langue spécifiée (pas auto)
            if language != "auto":
                lang_code = "fr" if language == "fr" else "ar"
                files["language"] = (None, lang_code)
            
            response = await client.post(
                "https://api.groq.com/openai/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                files=files
            )
            
            if response.status_code != 200:
                logger.error(f"GROQ STT Error: {response.text}")
                raise HTTPException(status_code=500, detail=f"STT Error: {response.text}")
            
            data = response.json()
            text = data.get("text", "")
            
            # Détection de langue simple basée sur caractères arabes
            has_arabic = any('\u0600' <= c <= '\u06FF' for c in text)
            detected_lang = "ar" if has_arabic else "fr"
            
            return STTResponse(
                text=text,
                language_detected=detected_lang,
                confidence=0.95  # GROQ Whisper est très précis
            )
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="STT timeout - audio trop long?")
    except Exception as e:
        logger.error(f"STT Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"STT Error: {str(e)}")


async def stt_openai(audio_bytes: bytes, language: str = "auto") -> STTResponse:
    """
    Transcription via OpenAI Whisper API
    """
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            files = {
                "file": ("audio.webm", audio_bytes, "audio/webm"),
                "model": (None, "whisper-1"),
            }
            
            if language != "auto":
                lang_code = "fr" if language == "fr" else "ar"
                files["language"] = (None, lang_code)
            
            response = await client.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                files=files
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"OpenAI STT Error: {response.text}")
            
            data = response.json()
            text = data.get("text", "")
            
            has_arabic = any('\u0600' <= c <= '\u06FF' for c in text)
            detected_lang = "ar" if has_arabic else "fr"
            
            return STTResponse(
                text=text,
                language_detected=detected_lang,
                confidence=0.95
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI STT Error: {str(e)}")


# ============================================================================
# TTS (Text-to-Speech) FUNCTIONS
# ============================================================================

async def tts_edge(text: str, language: str = "fr", voice: str = "default") -> bytes:
    """
    TTS via Edge TTS (gratuit, Microsoft)
    Supporte le français et l'arabe
    """
    try:
        import edge_tts
        
        # Sélection de la voix selon langue
        if language == "ar":
            # Voix arabe (on utilise arabe standard, proche darija)
            voice_name = "ar-DZ-AminaNeural" if voice in ["default", "female"] else "ar-DZ-IsmaelNeural"
        else:
            # Voix française
            voice_name = "fr-FR-DeniseNeural" if voice in ["default", "female"] else "fr-FR-HenriNeural"
        
        communicate = edge_tts.Communicate(text, voice_name)
        
        # Collecter l'audio en mémoire
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        return audio_data
        
    except ImportError:
        logger.warning("edge_tts not installed, falling back to silent response")
        return b""
    except Exception as e:
        logger.error(f"Edge TTS Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"TTS Error: {str(e)}")


async def tts_openai(text: str, language: str = "fr", voice: str = "default") -> bytes:
    """
    TTS via OpenAI API
    """
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # OpenAI voices
            voice_map = {
                "default": "alloy",
                "female": "nova",
                "male": "onyx"
            }
            
            response = await client.post(
                "https://api.openai.com/v1/audio/speech",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "tts-1",
                    "input": text,
                    "voice": voice_map.get(voice, "alloy"),
                    "response_format": "mp3"
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"OpenAI TTS Error: {response.text}")
            
            return response.content
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI TTS Error: {str(e)}")


# ============================================================================
# ROUTING FUNCTIONS - Appels aux autres assistants
# ============================================================================

async def call_rag(query: str) -> str:
    """Appel au RAG-DZ pour recherche documentaire"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{RAG_DZ_URL}/api/chat",
                json={"message": query, "mode": "hybrid"}
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", data.get("message", "Je n'ai pas trouvé de réponse."))
            else:
                return f"Erreur RAG: {response.status_code}"
                
    except Exception as e:
        logger.error(f"RAG call error: {str(e)}")
        return f"Erreur de connexion au RAG: {str(e)}"


async def call_legal(query: str) -> str:
    """Appel au DZ-LegalAssistant"""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{LEGAL_API_URL}/api/dz-legal/answer",
                json={"question": query, "category": "general"}
            )
            
            if response.status_code == 200:
                data = response.json()
                summary = data.get("summary", "")
                steps = data.get("steps", [])
                
                # Construire réponse vocale
                result = summary
                if steps and len(steps) > 0:
                    result += "\n\nÉtapes principales:\n"
                    for i, step in enumerate(steps[:3], 1):  # Max 3 étapes pour vocal
                        result += f"{i}. {step.get('title', '')}\n"
                
                return result
            else:
                return f"Erreur Legal: {response.status_code}"
                
    except Exception as e:
        logger.error(f"Legal call error: {str(e)}")
        return f"Erreur de connexion à l'assistant juridique: {str(e)}"


async def call_fiscal(query: str) -> str:
    """
    Appel au DZ-FiscalAssistant
    Note: Pour la voix, on fait un Q&A simplifié, pas une simulation complète
    """
    try:
        # Extraction basique de chiffres pour simulation simple
        import re
        numbers = re.findall(r'\d+(?:\s*\d+)*', query.replace(' ', ''))
        
        revenue = 0
        if numbers:
            # Prendre le premier nombre comme revenu
            revenue = int(numbers[0].replace(' ', ''))
        
        if revenue > 0:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{FISCAL_API_URL}/api/dz-fiscal/simulate",
                    json={
                        "profile_type": "freelance",
                        "regime_actuel": "IFU",
                        "revenue_amount": revenue,
                        "charges_amount": 0
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("summary", "Simulation effectuée.")
                else:
                    return f"Erreur Fiscal: {response.status_code}"
        else:
            # Sans montant, répondre de façon générique
            return """Pour une simulation fiscale, veuillez préciser votre revenu annuel. 
Par exemple: 'Calculez mes impôts pour un revenu de 5 millions de dinars'.
Je peux simuler l'IRG, l'IFU, la TAP et les cotisations CNAS/CASNOS."""
                
    except Exception as e:
        logger.error(f"Fiscal call error: {str(e)}")
        return f"Erreur de connexion à l'assistant fiscal: {str(e)}"


async def call_park(query: str) -> str:
    """Appel à iaFactoryPark (placeholder pour l'instant)"""
    return """iaFactoryPark propose des templates de projets IA.
Vous pouvez demander:
- Un template de chatbot
- Un template de système de recommandation
- Un template d'analyse de données
Tapez votre demande plus précisément."""


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/api/voice/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "DZ-VoiceAssistant",
        "timestamp": datetime.now().isoformat(),
        "stt_provider": STT_PROVIDER,
        "tts_provider": TTS_PROVIDER,
        "supported_languages": ["fr", "ar"],
        "targets": ["rag", "legal", "fiscal", "park"]
    }


@app.post("/api/voice/stt", response_model=STTResponse)
async def speech_to_text(
    audio: UploadFile = File(..., description="Audio file (webm, ogg, wav, mp3)"),
    language: str = Form(default="auto", description="Language: auto, fr, ar")
):
    """
    🎙️ Speech-to-Text - Convertit l'audio en texte
    
    Supporte:
    - Français (fr)
    - Arabe/Darija (ar)
    - Détection automatique (auto)
    
    Formats audio: webm, ogg, wav, mp3
    Durée max: 60 secondes
    """
    logger.info(f"STT Request - file: {audio.filename}, language: {language}")
    
    # Vérifier le type de fichier
    allowed_types = ["audio/webm", "audio/ogg", "audio/wav", "audio/mpeg", "audio/mp3", 
                     "video/webm", "application/octet-stream"]
    if audio.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Type de fichier non supporté: {audio.content_type}. Utilisez webm, ogg, wav ou mp3."
        )
    
    # Lire l'audio
    audio_bytes = await audio.read()
    
    # Vérifier la taille (max 25MB pour Whisper)
    max_size = 25 * 1024 * 1024  # 25MB
    if len(audio_bytes) > max_size:
        raise HTTPException(status_code=400, detail="Fichier trop volumineux (max 25MB)")
    
    # Appeler le STT selon le provider configuré
    if STT_PROVIDER == "groq":
        result = await stt_groq(audio_bytes, language)
    elif STT_PROVIDER == "openai":
        result = await stt_openai(audio_bytes, language)
    else:
        raise HTTPException(status_code=500, detail=f"STT provider inconnu: {STT_PROVIDER}")
    
    logger.info(f"STT Result - text: {result.text[:100]}..., lang: {result.language_detected}")
    return result


@app.post("/api/voice/route", response_model=RouteResponse)
async def route_to_assistant(request: RouteRequest):
    """
    🔀 Route la question vers l'assistant approprié
    
    Targets:
    - rag: Recherche documentaire RAG-DZ
    - legal: Assistant juridique DZ-LegalAssistant
    - fiscal: Assistant fiscal DZ-FiscalAssistant
    - park: iaFactoryPark templates
    
    Options:
    - language: auto, fr, ar
    - return_audio: true/false (génère la réponse vocale)
    """
    logger.info(f"Route Request - target: {request.target}, text: {request.text[:50]}...")
    
    options = request.options or {}
    return_audio = options.get("return_audio", True)
    language = options.get("language", "auto")
    
    # Router vers le bon assistant
    if request.target == "rag":
        text_answer = await call_rag(request.text)
    elif request.target == "legal":
        text_answer = await call_legal(request.text)
    elif request.target == "fiscal":
        text_answer = await call_fiscal(request.text)
    elif request.target == "park":
        text_answer = await call_park(request.text)
    else:
        raise HTTPException(status_code=400, detail=f"Target inconnu: {request.target}")
    
    # Générer l'audio si demandé
    audio_base64 = None
    if return_audio and text_answer:
        try:
            # Détecter la langue pour TTS
            has_arabic = any('\u0600' <= c <= '\u06FF' for c in text_answer)
            tts_lang = "ar" if has_arabic else "fr"
            
            # Limiter la longueur pour TTS (max 1000 caractères)
            text_for_tts = text_answer[:1000]
            if len(text_answer) > 1000:
                text_for_tts += "... Pour plus de détails, consultez la réponse écrite."
            
            if TTS_PROVIDER == "edge":
                audio_bytes = await tts_edge(text_for_tts, tts_lang)
            elif TTS_PROVIDER == "openai":
                audio_bytes = await tts_openai(text_for_tts, tts_lang)
            else:
                audio_bytes = b""
            
            if audio_bytes:
                audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
                
        except Exception as e:
            logger.error(f"TTS Error in route: {str(e)}")
            # Continue sans audio si erreur TTS
    
    return RouteResponse(
        text_answer=text_answer,
        audio_base64=audio_base64,
        source_module=request.target,
        meta={
            "status": "ok",
            "details": f"Réponse de {request.target}",
            "has_audio": audio_base64 is not None
        }
    )


@app.post("/api/voice/tts", response_model=TTSResponse)
async def text_to_speech(request: TTSRequest):
    """
    🔊 Text-to-Speech - Convertit le texte en audio
    
    Languages:
    - fr: Français
    - ar: Arabe/Darija
    
    Voices:
    - default: Voix par défaut
    - female: Voix féminine
    - male: Voix masculine
    """
    logger.info(f"TTS Request - lang: {request.language}, voice: {request.voice}, text: {request.text[:50]}...")
    
    # Limiter la longueur du texte
    max_chars = 5000
    if len(request.text) > max_chars:
        raise HTTPException(status_code=400, detail=f"Texte trop long (max {max_chars} caractères)")
    
    # Générer l'audio
    if TTS_PROVIDER == "edge":
        audio_bytes = await tts_edge(request.text, request.language, request.voice)
    elif TTS_PROVIDER == "openai":
        audio_bytes = await tts_openai(request.text, request.language, request.voice)
    else:
        raise HTTPException(status_code=500, detail=f"TTS provider inconnu: {TTS_PROVIDER}")
    
    if not audio_bytes:
        raise HTTPException(status_code=500, detail="Erreur génération audio")
    
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
    
    # Estimation durée (environ 150 mots/minute)
    word_count = len(request.text.split())
    duration_estimate = (word_count / 150) * 60  # en secondes
    
    return TTSResponse(
        audio_base64=audio_base64,
        format="mp3",
        duration_estimate=duration_estimate
    )


@app.get("/api/voice/voices")
async def list_voices():
    """Liste les voix disponibles pour le TTS"""
    return {
        "provider": TTS_PROVIDER,
        "voices": {
            "fr": [
                {"id": "fr-FR-DeniseNeural", "name": "Denise", "gender": "female", "default": True},
                {"id": "fr-FR-HenriNeural", "name": "Henri", "gender": "male"}
            ],
            "ar": [
                {"id": "ar-DZ-AminaNeural", "name": "Amina", "gender": "female", "default": True},
                {"id": "ar-DZ-IsmaelNeural", "name": "Ismael", "gender": "male"}
            ]
        },
        "note": "ar-DZ: Arabe algérien (le plus proche de la darija)"
    }


@app.get("/api/voice/targets")
async def list_targets():
    """Liste les assistants cibles disponibles"""
    return {
        "targets": [
            {
                "id": "rag",
                "name": "RAG-DZ",
                "description": "Recherche documentaire dans la base de connaissances",
                "icon": "📚"
            },
            {
                "id": "legal",
                "name": "Assistant Juridique",
                "description": "Questions sur le droit et les démarches administratives algériennes",
                "icon": "⚖️"
            },
            {
                "id": "fiscal",
                "name": "Assistant Fiscal",
                "description": "Simulation d'impôts et questions fiscales (IFU, IRG, TAP, CNAS...)",
                "icon": "💰"
            },
            {
                "id": "park",
                "name": "iaFactoryPark",
                "description": "Templates et modèles de projets IA",
                "icon": "🏗️"
            }
        ]
    }


# ============================================================================
# STARTUP
# ============================================================================

@app.on_event("startup")
async def startup_event():
    logger.info("🎙️ DZ-VoiceAssistant API starting...")
    logger.info(f"   STT Provider: {STT_PROVIDER}")
    logger.info(f"   TTS Provider: {TTS_PROVIDER}")
    logger.info(f"   GROQ API Key: {'✓' if GROQ_API_KEY else '✗'}")
    logger.info(f"   RAG URL: {RAG_DZ_URL}")
    logger.info(f"   Legal API URL: {LEGAL_API_URL}")
    logger.info(f"   Fiscal API URL: {FISCAL_API_URL}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8201)
