"""
INGEST_DZ_CH - Modèles Pydantic
===============================
Ingestion de documents pour BIG RAG Multi-Pays (DZ, CH, GLOBAL)

Ce module définit les modèles standards pour ingérer des documents
dans les collections Qdrant correspondantes.

Pays/Collections:
- DZ: rag_dz (Algérie - arabe, français)
- CH: rag_ch (Suisse - français, allemand, italien)  
- GLOBAL: rag_global (International - multilingue)

Sources officielles:
- DZ: DGI, CNAS, CASNOS, ANDI, CNRC, Journal Officiel
- CH: AVS, TVA-CH, AFC, Admin.ch
- GLOBAL: EU, OECD, UN, etc.
"""

from datetime import date as DateType, datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import uuid


# ============================================
# ENUMS
# ============================================

class Country(str, Enum):
    """Pays supportés"""
    DZ = "DZ"           # Algérie
    CH = "CH"           # Suisse
    GLOBAL = "GLOBAL"   # International


class Language(str, Enum):
    """Langues supportées"""
    ARABIC = "ar"
    FRENCH = "fr"
    ENGLISH = "en"
    GERMAN = "de"
    ITALIAN = "it"
    SPANISH = "es"
    DARIJA = "ar-dz"    # Dialecte algérien


class DocumentTheme(str, Enum):
    """Thèmes documentaires"""
    # Fiscalité
    FISCALITE = "Fiscalité"
    TVA = "TVA"
    IMPOTS = "Impôts"
    
    # Social
    SECURITE_SOCIALE = "Sécurité Sociale"
    RETRAITE = "Retraite"
    ASSURANCE_MALADIE = "Assurance Maladie"
    CHOMAGE = "Chômage"
    
    # Entreprise
    CREATION_ENTREPRISE = "Création d'entreprise"
    REGISTRE_COMMERCE = "Registre de commerce"
    STATUTS_JURIDIQUES = "Statuts juridiques"
    
    # Administration
    PROCEDURES_ADMIN = "Procédures administratives"
    DOCUMENTS_OFFICIELS = "Documents officiels"
    
    # Secteurs
    COMMERCE = "Commerce"
    INDUSTRIE = "Industrie"
    SERVICES = "Services"
    AGRICULTURE = "Agriculture"
    TECH = "Technologie"
    
    # Général
    GENERAL = "Général"
    AUTRE = "Autre"


class DocumentSource(str, Enum):
    """Sources officielles"""
    # Algérie
    DGI = "DGI"             # Direction Générale des Impôts
    CNAS = "CNAS"           # Caisse Nationale d'Assurances Sociales
    CASNOS = "CASNOS"       # Caisse des Non-Salariés
    ANDI = "ANDI"           # Agence Nationale de Développement de l'Investissement
    CNRC = "CNRC"           # Centre National du Registre de Commerce
    JORADP = "JORADP"       # Journal Officiel
    ANEM = "ANEM"           # Agence Nationale de l'Emploi
    ANSEJ = "ANSEJ"         # Agence Nationale de Soutien à l'Emploi des Jeunes
    CACI = "CACI"           # Chambre Algérienne de Commerce et d'Industrie
    
    # Suisse
    AVS = "AVS"             # Assurance-vieillesse et survivants
    AI = "AI"               # Assurance-invalidité
    AFC = "AFC"             # Administration Fédérale des Contributions
    TVA_CH = "TVA-CH"       # TVA Suisse
    SECO = "SECO"           # Secrétariat d'État à l'économie
    ADMIN_CH = "Admin.ch"   # Portail admin.ch
    
    # International
    EU = "EU"               # Union Européenne
    OECD = "OECD"           # OCDE
    UN = "UN"               # Nations Unies
    WTO = "WTO"             # OMC
    
    # Autres
    OFFICIAL = "Official"
    COMMUNITY = "Community"
    OTHER = "Other"


class IngestStatus(str, Enum):
    """Statut d'ingestion"""
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"


# ============================================
# DOCUMENT MODELS
# ============================================

class RAGDocument(BaseModel):
    """
    Document standard pour ingestion RAG
    
    Ce modèle représente un document à ingérer dans Qdrant.
    Il contient le texte, les métadonnées et les informations de classification.
    """
    # Identifiant
    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="ID unique du document (auto-généré si absent)"
    )
    
    # Contenu principal
    title: str = Field(..., min_length=1, max_length=500, description="Titre du document")
    text: str = Field(..., min_length=10, description="Contenu textuel principal")
    summary: Optional[str] = Field(None, max_length=1000, description="Résumé du document")
    
    # Classification géographique
    country: str = Field(..., description="Pays: DZ, CH, GLOBAL")
    language: str = Field("fr", description="Langue: ar, fr, en, de, it")
    
    # Classification thématique
    theme: Optional[str] = Field(None, description="Thème: Fiscalité, Sécurité Sociale, etc.")
    source: Optional[str] = Field(None, description="Source: DGI, CNAS, AVS, etc.")
    
    # Référence
    url: Optional[str] = Field(None, description="URL source")
    date: Optional[DateType] = Field(None, description="Date du document")
    
    # Tags et métadonnées
    tags: List[str] = Field(default_factory=list, description="Tags pour recherche")
    is_official: bool = Field(False, description="Document officiel (loi, décret, etc.)")
    
    # Métadonnées libres
    extra: Dict[str, Any] = Field(default_factory=dict, description="Métadonnées additionnelles")
    
    # Chunking (optionnel)
    chunk_index: Optional[int] = Field(None, description="Index du chunk (si document découpé)")
    total_chunks: Optional[int] = Field(None, description="Nombre total de chunks")
    parent_id: Optional[str] = Field(None, description="ID du document parent (si chunk)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "TVA en Algérie - Taux et obligations",
                "text": "La taxe sur la valeur ajoutée (TVA) en Algérie est appliquée aux taux de 19% (taux normal) et 9% (taux réduit). Les entreprises assujetties doivent déclarer et payer la TVA mensuellement ou trimestriellement selon leur chiffre d'affaires...",
                "country": "DZ",
                "language": "fr",
                "theme": "Fiscalité",
                "source": "DGI",
                "url": "https://www.mfdgi.gov.dz/",
                "date": "2024-01-01",
                "tags": ["TVA", "DGI", "Algérie", "Fiscalité"],
                "is_official": True,
            }
        }


class RAGDocumentCreate(BaseModel):
    """Document simplifié pour création rapide"""
    title: str = Field(..., min_length=1)
    text: str = Field(..., min_length=10)
    country: str = Field("DZ")
    language: str = Field("fr")
    theme: Optional[str] = None
    source: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    is_official: bool = Field(False)


# ============================================
# BATCH MODELS
# ============================================

class RAGIngestBatch(BaseModel):
    """
    Batch d'ingestion pour une collection
    
    Permet d'ingérer plusieurs documents à la fois dans une collection spécifique.
    """
    collection: str = Field(
        ..., 
        pattern="^rag_(dz|ch|global)$",
        description="Collection cible: rag_dz, rag_ch, rag_global"
    )
    docs: List[RAGDocument] = Field(..., min_length=1, description="Documents à ingérer")
    
    # Options
    skip_duplicates: bool = Field(True, description="Ignorer les doublons (même ID)")
    update_existing: bool = Field(False, description="Mettre à jour si ID existe")
    
    class Config:
        json_schema_extra = {
            "example": {
                "collection": "rag_dz",
                "docs": [
                    {
                        "title": "Registre de commerce en Algérie",
                        "text": "Le registre de commerce est un fichier public...",
                        "country": "DZ",
                        "language": "fr",
                        "theme": "Création d'entreprise",
                        "source": "CNRC",
                    }
                ]
            }
        }


class RAGIngestFile(BaseModel):
    """Ingestion depuis fichier"""
    file_path: str = Field(..., description="Chemin du fichier JSON/NDJSON")
    collection: str = Field(..., description="Collection cible")
    format: str = Field("json", pattern="^(json|ndjson)$", description="Format: json ou ndjson")


# ============================================
# RESULT MODELS
# ============================================

class IngestResult(BaseModel):
    """
    Résultat d'une opération d'ingestion
    """
    # Statut
    success: bool = Field(True)
    status: IngestStatus = Field(IngestStatus.SUCCESS)
    
    # Collection
    collection: str = Field(..., description="Collection cible")
    
    # Compteurs
    total: int = Field(0, description="Nombre total de documents traités")
    inserted: int = Field(0, description="Documents insérés avec succès")
    updated: int = Field(0, description="Documents mis à jour")
    skipped: int = Field(0, description="Documents ignorés (doublons)")
    failed: int = Field(0, description="Documents en échec")
    
    # Erreurs
    errors: List[str] = Field(default_factory=list, description="Messages d'erreur")
    failed_ids: List[str] = Field(default_factory=list, description="IDs des documents en échec")
    
    # Timing
    processing_time_ms: int = Field(0, description="Temps de traitement en ms")
    
    # Métadonnées
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class IngestStats(BaseModel):
    """Statistiques d'ingestion par collection"""
    collection: str
    total_documents: int = 0
    total_vectors: int = 0
    
    # Par pays
    by_country: Dict[str, int] = Field(default_factory=dict)
    
    # Par langue
    by_language: Dict[str, int] = Field(default_factory=dict)
    
    # Par thème
    by_theme: Dict[str, int] = Field(default_factory=dict)
    
    # Par source
    by_source: Dict[str, int] = Field(default_factory=dict)
    
    # Documents officiels
    official_count: int = 0
    
    # Dates
    oldest_doc: Optional[DateType] = None
    newest_doc: Optional[DateType] = None
    last_ingest: Optional[datetime] = None


class CollectionStatus(BaseModel):
    """Statut d'une collection Qdrant"""
    name: str
    exists: bool = False
    vectors_count: int = 0
    points_count: int = 0
    segments_count: int = 0
    status: str = "unknown"
    
    # Dimensions embedding
    vector_size: int = 0
    
    # Config
    distance: str = "Cosine"
    
    # Dernière mise à jour
    last_updated: Optional[datetime] = None


class IngestStatusResponse(BaseModel):
    """Statut global des collections"""
    ready: bool = True
    collections: List[CollectionStatus] = Field(default_factory=list)
    total_documents: int = 0
    
    # Par pays
    dz_count: int = 0
    ch_count: int = 0
    global_count: int = 0
    
    # Service
    embedding_model: Optional[str] = None
    qdrant_host: Optional[str] = None


# ============================================
# CONSTANTS
# ============================================

# Collections par défaut
DEFAULT_COLLECTIONS = {
    "DZ": "rag_dz",
    "CH": "rag_ch",
    "GLOBAL": "rag_global",
}

# Mapping pays -> collection
COUNTRY_TO_COLLECTION = {
    "DZ": "rag_dz",
    "CH": "rag_ch",
    "GLOBAL": "rag_global",
}

# Thèmes par pays
THEMES_DZ = [
    "Fiscalité", "TVA", "Impôts",
    "Sécurité Sociale", "CNAS", "CASNOS", "Retraite",
    "Création d'entreprise", "Registre de commerce",
    "Procédures administratives",
]

THEMES_CH = [
    "Fiscalité", "TVA", "Impôts",
    "AVS", "AI", "Assurance Maladie",
    "Création d'entreprise", "RC",
    "Procédures administratives",
]

# Sources par pays
SOURCES_DZ = ["DGI", "CNAS", "CASNOS", "ANDI", "CNRC", "JORADP", "ANEM", "ANSEJ"]
SOURCES_CH = ["AVS", "AI", "AFC", "TVA-CH", "SECO", "Admin.ch"]
