"""
API v1 Router
"""
from fastapi import APIRouter
from app.api.v1 import projects, scripts, assets, videos, publish, agents

router = APIRouter()

# Include all route modules
router.include_router(projects.router, prefix="/projects", tags=["Projects"])
router.include_router(scripts.router, prefix="/scripts", tags=["Scripts"])
router.include_router(assets.router, prefix="/assets", tags=["Assets"])
router.include_router(videos.router, prefix="/videos", tags=["Videos"])
router.include_router(publish.router, prefix="/publish", tags=["Publish"])
router.include_router(agents.router, prefix="/agents", tags=["Agents"])
