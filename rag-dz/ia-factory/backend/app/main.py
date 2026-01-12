"""
IA Factory - Complete Content Automation Platform
FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import logging
import os
from datetime import datetime

from app.config import settings
from app.database import connect_db, close_db
from app.api import brand, content, distribution, analytics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    # Startup
    logger.info("Starting IA Factory Platform...")
    await connect_db()
    
    # Create upload directories
    os.makedirs(settings.upload_dir, exist_ok=True)
    os.makedirs(settings.output_dir, exist_ok=True)
    
    logger.info(f"IA Factory v{settings.app_version} started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down IA Factory Platform...")
    await close_db()


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="""
    IA Factory - Complete Content Automation Platform
    
    Une plateforme d'automatisation de contenu propulsée par l'IA pour:
    - Configuration de marque et voix
    - Génération automatique de scripts avec Claude
    - Création de vidéos avec VEO 3
    - Édition automatique avec FFmpeg
    - Publication multi-plateformes
    - Analytics et optimisation
    """,
    version=settings.app_version,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = datetime.now()
    response = await call_next(request)
    duration = (datetime.now() - start_time).total_seconds()
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Duration: {duration:.3f}s"
    )
    
    return response


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "Une erreur interne s'est produite",
            "details": str(exc) if settings.debug else None
        }
    )


# Include API routers
app.include_router(
    brand.router,
    prefix="/api/brand",
    tags=["Brand Configuration"]
)

app.include_router(
    content.router,
    prefix="/api/content",
    tags=["Content Generation"]
)

app.include_router(
    distribution.router,
    prefix="/api/distribution",
    tags=["Distribution & Publishing"]
)

app.include_router(
    analytics.router,
    prefix="/api/analytics",
    tags=["Analytics & Optimization"]
)


# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "timestamp": datetime.utcnow().isoformat()
    }


# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "Complete Content Automation Platform",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "brand": "/api/brand",
            "content": "/api/content",
            "distribution": "/api/distribution",
            "analytics": "/api/analytics"
        }
    }


# API status endpoint
@app.get("/api/status", tags=["System"])
async def api_status():
    """Get detailed API status"""
    return {
        "status": "operational",
        "services": {
            "mongodb": "connected",
            "redis": "connected" if settings.redis_url else "not_configured",
            "anthropic": "configured" if settings.anthropic_api_key else "not_configured",
            "replicate": "configured" if settings.replicate_api_token else "not_configured"
        },
        "features": {
            "script_generation": True,
            "video_generation": bool(settings.replicate_api_token),
            "auto_editing": True,
            "multi_platform_publishing": True,
            "analytics": True
        },
        "version": settings.app_version,
        "environment": "production" if not settings.debug else "development"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
