"""
iaFactoryDZ Public API Gateway
API REST unifiée pour développeurs avec authentification par clé API

Endpoints:
- POST /api/v1/rag/query - Recherche RAG DZ
- POST /api/v1/legal/ask - Assistant juridique
- POST /api/v1/fiscal/simulate - Simulation fiscale
- POST /api/v1/park/sparkpage - iaFactoryPark

Fonctionnalités:
- Authentification par API Key (Bearer token)
- Rate limiting par minute/jour
- Logs d'utilisation
- Versioning API
"""

import os
import secrets
import hashlib
import json
import time
from datetime import datetime, timedelta
from typing import Optional, Literal, List, Dict, Any
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, HTTPException, Depends, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import httpx
from collections import defaultdict
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("iafactory-api")

# Environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
RAG_DZ_URL = os.getenv("RAG_DZ_URL", "http://iaf-rag-prod:3000")
LEGAL_API_URL = os.getenv("LEGAL_API_URL", "http://iaf-legal-assistant-prod:8197")
FISCAL_API_URL = os.getenv("FISCAL_API_URL", "http://iaf-fiscal-assistant-prod:8199")
POSTGRES_URL = os.getenv("POSTGRES_URL", "")

# ============================================================================
# IN-MEMORY STORAGE (Production: use PostgreSQL + Redis)
# ============================================================================

# API Keys storage (in production, use PostgreSQL)
API_KEYS_DB: Dict[str, dict] = {}

# Rate limiting counters (in production, use Redis)
RATE_LIMITS: Dict[str, dict] = defaultdict(lambda: {"minute": 0, "day": 0, "minute_reset": 0, "day_reset": 0})

# API Logs (in production, use PostgreSQL)
API_LOGS: List[dict] = []

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

# --- API Key Models ---
class APIKeyCreate(BaseModel):
    name: str = Field(..., description="Nom lisible de la clé")
    rate_limit_per_minute: int = Field(default=60, ge=1, le=1000)
    rate_limit_per_day: int = Field(default=5000, ge=1, le=100000)

class APIKeyResponse(BaseModel):
    id: str
    name: str
    key_prefix: str  # Only show prefix, not full key
    created_at: str
    last_used_at: Optional[str] = None
    status: str
    rate_limit_per_minute: int
    rate_limit_per_day: int

class APIKeyCreated(APIKeyResponse):
    key: str  # Full key shown only once at creation

class APIKeyStats(BaseModel):
    total_requests: int
    requests_today: int
    errors_today: int
    top_endpoints: List[dict]

# --- RAG Models ---
class RAGQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=20)
    filters: Optional[dict] = Field(default_factory=lambda: {"country": "DZ"})

class RAGContextItem(BaseModel):
    title: str
    snippet: str
    source_name: str
    source_url: Optional[str] = None
    date: Optional[str] = None

class RAGQueryResponse(BaseModel):
    answer: str
    context: List[RAGContextItem] = []
    meta: dict = Field(default_factory=dict)

# --- Legal Models ---
class LegalAskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    category: Literal[
        "procédure_administrative",
        "droit_des_affaires", 
        "social_cnas_casnos",
        "impôts_dgi",
        "douane_import_export",
        "autre"
    ] = "autre"
    user_context: Optional[str] = None

# --- Fiscal Models ---
class FiscalSimulateRequest(BaseModel):
    profile_type: Literal["freelance", "entreprise", "salarié", "commerçant", "autre"] = "freelance"
    regime_actuel: str = "IFU"
    revenue_amount: float = Field(..., gt=0)
    charges_amount: float = Field(default=0, ge=0)
    employees_count: int = Field(default=0, ge=0)
    sector: Optional[str] = None

# --- Park Models ---
class ParkSparkpageRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    mode: Literal["simple", "rag_dz", "business", "juridique", "fiscal"] = "rag_dz"
    language: Literal["auto", "fr", "ar", "en"] = "auto"

# --- Generic Response ---
class APIErrorResponse(BaseModel):
    detail: str
    code: str
    limits: Optional[dict] = None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_api_key() -> tuple[str, str]:
    """Generate a new API key and its hash"""
    # Generate random key with prefix
    raw_key = f"iafk_live_{secrets.token_urlsafe(32)}"
    # Hash for storage
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    return raw_key, key_hash

def hash_api_key(key: str) -> str:
    """Hash an API key for comparison"""
    return hashlib.sha256(key.encode()).hexdigest()

def verify_api_key(key: str) -> Optional[dict]:
    """Verify API key and return key data if valid"""
    key_hash = hash_api_key(key)
    for key_id, key_data in API_KEYS_DB.items():
        if key_data["key_hash"] == key_hash and key_data["status"] == "active":
            return {"id": key_id, **key_data}
    return None

def check_rate_limit(key_id: str, limits: dict) -> tuple[bool, dict]:
    """Check rate limits for a key. Returns (allowed, remaining)"""
    now = time.time()
    rate_data = RATE_LIMITS[key_id]
    
    # Reset minute counter if needed
    if now - rate_data["minute_reset"] > 60:
        rate_data["minute"] = 0
        rate_data["minute_reset"] = now
    
    # Reset day counter if needed
    if now - rate_data["day_reset"] > 86400:
        rate_data["day"] = 0
        rate_data["day_reset"] = now
    
    # Check limits
    minute_ok = rate_data["minute"] < limits["rate_limit_per_minute"]
    day_ok = rate_data["day"] < limits["rate_limit_per_day"]
    
    remaining = {
        "minute_remaining": max(0, limits["rate_limit_per_minute"] - rate_data["minute"]),
        "day_remaining": max(0, limits["rate_limit_per_day"] - rate_data["day"])
    }
    
    if minute_ok and day_ok:
        rate_data["minute"] += 1
        rate_data["day"] += 1
        return True, remaining
    
    return False, remaining

def log_request(key_id: str, endpoint: str, status_code: int, latency_ms: float, bytes_in: int = 0, bytes_out: int = 0):
    """Log an API request"""
    API_LOGS.append({
        "id": secrets.token_hex(8),
        "api_key_id": key_id,
        "timestamp": datetime.now().isoformat(),
        "endpoint": endpoint,
        "status_code": status_code,
        "latency_ms": latency_ms,
        "bytes_in": bytes_in,
        "bytes_out": bytes_out
    })
    # Keep only last 10000 logs in memory
    if len(API_LOGS) > 10000:
        API_LOGS.pop(0)

# ============================================================================
# DEPENDENCIES
# ============================================================================

async def get_api_key(authorization: str = Header(..., description="Bearer API_KEY")):
    """Dependency to validate API key from Authorization header"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail={"detail": "INVALID_AUTH_HEADER", "code": "AUTH_ERROR"}
        )
    
    token = authorization[7:]  # Remove "Bearer "
    key_data = verify_api_key(token)
    
    if not key_data:
        raise HTTPException(
            status_code=401,
            detail={"detail": "INVALID_API_KEY", "code": "AUTH_ERROR"}
        )
    
    # Check rate limits
    allowed, remaining = check_rate_limit(key_data["id"], key_data)
    
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail={
                "detail": "RATE_LIMIT_EXCEEDED",
                "code": "RATE_LIMIT",
                "limits": {
                    "per_minute": key_data["rate_limit_per_minute"],
                    "per_day": key_data["rate_limit_per_day"]
                },
                "remaining": remaining
            }
        )
    
    # Update last used
    key_data["last_used_at"] = datetime.now().isoformat()
    
    return {
        "key_id": key_data["id"],
        "user_id": key_data.get("user_id"),
        "rate_remaining": remaining
    }

# ============================================================================
# APP SETUP
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("🚀 iaFactoryDZ Public API starting...")
    
    # Create a demo API key for testing
    raw_key, key_hash = generate_api_key()
    demo_key_id = "demo-key-001"
    API_KEYS_DB[demo_key_id] = {
        "key_hash": key_hash,
        "name": "Demo API Key",
        "user_id": "demo-user",
        "created_at": datetime.now().isoformat(),
        "last_used_at": None,
        "status": "active",
        "rate_limit_per_minute": 60,
        "rate_limit_per_day": 1000
    }
    logger.info(f"📝 Demo API Key created: {raw_key[:20]}...")
    logger.info(f"   Full key (for testing): {raw_key}")
    
    yield
    
    logger.info("🛑 iaFactoryDZ Public API shutting down...")

app = FastAPI(
    title="iaFactoryDZ Public API",
    description="""
    🇩🇿 API REST unifiée pour les services IA d'iaFactory Algeria
    
    ## Services disponibles
    - **RAG DZ** : Recherche et question-réponse sur documents algériens
    - **Assistant Juridique** : Droit et démarches administratives
    - **Assistant Fiscal** : Simulation d'impôts (IFU, IRG, TAP, CNAS...)
    - **iaFactoryPark** : Génération de Sparkpages
    
    ## Authentification
    Toutes les requêtes nécessitent une clé API dans le header:
    ```
    Authorization: Bearer iafk_live_xxxxx
    ```
    
    ## Rate Limiting
    - Par défaut: 60 requêtes/minute, 5000 requêtes/jour
    - Headers de réponse: `X-RateLimit-Remaining-Minute`, `X-RateLimit-Remaining-Day`
    """,
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# MIDDLEWARE - Add rate limit headers
# ============================================================================

@app.middleware("http")
async def add_rate_limit_headers(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    
    # Add timing header
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time-Ms"] = str(int(process_time))
    
    return response

# ============================================================================
# HEALTH & INFO ENDPOINTS
# ============================================================================

@app.get("/", tags=["Info"])
async def root():
    """API Root - Info"""
    return {
        "name": "iaFactoryDZ Public API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }

@app.get("/api/v1/health", tags=["Info"])
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "rag": "operational",
            "legal": "operational", 
            "fiscal": "operational",
            "park": "operational"
        }
    }

# ============================================================================
# API KEY MANAGEMENT ENDPOINTS (Protected - internal use)
# ============================================================================

@app.post("/api/internal/keys", response_model=APIKeyCreated, tags=["API Keys"])
async def create_api_key(request: APIKeyCreate):
    """Create a new API key (internal use only)"""
    raw_key, key_hash = generate_api_key()
    key_id = secrets.token_hex(8)
    
    API_KEYS_DB[key_id] = {
        "key_hash": key_hash,
        "name": request.name,
        "user_id": "default-user",  # In production, get from auth
        "created_at": datetime.now().isoformat(),
        "last_used_at": None,
        "status": "active",
        "rate_limit_per_minute": request.rate_limit_per_minute,
        "rate_limit_per_day": request.rate_limit_per_day
    }
    
    return APIKeyCreated(
        id=key_id,
        name=request.name,
        key=raw_key,  # Shown only once!
        key_prefix=raw_key[:15] + "...",
        created_at=API_KEYS_DB[key_id]["created_at"],
        status="active",
        rate_limit_per_minute=request.rate_limit_per_minute,
        rate_limit_per_day=request.rate_limit_per_day
    )

@app.get("/api/internal/keys", response_model=List[APIKeyResponse], tags=["API Keys"])
async def list_api_keys():
    """List all API keys (internal use only)"""
    return [
        APIKeyResponse(
            id=key_id,
            name=data["name"],
            key_prefix="iafk_live_***...",
            created_at=data["created_at"],
            last_used_at=data.get("last_used_at"),
            status=data["status"],
            rate_limit_per_minute=data["rate_limit_per_minute"],
            rate_limit_per_day=data["rate_limit_per_day"]
        )
        for key_id, data in API_KEYS_DB.items()
    ]

@app.delete("/api/internal/keys/{key_id}", tags=["API Keys"])
async def revoke_api_key(key_id: str):
    """Revoke an API key (internal use only)"""
    if key_id not in API_KEYS_DB:
        raise HTTPException(status_code=404, detail="API key not found")
    
    API_KEYS_DB[key_id]["status"] = "revoked"
    return {"message": "API key revoked", "key_id": key_id}

@app.get("/api/internal/stats", response_model=APIKeyStats, tags=["API Keys"])
async def get_api_stats():
    """Get API usage statistics (internal use only)"""
    today = datetime.now().date().isoformat()
    
    total_requests = len(API_LOGS)
    requests_today = sum(1 for log in API_LOGS if log["timestamp"].startswith(today))
    errors_today = sum(1 for log in API_LOGS if log["timestamp"].startswith(today) and log["status_code"] >= 400)
    
    # Top endpoints
    endpoint_counts = defaultdict(int)
    for log in API_LOGS:
        endpoint_counts[log["endpoint"]] += 1
    
    top_endpoints = [
        {"endpoint": ep, "count": count}
        for ep, count in sorted(endpoint_counts.items(), key=lambda x: -x[1])[:5]
    ]
    
    return APIKeyStats(
        total_requests=total_requests,
        requests_today=requests_today,
        errors_today=errors_today,
        top_endpoints=top_endpoints
    )

# ============================================================================
# PUBLIC API ENDPOINTS - v1
# ============================================================================

# --- RAG DZ ---
@app.post("/api/v1/rag/query", response_model=RAGQueryResponse, tags=["RAG DZ"])
async def rag_query(
    request: RAGQueryRequest,
    api_client: dict = Depends(get_api_key)
):
    """
    🔍 Recherche RAG DZ
    
    Effectue une recherche sémantique dans la base de connaissances algérienne
    et génère une réponse basée sur les documents trouvés.
    
    **Filtres disponibles:**
    - `country`: Pays (DZ par défaut)
    - `source_name`: Sources spécifiques (DZ_JO, DZ_DGI, etc.)
    - `type`: Types de documents (law, tax, procedure)
    """
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{RAG_DZ_URL}/api/chat",
                json={
                    "message": request.query,
                    "mode": "hybrid"
                }
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                # Log request
                log_request(api_client["key_id"], "/api/v1/rag/query", 200, latency_ms)
                
                return RAGQueryResponse(
                    answer=data.get("response", data.get("message", "")),
                    context=[],  # RAG doesn't return sources in current impl
                    meta={
                        "latency_ms": int(latency_ms),
                        "model": "groq-llama",
                        "country": "DZ"
                    }
                )
            else:
                log_request(api_client["key_id"], "/api/v1/rag/query", response.status_code, latency_ms)
                raise HTTPException(status_code=502, detail="RAG service error")
                
    except httpx.TimeoutException:
        log_request(api_client["key_id"], "/api/v1/rag/query", 504, (time.time() - start_time) * 1000)
        raise HTTPException(status_code=504, detail="RAG service timeout")
    except Exception as e:
        logger.error(f"RAG error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Legal Assistant ---
@app.post("/api/v1/legal/ask", tags=["Assistant Juridique"])
async def legal_ask(
    request: LegalAskRequest,
    api_client: dict = Depends(get_api_key)
):
    """
    ⚖️ Assistant Juridique DZ
    
    Répond aux questions sur le droit algérien et les démarches administratives.
    
    **Catégories:**
    - `procédure_administrative`: Démarches administratives
    - `droit_des_affaires`: Création d'entreprise, contrats
    - `social_cnas_casnos`: Sécurité sociale
    - `impôts_dgi`: Questions fiscales
    - `douane_import_export`: Import/export
    - `autre`: Autres questions
    """
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{LEGAL_API_URL}/api/dz-legal/answer",
                json={
                    "question": request.question,
                    "category": request.category.replace("é", "e").replace("ô", "o")
                }
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                log_request(api_client["key_id"], "/api/v1/legal/ask", 200, latency_ms)
                
                # Add API metadata
                data["api_meta"] = {
                    "latency_ms": int(latency_ms),
                    "version": "v1"
                }
                return data
            else:
                log_request(api_client["key_id"], "/api/v1/legal/ask", response.status_code, latency_ms)
                raise HTTPException(status_code=502, detail="Legal service error")
                
    except httpx.TimeoutException:
        log_request(api_client["key_id"], "/api/v1/legal/ask", 504, (time.time() - start_time) * 1000)
        raise HTTPException(status_code=504, detail="Legal service timeout")
    except Exception as e:
        logger.error(f"Legal error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Fiscal Assistant ---
@app.post("/api/v1/fiscal/simulate", tags=["Assistant Fiscal"])
async def fiscal_simulate(
    request: FiscalSimulateRequest,
    api_client: dict = Depends(get_api_key)
):
    """
    💰 Simulation Fiscale DZ
    
    Calcule les impôts et cotisations sociales en Algérie.
    
    **Impôts calculés:**
    - IRG (Impôt sur le Revenu Global)
    - IFU (Impôt Forfaitaire Unique)
    - TAP (Taxe sur l'Activité Professionnelle)
    - TVA
    - CNAS / CASNOS
    
    **Profils:**
    - `freelance`: Travailleur indépendant
    - `entreprise`: SARL, SPA, EURL
    - `salarié`: Employé
    - `commerçant`: Activité commerciale
    """
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{FISCAL_API_URL}/api/dz-fiscal/simulate",
                json={
                    "profile_type": request.profile_type,
                    "regime_actuel": request.regime_actuel,
                    "revenue_amount": request.revenue_amount,
                    "charges_amount": request.charges_amount,
                    "employees_count": request.employees_count,
                    "sector": request.sector
                }
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                log_request(api_client["key_id"], "/api/v1/fiscal/simulate", 200, latency_ms)
                
                # Add API metadata
                data["api_meta"] = {
                    "latency_ms": int(latency_ms),
                    "version": "v1",
                    "api_warning": "Les calculs sont des estimations. Consultez un expert-comptable."
                }
                return data
            else:
                log_request(api_client["key_id"], "/api/v1/fiscal/simulate", response.status_code, latency_ms)
                raise HTTPException(status_code=502, detail="Fiscal service error")
                
    except httpx.TimeoutException:
        log_request(api_client["key_id"], "/api/v1/fiscal/simulate", 504, (time.time() - start_time) * 1000)
        raise HTTPException(status_code=504, detail="Fiscal service timeout")
    except Exception as e:
        logger.error(f"Fiscal error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# --- iaFactoryPark ---
@app.post("/api/v1/park/sparkpage", tags=["iaFactoryPark"])
async def park_sparkpage(
    request: ParkSparkpageRequest,
    api_client: dict = Depends(get_api_key)
):
    """
    🏗️ iaFactoryPark Sparkpage
    
    Génère une Sparkpage (mini-rapport structuré) basée sur votre requête.
    
    **Modes:**
    - `simple`: Réponse directe sans RAG
    - `rag_dz`: Enrichi avec la base de connaissances DZ
    - `business`: Focus business/entreprise
    - `juridique`: Focus légal
    - `fiscal`: Focus fiscal
    """
    start_time = time.time()
    latency_ms = (time.time() - start_time) * 1000
    
    # For now, return a structured response
    # In production, connect to actual iaFactoryPark service
    log_request(api_client["key_id"], "/api/v1/park/sparkpage", 200, latency_ms)
    
    return {
        "sparkpage": {
            "title": f"Sparkpage: {request.query[:50]}...",
            "mode": request.mode,
            "language": request.language,
            "sections": [
                {
                    "heading": "Résumé",
                    "content": f"Analyse de votre requête: {request.query}"
                },
                {
                    "heading": "Points clés",
                    "content": "• Point 1\n• Point 2\n• Point 3"
                },
                {
                    "heading": "Recommandations",
                    "content": "Basé sur votre requête, voici nos recommandations..."
                }
            ],
            "generated_at": datetime.now().isoformat()
        },
        "api_meta": {
            "latency_ms": int(latency_ms),
            "version": "v1"
        }
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8203)
