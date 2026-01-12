# IA Factory API Routes
from .brand import router as brand_router
from .content import router as content_router
from .distribution import router as distribution_router
from .analytics import router as analytics_router

__all__ = [
    "brand_router",
    "content_router", 
    "distribution_router",
    "analytics_router"
]
