"""
Calendar Router - API Mock pour Cal.com integration
Fournit des endpoints pour la gestion des rendez-vous
"""

import uuid
import logging
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, EmailStr

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/calendar", tags=["calendar"])


# ===================== Models =====================

class AppointmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    startTime: str
    endTime: str
    patientName: str
    patientEmail: Optional[str] = None
    patientPhone: Optional[str] = None
    motif: str
    location: Optional[str] = None
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class Appointment(AppointmentBase):
    id: str
    status: str  # confirmed, pending, cancelled, completed
    createdAt: str
    updatedAt: str


class AppointmentStats(BaseModel):
    total: int
    confirmed: int
    pending: int
    cancelled: int
    completed: int
    today: int
    thisWeek: int


# ===================== Mock Data =====================

# Données mock pour le développement
def generate_mock_appointments() -> List[dict]:
    """Génère des rendez-vous fictifs pour les tests"""
    now = datetime.utcnow()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)

    return [
        {
            "id": "apt-001",
            "title": "Consultation initiale",
            "description": "Première consultation patient",
            "startTime": (today + timedelta(hours=9)).isoformat(),
            "endTime": (today + timedelta(hours=9, minutes=30)).isoformat(),
            "patientName": "Jean Dupont",
            "patientEmail": "jean.dupont@email.com",
            "patientPhone": "+33 6 12 34 56 78",
            "motif": "Consultation générale",
            "status": "confirmed",
            "location": "Cabinet principal",
            "notes": "Patient régulier, suivi annuel",
            "createdAt": (now - timedelta(days=3)).isoformat(),
            "updatedAt": (now - timedelta(days=1)).isoformat(),
        },
        {
            "id": "apt-002",
            "title": "Suivi traitement",
            "description": "Suivi du traitement en cours",
            "startTime": (today + timedelta(hours=11, minutes=30)).isoformat(),
            "endTime": (today + timedelta(hours=12)).isoformat(),
            "patientName": "Marie Martin",
            "patientEmail": "marie.martin@email.com",
            "patientPhone": "+33 6 98 76 54 32",
            "motif": "Suivi médical",
            "status": "pending",
            "location": "Cabinet principal",
            "notes": None,
            "createdAt": (now - timedelta(days=1)).isoformat(),
            "updatedAt": (now - timedelta(days=1)).isoformat(),
        },
        {
            "id": "apt-003",
            "title": "Nouveau patient",
            "description": "Première visite",
            "startTime": (today + timedelta(hours=14)).isoformat(),
            "endTime": (today + timedelta(hours=14, minutes=45)).isoformat(),
            "patientName": "Pierre Bernard",
            "patientEmail": "pierre.bernard@email.com",
            "patientPhone": "+33 6 55 44 33 22",
            "motif": "Première consultation",
            "status": "confirmed",
            "location": "Cabinet principal",
            "notes": "Nouveau patient, dossier à créer",
            "createdAt": (now - timedelta(hours=12)).isoformat(),
            "updatedAt": (now - timedelta(hours=12)).isoformat(),
        },
        {
            "id": "apt-004",
            "title": "Téléconsultation",
            "description": "Consultation en ligne",
            "startTime": (today + timedelta(days=1, hours=10)).isoformat(),
            "endTime": (today + timedelta(days=1, hours=10, minutes=30)).isoformat(),
            "patientName": "Sophie Leroy",
            "patientEmail": "sophie.leroy@email.com",
            "patientPhone": "+33 6 11 22 33 44",
            "motif": "Renouvellement ordonnance",
            "status": "pending",
            "location": "Visio",
            "notes": "Préparer ordonnance à l'avance",
            "createdAt": (now - timedelta(hours=6)).isoformat(),
            "updatedAt": (now - timedelta(hours=6)).isoformat(),
        },
        {
            "id": "apt-005",
            "title": "Urgence annulée",
            "description": "Rendez-vous annulé par le patient",
            "startTime": (today - timedelta(days=1, hours=-15)).isoformat(),
            "endTime": (today - timedelta(days=1, hours=-14, minutes=-30)).isoformat(),
            "patientName": "Lucas Moreau",
            "patientEmail": "lucas.moreau@email.com",
            "patientPhone": "+33 6 77 88 99 00",
            "motif": "Urgence",
            "status": "cancelled",
            "location": "Cabinet principal",
            "notes": "Annulé - patient indisponible",
            "createdAt": (now - timedelta(days=2)).isoformat(),
            "updatedAt": (now - timedelta(days=1)).isoformat(),
        },
        {
            "id": "apt-006",
            "title": "Consultation terminée",
            "description": "Consultation effectuée",
            "startTime": (today - timedelta(days=2, hours=-9)).isoformat(),
            "endTime": (today - timedelta(days=2, hours=-8, minutes=-30)).isoformat(),
            "patientName": "Emma Petit",
            "patientEmail": "emma.petit@email.com",
            "patientPhone": "+33 6 66 55 44 33",
            "motif": "Bilan de santé",
            "status": "completed",
            "location": "Cabinet principal",
            "notes": "RAS, prochain RDV dans 6 mois",
            "createdAt": (now - timedelta(days=5)).isoformat(),
            "updatedAt": (now - timedelta(days=2)).isoformat(),
        },
    ]


# Cache mock data
_mock_appointments = generate_mock_appointments()


# ===================== Endpoints =====================

@router.get("/appointments", response_model=List[Appointment])
async def get_appointments(
    status: Optional[str] = Query(None, description="Filter by status"),
    start_date: Optional[str] = Query(None, description="Filter from date"),
    end_date: Optional[str] = Query(None, description="Filter to date"),
    patient_name: Optional[str] = Query(None, description="Filter by patient name"),
):
    """
    Récupère la liste des rendez-vous avec filtres optionnels
    """
    appointments = _mock_appointments.copy()

    # Filter by status
    if status:
        appointments = [a for a in appointments if a["status"] == status]

    # Filter by patient name
    if patient_name:
        appointments = [
            a for a in appointments
            if patient_name.lower() in a["patientName"].lower()
        ]

    # Filter by date range
    if start_date:
        start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
        appointments = [
            a for a in appointments
            if datetime.fromisoformat(a["startTime"].replace("Z", "+00:00")) >= start
        ]

    if end_date:
        end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
        appointments = [
            a for a in appointments
            if datetime.fromisoformat(a["startTime"].replace("Z", "+00:00")) <= end
        ]

    # Sort by start time
    appointments.sort(key=lambda x: x["startTime"])

    logger.info(f"Returning {len(appointments)} appointments")
    return appointments


@router.get("/appointments/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: str):
    """
    Récupère un rendez-vous par son ID
    """
    for apt in _mock_appointments:
        if apt["id"] == appointment_id:
            return apt

    raise HTTPException(status_code=404, detail="Rendez-vous non trouvé")


@router.post("/book", response_model=Appointment)
async def create_appointment(data: AppointmentCreate):
    """
    Crée un nouveau rendez-vous
    """
    new_id = f"apt-{str(uuid.uuid4())[:8]}"
    now = datetime.utcnow().isoformat()

    new_appointment = {
        "id": new_id,
        **data.dict(),
        "status": "pending",
        "createdAt": now,
        "updatedAt": now,
    }

    _mock_appointments.append(new_appointment)
    logger.info(f"Created appointment {new_id} for {data.patientName}")

    return new_appointment


@router.put("/appointments/{appointment_id}", response_model=Appointment)
async def update_appointment(appointment_id: str, data: AppointmentCreate):
    """
    Met à jour un rendez-vous existant
    """
    for i, apt in enumerate(_mock_appointments):
        if apt["id"] == appointment_id:
            _mock_appointments[i] = {
                **apt,
                **data.dict(),
                "updatedAt": datetime.utcnow().isoformat(),
            }
            return _mock_appointments[i]

    raise HTTPException(status_code=404, detail="Rendez-vous non trouvé")


@router.post("/appointments/{appointment_id}/confirm", response_model=Appointment)
async def confirm_appointment(appointment_id: str):
    """
    Confirme un rendez-vous en attente
    """
    for i, apt in enumerate(_mock_appointments):
        if apt["id"] == appointment_id:
            if apt["status"] == "cancelled":
                raise HTTPException(
                    status_code=400,
                    detail="Impossible de confirmer un rendez-vous annulé"
                )
            _mock_appointments[i]["status"] = "confirmed"
            _mock_appointments[i]["updatedAt"] = datetime.utcnow().isoformat()
            logger.info(f"Confirmed appointment {appointment_id}")
            return _mock_appointments[i]

    raise HTTPException(status_code=404, detail="Rendez-vous non trouvé")


@router.post("/appointments/{appointment_id}/reschedule", response_model=Appointment)
async def reschedule_appointment(
    appointment_id: str,
    start_time: str,
    end_time: str,
):
    """
    Reporte un rendez-vous à une nouvelle date/heure
    """
    for i, apt in enumerate(_mock_appointments):
        if apt["id"] == appointment_id:
            if apt["status"] == "cancelled":
                raise HTTPException(
                    status_code=400,
                    detail="Impossible de reporter un rendez-vous annulé"
                )
            _mock_appointments[i]["startTime"] = start_time
            _mock_appointments[i]["endTime"] = end_time
            _mock_appointments[i]["status"] = "pending"  # Reset to pending
            _mock_appointments[i]["updatedAt"] = datetime.utcnow().isoformat()
            logger.info(f"Rescheduled appointment {appointment_id} to {start_time}")
            return _mock_appointments[i]

    raise HTTPException(status_code=404, detail="Rendez-vous non trouvé")


@router.delete("/cancel/{appointment_id}")
async def cancel_appointment(appointment_id: str, reason: Optional[str] = None):
    """
    Annule un rendez-vous
    """
    for i, apt in enumerate(_mock_appointments):
        if apt["id"] == appointment_id:
            _mock_appointments[i]["status"] = "cancelled"
            _mock_appointments[i]["updatedAt"] = datetime.utcnow().isoformat()
            if reason:
                _mock_appointments[i]["notes"] = f"Annulé: {reason}"
            logger.info(f"Cancelled appointment {appointment_id}")
            return {"success": True, "message": "Rendez-vous annulé"}

    raise HTTPException(status_code=404, detail="Rendez-vous non trouvé")


@router.post("/sync")
async def sync_calendars():
    """
    Synchronise avec Google Calendar (mock)
    """
    # Simulation de synchronisation
    import random
    synced_count = random.randint(2, 8)

    logger.info(f"Calendar sync completed: {synced_count} events synced")

    return {
        "success": True,
        "synced_count": synced_count,
        "last_sync": datetime.utcnow().isoformat(),
    }


@router.get("/available-slots")
async def get_available_slots(
    date: str = Query(..., description="Date au format YYYY-MM-DD"),
    duration: int = Query(30, description="Durée en minutes"),
):
    """
    Récupère les créneaux disponibles pour une date donnée
    """
    # Parse date
    try:
        target_date = datetime.fromisoformat(date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Format de date invalide")

    # Working hours: 9h-18h
    slots = []
    current = target_date.replace(hour=9, minute=0, second=0, microsecond=0)
    end_of_day = target_date.replace(hour=18, minute=0, second=0, microsecond=0)

    while current < end_of_day:
        slot_end = current + timedelta(minutes=duration)

        # Check if slot conflicts with existing appointments
        is_available = True
        for apt in _mock_appointments:
            if apt["status"] in ["confirmed", "pending"]:
                apt_start = datetime.fromisoformat(apt["startTime"].replace("Z", "+00:00"))
                apt_end = datetime.fromisoformat(apt["endTime"].replace("Z", "+00:00"))

                if apt_start.date() == target_date.date():
                    # Check overlap
                    if not (slot_end <= apt_start or current >= apt_end):
                        is_available = False
                        break

        if is_available:
            slots.append({
                "start": current.isoformat(),
                "end": slot_end.isoformat(),
            })

        current = slot_end

    return slots


@router.get("/stats", response_model=AppointmentStats)
async def get_appointment_stats():
    """
    Récupère les statistiques des rendez-vous
    """
    now = datetime.utcnow()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today - timedelta(days=today.weekday())

    stats = {
        "total": len(_mock_appointments),
        "confirmed": 0,
        "pending": 0,
        "cancelled": 0,
        "completed": 0,
        "today": 0,
        "thisWeek": 0,
    }

    for apt in _mock_appointments:
        # Count by status
        stats[apt["status"]] = stats.get(apt["status"], 0) + 1

        # Count today
        apt_date = datetime.fromisoformat(apt["startTime"].replace("Z", "+00:00"))
        if apt_date.date() == today.date():
            stats["today"] += 1

        # Count this week
        if week_start <= apt_date < week_start + timedelta(days=7):
            stats["thisWeek"] += 1

    return stats


@router.get("/health")
async def calendar_health():
    """
    Vérifie le statut du service calendar
    """
    return {
        "status": "healthy",
        "service": "calendar",
        "mode": "mock",
        "appointments_count": len(_mock_appointments),
        "calcom_integration": "ready",
    }
