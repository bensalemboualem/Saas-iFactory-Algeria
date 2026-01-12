"""
RAG Public API - Endpoint public pour recherche sans authentification
Pour l'intégration avec le frontend Bolt
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import time
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/rag", tags=["RAG Public"])


class RagQueryRequest(BaseModel):
    """Requête de recherche RAG"""
    query: str = Field(..., min_length=1, max_length=1000, description="Question de recherche")
    region: str = Field(default="DZ", description="Région (DZ, CH, FR)")
    max_results: int = Field(default=5, ge=1, le=20, description="Nombre max de résultats")
    include_metadata: bool = Field(default=True, description="Inclure les métadonnées")
    rerank: bool = Field(default=False, description="Reranker les résultats")


class RagSource(BaseModel):
    """Source de résultat RAG"""
    id: str
    title: str
    content: str
    score: float
    metadata: Optional[dict] = None


class RagQueryResponse(BaseModel):
    """Réponse de recherche RAG"""
    success: bool
    query: str
    answer: str
    sources: List[RagSource]
    confidence: float
    processing_time: float


# Base de connaissances simulée pour démonstration
DEMO_KNOWLEDGE_BASE = [
    {
        "id": "doc_1",
        "title": "Loi 18-07 - Protection des données personnelles",
        "content": "La loi 18-07 du 10 juin 2018 relative à la protection des personnes physiques dans le traitement des données à caractère personnel établit les règles de collecte, traitement et conservation des données personnelles en Algérie. Elle définit les droits des personnes concernées et les obligations des responsables de traitement.",
        "category": "legal",
        "region": "DZ"
    },
    {
        "id": "doc_2",
        "title": "ARPCE - Régulation des télécoms",
        "content": "L'Autorité de Régulation de la Poste et des Communications Électroniques (ARPCE) est l'organisme de régulation du secteur des télécommunications en Algérie. Elle veille à la conformité des opérateurs et à la protection des consommateurs.",
        "category": "telecom",
        "region": "DZ"
    },
    {
        "id": "doc_3",
        "title": "Mobilis - Forfaits entreprise",
        "content": "Mobilis propose des solutions entreprise incluant des forfaits voix/data, des solutions M2M et des services cloud. Les offres incluent l'assistance technique 24/7 et des SLA garantis pour les professionnels.",
        "category": "telecom",
        "region": "DZ"
    },
    {
        "id": "doc_4",
        "title": "LPD Suisse - Nouvelle loi sur la protection des données",
        "content": "La nouvelle Loi sur la Protection des Données (nLPD) suisse entrée en vigueur le 1er septembre 2023 renforce les droits des personnes concernées et impose de nouvelles obligations aux entreprises traitant des données personnelles.",
        "category": "legal",
        "region": "CH"
    },
    {
        "id": "doc_5",
        "title": "RGPD - Règlement européen",
        "content": "Le Règlement Général sur la Protection des Données (RGPD) est le cadre juridique européen pour la protection des données personnelles. Il s'applique à toute organisation traitant des données de résidents européens.",
        "category": "legal",
        "region": "FR"
    },
    {
        "id": "doc_6",
        "title": "IA Factory - Plateforme souveraine",
        "content": "IA Factory est une plateforme d'intelligence artificielle souveraine permettant aux entreprises algériennes de bénéficier des technologies IA tout en gardant leurs données sur le territoire national. Elle inclut des fonctionnalités de chat, RAG et automatisation.",
        "category": "tech",
        "region": "DZ"
    },
    {
        "id": "doc_7",
        "title": "BMAD - Build Measure Analyze Deploy",
        "content": "BMAD est une méthodologie de développement agile intégrant des agents IA spécialisés. Elle comprend des agents Architecte, Développeur, QA, DevOps et Product Manager pour accompagner chaque phase du projet.",
        "category": "tech",
        "region": "DZ"
    },
    {
        "id": "doc_8",
        "title": "Archon - Framework d'agents IA",
        "content": "Archon est un framework permettant de créer et orchestrer des agents IA. Il supporte multiple LLMs (GPT-4, Claude, Llama) et intègre des fonctionnalités RAG pour augmenter les réponses avec des connaissances contextuelles.",
        "category": "tech",
        "region": "DZ"
    }
]


def simple_search(query: str, region: str, max_results: int) -> List[dict]:
    """Recherche simple par mots-clés"""
    query_lower = query.lower()
    query_words = set(query_lower.split())

    results = []
    for doc in DEMO_KNOWLEDGE_BASE:
        # Filtrer par région si spécifié
        if region and doc.get("region") != region and region != "ALL":
            continue

        # Score basé sur les mots-clés trouvés
        doc_text = f"{doc['title']} {doc['content']}".lower()
        matches = sum(1 for word in query_words if word in doc_text)

        if matches > 0:
            score = min(0.95, matches / len(query_words) * 0.8 + 0.2)
            results.append({
                **doc,
                "score": score
            })

    # Trier par score et limiter
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:max_results]


def generate_answer(query: str, sources: List[dict]) -> str:
    """Génère une réponse basée sur les sources"""
    if not sources:
        return "Je n'ai pas trouvé d'information pertinente dans ma base de connaissances pour répondre à cette question."

    # Construire une réponse simple basée sur les sources
    top_source = sources[0]
    answer = f"Basé sur les documents disponibles: {top_source['content'][:300]}"

    if len(sources) > 1:
        answer += f"\n\nPour plus d'informations, consultez également: {sources[1]['title']}."

    return answer


@router.post("/query", response_model=RagQueryResponse)
async def rag_query(request: RagQueryRequest):
    """
    Recherche RAG publique

    Effectue une recherche sémantique dans la base de connaissances
    et retourne une réponse avec les sources.
    """
    start_time = time.time()

    try:
        # Recherche dans la base de connaissances
        raw_results = simple_search(
            query=request.query,
            region=request.region,
            max_results=request.max_results
        )

        # Formater les sources
        sources = []
        for r in raw_results:
            source = RagSource(
                id=r["id"],
                title=r["title"],
                content=r["content"],
                score=r["score"],
                metadata={
                    "category": r.get("category"),
                    "region": r.get("region"),
                    "source_type": "document"
                } if request.include_metadata else None
            )
            sources.append(source)

        # Générer la réponse
        answer = generate_answer(request.query, raw_results)

        # Calculer la confiance
        confidence = sum(s.score for s in sources) / len(sources) * 100 if sources else 0

        processing_time = (time.time() - start_time) * 1000

        return RagQueryResponse(
            success=True,
            query=request.query,
            answer=answer,
            sources=sources,
            confidence=round(confidence, 1),
            processing_time=round(processing_time, 2)
        )

    except Exception as e:
        logger.error(f"RAG query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def rag_health():
    """Health check pour le service RAG"""
    return {
        "status": "healthy",
        "service": "RAG Public API",
        "documents_count": len(DEMO_KNOWLEDGE_BASE),
        "timestamp": time.time()
    }
