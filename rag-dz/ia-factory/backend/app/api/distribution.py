"""
IA Factory - Distribution API
Phase 3: Multi-Platform Publishing & Scheduling
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import List, Optional

from ..database import get_db, Collections
from ..models.distribution import Platform, PublishStatus, PLATFORM_SPECS
from ..services.platform_converter import PlatformConverter
from ..services.content_adapter import ContentAdapter
from ..services.platform_publishers import PublishingManager
from ..config import settings

router = APIRouter(tags=["Distribution"])


# =============================================================================
# PLATFORM MANAGEMENT
# =============================================================================

@router.get("/platforms", response_model=dict)
async def list_platforms():
    """Get list of supported platforms with specs"""
    
    platforms = []
    for platform, spec in PLATFORM_SPECS.items():
        platforms.append({
            "id": platform.value,
            "name": platform.value.replace("_", " ").title(),
            "aspect_ratio": spec.aspect_ratio,
            "max_duration": spec.max_duration,
            "max_file_size_mb": spec.max_file_size_mb,
            "max_caption_length": spec.max_caption_length,
            "max_hashtags": spec.max_hashtags
        })
    
    return {"platforms": platforms}


@router.post("/{brand_id}/platforms/connect", response_model=dict)
async def connect_platform(
    brand_id: str,
    platform: str,
    credentials: dict,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Connect a platform to the brand"""
    
    try:
        platform_enum = Platform(platform)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid platform: {platform}")
    
    # Save platform config
    config = {
        "brand_id": brand_id,
        "platform": platform,
        "is_connected": True,
        "credentials": credentials,  # Should be encrypted in production
        "connected_at": datetime.now()
    }
    
    await db.platform_configs.update_one(
        {"brand_id": brand_id, "platform": platform},
        {"$set": config},
        upsert=True
    )
    
    return {
        "status": "connected",
        "platform": platform,
        "message": f"Successfully connected {platform}"
    }


@router.get("/{brand_id}/platforms", response_model=dict)
async def get_connected_platforms(
    brand_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get connected platforms for a brand"""
    
    configs = await db.platform_configs.find({
        "brand_id": brand_id
    }).to_list(None)
    
    connected = []
    for config in configs:
        config["_id"] = str(config["_id"])
        # Remove sensitive credentials from response
        config.pop("credentials", None)
        connected.append(config)
    
    return {
        "brand_id": brand_id,
        "connected_platforms": connected
    }


# =============================================================================
# VIDEO CONVERSION
# =============================================================================

@router.post("/convert", response_model=dict)
async def convert_video_for_platforms(
    video_id: str,
    platforms: List[str],
    background_tasks: BackgroundTasks = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Phase 3: Convert video for multiple platforms
    """
    
    video = await db[Collections.VIDEOS].find_one({"_id": ObjectId(video_id)})
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    video_url = video.get('edited_video_url') or video.get('raw_video_url')
    if not video_url:
        raise HTTPException(status_code=400, detail="No video file available")
    
    # Validate platforms
    try:
        target_platforms = [Platform(p) for p in platforms]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid platform: {e}")
    
    # Create conversion job
    job = {
        "video_id": video_id,
        "type": "conversion",
        "platforms": platforms,
        "status": "started",
        "created_at": datetime.now()
    }
    
    result = await db[Collections.JOBS].insert_one(job)
    job_id = str(result.inserted_id)
    
    if background_tasks:
        background_tasks.add_task(
            _convert_video_task,
            db, job_id, video_id, video_url, target_platforms
        )
    
    return {
        "status": "started",
        "job_id": job_id,
        "platforms": platforms
    }


async def _convert_video_task(
    db: AsyncIOMotorDatabase,
    job_id: str,
    video_id: str,
    video_url: str,
    platforms: List[Platform]
):
    """Background task for video conversion"""
    
    try:
        converter = PlatformConverter()
        results = await converter.convert_for_platforms(
            source_video=video_url,
            platforms=platforms
        )
        
        # Update video with platform versions
        platform_versions = {}
        for platform, result in results.items():
            if result.success:
                platform_versions[platform] = result.output_path
        
        await db[Collections.VIDEOS].update_one(
            {"_id": ObjectId(video_id)},
            {"$set": {"platform_versions": platform_versions}}
        )
        
        await db[Collections.JOBS].update_one(
            {"_id": ObjectId(job_id)},
            {
                "$set": {
                    "status": "completed",
                    "results": {p: {"success": r.success, "path": r.output_path} for p, r in results.items()},
                    "completed_at": datetime.now()
                }
            }
        )
        
    except Exception as e:
        await db[Collections.JOBS].update_one(
            {"_id": ObjectId(job_id)},
            {"$set": {"status": "failed", "error": str(e)}}
        )


# =============================================================================
# CONTENT ADAPTATION
# =============================================================================

@router.post("/adapt", response_model=dict)
async def adapt_content_for_platforms(
    content_id: str,
    platforms: List[str],
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Phase 3: Adapt caption and hashtags for platforms
    """
    
    # Get content
    content = await db[Collections.CONTENT].find_one({"_id": ObjectId(content_id)})
    if not content:
        # Try scripts
        content = await db[Collections.SCRIPTS].find_one({"_id": ObjectId(content_id)})
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Get brand
    brand = await db[Collections.BRANDS].find_one({"_id": ObjectId(content.get('brand_id'))})
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    # Build original caption from script
    original_caption = f"{content.get('hook', '')}\n\n{content.get('body', '')}\n\n{content.get('cta', '')}"
    original_hashtags = content.get('hashtag_suggestions', [])
    
    # Adapt for all platforms
    adapter = ContentAdapter()
    
    try:
        target_platforms = [Platform(p) for p in platforms]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid platform: {e}")
    
    adapted = await adapter.adapt_for_all_platforms(
        original_caption=original_caption,
        original_hashtags=original_hashtags,
        platforms=target_platforms,
        brand_guidelines=brand,
        niche=brand.get('niche', 'Technology'),
        language=brand.get('language', 'en')
    )
    
    # Save adapted content
    await db[Collections.CONTENT].update_one(
        {"_id": ObjectId(content_id)},
        {"$set": {"adapted_content": adapted}},
        upsert=True
    )
    
    return {
        "status": "success",
        "content_id": content_id,
        "adapted": adapted
    }


# =============================================================================
# PUBLISHING
# =============================================================================

@router.post("/publish", response_model=dict)
async def publish_content(
    scheduled_post_id: str,
    background_tasks: BackgroundTasks = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Phase 3: Publish content to a platform
    """
    
    post = await db[Collections.SCHEDULED_POSTS].find_one({
        "_id": ObjectId(scheduled_post_id)
    })
    
    if not post:
        raise HTTPException(status_code=404, detail="Scheduled post not found")
    
    # Get video
    video = await db[Collections.VIDEOS].find_one({"_id": ObjectId(post.get('video_id'))})
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Get platform config
    platform_config = await db.platform_configs.find_one({
        "brand_id": post.get('brand_id'),
        "platform": post.get('platform')
    })
    
    if not platform_config or not platform_config.get('is_connected'):
        raise HTTPException(
            status_code=400,
            detail=f"Platform {post.get('platform')} not connected"
        )
    
    # Update status to publishing
    await db[Collections.SCHEDULED_POSTS].update_one(
        {"_id": ObjectId(scheduled_post_id)},
        {"$set": {"status": PublishStatus.PUBLISHING.value}}
    )
    
    if background_tasks:
        background_tasks.add_task(
            _publish_task,
            db, scheduled_post_id, post, video, platform_config
        )
    
    return {
        "status": "publishing",
        "scheduled_post_id": scheduled_post_id,
        "platform": post.get('platform')
    }


async def _publish_task(
    db: AsyncIOMotorDatabase,
    post_id: str,
    post: dict,
    video: dict,
    platform_config: dict
):
    """Background task for publishing"""
    
    try:
        platform = Platform(post.get('platform'))
        
        # Get video URL for platform
        video_url = video.get('platform_versions', {}).get(platform.value)
        if not video_url:
            video_url = video.get('edited_video_url') or video.get('raw_video_url')
        
        # Get adapted content
        adapted = post.get('adapted_content', {})
        
        # Initialize publisher
        credentials = {
            'instagram_token': settings.instagram_token,
            'instagram_account_id': settings.instagram_account_id,
            'tiktok_client_key': settings.tiktok_client_key,
            'tiktok_client_secret': settings.tiktok_client_secret,
        }
        
        manager = PublishingManager(credentials)
        
        result = await manager.publish_to_platform(
            platform=platform,
            video_path=video_url,
            metadata={
                'post_id': post_id,
                'brand_id': post.get('brand_id'),
                'caption': adapted.get('caption', ''),
                'hashtags': adapted.get('hashtags', []),
                'video_url': video_url
            }
        )
        
        # Update post status
        await db[Collections.SCHEDULED_POSTS].update_one(
            {"_id": ObjectId(post_id)},
            {
                "$set": {
                    "status": PublishStatus.PUBLISHED.value if result.success else PublishStatus.FAILED.value,
                    "platform_post_id": result.platform_post_id,
                    "platform_url": result.platform_url,
                    "published_at": datetime.now() if result.success else None,
                    "error_message": result.error_message
                }
            }
        )
        
        # Save publish result
        await db[Collections.PUBLISH_RESULTS].insert_one(result.model_dump())
        
    except Exception as e:
        await db[Collections.SCHEDULED_POSTS].update_one(
            {"_id": ObjectId(post_id)},
            {
                "$set": {
                    "status": PublishStatus.FAILED.value,
                    "error_message": str(e)
                }
            }
        )


@router.post("/publish-batch", response_model=dict)
async def publish_batch(
    brand_id: str,
    platforms: List[str] = None,
    limit: int = 10,
    background_tasks: BackgroundTasks = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Publish multiple scheduled posts
    """
    
    query = {
        "brand_id": brand_id,
        "status": PublishStatus.SCHEDULED.value,
        "scheduled_time": {"$lte": datetime.now().isoformat()}
    }
    
    if platforms:
        query["platform"] = {"$in": platforms}
    
    posts = await db[Collections.SCHEDULED_POSTS].find(query).limit(limit).to_list(None)
    
    if not posts:
        return {
            "status": "no_posts",
            "message": "No posts ready for publishing"
        }
    
    # Queue each post for publishing
    for post in posts:
        if background_tasks:
            video = await db[Collections.VIDEOS].find_one({"_id": ObjectId(post.get('video_id'))})
            platform_config = await db.platform_configs.find_one({
                "brand_id": brand_id,
                "platform": post.get('platform')
            })
            
            if video and platform_config:
                background_tasks.add_task(
                    _publish_task,
                    db, str(post["_id"]), post, video, platform_config
                )
    
    return {
        "status": "publishing",
        "posts_queued": len(posts),
        "message": f"Publishing {len(posts)} posts"
    }


# =============================================================================
# SCHEDULING
# =============================================================================

@router.post("/schedule", response_model=dict)
async def schedule_post(
    video_id: str,
    platform: str,
    scheduled_time: str,
    caption: Optional[str] = None,
    hashtags: Optional[List[str]] = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Schedule a single post"""
    
    video = await db[Collections.VIDEOS].find_one({"_id": ObjectId(video_id)})
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    try:
        scheduled_dt = datetime.fromisoformat(scheduled_time)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format")
    
    post = {
        "video_id": video_id,
        "brand_id": video.get('brand_id'),
        "platform": platform,
        "scheduled_time": scheduled_time,
        "status": PublishStatus.SCHEDULED.value,
        "adapted_content": {
            "caption": caption or "",
            "hashtags": hashtags or []
        },
        "created_at": datetime.now()
    }
    
    result = await db[Collections.SCHEDULED_POSTS].insert_one(post)
    
    return {
        "status": "scheduled",
        "post_id": str(result.inserted_id),
        "scheduled_time": scheduled_time,
        "platform": platform
    }


@router.get("/scheduled/{brand_id}", response_model=dict)
async def get_scheduled_posts(
    brand_id: str,
    status: Optional[str] = None,
    platform: Optional[str] = None,
    limit: int = 50,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get scheduled posts for a brand"""
    
    query = {"brand_id": brand_id}
    
    if status:
        query["status"] = status
    if platform:
        query["platform"] = platform
    
    posts = await db[Collections.SCHEDULED_POSTS].find(query).sort(
        "scheduled_time", 1
    ).limit(limit).to_list(None)
    
    for post in posts:
        post["_id"] = str(post["_id"])
    
    return {
        "brand_id": brand_id,
        "posts": posts,
        "total": len(posts)
    }


@router.delete("/scheduled/{post_id}", response_model=dict)
async def cancel_scheduled_post(
    post_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Cancel a scheduled post"""
    
    result = await db[Collections.SCHEDULED_POSTS].update_one(
        {"_id": ObjectId(post_id)},
        {"$set": {"status": PublishStatus.CANCELLED.value}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {"status": "cancelled", "post_id": post_id}
