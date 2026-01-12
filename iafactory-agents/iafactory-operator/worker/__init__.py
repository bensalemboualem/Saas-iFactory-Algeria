"""
IA Factory Operator - Worker Package
"""

from worker.tasks import process_video_job

__all__ = ["process_video_job"]
