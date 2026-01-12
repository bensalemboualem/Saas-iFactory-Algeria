"""
Publishing Tasks - Social media publishing tasks
"""
from celery import shared_task
from typing import Dict, Any, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def publish_to_platform(
    self,
    video_path: str,
    platform: str,
    title: str,
    description: str = "",
    tags: List[str] = None,
    privacy: str = "public"
) -> Dict[str, Any]:
    """Publish video to a single platform."""
    from app.agents.publish_agent import PublishAgent
    from app.agents.base import AgentTask
    import asyncio

    tags = tags or []

    try:
        agent = PublishAgent()
        task = AgentTask(
            task_type="publish_video",
            input_data={
                "video_path": video_path,
                "platform": platform,
                "title": title,
                "description": description,
                "tags": tags,
                "privacy": privacy
            }
        )

        result = asyncio.run(agent.execute(task))

        if not result.success:
            raise Exception(result.error_message)

        return result.output_data.get("publish_result", {})

    except Exception as e:
        logger.error(f"Publishing to {platform} failed: {e}")
        self.retry(exc=e)


@shared_task(bind=True)
def publish_to_multiple_platforms(
    self,
    video_path: str,
    platforms: List[str],
    base_title: str,
    base_description: str = "",
    base_tags: List[str] = None,
    auto_optimize: bool = True
) -> Dict[str, Any]:
    """Publish video to multiple platforms."""
    from app.agents.publish_agent import PublishAgent
    from app.agents.base import AgentTask
    import asyncio

    base_tags = base_tags or []

    try:
        agent = PublishAgent()
        task = AgentTask(
            task_type="batch_publish",
            input_data={
                "video_path": video_path,
                "platforms": platforms,
                "auto_optimize": auto_optimize,
                "metadata": {
                    "title": base_title,
                    "description": base_description,
                    "tags": base_tags
                }
            }
        )

        result = asyncio.run(agent.execute(task))
        return result.output_data

    except Exception as e:
        logger.error(f"Multi-platform publishing failed: {e}")
        raise


@shared_task
def process_scheduled():
    """Process scheduled publications that are due."""
    # TODO: Query database for scheduled publications that are due
    # and trigger publish_to_platform for each

    logger.info("Processing scheduled publications")

    # Placeholder - replace with actual DB query
    scheduled_items = []  # Get from database

    processed = 0
    for item in scheduled_items:
        scheduled_time = item.get("scheduled_time")
        if scheduled_time and datetime.utcnow() >= scheduled_time:
            publish_to_platform.delay(
                video_path=item.get("video_path"),
                platform=item.get("platform"),
                title=item.get("title"),
                description=item.get("description", ""),
                tags=item.get("tags", [])
            )
            processed += 1
            # TODO: Update status in database

    return {"processed": processed}


@shared_task(bind=True)
def sync_analytics(self) -> Dict[str, Any]:
    """Sync analytics from all published videos."""
    from app.agents.publish_agent import PublishAgent
    from app.agents.base import AgentTask
    import asyncio

    logger.info("Syncing analytics for published videos")

    # TODO: Get list of published videos from database
    published_videos = []  # Get from database

    agent = PublishAgent()
    updated = 0

    for video in published_videos:
        try:
            task = AgentTask(
                task_type="get_analytics",
                input_data={
                    "platform": video.get("platform"),
                    "platform_post_id": video.get("platform_post_id")
                }
            )

            result = asyncio.run(agent.execute(task))

            if result.success:
                analytics = result.output_data.get("analytics", {})
                # TODO: Update analytics in database
                updated += 1

        except Exception as e:
            logger.error(f"Failed to sync analytics for {video.get('id')}: {e}")

    return {"updated": updated, "total": len(published_videos)}


@shared_task(bind=True, max_retries=2)
def generate_thumbnail(
    self,
    video_path: str,
    platform: str,
    title_text: str = None,
    style: str = "modern"
) -> Dict[str, Any]:
    """Generate optimized thumbnail for a platform."""
    from app.agents.publish_agent import PublishAgent
    from app.agents.base import AgentTask
    import asyncio

    try:
        agent = PublishAgent()
        task = AgentTask(
            task_type="generate_thumbnail",
            input_data={
                "video_path": video_path,
                "platform": platform,
                "title_text": title_text,
                "style": style
            }
        )

        result = asyncio.run(agent.execute(task))

        if not result.success:
            raise Exception(result.error_message)

        return result.output_data.get("thumbnail", {})

    except Exception as e:
        logger.error(f"Thumbnail generation failed: {e}")
        self.retry(exc=e)


@shared_task(bind=True)
def optimize_metadata(
    self,
    content_summary: str,
    platform: str,
    language: str = "fr"
) -> Dict[str, Any]:
    """Optimize metadata for a platform using AI."""
    from app.agents.publish_agent import PublishAgent
    from app.agents.base import AgentTask
    import asyncio

    try:
        agent = PublishAgent()
        task = AgentTask(
            task_type="optimize_metadata",
            input_data={
                "platform": platform,
                "content_summary": content_summary,
                "language": language
            }
        )

        result = asyncio.run(agent.execute(task))
        return result.output_data.get("optimized_metadata", {})

    except Exception as e:
        logger.error(f"Metadata optimization failed: {e}")
        raise
