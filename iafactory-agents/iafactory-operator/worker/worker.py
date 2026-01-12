"""
IA Factory Operator - RQ Worker
Background worker for video processing
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from redis import Redis
from rq import Worker, Queue

from core.config import settings

# Create Redis connection
redis_conn = Redis.from_url(settings.redis_url)

# Create queue
queue = Queue("video-operator", connection=redis_conn)


def run_worker():
    """Run the RQ worker"""
    worker = Worker(
        queues=[queue],
        connection=redis_conn,
        name=f"video-worker-{os.getpid()}",
    )
    worker.work(with_scheduler=True)


if __name__ == "__main__":
    run_worker()
