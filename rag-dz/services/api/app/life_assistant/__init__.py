"""
Life Assistant Module - Geneva Digital Butler
=============================================

PHASE 3: Universal Life Assistant

Fonctionnalités:
- Daily Briefing (Weather + Emails + Calendar + Reminders)
- Travel Intelligence (Google Maps + TPG Geneva)
- Workspace Connector (Gmail + Google Calendar)
- Mobile Pairing (QR Code + Audio Upload)
- Medication & Task Reminders

Created: 2025-01-16
"""

from . import daily_briefing
from . import travel_service
from . import workspace_connector
from . import mobile_router

__all__ = [
    "daily_briefing",
    "travel_service",
    "workspace_connector",
    "mobile_router",
]
