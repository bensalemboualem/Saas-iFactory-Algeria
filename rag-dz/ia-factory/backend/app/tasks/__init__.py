"""
IA Factory - Celery Tasks Module
Background tasks for video processing, publishing, and analytics
"""

from celery import Celery
from app.config import settings

# Create Celery app
celery_app = Celery(
    'ia_factory',
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        'app.tasks.video_tasks',
        'app.tasks.publishing_tasks',
        'app.tasks.analytics_tasks'
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)

# Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    # Check and publish scheduled content every 5 minutes
    'check-scheduled-posts': {
        'task': 'app.tasks.publishing_tasks.check_scheduled_posts',
        'schedule': 300.0,  # 5 minutes
    },
    # Update analytics every hour
    'update-analytics': {
        'task': 'app.tasks.analytics_tasks.update_all_analytics',
        'schedule': 3600.0,  # 1 hour
    },
    # Generate daily report at midnight
    'daily-report': {
        'task': 'app.tasks.analytics_tasks.generate_daily_report',
        'schedule': 86400.0,  # 24 hours
    },
}
