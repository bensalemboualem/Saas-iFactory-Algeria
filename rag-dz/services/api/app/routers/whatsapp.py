"""
WhatsApp API Router via Twilio
Handles WhatsApp messaging through Twilio's WhatsApp Business API
"""
from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/whatsapp", tags=["whatsapp"])


# ============================================
# Models
# ============================================

class WhatsAppMessage(BaseModel):
    """WhatsApp message model"""
    id: Optional[str] = None
    to: str = Field(..., description="Recipient phone number with country code (e.g., +213555123456)")
    body: str = Field(..., description="Message body")
    media_url: Optional[str] = Field(None, description="URL of media to send (image, document, etc.)")
    template_name: Optional[str] = Field(None, description="Template name for approved messages")
    template_params: Optional[List[str]] = Field(None, description="Template parameters")
    status: Optional[str] = "pending"
    created_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None


class SendWhatsAppRequest(BaseModel):
    """Request to send WhatsApp message"""
    to: str = Field(..., description="Recipient phone number with country code")
    body: str = Field(..., description="Message content")
    media_url: Optional[str] = None


class SendTemplateRequest(BaseModel):
    """Request to send WhatsApp template message"""
    to: str = Field(..., description="Recipient phone number with country code")
    template_name: str = Field(..., description="Approved template name")
    template_params: Optional[List[str]] = Field(default=[], description="Template parameters")


class BulkWhatsAppRequest(BaseModel):
    """Request to send bulk WhatsApp messages"""
    recipients: List[str] = Field(..., description="List of phone numbers")
    body: str = Field(..., description="Message content")
    media_url: Optional[str] = None


class WhatsAppWebhookPayload(BaseModel):
    """Incoming WhatsApp webhook payload from Twilio"""
    MessageSid: Optional[str] = None
    From: Optional[str] = None
    To: Optional[str] = None
    Body: Optional[str] = None
    NumMedia: Optional[str] = None
    MediaUrl0: Optional[str] = None
    MediaContentType0: Optional[str] = None
    ProfileName: Optional[str] = None
    WaId: Optional[str] = None


class WhatsAppStats(BaseModel):
    """WhatsApp usage statistics"""
    messages_sent_today: int = 0
    messages_received_today: int = 0
    messages_sent_week: int = 0
    messages_received_week: int = 0
    delivery_rate: float = 0.0
    read_rate: float = 0.0
    response_rate: float = 0.0
    average_response_time: str = "N/A"


class WhatsAppConfig(BaseModel):
    """WhatsApp configuration status"""
    is_configured: bool = False
    whatsapp_number: Optional[str] = None
    is_sandbox: bool = True
    templates_available: List[str] = []


# ============================================
# In-memory storage (replace with DB in production)
# ============================================

message_history: List[dict] = []
received_messages: List[dict] = []


# ============================================
# Endpoints
# ============================================

@router.get("/config", response_model=WhatsAppConfig)
async def get_whatsapp_config():
    """Get WhatsApp configuration status"""
    from ..services.whatsapp_service import whatsapp_service
    return whatsapp_service.get_config()


@router.post("/send", response_model=WhatsAppMessage)
async def send_whatsapp_message(request: SendWhatsAppRequest, background_tasks: BackgroundTasks):
    """
    Send a WhatsApp message

    Note: For sandbox, recipient must have joined with "join <sandbox-code>"
    For production, use approved templates for first contact
    """
    from ..services.whatsapp_service import whatsapp_service

    try:
        result = await whatsapp_service.send_message(
            to=request.to,
            body=request.body,
            media_url=request.media_url
        )

        # Store in history
        message_history.append({
            **result.dict(),
            "direction": "outbound"
        })

        return result
    except Exception as e:
        logger.error(f"Failed to send WhatsApp message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-template", response_model=WhatsAppMessage)
async def send_template_message(request: SendTemplateRequest):
    """
    Send a WhatsApp template message

    Templates must be pre-approved by WhatsApp/Meta
    Used for initiating conversations or sending notifications
    """
    from ..services.whatsapp_service import whatsapp_service

    try:
        result = await whatsapp_service.send_template_message(
            to=request.to,
            template_name=request.template_name,
            template_params=request.template_params
        )

        message_history.append({
            **result.dict(),
            "direction": "outbound",
            "is_template": True
        })

        return result
    except Exception as e:
        logger.error(f"Failed to send template message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-bulk")
async def send_bulk_whatsapp(request: BulkWhatsAppRequest, background_tasks: BackgroundTasks):
    """
    Send WhatsApp messages to multiple recipients

    Messages are queued and sent in background
    """
    from ..services.whatsapp_service import whatsapp_service

    # Queue messages for background sending
    task_id = f"bulk_wa_{datetime.now().timestamp()}"

    background_tasks.add_task(
        whatsapp_service.send_bulk_messages,
        recipients=request.recipients,
        body=request.body,
        media_url=request.media_url,
        task_id=task_id
    )

    return {
        "status": "queued",
        "task_id": task_id,
        "recipient_count": len(request.recipients),
        "message": f"Sending to {len(request.recipients)} recipients"
    }


@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    """
    Webhook endpoint for incoming WhatsApp messages from Twilio

    Configure this URL in Twilio Console:
    https://your-domain.com/api/whatsapp/webhook
    """
    try:
        form_data = await request.form()
        payload = dict(form_data)

        logger.info(f"Received WhatsApp webhook: {payload}")

        # Extract message details
        message_sid = payload.get("MessageSid")
        from_number = payload.get("From", "").replace("whatsapp:", "")
        to_number = payload.get("To", "").replace("whatsapp:", "")
        body = payload.get("Body", "")
        profile_name = payload.get("ProfileName", "Unknown")
        wa_id = payload.get("WaId", "")

        # Check for media
        num_media = int(payload.get("NumMedia", "0"))
        media_urls = []
        for i in range(num_media):
            media_url = payload.get(f"MediaUrl{i}")
            if media_url:
                media_urls.append(media_url)

        # Store received message
        received_message = {
            "id": message_sid,
            "from": from_number,
            "to": to_number,
            "body": body,
            "profile_name": profile_name,
            "wa_id": wa_id,
            "media_urls": media_urls,
            "received_at": datetime.now().isoformat(),
            "direction": "inbound"
        }
        received_messages.append(received_message)

        logger.info(f"WhatsApp message from {profile_name} ({from_number}): {body}")

        # Return TwiML response (empty = no auto-reply)
        # You can add auto-reply logic here
        return """<?xml version="1.0" encoding="UTF-8"?>
<Response></Response>"""

    except Exception as e:
        logger.error(f"WhatsApp webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/messages")
async def get_message_history(
    limit: int = 50,
    direction: Optional[str] = None
):
    """
    Get WhatsApp message history

    Args:
        limit: Maximum number of messages to return
        direction: Filter by 'inbound' or 'outbound'
    """
    all_messages = message_history + received_messages

    if direction:
        all_messages = [m for m in all_messages if m.get("direction") == direction]

    # Sort by timestamp (newest first)
    all_messages.sort(
        key=lambda x: x.get("created_at") or x.get("received_at") or "",
        reverse=True
    )

    return all_messages[:limit]


@router.get("/messages/received")
async def get_received_messages(limit: int = 50):
    """Get received WhatsApp messages"""
    return sorted(
        received_messages,
        key=lambda x: x.get("received_at", ""),
        reverse=True
    )[:limit]


@router.get("/stats", response_model=WhatsAppStats)
async def get_whatsapp_stats():
    """Get WhatsApp usage statistics"""
    from ..services.whatsapp_service import whatsapp_service
    return await whatsapp_service.get_stats()


@router.get("/templates")
async def get_available_templates():
    """
    Get list of available WhatsApp message templates

    Templates must be approved by WhatsApp before use
    """
    # In production, fetch from Twilio/Meta API
    # For now, return common template examples
    return {
        "templates": [
            {
                "name": "appointment_reminder",
                "description": "Rappel de rendez-vous",
                "body": "Bonjour {{1}}, rappel de votre RDV le {{2}} à {{3}}. Répondez OUI pour confirmer.",
                "params": ["patient_name", "date", "time"],
                "status": "approved"
            },
            {
                "name": "appointment_confirmation",
                "description": "Confirmation de rendez-vous",
                "body": "Votre RDV du {{1}} à {{2}} est confirmé. Cabinet Dr {{3}}.",
                "params": ["date", "time", "doctor_name"],
                "status": "approved"
            },
            {
                "name": "results_ready",
                "description": "Résultats disponibles",
                "body": "Bonjour {{1}}, vos résultats d'analyse sont disponibles. Contactez-nous au {{2}}.",
                "params": ["patient_name", "phone"],
                "status": "approved"
            },
            {
                "name": "welcome_message",
                "description": "Message de bienvenue",
                "body": "Bienvenue {{1}}! Vous êtes maintenant connecté à notre service WhatsApp. Comment puis-je vous aider?",
                "params": ["name"],
                "status": "approved"
            }
        ]
    }


@router.post("/test-sandbox")
async def test_sandbox_connection():
    """
    Test WhatsApp sandbox connection

    Returns sandbox join instructions if not configured
    """
    from ..services.whatsapp_service import whatsapp_service

    config = whatsapp_service.get_config()

    if not config.is_configured:
        return {
            "status": "not_configured",
            "message": "Twilio credentials not configured",
            "instructions": [
                "1. Get your Twilio Account SID and Auth Token from console.twilio.com",
                "2. Add TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN to your .env file",
                "3. For sandbox: Add TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886",
                "4. Have recipients send 'join <your-sandbox-code>' to the sandbox number"
            ]
        }

    return {
        "status": "configured",
        "is_sandbox": config.is_sandbox,
        "whatsapp_number": config.whatsapp_number,
        "message": "WhatsApp is configured and ready to use"
    }
