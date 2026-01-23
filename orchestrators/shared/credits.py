"""
Credit System for IA Factory Algérie.
Gère les crédits utilisateur pour les opérations AI.
"""

import os
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class CreditOperation(str, Enum):
    """Types d'opérations consommant des crédits"""
    # Chat
    CHAT_MESSAGE = "chat_message"
    CHAT_WITH_RAG = "chat_with_rag"

    # Génération de code
    CODE_GENERATION = "code_generation"
    CODE_EDIT = "code_edit"
    CODE_REVIEW = "code_review"

    # Génération d'images
    IMAGE_GENERATION = "image_generation"
    IMAGE_EDIT = "image_edit"

    # Génération de vidéos
    VIDEO_GENERATION = "video_generation"
    VIDEO_EDIT = "video_edit"

    # Agents GOV
    GOV_AGENT_CNAS = "gov_agent_cnas"
    GOV_AGENT_CNRC = "gov_agent_cnrc"
    GOV_AGENT_DGI = "gov_agent_dgi"
    GOV_AGENT_SONELGAZ = "gov_agent_sonelgaz"

    # Documents
    DOCUMENT_ANALYSIS = "document_analysis"
    DOCUMENT_OCR = "document_ocr"
    DOCUMENT_TRANSLATION = "document_translation"

    # Voix
    VOICE_TO_TEXT = "voice_to_text"
    TEXT_TO_VOICE = "text_to_voice"

    # Recherche
    WEB_SEARCH = "web_search"
    DEEP_RESEARCH = "deep_research"


class CreditTransaction(BaseModel):
    """Transaction de crédits"""
    id: str
    user_id: str
    operation: CreditOperation | str
    amount: int  # Positif = débit, négatif = crédit
    balance_before: int
    balance_after: int
    description: str | None = None
    metadata: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CreditBalance(BaseModel):
    """Solde de crédits d'un utilisateur"""
    user_id: str
    balance: int
    tier: str = "free"  # free, starter, pro, business, enterprise
    monthly_limit: int = 100
    monthly_used: int = 0
    last_reset: datetime | None = None


# ============ TARIFICATION PAR OPÉRATION ============

CREDIT_RATES: dict[str, int] = {
    # Chat - opérations légères
    CreditOperation.CHAT_MESSAGE.value: 1,
    CreditOperation.CHAT_WITH_RAG.value: 2,

    # Code - opérations moyennes
    CreditOperation.CODE_GENERATION.value: 5,
    CreditOperation.CODE_EDIT.value: 3,
    CreditOperation.CODE_REVIEW.value: 2,

    # Images - opérations coûteuses
    CreditOperation.IMAGE_GENERATION.value: 20,
    CreditOperation.IMAGE_EDIT.value: 10,

    # Vidéos - opérations très coûteuses
    CreditOperation.VIDEO_GENERATION.value: 100,
    CreditOperation.VIDEO_EDIT.value: 50,

    # Agents GOV - opérations moyennes (automation browser)
    CreditOperation.GOV_AGENT_CNAS.value: 3,
    CreditOperation.GOV_AGENT_CNRC.value: 3,
    CreditOperation.GOV_AGENT_DGI.value: 3,
    CreditOperation.GOV_AGENT_SONELGAZ.value: 3,

    # Documents
    CreditOperation.DOCUMENT_ANALYSIS.value: 5,
    CreditOperation.DOCUMENT_OCR.value: 2,
    CreditOperation.DOCUMENT_TRANSLATION.value: 3,

    # Voix
    CreditOperation.VOICE_TO_TEXT.value: 2,
    CreditOperation.TEXT_TO_VOICE.value: 3,

    # Recherche
    CreditOperation.WEB_SEARCH.value: 1,
    CreditOperation.DEEP_RESEARCH.value: 10,
}

# ============ TIERS ET LIMITES ============

TIER_LIMITS = {
    "free": {
        "monthly_credits": 100,
        "max_balance": 100,
        "features": ["chat", "code_basic"]
    },
    "starter": {
        "monthly_credits": 500,
        "max_balance": 1000,
        "features": ["chat", "code", "rag", "gov_agents"]
    },
    "pro": {
        "monthly_credits": 2000,
        "max_balance": 5000,
        "features": ["chat", "code", "rag", "gov_agents", "images", "voice"]
    },
    "business": {
        "monthly_credits": 10000,
        "max_balance": 20000,
        "features": ["all"]
    },
    "enterprise": {
        "monthly_credits": -1,  # Illimité
        "max_balance": -1,
        "features": ["all", "priority", "custom_models"]
    }
}


class CreditSystem:
    """
    Système de gestion des crédits.
    Intègre avec Supabase pour la persistance.
    """

    def __init__(
        self,
        supabase_url: str | None = None,
        supabase_key: str | None = None
    ):
        """
        Initialize the credit system.

        Args:
            supabase_url: URL Supabase
            supabase_key: Clé Supabase
        """
        self.supabase_url = supabase_url or os.getenv("SUPABASE_URL")
        self.supabase_key = supabase_key or os.getenv("SUPABASE_SERVICE_KEY")
        self._client = None

    async def _get_client(self):
        """Get or create Supabase client"""
        if self._client is None:
            try:
                from supabase import create_client
                self._client = create_client(self.supabase_url, self.supabase_key)
            except ImportError:
                raise RuntimeError("Supabase client not installed")
        return self._client

    def get_rate(self, operation: CreditOperation | str) -> int:
        """
        Récupère le coût d'une opération.

        Args:
            operation: Type d'opération

        Returns:
            Coût en crédits
        """
        op_value = operation.value if isinstance(operation, CreditOperation) else operation
        return CREDIT_RATES.get(op_value, 1)

    async def check_balance(self, user_id: str) -> int:
        """
        Vérifie le solde de crédits.

        Args:
            user_id: ID utilisateur

        Returns:
            Solde actuel
        """
        client = await self._get_client()

        response = client.table("user_credits").select("balance").eq("user_id", user_id).single().execute()

        if response.data:
            return response.data.get("balance", 0)

        # Créer un compte avec crédits initiaux pour nouvel utilisateur
        await self._create_user_credits(user_id)
        return TIER_LIMITS["free"]["monthly_credits"]

    async def _create_user_credits(self, user_id: str, tier: str = "free"):
        """Crée un compte crédits pour un nouvel utilisateur"""
        client = await self._get_client()

        initial_credits = TIER_LIMITS[tier]["monthly_credits"]

        client.table("user_credits").insert({
            "user_id": user_id,
            "balance": initial_credits,
            "tier": tier,
            "monthly_limit": initial_credits,
            "monthly_used": 0,
            "last_reset": datetime.utcnow().isoformat()
        }).execute()

    async def get_balance_info(self, user_id: str) -> CreditBalance:
        """
        Récupère les informations complètes du solde.

        Args:
            user_id: ID utilisateur

        Returns:
            CreditBalance
        """
        client = await self._get_client()

        response = client.table("user_credits").select("*").eq("user_id", user_id).single().execute()

        if response.data:
            return CreditBalance(**response.data)

        # Créer un compte pour nouvel utilisateur
        await self._create_user_credits(user_id)
        return CreditBalance(
            user_id=user_id,
            balance=TIER_LIMITS["free"]["monthly_credits"],
            tier="free",
            monthly_limit=TIER_LIMITS["free"]["monthly_credits"]
        )

    async def can_afford(
        self,
        user_id: str,
        operation: CreditOperation | str,
        amount: int | None = None
    ) -> bool:
        """
        Vérifie si l'utilisateur peut effectuer une opération.

        Args:
            user_id: ID utilisateur
            operation: Type d'opération
            amount: Montant custom (optionnel)

        Returns:
            True si l'utilisateur a assez de crédits
        """
        cost = amount or self.get_rate(operation)
        balance = await self.check_balance(user_id)
        return balance >= cost

    async def deduct(
        self,
        user_id: str,
        operation: CreditOperation | str,
        amount: int | None = None,
        description: str | None = None,
        metadata: dict | None = None
    ) -> CreditTransaction | None:
        """
        Déduit des crédits pour une opération.

        Args:
            user_id: ID utilisateur
            operation: Type d'opération
            amount: Montant custom (optionnel)
            description: Description de l'opération
            metadata: Métadonnées additionnelles

        Returns:
            CreditTransaction ou None si échec
        """
        client = await self._get_client()
        cost = amount or self.get_rate(operation)

        # Récupérer le solde actuel
        balance_info = await self.get_balance_info(user_id)

        if balance_info.balance < cost:
            return None  # Pas assez de crédits

        new_balance = balance_info.balance - cost

        # Mettre à jour le solde
        client.table("user_credits").update({
            "balance": new_balance,
            "monthly_used": balance_info.monthly_used + cost,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("user_id", user_id).execute()

        # Créer la transaction
        import uuid
        transaction = CreditTransaction(
            id=str(uuid.uuid4()),
            user_id=user_id,
            operation=operation.value if isinstance(operation, CreditOperation) else operation,
            amount=cost,
            balance_before=balance_info.balance,
            balance_after=new_balance,
            description=description,
            metadata=metadata or {}
        )

        # Logger la transaction
        client.table("credit_transactions").insert({
            "id": transaction.id,
            "user_id": transaction.user_id,
            "operation": transaction.operation,
            "amount": transaction.amount,
            "balance_before": transaction.balance_before,
            "balance_after": transaction.balance_after,
            "description": transaction.description,
            "metadata": transaction.metadata,
            "created_at": transaction.created_at.isoformat()
        }).execute()

        return transaction

    async def add_credits(
        self,
        user_id: str,
        amount: int,
        source: str,
        reference: str | None = None,
        metadata: dict | None = None
    ) -> CreditTransaction:
        """
        Ajoute des crédits (achat, bonus, etc.).

        Args:
            user_id: ID utilisateur
            amount: Montant à ajouter
            source: Source (chargily, bonus, promo, etc.)
            reference: Référence (ID paiement, code promo, etc.)
            metadata: Métadonnées

        Returns:
            CreditTransaction
        """
        client = await self._get_client()

        balance_info = await self.get_balance_info(user_id)
        new_balance = balance_info.balance + amount

        # Vérifier le plafond
        max_balance = TIER_LIMITS[balance_info.tier]["max_balance"]
        if max_balance > 0 and new_balance > max_balance:
            new_balance = max_balance

        # Mettre à jour le solde
        client.table("user_credits").update({
            "balance": new_balance,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("user_id", user_id).execute()

        # Créer la transaction (montant négatif = crédit)
        import uuid
        transaction = CreditTransaction(
            id=str(uuid.uuid4()),
            user_id=user_id,
            operation=f"add_{source}",
            amount=-amount,
            balance_before=balance_info.balance,
            balance_after=new_balance,
            description=f"Ajout de {amount} crédits via {source}",
            metadata={
                "source": source,
                "reference": reference,
                **(metadata or {})
            }
        )

        client.table("credit_transactions").insert({
            "id": transaction.id,
            "user_id": transaction.user_id,
            "operation": transaction.operation,
            "amount": transaction.amount,
            "balance_before": transaction.balance_before,
            "balance_after": transaction.balance_after,
            "description": transaction.description,
            "metadata": transaction.metadata,
            "created_at": transaction.created_at.isoformat()
        }).execute()

        return transaction

    async def process_chargily_webhook(
        self,
        user_id: str,
        pack_id: str,
        payment_id: str
    ) -> CreditTransaction:
        """
        Traite un webhook Chargily pour ajouter des crédits.

        Args:
            user_id: ID utilisateur
            pack_id: ID du pack acheté
            payment_id: ID du paiement Chargily

        Returns:
            CreditTransaction
        """
        from .chargily import get_credit_pack

        pack = get_credit_pack(pack_id)
        if not pack:
            raise ValueError(f"Pack not found: {pack_id}")

        return await self.add_credits(
            user_id=user_id,
            amount=pack["credits"],
            source="chargily",
            reference=payment_id,
            metadata={
                "pack_id": pack_id,
                "pack_name": pack["name"],
                "price_dzd": pack["price_dzd"]
            }
        )

    async def get_transactions(
        self,
        user_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> list[CreditTransaction]:
        """
        Récupère l'historique des transactions.

        Args:
            user_id: ID utilisateur
            limit: Nombre max de transactions
            offset: Offset pour pagination

        Returns:
            Liste de CreditTransaction
        """
        client = await self._get_client()

        response = client.table("credit_transactions") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .range(offset, offset + limit - 1) \
            .execute()

        return [CreditTransaction(**t) for t in response.data]

    async def upgrade_tier(self, user_id: str, new_tier: str) -> CreditBalance:
        """
        Upgrade le tier d'un utilisateur.

        Args:
            user_id: ID utilisateur
            new_tier: Nouveau tier

        Returns:
            CreditBalance mis à jour
        """
        if new_tier not in TIER_LIMITS:
            raise ValueError(f"Invalid tier: {new_tier}")

        client = await self._get_client()
        tier_info = TIER_LIMITS[new_tier]

        client.table("user_credits").update({
            "tier": new_tier,
            "monthly_limit": tier_info["monthly_credits"],
            "updated_at": datetime.utcnow().isoformat()
        }).eq("user_id", user_id).execute()

        return await self.get_balance_info(user_id)

    async def reset_monthly_credits(self, user_id: str) -> CreditBalance:
        """
        Réinitialise les crédits mensuels.

        Args:
            user_id: ID utilisateur

        Returns:
            CreditBalance mis à jour
        """
        client = await self._get_client()
        balance_info = await self.get_balance_info(user_id)
        tier_info = TIER_LIMITS[balance_info.tier]

        monthly_credits = tier_info["monthly_credits"]

        client.table("user_credits").update({
            "balance": monthly_credits,
            "monthly_used": 0,
            "last_reset": datetime.utcnow().isoformat()
        }).eq("user_id", user_id).execute()

        return await self.get_balance_info(user_id)


# Singleton instance
_credit_system: CreditSystem | None = None


def get_credit_system() -> CreditSystem:
    """Get or create the credit system singleton"""
    global _credit_system
    if _credit_system is None:
        _credit_system = CreditSystem()
    return _credit_system
