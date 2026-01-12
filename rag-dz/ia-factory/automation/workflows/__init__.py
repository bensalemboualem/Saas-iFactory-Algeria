"""
IA Factory Automation - Workflows Package
"""

from .lead_generation import router as leads_router
from .proposal_automation import router as proposals_router
from .social_media_manager import router as social_router
from .digital_twin import router as twin_router

__all__ = [
    "leads_router",
    "proposals_router", 
    "social_router",
    "twin_router"
]
