"""
Team Seats Manager
==================
Gestion des seats ChatGPT Team et autres abonnements IA gérés
"""

from .team_seats_router import router as team_seats_router
from .team_seats_models import TeamSeat, TeamSeatStatus, TeamSeatProvider
from .team_seats_service import team_seats_service

__all__ = [
    "team_seats_router",
    "TeamSeat",
    "TeamSeatStatus",
    "TeamSeatProvider",
    "team_seats_service",
]
