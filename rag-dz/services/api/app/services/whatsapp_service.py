"""
WhatsApp Service via Twilio
Business logic for WhatsApp messaging
"""
import os
import logging
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class WhatsAppMessage(BaseModel):
    """WhatsApp message model"""
    id: Optional[str] = None
    to: str
    body: str
    media_url: Optional[str] = None
    template_name: Optional[str] = None
    template_params: Optional[List[str]] = None
    status: str = "pending"
    created_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None


class WhatsAppConfig(BaseModel):
    """WhatsApp configuration"""
    is_configured: bool = False
    whatsapp_number: Optional[str] = None
    is_sandbox: bool = True
    templates_available: List[str] = []


class WhatsAppStats(BaseModel):
    """WhatsApp statistics"""
    messages_sent_today: int = 0
    messages_received_today: int = 0
    messages_sent_week: int = 0
    messages_received_week: int = 0
    delivery_rate: float = 0.0
    read_rate: float = 0.0
    response_rate: float = 0.0
    average_response_time: str = "N/A"


class WhatsAppService:
    """
    WhatsApp messaging service using Twilio

    Supports:
    - Sending text messages
    - Sending media (images, documents)
    - Template messages (for business-initiated conversations)
    - Bulk messaging
    - Webhook handling for incoming messages
    """

    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        # WhatsApp number format: whatsapp:+14155238886 (Twilio sandbox)
        self.whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")
        self.client = None
        self._init_client()

        # Message tracking
        self.sent_messages: List[dict] = []
        self.received_messages: List[dict] = []

    def _init_client(self):
        """Initialize Twilio client"""
        if self.account_sid and self.auth_token:
            try:
                from twilio.rest import Client
                self.client = Client(self.account_sid, self.auth_token)
                logger.info("Twilio WhatsApp client initialized")
            except ImportError:
                logger.warning("Twilio library not installed. Run: pip install twilio")
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {e}")

    def get_config(self) -> WhatsAppConfig:
        """Get current WhatsApp configuration status"""
        is_configured = bool(self.client and self.account_sid and self.auth_token)
        is_sandbox = "14155238886" in self.whatsapp_number  # Twilio sandbox number

        return WhatsAppConfig(
            is_configured=is_configured,
            whatsapp_number=self.whatsapp_number.replace("whatsapp:", "") if self.whatsapp_number else None,
            is_sandbox=is_sandbox,
            templates_available=[
                "appointment_reminder",
                "appointment_confirmation",
                "results_ready",
                "welcome_message"
            ] if is_configured else []
        )

    def _format_whatsapp_number(self, phone: str) -> str:
        """
        Format phone number for WhatsApp

        Args:
            phone: Phone number (with or without whatsapp: prefix)

        Returns:
            Formatted number: whatsapp:+1234567890
        """
        # Remove any existing prefix
        phone = phone.replace("whatsapp:", "").strip()

        # Ensure + prefix for international format
        if not phone.startswith("+"):
            # Assume Algeria (+213) if no country code
            if phone.startswith("0"):
                phone = "+213" + phone[1:]
            else:
                phone = "+" + phone

        return f"whatsapp:{phone}"

    async def send_message(
        self,
        to: str,
        body: str,
        media_url: Optional[str] = None
    ) -> WhatsAppMessage:
        """
        Send a WhatsApp message

        Args:
            to: Recipient phone number
            body: Message text
            media_url: Optional media URL (image, PDF, etc.)

        Returns:
            WhatsAppMessage with status
        """
        if not self.client:
            raise Exception("Twilio client not configured. Check TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN")

        to_formatted = self._format_whatsapp_number(to)

        try:
            message_params = {
                "from_": self.whatsapp_number,
                "to": to_formatted,
                "body": body
            }

            if media_url:
                message_params["media_url"] = [media_url]

            message = self.client.messages.create(**message_params)

            result = WhatsAppMessage(
                id=message.sid,
                to=to,
                body=body,
                media_url=media_url,
                status=message.status,
                created_at=datetime.now(),
                sent_at=datetime.now()
            )

            self.sent_messages.append(result.dict())
            logger.info(f"WhatsApp message sent to {to}: {message.sid}")

            return result

        except Exception as e:
            logger.error(f"Failed to send WhatsApp message to {to}: {e}")
            raise Exception(f"Failed to send WhatsApp message: {str(e)}")

    async def send_template_message(
        self,
        to: str,
        template_name: str,
        template_params: Optional[List[str]] = None
    ) -> WhatsAppMessage:
        """
        Send a WhatsApp template message

        Template messages are pre-approved messages required for:
        - Initiating conversations (24h window expired)
        - Business notifications

        Args:
            to: Recipient phone number
            template_name: Name of approved template
            template_params: List of parameters to fill template

        Returns:
            WhatsAppMessage with status
        """
        if not self.client:
            raise Exception("Twilio client not configured")

        # Template body mapping (in production, fetch from Twilio/Meta)
        templates = {
            "appointment_reminder": "Bonjour {0}, rappel de votre RDV le {1} à {2}. Répondez OUI pour confirmer.",
            "appointment_confirmation": "Votre RDV du {0} à {1} est confirmé. Cabinet Dr {2}.",
            "results_ready": "Bonjour {0}, vos résultats d'analyse sont disponibles. Contactez-nous au {1}.",
            "welcome_message": "Bienvenue {0}! Vous êtes maintenant connecté à notre service WhatsApp."
        }

        template_body = templates.get(template_name)
        if not template_body:
            raise Exception(f"Unknown template: {template_name}")

        # Fill template with parameters
        if template_params:
            try:
                body = template_body.format(*template_params)
            except (IndexError, KeyError) as e:
                raise Exception(f"Invalid template parameters: {e}")
        else:
            body = template_body

        # Send as regular message (Twilio handles template validation)
        result = await self.send_message(to=to, body=body)
        result.template_name = template_name
        result.template_params = template_params

        return result

    async def send_bulk_messages(
        self,
        recipients: List[str],
        body: str,
        media_url: Optional[str] = None,
        task_id: Optional[str] = None
    ) -> dict:
        """
        Send WhatsApp messages to multiple recipients

        Args:
            recipients: List of phone numbers
            body: Message text
            media_url: Optional media URL
            task_id: Optional task ID for tracking

        Returns:
            Summary of sent/failed messages
        """
        results = {
            "task_id": task_id,
            "total": len(recipients),
            "sent": 0,
            "failed": 0,
            "errors": []
        }

        for recipient in recipients:
            try:
                await self.send_message(to=recipient, body=body, media_url=media_url)
                results["sent"] += 1
            except Exception as e:
                results["failed"] += 1
                results["errors"].append({
                    "recipient": recipient,
                    "error": str(e)
                })

        logger.info(f"Bulk WhatsApp: {results['sent']}/{results['total']} sent")
        return results

    async def get_stats(self) -> WhatsAppStats:
        """Get WhatsApp usage statistics"""
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=7)

        # Count messages
        sent_today = len([m for m in self.sent_messages
                        if m.get("created_at") and m["created_at"] >= today_start])
        sent_week = len([m for m in self.sent_messages
                        if m.get("created_at") and m["created_at"] >= week_start])

        received_today = len([m for m in self.received_messages
                             if m.get("received_at") and datetime.fromisoformat(m["received_at"]) >= today_start])
        received_week = len([m for m in self.received_messages
                            if m.get("received_at") and datetime.fromisoformat(m["received_at"]) >= week_start])

        # Calculate rates (mock data for now)
        total_sent = len(self.sent_messages)
        delivery_rate = 0.95 if total_sent > 0 else 0.0
        read_rate = 0.82 if total_sent > 0 else 0.0
        response_rate = (received_today / sent_today * 100) if sent_today > 0 else 0.0

        return WhatsAppStats(
            messages_sent_today=sent_today,
            messages_received_today=received_today,
            messages_sent_week=sent_week,
            messages_received_week=received_week,
            delivery_rate=delivery_rate,
            read_rate=read_rate,
            response_rate=min(response_rate, 100.0),
            average_response_time="5m 30s"  # Would calculate from actual data
        )

    def process_incoming_message(self, payload: dict) -> dict:
        """
        Process incoming WhatsApp message from webhook

        Args:
            payload: Twilio webhook payload

        Returns:
            Processed message data
        """
        message = {
            "id": payload.get("MessageSid"),
            "from": payload.get("From", "").replace("whatsapp:", ""),
            "to": payload.get("To", "").replace("whatsapp:", ""),
            "body": payload.get("Body", ""),
            "profile_name": payload.get("ProfileName", "Unknown"),
            "wa_id": payload.get("WaId", ""),
            "received_at": datetime.now().isoformat(),
            "direction": "inbound"
        }

        # Check for media
        num_media = int(payload.get("NumMedia", "0"))
        if num_media > 0:
            message["media_urls"] = [
                payload.get(f"MediaUrl{i}")
                for i in range(num_media)
                if payload.get(f"MediaUrl{i}")
            ]

        self.received_messages.append(message)
        return message


# Singleton instance
whatsapp_service = WhatsAppService()
