"""
IAFactory Video Studio Pro - Credits Service
Gestion complète des crédits et transactions
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import logging
import uuid

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# ============================================
# MODELS
# ============================================

class TransactionType(str, Enum):
    PURCHASE = "purchase"
    GENERATION = "generation"
    VOICE = "voice"
    TEMPLATE = "template"
    REFUND = "refund"
    BONUS = "bonus"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class CreditPack(BaseModel):
    """Pack de crédits."""
    id: str
    name: Dict[str, str]  # {"fr": "...", "ar": "...", "en": "..."}
    credits: int
    price_dzd: int
    price_eur: float
    stripe_price_id: Optional[str] = None
    features: Dict[str, List[str]]  # {"fr": [...], "ar": [...], "en": [...]}
    is_popular: bool = False


class CreditTransaction(BaseModel):
    """Transaction de crédits."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    type: TransactionType
    status: TransactionStatus = TransactionStatus.PENDING
    amount: int
    balance_before: int
    balance_after: int
    description: str
    reference_type: Optional[str] = None
    reference_id: Optional[str] = None
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserCredits(BaseModel):
    """État des crédits d'un utilisateur."""
    user_id: str
    balance: int
    lifetime_total: int
    last_transaction: Optional[CreditTransaction] = None


# ============================================
# CREDIT PACKS
# ============================================

CREDIT_PACKS: Dict[str, CreditPack] = {
    "starter": CreditPack(
        id="starter",
        name={
            "fr": "Starter",
            "ar": "المبتدئ",
            "en": "Starter"
        },
        credits=50,
        price_dzd=990,
        price_eur=5.0,
        features={
            "fr": [
                "50 crédits (~5 vidéos)",
                "Text-to-Video basique",
                "Image-to-Video basique",
                "Export 720p"
            ],
            "ar": [
                "50 رصيد (~5 فيديوهات)",
                "نص إلى فيديو أساسي",
                "صورة إلى فيديو أساسي",
                "تصدير 720p"
            ],
            "en": [
                "50 credits (~5 videos)",
                "Basic Text-to-Video",
                "Basic Image-to-Video",
                "720p Export"
            ]
        }
    ),
    "pro": CreditPack(
        id="pro",
        name={
            "fr": "Pro",
            "ar": "احترافي",
            "en": "Pro"
        },
        credits=200,
        price_dzd=2990,
        price_eur=15.0,
        is_popular=True,
        features={
            "fr": [
                "200 crédits (~20 vidéos)",
                "Tous les modèles IA",
                "Voix Darija incluse",
                "Export 1080p",
                "Support prioritaire"
            ],
            "ar": [
                "200 رصيد (~20 فيديو)",
                "جميع نماذج الذكاء الاصطناعي",
                "صوت الدارجة مضمن",
                "تصدير 1080p",
                "دعم ذو أولوية"
            ],
            "en": [
                "200 credits (~20 videos)",
                "All AI models",
                "Darija voice included",
                "1080p Export",
                "Priority support"
            ]
        }
    ),
    "business": CreditPack(
        id="business",
        name={
            "fr": "Business",
            "ar": "أعمال",
            "en": "Business"
        },
        credits=500,
        price_dzd=5990,
        price_eur=30.0,
        features={
            "fr": [
                "500 crédits (~50 vidéos)",
                "Accès API illimité",
                "Voix personnalisée",
                "Export 4K",
                "Account Manager dédié",
                "Facturation entreprise"
            ],
            "ar": [
                "500 رصيد (~50 فيديو)",
                "وصول API غير محدود",
                "صوت مخصص",
                "تصدير 4K",
                "مدير حساب مخصص",
                "فواتير الشركات"
            ],
            "en": [
                "500 credits (~50 videos)",
                "Unlimited API access",
                "Custom voice",
                "4K Export",
                "Dedicated Account Manager",
                "Enterprise billing"
            ]
        }
    ),
    "enterprise": CreditPack(
        id="enterprise",
        name={
            "fr": "Enterprise",
            "ar": "مؤسسة",
            "en": "Enterprise"
        },
        credits=2000,
        price_dzd=19990,
        price_eur=100.0,
        features={
            "fr": [
                "2000 crédits",
                "Tout inclus + API illimitée",
                "Voix clonées illimitées",
                "Export 4K/8K",
                "Support 24/7",
                "Intégration personnalisée",
                "SLA garanti"
            ],
            "ar": [
                "2000 رصيد",
                "كل شيء مضمن + API غير محدود",
                "أصوات مستنسخة غير محدودة",
                "تصدير 4K/8K",
                "دعم 24/7",
                "تكامل مخصص",
                "SLA مضمون"
            ],
            "en": [
                "2000 credits",
                "All inclusive + Unlimited API",
                "Unlimited cloned voices",
                "4K/8K Export",
                "24/7 Support",
                "Custom integration",
                "Guaranteed SLA"
            ]
        }
    )
}


# ============================================
# COST MATRIX
# ============================================

CREDIT_COSTS = {
    # Video generation
    "video_text_5s": 8,
    "video_text_10s": 15,
    "video_image_5s": 10,
    "video_image_10s": 18,
    
    # Premium models
    "video_kling_1.6": 12,
    "video_runway_gen3": 15,
    "video_minimax": 10,
    "video_wan_2.1": 0,  # Free tier
    "video_cogvideox": 0,  # Free tier
    
    # Image generation
    "image_flux_schnell": 1,
    "image_flux_dev": 2,
    "image_sdxl": 1,
    "image_sd3.5": 2,
    
    # TTS
    "tts_per_100_chars_standard": 1,
    "tts_per_100_chars_darija": 2,
    "tts_per_100_chars_premium": 3,
    
    # Voice cloning
    "voice_clone": 50,
    
    # Templates
    "template_basic": 5,
    "template_premium": 15,
    
    # Pipeline
    "pipeline_short_30s": 20,
    "pipeline_medium_60s": 35,
    "pipeline_long_120s": 60,
    
    # AI Agents
    "agent_script": 5,
    "agent_storyboard": 8,
    "agent_full_workflow": 15,
}


# ============================================
# CREDITS SERVICE
# ============================================

class CreditsService:
    """
    Service de gestion des crédits.
    
    En production, utiliser PostgreSQL + Redis pour le cache.
    """
    
    def __init__(self):
        # In-memory storage (remplacer par DB en prod)
        self._balances: Dict[str, int] = {"demo": 150}
        self._transactions: List[CreditTransaction] = []
        self._lifetime: Dict[str, int] = {"demo": 150}
    
    # ============================================
    # BALANCE OPERATIONS
    # ============================================
    
    def get_balance(self, user_id: str) -> int:
        """Récupère le solde d'un utilisateur."""
        return self._balances.get(user_id, 0)
    
    def get_user_credits(self, user_id: str) -> UserCredits:
        """Récupère l'état complet des crédits."""
        transactions = self.get_transactions(user_id, limit=1)
        
        return UserCredits(
            user_id=user_id,
            balance=self.get_balance(user_id),
            lifetime_total=self._lifetime.get(user_id, 0),
            last_transaction=transactions[0] if transactions else None
        )
    
    def has_enough_credits(self, user_id: str, amount: int) -> bool:
        """Vérifie si l'utilisateur a assez de crédits."""
        return self.get_balance(user_id) >= amount
    
    # ============================================
    # CREDIT OPERATIONS
    # ============================================
    
    def add_credits(
        self,
        user_id: str,
        amount: int,
        transaction_type: TransactionType,
        description: str,
        reference_type: Optional[str] = None,
        reference_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> CreditTransaction:
        """Ajoute des crédits au compte."""
        balance_before = self.get_balance(user_id)
        balance_after = balance_before + amount
        
        # Mettre à jour le solde
        self._balances[user_id] = balance_after
        
        # Mettre à jour le total lifetime
        if amount > 0:
            self._lifetime[user_id] = self._lifetime.get(user_id, 0) + amount
        
        # Créer la transaction
        transaction = CreditTransaction(
            user_id=user_id,
            type=transaction_type,
            status=TransactionStatus.COMPLETED,
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_after,
            description=description,
            reference_type=reference_type,
            reference_id=reference_id,
            metadata=metadata or {}
        )
        
        self._transactions.append(transaction)
        
        logger.info(f"Credits added: user={user_id}, amount={amount}, new_balance={balance_after}")
        
        return transaction
    
    def deduct_credits(
        self,
        user_id: str,
        amount: int,
        transaction_type: TransactionType,
        description: str,
        reference_type: Optional[str] = None,
        reference_id: Optional[str] = None,
        metadata: Optional[Dict] = None,
        check_balance: bool = True
    ) -> CreditTransaction:
        """Déduit des crédits du compte."""
        balance_before = self.get_balance(user_id)
        
        if check_balance and balance_before < amount:
            raise ValueError(f"Insufficient credits: have {balance_before}, need {amount}")
        
        balance_after = max(0, balance_before - amount)
        
        # Mettre à jour le solde
        self._balances[user_id] = balance_after
        
        # Créer la transaction (montant négatif)
        transaction = CreditTransaction(
            user_id=user_id,
            type=transaction_type,
            status=TransactionStatus.COMPLETED,
            amount=-amount,
            balance_before=balance_before,
            balance_after=balance_after,
            description=description,
            reference_type=reference_type,
            reference_id=reference_id,
            metadata=metadata or {}
        )
        
        self._transactions.append(transaction)
        
        logger.info(f"Credits deducted: user={user_id}, amount={amount}, new_balance={balance_after}")
        
        return transaction
    
    def reserve_credits(
        self,
        user_id: str,
        amount: int,
        description: str
    ) -> str:
        """Réserve des crédits (pré-autorisation)."""
        if not self.has_enough_credits(user_id, amount):
            raise ValueError(f"Insufficient credits for reservation")
        
        # Créer une transaction pending
        transaction = CreditTransaction(
            user_id=user_id,
            type=TransactionType.GENERATION,
            status=TransactionStatus.PENDING,
            amount=-amount,
            balance_before=self.get_balance(user_id),
            balance_after=self.get_balance(user_id) - amount,
            description=description,
            metadata={"reservation": True}
        )
        
        # Déduire immédiatement
        self._balances[user_id] = self.get_balance(user_id) - amount
        self._transactions.append(transaction)
        
        return transaction.id
    
    def confirm_reservation(self, reservation_id: str) -> bool:
        """Confirme une réservation de crédits."""
        for tx in self._transactions:
            if tx.id == reservation_id and tx.status == TransactionStatus.PENDING:
                tx.status = TransactionStatus.COMPLETED
                return True
        return False
    
    def cancel_reservation(self, reservation_id: str) -> bool:
        """Annule une réservation et rembourse les crédits."""
        for tx in self._transactions:
            if tx.id == reservation_id and tx.status == TransactionStatus.PENDING:
                # Rembourser
                self._balances[tx.user_id] = self.get_balance(tx.user_id) + abs(tx.amount)
                tx.status = TransactionStatus.FAILED
                tx.metadata["cancelled"] = True
                return True
        return False
    
    # ============================================
    # TRANSACTIONS
    # ============================================
    
    def get_transactions(
        self,
        user_id: str,
        transaction_type: Optional[TransactionType] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[CreditTransaction]:
        """Récupère l'historique des transactions."""
        user_transactions = [
            tx for tx in self._transactions 
            if tx.user_id == user_id
            and (transaction_type is None or tx.type == transaction_type)
        ]
        
        # Trier par date décroissante
        user_transactions.sort(key=lambda x: x.created_at, reverse=True)
        
        return user_transactions[offset:offset + limit]
    
    # ============================================
    # PURCHASES
    # ============================================
    
    def process_purchase(
        self,
        user_id: str,
        pack_id: str,
        payment_reference: Optional[str] = None
    ) -> CreditTransaction:
        """Traite un achat de crédits."""
        pack = CREDIT_PACKS.get(pack_id)
        if not pack:
            raise ValueError(f"Invalid pack ID: {pack_id}")
        
        return self.add_credits(
            user_id=user_id,
            amount=pack.credits,
            transaction_type=TransactionType.PURCHASE,
            description=f"Achat Pack {pack.name['fr']}",
            reference_type="pack",
            reference_id=pack_id,
            metadata={
                "payment_reference": payment_reference,
                "price_dzd": pack.price_dzd,
                "price_eur": pack.price_eur
            }
        )
    
    def apply_bonus(
        self,
        user_id: str,
        amount: int,
        reason: str
    ) -> CreditTransaction:
        """Applique un bonus de crédits."""
        return self.add_credits(
            user_id=user_id,
            amount=amount,
            transaction_type=TransactionType.BONUS,
            description=f"Bonus: {reason}"
        )
    
    def process_refund(
        self,
        transaction_id: str,
        reason: str
    ) -> Optional[CreditTransaction]:
        """Traite un remboursement."""
        # Trouver la transaction originale
        original = None
        for tx in self._transactions:
            if tx.id == transaction_id:
                original = tx
                break
        
        if not original or original.amount >= 0:
            return None
        
        return self.add_credits(
            user_id=original.user_id,
            amount=abs(original.amount),
            transaction_type=TransactionType.REFUND,
            description=f"Remboursement: {reason}",
            reference_type="refund",
            reference_id=transaction_id
        )
    
    # ============================================
    # COST CALCULATION
    # ============================================
    
    def calculate_cost(
        self,
        service: str,
        quantity: float = 1,
        options: Optional[Dict] = None
    ) -> int:
        """Calcule le coût d'un service."""
        base_cost = CREDIT_COSTS.get(service, 0)
        
        if options:
            # Multiplicateurs
            if options.get("premium_model"):
                base_cost = int(base_cost * 1.5)
            if options.get("4k_export"):
                base_cost = int(base_cost * 1.3)
        
        return int(base_cost * quantity)
    
    def estimate_pipeline_cost(
        self,
        duration: int,
        include_voice: bool = True,
        include_music: bool = True,
        model: str = "standard"
    ) -> Dict[str, Any]:
        """Estime le coût d'un pipeline complet."""
        costs = {}
        
        # Coût de base selon durée
        if duration <= 30:
            costs["generation"] = CREDIT_COSTS["pipeline_short_30s"]
        elif duration <= 60:
            costs["generation"] = CREDIT_COSTS["pipeline_medium_60s"]
        else:
            costs["generation"] = CREDIT_COSTS["pipeline_long_120s"]
        
        # AI agents
        costs["ai_agents"] = CREDIT_COSTS["agent_full_workflow"]
        
        # Voice
        if include_voice:
            # Estimation: ~10 chars/second
            chars = duration * 10
            costs["voice"] = (chars // 100) * CREDIT_COSTS["tts_per_100_chars_standard"]
        
        # Music (gratuit)
        if include_music:
            costs["music"] = 0
        
        total = sum(costs.values())
        
        return {
            "breakdown": costs,
            "total": total,
            "duration": duration,
            "estimate": True
        }
    
    # ============================================
    # PACKS
    # ============================================
    
    def get_packs(self, locale: str = "fr") -> List[Dict]:
        """Récupère les packs disponibles."""
        packs = []
        for pack in CREDIT_PACKS.values():
            packs.append({
                "id": pack.id,
                "name": pack.name.get(locale, pack.name["fr"]),
                "credits": pack.credits,
                "price": pack.price_dzd,
                "price_eur": pack.price_eur,
                "features": pack.features.get(locale, pack.features["fr"]),
                "is_popular": pack.is_popular
            })
        return packs


# Instance globale
credits_service = CreditsService()
