"""
Team Seats Service
==================
Logique métier pour gestion des seats ChatGPT Team et autres
"""

import logging
from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import Optional, List

from .team_seats_models import (
    TeamSeat, SeatRequest, TeamSeatStatus, TeamSeatProvider,
    SeatRequestInput, SeatRequestResponse, MySeatResponse,
    SeatRequestPriority, SEAT_PRICING,
)

logger = logging.getLogger(__name__)


# ============================================
# In-Memory Storage (MVP)
# ============================================

seats_db: dict[str, TeamSeat] = {}
requests_db: dict[str, SeatRequest] = {}


# ============================================
# Team Seats Service
# ============================================

class TeamSeatsService:
    """Service de gestion des seats Team"""
    
    def __init__(self):
        self.pricing = SEAT_PRICING
    
    # ========================================
    # User Methods
    # ========================================
    
    def request_seat(
        self,
        user_id: str,
        input: SeatRequestInput,
    ) -> SeatRequestResponse:
        """
        Soumettre une demande de seat
        
        Args:
            user_id: ID de l'utilisateur
            input: Détails de la demande
        
        Returns:
            SeatRequestResponse avec confirmation
        """
        # Vérifier si le provider est disponible
        pricing = self.pricing.get(input.provider)
        if not pricing or not pricing.is_available:
            return SeatRequestResponse(
                success=False,
                request_id="",
                message=f"Ce plan n'est pas disponible actuellement: {input.provider.value}",
                next_steps=["Contactez-nous pour plus d'informations"],
            )
        
        # Créer la demande
        request = SeatRequest(
            user_id=user_id,
            user_email=input.email,
            user_name=input.name,
            phone=input.phone,
            provider=input.provider,
            plan_requested=input.plan or pricing.plan_name,
            message=input.message,
        )
        
        requests_db[request.id] = request
        
        logger.info(f"New seat request {request.id} from {user_id} for {input.provider.value}")
        
        # Préparer les prochaines étapes
        next_steps = [
            "Votre demande a été enregistrée",
            f"Un conseiller vous contactera sous 24-48h à {input.email}",
            "Préparez votre paiement (CCP, BaridiMob, ou virement)",
            "Une fois le paiement confirmé, nous activerons votre seat sous 24h",
        ]
        
        return SeatRequestResponse(
            success=True,
            request_id=request.id,
            message=f"Demande de {pricing.plan_name} enregistrée avec succès!",
            estimated_processing_time="24-48h",
            next_steps=next_steps,
        )
    
    def get_my_seats(self, user_id: str) -> MySeatResponse:
        """
        Récupérer les seats d'un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
        
        Returns:
            MySeatResponse avec la liste des seats
        """
        user_seats = [s for s in seats_db.values() if s.user_id == user_id]
        
        # Trier par date de création (récent d'abord)
        user_seats.sort(key=lambda x: x.created_at, reverse=True)
        
        return MySeatResponse(
            success=True,
            seats=user_seats,
            total=len(user_seats),
        )
    
    def get_seat(self, seat_id: str, user_id: Optional[str] = None) -> Optional[TeamSeat]:
        """
        Récupérer un seat par son ID
        
        Args:
            seat_id: ID du seat
            user_id: Si fourni, vérifie que le seat appartient à cet utilisateur
        
        Returns:
            TeamSeat ou None
        """
        seat = seats_db.get(seat_id)
        
        if seat and user_id and seat.user_id != user_id:
            return None  # Pas le bon utilisateur
        
        return seat
    
    def get_my_requests(self, user_id: str) -> List[SeatRequest]:
        """
        Récupérer les demandes d'un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
        
        Returns:
            Liste des demandes
        """
        user_requests = [r for r in requests_db.values() if r.user_id == user_id]
        user_requests.sort(key=lambda x: x.created_at, reverse=True)
        return user_requests
    
    def get_available_plans(self) -> List[dict]:
        """
        Récupérer les plans disponibles avec leurs prix
        
        Returns:
            Liste des plans avec pricing
        """
        plans = []
        
        for provider, pricing in self.pricing.items():
            if pricing.is_available:
                plans.append({
                    "provider": provider.value,
                    "plan_name": pricing.plan_name,
                    "price_dzd_month": float(pricing.price_dzd_month),
                    "setup_fee_dzd": float(pricing.setup_fee_dzd),
                    "description": pricing.description,
                    "features": pricing.features,
                    "seats_available": pricing.max_seats,
                })
        
        return plans
    
    # ========================================
    # Admin Methods
    # ========================================
    
    def list_all_requests(
        self,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> List[SeatRequest]:
        """
        Lister toutes les demandes (admin)
        
        Args:
            status: Filtrer par status
            limit: Nombre max
        
        Returns:
            Liste des demandes
        """
        all_requests = list(requests_db.values())
        
        if status:
            all_requests = [r for r in all_requests if r.status == status]
        
        all_requests.sort(key=lambda x: x.created_at, reverse=True)
        
        return all_requests[:limit]
    
    def list_all_seats(
        self,
        status: Optional[TeamSeatStatus] = None,
        provider: Optional[TeamSeatProvider] = None,
        limit: int = 100,
    ) -> List[TeamSeat]:
        """
        Lister tous les seats (admin)
        
        Args:
            status: Filtrer par status
            provider: Filtrer par provider
            limit: Nombre max
        
        Returns:
            Liste des seats
        """
        all_seats = list(seats_db.values())
        
        if status:
            all_seats = [s for s in all_seats if s.status == status]
        
        if provider:
            all_seats = [s for s in all_seats if s.provider == provider]
        
        all_seats.sort(key=lambda x: x.created_at, reverse=True)
        
        return all_seats[:limit]
    
    def approve_request(
        self,
        request_id: str,
        admin_response: Optional[str] = None,
    ) -> Optional[TeamSeat]:
        """
        Approuver une demande et créer le seat
        
        Args:
            request_id: ID de la demande
            admin_response: Message de l'admin
        
        Returns:
            TeamSeat créé ou None
        """
        request = requests_db.get(request_id)
        if not request:
            return None
        
        # Récupérer le pricing
        pricing = self.pricing.get(request.provider)
        if not pricing:
            return None
        
        # Créer le seat
        seat = TeamSeat(
            user_id=request.user_id,
            user_email=request.user_email,
            user_name=request.user_name,
            provider=request.provider,
            plan_name=pricing.plan_name,
            status=TeamSeatStatus.PAYMENT_PENDING,
            price_dzd_month=pricing.price_dzd_month,
            cost_usd_month=pricing.cost_usd_month,
            billing_cycle_day=1,
        )
        
        seats_db[seat.id] = seat
        
        # Mettre à jour la demande
        request.status = "approved"
        request.seat_id = seat.id
        request.admin_response = admin_response
        request.processed_at = datetime.now()
        
        logger.info(f"Request {request_id} approved, seat {seat.id} created")
        
        return seat
    
    def reject_request(
        self,
        request_id: str,
        reason: str,
    ) -> bool:
        """
        Rejeter une demande
        
        Args:
            request_id: ID de la demande
            reason: Raison du rejet
        
        Returns:
            True si succès
        """
        request = requests_db.get(request_id)
        if not request:
            return False
        
        request.status = "rejected"
        request.admin_response = reason
        request.processed_at = datetime.now()
        
        logger.info(f"Request {request_id} rejected: {reason}")
        
        return True
    
    def activate_seat(
        self,
        seat_id: str,
        external_seat_id: Optional[str] = None,
        external_email: Optional[str] = None,
        admin_notes: Optional[str] = None,
    ) -> Optional[TeamSeat]:
        """
        Activer un seat (après paiement)
        
        Args:
            seat_id: ID du seat
            external_seat_id: ID côté provider
            external_email: Email utilisé côté provider
            admin_notes: Notes admin
        
        Returns:
            TeamSeat mis à jour ou None
        """
        seat = seats_db.get(seat_id)
        if not seat:
            return None
        
        # Calculer la prochaine date de facturation
        today = date.today()
        if today.day >= seat.billing_cycle_day:
            # Prochain mois
            if today.month == 12:
                next_billing = date(today.year + 1, 1, seat.billing_cycle_day)
            else:
                next_billing = date(today.year, today.month + 1, seat.billing_cycle_day)
        else:
            next_billing = date(today.year, today.month, seat.billing_cycle_day)
        
        # Mettre à jour le seat
        seat.status = TeamSeatStatus.ACTIVE
        seat.activated_at = datetime.now()
        seat.last_payment_date = today
        seat.next_billing_date = next_billing
        seat.external_seat_id = external_seat_id
        seat.external_email = external_email
        seat.admin_notes = admin_notes
        seat.updated_at = datetime.now()
        
        logger.info(f"Seat {seat_id} activated for {seat.user_email}")
        
        return seat
    
    def suspend_seat(
        self,
        seat_id: str,
        reason: str,
    ) -> Optional[TeamSeat]:
        """
        Suspendre un seat (impayé, violation, etc.)
        
        Args:
            seat_id: ID du seat
            reason: Raison de la suspension
        
        Returns:
            TeamSeat mis à jour ou None
        """
        seat = seats_db.get(seat_id)
        if not seat:
            return None
        
        seat.status = TeamSeatStatus.SUSPENDED
        seat.status_reason = reason
        seat.suspended_at = datetime.now()
        seat.updated_at = datetime.now()
        
        logger.info(f"Seat {seat_id} suspended: {reason}")
        
        return seat
    
    def cancel_seat(
        self,
        seat_id: str,
        reason: str,
    ) -> Optional[TeamSeat]:
        """
        Annuler un seat définitivement
        
        Args:
            seat_id: ID du seat
            reason: Raison de l'annulation
        
        Returns:
            TeamSeat mis à jour ou None
        """
        seat = seats_db.get(seat_id)
        if not seat:
            return None
        
        seat.status = TeamSeatStatus.CANCELED
        seat.status_reason = reason
        seat.canceled_at = datetime.now()
        seat.updated_at = datetime.now()
        
        logger.info(f"Seat {seat_id} canceled: {reason}")
        
        return seat
    
    def reactivate_seat(
        self,
        seat_id: str,
    ) -> Optional[TeamSeat]:
        """
        Réactiver un seat suspendu
        
        Args:
            seat_id: ID du seat
        
        Returns:
            TeamSeat mis à jour ou None
        """
        seat = seats_db.get(seat_id)
        if not seat or seat.status != TeamSeatStatus.SUSPENDED:
            return None
        
        seat.status = TeamSeatStatus.ACTIVE
        seat.status_reason = None
        seat.suspended_at = None
        seat.last_payment_date = date.today()
        seat.updated_at = datetime.now()
        
        logger.info(f"Seat {seat_id} reactivated")
        
        return seat
    
    def update_seat(
        self,
        seat_id: str,
        **kwargs,
    ) -> Optional[TeamSeat]:
        """
        Mettre à jour un seat (admin)
        
        Args:
            seat_id: ID du seat
            **kwargs: Champs à mettre à jour
        
        Returns:
            TeamSeat mis à jour ou None
        """
        seat = seats_db.get(seat_id)
        if not seat:
            return None
        
        for key, value in kwargs.items():
            if hasattr(seat, key) and value is not None:
                setattr(seat, key, value)
        
        seat.updated_at = datetime.now()
        
        return seat
    
    # ========================================
    # Stats
    # ========================================
    
    def get_stats(self) -> dict:
        """
        Obtenir les statistiques globales
        
        Returns:
            Dict avec les stats
        """
        all_seats = list(seats_db.values())
        all_requests = list(requests_db.values())
        
        # Par status
        status_counts = {}
        for status in TeamSeatStatus:
            status_counts[status.value] = len([s for s in all_seats if s.status == status])
        
        # Par provider
        provider_counts = {}
        for provider in TeamSeatProvider:
            provider_counts[provider.value] = len([s for s in all_seats if s.provider == provider])
        
        # Revenue mensuel estimé
        active_seats = [s for s in all_seats if s.status == TeamSeatStatus.ACTIVE]
        monthly_revenue_dzd = sum(float(s.price_dzd_month) for s in active_seats)
        monthly_cost_usd = sum(float(s.cost_usd_month) for s in active_seats)
        
        return {
            "total_seats": len(all_seats),
            "active_seats": len(active_seats),
            "pending_requests": len([r for r in all_requests if r.status == "pending"]),
            "status_breakdown": status_counts,
            "provider_breakdown": provider_counts,
            "monthly_revenue_dzd": monthly_revenue_dzd,
            "monthly_cost_usd": monthly_cost_usd,
            "monthly_margin_dzd": monthly_revenue_dzd - (monthly_cost_usd * 140),  # Approximation taux
        }


# Singleton
team_seats_service = TeamSeatsService()
