"""
IA Factory - Legal Document Reranker
Améliore la pertinence des résultats avec Cohere Rerank ou BGE
"""

import os
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import httpx

logger = logging.getLogger(__name__)

# Configuration
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
RERANKER_MODEL = os.getenv("RERANKER_MODEL", "rerank-multilingual-v3.0")
RERANKER_ENABLED = os.getenv("RERANKER_ENABLED", "true").lower() == "true"


@dataclass
class RankedResult:
    """Résultat re-ranké avec score de pertinence"""
    original_index: int
    content: str
    relevance_score: float  # 0.0 à 1.0
    article_number: Optional[str] = None
    source_title: str = ""
    context_prefix: str = ""
    original_score: float = 0.0


class LegalReranker:
    """
    Re-ranker pour documents juridiques.

    Utilise Cohere Rerank pour transformer les scores RRF relatifs
    en scores de pertinence absolus (probabilité de pertinence).
    """

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or COHERE_API_KEY
        self.model = model or RERANKER_MODEL
        self.enabled = RERANKER_ENABLED and bool(self.api_key)

        if not self.enabled:
            logger.warning("Reranker disabled - COHERE_API_KEY not set")

    async def rerank(
        self,
        query: str,
        documents: List[Dict],
        top_n: int = 10,
        return_documents: bool = True
    ) -> List[RankedResult]:
        """
        Re-rank les documents selon leur pertinence à la requête.

        Args:
            query: La requête utilisateur
            documents: Liste de documents avec 'content', 'article_number', etc.
            top_n: Nombre de résultats à retourner
            return_documents: Inclure le contenu dans la réponse

        Returns:
            Liste de RankedResult ordonnée par pertinence décroissante
        """
        if not documents:
            return []

        if not self.enabled:
            # Fallback: retourner les documents dans l'ordre original
            return self._fallback_ranking(documents, top_n)

        try:
            return await self._cohere_rerank(query, documents, top_n)
        except Exception as e:
            logger.error(f"Reranking failed: {e}, using fallback")
            return self._fallback_ranking(documents, top_n)

    async def _cohere_rerank(
        self,
        query: str,
        documents: List[Dict],
        top_n: int
    ) -> List[RankedResult]:
        """Appel à l'API Cohere Rerank"""

        # Préparer les documents pour Cohere
        doc_texts = []
        for doc in documents:
            # Enrichir avec le contexte pour meilleur ranking
            text = f"{doc.get('context_prefix', '')} {doc.get('content', '')}"
            doc_texts.append(text.strip())

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.cohere.ai/v1/rerank",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "query": query,
                    "documents": doc_texts,
                    "top_n": min(top_n, len(documents)),
                    "return_documents": False  # On a déjà les docs
                }
            )

            response.raise_for_status()
            data = response.json()

        # Construire les résultats
        results = []
        for item in data.get("results", []):
            idx = item["index"]
            original_doc = documents[idx]

            results.append(RankedResult(
                original_index=idx,
                content=original_doc.get("content", ""),
                relevance_score=item["relevance_score"],
                article_number=original_doc.get("article_number"),
                source_title=original_doc.get("source_title", ""),
                context_prefix=original_doc.get("context_prefix", ""),
                original_score=original_doc.get("score", 0.0)
            ))

        logger.info(f"Reranked {len(documents)} docs → top {len(results)} results")
        return results

    def _fallback_ranking(
        self,
        documents: List[Dict],
        top_n: int
    ) -> List[RankedResult]:
        """Fallback sans re-ranking (garde l'ordre original)"""
        results = []
        for i, doc in enumerate(documents[:top_n]):
            # Normaliser le score original en 0-1
            original_score = doc.get("score", 0.0)
            # Approximation: score RRF max ~0.03, on normalise
            normalized_score = min(original_score * 5, 1.0)

            results.append(RankedResult(
                original_index=i,
                content=doc.get("content", ""),
                relevance_score=normalized_score,
                article_number=doc.get("article_number"),
                source_title=doc.get("source_title", ""),
                context_prefix=doc.get("context_prefix", ""),
                original_score=original_score
            ))

        return results


class LegalSearchEnhancer:
    """
    Améliore la recherche juridique avec:
    - Re-ranking
    - Expansion de requête
    - Filtrage intelligent
    """

    def __init__(self):
        self.reranker = LegalReranker()

    async def enhanced_search(
        self,
        query: str,
        raw_results: List[Dict],
        top_n: int = 10,
        min_relevance: float = 0.3
    ) -> Tuple[List[RankedResult], Dict]:
        """
        Pipeline de recherche améliorée.

        Returns:
            Tuple[results, metadata] avec:
            - results: Liste de RankedResult filtrés
            - metadata: Infos sur le traitement (temps, scores, etc.)
        """
        import time
        start = time.time()

        # 1. Re-ranking
        reranked = await self.reranker.rerank(query, raw_results, top_n * 2)

        # 2. Filtrage par seuil de pertinence
        filtered = [r for r in reranked if r.relevance_score >= min_relevance]

        # 3. Limiter aux top_n
        final_results = filtered[:top_n]

        # 4. Calculer les métadonnées
        elapsed = time.time() - start
        metadata = {
            "original_count": len(raw_results),
            "reranked_count": len(reranked),
            "filtered_count": len(filtered),
            "final_count": len(final_results),
            "processing_time_ms": round(elapsed * 1000, 2),
            "reranker_enabled": self.reranker.enabled,
            "min_relevance_threshold": min_relevance,
            "avg_relevance": round(
                sum(r.relevance_score for r in final_results) / len(final_results), 3
            ) if final_results else 0
        }

        return final_results, metadata

    def expand_legal_query(self, query: str) -> str:
        """
        Expansion de requête avec synonymes juridiques.

        Exemple: "responsabilité" → "responsabilité responsable faute obligation"
        """
        # Dictionnaire de synonymes juridiques français
        legal_synonyms = {
            "responsabilité": ["responsable", "faute", "obligation", "imputation"],
            "dommage": ["préjudice", "tort", "atteinte", "lésion"],
            "contrat": ["convention", "accord", "engagement", "stipulation"],
            "obligation": ["devoir", "engagement", "charge", "dette"],
            "créancier": ["ayant droit", "bénéficiaire"],
            "débiteur": ["obligé", "redevable"],
            "réparation": ["indemnisation", "compensation", "dédommagement"],
            "faute": ["négligence", "imprudence", "manquement"],
            "nullité": ["annulation", "résolution", "caducité"],
            "prescription": ["délai", "forclusion", "péremption"],
        }

        words = query.lower().split()
        expanded_terms = set(words)

        for word in words:
            if word in legal_synonyms:
                expanded_terms.update(legal_synonyms[word])

        return " ".join(expanded_terms)


# Instance globale pour réutilisation
search_enhancer = LegalSearchEnhancer()
