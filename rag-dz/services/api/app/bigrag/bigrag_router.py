"""
BIG RAG - Router FastAPI
=========================
Endpoints pour RAG multi-pays international
DZ 🇩🇿 + CH 🇨🇭 + GLOBAL 🌍
"""

from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Header, BackgroundTasks
from pydantic import BaseModel, Field

from .country_detector import (
    CountryDetectionResult, Country, Language,
    get_country_emoji, get_country_name,
)
from .bigrag_service import (
    BigRAGService, bigrag_service,
    BigRAGRequest, BigRAGResponse,
    LLMModel,
)
from .qdrant_multi import IndexName, MultiSearchResult

router = APIRouter(prefix="/api/rag/multi", tags=["BIG RAG Multi-Pays"])


# ============================================
# REQUEST/RESPONSE MODELS
# ============================================

class QuickQueryRequest(BaseModel):
    """Requête simplifiée"""
    query: str = Field(..., min_length=3, description="Question")
    country: Optional[str] = Field(None, description="Pays (DZ, CH)")


class DetectCountryRequest(BaseModel):
    """Requête détection pays"""
    text: str = Field(..., min_length=3, description="Texte à analyser")


class SearchOnlyRequest(BaseModel):
    """Requête recherche seule"""
    query: str = Field(..., min_length=3)
    top_k: int = Field(10, ge=1, le=50)
    country: Optional[str] = Field(None, description="Forcer un pays")


class IngestRequest(BaseModel):
    """Requête d'ingestion de document"""
    text: str = Field(..., description="Contenu du document")
    country: str = Field(..., description="Pays (DZ, CH, GLOBAL)")
    source: str = Field(..., description="Source du document")
    theme: Optional[str] = Field(None, description="Thème/catégorie")
    title: Optional[str] = Field(None, description="Titre")
    url: Optional[str] = Field(None, description="URL source")
    metadata: Optional[dict] = Field(default_factory=dict)


class IngestBatchRequest(BaseModel):
    """Requête d'ingestion batch"""
    documents: List[IngestRequest]


# ============================================
# MAIN QUERY ENDPOINTS
# ============================================

@router.post("/query", response_model=BigRAGResponse)
async def multi_query(request: BigRAGRequest):
    """
    🌍 Query RAG Multi-Pays
    
    Pipeline complet:
    1. Détection automatique du pays (DZ 🇩🇿, CH 🇨🇭, GLOBAL 🌍)
    2. Recherche dans l'index approprié
    3. Reranking des résultats
    4. Génération de réponse par LLM
    
    **Exemples de requêtes:**
    - "Comment calculer l'IRG en Algérie ?" → DZ 🇩🇿
    - "Quelles sont les cotisations AVS en Suisse ?" → CH 🇨🇭
    - "Comment créer une entreprise ?" → GLOBAL (ou pays détecté)
    
    **Signaux de détection DZ:**
    - CNAS, CASNOS, DGI, IRG, IBS, TAP
    - Wilaya, Dinar, DZD
    - Texte en arabe
    
    **Signaux de détection CH:**
    - AVS, LPP, SUVA, AFC
    - Canton, CHF, Franc suisse
    - Texte en allemand
    """
    try:
        response = await bigrag_service.query(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/quick")
async def quick_query(request: QuickQueryRequest):
    """
    ⚡ Query rapide (paramètres par défaut)
    
    Version simplifiée pour intégration rapide.
    Utilise les paramètres optimaux par défaut.
    """
    full_request = BigRAGRequest(
        query=request.query,
        country_hint=request.country,
        top_k=8,
        include_global=True,
        rerank=True,
    )
    
    try:
        response = await bigrag_service.query(full_request)
        return {
            "answer": response.answer,
            "country": response.country_detected.value,
            "country_emoji": response.country_emoji,
            "language": response.language.value,
            "sources": response.sources[:5],
            "model": response.model_used,
            "time_ms": response.total_time_ms,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# COUNTRY DETECTION
# ============================================

@router.post("/detect-country", response_model=CountryDetectionResult)
async def detect_country(request: DetectCountryRequest):
    """
    🔍 Détecter le pays d'un texte
    
    Analyse le texte et retourne:
    - Pays détecté (DZ, CH, GLOBAL)
    - Confiance (0-1)
    - Langue détectée (fr, ar, de, en)
    - Signaux détectés
    
    **Exemple:**
    ```json
    {"text": "Je veux calculer mes cotisations CNAS"}
    ```
    
    **Retourne:**
    ```json
    {
      "country": "DZ",
      "confidence": 0.95,
      "language": "fr",
      "signals": ["CNAS (+0.95)"]
    }
    ```
    """
    return await bigrag_service.detect_country(request.text)


@router.get("/detect")
async def detect_country_get(
    text: str = Query(..., min_length=3, description="Texte à analyser")
):
    """
    🔍 Détecter le pays (GET)
    
    Version GET pour intégration simple.
    """
    result = await bigrag_service.detect_country(text)
    return {
        "country": result.country.value,
        "country_name": get_country_name(result.country),
        "country_emoji": get_country_emoji(result.country),
        "confidence": result.confidence,
        "language": result.language.value,
        "signals": result.signals,
    }


# ============================================
# SEARCH ENDPOINTS
# ============================================

@router.post("/search", response_model=MultiSearchResult)
async def search_only(request: SearchOnlyRequest):
    """
    🔎 Recherche seule (sans LLM)
    
    Retourne les documents pertinents sans génération de réponse.
    Utile pour:
    - Debug et tests
    - Afficher les sources brutes
    - Intégration avec un autre LLM
    """
    return await bigrag_service.search_only(
        query=request.query,
        top_k=request.top_k,
        country=request.country,
    )


@router.get("/search")
async def search_get(
    query: str = Query(..., min_length=3),
    top_k: int = Query(10, ge=1, le=50),
    country: Optional[str] = Query(None),
):
    """
    🔎 Recherche seule (GET)
    """
    result = await bigrag_service.search_only(
        query=query,
        top_k=top_k,
        country=country,
    )
    return {
        "results": [
            {
                "text": r.text[:500],
                "score": r.score,
                "country": r.metadata.get("country"),
                "source": r.metadata.get("source"),
            }
            for r in result.results
        ],
        "total": result.total,
        "indexes": result.indexes_searched,
        "time_ms": result.search_time_ms,
    }


# ============================================
# INGESTION ENDPOINTS
# ============================================

@router.post("/ingest")
async def ingest_document(
    request: IngestRequest,
    background_tasks: BackgroundTasks,
    x_admin_key: str = Header(None, alias="X-Admin-Key"),
):
    """
    📥 Ingérer un document
    
    Ajoute un document dans l'index approprié selon le pays.
    
    **Nécessite la clé admin X-Admin-Key**
    """
    # Vérification admin
    if x_admin_key != "admin-secret-key-2025":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    from .embedding_pipeline import embedding_pipeline
    from .qdrant_multi import qdrant_multi, get_index_for_country
    
    # Déterminer l'index
    index = get_index_for_country(request.country)
    
    # Créer l'embedding en background
    async def process_ingestion():
        embedding_result = await embedding_pipeline.embed_texts([request.text])
        
        doc = {
            "text": request.text,
            "country": request.country,
            "source": request.source,
            "theme": request.theme,
            "title": request.title,
            "url": request.url,
            **request.metadata,
        }
        
        await qdrant_multi.upsert_documents(
            index_name=index,
            documents=[doc],
            embeddings=embedding_result.embeddings,
        )
    
    background_tasks.add_task(process_ingestion)
    
    return {
        "status": "queued",
        "index": index.value,
        "country": request.country,
        "message": "Document en cours d'ingestion",
    }


@router.post("/ingest/batch")
async def ingest_batch(
    request: IngestBatchRequest,
    background_tasks: BackgroundTasks,
    x_admin_key: str = Header(None, alias="X-Admin-Key"),
):
    """
    📥 Ingérer plusieurs documents
    
    **Nécessite la clé admin X-Admin-Key**
    """
    if x_admin_key != "admin-secret-key-2025":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    from .embedding_pipeline import embedding_pipeline
    from .qdrant_multi import qdrant_multi, get_index_for_country
    
    async def process_batch():
        # Grouper par pays
        by_country = {}
        for doc in request.documents:
            country = doc.country
            if country not in by_country:
                by_country[country] = []
            by_country[country].append(doc)
        
        for country, docs in by_country.items():
            index = get_index_for_country(country)
            texts = [d.text for d in docs]
            
            # Embeddings
            embedding_result = await embedding_pipeline.embed_texts(texts)
            
            # Préparer les documents
            documents = [
                {
                    "text": d.text,
                    "country": d.country,
                    "source": d.source,
                    "theme": d.theme,
                    "title": d.title,
                    "url": d.url,
                    **(d.metadata or {}),
                }
                for d in docs
            ]
            
            await qdrant_multi.upsert_documents(
                index_name=index,
                documents=documents,
                embeddings=embedding_result.embeddings,
            )
    
    background_tasks.add_task(process_batch)
    
    return {
        "status": "queued",
        "documents_count": len(request.documents),
        "message": "Batch en cours d'ingestion",
    }


# ============================================
# STATUS & ADMIN
# ============================================

@router.get("/health")
async def health_check():
    """
    🏥 Vérifier l'état du service BIG RAG
    """
    return await bigrag_service.get_status()


@router.get("/status")
async def get_status():
    """
    📊 Statut détaillé du service
    """
    status = await bigrag_service.get_status()
    return {
        **status,
        "endpoints": {
            "/api/rag/multi/query": "POST - Query complet multi-pays",
            "/api/rag/multi/quick": "POST - Query rapide",
            "/api/rag/multi/detect-country": "POST - Détection pays",
            "/api/rag/multi/search": "POST - Recherche seule",
            "/api/rag/multi/ingest": "POST - Ingestion document",
            "/api/rag/multi/ingest/batch": "POST - Ingestion batch",
        },
        "countries": {
            "DZ": {"name": "Algérie", "emoji": "🇩🇿", "index": "rag_dz"},
            "CH": {"name": "Suisse", "emoji": "🇨🇭", "index": "rag_ch"},
            "GLOBAL": {"name": "International", "emoji": "🌍", "index": "rag_global"},
        },
    }


@router.get("/models")
async def list_models():
    """
    📋 Liste des modèles LLM disponibles
    """
    return {
        "models": [
            {"id": m.value, "name": m.name, "provider": "openai" if "gpt" in m.value else "anthropic" if "claude" in m.value else "groq"}
            for m in LLMModel
        ],
        "default": bigrag_service.default_model.value,
    }


@router.get("/collections")
async def list_collections():
    """
    📦 Liste des collections Qdrant
    """
    from .qdrant_multi import qdrant_multi
    return await qdrant_multi.get_all_collections_info()


# ============================================
# DEMO ENDPOINTS
# ============================================

@router.get("/demo/dz")
async def demo_dz():
    """
    🇩🇿 Démo requête Algérie
    """
    request = BigRAGRequest(
        query="Comment calculer les cotisations CNAS pour un salarié en Algérie ?",
        top_k=5,
        country_hint="DZ",
    )
    
    # Simuler une réponse si pas de données
    detection = await bigrag_service.detect_country(request.query)
    
    return {
        "demo": True,
        "query": request.query,
        "detection": {
            "country": detection.country.value,
            "country_emoji": get_country_emoji(detection.country),
            "confidence": detection.confidence,
            "signals": detection.signals,
            "language": detection.language.value,
        },
        "expected_index": "rag_dz",
        "note": "Ingestez des documents DZ pour obtenir des réponses complètes",
    }


@router.get("/demo/ch")
async def demo_ch():
    """
    🇨🇭 Démo requête Suisse
    """
    request = BigRAGRequest(
        query="Comment calculer les cotisations AVS pour un indépendant en Suisse ?",
        top_k=5,
        country_hint="CH",
    )
    
    detection = await bigrag_service.detect_country(request.query)
    
    return {
        "demo": True,
        "query": request.query,
        "detection": {
            "country": detection.country.value,
            "country_emoji": get_country_emoji(detection.country),
            "confidence": detection.confidence,
            "signals": detection.signals,
            "language": detection.language.value,
        },
        "expected_index": "rag_ch",
        "note": "Ingestez des documents CH pour obtenir des réponses complètes",
    }


@router.get("/demo/detect")
async def demo_detect():
    """
    🔍 Démo détection multi-langue
    """
    examples = [
        {
            "text": "Je veux déclarer mes impôts IRG à la DGI",
            "expected": "DZ",
        },
        {
            "text": "Wie melde ich mich bei der SVA an?",
            "expected": "CH (allemand)",
        },
        {
            "text": "Quelles sont les cotisations LPP en Suisse ?",
            "expected": "CH",
        },
        {
            "text": "أريد حساب ضريبة الدخل",
            "expected": "DZ (arabe)",
        },
        {
            "text": "How to create a company?",
            "expected": "GLOBAL",
        },
    ]
    
    results = []
    for ex in examples:
        detection = await bigrag_service.detect_country(ex["text"])
        results.append({
            "text": ex["text"],
            "expected": ex["expected"],
            "detected": detection.country.value,
            "emoji": get_country_emoji(detection.country),
            "confidence": detection.confidence,
            "language": detection.language.value,
            "signals": detection.signals[:3],
        })
    
    return {"examples": results}


# ============================================
# ADVANCED RAG ENDPOINTS (Agentic Patterns)
# ============================================

from .hybrid_search import hybrid_search_pipeline, SearchMode, HybridSearchResult
from .reasoning_pipeline import reasoning_pipeline, ReasoningResult
from .query_router import hybrid_router, RoutingDecision


class AgenticQueryRequest(BaseModel):
    """Requête RAG Agentic avec raisonnement"""
    query: str = Field(..., min_length=3, description="Question")
    enable_reasoning: bool = Field(True, description="Activer le raisonnement step-by-step")
    enable_hybrid_search: bool = Field(True, description="Activer recherche hybride (vector+BM25)")
    enable_smart_routing: bool = Field(True, description="Activer routage intelligent")
    top_k: int = Field(8, ge=1, le=20, description="Nombre de contextes")
    country_hint: Optional[str] = Field(None, description="Forcer un pays")


class AgenticQueryResponse(BaseModel):
    """Réponse RAG Agentic complète"""
    answer: str
    
    # Routing
    routing: Optional[RoutingDecision] = None
    collections_searched: List[str] = Field(default_factory=list)
    
    # Search
    search_mode: str = "hybrid"
    search_results_count: int = 0
    
    # Reasoning
    reasoning_enabled: bool = False
    reasoning_summary: Optional[str] = None
    confidence: float = 0.0
    
    # Timing
    routing_time_ms: float = 0
    search_time_ms: float = 0
    reasoning_time_ms: float = 0
    llm_time_ms: float = 0
    total_time_ms: float = 0
    
    # Sources
    sources: List[dict] = Field(default_factory=list)


@router.post("/agentic/query", response_model=AgenticQueryResponse)
async def agentic_query(request: AgenticQueryRequest):
    """
    🧠 Query RAG Agentic (Advanced)
    
    Pipeline avancé avec:
    1. **Smart Routing**: Route vers les bonnes collections (DZ, CH, Global)
    2. **Hybrid Search**: Combine Vector + BM25 pour meilleure couverture
    3. **Reasoning**: Analyse step-by-step avant génération
    4. **Enhanced Generation**: Prompt enrichi avec raisonnement
    
    Inspiré des patterns de awesome-llm-apps:
    - Agentic RAG with Reasoning
    - Database Routing
    - Hybrid Search RAG
    """
    import time
    start = time.time()
    
    timings = {
        "routing": 0,
        "search": 0,
        "reasoning": 0,
        "llm": 0,
    }
    
    try:
        # 1. SMART ROUTING
        routing_start = time.time()
        if request.enable_smart_routing:
            routing_decision = await hybrid_router.route(request.query)
            collections = hybrid_router.get_collections_to_search(
                routing_decision,
                include_global=True,
                max_collections=3,
            )
        else:
            routing_decision = None
            # Utiliser la détection pays classique
            detection = await bigrag_service.detect_country(request.query)
            from .qdrant_multi import get_index_for_country
            primary_index = get_index_for_country(detection.country)
            collections = [primary_index.value, "rag_global"]
        
        # Override si country_hint
        if request.country_hint:
            country_upper = request.country_hint.upper()
            if country_upper == "DZ":
                collections = ["rag_dz", "rag_global"]
            elif country_upper == "CH":
                collections = ["rag_ch", "rag_global"]
        
        timings["routing"] = (time.time() - routing_start) * 1000
        
        # 2. SEARCH (Hybrid ou Vector)
        search_start = time.time()
        
        # Obtenir l'embedding
        query_embedding = await bigrag_service.get_embedding(request.query)
        
        # Effectuer la recherche
        search_mode = SearchMode.HYBRID if request.enable_hybrid_search else SearchMode.VECTOR
        
        search_result = await hybrid_search_pipeline.search_multi(
            query=request.query,
            query_vector=query_embedding,
            qdrant_client=bigrag_service._get_qdrant_client(),
            collections=collections,
            top_k=request.top_k,
            mode=search_mode,
        )
        
        timings["search"] = (time.time() - search_start) * 1000
        
        # Convertir en format pour le service
        contexts = [
            {
                "id": r.id,
                "text": r.text,
                "score": r.combined_score,
                "vector_score": r.vector_score,
                "bm25_score": r.bm25_score,
                **r.metadata,
            }
            for r in search_result.results
        ]
        
        # 3. REASONING (optionnel)
        reasoning_start = time.time()
        reasoning_result = None
        enhanced_prompt = None
        
        if request.enable_reasoning and contexts:
            reasoning_result = await reasoning_pipeline.reason(
                query=request.query,
                contexts=contexts,
            )
            
            # Construire le prompt enrichi
            enhanced_prompt = reasoning_pipeline.build_enhanced_prompt(
                query=request.query,
                contexts=contexts,
                reasoning=reasoning_result,
            )
        
        timings["reasoning"] = (time.time() - reasoning_start) * 1000
        
        # 4. LLM GENERATION
        llm_start = time.time()
        
        if enhanced_prompt:
            # Utiliser le prompt enrichi
            answer = await bigrag_service.generate_answer(
                prompt=enhanced_prompt,
                contexts=[],  # Déjà inclus dans le prompt
            )
        else:
            # Génération classique
            answer = await bigrag_service.generate_answer_from_contexts(
                query=request.query,
                contexts=contexts,
            )
        
        timings["llm"] = (time.time() - llm_start) * 1000
        
        total_time = (time.time() - start) * 1000
        
        # Préparer les sources
        sources = [
            {
                "text": ctx["text"][:200] + "..." if len(ctx.get("text", "")) > 200 else ctx.get("text", ""),
                "source": ctx.get("source", "unknown"),
                "country": ctx.get("country", ""),
                "score": ctx.get("score", 0),
            }
            for ctx in contexts[:5]
        ]
        
        return AgenticQueryResponse(
            answer=answer,
            routing=routing_decision,
            collections_searched=collections,
            search_mode=search_mode.value,
            search_results_count=len(search_result.results),
            reasoning_enabled=request.enable_reasoning,
            reasoning_summary=reasoning_result.final_reasoning if reasoning_result else None,
            confidence=reasoning_result.confidence if reasoning_result else 0.7,
            routing_time_ms=timings["routing"],
            search_time_ms=timings["search"],
            reasoning_time_ms=timings["reasoning"],
            llm_time_ms=timings["llm"],
            total_time_ms=total_time,
            sources=sources,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agentic query failed: {str(e)}")


@router.post("/route", response_model=RoutingDecision)
async def route_query(query: str = Query(..., description="Question à router")):
    """
    🔀 Router une question vers les bonnes collections
    
    Analyse la question et détermine:
    - Collection principale à interroger
    - Collections secondaires
    - Pays/domaine détecté
    - Confiance du routage
    """
    try:
        decision = await hybrid_router.route(query)
        return decision
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/collections")
async def list_collections():
    """
    📚 Lister les collections disponibles
    """
    from .query_router import COLLECTION_REGISTRY
    
    return {
        "collections": [
            {
                "id": coll_id,
                "name": config.name,
                "description": config.description,
                "country": config.country,
                "priority": config.priority,
                "keywords_sample": config.keywords[:5],
            }
            for coll_id, config in COLLECTION_REGISTRY.items()
        ]
    }

