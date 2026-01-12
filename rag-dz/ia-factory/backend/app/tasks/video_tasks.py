"""
Video Processing Tasks
Background tasks for video generation and editing
"""

from celery import shared_task
from typing import Dict, Any
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
def generate_video_task(self, script_id: str, brand_id: str, style: str = "professional") -> Dict[str, Any]:
    """
    Background task to generate video from script using VEO 3
    """
    try:
        logger.info(f"Starting video generation for script: {script_id}")
        
        from app.services.video_generation import VideoGenerator
        from app.database import get_database
        
        async def _generate():
            db = await get_database()
            generator = VideoGenerator(db)
            
            # Get script from database
            script = await db.scripts.find_one({"_id": script_id})
            if not script:
                raise ValueError(f"Script not found: {script_id}")
            
            # Generate video
            result = await generator.generate_video(
                script_id=script_id,
                brand_id=brand_id,
                prompt=script.get("content", ""),
                style=style
            )
            
            return result
        
        result = run_async(_generate())
        logger.info(f"Video generation completed: {result.get('job_id')}")
        return result
        
    except Exception as exc:
        logger.error(f"Video generation failed: {exc}")
        self.retry(exc=exc, countdown=60 * (self.request.retries + 1))


@shared_task(bind=True, max_retries=3)
def auto_edit_video_task(self, video_path: str, brand_id: str, output_path: str = None) -> Dict[str, Any]:
    """
    Background task to auto-edit a video using AI analysis
    """
    try:
        logger.info(f"Starting auto-edit for video: {video_path}")
        
        from app.services.video_operator import VideoOperator
        from app.database import get_database
        
        async def _edit():
            db = await get_database()
            operator = VideoOperator(db)
            
            result = await operator.auto_edit_video(
                video_path=video_path,
                brand_id=brand_id,
                output_path=output_path
            )
            
            return result
        
        result = run_async(_edit())
        logger.info(f"Auto-edit completed: {result.get('output_path')}")
        return result
        
    except Exception as exc:
        logger.error(f"Auto-edit failed: {exc}")
        self.retry(exc=exc, countdown=60 * (self.request.retries + 1))


@shared_task(bind=True, max_retries=3)
def convert_for_platform_task(
    self,
    video_path: str,
    platform: str,
    output_dir: str = None
) -> Dict[str, Any]:
    """
    Background task to convert video for specific platform
    """
    try:
        logger.info(f"Converting video for platform: {platform}")
        
        from app.services.platform_converter import PlatformConverter
        
        async def _convert():
            converter = PlatformConverter()
            
            result = await converter.convert_for_platform(
                video_path=video_path,
                platform=platform,
                output_dir=output_dir
            )
            
            return result
        
        result = run_async(_convert())
        logger.info(f"Conversion completed: {result}")
        return {"output_path": result, "platform": platform}
        
    except Exception as exc:
        logger.error(f"Platform conversion failed: {exc}")
        self.retry(exc=exc, countdown=30 * (self.request.retries + 1))


@shared_task(bind=True)
def bulk_generate_videos_task(
    self,
    brand_id: str,
    topics: list,
    style: str = "professional"
) -> Dict[str, Any]:
    """
    Background task to generate multiple videos in bulk
    """
    try:
        logger.info(f"Starting bulk video generation for {len(topics)} topics")
        
        from app.services.script_generation import ScriptGenerator
        from app.services.video_generation import VideoGenerator
        from app.database import get_database
        
        async def _bulk_generate():
            db = await get_database()
            script_gen = ScriptGenerator(db)
            video_gen = VideoGenerator(db)
            
            # Get brand
            brand = await db.brands.find_one({"_id": brand_id})
            if not brand:
                raise ValueError(f"Brand not found: {brand_id}")
            
            results = []
            
            for topic in topics:
                try:
                    # Generate script
                    script = await script_gen.generate_script(
                        brand_id=brand_id,
                        topic=topic,
                        content_type="short_video"
                    )
                    
                    # Generate video
                    video = await video_gen.generate_video(
                        script_id=script["script_id"],
                        brand_id=brand_id,
                        prompt=script["content"],
                        style=style
                    )
                    
                    results.append({
                        "topic": topic,
                        "script_id": script["script_id"],
                        "video_job_id": video["job_id"],
                        "status": "success"
                    })
                    
                except Exception as e:
                    results.append({
                        "topic": topic,
                        "error": str(e),
                        "status": "failed"
                    })
            
            return {
                "total": len(topics),
                "successful": sum(1 for r in results if r["status"] == "success"),
                "failed": sum(1 for r in results if r["status"] == "failed"),
                "results": results
            }
        
        result = run_async(_bulk_generate())
        logger.info(f"Bulk generation completed: {result['successful']}/{result['total']} successful")
        return result
        
    except Exception as exc:
        logger.error(f"Bulk generation failed: {exc}")
        raise
