"""
Analytics Router - Real-Time Dashboard & Metrics
Provides live analytics for usage, performance, and business metrics
"""
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from collections import defaultdict

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import redis.asyncio as redis

from app.config import get_settings
from app.dependencies import get_current_user, require_admin

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


class TimeRange(str):
    """Time range options"""
    HOUR = "1h"
    DAY = "24h"
    WEEK = "7d"
    MONTH = "30d"


class MetricType(str):
    """Metric types"""
    API_CALLS = "api_calls"
    TOKENS_USED = "tokens_used"
    ERRORS = "errors"
    LATENCY = "latency"
    ACTIVE_USERS = "active_users"
    CREDITS_USED = "credits_used"
    WORKFLOW_RUNS = "workflow_runs"


class AnalyticsEvent(BaseModel):
    """Analytics event model"""
    event_type: str
    user_id: Optional[str] = None
    tenant_id: Optional[str] = None
    endpoint: Optional[str] = None
    model: Optional[str] = None
    tokens: int = 0
    latency_ms: float = 0
    credits: float = 0
    success: bool = True
    metadata: Dict[str, Any] = {}


class AnalyticsCollector:
    """
    Collects and aggregates analytics events
    Uses Redis for real-time aggregation
    """

    # Redis key patterns
    COUNTER_KEY = "analytics:{metric}:{period}:{bucket}"
    RECENT_KEY = "analytics:recent:{metric}"
    USER_KEY = "analytics:user:{user_id}:{metric}"

    def __init__(self):
        self._redis: Optional[redis.Redis] = None

    async def connect(self):
        if not self._redis:
            self._redis = redis.Redis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True
            )

    async def disconnect(self):
        if self._redis:
            await self._redis.close()

    async def _ensure_connected(self):
        if not self._redis:
            await self.connect()

    # ================================================
    # Event Collection
    # ================================================

    async def record_event(self, event: AnalyticsEvent):
        """Record an analytics event"""
        await self._ensure_connected()

        now = datetime.utcnow()

        # Increment counters for different time buckets
        pipe = self._redis.pipeline()

        # Minute bucket
        minute_bucket = now.strftime("%Y%m%d%H%M")
        pipe.incr(self.COUNTER_KEY.format(
            metric=event.event_type,
            period="minute",
            bucket=minute_bucket
        ))
        pipe.expire(self.COUNTER_KEY.format(
            metric=event.event_type,
            period="minute",
            bucket=minute_bucket
        ), 3600)  # 1 hour TTL

        # Hour bucket
        hour_bucket = now.strftime("%Y%m%d%H")
        pipe.incr(self.COUNTER_KEY.format(
            metric=event.event_type,
            period="hour",
            bucket=hour_bucket
        ))
        pipe.expire(self.COUNTER_KEY.format(
            metric=event.event_type,
            period="hour",
            bucket=hour_bucket
        ), 86400 * 7)  # 7 days TTL

        # Day bucket
        day_bucket = now.strftime("%Y%m%d")
        pipe.incr(self.COUNTER_KEY.format(
            metric=event.event_type,
            period="day",
            bucket=day_bucket
        ))

        # Token tracking
        if event.tokens > 0:
            pipe.incrby(self.COUNTER_KEY.format(
                metric="tokens",
                period="day",
                bucket=day_bucket
            ), event.tokens)

        # User tracking
        if event.user_id:
            pipe.sadd(f"analytics:active_users:{day_bucket}", event.user_id)
            pipe.expire(f"analytics:active_users:{day_bucket}", 86400 * 30)

            # Per-user metrics
            pipe.incr(self.USER_KEY.format(
                user_id=event.user_id,
                metric=event.event_type
            ))

        # Recent events (for real-time stream)
        event_data = {
            **event.model_dump(),
            "timestamp": now.isoformat()
        }
        pipe.lpush(self.RECENT_KEY.format(metric="all"), json.dumps(event_data))
        pipe.ltrim(self.RECENT_KEY.format(metric="all"), 0, 999)  # Keep last 1000

        await pipe.execute()

    async def record_api_call(
        self,
        endpoint: str,
        latency_ms: float,
        user_id: str = None,
        success: bool = True,
        tokens: int = 0,
        model: str = None
    ):
        """Convenience method for API call tracking"""
        await self.record_event(AnalyticsEvent(
            event_type=MetricType.API_CALLS,
            user_id=user_id,
            endpoint=endpoint,
            model=model,
            tokens=tokens,
            latency_ms=latency_ms,
            success=success
        ))

    # ================================================
    # Metrics Retrieval
    # ================================================

    async def get_metric_series(
        self,
        metric: str,
        period: str = "hour",
        buckets: int = 24
    ) -> List[Dict[str, Any]]:
        """Get time series data for a metric"""
        await self._ensure_connected()

        now = datetime.utcnow()
        data = []

        for i in range(buckets):
            if period == "minute":
                bucket_time = now - timedelta(minutes=i)
                bucket = bucket_time.strftime("%Y%m%d%H%M")
            elif period == "hour":
                bucket_time = now - timedelta(hours=i)
                bucket = bucket_time.strftime("%Y%m%d%H")
            else:  # day
                bucket_time = now - timedelta(days=i)
                bucket = bucket_time.strftime("%Y%m%d")

            key = self.COUNTER_KEY.format(metric=metric, period=period, bucket=bucket)
            value = await self._redis.get(key)

            data.append({
                "timestamp": bucket_time.isoformat(),
                "bucket": bucket,
                "value": int(value) if value else 0
            })

        return list(reversed(data))

    async def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get comprehensive dashboard statistics"""
        await self._ensure_connected()

        now = datetime.utcnow()
        today = now.strftime("%Y%m%d")
        yesterday = (now - timedelta(days=1)).strftime("%Y%m%d")
        this_hour = now.strftime("%Y%m%d%H")

        pipe = self._redis.pipeline()

        # Today's metrics
        pipe.get(self.COUNTER_KEY.format(metric="api_calls", period="day", bucket=today))
        pipe.get(self.COUNTER_KEY.format(metric="tokens", period="day", bucket=today))
        pipe.get(self.COUNTER_KEY.format(metric="errors", period="day", bucket=today))
        pipe.scard(f"analytics:active_users:{today}")

        # Yesterday's metrics (for comparison)
        pipe.get(self.COUNTER_KEY.format(metric="api_calls", period="day", bucket=yesterday))

        # This hour
        pipe.get(self.COUNTER_KEY.format(metric="api_calls", period="hour", bucket=this_hour))

        results = await pipe.execute()

        api_calls_today = int(results[0]) if results[0] else 0
        tokens_today = int(results[1]) if results[1] else 0
        errors_today = int(results[2]) if results[2] else 0
        active_users = int(results[3]) if results[3] else 0
        api_calls_yesterday = int(results[4]) if results[4] else 0
        api_calls_hour = int(results[5]) if results[5] else 0

        # Calculate growth
        growth = ((api_calls_today - api_calls_yesterday) / api_calls_yesterday * 100
                  if api_calls_yesterday > 0 else 0)

        return {
            "timestamp": now.isoformat(),
            "today": {
                "api_calls": api_calls_today,
                "tokens_used": tokens_today,
                "errors": errors_today,
                "active_users": active_users,
                "error_rate": round(errors_today / api_calls_today * 100, 2) if api_calls_today > 0 else 0
            },
            "this_hour": {
                "api_calls": api_calls_hour,
                "avg_per_minute": round(api_calls_hour / 60, 2)
            },
            "comparison": {
                "api_calls_growth_pct": round(growth, 1),
                "vs_yesterday": {
                    "api_calls": api_calls_yesterday
                }
            }
        }

    async def get_top_endpoints(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top endpoints by usage"""
        await self._ensure_connected()

        # Get recent events
        events = await self._redis.lrange(self.RECENT_KEY.format(metric="all"), 0, 999)

        # Aggregate by endpoint
        endpoint_counts = defaultdict(int)
        endpoint_latency = defaultdict(list)

        for event_str in events:
            event = json.loads(event_str)
            if event.get("endpoint"):
                endpoint_counts[event["endpoint"]] += 1
                if event.get("latency_ms"):
                    endpoint_latency[event["endpoint"]].append(event["latency_ms"])

        # Build result
        result = []
        for endpoint, count in sorted(endpoint_counts.items(), key=lambda x: x[1], reverse=True)[:limit]:
            latencies = endpoint_latency[endpoint]
            avg_latency = sum(latencies) / len(latencies) if latencies else 0

            result.append({
                "endpoint": endpoint,
                "calls": count,
                "avg_latency_ms": round(avg_latency, 2)
            })

        return result

    async def get_model_usage(self) -> List[Dict[str, Any]]:
        """Get usage breakdown by model"""
        await self._ensure_connected()

        events = await self._redis.lrange(self.RECENT_KEY.format(metric="all"), 0, 999)

        model_stats = defaultdict(lambda: {"calls": 0, "tokens": 0})

        for event_str in events:
            event = json.loads(event_str)
            if event.get("model"):
                model_stats[event["model"]]["calls"] += 1
                model_stats[event["model"]]["tokens"] += event.get("tokens", 0)

        return [
            {"model": model, **stats}
            for model, stats in sorted(model_stats.items(), key=lambda x: x[1]["calls"], reverse=True)
        ]


# Singleton instance
analytics = AnalyticsCollector()


# ================================================
# API Endpoints
# ================================================

@router.get("/dashboard")
async def get_dashboard(current_user: dict = Depends(require_admin)):
    """
    Get real-time dashboard statistics

    Requires admin privileges
    """
    return await analytics.get_dashboard_stats()


@router.get("/series/{metric}")
async def get_metric_series(
    metric: str,
    period: str = Query("hour", regex="^(minute|hour|day)$"),
    buckets: int = Query(24, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """
    Get time series data for a metric

    Parameters:
        - metric: api_calls, tokens, errors, etc.
        - period: minute, hour, or day
        - buckets: Number of data points
    """
    return await analytics.get_metric_series(metric, period, buckets)


@router.get("/top-endpoints")
async def get_top_endpoints(
    limit: int = Query(10, ge=1, le=50),
    current_user: dict = Depends(get_current_user)
):
    """Get top API endpoints by usage"""
    return await analytics.get_top_endpoints(limit)


@router.get("/models")
async def get_model_usage(current_user: dict = Depends(get_current_user)):
    """Get usage breakdown by LLM model"""
    return await analytics.get_model_usage()


@router.get("/stream")
async def stream_analytics(current_user: dict = Depends(require_admin)):
    """
    Stream real-time analytics via Server-Sent Events

    Updates every 5 seconds with latest metrics
    """
    async def event_generator():
        while True:
            try:
                stats = await analytics.get_dashboard_stats()
                yield f"data: {json.dumps(stats)}\n\n"
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"Analytics stream error: {e}")
                yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
                break

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.post("/track")
async def track_event(
    event: AnalyticsEvent,
    current_user: dict = Depends(get_current_user)
):
    """Track a custom analytics event"""
    event.user_id = current_user.get("sub")
    await analytics.record_event(event)
    return {"status": "tracked"}


@router.get("/user/{user_id}")
async def get_user_analytics(
    user_id: str,
    current_user: dict = Depends(require_admin)
):
    """Get analytics for a specific user (admin only)"""
    await analytics._ensure_connected()

    metrics = ["api_calls", "tokens", "errors"]
    result = {}

    for metric in metrics:
        key = analytics.USER_KEY.format(user_id=user_id, metric=metric)
        value = await analytics._redis.get(key)
        result[metric] = int(value) if value else 0

    return {
        "user_id": user_id,
        "metrics": result
    }


@router.get("/health")
async def analytics_health():
    """Check analytics service health"""
    try:
        await analytics._ensure_connected()
        await analytics._redis.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
