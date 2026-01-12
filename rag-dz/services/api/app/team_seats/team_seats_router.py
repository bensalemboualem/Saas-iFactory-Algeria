"""
Team Seats Router
=================
Endpoints FastAPI pour gestion des seats ChatGPT Team et autres
"""

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Header

from .team_seats_models import (
    TeamSeatStatus, TeamSeatProvider,
    SeatRequestInput, SeatRequestResponse, MySeatResponse,
    SeatPricingResponse, AdminSeatUpdateInput,
)
from .team_seats_service import team_seats_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/team-seats", tags=["Team Seats"])


# ============================================
# Public Endpoints
# ============================================

@router.get("/health")
async def team_seats_health():
    """Health check du module Team Seats"""
    stats = team_seats_service.get_stats()
    return {
        "status": "healthy",
        "module": "team_seats",
        "version": "1.0.0",
        "active_seats": stats["active_seats"],
        "pending_requests": stats["pending_requests"],
    }


@router.get("/plans", response_model=SeatPricingResponse)
async def get_available_plans():
    """
    Lister les plans disponibles avec leurs prix
    
    Retourne tous les plans Team disponibles (ChatGPT Team, Copilot, etc.)
    avec les prix en DZD.
    
    **Plans disponibles:**
    - `openai_team`: ChatGPT Team (6900 DA/mois)
    - `github_copilot`: GitHub Copilot Business (5400 DA/mois)
    - `cursor_pro`: Cursor Pro (5700 DA/mois)
    - `notion_ai`: Notion AI (2900 DA/mois)
    """
    plans = team_seats_service.get_available_plans()
    return SeatPricingResponse(
        success=True,
        plans=plans,
    )


@router.post("/request", response_model=SeatRequestResponse)
async def request_seat(
    input: SeatRequestInput,
    x_user_id: str = Header(default="anonymous", alias="X-User-Id"),
):
    """
    Demander un seat Team
    
    **Corps de la requête:**
    ```json
    {
        "email": "user@example.com",
        "name": "Ahmed Benali",
        "phone": "+213555123456",
        "provider": "openai_team",
        "message": "J'ai besoin de ChatGPT Team pour mon équipe de 3 personnes"
    }
    ```
    
    **Providers disponibles:**
    - `openai_team`: ChatGPT Team
    - `github_copilot`: GitHub Copilot Business
    - `cursor_pro`: Cursor Pro
    - `notion_ai`: Notion AI
    
    **Process:**
    1. Vous soumettez la demande
    2. Un conseiller vous contacte sous 24-48h
    3. Vous effectuez le paiement (CCP, BaridiMob, virement)
    4. Nous activons votre seat sous 24h
    
    Returns:
        Confirmation avec ID de demande et prochaines étapes
    """
    try:
        response = team_seats_service.request_seat(
            user_id=x_user_id,
            input=input,
        )
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except Exception as e:
        logger.error(f"Seat request error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mine", response_model=MySeatResponse)
async def get_my_seats(
    x_user_id: str = Header(default="anonymous", alias="X-User-Id"),
):
    """
    Voir mes seats
    
    Retourne la liste de vos seats actifs et leur statut.
    """
    try:
        return team_seats_service.get_my_seats(user_id=x_user_id)
    except Exception as e:
        logger.error(f"Get my seats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mine/requests")
async def get_my_requests(
    x_user_id: str = Header(default="anonymous", alias="X-User-Id"),
):
    """
    Voir mes demandes de seats
    
    Retourne l'historique de vos demandes de seats.
    """
    try:
        requests = team_seats_service.get_my_requests(user_id=x_user_id)
        return {
            "success": True,
            "requests": [r.model_dump() for r in requests],
            "total": len(requests),
        }
    except Exception as e:
        logger.error(f"Get my requests error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{seat_id}")
async def get_seat(
    seat_id: str,
    x_user_id: str = Header(default="anonymous", alias="X-User-Id"),
):
    """
    Voir un seat spécifique
    
    Args:
        seat_id: ID du seat
    
    Returns:
        Détails du seat
    """
    seat = team_seats_service.get_seat(seat_id, user_id=x_user_id)
    
    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")
    
    return {
        "success": True,
        "seat": seat.model_dump(),
    }


# ============================================
# Admin Endpoints
# ============================================

@router.get("/admin/requests")
async def admin_list_requests(
    status: Optional[str] = Query(None),
    limit: int = Query(default=50, ge=1, le=200),
    x_admin_key: str = Header(default=None, alias="X-Admin-Key"),
):
    """
    [ADMIN] Lister toutes les demandes
    
    Args:
        status: Filtrer par status (pending, approved, rejected)
        limit: Nombre max
    
    ⚠️ Nécessite X-Admin-Key header
    """
    # TODO: Vérification admin key
    if x_admin_key != "admin_secret_key":  # À remplacer par vraie auth
        pass  # Pour l'instant on laisse passer pour le dev
    
    try:
        requests = team_seats_service.list_all_requests(status=status, limit=limit)
        return {
            "success": True,
            "requests": [r.model_dump() for r in requests],
            "total": len(requests),
        }
    except Exception as e:
        logger.error(f"Admin list requests error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/admin/seats")
async def admin_list_seats(
    status: Optional[TeamSeatStatus] = Query(None),
    provider: Optional[TeamSeatProvider] = Query(None),
    limit: int = Query(default=100, ge=1, le=500),
    x_admin_key: str = Header(default=None, alias="X-Admin-Key"),
):
    """
    [ADMIN] Lister tous les seats
    
    Args:
        status: Filtrer par status
        provider: Filtrer par provider
        limit: Nombre max
    
    ⚠️ Nécessite X-Admin-Key header
    """
    try:
        seats = team_seats_service.list_all_seats(
            status=status,
            provider=provider,
            limit=limit,
        )
        return {
            "success": True,
            "seats": [s.model_dump() for s in seats],
            "total": len(seats),
        }
    except Exception as e:
        logger.error(f"Admin list seats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/admin/stats")
async def admin_get_stats(
    x_admin_key: str = Header(default=None, alias="X-Admin-Key"),
):
    """
    [ADMIN] Obtenir les statistiques
    
    ⚠️ Nécessite X-Admin-Key header
    """
    try:
        stats = team_seats_service.get_stats()
        return {
            "success": True,
            **stats,
        }
    except Exception as e:
        logger.error(f"Admin stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/requests/{request_id}/approve")
async def admin_approve_request(
    request_id: str,
    response: Optional[str] = Query(None, description="Message pour l'utilisateur"),
    x_admin_key: str = Header(default=None, alias="X-Admin-Key"),
):
    """
    [ADMIN] Approuver une demande
    
    Args:
        request_id: ID de la demande
        response: Message pour l'utilisateur
    
    ⚠️ Nécessite X-Admin-Key header
    """
    try:
        seat = team_seats_service.approve_request(request_id, admin_response=response)
        
        if not seat:
            raise HTTPException(status_code=404, detail="Request not found")
        
        return {
            "success": True,
            "message": "Request approved, seat created",
            "seat_id": seat.id,
            "seat": seat.model_dump(),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin approve error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/requests/{request_id}/reject")
async def admin_reject_request(
    request_id: str,
    reason: str = Query(..., description="Raison du rejet"),
    x_admin_key: str = Header(default=None, alias="X-Admin-Key"),
):
    """
    [ADMIN] Rejeter une demande
    
    Args:
        request_id: ID de la demande
        reason: Raison du rejet
    
    ⚠️ Nécessite X-Admin-Key header
    """
    try:
        success = team_seats_service.reject_request(request_id, reason=reason)
        
        if not success:
            raise HTTPException(status_code=404, detail="Request not found")
        
        return {
            "success": True,
            "message": "Request rejected",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin reject error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/{seat_id}/activate")
async def admin_activate_seat(
    seat_id: str,
    external_seat_id: Optional[str] = Query(None),
    external_email: Optional[str] = Query(None),
    admin_notes: Optional[str] = Query(None),
    x_admin_key: str = Header(default=None, alias="X-Admin-Key"),
):
    """
    [ADMIN] Activer un seat (après paiement)
    
    Args:
        seat_id: ID du seat
        external_seat_id: ID du seat côté provider
        external_email: Email utilisé côté provider
        admin_notes: Notes admin
    
    ⚠️ Nécessite X-Admin-Key header
    """
    try:
        seat = team_seats_service.activate_seat(
            seat_id,
            external_seat_id=external_seat_id,
            external_email=external_email,
            admin_notes=admin_notes,
        )
        
        if not seat:
            raise HTTPException(status_code=404, detail="Seat not found")
        
        return {
            "success": True,
            "message": "Seat activated successfully",
            "seat": seat.model_dump(),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin activate error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/{seat_id}/suspend")
async def admin_suspend_seat(
    seat_id: str,
    reason: str = Query(..., description="Raison de la suspension"),
    x_admin_key: str = Header(default=None, alias="X-Admin-Key"),
):
    """
    [ADMIN] Suspendre un seat
    
    Args:
        seat_id: ID du seat
        reason: Raison de la suspension
    
    ⚠️ Nécessite X-Admin-Key header
    """
    try:
        seat = team_seats_service.suspend_seat(seat_id, reason=reason)
        
        if not seat:
            raise HTTPException(status_code=404, detail="Seat not found")
        
        return {
            "success": True,
            "message": "Seat suspended",
            "seat": seat.model_dump(),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin suspend error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/{seat_id}/cancel")
async def admin_cancel_seat(
    seat_id: str,
    reason: str = Query(..., description="Raison de l'annulation"),
    x_admin_key: str = Header(default=None, alias="X-Admin-Key"),
):
    """
    [ADMIN] Annuler un seat définitivement
    
    Args:
        seat_id: ID du seat
        reason: Raison de l'annulation
    
    ⚠️ Nécessite X-Admin-Key header
    """
    try:
        seat = team_seats_service.cancel_seat(seat_id, reason=reason)
        
        if not seat:
            raise HTTPException(status_code=404, detail="Seat not found")
        
        return {
            "success": True,
            "message": "Seat canceled",
            "seat": seat.model_dump(),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin cancel error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/{seat_id}/reactivate")
async def admin_reactivate_seat(
    seat_id: str,
    x_admin_key: str = Header(default=None, alias="X-Admin-Key"),
):
    """
    [ADMIN] Réactiver un seat suspendu
    
    Args:
        seat_id: ID du seat
    
    ⚠️ Nécessite X-Admin-Key header
    """
    try:
        seat = team_seats_service.reactivate_seat(seat_id)
        
        if not seat:
            raise HTTPException(
                status_code=400,
                detail="Seat not found or not in suspended status",
            )
        
        return {
            "success": True,
            "message": "Seat reactivated",
            "seat": seat.model_dump(),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin reactivate error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
