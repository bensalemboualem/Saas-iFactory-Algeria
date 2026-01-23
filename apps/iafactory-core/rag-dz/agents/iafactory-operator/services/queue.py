"""
IA Factory Operator - Queue Service
Redis-based job queue using RQ
"""

import json
from typing import Optional, Dict, Any, Callable
from datetime import datetime, timedelta

import structlog
from redis import Redis
from rq import Queue, Worker
from rq.job import Job

from core.config import settings

logger = structlog.get_logger(__name__)


class QueueService:
    """
    Job queue service using Redis + RQ.
    Handles:
    - Job submission
    - Status tracking
    - Progress updates
    - Result retrieval
    """
    
    def __init__(self, redis_url: Optional[str] = None):
        self.redis_url = redis_url or settings.redis_url
        self._redis = None
        self._queue = None
    
    @property
    def redis(self) -> Redis:
        """Lazy-load Redis connection"""
        if self._redis is None:
            self._redis = Redis.from_url(self.redis_url)
        return self._redis
    
    @property
    def queue(self) -> Queue:
        """Get the main job queue"""
        if self._queue is None:
            self._queue = Queue(
                name="video-operator",
                connection=self.redis,
                default_timeout=600,  # 10 minutes
            )
        return self._queue
    
    def enqueue_job(
        self,
        func: Callable,
        *args,
        job_id: Optional[str] = None,
        job_timeout: Optional[int] = None,
        **kwargs,
    ) -> str:
        """
        Enqueue a job for processing.
        Returns job ID.
        """
        job = self.queue.enqueue(
            func,
            *args,
            job_id=job_id,
            job_timeout=job_timeout or 600,
            **kwargs,
        )
        
        logger.info(f"Enqueued job: {job.id}")
        return job.id
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID"""
        try:
            return Job.fetch(job_id, connection=self.redis)
        except Exception:
            return None
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get job status and metadata"""
        job = self.get_job(job_id)
        
        if not job:
            return {
                "job_id": job_id,
                "status": "not_found",
                "error": "Job not found",
            }
        
        # Get custom progress from Redis
        progress_key = f"job:{job_id}:progress"
        progress_data = self.redis.get(progress_key)
        
        progress = 0
        current_stage = ""
        if progress_data:
            try:
                data = json.loads(progress_data)
                progress = data.get("progress", 0)
                current_stage = data.get("stage", "")
            except json.JSONDecodeError:
                pass
        
        return {
            "job_id": job_id,
            "status": job.get_status(),
            "progress": progress,
            "current_stage": current_stage,
            "created_at": job.created_at.isoformat() if job.created_at else None,
            "started_at": job.started_at.isoformat() if job.started_at else None,
            "ended_at": job.ended_at.isoformat() if job.ended_at else None,
            "result": job.result if job.is_finished else None,
            "error": str(job.exc_info) if job.is_failed else None,
        }
    
    def update_progress(
        self,
        job_id: str,
        progress: int,
        stage: str = "",
        message: str = "",
    ):
        """Update job progress"""
        progress_key = f"job:{job_id}:progress"
        data = {
            "progress": progress,
            "stage": stage,
            "message": message,
            "updated_at": datetime.utcnow().isoformat(),
        }
        self.redis.setex(
            progress_key,
            timedelta(hours=24),
            json.dumps(data),
        )
    
    def store_result(self, job_id: str, result: Dict[str, Any]):
        """Store job result in Redis"""
        result_key = f"job:{job_id}:result"
        self.redis.setex(
            result_key,
            timedelta(days=7),  # Keep for 7 days
            json.dumps(result),
        )
    
    def get_result(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get stored job result"""
        result_key = f"job:{job_id}:result"
        data = self.redis.get(result_key)
        
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                pass
        return None
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a pending job"""
        job = self.get_job(job_id)
        if job and job.get_status() in ["queued", "scheduled"]:
            job.cancel()
            return True
        return False
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Get queue statistics"""
        return {
            "name": self.queue.name,
            "count": len(self.queue),
            "failed": self.queue.failed_job_registry.count,
            "started": self.queue.started_job_registry.count,
            "finished": self.queue.finished_job_registry.count,
        }


# =============================================================================
# SINGLETON
# =============================================================================

_queue_service: Optional[QueueService] = None


def get_queue_service() -> QueueService:
    """Get or create queue service singleton"""
    global _queue_service
    if _queue_service is None:
        _queue_service = QueueService()
    return _queue_service
