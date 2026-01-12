from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import time
import logging

from .middleware import RequestIDMiddleware, AuthMiddleware
from .monitoring import init_metrics
from .routers import test, upload, query

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

init_metrics()

app = FastAPI(
    title="RAG.dz API",
    version="1.0.0",
    description="Plateforme RAG multimodale trilingue pour l'Algerie"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)
app.add_middleware(RequestIDMiddleware)

# Routes
app.include_router(test.router, prefix="/api", tags=["Test"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(query.router, prefix="/api", tags=["Query"])

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": time.time(), "service": "RAG.dz"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/")
async def root():
    return {"message": "RAG.dz API", "docs": "/docs"}
