"""
Archon RAG Sovereign Server - Point d'entrée alternatif
Expose l'endpoint /api/rag/query pour le frontend Bolt-DIY
Port: 8181 (distinct du backend principal 8180)
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import des routes RAG existantes
from app.routers.query import router as query_router
from app.routers.knowledge import router as knowledge_router
from app.routers.upload import router as upload_router
from app.routers.ingest import router as ingest_router

app = FastAPI(
    title="Archon RAG Sovereign Server",
    description="Serveur RAG souverain - Base de connaissances IA Factory",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS pour Bolt-DIY
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes RAG
app.include_router(query_router, prefix="/api/rag", tags=["RAG Query"])
app.include_router(knowledge_router, prefix="/api/rag", tags=["Knowledge Base"])
app.include_router(upload_router, prefix="/api/rag", tags=["Document Upload"])
app.include_router(ingest_router, prefix="/api/rag", tags=["Document Ingest"])


@app.get("/health")
async def health():
    """Health check pour Docker/Kubernetes"""
    return {"status": "healthy", "service": "archon-rag-sovereign"}


@app.get("/")
async def root():
    return {
        "service": "Archon RAG Sovereign Server",
        "version": "1.0.0",
        "endpoints": {
            "query": "/api/rag/query",
            "search": "/api/rag/search",
            "upload": "/api/rag/upload",
            "knowledge": "/api/rag/knowledge"
        },
        "docs": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8181,
        reload=False,
        log_level="info"
    )
