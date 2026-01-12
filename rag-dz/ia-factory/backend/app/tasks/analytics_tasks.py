"""
Analytics Tasks
Background tasks for analytics collection and report generation
"""

from celery import shared_task
from typing import Dict, Any, List
from datetime import datetime, timezone, timedelta
import logging
import asyncio

logger = logging.getLogger(__name__)


def run_async(coro):
    """Helper to run async functions in Celery tasks"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@shared_task
def update_all_analytics() -> Dict[str, Any]:
    """
    Periodic task to update analytics for all brands
    Runs every hour via Celery Beat
    """
    try:
        logger.info("Starting analytics update for all brands...")
        
        from app.services.analytics_engine import AnalyticsEngine
        from app.database import get_database
        
        async def _update_all():
            db = await get_database()
            engine = AnalyticsEngine(db)
            
            # Get all active brands
            brands = await db.brands.find({"active": True}).to_list(1000)
            
            results = []
            
            for brand in brands:
                try:
                    brand_id = str(brand["_id"])
                    
                    # Fetch latest metrics from platforms
                    await _fetch_platform_metrics(db, brand_id)
                    
                    # Update analytics summary
                    summary = await engine.get_dashboard_summary(brand_id)
                    
                    results.append({
                        "brand_id": brand_id,
                        "brand_name": brand.get("name"),
                        "status": "updated",
                        "total_views": summary.get("total_views", 0)
                    })
                    
                except Exception as e:
                    results.append({
                        "brand_id": str(brand["_id"]),
                        "brand_name": brand.get("name"),
                        "status": "failed",
                        "error": str(e)
                    })
            
            return {
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "brands_processed": len(brands),
                "successful": sum(1 for r in results if r["status"] == "updated"),
                "results": results
            }
        
        result = run_async(_update_all())
        logger.info(f"Analytics update completed: {result['successful']}/{result['brands_processed']} brands")
        return result
        
    except Exception as exc:
        logger.error(f"Analytics update failed: {exc}")
        raise


async def _fetch_platform_metrics(db, brand_id: str):
    """
    Fetch latest metrics from all connected platforms
    """
    # Get published content
    content_items = await db.content.find({
        "brand_id": brand_id,
        "publish_results": {"$exists": True}
    }).to_list(100)
    
    for content in content_items:
        publish_results = content.get("publish_results", {})
        
        for platform, result in publish_results.items():
            if result.get("status") != "success":
                continue
            
            post_id = result.get("post_id")
            if not post_id:
                continue
            
            # In production, fetch real metrics from platform APIs
            # For now, simulate metrics update
            metrics = {
                "views": content.get(f"metrics.{platform}.views", 0) + 10,
                "likes": content.get(f"metrics.{platform}.likes", 0) + 1,
                "comments": content.get(f"metrics.{platform}.comments", 0),
                "shares": content.get(f"metrics.{platform}.shares", 0),
                "updated_at": datetime.now(timezone.utc)
            }
            
            await db.content.update_one(
                {"_id": content["_id"]},
                {"$set": {f"metrics.{platform}": metrics}}
            )


@shared_task
def generate_daily_report() -> Dict[str, Any]:
    """
    Generate daily performance report for all brands
    Runs at midnight via Celery Beat
    """
    try:
        logger.info("Generating daily reports...")
        
        from app.services.analytics_engine import AnalyticsEngine
        from app.database import get_database
        
        async def _generate_reports():
            db = await get_database()
            engine = AnalyticsEngine(db)
            
            yesterday = datetime.now(timezone.utc) - timedelta(days=1)
            
            # Get all active brands
            brands = await db.brands.find({"active": True}).to_list(1000)
            
            reports = []
            
            for brand in brands:
                try:
                    brand_id = str(brand["_id"])
                    
                    # Generate report
                    report = await engine.get_performance_report(
                        brand_id=brand_id,
                        start_date=yesterday.replace(hour=0, minute=0, second=0),
                        end_date=yesterday.replace(hour=23, minute=59, second=59)
                    )
                    
                    # Get AI recommendations
                    recommendations = await engine.get_ai_recommendations(brand_id)
                    
                    # Store report
                    report_doc = {
                        "brand_id": brand_id,
                        "report_date": yesterday.date().isoformat(),
                        "report_type": "daily",
                        "data": report,
                        "recommendations": recommendations,
                        "created_at": datetime.now(timezone.utc)
                    }
                    
                    await db.reports.insert_one(report_doc)
                    
                    reports.append({
                        "brand_id": brand_id,
                        "brand_name": brand.get("name"),
                        "status": "generated",
                        "summary": {
                            "total_views": report.get("total_views", 0),
                            "total_engagement": report.get("total_engagement", 0),
                            "content_published": report.get("content_published", 0)
                        }
                    })
                    
                except Exception as e:
                    reports.append({
                        "brand_id": str(brand["_id"]),
                        "brand_name": brand.get("name"),
                        "status": "failed",
                        "error": str(e)
                    })
            
            return {
                "report_date": yesterday.date().isoformat(),
                "brands_processed": len(brands),
                "successful": sum(1 for r in reports if r["status"] == "generated"),
                "reports": reports
            }
        
        result = run_async(_generate_reports())
        logger.info(f"Daily reports generated: {result['successful']}/{result['brands_processed']}")
        return result
        
    except Exception as exc:
        logger.error(f"Daily report generation failed: {exc}")
        raise


@shared_task(bind=True, max_retries=3)
def generate_custom_report_task(
    self,
    brand_id: str,
    start_date: str,
    end_date: str,
    report_type: str = "performance"
) -> Dict[str, Any]:
    """
    Generate a custom analytics report for a brand
    """
    try:
        logger.info(f"Generating custom {report_type} report for brand {brand_id}")
        
        from app.services.analytics_engine import AnalyticsEngine
        from app.database import get_database
        
        async def _generate():
            db = await get_database()
            engine = AnalyticsEngine(db)
            
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
            
            if report_type == "performance":
                report = await engine.get_performance_report(brand_id, start, end)
            elif report_type == "content":
                # Content-focused report
                content_items = await db.content.find({
                    "brand_id": brand_id,
                    "created_at": {"$gte": start, "$lte": end}
                }).to_list(1000)
                
                report = {
                    "content_count": len(content_items),
                    "content_items": [
                        {
                            "id": str(c["_id"]),
                            "title": c.get("title"),
                            "type": c.get("type"),
                            "status": c.get("status"),
                            "created_at": c.get("created_at").isoformat() if c.get("created_at") else None
                        }
                        for c in content_items
                    ]
                }
            elif report_type == "engagement":
                # Engagement-focused report
                summary = await engine.get_dashboard_summary(brand_id)
                report = {
                    "total_engagement": summary.get("total_engagement", 0),
                    "engagement_by_platform": summary.get("engagement_by_platform", {}),
                    "top_content": summary.get("top_performing", [])
                }
            else:
                report = await engine.get_performance_report(brand_id, start, end)
            
            # Get recommendations
            recommendations = await engine.get_ai_recommendations(brand_id)
            
            # Store report
            report_doc = {
                "brand_id": brand_id,
                "report_type": report_type,
                "start_date": start_date,
                "end_date": end_date,
                "data": report,
                "recommendations": recommendations,
                "created_at": datetime.now(timezone.utc)
            }
            
            result = await db.reports.insert_one(report_doc)
            
            return {
                "report_id": str(result.inserted_id),
                "brand_id": brand_id,
                "report_type": report_type,
                "period": f"{start_date} to {end_date}",
                "data": report,
                "recommendations_count": len(recommendations.get("recommendations", []))
            }
        
        result = run_async(_generate())
        logger.info(f"Custom report generated: {result['report_id']}")
        return result
        
    except Exception as exc:
        logger.error(f"Custom report generation failed: {exc}")
        self.retry(exc=exc, countdown=60)


@shared_task
def calculate_trending_topics() -> Dict[str, Any]:
    """
    Analyze content performance to identify trending topics
    """
    try:
        logger.info("Calculating trending topics...")
        
        from app.database import get_database
        
        async def _calculate():
            db = await get_database()
            
            # Get content from last 7 days
            week_ago = datetime.now(timezone.utc) - timedelta(days=7)
            
            pipeline = [
                {
                    "$match": {
                        "created_at": {"$gte": week_ago},
                        "metrics": {"$exists": True}
                    }
                },
                {
                    "$addFields": {
                        "total_engagement": {
                            "$sum": [
                                {"$ifNull": ["$metrics.instagram.likes", 0]},
                                {"$ifNull": ["$metrics.tiktok.likes", 0]},
                                {"$ifNull": ["$metrics.youtube.likes", 0]},
                                {"$ifNull": ["$metrics.linkedin.likes", 0]}
                            ]
                        }
                    }
                },
                {
                    "$group": {
                        "_id": "$content_pillar",
                        "total_engagement": {"$sum": "$total_engagement"},
                        "content_count": {"$sum": 1},
                        "avg_engagement": {"$avg": "$total_engagement"}
                    }
                },
                {"$sort": {"avg_engagement": -1}},
                {"$limit": 10}
            ]
            
            trending = await db.content.aggregate(pipeline).to_list(10)
            
            # Store trending data
            await db.trending.update_one(
                {"type": "topics"},
                {
                    "$set": {
                        "data": trending,
                        "updated_at": datetime.now(timezone.utc)
                    }
                },
                upsert=True
            )
            
            return {
                "calculated_at": datetime.now(timezone.utc).isoformat(),
                "trending_topics": trending
            }
        
        result = run_async(_calculate())
        logger.info(f"Trending topics calculated: {len(result['trending_topics'])} topics")
        return result
        
    except Exception as exc:
        logger.error(f"Trending calculation failed: {exc}")
        raise
