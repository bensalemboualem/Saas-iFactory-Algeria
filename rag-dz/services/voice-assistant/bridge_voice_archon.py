#!/usr/bin/env python3
"""
Bridge Voice Agent -> Archon (Version Full-Stream v3.5 - Apertus Sovereign)
- /transcribe-audio : Accepte audio multipart, transcrit via Archon, enrichit
- /transcribe : Accepte texte + tenant, enrichit via RAG Multi-Query
- /youtube-extract : Extrait audio de YouTube (Privacy-First)
CORS Whitelist: *.iafactory.ch only
Multi-Tenant: Support swiss (CH) et algeria (DZ) via RAG contextualisé
Privacy: Apertus-compliant anonymization layer
"""

import asyncio
import aiohttp
from aiohttp import web
import logging
import json
import base64
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import subprocess
import tempfile
import os
import re
import hashlib

# ============= CONFIGURATION =============
ARCHON_API_URL = "http://localhost:8180"  # LLM + enrichissement (uses internal Qdrant)
WHISPER_API_URL = "http://localhost:8201"  # Voice Agent avec Whisper
QDRANT_URL = "http://127.0.0.1:6333"       # Qdrant direct IP (bypass DNS)
QDRANT_DZ_URL = "http://127.0.0.1:6332"    # Qdrant DZ tenant (separate instance)
BRIDGE_PORT = 8205
TENANT = "swiss"

# ============= APERTUS PRIVACY CONFIG =============
LOCAL_LLM_ENABLED = False                  # If True, route to local Ollama
LOCAL_LLM_URL = "http://127.0.0.1:11434"   # Ollama endpoint
LOCAL_LLM_MODEL = "llama3.1:8b"            # Default local model
ANONYMIZE_LOGS = True                      # Strip PII from logs

# Privacy patterns to anonymize
PRIVACY_PATTERNS = [
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]'),  # Emails
    (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[IP]'),                   # IPs
    (r'\b(?:\+?41|0041|0)[\s.-]?\d{2}[\s.-]?\d{3}[\s.-]?\d{2}[\s.-]?\d{2}\b', '[PHONE_CH]'),  # Swiss phones
    (r'\b(?:\+?213|00213|0)[\s.-]?\d{2,3}[\s.-]?\d{2,3}[\s.-]?\d{2,3}\b', '[PHONE_DZ]'),     # Algerian phones
    (r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[NAME]'),                           # Names (basic)
]

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def anonymize_text(text: str) -> str:
    """Apertus Privacy Layer: Anonymize PII before logging"""
    if not ANONYMIZE_LOGS:
        return text
    anonymized = text
    for pattern, replacement in PRIVACY_PATTERNS:
        anonymized = re.sub(pattern, replacement, anonymized)
    return anonymized


def get_request_hash(text: str) -> str:
    """Generate anonymous request ID for tracking without PII"""
    return hashlib.sha256(f"{text[:50]}{datetime.now(timezone.utc).isoformat()}".encode()).hexdigest()[:12]

# Prompt pour enrichissement LLM
ENRICHMENT_PROMPT = """Tu es un assistant d'analyse. Analyse le message suivant et retourne UNIQUEMENT un JSON valide avec cette structure exacte:
{
    "summary": "Resume en une phrase du message",
    "action_items": ["action 1", "action 2"],
    "priority": "high" ou "medium" ou "low"
}

Regles de priorite:
- high (rouge): urgence, probleme critique, deadline immediate
- medium (orange): demande standard, tache a planifier
- low (vert): information generale, question simple

Message a analyser: """


# === YouTube Utils ===
def validate_youtube_url(url: str) -> bool:
    patterns = [
        r'^(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+',
        r'^(https?://)?(www\.)?youtu\.be/[\w-]+',
        r'^(https?://)?(www\.)?youtube\.com/shorts/[\w-]+'
    ]
    return any(re.match(p, url) for p in patterns)


def extract_video_id(url: str) -> str:
    patterns = [r'(?:v=|youtu\.be/|shorts/)([a-zA-Z0-9_-]{11})']
    for p in patterns:
        match = re.search(p, url)
        if match:
            return match.group(1)
    return None


async def youtube_extract_audio(url: str):
    """Extract audio from YouTube - Privacy First (no storage)"""
    if not validate_youtube_url(url):
        return None, None, "URL YouTube invalide"

    video_id = extract_video_id(url)
    if not video_id:
        return None, None, "Impossible d'extraire l'ID video"

    logger.info(f"YouTube extract: {video_id}")

    temp_dir = tempfile.mkdtemp(prefix="yt_")
    output_path = os.path.join(temp_dir, f"{video_id}.mp3")

    try:
        cmd = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "128K",
            "--no-playlist",
            "--no-warnings",
            "--quiet",
            "--output", output_path,
            url
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            logger.error(f"yt-dlp error: {result.stderr}")
            return None, video_id, f"Extraction failed: {result.stderr[:200]}"

        if not os.path.exists(output_path):
            return None, video_id, "Audio file not created"

        with open(output_path, "rb") as f:
            audio_bytes = f.read()

        logger.info(f"Audio extracted: {len(audio_bytes)} bytes")
        return audio_bytes, video_id, None

    except subprocess.TimeoutExpired:
        return None, video_id, "Extraction timeout (max 2 min)"
    except Exception as e:
        logger.error(f"YouTube extract error: {e}")
        return None, video_id, str(e)
    finally:
        try:
            if os.path.exists(output_path):
                os.remove(output_path)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
        except:
            pass


class VoiceArchonBridge:
    def __init__(self):
        self.session = None
        self.last_enriched_data: Optional[Dict[str, Any]] = None
        self.history: list = []

    async def init_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def close_session(self):
        if self.session:
            await self.session.close()

    def detect_priority(self, text: str) -> str:
        lower_text = text.lower()
        high_keywords = ["urgent", "critique", "probleme", "erreur", "down", "panne", "immediat", "bloqu"]
        low_keywords = ["info", "bonjour", "merci", "question", "comment", "aide"]

        if any(kw in lower_text for kw in high_keywords):
            return "high"
        elif any(kw in lower_text for kw in low_keywords):
            return "low"
        return "medium"

    async def transcribe_audio_via_whisper(self, audio_bytes: bytes, mime_type: str = "audio/webm") -> Dict[str, Any]:
        try:
            await self.init_session()
            logger.info(f"=== WHISPER TRANSCRIPTION ===")
            logger.info(f"Audio size: {len(audio_bytes)} bytes, MIME: {mime_type}")

            form_data = aiohttp.FormData()
            form_data.add_field('file', audio_bytes, filename='recording.webm', content_type=mime_type)
            form_data.add_field('language', 'fr')

            whisper_url = f"{WHISPER_API_URL}/api/voice-agent/transcribe"
            logger.info(f"POST vers: {whisper_url}")

            async with self.session.post(whisper_url, data=form_data, timeout=aiohttp.ClientTimeout(total=60)) as response:
                response_text = await response.text()
                logger.info(f"Whisper response status: {response.status}")

                if response.status == 200:
                    data = json.loads(response_text)
                    transcription = data.get("transcription", data.get("text", ""))
                    return {"success": True, "transcription": transcription}
                else:
                    return {"success": False, "error": f"Whisper error: {response.status}"}
        except Exception as e:
            logger.error(f"Whisper transcription error: {e}")
            return {"success": False, "error": str(e)}

    async def enrich_via_archon(self, text: str, tenant: str = "swiss") -> Dict[str, Any]:
        """Enrich text via LLM with Apertus privacy logging"""
        request_id = get_request_hash(text)
        logger.info(f"[APERTUS] Enrichment request {request_id} | tenant={tenant} | text_preview={anonymize_text(text[:100])}")

        try:
            await self.init_session()

            # Route to Local LLM if enabled (Apertus Sovereign mode)
            if LOCAL_LLM_ENABLED:
                return await self._enrich_via_local_llm(text, tenant, request_id)

            # Use RAG multi query endpoint
            archon_url = f"{ARCHON_API_URL}/api/rag/multi/query"
            country = "ch" if tenant == "swiss" else "dz"

            payload = {
                "query": f"{ENRICHMENT_PROMPT}\n\nMessage: {text}",
                "country": country
            }

            async with self.session.post(archon_url, json=payload, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status == 200:
                    data = await response.json()
                    answer = data.get("answer", "")
                    logger.info(f"[APERTUS] Enrichment {request_id} SUCCESS via Archon RAG")
                    try:
                        enrichment = json.loads(answer)
                    except:
                        enrichment = {
                            "summary": answer[:300] if answer else text[:200],
                            "action_items": [],
                            "priority": self.detect_priority(text)
                        }
                    return enrichment
                else:
                    logger.warning(f"[APERTUS] Enrichment {request_id} FALLBACK (Archon status={response.status})")
                    return {"summary": text[:200], "action_items": [], "priority": self.detect_priority(text)}
        except Exception as e:
            logger.error(f"[APERTUS] Enrichment {request_id} ERROR: {e}")
            return {"summary": text[:200], "action_items": [], "priority": self.detect_priority(text)}

    async def _enrich_via_local_llm(self, text: str, tenant: str, request_id: str) -> Dict[str, Any]:
        """Route to local Ollama for Apertus Sovereign mode"""
        try:
            ollama_url = f"{LOCAL_LLM_URL}/api/generate"
            payload = {
                "model": LOCAL_LLM_MODEL,
                "prompt": f"{ENRICHMENT_PROMPT}\n\nMessage: {text}",
                "stream": False
            }

            async with self.session.post(ollama_url, json=payload, timeout=aiohttp.ClientTimeout(total=120)) as response:
                if response.status == 200:
                    data = await response.json()
                    answer = data.get("response", "")
                    logger.info(f"[APERTUS] Enrichment {request_id} SUCCESS via LOCAL LLM (Ollama)")
                    try:
                        enrichment = json.loads(answer)
                    except:
                        enrichment = {
                            "summary": answer[:300] if answer else text[:200],
                            "action_items": [],
                            "priority": self.detect_priority(text)
                        }
                    return enrichment
                else:
                    logger.warning(f"[APERTUS] Local LLM {request_id} status={response.status}")
                    return {"summary": text[:200], "action_items": [], "priority": self.detect_priority(text)}
        except Exception as e:
            logger.error(f"[APERTUS] Local LLM {request_id} ERROR: {e}")
            return {"summary": text[:200], "action_items": [], "priority": self.detect_priority(text)}

    async def get_archon_response(self, text: str, tenant: str = "swiss") -> str:
        """Get LLM response with Apertus privacy logging"""
        request_id = get_request_hash(text)
        logger.info(f"[APERTUS] Response request {request_id} | tenant={tenant}")

        try:
            await self.init_session()

            # Route to Local LLM if enabled (Apertus Sovereign mode)
            if LOCAL_LLM_ENABLED:
                return await self._get_local_llm_response(text, tenant, request_id)

            # Use RAG multi query endpoint
            archon_url = f"{ARCHON_API_URL}/api/rag/multi/query"
            country = "ch" if tenant == "swiss" else "dz"

            payload = {
                "query": text,
                "country": country
            }

            async with self.session.post(archon_url, json=payload, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"[APERTUS] Response {request_id} SUCCESS via Archon RAG | country={country}")
                    return data.get("answer", "")
                logger.warning(f"[APERTUS] Response {request_id} FAILED (status={response.status})")
                return ""
        except Exception as e:
            logger.error(f"[APERTUS] Response {request_id} ERROR: {e}")
            return ""

    async def _get_local_llm_response(self, text: str, tenant: str, request_id: str) -> str:
        """Route to local Ollama for Apertus Sovereign mode"""
        try:
            ollama_url = f"{LOCAL_LLM_URL}/api/generate"
            context = "Focus Suisse: standards helvetiques, droit suisse." if tenant == "swiss" else "Focus Algerie: lois algeriennes, marche local."

            payload = {
                "model": LOCAL_LLM_MODEL,
                "prompt": f"{context}\n\n{text}",
                "stream": False
            }

            async with self.session.post(ollama_url, json=payload, timeout=aiohttp.ClientTimeout(total=120)) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"[APERTUS] Response {request_id} SUCCESS via LOCAL LLM (Ollama)")
                    return data.get("response", "")
                logger.warning(f"[APERTUS] Local LLM Response {request_id} status={response.status}")
                return ""
        except Exception as e:
            logger.error(f"[APERTUS] Local LLM Response {request_id} ERROR: {e}")
            return ""

    async def handle_audio_transcription(self, request):
        try:
            reader = await request.multipart()
            audio_bytes = None
            mime_type = "audio/webm"

            async for part in reader:
                if part.name == "audio" or part.name == "file":
                    audio_bytes = await part.read()
                    mime_type = part.headers.get("Content-Type", "audio/webm")

            if not audio_bytes:
                return web.json_response({"error": "No audio data"}, status=400)

            whisper_result = await self.transcribe_audio_via_whisper(audio_bytes, mime_type)

            if not whisper_result.get("success"):
                return web.json_response({"error": whisper_result.get("error")}, status=500)

            transcription = whisper_result["transcription"]
            enriched_data = await self.enrich_via_archon(transcription)
            archon_response = await self.get_archon_response(transcription)

            self.last_enriched_data = {
                "transcription": transcription,
                "enrichment": enriched_data,
                "archon_response": archon_response,
                "timestamp": datetime.utcnow().isoformat(),
                "tenant": TENANT
            }
            self.history.insert(0, self.last_enriched_data)
            self.history = self.history[:50]

            return web.json_response({
                "status": "success",
                "transcription": transcription,
                "summary": enriched_data.get("summary", ""),
                "action_items": enriched_data.get("action_items", []),
                "priority": enriched_data.get("priority", "medium"),
                "archon_response": archon_response,
                "tenant": TENANT
            })
        except Exception as e:
            logger.error(f"Audio transcription error: {e}")
            return web.json_response({"error": str(e)}, status=500)

    async def handle_transcription(self, request):
        try:
            data = await request.json()
            text = data.get("text", "")
            # Support dynamic tenant from request
            request_tenant = data.get("tenant", TENANT)

            # ============= MUR DE FER: DZ-PRIVATE Marker =============
            dz_private = data.get("dz_private", False) or request.headers.get("X-DZ-Private", "").lower() == "true"
            is_algeria = request_tenant == "algeria" or dz_private

            # Privacy marker for Algeria requests
            privacy_marker = "[DZ-PRIVATE]" if is_algeria else "[CH-STANDARD]"

            if not text:
                return web.json_response({"error": "No text provided"}, status=400)

            logger.info(f"{privacy_marker} Processing transcription for tenant: {request_tenant} | dz_private={dz_private}")

            enriched_data = await self.enrich_via_archon(text, tenant=request_tenant)
            archon_response = await self.get_archon_response(text, tenant=request_tenant)

            self.last_enriched_data = {
                "transcription": text,
                "enrichment": enriched_data,
                "archon_response": archon_response,
                "timestamp": datetime.utcnow().isoformat(),
                "tenant": request_tenant
            }
            self.history.insert(0, self.last_enriched_data)
            self.history = self.history[:50]

            return web.json_response({
                "status": "success",
                "transcription": text,
                "summary": enriched_data.get("summary", ""),
                "action_items": enriched_data.get("action_items", []),
                "priority": enriched_data.get("priority", "medium"),
                "archon_response": archon_response,
                "output_text": archon_response,  # Alias for frontend compatibility
                "tenant": request_tenant
            })
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return web.json_response({"error": str(e)}, status=500)

    async def handle_youtube_extract(self, request):
        """POST /youtube-extract - Extract audio from YouTube (Privacy-First)"""
        try:
            data = await request.json()
            url = data.get("url", "")

            if not url:
                return web.json_response({"error": "URL required"}, status=400)

            logger.info(f"YouTube extract request: {url[:50]}...")

            audio_bytes, video_id, error = await youtube_extract_audio(url)

            if error:
                return web.json_response({"error": error, "video_id": video_id}, status=400)

            return web.Response(
                body=audio_bytes,
                content_type="audio/mpeg",
                headers={
                    "Content-Disposition": f"attachment; filename={video_id}.mp3",
                    "X-Video-ID": video_id or "unknown"
                }
            )
        except Exception as e:
            logger.error(f"YouTube extract error: {e}")
            return web.json_response({"error": str(e)}, status=500)

    async def get_latest(self, request):
        if self.last_enriched_data:
            return web.json_response(self.last_enriched_data)
        return web.json_response({"status": "no_data", "message": "Aucune transcription encore recue"})

    async def get_history(self, request):
        limit = int(request.query.get("limit", 10))
        return web.json_response({"history": self.history[:limit], "total": len(self.history)})

    async def health(self, request):
        return web.json_response({
            "status": "healthy",
            "service": "voice-archon-bridge-fullstream",
            "version": "3.5-apertus",
            "tenant": TENANT,
            "whisper_url": WHISPER_API_URL,
            "archon_url": ARCHON_API_URL,
            "qdrant_ch": QDRANT_URL,
            "qdrant_dz": QDRANT_DZ_URL,
            "endpoints": ["/transcribe-audio", "/transcribe", "/youtube-extract", "/latest", "/history", "/health"],
            "cors_mode": "whitelist",
            "allowed_origins": len(CORS_ALLOWED_ORIGINS),
            "apertus": {
                "privacy_mode": "enabled" if ANONYMIZE_LOGS else "disabled",
                "local_llm_enabled": LOCAL_LLM_ENABLED,
                "local_llm_url": LOCAL_LLM_URL if LOCAL_LLM_ENABLED else None
            },
            "last_activity": self.last_enriched_data["timestamp"] if self.last_enriched_data else None
        })


# CORS Whitelist - IAFactory domains only (Production: no localhost)
CORS_ALLOWED_ORIGINS = [
    "https://iafactory.ch",
    "https://www.iafactory.ch",
    "https://app.iafactory.ch",
    "https://cockpit.iafactory.ch",
    "https://bolt.iafactory.ch",
    "https://n8n.iafactory.ch",
    "https://iafactoryalgeria.com",
    "https://www.iafactoryalgeria.com",
    "https://app.iafactoryalgeria.com"
]


@web.middleware
async def cors_middleware(request, handler):
    origin = request.headers.get("Origin", "")

    # Check if origin is in whitelist
    allowed_origin = origin if origin in CORS_ALLOWED_ORIGINS else ""

    if request.method == "OPTIONS":
        response = web.Response()
    else:
        try:
            response = await handler(request)
        except web.HTTPException as e:
            response = e

    # Only set CORS headers if origin is allowed
    if allowed_origin:
        response.headers["Access-Control-Allow-Origin"] = allowed_origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
    else:
        # Fallback for server-to-server calls (no Origin header)
        if not origin:
            response.headers["Access-Control-Allow-Origin"] = "*"

    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Tenant, X-DZ-Private"
    return response


async def main():
    bridge = VoiceArchonBridge()

    app = web.Application(middlewares=[cors_middleware], client_max_size=100*1024*1024)
    app.router.add_post("/transcribe-audio", bridge.handle_audio_transcription)
    app.router.add_post("/transcribe", bridge.handle_transcription)
    app.router.add_post("/youtube-extract", bridge.handle_youtube_extract)
    app.router.add_get("/latest", bridge.get_latest)
    app.router.add_get("/history", bridge.get_history)
    app.router.add_get("/health", bridge.health)

    async def cleanup(app):
        await bridge.close_session()

    app.on_cleanup.append(cleanup)

    logger.info("=" * 50)
    logger.info("Voice-Archon Bridge FULL-STREAM v3.5 (Apertus Sovereign)")
    logger.info(f"Port: {BRIDGE_PORT}")
    logger.info(f"CORS: Whitelist mode ({len(CORS_ALLOWED_ORIGINS)} origins)")
    logger.info(f"Tenant: {TENANT}")
    logger.info(f"Whisper API: {WHISPER_API_URL}")
    logger.info(f"Archon API: {ARCHON_API_URL}")
    logger.info("Endpoints:")
    logger.info("  POST /transcribe-audio - Audio -> Whisper -> LLM")
    logger.info("  POST /transcribe       - Text -> LLM enrichment")
    logger.info("  POST /youtube-extract  - YouTube -> Audio (Privacy-First)")
    logger.info("  GET  /latest           - Last transcription")
    logger.info("  GET  /history          - History")
    logger.info("  GET  /health           - Status")
    logger.info("=" * 50)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", BRIDGE_PORT)
    await site.start()

    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bridge stopped")
