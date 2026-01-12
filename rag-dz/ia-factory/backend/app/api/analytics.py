"""
IA Factory - Analytics API
Phase 4: Performance Analytics & Optimization
"""

from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime, timedelta
from typing import Optional

from ..database import get_db, Collections
from ..models.analytics import TimeRange, PerformanceMetric
from ..services.analytics_engine import AnalyticsEngine

router = APIRouter(tags=["Analytics"])


# =============================================================================
# DASHBOARD
# =============================================================================

@router.get("/dashboard/{brand_id}")
async def get_dashboard(
    brand_id: str,
    days: int = 30,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Phase 4: Get dashboard summary with key metrics
    """
    
    brand = await db[Collections.BRANDS].find_one({"_id": ObjectId(brand_id)})
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    engine = AnalyticsEngine(db)
    summary = await engine.get_dashboard_summary(brand_id, days)
    
    return summary.model_dump()


# =============================================================================
# PERFORMANCE METRICS
# =============================================================================

@router.get("/content/{content_id}")
async def get_content_performance(
    content_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get detailed performance for a single content piece"""
    
    # First try to find metrics
    metrics = await db[Collections.METRICS].find({
        "content_id": content_id
    }).to_list(None)
    
    if not metrics:
        raise HTTPException(status_code=404, detail="No metrics found for this content")
    
    # Aggregate metrics
    total_views = sum(m.get('views', 0) for m in metrics)
    total_likes = sum(m.get('likes', 0) for m in metrics)
    total_comments = sum(m.get('comments', 0) for m in metrics)
    total_shares = sum(m.get('shares', 0) for m in metrics)
    total_saves = sum(m.get('saves', 0) for m in metrics)
    total_engagement = total_likes + total_comments + total_shares + total_saves
    
    return {
        "content_id": content_id,
        "total_views": total_views,
        "total_engagement": total_engagement,
        "engagement_rate": (total_engagement / max(total_views, 1)) * 100,
        "breakdown": {
            "views": total_views,
            "likes": total_likes,
            "comments": total_comments,
            "shares": total_shares,
            "saves": total_saves
        },
        "by_platform": [
            {
                "platform": m.get('platform'),
                "views": m.get('views', 0),
                "likes": m.get('likes', 0),
                "comments": m.get('comments', 0)
            }
            for m in metrics
        ]
    }


@router.post("/content/{content_id}/metrics")
async def record_metrics(
    content_id: str,
    platform: str,
    views: int = 0,
    likes: int = 0,
    comments: int = 0,
    shares: int = 0,
    saves: int = 0,
    followers_gained: int = 0,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Record performance metrics for content"""
    
    # Get content to find brand_id
    content = await db[Collections.CONTENT].find_one({"_id": ObjectId(content_id)})
    if not content:
        content = await db[Collections.SCRIPTS].find_one({"_id": ObjectId(content_id)})
    
    brand_id = content.get('brand_id') if content else None
    
    metric = {
        "content_id": content_id,
        "brand_id": brand_id,
        "platform": platform,
        "views": views,
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "saves": saves,
        "followers_gained": followers_gained,
        "engagement_rate": ((likes + comments + shares + saves) / max(views, 1)) * 100,
        "timestamp": datetime.now()
    }
    
    result = await db[Collections.METRICS].insert_one(metric)
    
    return {
        "status": "recorded",
        "metric_id": str(result.inserted_id)
    }


# =============================================================================
# PILLAR ANALYTICS
# =============================================================================

@router.get("/pillars/{brand_id}")
async def get_pillar_performance(
    brand_id: str,
    time_range: str = "month",
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get performance broken down by content pillar"""
    
    try:
        tr = TimeRange(time_range)
    except ValueError:
        tr = TimeRange.MONTH
    
    engine = AnalyticsEngine(db)
    performances = await engine.get_pillar_performance(brand_id, tr)
    
    return {
        "brand_id": brand_id,
        "time_range": time_range,
        "pillars": [p.model_dump() for p in performances]
    }


# =============================================================================
# PLATFORM ANALYTICS
# =============================================================================

@router.get("/platforms/{brand_id}")
async def get_platform_performance(
    brand_id: str,
    time_range: str = "month",
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get performance broken down by platform"""
    
    try:
        tr = TimeRange(time_range)
    except ValueError:
        tr = TimeRange.MONTH
    
    engine = AnalyticsEngine(db)
    performances = await engine.get_platform_performance(brand_id, tr)
    
    return {
        "brand_id": brand_id,
        "time_range": time_range,
        "platforms": [p.model_dump() for p in performances]
    }


# =============================================================================
# AI RECOMMENDATIONS
# =============================================================================

@router.get("/recommendations/{brand_id}")
async def get_ai_recommendations(
    brand_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Phase 4: Get AI-powered optimization recommendations
    """
    
    brand = await db[Collections.BRANDS].find_one({"_id": ObjectId(brand_id)})
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    # Get pillars
    pillars = await db[Collections.PILLARS].find({"brand_id": brand_id}).to_list(None)
    brand['content_pillars'] = pillars
    
    engine = AnalyticsEngine(db)
    recommendations = await engine.get_ai_recommendations(brand_id, brand)
    
    return {
        "brand_id": brand_id,
        "recommendations": [r.model_dump() for r in recommendations],
        "generated_at": datetime.now().isoformat()
    }


@router.get("/content-ideas/{brand_id}")
async def get_content_ideas(
    brand_id: str,
    count: int = 5,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Phase 4: Get AI-generated content ideas based on performance
    """
    
    brand = await db[Collections.BRANDS].find_one({"_id": ObjectId(brand_id)})
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    pillars = await db[Collections.PILLARS].find({"brand_id": brand_id}).to_list(None)
    brand['content_pillars'] = pillars
    
    engine = AnalyticsEngine(db)
    ideas = await engine.generate_content_ideas(brand_id, brand, count)
    
    return {
        "brand_id": brand_id,
        "ideas": [i.model_dump() for i in ideas],
        "count": len(ideas)
    }


# =============================================================================
# REPORTS
# =============================================================================

@router.get("/report/{brand_id}")
async def generate_report(
    brand_id: str,
    time_range: str = "month",
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Phase 4: Generate comprehensive analytics report
    """
    
    brand = await db[Collections.BRANDS].find_one({"_id": ObjectId(brand_id)})
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    pillars = await db[Collections.PILLARS].find({"brand_id": brand_id}).to_list(None)
    brand['content_pillars'] = pillars
    
    try:
        tr = TimeRange(time_range)
    except ValueError:
        tr = TimeRange.MONTH
    
    engine = AnalyticsEngine(db)
    report = await engine.generate_full_report(brand_id, brand, tr)
    
    # Save report
    report_doc = report.model_dump()
    report_doc['brand_id'] = brand_id
    await db[Collections.ANALYTICS_REPORTS].insert_one(report_doc)
    
    return report_doc


@router.get("/reports/{brand_id}/history")
async def get_report_history(
    brand_id: str,
    limit: int = 10,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get historical reports for a brand"""
    
    reports = await db[Collections.ANALYTICS_REPORTS].find({
        "brand_id": brand_id
    }).sort("generated_at", -1).limit(limit).to_list(None)
    
    for report in reports:
        report["_id"] = str(report["_id"])
    
    return {
        "brand_id": brand_id,
        "reports": reports,
        "total": len(reports)
    }


# =============================================================================
# TRENDING & INSIGHTS
# =============================================================================

@router.get("/trending/{brand_id}")
async def get_trending_content(
    brand_id: str,
    limit: int = 10,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get top performing content"""
    
    # Get metrics sorted by views
    metrics = await db[Collections.METRICS].find({
        "brand_id": brand_id
    }).sort("views", -1).limit(limit).to_list(None)
    
    for m in metrics:
        m["_id"] = str(m["_id"])
    
    return {
        "brand_id": brand_id,
        "trending": metrics
    }


@router.get("/best-times/{brand_id}")
async def get_best_posting_times(
    brand_id: str,
    platform: Optional[str] = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Analyze best posting times based on performance"""
    
    # Aggregate metrics by hour
    match_query = {"brand_id": brand_id}
    if platform:
        match_query["platform"] = platform
    
    pipeline = [
        {"$match": match_query},
        {"$project": {
            "hour": {"$hour": "$timestamp"},
            "day_of_week": {"$dayOfWeek": "$timestamp"},
            "engagement": {"$add": ["$likes", "$comments", "$shares", "$saves"]},
            "views": 1
        }},
        {"$group": {
            "_id": {"hour": "$hour", "day": "$day_of_week"},
            "avg_engagement": {"$avg": "$engagement"},
            "avg_views": {"$avg": "$views"},
            "post_count": {"$sum": 1}
        }},
        {"$sort": {"avg_engagement": -1}}
    ]
    
    results = await db[Collections.METRICS].aggregate(pipeline).to_list(None)
    
    # Find best times
    best_hours = {}
    for r in results:
        hour = r['_id']['hour']
        if hour not in best_hours or r['avg_engagement'] > best_hours[hour]['avg_engagement']:
            best_hours[hour] = r
    
    sorted_hours = sorted(best_hours.items(), key=lambda x: x[1]['avg_engagement'], reverse=True)
    
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    
    return {
        "brand_id": brand_id,
        "platform": platform,
        "best_times": [
            {
                "hour": h,
                "day": days[data['_id']['day'] - 1] if data['_id'].get('day') else "Any",
                "avg_engagement": data['avg_engagement'],
                "post_count": data['post_count']
            }
            for h, data in sorted_hours[:5]
        ],
        "recommendation": f"Best time to post: {sorted_hours[0][0]}:00" if sorted_hours else "Not enough data"
    }
