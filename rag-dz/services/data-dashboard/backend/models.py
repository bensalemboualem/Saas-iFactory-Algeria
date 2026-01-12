"""
DZ Data Dashboard - ORM Models
Tables pour le suivi des documents indexés et des logs d'ingestion
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, Field
from enum import Enum


# ==================== ENUMS ====================

class DocumentStatus(str, Enum):
    OK = "ok"
    ERROR = "error"
    PARTIAL = "partial"


class RunStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    ERROR = "error"


class SourceHealth(str, Enum):
    OK = "ok"
    WARNING = "warning"
    ERROR = "error"


class DocumentType(str, Enum):
    LAW = "law"
    TAX = "tax"
    PROCEDURE = "procedure"
    NEWS = "news"
    STATISTIC = "statistic"
    REPORT = "report"
    DECREE = "decree"
    CIRCULAR = "circular"
    INSTRUCTION = "instruction"
    OTHER = "other"


# ==================== DATABASE MODELS (Pydantic for in-memory demo) ====================

class DocumentIndexed(BaseModel):
    """Document indexé dans le RAG-DZ"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    doc_id: str  # Hash ou ID logique du document source
    title: str
    source_name: str  # DZ_JO, DZ_DGI, DZ_ONS, DZ_DOUANE, DZ_NEWS
    type: DocumentType
    country: str = "DZ"
    source_url: Optional[str] = None
    date_document: Optional[datetime] = None  # Date du document original
    date_ingested: datetime = Field(default_factory=datetime.utcnow)
    nb_chunks: int = 0
    status: DocumentStatus = DocumentStatus.OK
    metadata: dict = Field(default_factory=dict)


class IngestionLog(BaseModel):
    """Log d'une exécution d'ingestion"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    source_name: str
    run_id: str  # Identifiant du run n8n / batch
    start_time: datetime
    end_time: Optional[datetime] = None
    status: RunStatus = RunStatus.SUCCESS
    nb_documents: int = 0
    nb_chunks: int = 0
    error_message: Optional[str] = None


# ==================== API RESPONSE MODELS ====================

class SourceSummary(BaseModel):
    """Résumé d'une source"""
    source_name: str
    document_count: int
    chunk_count: int
    last_document_date: Optional[str] = None
    last_ingested_at: Optional[str] = None


class TypeSummary(BaseModel):
    """Résumé par type de document"""
    type: str
    document_count: int


class RunSummary(BaseModel):
    """Résumé d'un run d'ingestion"""
    source_name: str
    run_id: str
    start_time: str
    end_time: Optional[str] = None
    status: str
    nb_documents: int
    nb_chunks: int
    error_message: Optional[str] = None
    duration_seconds: Optional[int] = None


class DataSummaryResponse(BaseModel):
    """Réponse du endpoint /summary"""
    total_documents: int
    total_chunks: int
    sources_count: int
    by_source: list[SourceSummary]
    by_type: list[TypeSummary]
    last_runs: list[RunSummary]


class DocumentDetail(BaseModel):
    """Détail d'un document"""
    id: str
    title: str
    type: str
    source_url: Optional[str] = None
    date_document: Optional[str] = None
    date_ingested: str
    nb_chunks: int
    status: str


class SourceDetailResponse(BaseModel):
    """Réponse du endpoint /source/{source_name}"""
    source_name: str
    total_documents: int
    total_chunks: int
    documents: list[DocumentDetail]
    page: int = 1
    limit: int = 50
    has_more: bool = False


class RunsListResponse(BaseModel):
    """Réponse du endpoint /runs"""
    runs: list[RunSummary]
    total: int


class SourceHealthStatus(BaseModel):
    """Statut de santé d'une source"""
    source_name: str
    status: str  # ok, warning, error
    last_run_at: Optional[str] = None
    last_run_status: Optional[str] = None
    last_document_date: Optional[str] = None
    freshness_days: Optional[int] = None
    document_count: int = 0


class HealthResponse(BaseModel):
    """Réponse du endpoint /health"""
    overall_status: str
    sources: list[SourceHealthStatus]
    last_check: str


class PublicStatsResponse(BaseModel):
    """Stats publiques pour le marketing"""
    total_laws_indexed: int
    total_tax_documents: int
    total_procedures: int
    total_sources: int
    last_update: str
    coverage: dict  # Ex: {"journal_officiel": True, "dgi": True, ...}
