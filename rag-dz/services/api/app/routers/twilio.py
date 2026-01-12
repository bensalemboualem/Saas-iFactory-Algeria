"""
Twilio SMS Routes
Handles SMS sending, reminders, and webhooks
"""

from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import httpx
from datetime import datetime
import base64
import logging

router = APIRouter(prefix="/api/twilio", tags=["twilio"])
logger = logging.getLogger(__name__)

# Environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")

# In-memory storage for demo (use database in production)
message_history: List[Dict] = []
scheduled_reminders: List[Dict] = []


# ============================================
# Pydantic Models
# ============================================

class SendSMSRequest(BaseModel):
    to: str
    message: str
    templateId: Optional[str] = None
    templateVars: Optional[Dict[str, str]] = None


class BulkSMSRequest(BaseModel):
    recipients: List[str]
    template: str
    templateVars: Optional[Dict[str, str]] = None


class ScheduleReminderRequest(BaseModel):
    to: str
    message: str
    scheduledAt: str
    templateId: Optional[str] = None
    templateVars: Optional[Dict[str, str]] = None
    relatedTo: Optional[Dict[str, str]] = None


class SMSMessage(BaseModel):
    id: str
    to: str
    from_: str
    body: str
    status: str
    direction: str
    createdAt: str
    updatedAt: str
    errorCode: Optional[str] = None
    errorMessage: Optional[str] = None


class SMSTemplate(BaseModel):
    id: str
    name: str
    description: str
    body: str
    variables: List[str]
    category: str
    isActive: bool = True


# Pre-defined templates
SMS_TEMPLATES = [
    SMSTemplate(
        id="rappel_rdv_24h",
        name="Rappel RDV (24h)",
        description="Rappel automatique 24h avant le rendez-vous",
        body="Rappel: Votre RDV est prévu demain {date} à {heure}. Pour annuler: {link}",
        variables=["date", "heure", "link"],
        category="appointment",
    ),
    SMSTemplate(
        id="confirmation_rdv",
        name="Confirmation RDV",
        description="Confirmation de rendez-vous",
        body="Votre RDV du {date} à {heure} est confirmé. Dr. {nom}",
        variables=["date", "heure", "nom"],
        category="appointment",
    ),
    SMSTemplate(
        id="rappel_document",
        name="Rappel Document",
        description="Rappel pour apporter un document",
        body="Merci d'apporter {document} à votre prochain RDV.",
        variables=["document"],
        category="reminder",
    ),
    SMSTemplate(
        id="annulation",
        name="Annulation RDV",
        description="Notification d'annulation",
        body="Votre RDV du {date} a été annulé. Contactez-nous pour reprogrammer.",
        variables=["date"],
        category="appointment",
    ),
]


# ============================================
# Helper Functions
# ============================================

def get_twilio_auth():
    """Get Twilio Basic Auth header"""
    credentials = f"{TWILIO_ACCOUNT_SID}:{TWILIO_AUTH_TOKEN}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


async def send_twilio_sms(to: str, body: str) -> Dict:
    """Send SMS via Twilio API"""
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        # Mock response for development
        return {
            "sid": f"SM{datetime.now().strftime('%Y%m%d%H%M%S')}mock",
            "status": "queued",
            "to": to,
            "body": body,
        }

    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers={"Authorization": get_twilio_auth()},
            data={
                "To": to,
                "From": TWILIO_PHONE_NUMBER,
                "Body": body,
            },
            timeout=30.0,
        )

        if not response.is_success:
            error_data = response.json()
            raise HTTPException(
                status_code=response.status_code,
                detail=error_data.get("message", "Twilio API error"),
            )

        return response.json()


def render_template(template: str, variables: Dict[str, str]) -> str:
    """Render template with variables"""
    result = template
    for key, value in variables.items():
        result = result.replace(f"{{{key}}}", value)
    return result


# ============================================
# SMS Routes
# ============================================

@router.post("/sms/send")
async def send_sms(request: SendSMSRequest):
    """Send a single SMS"""
    message = request.message

    # Render template if provided
    if request.templateId and request.templateVars:
        template = next((t for t in SMS_TEMPLATES if t.id == request.templateId), None)
        if template:
            message = render_template(template.body, request.templateVars)

    try:
        result = await send_twilio_sms(request.to, message)

        # Store in history
        msg_data = {
            "id": result.get("sid", f"msg-{len(message_history)+1}"),
            "to": request.to,
            "from": TWILIO_PHONE_NUMBER or "+12345678901",
            "body": message,
            "status": result.get("status", "sent"),
            "direction": "outbound",
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat(),
        }
        message_history.insert(0, msg_data)

        return msg_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sms/bulk")
async def send_bulk_sms(request: BulkSMSRequest):
    """Send SMS to multiple recipients"""
    results = {"success": 0, "failed": 0, "messages": []}

    message = request.template
    if request.templateVars:
        message = render_template(message, request.templateVars)

    for recipient in request.recipients:
        try:
            result = await send_twilio_sms(recipient, message)
            msg_data = {
                "id": result.get("sid", f"msg-{len(message_history)+1}"),
                "to": recipient,
                "from": TWILIO_PHONE_NUMBER or "+12345678901",
                "body": message,
                "status": result.get("status", "sent"),
                "direction": "outbound",
                "createdAt": datetime.now().isoformat(),
                "updatedAt": datetime.now().isoformat(),
            }
            message_history.insert(0, msg_data)
            results["messages"].append(msg_data)
            results["success"] += 1
        except Exception as e:
            results["failed"] += 1
            logger.error(f"Failed to send to {recipient}: {e}")

    return results


@router.get("/sms/history")
async def get_history(limit: int = 50, offset: int = 0, direction: Optional[str] = None):
    """Get SMS message history"""
    filtered = message_history
    if direction:
        filtered = [m for m in filtered if m.get("direction") == direction]

    return {
        "messages": filtered[offset : offset + limit],
        "total": len(filtered),
    }


@router.get("/sms/{message_id}")
async def get_message(message_id: str):
    """Get a single message by ID"""
    msg = next((m for m in message_history if m["id"] == message_id), None)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg


# ============================================
# Reminder Routes
# ============================================

@router.post("/reminders")
async def schedule_reminder(request: ScheduleReminderRequest, background_tasks: BackgroundTasks):
    """Schedule a reminder SMS"""
    message = request.message

    if request.templateId and request.templateVars:
        template = next((t for t in SMS_TEMPLATES if t.id == request.templateId), None)
        if template:
            message = render_template(template.body, request.templateVars)

    reminder = {
        "id": f"rem-{len(scheduled_reminders)+1}",
        "to": request.to,
        "message": message,
        "scheduledAt": request.scheduledAt,
        "status": "pending",
        "createdAt": datetime.now().isoformat(),
        "relatedTo": request.relatedTo,
    }

    scheduled_reminders.append(reminder)

    # In production, use a proper job scheduler (Celery, APScheduler, etc.)
    # background_tasks.add_task(send_scheduled_reminder, reminder)

    return reminder


@router.get("/reminders")
async def get_reminders(status: Optional[str] = None):
    """Get scheduled reminders"""
    filtered = scheduled_reminders
    if status:
        filtered = [r for r in filtered if r["status"] == status]
    return filtered


@router.post("/reminders/{reminder_id}/cancel")
async def cancel_reminder(reminder_id: str):
    """Cancel a scheduled reminder"""
    reminder = next((r for r in scheduled_reminders if r["id"] == reminder_id), None)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")

    reminder["status"] = "cancelled"
    return {"success": True}


# ============================================
# Template Routes
# ============================================

@router.get("/templates")
async def get_templates():
    """Get all SMS templates"""
    return [t.dict() for t in SMS_TEMPLATES]


@router.get("/templates/{template_id}")
async def get_template(template_id: str):
    """Get a template by ID"""
    template = next((t for t in SMS_TEMPLATES if t.id == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template.dict()


# ============================================
# Statistics Routes
# ============================================

@router.get("/stats")
async def get_stats():
    """Get SMS statistics"""
    now = datetime.now()
    this_month = [
        m for m in message_history
        if datetime.fromisoformat(m["createdAt"]).month == now.month
    ]

    total_sent = len(message_history)
    total_delivered = len([m for m in message_history if m["status"] == "delivered"])
    total_failed = len([m for m in message_history if m["status"] == "failed"])

    month_sent = len(this_month)
    month_delivered = len([m for m in this_month if m["status"] == "delivered"])
    month_failed = len([m for m in this_month if m["status"] == "failed"])

    # Generate by day stats (last 7 days)
    by_day = []
    for i in range(6, -1, -1):
        from datetime import timedelta
        day = now - timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        day_msgs = [
            m for m in message_history
            if m["createdAt"].startswith(day_str)
        ]
        by_day.append({
            "date": day_str,
            "sent": len(day_msgs),
            "delivered": len([m for m in day_msgs if m["status"] == "delivered"]),
            "failed": len([m for m in day_msgs if m["status"] == "failed"]),
        })

    return {
        "totalSent": total_sent,
        "totalDelivered": total_delivered,
        "totalFailed": total_failed,
        "deliveryRate": (total_delivered / total_sent * 100) if total_sent > 0 else 0,
        "thisMonth": {
            "sent": month_sent,
            "delivered": month_delivered,
            "failed": month_failed,
        },
        "byDay": by_day,
    }


# ============================================
# Webhook Routes
# ============================================

@router.post("/webhook/status")
async def twilio_status_webhook(request: Request):
    """
    Receive status updates from Twilio
    Updates message status (delivered, failed, read, etc.)
    """
    form_data = await request.form()

    message_sid = form_data.get("MessageSid")
    message_status = form_data.get("MessageStatus")
    error_code = form_data.get("ErrorCode")
    error_message = form_data.get("ErrorMessage")

    logger.info(f"Twilio status update: {message_sid} -> {message_status}")

    # Update message in history
    for msg in message_history:
        if msg["id"] == message_sid:
            msg["status"] = message_status
            msg["updatedAt"] = datetime.now().isoformat()
            if error_code:
                msg["errorCode"] = error_code
            if error_message:
                msg["errorMessage"] = error_message
            break

    return {"success": True}


@router.post("/webhook/inbound")
async def twilio_inbound_webhook(request: Request):
    """
    Receive inbound SMS from Twilio
    """
    form_data = await request.form()

    message_data = {
        "id": form_data.get("MessageSid"),
        "to": form_data.get("To"),
        "from": form_data.get("From"),
        "body": form_data.get("Body"),
        "status": "received",
        "direction": "inbound",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
    }

    message_history.insert(0, message_data)
    logger.info(f"Inbound SMS from {message_data['from']}: {message_data['body']}")

    return {"success": True}


# ============================================
# Configuration Routes
# ============================================

@router.get("/config")
async def get_config():
    """Get Twilio configuration status"""
    return {
        "isConfigured": bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN),
        "phoneNumber": TWILIO_PHONE_NUMBER if TWILIO_PHONE_NUMBER else None,
        "accountStatus": "active" if TWILIO_ACCOUNT_SID else None,
    }


@router.get("/test")
async def test_connection():
    """Test Twilio connection"""
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        return {"success": False, "message": "Twilio credentials not configured"}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}.json",
                headers={"Authorization": get_twilio_auth()},
                timeout=10.0,
            )

            if response.is_success:
                return {"success": True, "message": "Connection successful"}
            else:
                return {"success": False, "message": f"API error: {response.status_code}"}

    except Exception as e:
        return {"success": False, "message": str(e)}
