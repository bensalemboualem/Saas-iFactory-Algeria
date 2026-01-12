from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog

from app.core.config import settings
from app.api.routes import video, audio, templates, credits, auth, pipeline
from app.api.routes import scripts, storyboard, production, distribution
from app.api.routes import agents


# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(20),  # INFO level
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting IA Factory Video Studio API", version=settings.APP_VERSION)
    yield
    # Shutdown
    logger.info("Shutting down API")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API de génération vidéo IA pour le marché algérien",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["auth"])
app.include_router(video.router, prefix=f"{settings.API_V1_PREFIX}/video", tags=["video"])
app.include_router(audio.router, prefix=f"{settings.API_V1_PREFIX}/audio", tags=["audio"])
app.include_router(templates.router, prefix=f"{settings.API_V1_PREFIX}/templates", tags=["templates"])
app.include_router(credits.router, prefix=f"{settings.API_V1_PREFIX}/credits", tags=["credits"])
app.include_router(pipeline.router, prefix=f"{settings.API_V1_PREFIX}/pipeline", tags=["pipeline"])

# Agents & Production Routes
app.include_router(agents.router, prefix=f"{settings.API_V1_PREFIX}/agents", tags=["agents"])
app.include_router(scripts.router, prefix=f"{settings.API_V1_PREFIX}/scripts", tags=["scripts"])
app.include_router(storyboard.router, prefix=f"{settings.API_V1_PREFIX}/storyboard", tags=["storyboard"])
app.include_router(production.router, prefix=f"{settings.API_V1_PREFIX}/production", tags=["production"])
app.include_router(distribution.router, prefix=f"{settings.API_V1_PREFIX}/distribution", tags=["distribution"])


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
