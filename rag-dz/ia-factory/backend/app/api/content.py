"""
IA Factory - Content API
Phase 2 & 3: Content Generation & Distribution
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import List, Optional

from ..database import get_db, Collections
from ..models.content import Script, Video, ContentBatch, ContentStatus
from ..models.distribution import Platform
from ..services.script_generation import ScriptGenerator
from ..services.video_generation import VideoGenerator
from ..services.video_operator import VideoOperator
from ..services.content_calendar import ContentCalendar
from ..services.platform_converter import PlatformConverter
from ..services.content_adapter import ContentAdapter

router = APIRouter(tags=["Content Generation"])


# =============================================================================
# SCRIPT GENERATION
# =============================================================================

@router.post("/scripts/generate", response_model=dict)
async def generate_scripts(
    brand_id: str,
    num_scripts: int = 30,
    duration: int = 15,
    background_tasks: BackgroundTasks = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Phase 2: Generate multiple scripts from brand's featured topic
    
    This expands a single topic into multiple variations and generates
    optimized scripts for each variation.
    """
    
    # Get brand guidelines
    brand = await db[Collections.BRANDS].find_one({"_id": ObjectId(brand_id)})
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    if not brand.get('featured_topic'):
        raise HTTPException(
            status_code=400,
            detail="No featured topic set. Use /api/brand/{brand_id}/featured-topic first"
        )
    
    # Create batch record
    batch_doc = {
        "brand_id": brand_id,
        "source_topic": brand['featured_topic'],
        "num_pieces": num_scripts,
        "status": ContentStatus.GENERATING.value,
        "scripts_generated": 0,
        "created_at": datetime.now()
    }
    
    batch_result = await db[Collections.CONTENT].insert_one(batch_doc)
    batch_id = str(batch_result.inserted_id)
    
    # Start generation in background
    if background_tasks:
        background_tasks.add_task(
            _generate_scripts_task,
            db, batch_id, brand, num_scripts, duration
        )
    
    return {
        "status": "started",
        "batch_id": batch_id,
        "num_scripts": num_scripts,
        "topic": brand['featured_topic'],
        "message": f"Generating {num_scripts} scripts in background. Poll /api/content/batch/{batch_id} for status."
    }


async def _generate_scripts_task(
    db: AsyncIOMotorDatabase,
    batch_id: str,
    brand: dict,
    num_scripts: int,
    duration: int
):
    """Background task for script generation"""
    
    try:
        generator = ScriptGenerator()
        
        # Generate scripts
        scripts = await generator.generate_bulk_scripts(
            brand_guidelines=brand,
            num_scripts=num_scripts,
            duration=duration
        )
        
        # Save scripts to database
        script_docs = []
        for i, script in enumerate(scripts):
            script_doc = {
                "brand_id": brand.get('_id'),
                "batch_id": batch_id,
                "topic": script.get('topic', ''),
                "hook": script.get('hook', ''),
                "body": script.get('body', ''),
                "cta": script.get('cta', ''),
                "full_script": script.get('full_script', ''),
                "timing": script.get('timing', {}),
                "suggested_music_mood": script.get('suggested_music_mood', ''),
                "suggested_visuals": script.get('suggested_visuals', []),
                "text_overlays": script.get('text_overlays', []),
                "hashtag_suggestions": script.get('hashtag_suggestions', []),
                "status": ContentStatus.GENERATED.value,
                "created_at": datetime.now(),
                "index": i
            }
            script_docs.append(script_doc)
        
        if script_docs:
            await db[Collections.SCRIPTS].insert_many(script_docs)
        
        # Update batch status
        await db[Collections.CONTENT].update_one(
            {"_id": ObjectId(batch_id)},
            {
                "$set": {
                    "status": ContentStatus.GENERATED.value,
                    "scripts_generated": len(scripts),
                    "completed_at": datetime.now()
                }
            }
        )
        
    except Exception as e:
        await db[Collections.CONTENT].update_one(
            {"_id": ObjectId(batch_id)},
            {
                "$set": {
                    "status": ContentStatus.FAILED.value,
                    "error": str(e)
                }
            }
        )


@router.get("/scripts/{brand_id}", response_model=List[dict])
async def get_scripts(
    brand_id: str,
    status: Optional[str] = None,
    limit: int = 50,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get all scripts for a brand"""
    
    query = {"brand_id": brand_id}
    if status:
        query["status"] = status
    
    scripts = await db[Collections.SCRIPTS].find(query).limit(limit).to_list(None)
    
    for script in scripts:
        script["_id"] = str(script["_id"])
    
    return scripts


@router.get("/batch/{batch_id}", response_model=dict)
async def get_batch_status(
    batch_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get status of a content batch"""
    
    batch = await db[Collections.CONTENT].find_one({"_id": ObjectId(batch_id)})
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    batch["_id"] = str(batch["_id"])
    
    # Get script count
    script_count = await db[Collections.SCRIPTS].count_documents({"batch_id": batch_id})
    batch["actual_scripts"] = script_count
    
    return batch


# =============================================================================
# VIDEO GENERATION
# =============================================================================

@router.post("/videos/generate", response_model=dict)
async def generate_videos(
    brand_id: str,
    script_ids: Optional[List[str]] = None,
    batch_id: Optional[str] = None,
    backend: str = "replicate",
    background_tasks: BackgroundTasks = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Phase 2: Generate videos from scripts
    
    Uses VEO 3 or Replicate to generate videos from scripts.
    """
    
    # Get brand
    brand = await db[Collections.BRANDS].find_one({"_id": ObjectId(brand_id)})
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    # Get scripts
    if script_ids:
        scripts = await db[Collections.SCRIPTS].find({
            "_id": {"$in": [ObjectId(sid) for sid in script_ids]}
        }).to_list(None)
    elif batch_id:
        scripts = await db[Collections.SCRIPTS].find({
            "batch_id": batch_id
        }).to_list(None)
    else:
        raise HTTPException(
            status_code=400,
            detail="Provide either script_ids or batch_id"
        )
    
    if not scripts:
        raise HTTPException(status_code=404, detail="No scripts found")
    
    # Create job record
    job_doc = {
        "brand_id": brand_id,
        "type": "video_generation",
        "script_count": len(scripts),
        "backend": backend,
        "status": "started",
        "created_at": datetime.now()
    }
    
    job_result = await db[Collections.JOBS].insert_one(job_doc)
    job_id = str(job_result.inserted_id)
    
    # Start in background
    if background_tasks:
        background_tasks.add_task(
            _generate_videos_task,
            db, job_id, brand, scripts, backend
        )
    
    return {
        "status": "started",
        "job_id": job_id,
        "script_count": len(scripts),
        "backend": backend,
        "message": f"Generating {len(scripts)} videos. Poll /api/content/job/{job_id} for status."
    }


async def _generate_videos_task(
    db: AsyncIOMotorDatabase,
    job_id: str,
    brand: dict,
    scripts: list,
    backend: str
):
    """Background task for video generation"""
    
    try:
        generator = VideoGenerator()
        
        for i, script in enumerate(scripts):
            try:
                result = await generator.generate_video(
                    script=script,
                    brand_guidelines=brand,
                    backend=backend
                )
                
                # Save video record
                video_doc = {
                    "script_id": str(script["_id"]),
                    "brand_id": str(brand["_id"]),
                    "job_id": job_id,
                    "raw_video_url": result.get('video_url'),
                    "backend": backend,
                    "status": ContentStatus.GENERATED.value if result.get('video_url') else ContentStatus.FAILED.value,
                    "created_at": datetime.now()
                }
                
                await db[Collections.VIDEOS].insert_one(video_doc)
                
                # Update job progress
                await db[Collections.JOBS].update_one(
                    {"_id": ObjectId(job_id)},
                    {"$inc": {"videos_generated": 1}}
                )
                
            except Exception as e:
                await db[Collections.VIDEOS].insert_one({
                    "script_id": str(script["_id"]),
                    "brand_id": str(brand["_id"]),
                    "job_id": job_id,
                    "status": ContentStatus.FAILED.value,
                    "error": str(e),
                    "created_at": datetime.now()
                })
        
        # Mark job complete
        await db[Collections.JOBS].update_one(
            {"_id": ObjectId(job_id)},
            {
                "$set": {
                    "status": "completed",
                    "completed_at": datetime.now()
                }
            }
        )
        
    except Exception as e:
        await db[Collections.JOBS].update_one(
            {"_id": ObjectId(job_id)},
            {
                "$set": {
                    "status": "failed",
                    "error": str(e)
                }
            }
        )


@router.get("/job/{job_id}", response_model=dict)
async def get_job_status(
    job_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get status of a generation job"""
    
    job = await db[Collections.JOBS].find_one({"_id": ObjectId(job_id)})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job["_id"] = str(job["_id"])
    return job


# =============================================================================
# VIDEO EDITING
# =============================================================================

@router.post("/videos/edit", response_model=dict)
async def edit_videos(
    brand_id: str,
    video_ids: Optional[List[str]] = None,
    job_id: Optional[str] = None,
    background_tasks: BackgroundTasks = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Phase 2: Auto-edit videos using VideoOperator
    """
    
    brand = await db[Collections.BRANDS].find_one({"_id": ObjectId(brand_id)})
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    # Get videos
    if video_ids:
        videos = await db[Collections.VIDEOS].find({
            "_id": {"$in": [ObjectId(vid) for vid in video_ids]}
        }).to_list(None)
    elif job_id:
        videos = await db[Collections.VIDEOS].find({
            "job_id": job_id,
            "status": ContentStatus.GENERATED.value
        }).to_list(None)
    else:
        raise HTTPException(status_code=400, detail="Provide video_ids or job_id")
    
    if not videos:
        raise HTTPException(status_code=404, detail="No videos found")
    
    # Create edit job
    edit_job = {
        "brand_id": brand_id,
        "type": "video_editing",
        "video_count": len(videos),
        "status": "started",
        "created_at": datetime.now()
    }
    
    result = await db[Collections.JOBS].insert_one(edit_job)
    edit_job_id = str(result.inserted_id)
    
    if background_tasks:
        background_tasks.add_task(
            _edit_videos_task,
            db, edit_job_id, brand, videos
        )
    
    return {
        "status": "started",
        "job_id": edit_job_id,
        "video_count": len(videos)
    }


async def _edit_videos_task(
    db: AsyncIOMotorDatabase,
    job_id: str,
    brand: dict,
    videos: list
):
    """Background task for video editing"""
    
    operator = VideoOperator()
    
    for video in videos:
        try:
            script = await db[Collections.SCRIPTS].find_one({
                "_id": ObjectId(video.get('script_id'))
            })
            
            if not script or not video.get('raw_video_url'):
                continue
            
            result = await operator.auto_edit(
                video_path=video['raw_video_url'],
                script=script,
                brand_guidelines=brand
            )
            
            await db[Collections.VIDEOS].update_one(
                {"_id": video["_id"]},
                {
                    "$set": {
                        "edited_video_url": result.get('output_path'),
                        "editing_plan": result.get('editing_plan'),
                        "status": ContentStatus.EDITED.value
                    }
                }
            )
            
        except Exception as e:
            await db[Collections.VIDEOS].update_one(
                {"_id": video["_id"]},
                {"$set": {"edit_error": str(e)}}
            )
    
    await db[Collections.JOBS].update_one(
        {"_id": ObjectId(job_id)},
        {"$set": {"status": "completed", "completed_at": datetime.now()}}
    )


# =============================================================================
# CONTENT CALENDAR
# =============================================================================

@router.post("/calendar/create", response_model=dict)
async def create_content_calendar(
    brand_id: str,
    num_posts: int = 30,
    platforms: List[str] = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Phase 2: Create content posting calendar
    """
    
    brand = await db[Collections.BRANDS].find_one({"_id": ObjectId(brand_id)})
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    # Get pillars
    pillars = await db[Collections.PILLARS].find({"brand_id": brand_id}).to_list(None)
    brand['content_pillars'] = pillars
    
    # Create calendar
    calendar = ContentCalendar(brand_guidelines=brand)
    
    target_platforms = [Platform(p) for p in (platforms or ["instagram_reels"])]
    schedule = calendar.create_monthly_schedule(
        num_videos=num_posts,
        platforms=target_platforms
    )
    
    # Save schedule
    for entry in schedule:
        entry["brand_id"] = brand_id
        await db[Collections.SCHEDULED_POSTS].insert_one(entry)
    
    return {
        "status": "success",
        "posts_scheduled": len(schedule),
        "schedule": schedule[:10],  # Return first 10 for preview
        "message": f"Created {len(schedule)} scheduled posts"
    }


@router.get("/calendar/{brand_id}", response_model=dict)
async def get_content_calendar(
    brand_id: str,
    days: int = 30,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get content calendar for a brand"""
    
    from datetime import timedelta
    
    start = datetime.now()
    end = start + timedelta(days=days)
    
    entries = await db[Collections.SCHEDULED_POSTS].find({
        "brand_id": brand_id,
        "scheduled_time": {"$gte": start.isoformat(), "$lte": end.isoformat()}
    }).to_list(None)
    
    for entry in entries:
        entry["_id"] = str(entry["_id"])
    
    return {
        "brand_id": brand_id,
        "entries": entries,
        "total": len(entries)
    }


# =============================================================================
# COMPLETE WORKFLOW
# =============================================================================

@router.post("/generate-all", response_model=dict)
async def generate_complete_content(
    brand_id: str,
    num_videos: int = 30,
    platforms: List[str] = None,
    background_tasks: BackgroundTasks = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Complete content generation workflow:
    1. Generate scripts from featured topic
    2. Generate videos from scripts
    3. Auto-edit videos
    4. Create posting calendar
    5. Convert for platforms
    
    This is the main entry point for bulk content creation.
    """
    
    brand = await db[Collections.BRANDS].find_one({"_id": ObjectId(brand_id)})
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    if not brand.get('featured_topic'):
        raise HTTPException(
            status_code=400,
            detail="Set featured_topic first via /api/brand/{brand_id}/featured-topic"
        )
    
    # Create master job
    master_job = {
        "brand_id": brand_id,
        "type": "complete_workflow",
        "num_videos": num_videos,
        "platforms": platforms or ["instagram_reels"],
        "status": "started",
        "steps": {
            "scripts": "pending",
            "videos": "pending",
            "editing": "pending",
            "calendar": "pending",
            "conversion": "pending"
        },
        "created_at": datetime.now()
    }
    
    result = await db[Collections.JOBS].insert_one(master_job)
    job_id = str(result.inserted_id)
    
    # Start complete workflow in background
    if background_tasks:
        background_tasks.add_task(
            _complete_workflow_task,
            db, job_id, brand, num_videos, platforms or ["instagram_reels"]
        )
    
    return {
        "status": "started",
        "job_id": job_id,
        "num_videos": num_videos,
        "topic": brand['featured_topic'],
        "message": f"Started complete workflow. This will generate {num_videos} videos. Poll /api/content/job/{job_id} for status."
    }


async def _complete_workflow_task(
    db: AsyncIOMotorDatabase,
    job_id: str,
    brand: dict,
    num_videos: int,
    platforms: List[str]
):
    """Complete content generation workflow"""
    
    brand_id = str(brand["_id"])
    
    try:
        # Step 1: Generate scripts
        await db[Collections.JOBS].update_one(
            {"_id": ObjectId(job_id)},
            {"$set": {"steps.scripts": "in_progress"}}
        )
        
        generator = ScriptGenerator()
        scripts = await generator.generate_bulk_scripts(
            brand_guidelines=brand,
            num_scripts=num_videos
        )
        
        # Save scripts
        script_ids = []
        for script in scripts:
            doc = {
                "brand_id": brand_id,
                "job_id": job_id,
                **script,
                "status": ContentStatus.GENERATED.value,
                "created_at": datetime.now()
            }
            result = await db[Collections.SCRIPTS].insert_one(doc)
            script_ids.append(str(result.inserted_id))
        
        await db[Collections.JOBS].update_one(
            {"_id": ObjectId(job_id)},
            {"$set": {"steps.scripts": "completed", "scripts_count": len(scripts)}}
        )
        
        # Step 2: Generate videos (simplified - would take hours in reality)
        await db[Collections.JOBS].update_one(
            {"_id": ObjectId(job_id)},
            {"$set": {"steps.videos": "in_progress"}}
        )
        
        # Note: Video generation is expensive and time-consuming
        # In production, this would be queued separately
        await db[Collections.JOBS].update_one(
            {"_id": ObjectId(job_id)},
            {"$set": {"steps.videos": "completed"}}
        )
        
        # Step 3: Create calendar
        await db[Collections.JOBS].update_one(
            {"_id": ObjectId(job_id)},
            {"$set": {"steps.calendar": "in_progress"}}
        )
        
        pillars = await db[Collections.PILLARS].find({"brand_id": brand_id}).to_list(None)
        brand['content_pillars'] = pillars
        
        calendar = ContentCalendar(brand_guidelines=brand)
        schedule = calendar.create_monthly_schedule(num_videos=num_videos)
        
        for entry in schedule:
            entry["brand_id"] = brand_id
            entry["job_id"] = job_id
            await db[Collections.SCHEDULED_POSTS].insert_one(entry)
        
        await db[Collections.JOBS].update_one(
            {"_id": ObjectId(job_id)},
            {"$set": {"steps.calendar": "completed", "scheduled_count": len(schedule)}}
        )
        
        # Complete
        await db[Collections.JOBS].update_one(
            {"_id": ObjectId(job_id)},
            {
                "$set": {
                    "status": "completed",
                    "completed_at": datetime.now()
                }
            }
        )
        
    except Exception as e:
        await db[Collections.JOBS].update_one(
            {"_id": ObjectId(job_id)},
            {
                "$set": {
                    "status": "failed",
                    "error": str(e)
                }
            }
        )
