"""
IA Factory - Database Connection
MongoDB async client with Motor
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING
from typing import Optional
import logging

from .config import settings

logger = logging.getLogger(__name__)


class Database:
    """Database connection manager"""
    
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None


# Global database instance
database = Database()


async def connect_db() -> None:
    """Connect to MongoDB and create indexes"""
    
    logger.info(f"Connecting to MongoDB: {settings.mongodb_url}")
    
    database.client = AsyncIOMotorClient(settings.mongodb_url)
    database.db = database.client[settings.db_name]
    
    # Create indexes for optimal queries
    await create_indexes()
    
    logger.info(f"✅ Connected to database: {settings.db_name}")


async def close_db() -> None:
    """Close database connection"""
    
    if database.client:
        database.client.close()
        logger.info("❌ Database connection closed")


async def create_indexes() -> None:
    """Create database indexes for performance"""
    
    db = database.db
    
    # Brands collection
    await db.brands.create_index([("brand_name", ASCENDING)], unique=True)
    await db.brands.create_index([("created_at", DESCENDING)])
    
    # Content pillars
    await db.pillars.create_index([("brand_id", ASCENDING)])
    await db.pillars.create_index([("brand_id", ASCENDING), ("name", ASCENDING)], unique=True)
    
    # Users
    await db.users.create_index([("email", ASCENDING)], unique=True)
    await db.users.create_index([("brand_id", ASCENDING)])
    
    # Scripts
    await db.scripts.create_index([("brand_id", ASCENDING)])
    await db.scripts.create_index([("brand_id", ASCENDING), ("status", ASCENDING)])
    await db.scripts.create_index([("created_at", DESCENDING)])
    
    # Videos
    await db.videos.create_index([("brand_id", ASCENDING)])
    await db.videos.create_index([("script_id", ASCENDING)])
    await db.videos.create_index([("status", ASCENDING)])
    await db.videos.create_index([("created_at", DESCENDING)])
    
    # Content pieces
    await db.content.create_index([("brand_id", ASCENDING)])
    await db.content.create_index([("brand_id", ASCENDING), ("status", ASCENDING)])
    await db.content.create_index([("scheduled_time", ASCENDING)])
    
    # Scheduled posts
    await db.scheduled_posts.create_index([("brand_id", ASCENDING)])
    await db.scheduled_posts.create_index([("scheduled_time", ASCENDING)])
    await db.scheduled_posts.create_index([("status", ASCENDING)])
    await db.scheduled_posts.create_index([
        ("status", ASCENDING),
        ("scheduled_time", ASCENDING)
    ])
    
    # Metrics
    await db.metrics.create_index([("brand_id", ASCENDING), ("timestamp", DESCENDING)])
    await db.metrics.create_index([("content_id", ASCENDING)])
    await db.metrics.create_index([("platform", ASCENDING), ("timestamp", DESCENDING)])
    
    # Jobs queue
    await db.jobs.create_index([("status", ASCENDING)])
    await db.jobs.create_index([("created_at", DESCENDING)])
    await db.jobs.create_index([("brand_id", ASCENDING), ("status", ASCENDING)])
    
    logger.info("✅ Database indexes created")


async def get_db() -> AsyncIOMotorDatabase:
    """Get database instance (dependency injection)"""
    
    if database.db is None:
        raise RuntimeError("Database not connected. Call connect_db() first.")
    
    return database.db


# Collection helpers for type hints
class Collections:
    """Collection name constants"""
    
    BRANDS = "brands"
    PILLARS = "pillars"
    USERS = "users"
    SCRIPTS = "scripts"
    VIDEOS = "videos"
    CONTENT = "content"
    SCHEDULED_POSTS = "scheduled_posts"
    METRICS = "metrics"
    JOBS = "jobs"
    PUBLISH_RESULTS = "publish_results"
    ANALYTICS_REPORTS = "analytics_reports"
