"""
IAFactory Video Studio Pro - Main Application
Point d'entrée FastAPI
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from config import settings

# Import des routes (à décommenter une fois créées)
# from api.routes import video, audio, scripts, publish, tokens


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Gestion du cycle de vie de l'application.
    - Startup: Initialisation des connexions, cache, etc.
    - Shutdown: Nettoyage des ressources
    """
    # === STARTUP ===
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📍 Environment: {settings.ENVIRONMENT}")
    
    # TODO: Initialiser les connexions
    # - Database
    # - Redis
    # - Services externes
    
    yield
    
    # === SHUTDOWN ===
    print("🛑 Shutting down gracefully...")
    # TODO: Fermer les connexions


# Création de l'application FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    🎬 **IAFactory Video Studio Pro** - Usine à contenu multimédia automatisée
    
    ## Fonctionnalités
    
    * **Scripts IA** - Génération de scripts viraux avec Claude Opus 4
    * **Vidéos IA** - Création de vidéos avec MiniMax/Luma
    * **Voix IA** - Synthèse vocale multilingue avec ElevenLabs
    * **Montage Auto** - Assemblage automatisé avec FFmpeg
    * **Publication** - Distribution multi-plateformes
    
    ## Marchés cibles
    
    * 🇩🇿 **Algérie** - Français, Arabe, Darija
    * 🇲🇦 **Maroc** - Français, Arabe, Darija
    * 🇹🇳 **Tunisie** - Français, Arabe
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# ============================================
# MIDDLEWARE
# ============================================

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware de logging des requêtes
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log toutes les requêtes entrantes."""
    import time
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    print(f"📥 {request.method} {request.url.path} - {response.status_code} ({process_time:.3f}s)")
    
    response.headers["X-Process-Time"] = str(process_time)
    return response


# ============================================
# ROUTES
# ============================================

# Health Check
@app.get("/health", tags=["System"])
async def health_check():
    """Vérification de l'état du service."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


# Root
@app.get("/", tags=["System"])
async def root():
    """Page d'accueil de l'API."""
    return {
        "message": f"Bienvenue sur {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }


# Informations sur les tokens
@app.get("/api/v1/info/token-costs", tags=["Info"])
async def get_token_costs():
    """Retourne la grille tarifaire des IAF-Tokens."""
    return {
        "costs": settings.TOKEN_COSTS,
        "plans": settings.PLANS,
    }


# Langues supportées
@app.get("/api/v1/info/languages", tags=["Info"])
async def get_supported_languages():
    """Retourne les langues supportées."""
    return {
        "languages": settings.LANGUAGE_CONFIG,
    }


# ============================================
# ENREGISTREMENT DES ROUTERS
# ============================================

# TODO: Décommenter une fois les routes créées
# app.include_router(
#     video.router,
#     prefix=f"{settings.API_V1_PREFIX}/video",
#     tags=["Video"]
# )
# app.include_router(
#     audio.router,
#     prefix=f"{settings.API_V1_PREFIX}/audio",
#     tags=["Audio"]
# )
# app.include_router(
#     scripts.router,
#     prefix=f"{settings.API_V1_PREFIX}/scripts",
#     tags=["Scripts"]
# )
# app.include_router(
#     publish.router,
#     prefix=f"{settings.API_V1_PREFIX}/publish",
#     tags=["Publication"]
# )
# app.include_router(
#     tokens.router,
#     prefix=f"{settings.API_V1_PREFIX}/tokens",
#     tags=["Tokens"]
# )


# ============================================
# GESTION DES ERREURS
# ============================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handler global pour les exceptions non gérées."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc) if settings.DEBUG else "Une erreur est survenue",
            "path": str(request.url.path),
        },
    )


# ============================================
# POINT D'ENTRÉE
# ============================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else 4,
    )
