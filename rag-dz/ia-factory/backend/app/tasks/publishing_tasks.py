"""
Publishing Tasks
Background tasks for scheduled publishing and content distribution
"""

from celery import shared_task
from typing import Dict, Any, List
from datetime import datetime, timezone
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


@shared_task(bind=True, max_retries=3)
def publish_to_platform_task(
    self,
    content_id: str,
    platform: str,
    credentials: Dict[str, str]
) -> Dict[str, Any]:
    """
    Background task to publish content to a specific platform
    """
    try:
        logger.info(f"Publishing content {content_id} to {platform}")
        
        from app.services.platform_publishers import PublishingManager
        from app.database import get_database
        
        async def _publish():
            db = await get_database()
            
            # Get content from database
            content = await db.content.find_one({"_id": content_id})
            if not content:
                raise ValueError(f"Content not found: {content_id}")
            
            manager = PublishingManager(db)
            
            result = await manager.publish_to_platform(
                content_id=content_id,
                platform=platform,
                video_path=content.get("video_path"),
                caption=content.get("caption"),
                credentials=credentials
            )
            
            # Update content status
            await db.content.update_one(
                {"_id": content_id},
                {
                    "$set": {
                        f"platforms.{platform}.published": True,
                        f"platforms.{platform}.published_at": datetime.now(timezone.utc),
                        f"platforms.{platform}.post_id": result.get("post_id")
                    }
                }
            )
            
            return result
        
        result = run_async(_publish())
        logger.info(f"Published successfully to {platform}: {result.get('post_id')}")
        return result
        
    except Exception as exc:
        logger.error(f"Publishing to {platform} failed: {exc}")
        self.retry(exc=exc, countdown=60 * (self.request.retries + 1))


@shared_task
def check_scheduled_posts() -> Dict[str, Any]:
    """
    Periodic task to check and publish scheduled posts
    Runs every 5 minutes via Celery Beat
    """
    try:
        logger.info("Checking for scheduled posts...")
        
        from app.database import get_database
        
        async def _check_scheduled():
            db = await get_database()
            now = datetime.now(timezone.utc)
            
            # Find posts scheduled for now or earlier that haven't been published
            scheduled_posts = await db.scheduled_posts.find({
                "scheduled_time": {"$lte": now},
                "status": "scheduled"
            }).to_list(100)
            
            results = []
            
            for post in scheduled_posts:
                try:
                    # Update status to processing
                    await db.scheduled_posts.update_one(
                        {"_id": post["_id"]},
                        {"$set": {"status": "processing"}}
                    )
                    
                    # Queue the publish task
                    publish_to_platform_task.delay(
                        content_id=post["content_id"],
                        platform=post["platform"],
                        credentials=post.get("credentials", {})
                    )
                    
                    results.append({
                        "post_id": str(post["_id"]),
                        "platform": post["platform"],
                        "status": "queued"
                    })
                    
                except Exception as e:
                    # Mark as failed
                    await db.scheduled_posts.update_one(
                        {"_id": post["_id"]},
                        {
                            "$set": {
                                "status": "failed",
                                "error": str(e)
                            }
                        }
                    )
                    results.append({
                        "post_id": str(post["_id"]),
                        "platform": post["platform"],
                        "status": "failed",
                        "error": str(e)
                    })
            
            return {
                "checked_at": now.isoformat(),
                "posts_found": len(scheduled_posts),
                "results": results
            }
        
        result = run_async(_check_scheduled())
        logger.info(f"Scheduled posts check completed: {result['posts_found']} posts processed")
        return result
        
    except Exception as exc:
        logger.error(f"Scheduled posts check failed: {exc}")
        raise


@shared_task(bind=True, max_retries=2)
def multi_platform_publish_task(
    self,
    content_id: str,
    platforms: List[str],
    brand_id: str
) -> Dict[str, Any]:
    """
    Background task to publish content to multiple platforms
    """
    try:
        logger.info(f"Multi-platform publish for content {content_id} to {platforms}")
        
        from app.services.platform_publishers import PublishingManager
        from app.services.content_adapter import ContentAdapter
        from app.database import get_database
        
        async def _multi_publish():
            db = await get_database()
            
            # Get content and brand
            content = await db.content.find_one({"_id": content_id})
            brand = await db.brands.find_one({"_id": brand_id})
            
            if not content:
                raise ValueError(f"Content not found: {content_id}")
            if not brand:
                raise ValueError(f"Brand not found: {brand_id}")
            
            adapter = ContentAdapter(db)
            manager = PublishingManager(db)
            
            results = {}
            
            for platform in platforms:
                try:
                    # Get platform credentials
                    creds = await db.platform_credentials.find_one({
                        "brand_id": brand_id,
                        "platform": platform
                    })
                    
                    if not creds:
                        results[platform] = {
                            "status": "skipped",
                            "reason": "No credentials configured"
                        }
                        continue
                    
                    # Adapt caption for platform
                    adapted_caption = await adapter.adapt_caption(
                        original_caption=content.get("caption", ""),
                        platform=platform,
                        brand_id=brand_id
                    )
                    
                    # Publish
                    result = await manager.publish_to_platform(
                        content_id=content_id,
                        platform=platform,
                        video_path=content.get("video_path"),
                        caption=adapted_caption["adapted_caption"],
                        credentials=creds
                    )
                    
                    results[platform] = {
                        "status": "success",
                        "post_id": result.get("post_id"),
                        "url": result.get("url")
                    }
                    
                except Exception as e:
                    results[platform] = {
                        "status": "failed",
                        "error": str(e)
                    }
            
            # Update content with publish results
            await db.content.update_one(
                {"_id": content_id},
                {
                    "$set": {
                        "publish_results": results,
                        "last_published_at": datetime.now(timezone.utc)
                    }
                }
            )
            
            return {
                "content_id": content_id,
                "platforms": platforms,
                "results": results,
                "successful": sum(1 for r in results.values() if r["status"] == "success"),
                "failed": sum(1 for r in results.values() if r["status"] == "failed")
            }
        
        result = run_async(_multi_publish())
        logger.info(f"Multi-platform publish completed: {result['successful']}/{len(platforms)} successful")
        return result
        
    except Exception as exc:
        logger.error(f"Multi-platform publish failed: {exc}")
        self.retry(exc=exc, countdown=120)


@shared_task
def cleanup_old_scheduled_posts() -> Dict[str, Any]:
    """
    Cleanup task to remove old processed scheduled posts
    """
    try:
        from app.database import get_database
        from datetime import timedelta
        
        async def _cleanup():
            db = await get_database()
            cutoff = datetime.now(timezone.utc) - timedelta(days=30)
            
            result = await db.scheduled_posts.delete_many({
                "status": {"$in": ["published", "failed"]},
                "scheduled_time": {"$lt": cutoff}
            })
            
            return {
                "deleted_count": result.deleted_count,
                "cutoff_date": cutoff.isoformat()
            }
        
        result = run_async(_cleanup())
        logger.info(f"Cleaned up {result['deleted_count']} old scheduled posts")
        return result
        
    except Exception as exc:
        logger.error(f"Cleanup failed: {exc}")
        raise
