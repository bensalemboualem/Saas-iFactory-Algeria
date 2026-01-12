"""
Modèle pour la gestion des clés API revendues (Key Reselling)
Collection Firestore: user_keys
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from enum import Enum


class KeyStatus(str, Enum):
    NEW = "NEW"  # Clé créée mais non attribuée
    ACTIVE = "ACTIVE"
    DEPLETED = "DEPLETED"
    EXPIRED = "EXPIRED"


class UserKey(BaseModel):
    """Modèle Firestore pour les clés API utilisateur"""
    key_code: str = Field(..., description="Code unique vendu à l'utilisateur (ex: GROQ-XYZ-123)")
    provider: str = Field(..., description="Fournisseur API (ex: Groq, OpenRouter)")
    user_id: Optional[str] = Field(default=None, description="ID de l'utilisateur propriétaire (None si non attribuée)")
    balance_usd: float = Field(..., ge=0, description="Solde initial en USD")
    current_usage: float = Field(default=0.0, ge=0, description="Consommation actuelle en USD")
    status: KeyStatus = Field(default=KeyStatus.NEW, description="Statut de la clé")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    activated_at: Optional[datetime] = Field(default=None, description="Date de première activation")

    @property
    def remaining_balance(self) -> float:
        """Solde restant"""
        return max(0, self.balance_usd - self.current_usage)

    @property
    def is_valid(self) -> bool:
        """Vérifie si la clé est utilisable"""
        if self.status != KeyStatus.ACTIVE:
            return False
        if self.remaining_balance <= 0:
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return True


class KeyValidateRequest(BaseModel):
    key_code: str
    user_id: Optional[str] = Field(default=None, description="ID utilisateur pour attribution automatique")


class KeyValidateResponse(BaseModel):
    valid: bool
    provider: Optional[str] = None
    remaining_balance: Optional[float] = None
    status: Optional[str] = None
    message: str


class KeyDebitRequest(BaseModel):
    key_code: str
    amount_usd: float = Field(..., gt=0, description="Montant à débiter en USD")
    description: Optional[str] = None


class KeyDebitResponse(BaseModel):
    success: bool
    new_balance: float
    message: str


class KeyCreateRequest(BaseModel):
    provider: str
    user_id: str
    balance_usd: float = Field(..., gt=0)
    expires_days: Optional[int] = Field(default=365, description="Durée de validité en jours")


class KeyBalanceResponse(BaseModel):
    key_code: str
    provider: str
    balance_usd: float
    current_usage: float
    remaining_balance: float
    status: str
    expires_at: Optional[datetime] = None
