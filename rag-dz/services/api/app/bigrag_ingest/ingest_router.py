"""
INGEST_DZ_CH - Router FastAPI
=============================
Endpoints pour l'ingestion de documents BIG RAG Multi-Pays

Endpoints:
- POST /seed/batch     - Ingestion batch vers une collection
- POST /seed/dz        - Ingestion Algérie (rag_dz)
- POST /seed/ch        - Ingestion Suisse (rag_ch)
- POST /seed/global    - Ingestion internationale (rag_global)
- POST /seed/auto      - Ingestion auto-routée par pays
- POST /seed/file      - Ingestion depuis fichier
- GET  /seed/status    - Statut des collections
- GET  /seed/stats/{collection} - Stats d'une collection
"""

import logging
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .ingest_models import (
    RAGDocument,
    RAGDocumentCreate,
    RAGIngestBatch,
    RAGIngestFile,
    IngestResult,
    IngestStats,
    IngestStatusResponse,
    COUNTRY_TO_COLLECTION,
)
from .ingest_service import get_ingest_service


logger = logging.getLogger(__name__)

# Router avec prefix /api/rag/multi/seed
router = APIRouter(prefix="/api/rag/multi/seed", tags=["🌱 BigRAG Ingest"])


# ============================================
# HEALTH & STATUS
# ============================================

@router.get("/health")
async def health_check():
    """
    Health check du service d'ingestion
    """
    try:
        service = get_ingest_service()
        status = await service.get_status()
        
        return {
            "status": "healthy" if status.ready else "degraded",
            "ready": status.ready,
            "collections": len(status.collections),
            "total_documents": status.total_documents,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }
        )


@router.get("/status", response_model=IngestStatusResponse)
async def get_status():
    """
    📊 Statut détaillé des collections RAG
    
    Retourne:
    - État de chaque collection (rag_dz, rag_ch, rag_global)
    - Nombre de documents par collection
    - Modèle d'embedding utilisé
    """
    try:
        service = get_ingest_service()
        return await service.get_status()
    except Exception as e:
        logger.error(f"Status error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# BATCH INGESTION
# ============================================

@router.post("/batch", response_model=IngestResult)
async def ingest_batch(batch: RAGIngestBatch):
    """
    📦 Ingestion batch vers une collection
    
    Ingère plusieurs documents dans la collection spécifiée.
    
    Collections valides:
    - rag_dz: Documents Algérie
    - rag_ch: Documents Suisse
    - rag_global: Documents internationaux
    
    Args:
        batch: RAGIngestBatch avec collection et liste de documents
        
    Returns:
        IngestResult avec statistiques (inserted, failed, errors)
    """
    try:
        service = get_ingest_service()
        result = await service.ingest_batch(batch)
        
        logger.info(f"Batch ingest: {batch.collection} - {result.inserted}/{result.total} docs")
        return result
        
    except Exception as e:
        logger.error(f"Batch ingest error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# COUNTRY-SPECIFIC INGESTION
# ============================================

@router.post("/dz", response_model=IngestResult)
async def ingest_dz(docs: List[RAGDocument]):
    """
    🇩🇿 Ingestion Algérie (rag_dz)
    
    Ingère des documents dans la collection rag_dz.
    Le champ country sera forcé à "DZ".
    
    Sources typiques: DGI, CNAS, CASNOS, ANDI, CNRC, JORADP
    Langues: ar, fr, ar-dz
    
    Args:
        docs: Liste de RAGDocument
        
    Returns:
        IngestResult
    """
    try:
        service = get_ingest_service()
        result = await service.ingest_dz_docs(docs)
        
        logger.info(f"DZ ingest: {result.inserted}/{result.total} docs")
        return result
        
    except Exception as e:
        logger.error(f"DZ ingest error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ch", response_model=IngestResult)
async def ingest_ch(docs: List[RAGDocument]):
    """
    🇨🇭 Ingestion Suisse (rag_ch)
    
    Ingère des documents dans la collection rag_ch.
    Le champ country sera forcé à "CH".
    
    Sources typiques: AVS, AI, AFC, TVA-CH, SECO, Admin.ch
    Langues: fr, de, it, en
    
    Args:
        docs: Liste de RAGDocument
        
    Returns:
        IngestResult
    """
    try:
        service = get_ingest_service()
        result = await service.ingest_ch_docs(docs)
        
        logger.info(f"CH ingest: {result.inserted}/{result.total} docs")
        return result
        
    except Exception as e:
        logger.error(f"CH ingest error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/global", response_model=IngestResult)
async def ingest_global(docs: List[RAGDocument]):
    """
    🌍 Ingestion internationale (rag_global)
    
    Ingère des documents dans la collection rag_global.
    Le champ country sera forcé à "GLOBAL".
    
    Sources typiques: EU, OECD, UN, WTO
    Langues: en, fr, ar, de, es
    
    Args:
        docs: Liste de RAGDocument
        
    Returns:
        IngestResult
    """
    try:
        service = get_ingest_service()
        result = await service.ingest_global_docs(docs)
        
        logger.info(f"GLOBAL ingest: {result.inserted}/{result.total} docs")
        return result
        
    except Exception as e:
        logger.error(f"GLOBAL ingest error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/auto")
async def ingest_auto(docs: List[RAGDocument]):
    """
    🔄 Ingestion auto-routée par pays
    
    Les documents sont automatiquement routés vers la bonne collection
    selon leur champ country (DZ → rag_dz, CH → rag_ch, autre → rag_global).
    
    Args:
        docs: Liste de RAGDocument avec country renseigné
        
    Returns:
        Dict avec résultats par collection
    """
    try:
        service = get_ingest_service()
        results = await service.ingest_by_country(docs)
        
        summary = {
            "total": len(docs),
            "results": {k: {"inserted": v.inserted, "failed": v.failed} for k, v in results.items()},
        }
        
        logger.info(f"Auto ingest: {summary}")
        return summary
        
    except Exception as e:
        logger.error(f"Auto ingest error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# FILE INGESTION
# ============================================

@router.post("/file", response_model=IngestResult)
async def ingest_from_file(request: RAGIngestFile):
    """
    📄 Ingestion depuis fichier JSON/NDJSON
    
    Charge un fichier et ingère son contenu dans la collection spécifiée.
    
    Formats supportés:
    - JSON: Array de documents ou objet avec clé "docs"
    - NDJSON/JSONL: Une ligne = un document
    
    Args:
        request: RAGIngestFile avec file_path et collection
        
    Returns:
        IngestResult
    """
    try:
        service = get_ingest_service()
        result = await service.ingest_from_file(request.file_path, request.collection)
        
        logger.info(f"File ingest: {request.file_path} → {request.collection} - {result.inserted} docs")
        return result
        
    except Exception as e:
        logger.error(f"File ingest error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_and_ingest(
    file: UploadFile = File(..., description="Fichier JSON ou NDJSON"),
    collection: str = Form("rag_dz", pattern="^rag_(dz|ch|global)$"),
):
    """
    📤 Upload et ingestion de fichier
    
    Upload un fichier JSON/NDJSON et ingère son contenu.
    
    Args:
        file: Fichier à uploader
        collection: Collection cible (rag_dz, rag_ch, rag_global)
        
    Returns:
        IngestResult
    """
    import json
    import tempfile
    from pathlib import Path
    
    try:
        # Lire le contenu
        content = await file.read()
        content_str = content.decode("utf-8")
        
        # Parser selon le format
        docs = []
        if file.filename.endswith(".ndjson") or file.filename.endswith(".jsonl"):
            for line in content_str.strip().split("\n"):
                if line.strip():
                    docs.append(RAGDocument(**json.loads(line)))
        else:
            data = json.loads(content_str)
            if isinstance(data, list):
                docs = [RAGDocument(**d) for d in data]
            elif isinstance(data, dict) and "docs" in data:
                docs = [RAGDocument(**d) for d in data["docs"]]
        
        if not docs:
            return IngestResult(
                collection=collection,
                success=True,
                total=0,
                inserted=0,
            )
        
        # Ingérer
        service = get_ingest_service()
        batch = RAGIngestBatch(collection=collection, docs=docs)
        result = await service.ingest_batch(batch)
        
        logger.info(f"Upload ingest: {file.filename} → {collection} - {result.inserted} docs")
        return result
        
    except Exception as e:
        logger.error(f"Upload ingest error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# SIMPLE INGESTION
# ============================================

@router.post("/simple")
async def simple_ingest(
    title: str = Form(...),
    text: str = Form(...),
    country: str = Form("DZ"),
    language: str = Form("fr"),
    theme: Optional[str] = Form(None),
    source: Optional[str] = Form(None),
    is_official: bool = Form(False),
):
    """
    ✏️ Ingestion simple (formulaire)
    
    Ingère un seul document via formulaire.
    Utile pour tests et ajouts manuels.
    
    Args:
        title: Titre du document
        text: Contenu textuel
        country: Pays (DZ, CH, GLOBAL)
        language: Langue (ar, fr, en, de, it)
        theme: Thème (optionnel)
        source: Source (optionnel)
        is_official: Document officiel
        
    Returns:
        IngestResult
    """
    try:
        doc = RAGDocument(
            title=title,
            text=text,
            country=country.upper(),
            language=language.lower(),
            theme=theme,
            source=source,
            is_official=is_official,
        )
        
        collection = COUNTRY_TO_COLLECTION.get(country.upper(), "rag_global")
        
        service = get_ingest_service()
        batch = RAGIngestBatch(collection=collection, docs=[doc])
        result = await service.ingest_batch(batch)
        
        return result
        
    except Exception as e:
        logger.error(f"Simple ingest error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# INFO
# ============================================

@router.get("/info")
async def ingest_info():
    """
    ℹ️ Informations sur le service d'ingestion
    """
    return {
        "service": "BigRAG Ingest",
        "version": "1.0.0",
        "description": "Ingestion de documents pour BIG RAG Multi-Pays",
        "collections": {
            "rag_dz": {
                "country": "DZ",
                "name": "Algérie",
                "sources": ["DGI", "CNAS", "CASNOS", "ANDI", "CNRC", "JORADP"],
                "languages": ["ar", "fr", "ar-dz"],
            },
            "rag_ch": {
                "country": "CH",
                "name": "Suisse",
                "sources": ["AVS", "AI", "AFC", "TVA-CH", "SECO", "Admin.ch"],
                "languages": ["fr", "de", "it", "en"],
            },
            "rag_global": {
                "country": "GLOBAL",
                "name": "International",
                "sources": ["EU", "OECD", "UN", "WTO"],
                "languages": ["en", "fr", "ar", "de", "es"],
            },
        },
        "endpoints": [
            "POST /seed/batch - Ingestion batch",
            "POST /seed/dz - Ingestion Algérie",
            "POST /seed/ch - Ingestion Suisse",
            "POST /seed/global - Ingestion internationale",
            "POST /seed/auto - Ingestion auto-routée",
            "POST /seed/file - Ingestion depuis fichier",
            "POST /seed/upload - Upload et ingestion",
            "POST /seed/simple - Ingestion simple",
            "GET /seed/status - Statut des collections",
            "GET /seed/stats/{collection} - Stats d'une collection",
            "DELETE /seed/clear/{collection} - Vider une collection",
            "POST /seed/sample/dz - Données de test DZ",
            "POST /seed/sample/ch - Données de test CH",
        ],
        "document_schema": {
            "required": ["title", "text", "country", "language"],
            "optional": ["theme", "source", "url", "date", "tags", "is_official", "summary", "extra"],
        },
    }


# ============================================
# COLLECTION STATS & MANAGEMENT
# ============================================

@router.get("/stats/{collection}")
async def get_collection_stats(collection: str):
    """
    📊 Statistiques d'une collection
    
    Args:
        collection: rag_dz, rag_ch ou rag_global
    """
    if collection not in ["rag_dz", "rag_ch", "rag_global"]:
        raise HTTPException(status_code=400, detail="Invalid collection. Use: rag_dz, rag_ch, rag_global")
    
    try:
        service = get_ingest_service()
        status = service.get_collection_status(collection)
        return {
            "collection": collection,
            "exists": status.exists,
            "vectors_count": status.vectors_count,
            "points_count": status.points_count,
            "status": status.status,
            "vector_size": status.vector_size,
        }
    except Exception as e:
        logger.error(f"Stats error for {collection}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear/{collection}")
async def clear_collection(collection: str, confirm: bool = False):
    """
    🗑️ Vider une collection
    
    ⚠️ ATTENTION: Supprime tous les documents de la collection!
    Requiert le paramètre confirm=true.
    
    Args:
        collection: rag_dz, rag_ch ou rag_global
        confirm: Confirmation requise (true)
    """
    if collection not in ["rag_dz", "rag_ch", "rag_global"]:
        raise HTTPException(status_code=400, detail="Invalid collection")
    
    if not confirm:
        raise HTTPException(
            status_code=400,
            detail="⚠️ Confirmation required. Add ?confirm=true to proceed."
        )
    
    try:
        service = get_ingest_service()
        
        # Supprimer et recréer
        service.qdrant.delete_collection(collection)
        service.ensure_collection(collection)
        
        return {
            "success": True,
            "collection": collection,
            "action": "cleared",
            "message": f"Collection '{collection}' has been cleared and recreated",
        }
    except Exception as e:
        logger.error(f"Clear collection error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ensure-collections")
async def ensure_all_collections():
    """
    🔧 S'assurer que toutes les collections existent
    
    Crée les collections manquantes avec la bonne config vectorielle.
    """
    try:
        service = get_ingest_service()
        
        results = {}
        for name in ["rag_dz", "rag_ch", "rag_global"]:
            success = service.ensure_collection(name)
            status = service.get_collection_status(name)
            results[name] = {
                "created": success,
                "exists": status.exists,
                "vectors_count": status.vectors_count,
            }
        
        return {
            "success": True,
            "collections": results,
        }
    except Exception as e:
        logger.error(f"Ensure collections error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# SAMPLE DATA
# ============================================

@router.post("/sample/dz")
async def ingest_sample_dz():
    """
    🧪 Données de test Algérie
    
    Ingère quelques documents de démonstration dans rag_dz
    """
    sample_docs = [
        RAGDocument(
            title="TVA en Algérie - Taux et obligations",
            text="""La taxe sur la valeur ajoutée (TVA) en Algérie est un impôt indirect 
            prélevé sur la consommation. Elle est appliquée aux taux suivants:
            - Taux normal: 19% (applicable à la plupart des biens et services)
            - Taux réduit: 9% (applicable à certains produits de première nécessité)
            
            Les entreprises dont le chiffre d'affaires annuel dépasse 30 millions DA 
            sont assujetties à la TVA. La déclaration se fait mensuellement via le 
            formulaire G50 pour le régime réel, ou trimestriellement pour le régime 
            simplifié.""",
            country="DZ",
            language="fr",
            theme="Fiscalité",
            source="DGI",
            tags=["TVA", "DGI", "Fiscalité", "Algérie"],
            is_official=True,
        ),
        RAGDocument(
            title="CNAS - Cotisations sociales employeur",
            text="""La Caisse Nationale des Assurances Sociales (CNAS) gère le régime 
            de sécurité sociale des travailleurs salariés en Algérie.
            
            Taux de cotisation:
            - Part employeur: 25% (répartis entre assurance maladie, retraite, accidents du travail)
            - Part salarié: 9%
            - Total: 34% du salaire brut
            
            Les cotisations sont calculées sur le salaire brut plafonné à 8 fois le SNMG.
            La déclaration et le paiement se font mensuellement.""",
            country="DZ",
            language="fr",
            theme="Sécurité Sociale",
            source="CNAS",
            tags=["CNAS", "Cotisations", "Sécurité sociale"],
            is_official=True,
        ),
        RAGDocument(
            title="Création d'entreprise - SARL en Algérie",
            text="""La SARL (Société à Responsabilité Limitée) est la forme juridique 
            la plus courante pour les PME en Algérie.
            
            Étapes de création:
            1. Réservation du nom commercial au CNRC
            2. Établissement des statuts (acte notarié)
            3. Dépôt du capital social (minimum 100.000 DA)
            4. Inscription au registre de commerce
            5. Obtention du NIF (Numéro d'Identification Fiscale)
            6. Affiliation à la CNAS/CASNOS
            
            Délai moyen: 7-15 jours ouvrables.""",
            country="DZ",
            language="fr",
            theme="Création d'entreprise",
            source="CNRC",
            tags=["SARL", "Création entreprise", "CNRC"],
            is_official=True,
        ),
        RAGDocument(
            title="ضريبة القيمة المضافة في الجزائر",
            text="""ضريبة القيمة المضافة هي ضريبة غير مباشرة تفرض على الاستهلاك.
            
            معدلات الضريبة:
            - المعدل العادي: 19%
            - المعدل المخفض: 9% (للسلع الأساسية)
            
            الشركات التي يتجاوز رقم أعمالها السنوي 30 مليون دج تخضع لضريبة القيمة المضافة.
            يتم التصريح شهريا عبر النموذج G50.""",
            country="DZ",
            language="ar",
            theme="Fiscalité",
            source="DGI",
            tags=["TVA", "DGI", "ضرائب", "الجزائر"],
            is_official=True,
        ),
    ]
    
    try:
        service = get_ingest_service()
        result = await service.ingest_dz_docs(sample_docs)
        
        return {
            "success": result.success,
            "message": f"Inserted {result.inserted} sample documents in rag_dz",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Sample DZ error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sample/ch")
async def ingest_sample_ch():
    """
    🧪 Données de test Suisse
    
    Ingère quelques documents de démonstration dans rag_ch
    """
    sample_docs = [
        RAGDocument(
            title="AVS - Assurance vieillesse et survivants",
            text="""L'AVS est le premier pilier du système de prévoyance suisse.
            
            Cotisations:
            - Salariés: 4.35% (part employé) + 4.35% (part employeur) = 8.7%
            - Indépendants: 7.8% à 8.1% selon le revenu
            
            L'AVS assure une rente de base à la retraite (65 ans hommes, 64 ans femmes)
            et des rentes de survivants en cas de décès.
            
            Montant de la rente complète: CHF 1'225 à 2'450 par mois (2024).""",
            country="CH",
            language="fr",
            theme="Sécurité Sociale",
            source="AVS",
            tags=["AVS", "Retraite", "Prévoyance", "Suisse"],
            is_official=True,
        ),
        RAGDocument(
            title="TVA Suisse - Taux et assujettissement",
            text="""La taxe sur la valeur ajoutée en Suisse est gérée par l'AFC.
            
            Taux de TVA (2024):
            - Taux normal: 8.1%
            - Taux réduit: 2.6% (biens de première nécessité, médicaments)
            - Taux spécial: 3.8% (hébergement)
            
            Assujettissement: Chiffre d'affaires annuel > CHF 100'000
            
            Déclaration: Trimestrielle ou semestrielle selon option.""",
            country="CH",
            language="fr",
            theme="Fiscalité",
            source="TVA-CH",
            tags=["TVA", "AFC", "Fiscalité", "Suisse"],
            is_official=True,
        ),
        RAGDocument(
            title="Création d'entreprise - Sàrl en Suisse",
            text="""La Sàrl (Société à responsabilité limitée) est une forme juridique 
            populaire pour les PME en Suisse.
            
            Caractéristiques:
            - Capital minimum: CHF 20'000 (libéré intégralement)
            - Minimum 1 associé
            - Responsabilité limitée au capital
            
            Étapes:
            1. Rédaction des statuts (acte authentique)
            2. Versement du capital
            3. Inscription au registre du commerce
            4. Affiliation aux assurances sociales (AVS, LAA, LPP)
            
            Délai: 2-4 semaines.""",
            country="CH",
            language="fr",
            theme="Création d'entreprise",
            source="Admin.ch",
            tags=["Sàrl", "Création entreprise", "RC", "Suisse"],
            is_official=True,
        ),
    ]
    
    try:
        service = get_ingest_service()
        result = await service.ingest_ch_docs(sample_docs)
        
        return {
            "success": result.success,
            "message": f"Inserted {result.inserted} sample documents in rag_ch",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Sample CH error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# SEARCH ENDPOINT (using same embedder)
# ============================================

class SearchRequest(BaseModel):
    """Requête de recherche"""
    query: str = Field(..., min_length=1, max_length=500)
    collection: str = Field("rag_dz", pattern="^rag_(dz|ch|global)$")
    top_k: int = Field(5, ge=1, le=20)
    country_filter: Optional[str] = None
    theme_filter: Optional[str] = None


class SearchHit(BaseModel):
    """Résultat de recherche"""
    id: str
    title: str
    text: str
    score: float
    country: str
    language: str
    theme: Optional[str] = None
    source: Optional[str] = None
    tags: List[str] = []


class SearchResponse(BaseModel):
    """Réponse de recherche"""
    results: List[SearchHit]
    total: int
    collection: str
    query: str
    search_time_ms: float


@router.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """
    🔍 Recherche dans une collection
    
    Utilise le même embedder que l'ingestion (sentence-transformers multilingue)
    pour rechercher des documents par similarité sémantique.
    
    Args:
        query: Texte de recherche
        collection: Collection cible (rag_dz, rag_ch, rag_global)
        top_k: Nombre de résultats
    """
    import time
    start = time.time()
    
    try:
        service = get_ingest_service()
        
        # Vérifier que la collection existe
        status = service.get_collection_status(request.collection)
        if not status.exists:
            raise HTTPException(status_code=404, detail=f"Collection '{request.collection}' not found")
        
        # Générer l'embedding de la requête
        query_vector = service.embedder.embed_text(request.query)
        
        # Rechercher dans Qdrant
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        
        # Construire les filtres
        conditions = []
        if request.country_filter:
            conditions.append(FieldCondition(key="country", match=MatchValue(value=request.country_filter)))
        if request.theme_filter:
            conditions.append(FieldCondition(key="theme", match=MatchValue(value=request.theme_filter)))
        
        search_filter = Filter(must=conditions) if conditions else None
        
        results = service.qdrant.search(
            collection_name=request.collection,
            query_vector=query_vector,
            limit=request.top_k,
            query_filter=search_filter,
        )
        
        # Convertir les résultats
        hits = []
        for result in results:
            payload = result.payload or {}
            hits.append(SearchHit(
                id=str(result.id),
                title=payload.get("title", ""),
                text=payload.get("text", "")[:500],  # Tronquer le texte
                score=result.score,
                country=payload.get("country", ""),
                language=payload.get("language", ""),
                theme=payload.get("theme"),
                source=payload.get("source"),
                tags=payload.get("tags", []),
            ))
        
        search_time = (time.time() - start) * 1000
        
        return SearchResponse(
            results=hits,
            total=len(hits),
            collection=request.collection,
            query=request.query,
            search_time_ms=round(search_time, 2),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
