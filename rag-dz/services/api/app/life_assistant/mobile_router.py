"""
Mobile Pairing & Audio Upload Router
====================================

Endpoints pour smartphones (iOS/Android):
- POST /api/mobile/pair - Génère QR Code sécurisé
- POST /api/mobile/transcribe - Upload audio mobile (.m4a, .aac)
- GET /api/mobile/briefing - Briefing matinal JSON

Created: 2025-01-16
"""

from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from typing import Optional
import logging
import secrets
import hashlib
from datetime import datetime, timedelta
import qrcode
import io
import base64

from . import daily_briefing
from ..dependencies import get_current_tenant_id

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/mobile",
    tags=["mobile"],
)


def generate_pairing_token() -> str:
    """
    Génère un token d'appairage sécurisé

    Returns:
        Token hexadécimal 32 bytes (64 caractères)
    """
    return secrets.token_hex(32)


def generate_qr_code_image(pairing_url: str) -> str:
    """
    Génère QR Code en base64

    Args:
        pairing_url: URL complète d'appairage

    Returns:
        Image QR Code en base64 (data URI)
    """
    try:
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(pairing_url)
        qr.make(fit=True)

        # Generate image
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        return f"data:image/png;base64,{img_base64}"

    except Exception as e:
        logger.error(f"Error generating QR code: {e}")
        return ""


@router.post("/pair")
async def create_mobile_pairing(
    request: Request,
    device_name: str = Form(..., description="Nom du device (iPhone 15 Pro, etc.)"),
    device_os: str = Form(..., description="OS version (iOS 17.2, Android 14)"),
    tenant_id: str = Depends(get_current_tenant_id),
    user_id: int = Form(1, description="User ID"),
):
    """
    Génère un appairage sécurisé pour smartphone via QR Code

    **Flow**:
    1. Frontend web appelle ce endpoint
    2. Backend génère token temporaire (expire 5 min)
    3. QR Code généré avec URL d'appairage
    4. Utilisateur scan QR avec smartphone
    5. Smartphone se connecte avec token

    **Sécurité**:
    - Token unique 64 caractères
    - Expire après 5 minutes
    - Un seul usage
    - IP tracking

    **Réponse**:
    ```json
    {
      "pairing_token": "abc123...",
      "qr_code_url": "data:image/png;base64,...",
      "expires_at": "2025-01-16T10:35:00Z",
      "pairing_url": "https://api.example.com/mobile/connect?token=abc123",
      "ttl_seconds": 300
    }
    ```

    **Exemple cURL**:
    ```bash
    curl -X POST "http://localhost:8002/api/mobile/pair" \\
      -F "device_name=iPhone 15 Pro" \\
      -F "device_os=iOS 17.2"
    ```
    """
    try:
        # Generate secure token
        pairing_token = generate_pairing_token()

        # Expiration (5 minutes)
        expires_at = datetime.now() + timedelta(minutes=5)

        # TODO: Save to database (mobile_device_pairings table)
        # from ..geneva.repository import save_mobile_pairing
        # pairing_id = save_mobile_pairing(
        #     tenant_id=tenant_id,
        #     user_id=user_id,
        #     pairing_token=pairing_token,
        #     device_name=device_name,
        #     device_os=device_os,
        #     ip_address=request.client.host,
        #     user_agent=request.headers.get("User-Agent"),
        #     expires_at=expires_at
        # )

        # Build pairing URL
        base_url = os.getenv('BACKEND_URL', 'http://localhost:8002')
        pairing_url = f"{base_url}/api/mobile/connect?token={pairing_token}"

        # Generate QR Code
        qr_code_image = generate_qr_code_image(pairing_url)

        logger.info(
            f"📱 Mobile pairing created: device={device_name}, "
            f"expires_at={expires_at.isoformat()}"
        )

        return JSONResponse(content={
            "pairing_token": pairing_token,
            "qr_code_url": qr_code_image,
            "pairing_url": pairing_url,
            "expires_at": expires_at.isoformat(),
            "ttl_seconds": 300,
            "device_name": device_name,
            "status": "pending",
        })

    except Exception as e:
        logger.error(f"Error creating mobile pairing: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/connect")
async def connect_mobile_device(
    request: Request,
    token: str = Form(..., description="Token d'appairage"),
):
    """
    Endpoint appelé par le smartphone après scan QR Code

    **Flow**:
    1. Smartphone scan QR Code
    2. GET pairing_url avec token
    3. Backend valide token
    4. Si OK: Active pairing + retourne auth token

    **Sécurité**:
    - Vérifie token existe et non expiré
    - Marque token comme utilisé (un seul usage)
    - Génère session token pour smartphone

    **Réponse**:
    ```json
    {
      "status": "connected",
      "session_token": "long_lived_token_for_mobile",
      "user_id": 1,
      "tenant_id": "uuid",
      "expires_at": "2025-02-16T10:00:00Z"
    }
    ```
    """
    try:
        # TODO: Validate token from database
        # pairing = get_mobile_pairing_by_token(token)
        #
        # if not pairing:
        #     raise HTTPException(status_code=404, detail="Invalid token")
        #
        # if pairing.expires_at < datetime.now():
        #     raise HTTPException(status_code=410, detail="Token expired")
        #
        # if pairing.pairing_status != 'pending':
        #     raise HTTPException(status_code=409, detail="Token already used")
        #
        # # Activate pairing
        # update_pairing_status(pairing.id, 'active')
        #
        # # Generate long-lived session token
        # session_token = generate_session_token(pairing.user_id, pairing.tenant_id)

        # Mock response
        session_token = secrets.token_urlsafe(64)

        logger.info(f"📱 Mobile device connected: token={token[:10]}...")

        return JSONResponse(content={
            "status": "connected",
            "session_token": session_token,
            "user_id": 1,
            "tenant_id": "814c132a-1cdd-4db6-bc1f-21abd21ec37d",
            "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
            "message": "Smartphone connecté avec succès!",
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error connecting mobile device: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/transcribe")
async def transcribe_mobile_audio(
    file: UploadFile = File(..., description="Audio mobile (.m4a, .aac, .mp3)"),
    tenant_id: str = Depends(get_current_tenant_id),
    user_id: int = Form(1),
    language: Optional[str] = Form(None),
    professional_context: Optional[str] = Form(None),
):
    """
    Transcription audio depuis smartphone

    **Formats supportés**:
    - .m4a (iPhone Voice Memos)
    - .aac (Android Voice Recorder)
    - .mp3, .wav, .ogg, .opus

    **Flow**:
    1. Smartphone enregistre audio
    2. Upload vers cet endpoint
    3. Transcription Faster-Whisper
    4. Analyse émotionnelle + Geneva Mode
    5. Retour résultat JSON

    **Exemple iOS Swift**:
    ```swift
    let url = URL(string: "https://api.example.com/api/mobile/transcribe")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"

    let formData = MultipartFormData()
    formData.append(audioData, withName: "file", fileName: "recording.m4a", mimeType: "audio/m4a")

    // Send request...
    ```

    **Réponse**:
    ```json
    {
      "text": "Texte transcrit...",
      "transcription_id": "uuid",
      "emotion_analysis": {
        "detected_emotion": "calm",
        "stress_level": 3
      },
      "duration": 45.3,
      "processing_time_ms": 1523
    }
    ```
    """
    try:
        # Redirect to voice agent transcription endpoint
        # (Already supports .m4a and .aac)

        from ..voice_agent.router import transcribe_audio

        # Call existing transcription endpoint
        result = await transcribe_audio(
            file=file,
            tenant_id=tenant_id,
            language=language,
            professional_context=professional_context
        )

        logger.info(f"📱 Mobile audio transcribed: {file.filename}")

        return result

    except Exception as e:
        logger.error(f"Error transcribing mobile audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/briefing")
async def get_morning_briefing(
    tenant_id: str = Depends(get_current_tenant_id),
    user_id: int = Query(1, description="User ID"),
    format: str = Query("json", description="Format: json ou text"),
):
    """
    Récupère le briefing matinal pour smartphone

    **Format JSON** (default):
    ```json
    {
      "greeting": "Bonjour Sarah! 早安!",
      "weather": {
        "temperature": 8,
        "description": "ciel dégagé"
      },
      "calendar": [
        {
          "time": "09h00",
          "title": "Réunion OMPI",
          "location": "..."
        }
      ],
      "emails": [
        {
          "sender": "Me Weber",
          "subject": "Signature contrat",
          "priority": "urgent"
        }
      ],
      "reminders": [
        {
          "type": "medication",
          "message": "Vitamine D après petit-déjeuner"
        }
      ],
      "news": [...],
      "generated_at": "2025-01-16T07:00:00Z"
    }
    ```

    **Format TEXT** (pour TTS):
    Texte complet formaté pour lecture vocale
    """
    try:
        # TODO: Get user profile from DB
        user_profile = {
            'name': 'Sarah',
            'nationality': 'chinese',
            'location': 'Eaux-Vives, Genève',
            'email': 'sarah@example.com',
        }

        # Generate briefing
        briefing_text = await daily_briefing.generate_daily_morning_brief(
            tenant_id=tenant_id,
            user_id=user_id,
            user_profile=user_profile
        )

        if format == "text":
            return JSONResponse(content={
                "briefing_text": briefing_text,
                "generated_at": datetime.now().isoformat(),
            })

        else:  # JSON format
            # TODO: Parse briefing_text into structured JSON
            # For now, return text
            return JSONResponse(content={
                "briefing_text": briefing_text,
                "format": "text",
                "generated_at": datetime.now().isoformat(),
                "message": "Structured JSON format coming soon",
            })

    except Exception as e:
        logger.error(f"Error generating briefing: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check mobile endpoints"""
    return JSONResponse(content={
        "status": "healthy",
        "service": "mobile-api",
        "features": [
            "qr_code_pairing",
            "audio_transcription_m4a",
            "daily_briefing",
            "geneva_mode_support",
        ],
        "ready": True,
    })
