"""
Promo Codes API Router
======================
Gestion des codes promo pour le lancement 30 premiers clients.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/promo", tags=["Promo Codes"])

# ============================================
# Models
# ============================================

class PromoCode(BaseModel):
    code: str
    discount_percent: int
    max_uses: int
    current_uses: int = 0
    valid_from: datetime
    valid_until: datetime
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True
    applicable_packages: List[str]  # ["starter", "dev"]
    duration_months: int  # 6

class ValidatePromoRequest(BaseModel):
    code: str
    package: str

class ValidatePromoResponse(BaseModel):
    valid: bool
    discount_percent: Optional[int] = None
    duration_months: Optional[int] = None
    message: str

class PromoRemainingResponse(BaseModel):
    remaining: int
    total: int
    percent_filled: float

class SignupRequest(BaseModel):
    email: str
    package: str  # "starter", "dev", "business", "premium"
    promo_code: Optional[str] = None

class SignupResponse(BaseModel):
    success: bool
    user_id: str
    package: str
    price_dzd: int
    discount_percent: int = 0
    discount_until: Optional[datetime] = None
    message: str

# ============================================
# In-memory store
# ============================================

# Codes promo actifs (en production: PostgreSQL)
_promo_codes = {
    "LAUNCH30": PromoCode(
        code="LAUNCH30",
        discount_percent=25,  # 25% pour Starter, 33% pour Dev (calculé dynamiquement)
        max_uses=30,
        current_uses=0,
        valid_from=datetime(2025, 12, 6),  # Actif dès aujourd'hui
        valid_until=datetime(2026, 1, 7),  # 1 mois
        applicable_packages=["starter", "dev"],
        duration_months=6
    )
}

# Clients inscrits (en production: PostgreSQL)
_clients = {}

# Pricing normal
_PRICING = {
    "starter": 10000,  # DZD/mois
    "dev": 15000,
    "business": 75000,
    "premium": 250000
}

# Pricing promo (-25% Starter, -33% Dev)
_PROMO_PRICING = {
    "starter": 7500,  # -25%
    "dev": 10000,     # -33%
}

# ============================================
# Helper Functions
# ============================================

def get_promo_code(code: str) -> Optional[PromoCode]:
    """Récupère un code promo"""
    return _promo_codes.get(code.upper())

def validate_promo_code(code: str, package: str) -> tuple[bool, str, Optional[PromoCode]]:
    """
    Valide un code promo.
    Returns: (valid, message, promo_code)
    """
    promo = get_promo_code(code)

    if not promo:
        return False, "Code promo invalide", None

    if not promo.is_active:
        return False, "Code promo désactivé", None

    now = datetime.now()
    if now < promo.valid_from:
        return False, "Code promo pas encore valide", None

    if now > promo.valid_until:
        return False, "Code promo expiré", None

    if promo.current_uses >= promo.max_uses:
        return False, f"Code promo expiré ({promo.max_uses} clients atteints)", None

    if package.lower() not in promo.applicable_packages:
        return False, f"Code promo non applicable au package {package}", None

    return True, "Code promo valide", promo

def increment_promo_usage(code: str):
    """Incrémente le compteur d'utilisation d'un code promo"""
    promo = get_promo_code(code)
    if promo:
        promo.current_uses += 1
        logger.info(f"Promo code {code} used: {promo.current_uses}/{promo.max_uses}")

def calculate_discount(package: str, promo: Optional[PromoCode]) -> int:
    """Calcule la réduction en %"""
    if not promo or package.lower() not in promo.applicable_packages:
        return 0

    # Pour LAUNCH30: 25% Starter, 33% Dev
    if promo.code == "LAUNCH30":
        return 25 if package.lower() == "starter" else 33

    return promo.discount_percent

# ============================================
# Endpoints
# ============================================

@router.post("/validate", response_model=ValidatePromoResponse)
async def validate_promo(request: ValidatePromoRequest):
    """
    Valide un code promo pour un package donné.

    **Exemple**:
    ```json
    {
        "code": "LAUNCH30",
        "package": "starter"
    }
    ```
    """
    valid, message, promo = validate_promo_code(request.code, request.package)

    if not valid:
        return ValidatePromoResponse(
            valid=False,
            message=message
        )

    discount = calculate_discount(request.package, promo)

    return ValidatePromoResponse(
        valid=True,
        discount_percent=discount,
        duration_months=promo.duration_months,
        message=f"Réduction de {discount}% pendant {promo.duration_months} mois !"
    )

@router.get("/launch30/remaining", response_model=PromoRemainingResponse)
async def get_launch30_remaining():
    """
    Récupère le nombre de places restantes pour l'offre LAUNCH30.
    Utilisé par le counter widget sur la landing page.

    **Returns**:
    ```json
    {
        "remaining": 28,
        "total": 30,
        "percent_filled": 6.7
    }
    ```
    """
    promo = get_promo_code("LAUNCH30")

    if not promo:
        raise HTTPException(status_code=404, detail="Promo code LAUNCH30 not found")

    remaining = promo.max_uses - promo.current_uses
    percent_filled = (promo.current_uses / promo.max_uses) * 100

    return PromoRemainingResponse(
        remaining=remaining,
        total=promo.max_uses,
        percent_filled=round(percent_filled, 1)
    )

@router.post("/signup", response_model=SignupResponse)
async def signup_with_promo(request: SignupRequest):
    """
    Inscription client avec code promo optionnel.

    **Exemple**:
    ```json
    {
        "email": "client@example.com",
        "package": "starter",
        "promo_code": "LAUNCH30"
    }
    ```

    **Packages disponibles**:
    - `starter`: 10,000 DZD/mois → 7,500 DZD (-25% avec LAUNCH30)
    - `dev`: 15,000 DZD/mois → 10,000 DZD (-33% avec LAUNCH30)
    - `business`: 75,000 DZD/mois
    - `premium`: 250,000 DZD/mois
    """
    # Vérifier package
    if request.package.lower() not in _PRICING:
        raise HTTPException(status_code=400, detail=f"Package invalide: {request.package}")

    # Vérifier si email déjà inscrit
    if request.email in _clients:
        raise HTTPException(status_code=400, detail="Email déjà inscrit")

    # Variables
    discount_percent = 0
    discount_until = None
    price_dzd = _PRICING[request.package.lower()]

    # Appliquer promo code si fourni
    if request.promo_code:
        valid, message, promo = validate_promo_code(request.promo_code, request.package)

        if not valid:
            raise HTTPException(status_code=400, detail=message)

        # Calculer réduction
        discount_percent = calculate_discount(request.package, promo)
        price_dzd = _PROMO_PRICING.get(request.package.lower(), price_dzd)
        discount_until = datetime.now() + timedelta(days=promo.duration_months * 30)

        # Incrémenter usage
        increment_promo_usage(request.promo_code)

    # Créer client
    user_id = f"user_{len(_clients) + 1}"
    _clients[request.email] = {
        "user_id": user_id,
        "email": request.email,
        "package": request.package.lower(),
        "price_dzd": price_dzd,
        "promo_code": request.promo_code,
        "discount_percent": discount_percent,
        "discount_until": discount_until,
        "created_at": datetime.now()
    }

    logger.info(f"New signup: {request.email} - Package: {request.package} - Promo: {request.promo_code}")

    return SignupResponse(
        success=True,
        user_id=user_id,
        package=request.package.lower(),
        price_dzd=price_dzd,
        discount_percent=discount_percent,
        discount_until=discount_until,
        message=f"Inscription réussie! Prix: {price_dzd} DZD/mois" +
                (f" (-{discount_percent}% pendant {promo.duration_months} mois)" if request.promo_code else "")
    )

@router.get("/codes", response_model=List[str])
async def list_promo_codes():
    """
    Liste tous les codes promo actifs.
    """
    return [code for code, promo in _promo_codes.items() if promo.is_active]

@router.get("/stats")
async def get_promo_stats():
    """
    Statistiques sur les inscriptions avec promo codes.

    **Returns**:
    ```json
    {
        "total_signups": 12,
        "launch30_used": 12,
        "launch30_remaining": 18,
        "revenue_dzd": 102500,
        "breakdown": {
            "starter": 7,
            "dev": 5
        }
    }
    ```
    """
    total_signups = len(_clients)
    launch30_promo = get_promo_code("LAUNCH30")

    # Breakdown par package
    breakdown = {}
    revenue = 0

    for client in _clients.values():
        pkg = client["package"]
        breakdown[pkg] = breakdown.get(pkg, 0) + 1
        revenue += client["price_dzd"]

    return {
        "total_signups": total_signups,
        "launch30_used": launch30_promo.current_uses if launch30_promo else 0,
        "launch30_remaining": (launch30_promo.max_uses - launch30_promo.current_uses) if launch30_promo else 0,
        "revenue_monthly_dzd": revenue,
        "breakdown": breakdown,
        "clients": list(_clients.keys())  # Pour debug
    }

@router.get("/health")
async def promo_health():
    """Health check pour le système de promo codes"""
    return {
        "status": "healthy",
        "promo_codes_active": len([p for p in _promo_codes.values() if p.is_active]),
        "total_clients": len(_clients)
    }
