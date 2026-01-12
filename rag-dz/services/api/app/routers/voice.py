"""
Voice API Router - Intégration Vapi.ai
Agent vocal téléphonique pour IA Factory
"""

import os
import json
import hmac
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Request, Header
from pydantic import BaseModel
import httpx
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/voice", tags=["voice"])

# ============ MODELS ============

class VoiceAgentStatus(BaseModel):
    isActive: bool
    agentId: str
    phoneNumber: str
    currentCallId: Optional[str] = None
    uptime: int  # seconds
    lastActivity: str
    health: str  # 'healthy', 'degraded', 'offline'


class CallRecord(BaseModel):
    id: str
    callId: str
    direction: str  # 'inbound', 'outbound'
    callerNumber: str
    callerName: Optional[str] = None
    status: str  # 'completed', 'missed', 'voicemail', 'transferred', 'in_progress'
    startTime: str
    endTime: Optional[str] = None
    duration: int  # seconds
    transcription: Optional[str] = None
    summary: Optional[str] = None
    sentiment: Optional[str] = None  # 'positive', 'neutral', 'negative'
    appointmentCreated: bool = False
    appointmentId: Optional[str] = None
    recordingUrl: Optional[str] = None
    tags: List[str] = []


class VoiceConfig(BaseModel):
    agentName: str
    voice: str
    language: str
    firstMessage: str
    systemPrompt: str
    workingHours: dict
    afterHoursMessage: str
    maxCallDuration: int
    transferNumber: Optional[str] = None
    voicemailEnabled: bool
    recordingEnabled: bool


class CallStats(BaseModel):
    totalCalls: int
    inboundCalls: int
    outboundCalls: int
    missedCalls: int
    avgDuration: int
    appointmentsBooked: int
    transferredCalls: int
    todayCalls: int
    weekCalls: int


class OutboundCallRequest(BaseModel):
    phoneNumber: str
    patientName: Optional[str] = None
    reason: Optional[str] = None
    appointmentId: Optional[str] = None


class ToggleAgentRequest(BaseModel):
    active: bool


class TransferCallRequest(BaseModel):
    targetNumber: Optional[str] = None


# ============ MOCK DATA ============
# Agent state (in production, use Redis or DB)
_agent_state = {
    "isActive": True,
    "agentId": "vapi-agent-ia-factory",
    "phoneNumber": "+33 1 23 45 67 89",
    "currentCallId": None,
    "startTime": datetime.now().isoformat(),
    "lastActivity": datetime.now().isoformat(),
}

# Mock call history
_mock_calls: List[dict] = [
    {
        "id": "call-001",
        "callId": "vapi-call-abc123",
        "direction": "inbound",
        "callerNumber": "+33 6 12 34 56 78",
        "callerName": "Marie Dupont",
        "status": "completed",
        "startTime": (datetime.now() - timedelta(hours=1)).isoformat(),
        "endTime": (datetime.now() - timedelta(hours=1) + timedelta(minutes=5)).isoformat(),
        "duration": 312,
        "transcription": "Bonjour, je souhaite prendre rendez-vous pour une consultation sur l'intégration d'IA dans mon entreprise...",
        "summary": "Demande de RDV pour consultation IA - Entreprise de logistique",
        "sentiment": "positive",
        "appointmentCreated": True,
        "appointmentId": "apt-001",
        "recordingUrl": "https://storage.vapi.ai/recordings/abc123.mp3",
        "tags": ["rdv", "nouveau-client", "IA"],
    },
    {
        "id": "call-002",
        "callId": "vapi-call-def456",
        "direction": "inbound",
        "callerNumber": "+33 6 98 76 54 32",
        "callerName": None,
        "status": "missed",
        "startTime": (datetime.now() - timedelta(hours=3)).isoformat(),
        "endTime": None,
        "duration": 0,
        "transcription": None,
        "summary": None,
        "sentiment": None,
        "appointmentCreated": False,
        "appointmentId": None,
        "recordingUrl": None,
        "tags": ["rappeler"],
    },
    {
        "id": "call-003",
        "callId": "vapi-call-ghi789",
        "direction": "outbound",
        "callerNumber": "+33 6 11 22 33 44",
        "callerName": "Jean Martin",
        "status": "completed",
        "startTime": (datetime.now() - timedelta(hours=5)).isoformat(),
        "endTime": (datetime.now() - timedelta(hours=5) + timedelta(minutes=3)).isoformat(),
        "duration": 185,
        "transcription": "Confirmation du rendez-vous de demain à 14h...",
        "summary": "Confirmation RDV - Client satisfait",
        "sentiment": "positive",
        "appointmentCreated": False,
        "appointmentId": "apt-002",
        "recordingUrl": "https://storage.vapi.ai/recordings/ghi789.mp3",
        "tags": ["confirmation", "suivi"],
    },
    {
        "id": "call-004",
        "callId": "vapi-call-jkl012",
        "direction": "inbound",
        "callerNumber": "+33 6 55 44 33 22",
        "callerName": "Pierre Leroy",
        "status": "voicemail",
        "startTime": (datetime.now() - timedelta(days=1)).isoformat(),
        "endTime": (datetime.now() - timedelta(days=1) + timedelta(seconds=45)).isoformat(),
        "duration": 45,
        "transcription": "Bonjour, c'est Pierre Leroy. Rappelez-moi s'il vous plaît concernant mon projet...",
        "summary": "Message vocal - Demande de rappel",
        "sentiment": "neutral",
        "appointmentCreated": False,
        "appointmentId": None,
        "recordingUrl": "https://storage.vapi.ai/recordings/jkl012.mp3",
        "tags": ["rappeler", "voicemail"],
    },
    {
        "id": "call-005",
        "callId": "vapi-call-mno345",
        "direction": "inbound",
        "callerNumber": "+33 6 77 88 99 00",
        "callerName": "Sophie Bernard",
        "status": "transferred",
        "startTime": (datetime.now() - timedelta(days=1, hours=2)).isoformat(),
        "endTime": (datetime.now() - timedelta(days=1, hours=2) + timedelta(minutes=8)).isoformat(),
        "duration": 480,
        "transcription": "Je souhaite parler à un expert technique concernant une intégration complexe...",
        "summary": "Demande technique complexe - Transféré vers équipe technique",
        "sentiment": "neutral",
        "appointmentCreated": False,
        "appointmentId": None,
        "recordingUrl": "https://storage.vapi.ai/recordings/mno345.mp3",
        "tags": ["technique", "transfert"],
    },
]

# Default config
_voice_config: VoiceConfig = VoiceConfig(
    agentName="Agent IA Factory",
    voice="alloy",
    language="fr-FR",
    firstMessage="Bonjour, bienvenue chez IA Factory, votre partenaire en intelligence artificielle. Comment puis-je vous aider ?",
    systemPrompt="""Tu es l'assistant vocal de IA Factory, une agence spécialisée en intelligence artificielle et automatisation.

Tes responsabilités:
- Répondre aux questions sur les services de IA Factory
- Prendre des rendez-vous pour des consultations
- Transférer les appels complexes vers l'équipe
- Collecter les coordonnées des prospects intéressés

Ton ton est professionnel mais chaleureux. Tu parles en français.

Services de IA Factory:
- Développement d'assistants IA personnalisés
- Automatisation des processus métier
- Intégration d'IA dans les applications existantes
- Formation et accompagnement IA
- Agents vocaux intelligents (comme toi!)

Si le client souhaite un rendez-vous, propose les créneaux disponibles.
Si la demande est trop technique, propose de transférer vers un expert.""",
    workingHours={
        "enabled": True,
        "timezone": "Europe/Paris",
        "schedule": {
            "monday": {"start": "09:00", "end": "18:00"},
            "tuesday": {"start": "09:00", "end": "18:00"},
            "wednesday": {"start": "09:00", "end": "18:00"},
            "thursday": {"start": "09:00", "end": "18:00"},
            "friday": {"start": "09:00", "end": "17:00"},
            "saturday": None,
            "sunday": None,
        },
    },
    afterHoursMessage="Nos bureaux sont actuellement fermés. Laissez-nous un message et nous vous rappellerons dès que possible. Vous pouvez également prendre rendez-vous sur notre site web.",
    maxCallDuration=600,
    transferNumber="+33 1 98 76 54 32",
    voicemailEnabled=True,
    recordingEnabled=True,
)


# ============ VAPI API CLIENT ============

def get_vapi_client():
    """Get Vapi API client with authentication"""
    api_key = os.getenv("VAPI_API_KEY")
    if not api_key:
        logger.warning("VAPI_API_KEY not configured")
        return None
    return api_key


async def call_vapi_api(method: str, endpoint: str, data: dict = None):
    """Make authenticated call to Vapi API"""
    api_key = get_vapi_client()
    if not api_key:
        raise HTTPException(status_code=503, detail="Vapi API not configured")

    base_url = "https://api.vapi.ai"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        if method == "GET":
            response = await client.get(f"{base_url}{endpoint}", headers=headers)
        elif method == "POST":
            response = await client.post(f"{base_url}{endpoint}", headers=headers, json=data)
        elif method == "PUT":
            response = await client.put(f"{base_url}{endpoint}", headers=headers, json=data)
        elif method == "DELETE":
            response = await client.delete(f"{base_url}{endpoint}", headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        if response.status_code >= 400:
            logger.error(f"Vapi API error: {response.status_code} - {response.text}")
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.json() if response.content else None


# ============ ENDPOINTS ============

@router.get("/status", response_model=VoiceAgentStatus)
async def get_agent_status():
    """Get current voice agent status"""
    start_time = datetime.fromisoformat(_agent_state["startTime"])
    uptime = int((datetime.now() - start_time).total_seconds()) if _agent_state["isActive"] else 0

    return VoiceAgentStatus(
        isActive=_agent_state["isActive"],
        agentId=_agent_state["agentId"],
        phoneNumber=_agent_state["phoneNumber"],
        currentCallId=_agent_state["currentCallId"],
        uptime=uptime,
        lastActivity=_agent_state["lastActivity"],
        health="healthy" if _agent_state["isActive"] else "offline",
    )


@router.post("/toggle", response_model=VoiceAgentStatus)
async def toggle_agent(request: ToggleAgentRequest):
    """Toggle voice agent on/off"""
    global _agent_state

    _agent_state["isActive"] = request.active
    if request.active:
        _agent_state["startTime"] = datetime.now().isoformat()
    _agent_state["lastActivity"] = datetime.now().isoformat()

    logger.info(f"Voice agent toggled: {'ON' if request.active else 'OFF'}")

    return await get_agent_status()


@router.get("/calls")
async def get_call_history(
    limit: int = 20,
    offset: int = 0,
    status: Optional[str] = None,
    direction: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """Get call history with filters"""
    calls = _mock_calls.copy()

    # Apply filters
    if status:
        calls = [c for c in calls if c["status"] == status]
    if direction:
        calls = [c for c in calls if c["direction"] == direction]
    if start_date:
        start = datetime.fromisoformat(start_date)
        calls = [c for c in calls if datetime.fromisoformat(c["startTime"]) >= start]
    if end_date:
        end = datetime.fromisoformat(end_date)
        calls = [c for c in calls if datetime.fromisoformat(c["startTime"]) <= end]

    total = len(calls)
    calls = calls[offset : offset + limit]

    return {"calls": calls, "total": total}


@router.get("/calls/{call_id}", response_model=CallRecord)
async def get_call_details(call_id: str):
    """Get details of a specific call"""
    for call in _mock_calls:
        if call["id"] == call_id or call["callId"] == call_id:
            return CallRecord(**call)
    raise HTTPException(status_code=404, detail="Call not found")


@router.get("/config", response_model=VoiceConfig)
async def get_voice_config():
    """Get voice agent configuration"""
    return _voice_config


@router.put("/config", response_model=VoiceConfig)
async def update_voice_config(config: VoiceConfig):
    """Update voice agent configuration"""
    global _voice_config
    _voice_config = config
    logger.info("Voice config updated")
    return _voice_config


@router.post("/call/outbound")
async def trigger_outbound_call(request: OutboundCallRequest):
    """Trigger an outbound call"""
    global _agent_state

    # In production, this would call Vapi API
    call_id = f"vapi-call-out-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    _agent_state["currentCallId"] = call_id
    _agent_state["lastActivity"] = datetime.now().isoformat()

    logger.info(f"Outbound call triggered: {request.phoneNumber}")

    return {
        "callId": call_id,
        "status": "initiated",
        "phoneNumber": request.phoneNumber,
        "message": f"Appel sortant initié vers {request.phoneNumber}",
    }


@router.get("/stats", response_model=CallStats)
async def get_call_stats(period: Optional[str] = None):
    """Get call statistics"""
    # Calculate from mock data
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=today_start.weekday())

    total = len(_mock_calls)
    inbound = len([c for c in _mock_calls if c["direction"] == "inbound"])
    outbound = len([c for c in _mock_calls if c["direction"] == "outbound"])
    missed = len([c for c in _mock_calls if c["status"] == "missed"])
    transferred = len([c for c in _mock_calls if c["status"] == "transferred"])
    appointments = len([c for c in _mock_calls if c["appointmentCreated"]])

    durations = [c["duration"] for c in _mock_calls if c["duration"] > 0]
    avg_duration = int(sum(durations) / len(durations)) if durations else 0

    today_calls = len([
        c for c in _mock_calls
        if datetime.fromisoformat(c["startTime"]) >= today_start
    ])
    week_calls = len([
        c for c in _mock_calls
        if datetime.fromisoformat(c["startTime"]) >= week_start
    ])

    return CallStats(
        totalCalls=total,
        inboundCalls=inbound,
        outboundCalls=outbound,
        missedCalls=missed,
        avgDuration=avg_duration,
        appointmentsBooked=appointments,
        transferredCalls=transferred,
        todayCalls=today_calls,
        weekCalls=week_calls,
    )


@router.get("/voices")
async def get_available_voices():
    """Get list of available voices"""
    # These are Vapi/ElevenLabs available voices
    return [
        {"id": "alloy", "name": "Alloy", "language": "fr-FR", "gender": "female"},
        {"id": "echo", "name": "Echo", "language": "fr-FR", "gender": "male"},
        {"id": "fable", "name": "Fable", "language": "fr-FR", "gender": "female"},
        {"id": "onyx", "name": "Onyx", "language": "fr-FR", "gender": "male"},
        {"id": "nova", "name": "Nova", "language": "fr-FR", "gender": "female"},
        {"id": "shimmer", "name": "Shimmer", "language": "fr-FR", "gender": "female"},
    ]


@router.post("/calls/{call_id}/transfer")
async def transfer_call(call_id: str, request: TransferCallRequest):
    """Transfer an active call to a human agent"""
    global _agent_state

    # Find the call
    call = None
    for c in _mock_calls:
        if c["id"] == call_id or c["callId"] == call_id:
            call = c
            break

    if not call:
        raise HTTPException(status_code=404, detail="Call not found")

    target = request.targetNumber or _voice_config.transferNumber
    if not target:
        raise HTTPException(status_code=400, detail="No transfer number configured")

    # In production, this would call Vapi API to transfer
    call["status"] = "transferred"
    _agent_state["currentCallId"] = None
    _agent_state["lastActivity"] = datetime.now().isoformat()

    logger.info(f"Call {call_id} transferred to {target}")

    return {"success": True, "transferredTo": target}


# ============ WEBHOOK ENDPOINT ============

def verify_vapi_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify Vapi webhook signature"""
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)


@router.post("/webhook")
async def vapi_webhook(
    request: Request,
    x_vapi_signature: Optional[str] = Header(None),
):
    """
    Webhook endpoint for Vapi.ai events

    Events:
    - call.started: When a call begins
    - call.ended: When a call ends
    - call.analyzed: When call analysis is complete
    - assistant.message: When the assistant sends a message
    - user.message: When the user speaks
    - function.call: When a function needs to be executed
    """
    global _agent_state, _mock_calls

    body = await request.body()

    # Verify signature in production
    webhook_secret = os.getenv("VAPI_WEBHOOK_SECRET")
    if webhook_secret and x_vapi_signature:
        if not verify_vapi_signature(body, x_vapi_signature, webhook_secret):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    event_type = data.get("type", data.get("event"))
    logger.info(f"Vapi webhook received: {event_type}")

    # Handle different event types
    if event_type == "call.started" or event_type == "call-started":
        call_data = data.get("call", data)
        _agent_state["currentCallId"] = call_data.get("id")
        _agent_state["lastActivity"] = datetime.now().isoformat()

        # Create new call record
        new_call = {
            "id": f"call-{len(_mock_calls) + 1:03d}",
            "callId": call_data.get("id"),
            "direction": call_data.get("direction", "inbound"),
            "callerNumber": call_data.get("customer", {}).get("number", "Unknown"),
            "callerName": call_data.get("customer", {}).get("name"),
            "status": "in_progress",
            "startTime": datetime.now().isoformat(),
            "endTime": None,
            "duration": 0,
            "transcription": None,
            "summary": None,
            "sentiment": None,
            "appointmentCreated": False,
            "appointmentId": None,
            "recordingUrl": None,
            "tags": [],
        }
        _mock_calls.insert(0, new_call)

        return {"message": "Call started recorded"}

    elif event_type == "call.ended" or event_type == "call-ended":
        call_data = data.get("call", data)
        call_id = call_data.get("id")

        _agent_state["currentCallId"] = None
        _agent_state["lastActivity"] = datetime.now().isoformat()

        # Update call record
        for call in _mock_calls:
            if call["callId"] == call_id:
                call["status"] = call_data.get("status", "completed")
                call["endTime"] = datetime.now().isoformat()
                start = datetime.fromisoformat(call["startTime"])
                call["duration"] = int((datetime.now() - start).total_seconds())
                call["recordingUrl"] = call_data.get("recordingUrl")
                break

        return {"message": "Call ended recorded"}

    elif event_type == "call.analyzed" or event_type == "analysis":
        analysis = data.get("analysis", data)
        call_id = data.get("call", {}).get("id") or data.get("callId")

        # Update call with analysis
        for call in _mock_calls:
            if call["callId"] == call_id:
                call["transcription"] = analysis.get("transcript")
                call["summary"] = analysis.get("summary")
                call["sentiment"] = analysis.get("sentiment")
                break

        return {"message": "Analysis recorded"}

    elif event_type == "function.call" or event_type == "function-call":
        # Handle function calls from the voice agent
        function_name = data.get("functionCall", {}).get("name")
        function_args = data.get("functionCall", {}).get("parameters", {})

        logger.info(f"Function call: {function_name} with args: {function_args}")

        # Handle booking appointment
        if function_name == "book_appointment":
            # In production, integrate with calendar API
            return {
                "result": {
                    "success": True,
                    "message": "Rendez-vous confirmé pour le créneau demandé",
                    "appointmentId": f"apt-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                }
            }

        # Handle transfer request
        elif function_name == "transfer_to_human":
            return {
                "result": {
                    "success": True,
                    "message": "Transfert en cours vers un conseiller",
                }
            }

        return {"result": {"message": "Function not implemented"}}

    # Default response
    return {"message": f"Event {event_type} received"}


# ============ VAPI ASSISTANT CONFIG EXPORT ============

@router.get("/vapi-config")
async def get_vapi_assistant_config():
    """
    Export the voice agent configuration in Vapi format
    Use this to configure your Vapi assistant
    """
    return {
        "name": _voice_config.agentName,
        "model": {
            "provider": "openai",
            "model": "gpt-4-turbo-preview",
            "systemPrompt": _voice_config.systemPrompt,
            "temperature": 0.7,
        },
        "voice": {
            "provider": "openai",
            "voiceId": _voice_config.voice,
        },
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-2",
            "language": _voice_config.language,
        },
        "firstMessage": _voice_config.firstMessage,
        "endCallMessage": "Merci de votre appel. À bientôt chez IA Factory !",
        "serverUrl": os.getenv("VAPI_WEBHOOK_URL", "https://your-domain.com/api/voice/webhook"),
        "functions": [
            {
                "name": "book_appointment",
                "description": "Réserver un rendez-vous pour le client",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string", "description": "Date souhaitée (format: YYYY-MM-DD)"},
                        "time": {"type": "string", "description": "Heure souhaitée (format: HH:MM)"},
                        "name": {"type": "string", "description": "Nom du client"},
                        "phone": {"type": "string", "description": "Numéro de téléphone"},
                        "email": {"type": "string", "description": "Email du client"},
                        "topic": {"type": "string", "description": "Sujet du rendez-vous"},
                    },
                    "required": ["date", "time", "name"],
                },
            },
            {
                "name": "transfer_to_human",
                "description": "Transférer l'appel vers un conseiller humain",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reason": {"type": "string", "description": "Raison du transfert"},
                    },
                },
            },
        ],
        "maxDurationSeconds": _voice_config.maxCallDuration,
        "silenceTimeoutSeconds": 30,
        "recordingEnabled": _voice_config.recordingEnabled,
    }
