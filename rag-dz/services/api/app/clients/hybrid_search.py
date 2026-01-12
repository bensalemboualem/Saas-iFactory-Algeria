from typing import List, Dict, Any, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
import logging

from .embeddings import embed_queries
from .qdrant_client import client as qdrant_client
from .reranking import RerankingStrategy, load_reranking_config
from meilisearch import Client as MeiliClient
import os

logger = logging.getLogger(__name__)

class HybridSearchEngine:
    def __init__(self):
        self.meili_client = MeiliClient(
            url=os.getenv("MEILI_URL", "http://meilisearch:7700"),
            api_key=os.getenv("MEILI_MASTER_KEY", "ragdzMasterKey2024")
        )
        self.executor = ThreadPoolExecutor(max_workers=4)

        # Initialiser le reranking si activé
        reranking_config = load_reranking_config()
        self.use_reranking = reranking_config['enabled']
        self.reranking_top_k = reranking_config['top_k']
        self.reranking_strategy = None

        if self.use_reranking:
            try:
                self.reranking_strategy = RerankingStrategy(
                    model_name=reranking_config['model_name']
                )
                if self.reranking_strategy.is_available():
                    logger.info("Reranking strategy activée avec succès")
                else:
                    logger.warning("Reranking activé mais modèle non disponible")
                    self.use_reranking = False
            except Exception as e:
                logger.error(f"Échec d'initialisation du reranking: {e}")
                self.use_reranking = False
    
    def setup_meilisearch_index(self, collection_name: str):
        """Configurer index Meilisearch pour recherche lexicale"""
        try:
            try:
                index = self.meili_client.get_index(collection_name)
            except:
                index = self.meili_client.create_index(collection_name, {'primaryKey': 'id'})
            
            index.update_settings({
                'searchableAttributes': ['title', 'text', 'language'],
                'filterableAttributes': ['tenant_id', 'language', 'created_at'],
                'sortableAttributes': ['created_at'],
                'typoTolerance': {
                    'enabled': True,
                    'minWordSizeForTypos': {'oneTypo': 4, 'twoTypos': 8}
                }
            })
            
            return index
        except Exception as e:
            logger.error(f"Meilisearch setup error: {e}")
            return None
    
    def add_to_meilisearch(self, collection_name: str, documents: List[Dict]):
        """Ajouter documents à Meilisearch"""
        try:
            index = self.setup_meilisearch_index(collection_name)
            if index:
                index.add_documents(documents)
        except Exception as e:
            logger.error(f"Meilisearch indexing error: {e}")

    def _search_meilisearch(self, collection_name: str, query: str, tenant_id: str, max_results: int) -> List[Dict[str, Any]]:
        """Recherche lexicale via Meilisearch (exécutée dans un thread)."""
        index = self.setup_meilisearch_index(collection_name)
        if not index:
            return []
        try:
            search_params = {
                "limit": max_results,
                "filter": [f"tenant_id = '{tenant_id}'"],
            }
            response = index.search(query, search_params)
            hits = response.get("hits", [])
            results: List[Dict[str, Any]] = []
            for rank, hit in enumerate(hits, start=1):
                raw_score = hit.get("_rankingScore")
                score = float(raw_score) if raw_score is not None else 1.0 / rank
                results.append({
                    "id": str(hit.get("id")),
                    "title": hit.get("title", ""),
                    "text": hit.get("text", ""),
                    "language": hit.get("language", "fr"),
                    "score": score,
                    "lexical_rank": rank,
                    "created_at": hit.get("created_at"),
                })
            return results
        except Exception as e:
            logger.error(f"Meilisearch query error: {e}")
            return []
    
    async def hybrid_search(self, query: str, tenant_id: str, collection_name: str, max_results: int = 10) -> Dict[str, Any]:
        """Recherche hybride complete combinant vectoriel et lexical"""
        start_time = time.time()

        try:
            query_vector = embed_queries([query])[0]
        except Exception as e:
            logger.error(f"Embedding generation error: {e}")
            query_vector = []

        vector_results: List[Dict[str, Any]] = []
        if query_vector:
            try:
                raw_vector_results = qdrant_client.search(
                    collection_name=collection_name,
                    query_vector=query_vector,
                    limit=max_results,
                    score_threshold=0.3
                )

                for rank, result in enumerate(raw_vector_results, start=1):
                    payload = result.payload or {}
                    score = float(result.score) if result.score is not None else 0.0
                    vector_results.append({
                        'id': str(result.id),
                        'title': payload.get('title', ''),
                        'text': payload.get('text', ''),
                        'language': payload.get('language', 'fr'),
                        'score': score,
                        'vector_score': score,
                        'vector_rank': rank,
                        'source': 'vector',
                        'created_at': payload.get('created_at'),
                    })
            except Exception as e:
                logger.error(f"Vector search error: {e}")

        lexical_results: List[Dict[str, Any]] = []
        try:
            loop = asyncio.get_running_loop()
            lexical_results = await loop.run_in_executor(
                self.executor,
                self._search_meilisearch,
                collection_name,
                query,
                tenant_id,
                max_results,
            )
        except Exception as e:
            logger.error(f"Meilisearch hybrid error: {e}")

        combined: List[Dict[str, Any]] = []
        seen: Dict[str, Dict[str, Any]] = {}

        for item in vector_results:
            combined.append(item)
            seen[item['id']] = item

        for lexical_item in lexical_results:
            lexical_id = lexical_item.get('id')
            if not lexical_id:
                continue

            lexical_score = float(lexical_item.get('score') or 0.0)
            existing = seen.get(lexical_id)
            if existing:
                existing['lexical_score'] = lexical_score
                existing['score'] = max(existing.get('score', 0.0), lexical_score)
                if existing.get('source') == 'vector':
                    existing['source'] = 'hybrid'
            else:
                lexical_item = dict(lexical_item)
                lexical_item['lexical_score'] = lexical_score
                lexical_item['score'] = lexical_score
                lexical_item['source'] = 'lexical'
                combined.append(lexical_item)
                seen[lexical_id] = lexical_item

        combined.sort(key=lambda item: item.get('score', 0.0), reverse=True)
        if len(combined) > max_results:
            combined = combined[:max_results]

        # Appliquer reranking si activé
        if self.use_reranking and self.reranking_strategy and combined:
            logger.info(f"Application du reranking sur {len(combined)} résultats")
            combined = await self.reranking_strategy.rerank_results(
                query=query,
                results=combined,
                content_key='text',  # Utiliser 'text' au lieu de 'content'
                top_k=self.reranking_top_k
            )

        search_time = (time.time() - start_time) * 1000

        return {
            'results': combined,
            'search_time_ms': int(search_time),
            'vector_count': len(vector_results),
            'lexical_count': len(lexical_results),
            'total_results': len(combined),
            'reranked': self.use_reranking and self.reranking_strategy is not None
        }
    
    def generate_answer(self, query: str, results: List[Dict], language: str = "fr") -> str:
        """Génération de réponse basée sur contexte"""
        if not results:
            if language == "ar":
                return "لم يتم العثور على مستندات ذات صلة في قاعدة المعرفة."
            elif language == "en":
                return "No relevant documents found in the knowledge base."
            else:
                return "Aucun document pertinent trouvé dans la base de connaissances."
        
        context_parts = []
        for i, result in enumerate(results[:3]):
            text = result.get('text', '')[:400]
            title = result.get('title', f'Document {i+1}')
            context_parts.append(f"[{title}] {text}")
        
        context = "\n\n".join(context_parts)
        
        if language == "ar":
            return f"بناءً على المستندات الموجودة:\n\n{context}"
        elif language == "en":
            return f"Based on the found documents:\n\n{context}"
        else:
            return f"Basé sur les documents trouvés:\n\n{context}"

