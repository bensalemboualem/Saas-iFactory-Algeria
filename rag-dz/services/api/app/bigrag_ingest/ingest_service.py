"""
INGEST_DZ_CH - Service d'Ingestion
==================================
Service pour ingérer des documents dans BIG RAG Multi-Pays

Ce service:
1. Génère les embeddings pour chaque document
2. Envoie les vecteurs vers Qdrant (rag_dz, rag_ch, rag_global)
3. Stocke les métadonnées (country, language, theme, source, etc.)
4. Gère les erreurs et retourne un rapport détaillé
"""

import os
import json
import time
import logging
import uuid
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from pathlib import Path

# Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
from qdrant_client.http.exceptions import UnexpectedResponse

# Models
from .ingest_models import (
    RAGDocument,
    RAGDocumentCreate,
    RAGIngestBatch,
    RAGIngestFile,
    IngestResult,
    IngestStats,
    CollectionStatus,
    IngestStatusResponse,
    IngestStatus,
    COUNTRY_TO_COLLECTION,
    DEFAULT_COLLECTIONS,
)

# Embedding (sentence-transformers)
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

# OpenAI embeddings (fallback)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


logger = logging.getLogger(__name__)


# ============================================
# EMBEDDING PIPELINE
# ============================================

class EmbeddingPipeline:
    """
    Pipeline d'embeddings pour les documents RAG
    
    Supporte:
    - sentence-transformers (local, multilingue)
    - OpenAI embeddings (cloud)
    """
    
    def __init__(
        self,
        model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
        use_openai: bool = False,
        openai_model: str = "text-embedding-3-small",
        device: str = "cpu",
    ):
        self.model_name = model_name
        self.use_openai = use_openai
        self.openai_model = openai_model
        self.device = device
        
        # Initialiser le modèle
        self._model = None
        self._openai_client = None
        self._vector_size = 768  # Défaut pour multilingual-mpnet
        
    def _init_model(self):
        """Initialise le modèle d'embeddings"""
        if self.use_openai:
            if not OPENAI_AVAILABLE:
                raise ImportError("OpenAI not installed")
            self._openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self._vector_size = 1536 if "3-small" in self.openai_model else 3072
            logger.info(f"Using OpenAI embeddings: {self.openai_model}")
        else:
            if not SENTENCE_TRANSFORMERS_AVAILABLE:
                raise ImportError("sentence-transformers not installed")
            self._model = SentenceTransformer(self.model_name, device=self.device)
            self._vector_size = self._model.get_sentence_embedding_dimension()
            logger.info(f"Using local embeddings: {self.model_name} (dim={self._vector_size})")
    
    @property
    def vector_size(self) -> int:
        if self._model is None and self._openai_client is None:
            self._init_model()
        return self._vector_size
    
    def embed_text(self, text: str) -> List[float]:
        """Génère l'embedding pour un texte"""
        if self._model is None and self._openai_client is None:
            self._init_model()
        
        if self.use_openai and self._openai_client:
            response = self._openai_client.embeddings.create(
                model=self.openai_model,
                input=text,
            )
            return response.data[0].embedding
        else:
            embedding = self._model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
    
    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """Génère les embeddings pour plusieurs textes"""
        if self._model is None and self._openai_client is None:
            self._init_model()
        
        if self.use_openai and self._openai_client:
            embeddings = []
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i+batch_size]
                response = self._openai_client.embeddings.create(
                    model=self.openai_model,
                    input=batch,
                )
                embeddings.extend([d.embedding for d in response.data])
            return embeddings
        else:
            embeddings = self._model.encode(texts, convert_to_numpy=True, batch_size=batch_size)
            return embeddings.tolist()


# ============================================
# INGEST SERVICE
# ============================================

class IngestService:
    """
    Service d'ingestion pour BIG RAG Multi-Pays
    
    Gère l'ingestion de documents vers les collections Qdrant:
    - rag_dz: Documents Algérie
    - rag_ch: Documents Suisse
    - rag_global: Documents internationaux
    """
    
    def __init__(
        self,
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
        use_openai_embeddings: bool = False,
        embedding_device: str = "cpu",
    ):
        """
        Initialise le service d'ingestion
        
        Args:
            qdrant_host: Hôte Qdrant
            qdrant_port: Port Qdrant
            embedding_model: Modèle d'embeddings
            use_openai_embeddings: Utiliser OpenAI pour les embeddings
            embedding_device: Device pour sentence-transformers (cpu/cuda)
        """
        self.qdrant_host = qdrant_host
        self.qdrant_port = qdrant_port
        
        # Client Qdrant
        self.qdrant = QdrantClient(host=qdrant_host, port=qdrant_port)
        
        # Pipeline d'embeddings
        self.embedder = EmbeddingPipeline(
            model_name=embedding_model,
            use_openai=use_openai_embeddings,
            device=embedding_device,
        )
        
        logger.info(f"IngestService initialized: Qdrant={qdrant_host}:{qdrant_port}")
    
    # ----------------------------------------
    # COLLECTION MANAGEMENT
    # ----------------------------------------
    
    def ensure_collection(self, collection_name: str) -> bool:
        """S'assure que la collection existe, la crée si nécessaire"""
        try:
            collections = self.qdrant.get_collections().collections
            exists = any(c.name == collection_name for c in collections)
            
            if not exists:
                self.qdrant.create_collection(
                    collection_name=collection_name,
                    vectors_config=qdrant_models.VectorParams(
                        size=self.embedder.vector_size,
                        distance=qdrant_models.Distance.COSINE,
                    ),
                )
                logger.info(f"Collection '{collection_name}' created")
            
            return True
            
        except Exception as e:
            logger.error(f"Error ensuring collection '{collection_name}': {e}")
            return False
    
    def get_collection_status(self, collection_name: str) -> CollectionStatus:
        """Retourne le statut d'une collection"""
        try:
            info = self.qdrant.get_collection(collection_name)
            return CollectionStatus(
                name=collection_name,
                exists=True,
                vectors_count=info.vectors_count or 0,
                points_count=info.points_count or 0,
                segments_count=info.segments_count or 0,
                status=info.status.value if info.status else "unknown",
                vector_size=info.config.params.vectors.size if info.config else 0,
            )
        except UnexpectedResponse:
            return CollectionStatus(name=collection_name, exists=False)
        except Exception as e:
            logger.error(f"Error getting collection status: {e}")
            return CollectionStatus(name=collection_name, exists=False, status=str(e))
    
    # ----------------------------------------
    # MAIN INGESTION METHODS
    # ----------------------------------------
    
    async def ingest_batch(self, batch: RAGIngestBatch) -> IngestResult:
        """
        Ingère un batch de documents dans une collection
        
        Args:
            batch: Batch avec collection et documents
            
        Returns:
            IngestResult avec statistiques
        """
        start_time = time.time()
        collection = batch.collection
        docs = batch.docs
        
        # Résultat
        result = IngestResult(
            collection=collection,
            total=len(docs),
            status=IngestStatus.PROCESSING,
        )
        
        # Vérifier/créer la collection
        if not self.ensure_collection(collection):
            result.success = False
            result.status = IngestStatus.FAILED
            result.errors.append(f"Failed to ensure collection '{collection}'")
            return result
        
        # Préparer les points
        points = []
        errors = []
        
        for doc in docs:
            try:
                # Générer ID si absent
                doc_id = doc.id or str(uuid.uuid4())
                
                # Texte pour embedding (title + text)
                embed_text = f"{doc.title}\n\n{doc.text}"
                if doc.summary:
                    embed_text = f"{doc.title}\n\n{doc.summary}\n\n{doc.text}"
                
                # Générer embedding
                embedding = self.embedder.embed_text(embed_text)
                
                # Payload (métadonnées)
                payload = {
                    "title": doc.title,
                    "text": doc.text,
                    "country": doc.country,
                    "language": doc.language,
                    "theme": doc.theme,
                    "source": doc.source,
                    "url": doc.url,
                    "date": doc.date.isoformat() if doc.date else None,
                    "tags": doc.tags,
                    "is_official": doc.is_official,
                    "summary": doc.summary,
                    "chunk_index": doc.chunk_index,
                    "total_chunks": doc.total_chunks,
                    "parent_id": doc.parent_id,
                    "extra": doc.extra,
                    "ingested_at": datetime.utcnow().isoformat(),
                }
                
                # Créer le point Qdrant
                point = qdrant_models.PointStruct(
                    id=doc_id,
                    vector=embedding,
                    payload=payload,
                )
                points.append(point)
                
            except Exception as e:
                errors.append(f"Doc '{doc.id or doc.title[:30]}': {str(e)}")
                result.failed_ids.append(doc.id or "unknown")
        
        # Upsert les points dans Qdrant
        if points:
            try:
                self.qdrant.upsert(
                    collection_name=collection,
                    points=points,
                    wait=True,
                )
                result.inserted = len(points)
            except Exception as e:
                errors.append(f"Qdrant upsert error: {str(e)}")
                result.status = IngestStatus.FAILED
        
        # Finaliser le résultat
        result.failed = len(docs) - len(points)
        result.errors = errors
        result.processing_time_ms = int((time.time() - start_time) * 1000)
        
        if result.failed == 0:
            result.status = IngestStatus.SUCCESS
            result.success = True
        elif result.inserted > 0:
            result.status = IngestStatus.PARTIAL
            result.success = True
        else:
            result.status = IngestStatus.FAILED
            result.success = False
        
        logger.info(f"Ingest batch: {collection} - {result.inserted}/{result.total} docs, {result.processing_time_ms}ms")
        return result
    
    # ----------------------------------------
    # COUNTRY-SPECIFIC HELPERS
    # ----------------------------------------
    
    async def ingest_dz_docs(self, docs: List[RAGDocument]) -> IngestResult:
        """Ingère des documents dans rag_dz (Algérie)"""
        # Forcer country = DZ
        for doc in docs:
            doc.country = "DZ"
        
        batch = RAGIngestBatch(collection="rag_dz", docs=docs)
        return await self.ingest_batch(batch)
    
    async def ingest_ch_docs(self, docs: List[RAGDocument]) -> IngestResult:
        """Ingère des documents dans rag_ch (Suisse)"""
        # Forcer country = CH
        for doc in docs:
            doc.country = "CH"
        
        batch = RAGIngestBatch(collection="rag_ch", docs=docs)
        return await self.ingest_batch(batch)
    
    async def ingest_global_docs(self, docs: List[RAGDocument]) -> IngestResult:
        """Ingère des documents dans rag_global"""
        # Forcer country = GLOBAL
        for doc in docs:
            doc.country = "GLOBAL"
        
        batch = RAGIngestBatch(collection="rag_global", docs=docs)
        return await self.ingest_batch(batch)
    
    async def ingest_by_country(self, docs: List[RAGDocument]) -> Dict[str, IngestResult]:
        """
        Ingère des documents en les routant vers la bonne collection selon le pays
        
        Returns:
            Dict avec résultats par collection
        """
        # Grouper par pays
        by_country: Dict[str, List[RAGDocument]] = {"DZ": [], "CH": [], "GLOBAL": []}
        
        for doc in docs:
            country = doc.country.upper()
            if country in by_country:
                by_country[country].append(doc)
            else:
                by_country["GLOBAL"].append(doc)
        
        # Ingérer chaque groupe
        results = {}
        
        if by_country["DZ"]:
            results["rag_dz"] = await self.ingest_dz_docs(by_country["DZ"])
        
        if by_country["CH"]:
            results["rag_ch"] = await self.ingest_ch_docs(by_country["CH"])
        
        if by_country["GLOBAL"]:
            results["rag_global"] = await self.ingest_global_docs(by_country["GLOBAL"])
        
        return results
    
    # ----------------------------------------
    # FILE INGESTION
    # ----------------------------------------
    
    async def ingest_from_file(self, file_path: str, collection: str) -> IngestResult:
        """
        Ingère des documents depuis un fichier JSON ou NDJSON
        
        Args:
            file_path: Chemin du fichier
            collection: Collection cible
            
        Returns:
            IngestResult
        """
        path = Path(file_path)
        
        if not path.exists():
            return IngestResult(
                collection=collection,
                success=False,
                status=IngestStatus.FAILED,
                errors=[f"File not found: {file_path}"],
            )
        
        docs = []
        
        try:
            content = path.read_text(encoding="utf-8")
            
            # JSON array
            if file_path.endswith(".json"):
                data = json.loads(content)
                if isinstance(data, list):
                    docs = [RAGDocument(**d) for d in data]
                elif isinstance(data, dict) and "docs" in data:
                    docs = [RAGDocument(**d) for d in data["docs"]]
            
            # NDJSON (une ligne = un document)
            elif file_path.endswith(".ndjson") or file_path.endswith(".jsonl"):
                for line in content.strip().split("\n"):
                    if line.strip():
                        docs.append(RAGDocument(**json.loads(line)))
            
        except Exception as e:
            return IngestResult(
                collection=collection,
                success=False,
                status=IngestStatus.FAILED,
                errors=[f"File parsing error: {str(e)}"],
            )
        
        if not docs:
            return IngestResult(
                collection=collection,
                success=True,
                status=IngestStatus.SUCCESS,
                total=0,
            )
        
        batch = RAGIngestBatch(collection=collection, docs=docs)
        return await self.ingest_batch(batch)
    
    # ----------------------------------------
    # STATUS
    # ----------------------------------------
    
    async def get_status(self) -> IngestStatusResponse:
        """Retourne le statut global des collections"""
        collections = []
        total = 0
        dz_count = 0
        ch_count = 0
        global_count = 0
        
        for name in ["rag_dz", "rag_ch", "rag_global"]:
            status = self.get_collection_status(name)
            collections.append(status)
            total += status.points_count
            
            if name == "rag_dz":
                dz_count = status.points_count
            elif name == "rag_ch":
                ch_count = status.points_count
            elif name == "rag_global":
                global_count = status.points_count
        
        return IngestStatusResponse(
            ready=True,
            collections=collections,
            total_documents=total,
            dz_count=dz_count,
            ch_count=ch_count,
            global_count=global_count,
            embedding_model=self.embedder.model_name,
            qdrant_host=f"{self.qdrant_host}:{self.qdrant_port}",
        )


# ============================================
# SINGLETON
# ============================================

_ingest_service: Optional[IngestService] = None


def get_ingest_service() -> IngestService:
    """Retourne l'instance singleton du service d'ingestion"""
    global _ingest_service
    if _ingest_service is None:
        _ingest_service = IngestService(
            qdrant_host=os.getenv("QDRANT_HOST", "localhost"),
            qdrant_port=int(os.getenv("QDRANT_PORT", "6333")),
            embedding_model=os.getenv(
                "EMBEDDING_MODEL", 
                "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
            ),
            embedding_device=os.getenv("EMBEDDING_DEVICE", "cpu"),
        )
    return _ingest_service


def init_ingest_service(**kwargs) -> IngestService:
    """Initialise le service avec configuration custom"""
    global _ingest_service
    _ingest_service = IngestService(**kwargs)
    return _ingest_service
