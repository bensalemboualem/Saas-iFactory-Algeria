"""
Google OAuth2 and API Routes
Handles Calendar and Gmail integration
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os
from datetime import datetime

router = APIRouter(prefix="/api/google", tags=["google"])

# Environment variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3737/auth/google/callback")


# ============================================
# Pydantic Models
# ============================================

class TokenExchangeRequest(BaseModel):
    code: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: int
    email: Optional[str] = None
    picture: Optional[str] = None


class CalendarEventsRequest(BaseModel):
    timeMin: str
    timeMax: str


class CalendarEvent(BaseModel):
    id: str
    summary: str
    description: Optional[str] = None
    start: dict
    end: dict
    attendees: Optional[List[dict]] = None
    location: Optional[str] = None
    status: str = "confirmed"
    htmlLink: Optional[str] = None


class CreateEventRequest(BaseModel):
    summary: str
    description: Optional[str] = None
    start: str
    end: str
    attendees: Optional[List[str]] = None
    location: Optional[str] = None
    sendUpdates: str = "none"


class SendEmailRequest(BaseModel):
    to: List[str]
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None
    subject: str
    body: str
    isHtml: bool = False
    replyToMessageId: Optional[str] = None


# ============================================
# Helper Functions
# ============================================

def get_authorization_token(authorization: str = Header(None)) -> str:
    """Extract Bearer token from Authorization header"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    return authorization.split(" ")[1]


async def google_api_request(
    method: str,
    url: str,
    access_token: str,
    data: dict = None,
    params: dict = None
) -> dict:
    """Make authenticated request to Google API"""
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            json=data,
            params=params,
            timeout=30.0
        )

        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Google token expired or invalid")

        if not response.is_success:
            raise HTTPException(status_code=response.status_code, detail=f"Google API error: {response.text}")

        return response.json() if response.text else {}


# ============================================
# OAuth Routes
# ============================================

@router.post("/auth/callback", response_model=TokenResponse)
async def exchange_code_for_tokens(request: TokenExchangeRequest):
    """Exchange authorization code for access and refresh tokens"""
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "code": request.code,
                "grant_type": "authorization_code",
                "redirect_uri": GOOGLE_REDIRECT_URI,
            },
            timeout=30.0
        )

        if not token_response.is_success:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to exchange code: {token_response.text}"
            )

        tokens = token_response.json()

        # Get user info
        user_info = None
        try:
            user_response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {tokens['access_token']}"},
                timeout=10.0
            )
            if user_response.is_success:
                user_info = user_response.json()
        except Exception:
            pass

        return TokenResponse(
            access_token=tokens["access_token"],
            refresh_token=tokens.get("refresh_token"),
            expires_in=tokens.get("expires_in", 3600),
            email=user_info.get("email") if user_info else None,
            picture=user_info.get("picture") if user_info else None,
        )


# ============================================
# Calendar Routes
# ============================================

@router.post("/calendar/events", response_model=dict)
async def get_calendar_events(
    request: CalendarEventsRequest,
    access_token: str = Depends(get_authorization_token)
):
    """Get calendar events for a date range"""
    params = {
        "timeMin": request.timeMin,
        "timeMax": request.timeMax,
        "singleEvents": "true",
        "orderBy": "startTime",
        "maxResults": 50,
    }

    result = await google_api_request(
        method="GET",
        url="https://www.googleapis.com/calendar/v3/calendars/primary/events",
        access_token=access_token,
        params=params
    )

    events = [
        CalendarEvent(
            id=e.get("id", ""),
            summary=e.get("summary", "Sans titre"),
            description=e.get("description"),
            start=e.get("start", {}),
            end=e.get("end", {}),
            attendees=e.get("attendees"),
            location=e.get("location"),
            status=e.get("status", "confirmed"),
            htmlLink=e.get("htmlLink"),
        )
        for e in result.get("items", [])
    ]

    return {"events": [e.dict() for e in events]}


@router.put("/calendar/events", response_model=dict)
async def create_calendar_event(
    request: CreateEventRequest,
    access_token: str = Depends(get_authorization_token)
):
    """Create a new calendar event"""
    event_data = {
        "summary": request.summary,
        "start": {"dateTime": request.start, "timeZone": "Europe/Paris"},
        "end": {"dateTime": request.end, "timeZone": "Europe/Paris"},
    }

    if request.description:
        event_data["description"] = request.description
    if request.location:
        event_data["location"] = request.location
    if request.attendees:
        event_data["attendees"] = [{"email": email} for email in request.attendees]

    result = await google_api_request(
        method="POST",
        url="https://www.googleapis.com/calendar/v3/calendars/primary/events",
        access_token=access_token,
        data=event_data,
        params={"sendUpdates": request.sendUpdates}
    )

    return result


# ============================================
# Gmail Routes
# ============================================

@router.get("/gmail/messages", response_model=dict)
async def get_emails(
    q: str = "",
    maxResults: int = 20,
    access_token: str = Depends(get_authorization_token)
):
    """Get emails with optional query filter"""
    params = {
        "maxResults": maxResults,
    }
    if q:
        params["q"] = q

    # Get message list
    result = await google_api_request(
        method="GET",
        url="https://www.googleapis.com/gmail/v1/users/me/messages",
        access_token=access_token,
        params=params
    )

    emails = []
    for msg in result.get("messages", [])[:maxResults]:
        # Get full message details
        msg_detail = await google_api_request(
            method="GET",
            url=f"https://www.googleapis.com/gmail/v1/users/me/messages/{msg['id']}",
            access_token=access_token,
            params={"format": "metadata", "metadataHeaders": ["From", "To", "Subject", "Date"]}
        )

        headers = {h["name"]: h["value"] for h in msg_detail.get("payload", {}).get("headers", [])}

        emails.append({
            "id": msg_detail.get("id"),
            "threadId": msg_detail.get("threadId"),
            "snippet": msg_detail.get("snippet", ""),
            "subject": headers.get("Subject", "(Sans sujet)"),
            "from": parse_email_address(headers.get("From", "")),
            "to": [parse_email_address(headers.get("To", ""))],
            "date": headers.get("Date", ""),
            "isRead": "UNREAD" not in msg_detail.get("labelIds", []),
            "isStarred": "STARRED" in msg_detail.get("labelIds", []),
            "labels": msg_detail.get("labelIds", []),
            "hasAttachments": has_attachments(msg_detail),
        })

    return {"emails": emails}


@router.get("/gmail/threads/{thread_id}", response_model=dict)
async def get_email_thread(
    thread_id: str,
    access_token: str = Depends(get_authorization_token)
):
    """Get full email thread"""
    result = await google_api_request(
        method="GET",
        url=f"https://www.googleapis.com/gmail/v1/users/me/threads/{thread_id}",
        access_token=access_token,
        params={"format": "full"}
    )

    messages = []
    for msg in result.get("messages", []):
        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        body = extract_email_body(msg.get("payload", {}))

        messages.append({
            "id": msg.get("id"),
            "from": parse_email_address(headers.get("From", "")),
            "to": [parse_email_address(headers.get("To", ""))],
            "cc": [parse_email_address(cc) for cc in headers.get("Cc", "").split(",")] if headers.get("Cc") else [],
            "date": headers.get("Date", ""),
            "body": body,
        })

    return {
        "id": thread_id,
        "messages": messages,
        "subject": messages[0].get("subject", "") if messages else ""
    }


@router.post("/gmail/send", response_model=dict)
async def send_email(
    request: SendEmailRequest,
    access_token: str = Depends(get_authorization_token)
):
    """Send an email"""
    import base64
    from email.mime.text import MIMEText

    message = MIMEText(request.body, "html" if request.isHtml else "plain")
    message["to"] = ", ".join(request.to)
    message["subject"] = request.subject

    if request.cc:
        message["cc"] = ", ".join(request.cc)
    if request.bcc:
        message["bcc"] = ", ".join(request.bcc)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    body = {"raw": raw_message}
    if request.replyToMessageId:
        body["threadId"] = request.replyToMessageId

    result = await google_api_request(
        method="POST",
        url="https://www.googleapis.com/gmail/v1/users/me/messages/send",
        access_token=access_token,
        data=body
    )

    return {"id": result.get("id"), "threadId": result.get("threadId")}


@router.post("/gmail/messages/{message_id}/read")
async def mark_as_read(
    message_id: str,
    access_token: str = Depends(get_authorization_token)
):
    """Mark email as read"""
    await google_api_request(
        method="POST",
        url=f"https://www.googleapis.com/gmail/v1/users/me/messages/{message_id}/modify",
        access_token=access_token,
        data={"removeLabelIds": ["UNREAD"]}
    )
    return {"success": True}


@router.get("/gmail/unread-count", response_model=dict)
async def get_unread_count(access_token: str = Depends(get_authorization_token)):
    """Get count of unread emails"""
    result = await google_api_request(
        method="GET",
        url="https://www.googleapis.com/gmail/v1/users/me/messages",
        access_token=access_token,
        params={"q": "is:unread", "maxResults": 1}
    )

    return {"count": result.get("resultSizeEstimate", 0)}


# ============================================
# Helper Functions
# ============================================

def parse_email_address(raw: str) -> dict:
    """Parse email address from 'Name <email>' format"""
    import re
    match = re.match(r'^(.*?)\s*<(.+?)>$', raw.strip())
    if match:
        return {"name": match.group(1).strip('" '), "email": match.group(2)}
    return {"email": raw.strip(), "name": None}


def has_attachments(message: dict) -> bool:
    """Check if message has attachments"""
    payload = message.get("payload", {})
    parts = payload.get("parts", [])
    return any(part.get("filename") for part in parts)


def extract_email_body(payload: dict) -> str:
    """Extract email body from payload"""
    import base64

    if payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")

    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
            return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
        if part.get("mimeType") == "text/html" and part.get("body", {}).get("data"):
            return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")

    return ""
