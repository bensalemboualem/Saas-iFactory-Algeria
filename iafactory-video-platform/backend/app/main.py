"""
IAFactory Video Platform - FastAPI Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import init_db
from app.api.v1 import router as api_router

# Configuration du logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events"""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")

    # Initialize database
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

    yield

    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="""
    ## IAFactory Video Platform API

    Plateforme de création vidéo automatisée avec IA.

    ### Fonctionnalités principales:
    - **Création de projets** - Créez des projets vidéo à partir de prompts NLP
    - **Génération de scripts** - Scripts structurés avec scènes et timeline
    - **Génération d'assets** - Images, vidéos, avatars, voix, musique
    - **Montage automatique** - Assemblage et édition vidéo
    - **Publication multi-plateforme** - YouTube, TikTok, Instagram, etc.

    ### Agents IA:
    - Orchestrator Agent - Chef d'orchestre du pipeline
    - Script Agent - Génération de scripts
    - Image Agent - Génération d'images
    - Video Agent - Génération de clips vidéo
    - Avatar Agent - Avatars parlants
    - Voice Agent - TTS, STT, musique
    - Montage Agent - Édition vidéo
    - Publish Agent - Publication multi-plateforme
    """,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Vérifie l'état de santé de l'application"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Endpoint racine avec informations de base"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


# Include API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
