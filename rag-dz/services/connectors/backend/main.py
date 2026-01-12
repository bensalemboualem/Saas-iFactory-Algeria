"""
DZ-Connectors Backend API
========================
Module d'ingestion automatique de données algériennes pour IAFactory RAG

Endpoints:
- POST /api/ingest - Ingérer un document
- POST /api/ingest/batch - Ingérer plusieurs documents
- GET /api/sources - Liste des sources disponibles
- GET /api/stats - Statistiques d'ingestion
- POST /api/scrape/{source} - Lancer un scraping manuel
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime, date
import hashlib
import asyncio
import logging
from contextlib import asynccontextmanager

# Local imports
from scrapers import JORADPScraper, DGIScraper, ONSScraper, BankAlgeriaScraper
from scrapers import DouanesScraper, ANEMScraper, ANDIScraper, NewsScraper
from embeddings import EmbeddingService
from database import Database, IngestionLog
from chunker import TextChunker

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dz-connectors")

# Configuration
SOURCES = {
    "DZ_JO": {"name": "Journal Officiel", "url": "https://www.joradp.dz", "frequency": "weekly"},
    "DZ_DGI": {"name": "Direction Générale des Impôts", "url": "https://www.mfdgi.gov.dz", "frequency": "weekly"},
    "DZ_ONS": {"name": "Office National des Statistiques", "url": "https://www.ons.dz", "frequency": "monthly"},
    "DZ_BANK": {"name": "Banque d'Algérie", "url": "https://www.bank-of-algeria.dz", "frequency": "weekly"},
    "DZ_DOUANE": {"name": "Douanes Algériennes", "url": "https://www.douane.gov.dz", "frequency": "weekly"},
    "DZ_ANEM": {"name": "ANEM Emploi", "url": "https://www.anem.dz", "frequency": "weekly"},
    "DZ_ANDI": {"name": "ANDI Investissement", "url": "https://andi.dz", "frequency": "monthly"},
    "DZ_NEWS": {"name": "Actualités DZ", "url": "multiple", "frequency": "daily"},
}

# Services
db: Optional[Database] = None
embedding_service: Optional[EmbeddingService] = None
chunker: Optional[TextChunker] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management"""
    global db, embedding_service, chunker
    
    logger.info("🚀 Initialisation DZ-Connectors...")
    
    # Initialize services
    db = Database()
    await db.connect()
    
    embedding_service = EmbeddingService()
    chunker = TextChunker(chunk_size=500, overlap=50)
    
    logger.info("✅ DZ-Connectors prêt!")
    
    yield
    
    # Cleanup
    await db.disconnect()
    logger.info("👋 DZ-Connectors arrêté")


app = FastAPI(
    title="DZ-Connectors API",
    description="Module d'ingestion automatique de données algériennes",
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


# ============== MODELS ==============

class DocumentInput(BaseModel):
    """Document à ingérer"""
    title: str = Field(..., description="Titre du document")
    text: str = Field(..., description="Contenu textuel")
    source_url: str = Field(..., description="URL source")
    source_name: Literal[
        "DZ_JO", "DZ_DGI", "DZ_ONS", "DZ_BANK", 
        "DZ_DOUANE", "DZ_ANEM", "DZ_ANDI", "DZ_NEWS"
    ] = Field(..., description="Identifiant de la source")
    type: Literal[
        "law", "decree", "tax", "procedure", 
        "news", "statistic", "circular", "report"
    ] = Field(..., description="Type de document")
    date: Optional[str] = Field(None, description="Date du document (YYYY-MM-DD)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Loi de Finances 2024",
                "text": "Article 1: Les dispositions de la présente loi...",
                "source_url": "https://www.joradp.dz/FTP/JO-FRANCAIS/2023/F2023086.pdf",
                "source_name": "DZ_JO",
                "type": "law",
                "date": "2023-12-28"
            }
        }


class BatchInput(BaseModel):
    """Lot de documents à ingérer"""
    documents: List[DocumentInput]


class IngestionResult(BaseModel):
    """Résultat d'ingestion"""
    success: bool
    document_id: Optional[str] = None
    chunks_count: int = 0
    message: str


class SourceInfo(BaseModel):
    """Information sur une source"""
    id: str
    name: str
    url: str
    frequency: str
    last_scrape: Optional[datetime] = None
    documents_count: int = 0
    status: str = "active"


class StatsResponse(BaseModel):
    """Statistiques globales"""
    total_documents: int
    total_chunks: int
    sources: dict
    last_ingestion: Optional[datetime]
    by_type: dict
    by_source: dict


# ============== HELPERS ==============

def generate_doc_id(doc: DocumentInput) -> str:
    """Génère un ID unique pour un document"""
    content = f"{doc.source_name}:{doc.source_url}:{doc.title}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def clean_text(text: str) -> str:
    """Nettoie le texte avant ingestion"""
    import re
    
    # Supprimer les numéros de page
    text = re.sub(r'\n\s*-?\s*\d+\s*-?\s*\n', '\n', text)
    text = re.sub(r'Page \d+ sur \d+', '', text)
    
    # Supprimer les headers répétitifs
    text = re.sub(r'JOURNAL OFFICIEL DE LA REPUBLIQUE ALGERIENNE.*?\n', '', text)
    text = re.sub(r'République Algérienne Démocratique et Populaire.*?\n', '', text)
    
    # Normaliser les espaces
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Supprimer caractères spéciaux problématiques
    text = text.replace('\x00', '')
    
    return text.strip()


# ============== ENDPOINTS ==============

@app.get("/")
async def root():
    """Health check"""
    return {
        "service": "DZ-Connectors",
        "version": "1.0.0",
        "status": "running",
        "country": "DZ",
        "description": "Module d'ingestion de données algériennes"
    }


@app.get("/health")
async def health():
    """Health check détaillé"""
    return {
        "status": "healthy",
        "database": await db.ping() if db else False,
        "embedding_service": embedding_service is not None,
        "sources_count": len(SOURCES)
    }


@app.post("/api/ingest", response_model=IngestionResult)
async def ingest_document(doc: DocumentInput, background_tasks: BackgroundTasks):
    """
    Ingérer un document dans le RAG
    
    Étapes:
    1. Nettoyage du texte
    2. Chunking (découpage en morceaux)
    3. Génération des embeddings
    4. Stockage dans la base vectorielle
    """
    try:
        # Générer ID unique
        doc_id = generate_doc_id(doc)
        
        # Vérifier si déjà ingéré
        if await db.document_exists(doc_id):
            return IngestionResult(
                success=True,
                document_id=doc_id,
                chunks_count=0,
                message="Document déjà ingéré"
            )
        
        # Nettoyage
        cleaned_text = clean_text(doc.text)
        
        if len(cleaned_text) < 50:
            return IngestionResult(
                success=False,
                message="Texte trop court après nettoyage"
            )
        
        # Chunking
        chunks = chunker.chunk(cleaned_text)
        
        # Métadonnées communes
        metadata = {
            "country": "DZ",
            "source_name": doc.source_name,
            "source_url": doc.source_url,
            "type": doc.type,
            "title": doc.title,
            "date": doc.date or datetime.now().strftime("%Y-%m-%d"),
            "ingested_at": datetime.now().isoformat()
        }
        
        # Générer embeddings et stocker
        for i, chunk in enumerate(chunks):
            chunk_metadata = {**metadata, "chunk_index": i, "total_chunks": len(chunks)}
            embedding = await embedding_service.embed(chunk)
            await db.store_embedding(
                doc_id=f"{doc_id}_{i}",
                text=chunk,
                embedding=embedding,
                metadata=chunk_metadata
            )
        
        # Logger l'ingestion
        await db.log_ingestion(IngestionLog(
            source_name=doc.source_name,
            document_id=doc_id,
            title=doc.title,
            chunks_count=len(chunks),
            status="success"
        ))
        
        logger.info(f"✅ Document ingéré: {doc.title} ({len(chunks)} chunks)")
        
        return IngestionResult(
            success=True,
            document_id=doc_id,
            chunks_count=len(chunks),
            message=f"Document ingéré avec succès ({len(chunks)} chunks)"
        )
        
    except Exception as e:
        logger.error(f"❌ Erreur ingestion: {e}")
        
        # Logger l'échec
        await db.log_ingestion(IngestionLog(
            source_name=doc.source_name,
            document_id=doc_id if 'doc_id' in locals() else "unknown",
            title=doc.title,
            chunks_count=0,
            status="error",
            error_message=str(e)
        ))
        
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ingest/batch", response_model=List[IngestionResult])
async def ingest_batch(batch: BatchInput, background_tasks: BackgroundTasks):
    """Ingérer plusieurs documents en lot"""
    results = []
    
    for doc in batch.documents:
        try:
            result = await ingest_document(doc, background_tasks)
            results.append(result)
        except Exception as e:
            results.append(IngestionResult(
                success=False,
                message=f"Erreur: {str(e)}"
            ))
    
    return results


@app.get("/api/sources", response_model=List[SourceInfo])
async def list_sources():
    """Liste toutes les sources DZ disponibles"""
    sources = []
    
    for source_id, info in SOURCES.items():
        stats = await db.get_source_stats(source_id)
        sources.append(SourceInfo(
            id=source_id,
            name=info["name"],
            url=info["url"],
            frequency=info["frequency"],
            last_scrape=stats.get("last_scrape"),
            documents_count=stats.get("count", 0),
            status="active"
        ))
    
    return sources


@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """Statistiques globales d'ingestion"""
    stats = await db.get_global_stats()
    
    return StatsResponse(
        total_documents=stats.get("total_documents", 0),
        total_chunks=stats.get("total_chunks", 0),
        sources=SOURCES,
        last_ingestion=stats.get("last_ingestion"),
        by_type=stats.get("by_type", {}),
        by_source=stats.get("by_source", {})
    )


@app.post("/api/scrape/{source}")
async def trigger_scrape(source: str, background_tasks: BackgroundTasks):
    """Lancer un scraping manuel pour une source"""
    
    if source not in SOURCES and source != "all":
        raise HTTPException(status_code=404, detail=f"Source inconnue: {source}")
    
    # Lancer en arrière-plan
    background_tasks.add_task(run_scraper, source)
    
    return {
        "status": "started",
        "source": source,
        "message": f"Scraping de {source} lancé en arrière-plan"
    }


async def run_scraper(source: str):
    """Exécute le scraper pour une source"""
    scrapers = {
        "DZ_JO": JORADPScraper(),
        "DZ_DGI": DGIScraper(),
        "DZ_ONS": ONSScraper(),
        "DZ_BANK": BankAlgeriaScraper(),
        "DZ_DOUANE": DouanesScraper(),
        "DZ_ANEM": ANEMScraper(),
        "DZ_ANDI": ANDIScraper(),
        "DZ_NEWS": NewsScraper(),
    }
    
    if source == "all":
        for src_id, scraper in scrapers.items():
            try:
                documents = await scraper.scrape()
                for doc in documents:
                    await ingest_document(doc, BackgroundTasks())
            except Exception as e:
                logger.error(f"Erreur scraping {src_id}: {e}")
    else:
        scraper = scrapers.get(source)
        if scraper:
            documents = await scraper.scrape()
            for doc in documents:
                await ingest_document(doc, BackgroundTasks())


@app.get("/api/search")
async def search_dz(
    query: str,
    source: Optional[str] = None,
    doc_type: Optional[str] = None,
    limit: int = 10
):
    """
    Recherche dans les documents DZ ingérés
    """
    # Générer embedding de la requête
    query_embedding = await embedding_service.embed(query)
    
    # Filtres
    filters = {"country": "DZ"}
    if source:
        filters["source_name"] = source
    if doc_type:
        filters["type"] = doc_type
    
    # Recherche vectorielle
    results = await db.search(
        embedding=query_embedding,
        filters=filters,
        limit=limit
    )
    
    return {
        "query": query,
        "results": results,
        "count": len(results)
    }


@app.get("/api/documents")
async def list_documents(
    source: Optional[str] = None,
    doc_type: Optional[str] = None,
    page: int = 1,
    per_page: int = 20
):
    """Liste les documents ingérés avec pagination"""
    
    filters = {"country": "DZ"}
    if source:
        filters["source_name"] = source
    if doc_type:
        filters["type"] = doc_type
    
    documents = await db.list_documents(
        filters=filters,
        page=page,
        per_page=per_page
    )
    
    return {
        "documents": documents,
        "page": page,
        "per_page": per_page,
        "total": await db.count_documents(filters)
    }


# ============== MAIN ==============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8195)
