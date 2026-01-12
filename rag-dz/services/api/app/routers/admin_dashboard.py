"""
Admin Dashboard - Monitoring temps réel coûts et usage

Métriques:
- Budget quotidien (dépensé vs limite)
- Users actifs
- Coût moyen par user
- Provider stats
- Revenue vs Costs
- Alertes automatiques
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import redis.asyncio as redis
import asyncpg
import logging
import os
from datetime import datetime, timedelta

from app.dependencies import get_current_superuser, get_db_pool
from app.models.user import UserInDB

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])


class BudgetStats(BaseModel):
    """Stats budget quotidien"""
    spent_usd: float
    limit_usd: float
    remaining_usd: float
    percent_used: float
    alert_level: str  # "ok", "warning", "critical"


class UserStats(BaseModel):
    """Stats utilisateurs"""
    active_today: int
    avg_cost_per_user: float
    abusive_count: int
    abusive_users: List[Dict[str, Any]]


class ProviderStats(BaseModel):
    """Stats providers"""
    provider: str
    requests_count: int
    tokens_total: int
    cost_total: float
    avg_latency_ms: float
    error_rate: float


class EconomicsStats(BaseModel):
    """Stats économiques"""
    revenue_usd: float
    costs_usd: float
    profit_usd: float
    margin_percent: float


class Alert(BaseModel):
    """Alerte automatique"""
    level: str  # "info", "warning", "critical"
    message: str
    action: str
    timestamp: datetime


class DashboardResponse(BaseModel):
    """Réponse complète dashboard"""
    date: datetime
    budget: BudgetStats
    users: UserStats
    providers: List[ProviderStats]
    economics: EconomicsStats
    alerts: List[Alert]


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    admin: UserInDB = Depends(get_current_superuser),
    db: asyncpg.Pool = Depends(get_db_pool)
):
    """
    Dashboard admin complet - Monitoring temps réel

    Nécessite:
    - is_superuser = True

    Returns:
        Dashboard complet avec toutes métriques
    """

    redis_client = redis.from_url(
        os.getenv("REDIS_URL", "redis://iafactory-redis:6379/0"),
        decode_responses=True
    )

    try:
        # === BUDGET ===
        budget_spent_today = float(await redis_client.get("budget:today:usd") or 0)
        budget_limit = float(os.getenv("DAILY_BUDGET_USD", "50.0"))
        budget_remaining = max(0, budget_limit - budget_spent_today)
        budget_percent = (budget_spent_today / budget_limit) * 100 if budget_limit > 0 else 0

        # Alert level
        if budget_percent >= 90:
            alert_level = "critical"
        elif budget_percent >= 75:
            alert_level = "warning"
        else:
            alert_level = "ok"

        budget_stats = BudgetStats(
            spent_usd=round(budget_spent_today, 2),
            limit_usd=budget_limit,
            remaining_usd=round(budget_remaining, 2),
            percent_used=round(budget_percent, 1),
            alert_level=alert_level
        )

        # === USERS ===
        # Users actifs aujourd'hui (au moins 1 message)
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        active_users_today = await db.fetchval(
            """
            SELECT COUNT(DISTINCT user_id)
            FROM llm_usage_logs
            WHERE created_at >= $1
            """,
            today_start
        ) or 0

        # Coût moyen par user actif
        avg_cost_per_user = (
            budget_spent_today / active_users_today
            if active_users_today > 0 else 0
        )

        # Users qui abusent (>300 msg/jour)
        abusive_users_data = await db.fetch(
            """
            SELECT
                user_id,
                COUNT(*) as message_count,
                SUM(tokens_input + tokens_output) as total_tokens,
                SUM(cost_usd) as total_cost
            FROM llm_usage_logs
            WHERE created_at >= $1
            GROUP BY user_id
            HAVING COUNT(*) > 300
            ORDER BY COUNT(*) DESC
            LIMIT 10
            """,
            today_start
        )

        abusive_users = [
            {
                "user_id": row["user_id"],
                "message_count": row["message_count"],
                "total_tokens": row["total_tokens"],
                "total_cost": float(row["total_cost"]) if row["total_cost"] else 0
            }
            for row in abusive_users_data
        ]

        user_stats = UserStats(
            active_today=active_users_today,
            avg_cost_per_user=round(avg_cost_per_user, 2),
            abusive_count=len(abusive_users),
            abusive_users=abusive_users
        )

        # === PROVIDERS ===
        providers_data = await db.fetch(
            """
            SELECT
                provider,
                COUNT(*) as requests_count,
                SUM(tokens_input + tokens_output) as tokens_total,
                SUM(cost_usd) as cost_total,
                AVG(EXTRACT(EPOCH FROM (created_at - LAG(created_at) OVER (PARTITION BY user_id ORDER BY created_at)))) * 1000 as avg_latency_ms
            FROM llm_usage_logs
            WHERE created_at >= $1
            GROUP BY provider
            ORDER BY cost_total DESC
            """,
            today_start
        )

        provider_stats_list = []
        for row in providers_data:
            # Calculer error rate (TODO: ajouter colonne error_flag dans logs)
            error_rate = 0.0  # Placeholder

            provider_stats_list.append(
                ProviderStats(
                    provider=row["provider"],
                    requests_count=row["requests_count"],
                    tokens_total=row["tokens_total"] or 0,
                    cost_total=round(float(row["cost_total"]) if row["cost_total"] else 0, 2),
                    avg_latency_ms=round(float(row["avg_latency_ms"]) if row["avg_latency_ms"] else 0, 1),
                    error_rate=error_rate
                )
            )

        # === ECONOMICS ===
        # Revenue aujourd'hui (abonnements payés aujourd'hui)
        revenue_today = await db.fetchval(
            """
            SELECT COALESCE(SUM(
                CASE
                    WHEN tier = 'student' THEN 6.91
                    WHEN tier = 'pro' THEN 11.26
                    ELSE 0
                END
            ), 0)
            FROM user_tiers
            WHERE DATE(subscribed_at) = CURRENT_DATE
            """
        ) or 0.0

        profit_today = revenue_today - budget_spent_today
        margin_percent = (
            (profit_today / revenue_today * 100)
            if revenue_today > 0 else 0
        )

        economics_stats = EconomicsStats(
            revenue_usd=round(revenue_today, 2),
            costs_usd=round(budget_spent_today, 2),
            profit_usd=round(profit_today, 2),
            margin_percent=round(margin_percent, 1)
        )

        # === ALERTES ===
        alerts = []

        # Alerte budget
        if budget_percent >= 90:
            alerts.append(Alert(
                level="critical",
                message=f"Budget quotidien à {budget_percent:.1f}%! Basculement auto sur Groq imminent.",
                action="Augmenter DAILY_BUDGET_USD ou attendre minuit",
                timestamp=datetime.now()
            ))
        elif budget_percent >= 75:
            alerts.append(Alert(
                level="warning",
                message=f"Budget quotidien à {budget_percent:.1f}%. Surveillance recommandée.",
                action="Vérifier usage des users PRO",
                timestamp=datetime.now()
            ))

        # Alerte users abusifs
        if len(abusive_users) > 10:
            alerts.append(Alert(
                level="warning",
                message=f"{len(abusive_users)} users dépassent fair use (300 msg/jour)",
                action="Vérifier si bots ou usage légitime. Envisager soft-ban.",
                timestamp=datetime.now()
            ))

        # Alerte provider errors
        for provider_stat in provider_stats_list:
            if provider_stat.error_rate > 5:
                alerts.append(Alert(
                    level="warning",
                    message=f"{provider_stat.provider} error rate: {provider_stat.error_rate}%",
                    action=f"Vérifier santé API {provider_stat.provider}",
                    timestamp=datetime.now()
                ))

        # Alerte marge négative
        if profit_today < 0:
            alerts.append(Alert(
                level="critical",
                message=f"Marge négative aujourd'hui: ${profit_today:.2f}",
                action="Vérifier pricing ou réduire usage OpenRouter",
                timestamp=datetime.now()
            ))

        # === RESPONSE ===
        return DashboardResponse(
            date=datetime.now(),
            budget=budget_stats,
            users=user_stats,
            providers=provider_stats_list,
            economics=economics_stats,
            alerts=alerts
        )

    finally:
        await redis_client.close()


@router.get("/users/abusive")
async def get_abusive_users(
    admin: UserInDB = Depends(get_current_superuser),
    db: asyncpg.Pool = Depends(get_db_pool),
    threshold: int = 300
):
    """
    Liste les users qui dépassent le fair use

    Args:
        threshold: Nombre de messages au-delà duquel on considère "abusif"

    Returns:
        Liste users avec stats détaillées
    """
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    users = await db.fetch(
        """
        SELECT
            l.user_id,
            u.email,
            ut.tier,
            COUNT(*) as message_count,
            SUM(l.tokens_input + l.tokens_output) as total_tokens,
            SUM(l.cost_usd) as total_cost,
            MIN(l.created_at) as first_message,
            MAX(l.created_at) as last_message
        FROM llm_usage_logs l
        JOIN users u ON u.id = l.user_id
        LEFT JOIN user_tiers ut ON ut.user_id = l.user_id
        WHERE l.created_at >= $1
        GROUP BY l.user_id, u.email, ut.tier
        HAVING COUNT(*) > $2
        ORDER BY COUNT(*) DESC
        """,
        today_start,
        threshold
    )

    return [
        {
            "user_id": row["user_id"],
            "email": row["email"],
            "tier": row["tier"] or "free",
            "message_count": row["message_count"],
            "total_tokens": row["total_tokens"],
            "total_cost": float(row["total_cost"]) if row["total_cost"] else 0,
            "first_message": row["first_message"].isoformat(),
            "last_message": row["last_message"].isoformat(),
            "duration_hours": (row["last_message"] - row["first_message"]).total_seconds() / 3600
        }
        for row in users
    ]


@router.get("/costs/breakdown")
async def get_costs_breakdown(
    admin: UserInDB = Depends(get_current_superuser),
    db: asyncpg.Pool = Depends(get_db_pool),
    days: int = 7
):
    """
    Breakdown coûts sur N derniers jours

    Args:
        days: Nombre de jours (default 7)

    Returns:
        Coûts par jour, par provider, par tier user
    """
    start_date = datetime.now() - timedelta(days=days)

    # Coûts par jour
    by_day = await db.fetch(
        """
        SELECT
            DATE(created_at) as date,
            SUM(cost_usd) as cost,
            COUNT(*) as requests
        FROM llm_usage_logs
        WHERE created_at >= $1
        GROUP BY DATE(created_at)
        ORDER BY date DESC
        """,
        start_date
    )

    # Coûts par provider
    by_provider = await db.fetch(
        """
        SELECT
            provider,
            SUM(cost_usd) as cost,
            COUNT(*) as requests,
            SUM(tokens_input + tokens_output) as tokens
        FROM llm_usage_logs
        WHERE created_at >= $1
        GROUP BY provider
        ORDER BY cost DESC
        """,
        start_date
    )

    # Coûts par tier user
    by_tier = await db.fetch(
        """
        SELECT
            COALESCE(ut.tier, 'free') as tier,
            SUM(l.cost_usd) as cost,
            COUNT(*) as requests
        FROM llm_usage_logs l
        LEFT JOIN user_tiers ut ON ut.user_id = l.user_id
        WHERE l.created_at >= $1
        GROUP BY COALESCE(ut.tier, 'free')
        ORDER BY cost DESC
        """,
        start_date
    )

    return {
        "period_days": days,
        "by_day": [
            {
                "date": row["date"].isoformat(),
                "cost": float(row["cost"]) if row["cost"] else 0,
                "requests": row["requests"]
            }
            for row in by_day
        ],
        "by_provider": [
            {
                "provider": row["provider"],
                "cost": float(row["cost"]) if row["cost"] else 0,
                "requests": row["requests"],
                "tokens": row["tokens"]
            }
            for row in by_provider
        ],
        "by_tier": [
            {
                "tier": row["tier"],
                "cost": float(row["cost"]) if row["cost"] else 0,
                "requests": row["requests"]
            }
            for row in by_tier
        ]
    }


@router.post("/users/{user_id}/soft-ban")
async def soft_ban_user(
    user_id: int,
    duration_hours: int = 24,
    admin: UserInDB = Depends(get_current_superuser)
):
    """
    Soft ban temporaire d'un user abusif

    Args:
        user_id: ID user à bannir
        duration_hours: Durée du ban (default 24h)
    """
    redis_client = redis.from_url(
        os.getenv("REDIS_URL", "redis://iafactory-redis:6379/0")
    )

    try:
        key = f"banned:user:{user_id}"
        await redis_client.setex(key, duration_hours * 3600, "1")

        logger.warning(f"User {user_id} soft-banned by admin {admin.id} for {duration_hours}h")

        return {
            "status": "ok",
            "user_id": user_id,
            "banned_until": (datetime.now() + timedelta(hours=duration_hours)).isoformat()
        }

    finally:
        await redis_client.close()


@router.delete("/users/{user_id}/soft-ban")
async def unban_user(
    user_id: int,
    admin: UserInDB = Depends(get_current_superuser)
):
    """Retirer ban d'un user"""
    redis_client = redis.from_url(
        os.getenv("REDIS_URL", "redis://iafactory-redis:6379/0")
    )

    try:
        key = f"banned:user:{user_id}"
        await redis_client.delete(key)

        logger.info(f"User {user_id} unbanned by admin {admin.id}")

        return {"status": "ok", "user_id": user_id}

    finally:
        await redis_client.close()
