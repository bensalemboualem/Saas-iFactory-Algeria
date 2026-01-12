"""
Workspace Connector - Email & Calendar Intelligence
===================================================

Intégration Gmail + Google Calendar:
- Scan emails récents
- Résumés intelligents LLM
- Détection actions requises
- Extraction deadlines

Mock Mode: Development without Gmail API
Production: Requires Google OAuth + Gmail API enabled

Created: 2025-01-16
"""

import logging
import os
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class EmailSummary:
    """Résumé email généré par LLM"""
    email_id: str
    sender_email: str
    sender_name: str
    subject: str
    received_at: datetime

    # IA Analysis
    summary_text: str  # 2-3 sentences
    key_points: List[str]
    action_items: List[str]
    deadline_detected: Optional[datetime] = None

    # Classification
    priority_level: str = 'normal'  # 'urgent', 'high', 'normal', 'low'
    category: str = 'work'  # 'work', 'personal', 'newsletter'
    requires_action: bool = False

    sentiment: str = 'neutral'  # 'positive', 'negative', 'urgent', 'neutral'
    language_detected: str = 'fr'

    # Metadata
    contains_attachments: bool = False
    attachment_types: List[str] = None


def get_gmail_api_credentials() -> Optional[str]:
    """Récupère Gmail API credentials depuis env"""
    return os.getenv('GOOGLE_GMAIL_CREDENTIALS')


async def fetch_recent_emails_gmail(
    user_email: str,
    max_results: int = 20,
    unread_only: bool = False
) -> List[Dict[str, Any]]:
    """
    Récupère les emails récents via Gmail API

    Args:
        user_email: Email de l'utilisateur
        max_results: Nombre max d'emails à récupérer
        unread_only: Seulement les non-lus

    Returns:
        Liste d'emails bruts
    """
    credentials = get_gmail_api_credentials()

    if not credentials:
        logger.warning("Gmail API credentials not configured - using MOCK data")
        return _mock_emails_geneva()

    try:
        # TODO: Implémenter Gmail API v1
        # from googleapiclient.discovery import build
        # service = build('gmail', 'v1', credentials=credentials)
        #
        # query = 'is:unread' if unread_only else ''
        # results = service.users().messages().list(
        #     userId='me',
        #     maxResults=max_results,
        #     q=query
        # ).execute()
        #
        # messages = results.get('messages', [])
        # ...

        logger.warning("Gmail API integration not yet implemented - using MOCK")
        return _mock_emails_geneva()

    except Exception as e:
        logger.error(f"Error fetching Gmail emails: {e}")
        return _mock_emails_geneva()


def _mock_emails_geneva() -> List[Dict[str, Any]]:
    """
    Mock emails for development
    Realistic Geneva professional emails
    """
    now = datetime.now()

    return [
        {
            'id': 'msg_001',
            'sender_email': 'weber@avocat-geneve.ch',
            'sender_name': 'Me Christian Weber',
            'subject': 'URGENT: Signature contrat Novartis avant 17h',
            'received_at': now - timedelta(hours=2),
            'body_snippet': 'Bonjour, Le contrat de licence exclusive attend votre signature...',
            'has_attachments': True,
            'attachment_types': ['pdf'],
            'is_unread': True,
        },
        {
            'id': 'msg_002',
            'sender_email': 'ompi@wipo.int',
            'sender_name': 'OMPI - Greffe',
            'subject': 'Opposition brevet EP3456789 - Audience 28 janvier',
            'received_at': now - timedelta(hours=5),
            'body_snippet': 'Madame, Nous confirmons la date d\'audience pour votre client...',
            'has_attachments': False,
            'is_unread': True,
        },
        {
            'id': 'msg_003',
            'sender_email': 'formation@barreau-geneve.ch',
            'sender_name': 'Barreau de Genève',
            'subject': 'Webinar: IA et Propriété Intellectuelle - 25 janvier',
            'received_at': now - timedelta(hours=8),
            'body_snippet': 'Formation continue obligatoire: Impact de l\'IA sur les brevets...',
            'has_attachments': False,
            'is_unread': False,
        },
        {
            'id': 'msg_004',
            'sender_email': 'client@biogeneve.ch',
            'sender_name': 'Klaus Müller',
            'subject': 'Suivi dossier brevet vaccin',
            'received_at': now - timedelta(hours=12),
            'body_snippet': 'Bonjour Maître, Avez-vous des nouvelles de l\'EPO concernant...',
            'has_attachments': False,
            'is_unread': True,
        },
        {
            'id': 'msg_005',
            'sender_email': 'newsletter@swissinfo.ch',
            'sender_name': 'SwissInfo',
            'subject': 'Actualités Genève - 16 janvier',
            'received_at': now - timedelta(hours=14),
            'body_snippet': 'Nouvelle politique parking Eaux-Vives: +20% tarifs...',
            'has_attachments': False,
            'is_unread': False,
        },
    ]


async def summarize_email_with_llm(
    email_data: Dict[str, Any],
    llm_model: str = "groq/llama-3.3-70b-versatile"
) -> EmailSummary:
    """
    Résume un email avec un LLM

    Args:
        email_data: Données email brutes
        llm_model: Modèle LLM à utiliser

    Returns:
        EmailSummary avec analyse IA
    """
    # Extract email content
    subject = email_data.get('subject', '')
    body = email_data.get('body_snippet', '')
    sender = email_data.get('sender_name', email_data.get('sender_email', ''))

    # Build LLM prompt
    prompt = f"""
    Analyse cet email professionnel et génère un résumé structuré.

    Expéditeur: {sender}
    Sujet: {subject}
    Contenu: {body}

    Fournis l'analyse en JSON:
    {{
        "summary": "Résumé en 1-2 phrases",
        "key_points": ["Point 1", "Point 2"],
        "action_items": ["Action 1", "Action 2"],
        "deadline": "YYYY-MM-DD ou null",
        "priority": "urgent|high|normal|low",
        "sentiment": "positive|negative|neutral|urgent",
        "requires_action": true|false
    }}
    """

    try:
        # TODO: Call LLM Proxy
        # from ..tokens.llm_proxy import proxy_groq_call
        # response = await proxy_groq_call(
        #     tenant_id=tenant_id,
        #     prompt=prompt,
        #     model="llama-3.3-70b-versatile"
        # )
        # analysis = json.loads(response)

        # Mock analysis for now
        analysis = _mock_email_analysis(email_data)

        # Create EmailSummary
        summary = EmailSummary(
            email_id=email_data['id'],
            sender_email=email_data['sender_email'],
            sender_name=email_data.get('sender_name', ''),
            subject=subject,
            received_at=email_data['received_at'],
            summary_text=analysis['summary'],
            key_points=analysis.get('key_points', []),
            action_items=analysis.get('action_items', []),
            deadline_detected=analysis.get('deadline'),
            priority_level=analysis.get('priority', 'normal'),
            sentiment=analysis.get('sentiment', 'neutral'),
            requires_action=analysis.get('requires_action', False),
            contains_attachments=email_data.get('has_attachments', False),
            attachment_types=email_data.get('attachment_types'),
        )

        logger.info(f"📧 Email summarized: {subject[:50]}... (priority={summary.priority_level})")

        return summary

    except Exception as e:
        logger.error(f"Error summarizing email: {e}")
        # Fallback simple summary
        return EmailSummary(
            email_id=email_data['id'],
            sender_email=email_data['sender_email'],
            sender_name=email_data.get('sender_name', ''),
            subject=subject,
            received_at=email_data['received_at'],
            summary_text=f"Email de {sender} concernant: {subject}",
            key_points=[],
            action_items=[],
        )


def _mock_email_analysis(email_data: Dict[str, Any]) -> Dict[str, Any]:
    """Mock LLM analysis for development"""
    subject = email_data.get('subject', '').lower()

    # Detect urgency
    is_urgent = 'urgent' in subject or 'asap' in subject or 'immédiat' in subject
    has_deadline = any(word in subject for word in ['avant', 'deadline', 'date limite'])

    # Detect action needed
    action_keywords = ['signature', 'confirmer', 'répondre', 'envoyer', 'approval']
    requires_action = any(word in subject for word in action_keywords)

    priority = 'urgent' if is_urgent else 'high' if has_deadline else 'normal'

    # Mock deadline detection
    deadline = None
    if 'avant 17h' in subject or '17h' in subject:
        deadline = datetime.now().replace(hour=17, minute=0)
    elif '28 janvier' in subject:
        deadline = datetime(2025, 1, 28, 9, 0)

    return {
        'summary': f"{email_data.get('body_snippet', '')[:150]}...",
        'key_points': ['Point clé 1', 'Point clé 2'] if requires_action else [],
        'action_items': ['Signer le contrat'] if 'signature' in subject else [],
        'deadline': deadline,
        'priority': priority,
        'sentiment': 'urgent' if is_urgent else 'neutral',
        'requires_action': requires_action,
    }


async def get_top_priority_emails(
    user_email: str,
    limit: int = 3
) -> List[EmailSummary]:
    """
    Récupère le TOP N emails prioritaires

    Args:
        user_email: Email utilisateur
        limit: Nombre d'emails à retourner

    Returns:
        Liste d'EmailSummary triés par priorité
    """
    # Fetch recent emails
    emails_raw = await fetch_recent_emails_gmail(user_email, max_results=20, unread_only=True)

    # Summarize with LLM
    summaries = []
    for email_data in emails_raw[:10]:  # Limit LLM calls
        summary = await summarize_email_with_llm(email_data)
        summaries.append(summary)

    # Sort by priority
    priority_order = {'urgent': 0, 'high': 1, 'normal': 2, 'low': 3}

    summaries.sort(key=lambda s: (
        priority_order.get(s.priority_level, 2),
        s.received_at
    ), reverse=True)

    return summaries[:limit]


def format_email_summary_for_briefing(
    email_summary: EmailSummary,
    index: int
) -> str:
    """
    Formate un email pour briefing vocal matinal

    Args:
        email_summary: Résumé email
        index: Numéro dans la liste (1, 2, 3)

    Returns:
        Texte formaté pour TTS
    """
    priority_emoji = {
        'urgent': '⚠️ URGENT',
        'high': '📄',
        'normal': '📧',
        'low': '📬',
    }

    emoji = priority_emoji.get(email_summary.priority_level, '📧')

    message = f"{index}. {emoji} {email_summary.sender_name}\n"
    message += f"   Sujet: \"{email_summary.subject}\"\n"
    message += f"   Résumé IA: {email_summary.summary_text}\n"

    if email_summary.action_items:
        action = email_summary.action_items[0]
        message += f"   💡 Action suggérée: {action}\n"

    if email_summary.deadline_detected:
        deadline_str = email_summary.deadline_detected.strftime('%d/%m à %Hh%M')
        message += f"   ⏰ Deadline: {deadline_str}\n"

    return message


async def get_next_calendar_event(
    user_email: str
) -> Optional[Dict[str, Any]]:
    """
    Récupère le prochain événement Google Calendar

    Args:
        user_email: Email utilisateur

    Returns:
        Prochain événement ou None
    """
    # TODO: Implement Google Calendar API
    # For now, return mock data

    now = datetime.now()

    return {
        'id': 'event_001',
        'summary': 'Réunion client - Office OMPI',
        'location': 'Chemin des Colombettes 34, 1211 Genève',
        'start_time': now.replace(hour=9, minute=0),
        'end_time': now.replace(hour=10, minute=0),
        'attendees': ['klaus.mueller@biogeneve.ch'],
        'description': 'Dossier: Brevet vaccin COVID variant',
    }


def format_calendar_event_for_briefing(
    event: Dict[str, Any]
) -> str:
    """
    Formate un événement calendrier pour briefing

    Args:
        event: Événement Google Calendar

    Returns:
        Texte formaté pour TTS
    """
    start_time = event['start_time'].strftime('%Hh%M')

    message = f"📅 [{start_time}] {event['summary']}\n"

    if event.get('location'):
        message += f"   📍 {event['location']}\n"

    if event.get('description'):
        message += f"   📋 Note: {event['description']}\n"

    return message
