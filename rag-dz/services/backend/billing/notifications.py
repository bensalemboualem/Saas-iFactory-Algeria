"""
IAFactory - Système de Notifications Crédits
=============================================
Alertes consommation, low credits, upgrade suggestions
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import json
import httpx
import asyncio

# ==============================================
# NOTIFICATION TYPES
# ==============================================

class NotificationType(Enum):
    LOW_CREDITS = "low_credits"           # < 10% restants
    CREDITS_EXHAUSTED = "credits_exhausted"  # 0 crédits
    DAILY_LIMIT_REACHED = "daily_limit"   # Limite quotidienne
    USAGE_SPIKE = "usage_spike"           # Usage anormal
    UPGRADE_SUGGESTION = "upgrade"        # Suggestion upgrade
    RENEWAL_REMINDER = "renewal"          # Rappel renouvellement
    NEW_FEATURE = "new_feature"           # Nouvelle fonctionnalité

@dataclass
class Notification:
    type: NotificationType
    user_id: str
    title: Dict[str, str]  # Multilingue
    message: Dict[str, str]
    action_url: Optional[str] = None
    action_text: Optional[Dict[str, str]] = None
    priority: int = 1  # 1=high, 2=medium, 3=low
    created_at: datetime = None
    read: bool = False
    data: Optional[Dict] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()

# ==============================================
# NOTIFICATION TEMPLATES
# ==============================================

TEMPLATES = {
    NotificationType.LOW_CREDITS: {
        "title": {
            "fr": "⚠️ Crédits faibles",
            "ar": "⚠️ رصيد منخفض",
            "en": "⚠️ Low Credits"
        },
        "message": {
            "fr": "Il vous reste {remaining} crédits ({percent}%). Rechargez maintenant pour continuer à utiliser nos services.",
            "ar": "لديك {remaining} رصيد متبقي ({percent}%). اشحن الآن للاستمرار.",
            "en": "You have {remaining} credits remaining ({percent}%). Recharge now to continue using our services."
        },
        "action_url": "/billing/recharge",
        "action_text": {
            "fr": "Recharger maintenant",
            "ar": "اشحن الآن",
            "en": "Recharge Now"
        },
        "priority": 1
    },
    NotificationType.CREDITS_EXHAUSTED: {
        "title": {
            "fr": "🚨 Crédits épuisés",
            "ar": "🚨 نفاد الرصيد",
            "en": "🚨 Credits Exhausted"
        },
        "message": {
            "fr": "Vos crédits sont épuisés. Rechargez ou passez à un plan supérieur pour continuer.",
            "ar": "نفد رصيدك. اشحن أو قم بالترقية للاستمرار.",
            "en": "Your credits are exhausted. Recharge or upgrade to continue."
        },
        "action_url": "/pricing",
        "action_text": {
            "fr": "Voir les plans",
            "ar": "عرض الخطط",
            "en": "View Plans"
        },
        "priority": 1
    },
    NotificationType.DAILY_LIMIT_REACHED: {
        "title": {
            "fr": "📊 Limite quotidienne atteinte",
            "ar": "📊 تم الوصول للحد اليومي",
            "en": "📊 Daily Limit Reached"
        },
        "message": {
            "fr": "Vous avez atteint votre limite de {limit} requêtes/jour. Passez à Pro pour des requêtes illimitées.",
            "ar": "وصلت للحد اليومي {limit} طلبات. ترقية للحصول على طلبات غير محدودة.",
            "en": "You've reached your {limit} queries/day limit. Upgrade to Pro for unlimited queries."
        },
        "action_url": "/pricing?upgrade=pro",
        "action_text": {
            "fr": "Passer à Pro",
            "ar": "الترقية إلى Pro",
            "en": "Upgrade to Pro"
        },
        "priority": 2
    },
    NotificationType.UPGRADE_SUGGESTION: {
        "title": {
            "fr": "💡 Optimisez votre usage",
            "ar": "💡 حسّن استخدامك",
            "en": "💡 Optimize Your Usage"
        },
        "message": {
            "fr": "Basé sur votre usage, le plan {suggested_plan} vous ferait économiser {savings} CHF/mois.",
            "ar": "بناءً على استخدامك، خطة {suggested_plan} ستوفر لك {savings} فرنك/شهر.",
            "en": "Based on your usage, the {suggested_plan} plan would save you {savings} CHF/month."
        },
        "action_url": "/pricing?upgrade={plan_id}",
        "action_text": {
            "fr": "Voir les économies",
            "ar": "عرض التوفير",
            "en": "See Savings"
        },
        "priority": 3
    },
    NotificationType.RENEWAL_REMINDER: {
        "title": {
            "fr": "🔄 Renouvellement proche",
            "ar": "🔄 اقتراب التجديد",
            "en": "🔄 Renewal Coming Up"
        },
        "message": {
            "fr": "Votre abonnement {plan_name} se renouvelle dans {days} jours. {credits_unused} crédits non utilisés.",
            "ar": "اشتراكك {plan_name} يتجدد خلال {days} أيام. {credits_unused} رصيد غير مستخدم.",
            "en": "Your {plan_name} subscription renews in {days} days. {credits_unused} unused credits."
        },
        "action_url": "/account/subscription",
        "action_text": {
            "fr": "Gérer l'abonnement",
            "ar": "إدارة الاشتراك",
            "en": "Manage Subscription"
        },
        "priority": 2
    },
    NotificationType.USAGE_SPIKE: {
        "title": {
            "fr": "📈 Usage élevé détecté",
            "ar": "📈 تم اكتشاف استخدام عالي",
            "en": "📈 High Usage Detected"
        },
        "message": {
            "fr": "Votre usage a augmenté de {increase}% cette semaine. Estimé: {estimated_credits} crédits ce mois.",
            "ar": "زاد استخدامك بنسبة {increase}% هذا الأسبوع. التقدير: {estimated_credits} رصيد هذا الشهر.",
            "en": "Your usage increased by {increase}% this week. Estimated: {estimated_credits} credits this month."
        },
        "action_url": "/dashboard",
        "action_text": {
            "fr": "Voir le dashboard",
            "ar": "عرض لوحة التحكم",
            "en": "View Dashboard"
        },
        "priority": 2
    }
}

# ==============================================
# NOTIFICATION SERVICE
# ==============================================

class NotificationService:
    """Service de gestion des notifications"""

    def __init__(self, redis_client=None, webhook_url: Optional[str] = None):
        self.redis = redis_client
        self.webhook_url = webhook_url
        self.thresholds = {
            "low_credits_percent": 10,  # Alerte à 10%
            "usage_spike_percent": 50,  # Alerte si +50%
            "renewal_days": 7,  # Rappel 7 jours avant
        }

    async def check_and_notify(
        self,
        user_id: str,
        user_data: Dict
    ) -> List[Notification]:
        """
        Vérifie l'état d'un utilisateur et génère les notifications nécessaires

        user_data: {
            "plan_id": str,
            "credits_remaining": int,
            "credits_total": int,
            "daily_queries": int,
            "daily_limit": int | None,
            "renewal_date": datetime,
            "last_week_usage": int,
            "current_week_usage": int
        }
        """
        notifications = []

        # Check low credits
        if user_data.get("credits_total", 0) > 0:
            percent = (user_data["credits_remaining"] / user_data["credits_total"]) * 100

            if user_data["credits_remaining"] == 0:
                notifications.append(
                    self._create_notification(
                        NotificationType.CREDITS_EXHAUSTED,
                        user_id,
                        {}
                    )
                )
            elif percent <= self.thresholds["low_credits_percent"]:
                notifications.append(
                    self._create_notification(
                        NotificationType.LOW_CREDITS,
                        user_id,
                        {
                            "remaining": user_data["credits_remaining"],
                            "percent": round(percent, 1)
                        }
                    )
                )

        # Check daily limit
        daily_limit = user_data.get("daily_limit")
        if daily_limit and user_data.get("daily_queries", 0) >= daily_limit:
            notifications.append(
                self._create_notification(
                    NotificationType.DAILY_LIMIT_REACHED,
                    user_id,
                    {"limit": daily_limit}
                )
            )

        # Check usage spike
        last_week = user_data.get("last_week_usage", 0)
        current_week = user_data.get("current_week_usage", 0)
        if last_week > 0:
            increase = ((current_week - last_week) / last_week) * 100
            if increase >= self.thresholds["usage_spike_percent"]:
                estimated = current_week * 4  # Projection mensuelle
                notifications.append(
                    self._create_notification(
                        NotificationType.USAGE_SPIKE,
                        user_id,
                        {
                            "increase": round(increase, 0),
                            "estimated_credits": estimated
                        }
                    )
                )

        # Check renewal
        renewal_date = user_data.get("renewal_date")
        if renewal_date:
            days_until = (renewal_date - datetime.utcnow()).days
            if 0 < days_until <= self.thresholds["renewal_days"]:
                notifications.append(
                    self._create_notification(
                        NotificationType.RENEWAL_REMINDER,
                        user_id,
                        {
                            "plan_name": user_data.get("plan_id", "").replace("_", " ").title(),
                            "days": days_until,
                            "credits_unused": user_data.get("credits_remaining", 0)
                        }
                    )
                )

        # Send notifications
        for notif in notifications:
            await self._send_notification(notif)

        return notifications

    def _create_notification(
        self,
        notif_type: NotificationType,
        user_id: str,
        params: Dict
    ) -> Notification:
        """Crée une notification à partir d'un template"""
        template = TEMPLATES.get(notif_type, {})

        # Format messages with params
        title = {
            lang: text for lang, text in template.get("title", {}).items()
        }
        message = {
            lang: text.format(**params)
            for lang, text in template.get("message", {}).items()
        }
        action_url = template.get("action_url", "").format(**params)

        return Notification(
            type=notif_type,
            user_id=user_id,
            title=title,
            message=message,
            action_url=action_url,
            action_text=template.get("action_text"),
            priority=template.get("priority", 2),
            data=params
        )

    async def _send_notification(self, notification: Notification):
        """Envoie une notification via différents canaux"""

        # Store in Redis for in-app notifications
        if self.redis:
            key = f"notifications:{notification.user_id}"
            await self.redis.lpush(key, json.dumps({
                "type": notification.type.value,
                "title": notification.title,
                "message": notification.message,
                "action_url": notification.action_url,
                "action_text": notification.action_text,
                "priority": notification.priority,
                "created_at": notification.created_at.isoformat(),
                "read": False,
                "data": notification.data
            }))
            # Keep only last 50 notifications
            await self.redis.ltrim(key, 0, 49)

        # Send webhook for critical notifications
        if self.webhook_url and notification.priority == 1:
            async with httpx.AsyncClient() as client:
                try:
                    await client.post(
                        self.webhook_url,
                        json={
                            "user_id": notification.user_id,
                            "type": notification.type.value,
                            "title": notification.title.get("fr"),
                            "message": notification.message.get("fr"),
                            "priority": "high"
                        },
                        timeout=5.0
                    )
                except Exception as e:
                    print(f"Webhook error: {e}")

    async def get_user_notifications(
        self,
        user_id: str,
        lang: str = "fr",
        limit: int = 20
    ) -> List[Dict]:
        """Récupère les notifications d'un utilisateur"""
        if not self.redis:
            return []

        key = f"notifications:{user_id}"
        raw_notifications = await self.redis.lrange(key, 0, limit - 1)

        notifications = []
        for raw in raw_notifications:
            notif = json.loads(raw)
            notifications.append({
                "type": notif["type"],
                "title": notif["title"].get(lang, notif["title"].get("fr")),
                "message": notif["message"].get(lang, notif["message"].get("fr")),
                "action_url": notif["action_url"],
                "action_text": notif["action_text"].get(lang) if notif["action_text"] else None,
                "priority": notif["priority"],
                "created_at": notif["created_at"],
                "read": notif["read"],
                "data": notif.get("data")
            })

        return notifications

    async def mark_as_read(self, user_id: str, notification_index: int):
        """Marque une notification comme lue"""
        if not self.redis:
            return

        key = f"notifications:{user_id}"
        raw = await self.redis.lindex(key, notification_index)
        if raw:
            notif = json.loads(raw)
            notif["read"] = True
            await self.redis.lset(key, notification_index, json.dumps(notif))


# ==============================================
# FASTAPI ENDPOINTS
# ==============================================

def create_notification_routes(app, notification_service: NotificationService):
    """Crée les routes FastAPI pour les notifications"""

    from fastapi import APIRouter, Query
    router = APIRouter(prefix="/api/notifications", tags=["notifications"])

    @router.get("/")
    async def get_notifications(
        user_id: str = Query(...),
        lang: str = Query("fr"),
        limit: int = Query(20, le=50)
    ):
        notifications = await notification_service.get_user_notifications(
            user_id, lang, limit
        )
        return {"notifications": notifications, "count": len(notifications)}

    @router.post("/{index}/read")
    async def mark_read(
        user_id: str = Query(...),
        index: int = 0
    ):
        await notification_service.mark_as_read(user_id, index)
        return {"status": "ok"}

    @router.get("/unread-count")
    async def unread_count(user_id: str = Query(...)):
        notifications = await notification_service.get_user_notifications(user_id)
        unread = sum(1 for n in notifications if not n.get("read"))
        return {"unread": unread}

    app.include_router(router)


# ==============================================
# TEST
# ==============================================

if __name__ == "__main__":
    print("=" * 60)
    print("NOTIFICATION SYSTEM TEST")
    print("=" * 60)

    service = NotificationService()

    # Test user data scenarios
    test_cases = [
        {
            "name": "Low credits (8%)",
            "data": {
                "plan_id": "dz_pro",
                "credits_remaining": 80,
                "credits_total": 1000,
                "daily_queries": 10,
                "daily_limit": None
            }
        },
        {
            "name": "Credits exhausted",
            "data": {
                "plan_id": "dz_starter",
                "credits_remaining": 0,
                "credits_total": 100,
                "daily_queries": 5,
                "daily_limit": 5
            }
        },
        {
            "name": "Daily limit reached",
            "data": {
                "plan_id": "dz_starter",
                "credits_remaining": 50,
                "credits_total": 100,
                "daily_queries": 5,
                "daily_limit": 5
            }
        },
        {
            "name": "Usage spike",
            "data": {
                "plan_id": "dz_business",
                "credits_remaining": 3000,
                "credits_total": 5000,
                "last_week_usage": 200,
                "current_week_usage": 400
            }
        }
    ]

    async def run_tests():
        for i, case in enumerate(test_cases):
            print(f"\n--- Test {i+1}: {case['name']} ---")
            notifications = await service.check_and_notify(
                f"test_user_{i}",
                case["data"]
            )
            for notif in notifications:
                print(f"  📬 {notif.title['fr']}")
                print(f"     {notif.message['fr']}")
                print(f"     Action: {notif.action_text['fr'] if notif.action_text else 'N/A'}")

    asyncio.run(run_tests())
