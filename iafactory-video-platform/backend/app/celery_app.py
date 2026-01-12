"""
Celery Application Configuration
Background task processing for video generation pipeline
"""
from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "iafactory_video",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.pipeline",
        "app.tasks.generation",
        "app.tasks.publishing",
    ]
)

# Celery configuration
celery_app.conf.update(
    # Task settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,

    # Task execution
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_time_limit=3600,  # 1 hour max per task
    task_soft_time_limit=3300,  # 55 minutes soft limit

    # Worker settings
    worker_prefetch_multiplier=1,
    worker_concurrency=4,

    # Result settings
    result_expires=86400,  # 24 hours

    # Rate limiting
    task_default_rate_limit="10/m",

    # Retry settings
    task_default_retry_delay=60,
    task_max_retries=3,

    # Beat schedule for periodic tasks
    beat_schedule={
        "cleanup-old-files": {
            "task": "app.tasks.pipeline.cleanup_old_files",
            "schedule": 3600.0,  # Every hour
        },
        "sync-analytics": {
            "task": "app.tasks.publishing.sync_analytics",
            "schedule": 1800.0,  # Every 30 minutes
        },
        "process-scheduled-publishes": {
            "task": "app.tasks.publishing.process_scheduled",
            "schedule": 60.0,  # Every minute
        },
    },
)

# Task routing
celery_app.conf.task_routes = {
    "app.tasks.generation.*": {"queue": "generation"},
    "app.tasks.publishing.*": {"queue": "publishing"},
    "app.tasks.pipeline.*": {"queue": "pipeline"},
}
