"""
Chargily Payment Integration pour IA Factory Algérie.
Chargily est le SEUL provider de paiement autorisé (pas Stripe).
"""

import os
import hmac
import hashlib
from typing import Any
from datetime import datetime
from enum import Enum

import httpx
from pydantic import BaseModel, Field, EmailStr


class PaymentMode(str, Enum):
    """Modes de paiement Chargily"""
    CIB = "cib"           # Carte CIB (Algérie)
    EDAHABIA = "edahabia" # Carte EDAHABIA (Algérie Poste)


class PaymentStatus(str, Enum):
    """Statuts de paiement"""
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    CANCELED = "canceled"
    EXPIRED = "expired"


class ChargilyPayment(BaseModel):
    """Requête de paiement Chargily"""
    amount: int  # En centimes DZD (ex: 10000 = 100.00 DZD)
    currency: str = "DZD"
    client_name: str
    client_email: EmailStr
    client_phone: str | None = None
    description: str
    webhook_url: str
    back_url: str | None = None
    metadata: dict = Field(default_factory=dict)
    locale: str = "fr"  # fr, ar, en


class ChargilyCheckout(BaseModel):
    """Réponse checkout Chargily"""
    id: str
    entity: str = "checkout"
    status: PaymentStatus
    amount: int
    currency: str
    checkout_url: str
    success_url: str | None = None
    failure_url: str | None = None
    webhook_endpoint: str | None = None
    payment_method: PaymentMode | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ChargilyWebhookPayload(BaseModel):
    """Payload du webhook Chargily"""
    id: str
    entity: str
    livemode: bool
    type: str  # checkout.paid, checkout.failed, etc.
    data: dict


class ChargilyService:
    """
    Service d'intégration Chargily pour les paiements en Algérie.
    Supporte CIB et EDAHABIA uniquement.

    Usage:
        service = ChargilyService()
        checkout = await service.create_checkout(payment)
        # Rediriger vers checkout.checkout_url
    """

    BASE_URL = "https://pay.chargily.net/api/v2"

    def __init__(
        self,
        api_key: str | None = None,
        secret_key: str | None = None,
        webhook_secret: str | None = None
    ):
        """
        Initialise le service Chargily.

        Args:
            api_key: Clé API Chargily (ou CHARGILY_API_KEY env)
            secret_key: Clé secrète Chargily (ou CHARGILY_SECRET_KEY env)
            webhook_secret: Secret pour vérification webhooks (ou CHARGILY_WEBHOOK_SECRET env)
        """
        self.api_key = api_key or os.getenv("CHARGILY_API_KEY")
        self.secret_key = secret_key or os.getenv("CHARGILY_SECRET_KEY")
        self.webhook_secret = webhook_secret or os.getenv("CHARGILY_WEBHOOK_SECRET")

        if not self.api_key:
            raise ValueError("CHARGILY_API_KEY is required")

        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            timeout=30.0
        )

    async def close(self):
        """Ferme le client HTTP"""
        await self.client.aclose()

    # ============ CHECKOUT ============

    async def create_checkout(self, payment: ChargilyPayment) -> ChargilyCheckout:
        """
        Crée une session de paiement (checkout).

        Args:
            payment: Détails du paiement

        Returns:
            ChargilyCheckout avec l'URL de paiement
        """
        payload = {
            "amount": payment.amount,
            "currency": payment.currency,
            "description": payment.description,
            "webhook_endpoint": payment.webhook_url,
            "locale": payment.locale,
            "metadata": {
                "client_name": payment.client_name,
                "client_email": payment.client_email,
                **payment.metadata
            }
        }

        if payment.back_url:
            payload["success_url"] = payment.back_url
            payload["failure_url"] = payment.back_url

        if payment.client_phone:
            payload["metadata"]["client_phone"] = payment.client_phone

        response = await self.client.post("/checkouts", json=payload)
        response.raise_for_status()

        data = response.json()
        return ChargilyCheckout(**data)

    async def get_checkout(self, checkout_id: str) -> ChargilyCheckout:
        """
        Récupère les détails d'un checkout.

        Args:
            checkout_id: ID du checkout

        Returns:
            ChargilyCheckout
        """
        response = await self.client.get(f"/checkouts/{checkout_id}")
        response.raise_for_status()
        return ChargilyCheckout(**response.json())

    async def list_checkouts(
        self,
        page: int = 1,
        per_page: int = 10
    ) -> list[ChargilyCheckout]:
        """
        Liste les checkouts.

        Args:
            page: Numéro de page
            per_page: Nombre par page

        Returns:
            Liste de ChargilyCheckout
        """
        response = await self.client.get(
            "/checkouts",
            params={"page": page, "per_page": per_page}
        )
        response.raise_for_status()
        data = response.json()
        return [ChargilyCheckout(**item) for item in data.get("data", [])]

    # ============ PAYMENTS ============

    async def get_payment(self, payment_id: str) -> dict:
        """
        Récupère les détails d'un paiement.

        Args:
            payment_id: ID du paiement

        Returns:
            Détails du paiement
        """
        response = await self.client.get(f"/payments/{payment_id}")
        response.raise_for_status()
        return response.json()

    async def list_payments(
        self,
        page: int = 1,
        per_page: int = 10,
        status: PaymentStatus | None = None
    ) -> list[dict]:
        """
        Liste les paiements.

        Args:
            page: Numéro de page
            per_page: Nombre par page
            status: Filtrer par statut

        Returns:
            Liste des paiements
        """
        params = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status.value

        response = await self.client.get("/payments", params=params)
        response.raise_for_status()
        return response.json().get("data", [])

    # ============ WEBHOOK VERIFICATION ============

    def verify_webhook(self, signature: str, payload: bytes) -> bool:
        """
        Vérifie la signature d'un webhook Chargily.

        Args:
            signature: Header X-Chargily-Signature
            payload: Corps de la requête (bytes)

        Returns:
            True si la signature est valide
        """
        if not self.webhook_secret:
            raise ValueError("CHARGILY_WEBHOOK_SECRET is required for webhook verification")

        expected = hmac.new(
            self.webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected)

    def parse_webhook(self, payload: bytes) -> ChargilyWebhookPayload:
        """
        Parse le payload d'un webhook.

        Args:
            payload: Corps de la requête

        Returns:
            ChargilyWebhookPayload
        """
        import json
        data = json.loads(payload)
        return ChargilyWebhookPayload(**data)

    # ============ UTILITY METHODS ============

    @staticmethod
    def dzd_to_centimes(amount: float) -> int:
        """
        Convertit DZD en centimes.

        Args:
            amount: Montant en DZD (ex: 100.50)

        Returns:
            Montant en centimes (ex: 10050)
        """
        return int(amount * 100)

    @staticmethod
    def centimes_to_dzd(centimes: int) -> float:
        """
        Convertit centimes en DZD.

        Args:
            centimes: Montant en centimes

        Returns:
            Montant en DZD
        """
        return centimes / 100

    async def health(self) -> dict:
        """
        Vérifie la connexion à Chargily.

        Returns:
            Status de santé
        """
        try:
            response = await self.client.get("/balance")
            if response.status_code == 200:
                return {"status": "healthy", "connected": True}
            return {"status": "unhealthy", "connected": False}
        except Exception as e:
            return {"status": "error", "error": str(e)}


# ============ CREDIT PACKS ============

CREDIT_PACKS = [
    {
        "id": "pack_starter",
        "name": "Pack Starter",
        "credits": 100,
        "price_dzd": 500,  # 500 DZD
        "price_centimes": 50000
    },
    {
        "id": "pack_pro",
        "name": "Pack Pro",
        "credits": 500,
        "price_dzd": 2000,  # 2000 DZD
        "price_centimes": 200000
    },
    {
        "id": "pack_business",
        "name": "Pack Business",
        "credits": 2000,
        "price_dzd": 6000,  # 6000 DZD
        "price_centimes": 600000
    },
    {
        "id": "pack_enterprise",
        "name": "Pack Enterprise",
        "credits": 10000,
        "price_dzd": 25000,  # 25000 DZD
        "price_centimes": 2500000
    }
]


def get_credit_pack(pack_id: str) -> dict | None:
    """Récupère un pack de crédits par ID"""
    return next((p for p in CREDIT_PACKS if p["id"] == pack_id), None)
