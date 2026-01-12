"""
iaFactory API Portal - Usage & Logs
Module 16 - Statistiques d'utilisation et logs API
"""

from datetime import datetime, timedelta
from typing import Optional, List, Literal
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..auth import get_current_user
from ..models import User, ApiKey, ApiLog, UsageEvent, UserCredits

router = APIRouter(prefix="/api/dev", tags=["Developer - Usage & Logs"])


# ==============================================
# SCHEMAS
# ==============================================

class EndpointUsage(BaseModel):
    """Usage par endpoint"""
    endpoint: str
    count: int
    avg_latency_ms: float
    error_count: int


class TimeseriesPoint(BaseModel):
    """Point de données temporelles"""
    date: str
    count: int
    errors: int = 0
    avg_latency_ms: float = 0


class UsageStats(BaseModel):
    """Statistiques d'usage agrégées"""
    range: str
    total_requests: int
    avg_requests_per_day: float
    error_rate: float
    avg_latency_ms: float
    credits_consumed: int
    credits_remaining: int
    by_endpoint: List[EndpointUsage]
    timeseries: List[TimeseriesPoint]


class LogEntry(BaseModel):
    """Entrée de log API"""
    id: str
    timestamp: datetime
    api_key_prefix: str
    endpoint: str
    method: str
    status_code: int
    latency_ms: int
    credits_used: int
    request_body_preview: Optional[str] = None
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True


class LogsResponse(BaseModel):
    """Réponse paginée des logs"""
    logs: List[LogEntry]
    total: int
    page: int
    page_size: int
    has_more: bool


class CreditsOverview(BaseModel):
    """Vue d'ensemble des crédits"""
    current_credits: int
    credits_used_today: int
    credits_used_this_week: int
    credits_used_this_month: int
    plan: str
    monthly_limit: Optional[int]
    usage_percent: float


# ==============================================
# HELPERS
# ==============================================

def get_date_range(range_str: str) -> tuple[datetime, datetime]:
    """Convertit une chaîne de plage en dates"""
    now = datetime.utcnow()
    
    if range_str == "24h":
        start = now - timedelta(hours=24)
    elif range_str == "7d":
        start = now - timedelta(days=7)
    elif range_str == "30d":
        start = now - timedelta(days=30)
    elif range_str == "90d":
        start = now - timedelta(days=90)
    else:
        start = now - timedelta(days=7)  # Défaut: 7 jours
    
    return start, now


# ==============================================
# ENDPOINTS
# ==============================================

@router.get("/usage", response_model=UsageStats)
async def get_usage_stats(
    range: Literal["24h", "7d", "30d", "90d"] = Query("7d", description="Période d'analyse"),
    api_key_id: Optional[str] = Query(None, description="Filtrer par clé API"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère les statistiques d'usage agrégées
    
    - **range**: Période (24h, 7d, 30d, 90d)
    - **api_key_id**: Optionnel - filtrer par clé spécifique
    """
    start_date, end_date = get_date_range(range)
    
    # Récupérer les IDs des clés de l'utilisateur
    keys_result = await db.execute(
        select(ApiKey.id).where(ApiKey.user_id == current_user.id)
    )
    user_key_ids = [k[0] for k in keys_result.fetchall()]
    
    if not user_key_ids:
        # Pas de clés, retourner des stats vides
        return UsageStats(
            range=range,
            total_requests=0,
            avg_requests_per_day=0,
            error_rate=0,
            avg_latency_ms=0,
            credits_consumed=0,
            credits_remaining=0,
            by_endpoint=[],
            timeseries=[]
        )
    
    # Filtre de base
    base_filter = and_(
        ApiLog.api_key_id.in_(user_key_ids),
        ApiLog.created_at >= start_date,
        ApiLog.created_at <= end_date
    )
    
    # Si filtre par clé spécifique
    if api_key_id:
        import uuid
        try:
            key_uuid = uuid.UUID(api_key_id)
            if key_uuid not in user_key_ids:
                raise HTTPException(status_code=404, detail="Clé non trouvée")
            base_filter = and_(base_filter, ApiLog.api_key_id == key_uuid)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de clé invalide")
    
    # Total requêtes
    total_result = await db.execute(
        select(func.count(ApiLog.id)).where(base_filter)
    )
    total_requests = total_result.scalar() or 0
    
    # Erreurs (status >= 400)
    error_result = await db.execute(
        select(func.count(ApiLog.id))
        .where(and_(base_filter, ApiLog.status_code >= 400))
    )
    error_count = error_result.scalar() or 0
    
    # Latence moyenne
    latency_result = await db.execute(
        select(func.avg(ApiLog.latency_ms)).where(base_filter)
    )
    avg_latency = latency_result.scalar() or 0
    
    # Crédits consommés
    credits_result = await db.execute(
        select(func.sum(ApiLog.credits_used)).where(base_filter)
    )
    credits_consumed = credits_result.scalar() or 0
    
    # Crédits restants
    user_credits_result = await db.execute(
        select(UserCredits).where(UserCredits.user_id == current_user.id)
    )
    user_credits = user_credits_result.scalar_one_or_none()
    credits_remaining = user_credits.current_credits if user_credits else 0
    
    # Stats par endpoint
    endpoint_stats_result = await db.execute(
        select(
            ApiLog.endpoint,
            func.count(ApiLog.id).label("count"),
            func.avg(ApiLog.latency_ms).label("avg_latency"),
            func.sum(
                func.cast(ApiLog.status_code >= 400, db.bind.dialect.type_descriptor(int))
            ).label("errors")
        )
        .where(base_filter)
        .group_by(ApiLog.endpoint)
        .order_by(func.count(ApiLog.id).desc())
    )
    
    by_endpoint = []
    for row in endpoint_stats_result.fetchall():
        by_endpoint.append(EndpointUsage(
            endpoint=row.endpoint,
            count=row.count,
            avg_latency_ms=round(row.avg_latency or 0, 2),
            error_count=row.errors or 0
        ))
    
    # Timeseries (par jour)
    timeseries_result = await db.execute(
        select(
            func.date(ApiLog.created_at).label("date"),
            func.count(ApiLog.id).label("count"),
            func.sum(
                func.cast(ApiLog.status_code >= 400, db.bind.dialect.type_descriptor(int))
            ).label("errors"),
            func.avg(ApiLog.latency_ms).label("avg_latency")
        )
        .where(base_filter)
        .group_by(func.date(ApiLog.created_at))
        .order_by(func.date(ApiLog.created_at))
    )
    
    timeseries = []
    for row in timeseries_result.fetchall():
        timeseries.append(TimeseriesPoint(
            date=row.date.isoformat() if row.date else "",
            count=row.count,
            errors=row.errors or 0,
            avg_latency_ms=round(row.avg_latency or 0, 2)
        ))
    
    # Calculer moyenne par jour
    days = max((end_date - start_date).days, 1)
    avg_per_day = total_requests / days
    
    # Taux d'erreur
    error_rate = (error_count / total_requests) if total_requests > 0 else 0
    
    return UsageStats(
        range=range,
        total_requests=total_requests,
        avg_requests_per_day=round(avg_per_day, 2),
        error_rate=round(error_rate, 4),
        avg_latency_ms=round(avg_latency, 2),
        credits_consumed=credits_consumed,
        credits_remaining=credits_remaining,
        by_endpoint=by_endpoint,
        timeseries=timeseries
    )


@router.get("/logs", response_model=LogsResponse)
async def get_logs(
    page: int = Query(1, ge=1, description="Numéro de page"),
    page_size: int = Query(50, ge=10, le=100, description="Taille de page"),
    range: Literal["24h", "7d", "30d", "90d"] = Query("7d", description="Période"),
    api_key_id: Optional[str] = Query(None, description="Filtrer par clé API"),
    endpoint: Optional[str] = Query(None, description="Filtrer par endpoint"),
    status: Optional[str] = Query(None, description="Filtrer par status (success, error)"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère les logs API avec pagination et filtres
    
    - **page**: Numéro de page (commence à 1)
    - **page_size**: Nombre de logs par page (10-100)
    - **range**: Période de temps
    - **api_key_id**: Filtrer par clé
    - **endpoint**: Filtrer par endpoint (ex: /api/v1/rag/query)
    - **status**: "success" (2xx) ou "error" (4xx/5xx)
    """
    start_date, end_date = get_date_range(range)
    
    # Récupérer les clés de l'utilisateur
    keys_result = await db.execute(
        select(ApiKey).where(ApiKey.user_id == current_user.id)
    )
    user_keys = {k.id: k for k in keys_result.scalars().all()}
    user_key_ids = list(user_keys.keys())
    
    if not user_key_ids:
        return LogsResponse(
            logs=[],
            total=0,
            page=page,
            page_size=page_size,
            has_more=False
        )
    
    # Construire les filtres
    filters = [
        ApiLog.api_key_id.in_(user_key_ids),
        ApiLog.created_at >= start_date,
        ApiLog.created_at <= end_date
    ]
    
    if api_key_id:
        import uuid
        try:
            key_uuid = uuid.UUID(api_key_id)
            filters.append(ApiLog.api_key_id == key_uuid)
        except ValueError:
            pass
    
    if endpoint:
        filters.append(ApiLog.endpoint.ilike(f"%{endpoint}%"))
    
    if status == "success":
        filters.append(ApiLog.status_code < 400)
    elif status == "error":
        filters.append(ApiLog.status_code >= 400)
    
    # Total
    count_result = await db.execute(
        select(func.count(ApiLog.id)).where(and_(*filters))
    )
    total = count_result.scalar() or 0
    
    # Logs paginés
    offset = (page - 1) * page_size
    logs_result = await db.execute(
        select(ApiLog)
        .where(and_(*filters))
        .order_by(ApiLog.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    logs = logs_result.scalars().all()
    
    # Convertir en réponse
    log_entries = []
    for log in logs:
        api_key = user_keys.get(log.api_key_id)
        log_entries.append(LogEntry(
            id=str(log.id),
            timestamp=log.created_at,
            api_key_prefix=api_key.prefix if api_key else "unknown",
            endpoint=log.endpoint,
            method=log.method,
            status_code=log.status_code,
            latency_ms=log.latency_ms or 0,
            credits_used=log.credits_used or 0,
            request_body_preview=log.request_body[:200] if log.request_body else None,
            error_message=log.error_message
        ))
    
    return LogsResponse(
        logs=log_entries,
        total=total,
        page=page,
        page_size=page_size,
        has_more=(offset + page_size) < total
    )


@router.get("/credits", response_model=CreditsOverview)
async def get_credits_overview(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère la vue d'ensemble des crédits de l'utilisateur
    """
    now = datetime.utcnow()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    
    # Crédits utilisateur
    credits_result = await db.execute(
        select(UserCredits).where(UserCredits.user_id == current_user.id)
    )
    user_credits = credits_result.scalar_one_or_none()
    
    if not user_credits:
        return CreditsOverview(
            current_credits=0,
            credits_used_today=0,
            credits_used_this_week=0,
            credits_used_this_month=0,
            plan="free",
            monthly_limit=100,
            usage_percent=0
        )
    
    # Récupérer les clés de l'utilisateur
    keys_result = await db.execute(
        select(ApiKey.id).where(ApiKey.user_id == current_user.id)
    )
    user_key_ids = [k[0] for k in keys_result.fetchall()]
    
    # Crédits utilisés aujourd'hui
    today_result = await db.execute(
        select(func.sum(ApiLog.credits_used))
        .where(and_(
            ApiLog.api_key_id.in_(user_key_ids),
            ApiLog.created_at >= today
        ))
    )
    credits_today = today_result.scalar() or 0
    
    # Crédits utilisés cette semaine
    week_result = await db.execute(
        select(func.sum(ApiLog.credits_used))
        .where(and_(
            ApiLog.api_key_id.in_(user_key_ids),
            ApiLog.created_at >= week_start
        ))
    )
    credits_week = week_result.scalar() or 0
    
    # Crédits utilisés ce mois
    month_result = await db.execute(
        select(func.sum(ApiLog.credits_used))
        .where(and_(
            ApiLog.api_key_id.in_(user_key_ids),
            ApiLog.created_at >= month_start
        ))
    )
    credits_month = month_result.scalar() or 0
    
    # Calculer pourcentage d'utilisation
    monthly_limit = user_credits.monthly_limit or 1000
    usage_percent = (credits_month / monthly_limit * 100) if monthly_limit > 0 else 0
    
    return CreditsOverview(
        current_credits=user_credits.current_credits,
        credits_used_today=credits_today,
        credits_used_this_week=credits_week,
        credits_used_this_month=credits_month,
        plan=user_credits.plan or "free",
        monthly_limit=monthly_limit,
        usage_percent=round(usage_percent, 2)
    )


@router.get("/overview")
async def get_dashboard_overview(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Vue d'ensemble rapide pour le dashboard développeur
    """
    now = datetime.utcnow()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    # Récupérer les clés de l'utilisateur
    keys_result = await db.execute(
        select(ApiKey.id).where(ApiKey.user_id == current_user.id)
    )
    user_key_ids = [k[0] for k in keys_result.fetchall()]
    
    if not user_key_ids:
        return {
            "requests_today": 0,
            "requests_30d": 0,
            "credits_consumed_month": 0,
            "errors_7d": 0,
            "active_keys": 0,
            "plan": "free"
        }
    
    # Requêtes aujourd'hui
    today_result = await db.execute(
        select(func.count(ApiLog.id))
        .where(and_(
            ApiLog.api_key_id.in_(user_key_ids),
            ApiLog.created_at >= today
        ))
    )
    requests_today = today_result.scalar() or 0
    
    # Requêtes 30 jours
    month_result = await db.execute(
        select(func.count(ApiLog.id))
        .where(and_(
            ApiLog.api_key_id.in_(user_key_ids),
            ApiLog.created_at >= month_ago
        ))
    )
    requests_30d = month_result.scalar() or 0
    
    # Erreurs 7 jours
    errors_result = await db.execute(
        select(func.count(ApiLog.id))
        .where(and_(
            ApiLog.api_key_id.in_(user_key_ids),
            ApiLog.created_at >= week_ago,
            ApiLog.status_code >= 400
        ))
    )
    errors_7d = errors_result.scalar() or 0
    
    # Crédits ce mois
    month_start = today.replace(day=1)
    credits_result = await db.execute(
        select(func.sum(ApiLog.credits_used))
        .where(and_(
            ApiLog.api_key_id.in_(user_key_ids),
            ApiLog.created_at >= month_start
        ))
    )
    credits_month = credits_result.scalar() or 0
    
    # Clés actives
    active_keys_result = await db.execute(
        select(func.count(ApiKey.id))
        .where(and_(
            ApiKey.user_id == current_user.id,
            ApiKey.status == "active"
        ))
    )
    active_keys = active_keys_result.scalar() or 0
    
    # Plan
    user_credits_result = await db.execute(
        select(UserCredits.plan).where(UserCredits.user_id == current_user.id)
    )
    plan = user_credits_result.scalar() or "free"
    
    return {
        "requests_today": requests_today,
        "requests_30d": requests_30d,
        "credits_consumed_month": credits_month,
        "errors_7d": errors_7d,
        "active_keys": active_keys,
        "plan": plan
    }
