"""
Workflow State Manager - Redis-based State Persistence
Replaces in-memory workflow tracking for production scalability
"""
import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from enum import Enum
import asyncio

from pydantic import BaseModel
import redis.asyncio as redis

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class WorkflowStage(str, Enum):
    """Workflow execution stages"""
    INIT = "init"
    BMAD_BRAINSTORM = "bmad_brainstorm"
    BMAD_PLANNING = "bmad_planning"
    ORCHESTRATOR_PROCESS = "orchestrator_process"
    ARCHON_KNOWLEDGE = "archon_knowledge"
    PROMPT_CREATION = "prompt_creation"
    BOLT_EXECUTION = "bolt_execution"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowStatus(str, Enum):
    """Workflow status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StageResult(BaseModel):
    """Result of a workflow stage"""
    stage: WorkflowStage
    status: WorkflowStatus
    output: Dict[str, Any] = {}
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration_ms: Optional[int] = None


class WorkflowState(BaseModel):
    """Complete workflow state"""
    workflow_id: str
    name: str
    description: str = ""
    user_id: str
    tenant_id: Optional[str] = None

    # Current state
    current_stage: WorkflowStage = WorkflowStage.INIT
    status: WorkflowStatus = WorkflowStatus.PENDING

    # Stage results
    stages: Dict[str, StageResult] = {}

    # Outputs
    brainstorm_result: Optional[str] = None
    project_plan: Optional[str] = None
    generated_prompt: Optional[str] = None
    bolt_project_id: Optional[str] = None

    # Metadata
    created_at: str = ""
    updated_at: str = ""
    completed_at: Optional[str] = None

    # Configuration
    selected_agents: List[str] = ["bmm-pm", "bmm-architect", "bmm-developer"]
    config: Dict[str, Any] = {}

    def __init__(self, **data):
        if not data.get("created_at"):
            data["created_at"] = datetime.utcnow().isoformat()
        if not data.get("updated_at"):
            data["updated_at"] = datetime.utcnow().isoformat()
        super().__init__(**data)


class WorkflowStateManager:
    """
    Redis-based workflow state manager
    Provides distributed state management for horizontal scaling
    """

    # Redis key prefixes
    WORKFLOW_KEY = "workflow:{workflow_id}"
    USER_WORKFLOWS_KEY = "user:{user_id}:workflows"
    ACTIVE_WORKFLOWS_KEY = "active_workflows"
    WORKFLOW_EVENTS_KEY = "workflow:{workflow_id}:events"

    # TTL settings
    WORKFLOW_TTL = 86400 * 7  # 7 days
    EVENT_TTL = 86400  # 1 day

    def __init__(self):
        self._redis: Optional[redis.Redis] = None
        self._pubsub = None

    async def connect(self):
        """Initialize Redis connection"""
        if not self._redis:
            try:
                self._redis = redis.Redis.from_url(
                    settings.redis_url,
                    encoding="utf-8",
                    decode_responses=True
                )
                await self._redis.ping()
                logger.info("WorkflowStateManager connected to Redis")
            except Exception as e:
                logger.error(f"Redis connection failed: {e}")
                raise

    async def disconnect(self):
        """Close Redis connection"""
        if self._redis:
            await self._redis.close()
            self._redis = None

    async def _ensure_connected(self):
        """Ensure Redis connection is active"""
        if not self._redis:
            await self.connect()

    # ================================================
    # CRUD Operations
    # ================================================

    async def create_workflow(self, workflow: WorkflowState) -> WorkflowState:
        """Create new workflow"""
        await self._ensure_connected()

        key = self.WORKFLOW_KEY.format(workflow_id=workflow.workflow_id)

        # Store workflow
        await self._redis.setex(
            key,
            self.WORKFLOW_TTL,
            workflow.model_dump_json()
        )

        # Add to user's workflow list
        await self._redis.sadd(
            self.USER_WORKFLOWS_KEY.format(user_id=workflow.user_id),
            workflow.workflow_id
        )

        # Add to active workflows
        await self._redis.sadd(self.ACTIVE_WORKFLOWS_KEY, workflow.workflow_id)

        # Publish creation event
        await self._publish_event(workflow.workflow_id, "created", workflow.model_dump())

        logger.info(f"Workflow created: {workflow.workflow_id}")
        return workflow

    async def get_workflow(self, workflow_id: str) -> Optional[WorkflowState]:
        """Get workflow by ID"""
        await self._ensure_connected()

        key = self.WORKFLOW_KEY.format(workflow_id=workflow_id)
        data = await self._redis.get(key)

        if data:
            return WorkflowState.model_validate_json(data)
        return None

    async def update_workflow(self, workflow: WorkflowState) -> WorkflowState:
        """Update workflow state"""
        await self._ensure_connected()

        workflow.updated_at = datetime.utcnow().isoformat()

        key = self.WORKFLOW_KEY.format(workflow_id=workflow.workflow_id)
        await self._redis.setex(
            key,
            self.WORKFLOW_TTL,
            workflow.model_dump_json()
        )

        # Publish update event
        await self._publish_event(workflow.workflow_id, "updated", {
            "stage": workflow.current_stage,
            "status": workflow.status
        })

        return workflow

    async def delete_workflow(self, workflow_id: str, user_id: str):
        """Delete workflow"""
        await self._ensure_connected()

        key = self.WORKFLOW_KEY.format(workflow_id=workflow_id)

        # Remove from all sets
        await self._redis.delete(key)
        await self._redis.srem(
            self.USER_WORKFLOWS_KEY.format(user_id=user_id),
            workflow_id
        )
        await self._redis.srem(self.ACTIVE_WORKFLOWS_KEY, workflow_id)

        # Publish deletion event
        await self._publish_event(workflow_id, "deleted", {})

        logger.info(f"Workflow deleted: {workflow_id}")

    # ================================================
    # Stage Management
    # ================================================

    async def start_stage(
        self,
        workflow_id: str,
        stage: WorkflowStage
    ) -> Optional[WorkflowState]:
        """Start a workflow stage"""
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return None

        # Create stage result
        stage_result = StageResult(
            stage=stage,
            status=WorkflowStatus.RUNNING,
            started_at=datetime.utcnow().isoformat()
        )

        workflow.stages[stage.value] = stage_result
        workflow.current_stage = stage
        workflow.status = WorkflowStatus.RUNNING

        await self.update_workflow(workflow)

        # Publish stage event
        await self._publish_event(workflow_id, "stage_started", {
            "stage": stage.value
        })

        return workflow

    async def complete_stage(
        self,
        workflow_id: str,
        stage: WorkflowStage,
        output: Dict[str, Any],
        next_stage: Optional[WorkflowStage] = None
    ) -> Optional[WorkflowState]:
        """Complete a workflow stage"""
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return None

        # Update stage result
        stage_result = workflow.stages.get(stage.value)
        if stage_result:
            stage_result.status = WorkflowStatus.COMPLETED
            stage_result.output = output
            stage_result.completed_at = datetime.utcnow().isoformat()

            # Calculate duration
            if stage_result.started_at:
                started = datetime.fromisoformat(stage_result.started_at)
                completed = datetime.fromisoformat(stage_result.completed_at)
                stage_result.duration_ms = int((completed - started).total_seconds() * 1000)

            workflow.stages[stage.value] = stage_result

        # Update workflow state
        if next_stage:
            workflow.current_stage = next_stage
        elif stage == WorkflowStage.BOLT_EXECUTION:
            workflow.current_stage = WorkflowStage.COMPLETED
            workflow.status = WorkflowStatus.COMPLETED
            workflow.completed_at = datetime.utcnow().isoformat()

            # Remove from active workflows
            await self._redis.srem(self.ACTIVE_WORKFLOWS_KEY, workflow_id)

        await self.update_workflow(workflow)

        # Publish completion event
        await self._publish_event(workflow_id, "stage_completed", {
            "stage": stage.value,
            "output_keys": list(output.keys())
        })

        return workflow

    async def fail_stage(
        self,
        workflow_id: str,
        stage: WorkflowStage,
        error: str
    ) -> Optional[WorkflowState]:
        """Mark stage as failed"""
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return None

        # Update stage result
        stage_result = workflow.stages.get(stage.value, StageResult(stage=stage, status=WorkflowStatus.RUNNING))
        stage_result.status = WorkflowStatus.FAILED
        stage_result.error = error
        stage_result.completed_at = datetime.utcnow().isoformat()

        workflow.stages[stage.value] = stage_result
        workflow.current_stage = WorkflowStage.FAILED
        workflow.status = WorkflowStatus.FAILED

        # Remove from active workflows
        await self._redis.srem(self.ACTIVE_WORKFLOWS_KEY, workflow_id)

        await self.update_workflow(workflow)

        # Publish failure event
        await self._publish_event(workflow_id, "stage_failed", {
            "stage": stage.value,
            "error": error
        })

        return workflow

    # ================================================
    # Query Operations
    # ================================================

    async def get_user_workflows(
        self,
        user_id: str,
        limit: int = 20
    ) -> List[WorkflowState]:
        """Get all workflows for a user"""
        await self._ensure_connected()

        workflow_ids = await self._redis.smembers(
            self.USER_WORKFLOWS_KEY.format(user_id=user_id)
        )

        workflows = []
        for wf_id in list(workflow_ids)[:limit]:
            workflow = await self.get_workflow(wf_id)
            if workflow:
                workflows.append(workflow)

        # Sort by created_at descending
        workflows.sort(key=lambda w: w.created_at, reverse=True)
        return workflows

    async def get_active_workflows(self) -> List[WorkflowState]:
        """Get all active workflows"""
        await self._ensure_connected()

        workflow_ids = await self._redis.smembers(self.ACTIVE_WORKFLOWS_KEY)

        workflows = []
        for wf_id in workflow_ids:
            workflow = await self.get_workflow(wf_id)
            if workflow and workflow.status == WorkflowStatus.RUNNING:
                workflows.append(workflow)

        return workflows

    async def get_workflow_stats(self) -> Dict[str, Any]:
        """Get workflow statistics"""
        await self._ensure_connected()

        active_count = await self._redis.scard(self.ACTIVE_WORKFLOWS_KEY)

        return {
            "active_workflows": active_count,
            "timestamp": datetime.utcnow().isoformat()
        }

    # ================================================
    # Event System
    # ================================================

    async def _publish_event(
        self,
        workflow_id: str,
        event_type: str,
        data: Dict[str, Any]
    ):
        """Publish workflow event"""
        await self._ensure_connected()

        event = {
            "type": event_type,
            "workflow_id": workflow_id,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Store event in list
        event_key = self.WORKFLOW_EVENTS_KEY.format(workflow_id=workflow_id)
        await self._redis.lpush(event_key, json.dumps(event))
        await self._redis.expire(event_key, self.EVENT_TTL)

        # Publish to channel
        channel = f"workflow:{workflow_id}"
        await self._redis.publish(channel, json.dumps(event))

    async def get_workflow_events(
        self,
        workflow_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get workflow event history"""
        await self._ensure_connected()

        event_key = self.WORKFLOW_EVENTS_KEY.format(workflow_id=workflow_id)
        events = await self._redis.lrange(event_key, 0, limit - 1)

        return [json.loads(e) for e in events]

    async def subscribe_workflow(self, workflow_id: str):
        """Subscribe to workflow events (async generator)"""
        await self._ensure_connected()

        pubsub = self._redis.pubsub()
        channel = f"workflow:{workflow_id}"
        await pubsub.subscribe(channel)

        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    yield json.loads(message["data"])
        finally:
            await pubsub.unsubscribe(channel)
            await pubsub.close()


# Singleton instance
workflow_state_manager = WorkflowStateManager()


# Lifecycle hooks
async def init_workflow_state():
    """Initialize workflow state manager"""
    await workflow_state_manager.connect()


async def shutdown_workflow_state():
    """Shutdown workflow state manager"""
    await workflow_state_manager.disconnect()
