"""
BIGRAG_INGEST - Module d'ingestion BIG RAG Multi-Pays
=====================================================
Ingestion de documents vers Qdrant (rag_dz, rag_ch, rag_global)

Ce module permet de:
1. Standardiser les documents à ingérer (RAGDocument)
2. Générer les embeddings multilingues
3. Stocker dans les collections Qdrant par pays
4. Fournir des endpoints REST pour l'ingestion

Collections:
- rag_dz: Documents Algérie (DGI, CNAS, CASNOS, etc.)
- rag_ch: Documents Suisse (AVS, TVA-CH, AFC, etc.)
- rag_global: Documents internationaux (EU, OECD, UN, etc.)

Endpoints:
- POST /api/rag/multi/seed/batch  - Ingestion batch
- POST /api/rag/multi/seed/dz     - Ingestion Algérie
- POST /api/rag/multi/seed/ch     - Ingestion Suisse
- POST /api/rag/multi/seed/global - Ingestion internationale
- POST /api/rag/multi/seed/auto   - Auto-routage par pays
- GET  /api/rag/multi/seed/status - Statut des collections
"""

from .ingest_models import (
    # Enums
    Country,
    Language,
    DocumentTheme,
    DocumentSource,
    IngestStatus,
    
    # Document models
    RAGDocument,
    RAGDocumentCreate,
    
    # Batch models
    RAGIngestBatch,
    RAGIngestFile,
    
    # Result models
    IngestResult,
    IngestStats,
    CollectionStatus,
    IngestStatusResponse,
    
    # Constants
    COUNTRY_TO_COLLECTION,
    DEFAULT_COLLECTIONS,
    THEMES_DZ,
    THEMES_CH,
    SOURCES_DZ,
    SOURCES_CH,
)

from .ingest_service import (
    IngestService,
    EmbeddingPipeline,
    get_ingest_service,
    init_ingest_service,
)

from .ingest_router import router as ingest_router


__all__ = [
    # Router
    "ingest_router",
    
    # Service
    "IngestService",
    "EmbeddingPipeline",
    "get_ingest_service",
    "init_ingest_service",
    
    # Enums
    "Country",
    "Language",
    "DocumentTheme",
    "DocumentSource",
    "IngestStatus",
    
    # Document models
    "RAGDocument",
    "RAGDocumentCreate",
    
    # Batch models
    "RAGIngestBatch",
    "RAGIngestFile",
    
    # Result models
    "IngestResult",
    "IngestStats",
    "CollectionStatus",
    "IngestStatusResponse",
    
    # Constants
    "COUNTRY_TO_COLLECTION",
    "DEFAULT_COLLECTIONS",
    "THEMES_DZ",
    "THEMES_CH",
    "SOURCES_DZ",
    "SOURCES_CH",
]


# Version
__version__ = "1.0.0"
__author__ = "iaFactoryDZ"
__description__ = "Ingestion documents BIG RAG Multi-Pays (DZ, CH, GLOBAL)"
