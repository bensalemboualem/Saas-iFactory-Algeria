"""
BIG RAG - Qdrant Multi-Index
=============================
Gestion multi-index Qdrant pour RAG international
rag_dz, rag_ch, rag_global avec recherche hybride
"""

import os
import uuid
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from enum import Enum
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# ============================================
# ENUMS & MODELS
# ============================================

class IndexName(str, Enum):
    """Noms des index Qdrant"""
    RAG_DZ = "rag_dz"
    RAG_CH = "rag_ch"
    RAG_GLOBAL = "rag_global"
    RAG_FR = "rag_fr"  # France (optionnel)


class DocumentMetadata(BaseModel):
    """Métadonnées d'un document"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    country: str = Field(..., description="Pays (DZ, CH, FR, GLOBAL)")
    source: str = Field(..., description="Source du document")
    theme: Optional[str] = Field(None, description="Thème/catégorie")
    title: Optional[str] = Field(None, description="Titre du document")
    date: Optional[str] = Field(None, description="Date du document")
    language: str = Field("fr", description="Langue")
    url: Optional[str] = Field(None, description="URL source")
    
    # Métadonnées additionnelles
    chunk_index: int = Field(0, description="Index du chunk")
    total_chunks: int = Field(1, description="Nombre total de chunks")
    file_type: Optional[str] = Field(None, description="Type de fichier")
    
    # Indexation
    indexed_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class SearchResult(BaseModel):
    """Résultat de recherche"""
    id: str
    text: str
    score: float
    metadata: Dict[str, Any]
    index_name: str


class MultiSearchResult(BaseModel):
    """Résultats de recherche multi-index"""
    results: List[SearchResult]
    total: int
    indexes_searched: List[str]
    query: str
    search_time_ms: float


# ============================================
# QDRANT CLIENT WRAPPER
# ============================================

class QdrantMultiIndex:
    """
    Client Qdrant multi-index pour RAG international
    
    Gère plusieurs collections:
    - rag_dz: Documents Algérie
    - rag_ch: Documents Suisse
    - rag_global: Documents internationaux
    """
    
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        vector_size: int = 1536,
    ):
        self.host = host or os.getenv("QDRANT_HOST", "localhost")
        self.port = port or int(os.getenv("QDRANT_PORT", "6333"))
        self.url = url or os.getenv("QDRANT_URL")
        self.api_key = api_key or os.getenv("QDRANT_API_KEY")
        self.vector_size = vector_size
        
        self._client = None
        self._indexes = [IndexName.RAG_DZ, IndexName.RAG_CH, IndexName.RAG_GLOBAL]
    
    def _get_client(self):
        """Obtenir le client Qdrant (lazy loading)"""
        if self._client is None:
            try:
                from qdrant_client import QdrantClient
                
                if self.url:
                    self._client = QdrantClient(
                        url=self.url,
                        api_key=self.api_key,
                    )
                else:
                    self._client = QdrantClient(
                        host=self.host,
                        port=self.port,
                    )
                
                logger.info(f"Connected to Qdrant at {self.url or f'{self.host}:{self.port}'}")
                
            except ImportError:
                raise RuntimeError(
                    "qdrant-client not installed. "
                    "Run: pip install qdrant-client"
                )
        
        return self._client
    
    async def ensure_collections(self):
        """Créer les collections si elles n'existent pas"""
        from qdrant_client.models import Distance, VectorParams
        
        client = self._get_client()
        
        for index_name in self._indexes:
            try:
                client.get_collection(index_name.value)
                logger.info(f"Collection {index_name.value} exists")
            except Exception:
                client.create_collection(
                    collection_name=index_name.value,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE,
                    ),
                )
                logger.info(f"Created collection {index_name.value}")
    
    async def upsert_documents(
        self,
        index_name: IndexName,
        documents: List[Dict[str, Any]],
        embeddings: List[List[float]],
    ) -> int:
        """
        Insérer ou mettre à jour des documents
        
        Args:
            index_name: Nom de l'index
            documents: Liste de documents avec métadonnées
            embeddings: Embeddings correspondants
            
        Returns:
            Nombre de documents insérés
        """
        from qdrant_client.models import PointStruct
        
        client = self._get_client()
        
        points = []
        for doc, embedding in zip(documents, embeddings):
            point_id = doc.get("id", str(uuid.uuid4()))
            
            # Préparer le payload
            payload = {
                "text": doc.get("text", ""),
                "country": doc.get("country", "GLOBAL"),
                "source": doc.get("source", "unknown"),
                "theme": doc.get("theme"),
                "title": doc.get("title"),
                "date": doc.get("date"),
                "language": doc.get("language", "fr"),
                "url": doc.get("url"),
                "chunk_index": doc.get("chunk_index", 0),
                "indexed_at": datetime.utcnow().isoformat(),
            }
            
            # Ajouter métadonnées custom
            for key, value in doc.items():
                if key not in payload and key not in ["text", "embedding"]:
                    payload[key] = value
            
            points.append(PointStruct(
                id=point_id if isinstance(point_id, int) else hash(point_id) % (2**63),
                vector=embedding,
                payload=payload,
            ))
        
        client.upsert(
            collection_name=index_name.value,
            points=points,
        )
        
        logger.info(f"Upserted {len(points)} documents to {index_name.value}")
        return len(points)
    
    async def search(
        self,
        index_name: IndexName,
        query_vector: List[float],
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        score_threshold: float = 0.0,
    ) -> List[SearchResult]:
        """
        Recherche dans un index spécifique
        
        Args:
            index_name: Nom de l'index
            query_vector: Vecteur de requête
            top_k: Nombre de résultats
            filters: Filtres Qdrant
            score_threshold: Score minimum
            
        Returns:
            Liste de SearchResult
        """
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        
        client = self._get_client()
        
        # Construire les filtres Qdrant
        qdrant_filter = None
        if filters:
            conditions = []
            for key, value in filters.items():
                if isinstance(value, list):
                    for v in value:
                        conditions.append(
                            FieldCondition(key=key, match=MatchValue(value=v))
                        )
                else:
                    conditions.append(
                        FieldCondition(key=key, match=MatchValue(value=value))
                    )
            if conditions:
                qdrant_filter = Filter(should=conditions)
        
        try:
            results = client.search(
                collection_name=index_name.value,
                query_vector=query_vector,
                limit=top_k,
                query_filter=qdrant_filter,
                score_threshold=score_threshold,
            )
        except Exception as e:
            logger.warning(f"Search failed in {index_name.value}: {e}")
            return []
        
        search_results = []
        for result in results:
            payload = result.payload or {}
            search_results.append(SearchResult(
                id=str(result.id),
                text=payload.get("text", ""),
                score=result.score,
                metadata={k: v for k, v in payload.items() if k != "text"},
                index_name=index_name.value,
            ))
        
        return search_results
    
    async def search_multi(
        self,
        indexes: List[IndexName],
        query_vector: List[float],
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> MultiSearchResult:
        """
        Recherche dans plusieurs index simultanément
        
        Args:
            indexes: Liste des index à chercher
            query_vector: Vecteur de requête
            top_k: Nombre de résultats par index
            filters: Filtres optionnels
            
        Returns:
            MultiSearchResult avec résultats fusionnés
        """
        import time
        start = time.time()
        
        all_results = []
        
        for index_name in indexes:
            try:
                results = await self.search(
                    index_name=index_name,
                    query_vector=query_vector,
                    top_k=top_k,
                    filters=filters,
                )
                all_results.extend(results)
            except Exception as e:
                logger.warning(f"Search failed in {index_name.value}: {e}")
        
        # Trier par score et dédupliquer
        all_results.sort(key=lambda x: x.score, reverse=True)
        
        # Dédupliquer par texte (garder le meilleur score)
        seen_texts = set()
        unique_results = []
        for result in all_results:
            text_hash = hash(result.text[:200])
            if text_hash not in seen_texts:
                seen_texts.add(text_hash)
                unique_results.append(result)
        
        search_time = (time.time() - start) * 1000
        
        return MultiSearchResult(
            results=unique_results[:top_k * len(indexes)],
            total=len(unique_results),
            indexes_searched=[idx.value for idx in indexes],
            query="",  # Sera rempli par l'appelant
            search_time_ms=round(search_time, 2),
        )
    
    async def hybrid_search(
        self,
        query_vector: List[float],
        primary_country: str,
        top_k_primary: int = 8,
        top_k_secondary: int = 3,
    ) -> MultiSearchResult:
        """
        Recherche hybride: index principal + index global
        
        Args:
            query_vector: Vecteur de requête
            primary_country: Pays principal (DZ, CH)
            top_k_primary: Résultats de l'index principal
            top_k_secondary: Résultats de l'index global
            
        Returns:
            Résultats fusionnés avec priorité pays
        """
        import time
        start = time.time()
        
        # Déterminer l'index principal
        primary_index = {
            "DZ": IndexName.RAG_DZ,
            "CH": IndexName.RAG_CH,
        }.get(primary_country, IndexName.RAG_GLOBAL)
        
        # Recherche index principal
        primary_results = await self.search(
            index_name=primary_index,
            query_vector=query_vector,
            top_k=top_k_primary,
        )
        
        # Boost des scores pour le pays principal
        for result in primary_results:
            result.score *= 1.2  # Bonus 20%
        
        # Recherche index global (si différent)
        global_results = []
        if primary_index != IndexName.RAG_GLOBAL:
            global_results = await self.search(
                index_name=IndexName.RAG_GLOBAL,
                query_vector=query_vector,
                top_k=top_k_secondary,
            )
        
        # Fusionner et trier
        all_results = primary_results + global_results
        all_results.sort(key=lambda x: x.score, reverse=True)
        
        # Dédupliquer
        seen_texts = set()
        unique_results = []
        for result in all_results:
            text_hash = hash(result.text[:200])
            if text_hash not in seen_texts:
                seen_texts.add(text_hash)
                unique_results.append(result)
        
        search_time = (time.time() - start) * 1000
        
        indexes_searched = [primary_index.value]
        if primary_index != IndexName.RAG_GLOBAL:
            indexes_searched.append(IndexName.RAG_GLOBAL.value)
        
        return MultiSearchResult(
            results=unique_results[:top_k_primary + top_k_secondary],
            total=len(unique_results),
            indexes_searched=indexes_searched,
            query="",
            search_time_ms=round(search_time, 2),
        )
    
    async def get_collection_info(self, index_name: IndexName) -> Dict[str, Any]:
        """Obtenir les informations sur une collection"""
        client = self._get_client()
        
        try:
            info = client.get_collection(index_name.value)
            return {
                "name": index_name.value,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status.value,
                "config": {
                    "size": info.config.params.vectors.size,
                    "distance": info.config.params.vectors.distance.value,
                },
            }
        except Exception as e:
            return {
                "name": index_name.value,
                "error": str(e),
            }
    
    async def get_all_collections_info(self) -> List[Dict[str, Any]]:
        """Obtenir les infos de toutes les collections"""
        infos = []
        for index_name in self._indexes:
            info = await self.get_collection_info(index_name)
            infos.append(info)
        return infos
    
    async def delete_by_filter(
        self,
        index_name: IndexName,
        filters: Dict[str, Any],
    ) -> int:
        """Supprimer des documents par filtre"""
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        
        client = self._get_client()
        
        conditions = []
        for key, value in filters.items():
            conditions.append(
                FieldCondition(key=key, match=MatchValue(value=value))
            )
        
        if not conditions:
            return 0
        
        qdrant_filter = Filter(must=conditions)
        
        result = client.delete(
            collection_name=index_name.value,
            points_selector=qdrant_filter,
        )
        
        logger.info(f"Deleted documents from {index_name.value} with filter {filters}")
        return result.status


# ============================================
# SINGLETON
# ============================================

qdrant_multi = QdrantMultiIndex(
    vector_size=int(os.getenv("EMBEDDING_DIMENSION", "1536")),
)


# ============================================
# UTILITY FUNCTIONS
# ============================================

def get_index_for_country(country: str) -> IndexName:
    """Retourne l'index approprié pour un pays"""
    return {
        "DZ": IndexName.RAG_DZ,
        "CH": IndexName.RAG_CH,
        "FR": IndexName.RAG_FR,
    }.get(country, IndexName.RAG_GLOBAL)


def get_all_indexes() -> List[IndexName]:
    """Retourne tous les index disponibles"""
    return [IndexName.RAG_DZ, IndexName.RAG_CH, IndexName.RAG_GLOBAL]
