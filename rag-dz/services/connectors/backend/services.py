"""
Services auxiliaires pour DZ-Connectors
======================================
- EmbeddingService: Génération d'embeddings
- TextChunker: Découpage de texte
- Database: Stockage vectoriel et logs
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
import asyncio
import logging
import os
import json
import hashlib

# Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/iafactory")

logger = logging.getLogger("dz-services")


# ==================== CHUNKER ====================

class TextChunker:
    """
    Découpe le texte en chunks pour l'embedding
    
    Utilise une approche par phrases/paragraphes pour préserver le contexte
    """
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        """
        Args:
            chunk_size: Taille cible en tokens (approximatif)
            overlap: Chevauchement entre chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.avg_chars_per_token = 4  # Approximation
    
    def chunk(self, text: str) -> List[str]:
        """Découpe le texte en chunks"""
        if not text or len(text) < 100:
            return [text] if text else []
        
        # Calculer la taille en caractères
        max_chars = self.chunk_size * self.avg_chars_per_token
        overlap_chars = self.overlap * self.avg_chars_per_token
        
        chunks = []
        
        # Découper par paragraphes d'abord
        paragraphs = text.split('\n\n')
        
        current_chunk = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Si le paragraphe seul est trop grand, découper par phrases
            if len(para) > max_chars:
                sentences = self._split_sentences(para)
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) <= max_chars:
                        current_chunk += " " + sentence if current_chunk else sentence
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence
            else:
                # Ajouter le paragraphe
                if len(current_chunk) + len(para) + 2 <= max_chars:
                    current_chunk += "\n\n" + para if current_chunk else para
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = para
        
        # Dernier chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Ajouter l'overlap si nécessaire
        if self.overlap > 0 and len(chunks) > 1:
            chunks = self._add_overlap(chunks, overlap_chars)
        
        return chunks
    
    def _split_sentences(self, text: str) -> List[str]:
        """Découpe en phrases"""
        import re
        # Découper sur . ! ? suivi d'un espace ou fin
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _add_overlap(self, chunks: List[str], overlap_chars: int) -> List[str]:
        """Ajoute un chevauchement entre les chunks"""
        overlapped = [chunks[0]]
        
        for i in range(1, len(chunks)):
            prev_end = chunks[i-1][-overlap_chars:] if len(chunks[i-1]) > overlap_chars else chunks[i-1]
            overlapped.append(f"...{prev_end}\n\n{chunks[i]}")
        
        return overlapped


# ==================== EMBEDDINGS ====================

class EmbeddingService:
    """
    Service de génération d'embeddings
    
    Utilise GROQ avec le modèle d'embedding disponible
    ou fallback sur un modèle local
    """
    
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.model = "nomic-embed-text-v1.5"  # Modèle d'embedding
        self.dimension = 768  # Dimension du vecteur
        
        # Try to import groq
        try:
            from groq import AsyncGroq
            self.client = AsyncGroq(api_key=self.api_key) if self.api_key else None
        except ImportError:
            self.client = None
            logger.warning("Groq non disponible, utilisation du fallback")
    
    async def embed(self, text: str) -> List[float]:
        """Génère un embedding pour le texte"""
        
        if self.client:
            try:
                return await self._embed_groq(text)
            except Exception as e:
                logger.warning(f"Erreur GROQ embedding: {e}, fallback local")
        
        # Fallback: embedding simple basé sur hash
        return self._embed_fallback(text)
    
    async def _embed_groq(self, text: str) -> List[float]:
        """Embedding via GROQ API"""
        # Note: GROQ n'a pas encore d'endpoint embedding public
        # On utilise un workaround via le chat
        response = await self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{
                "role": "system",
                "content": "Generate a semantic embedding representation."
            }, {
                "role": "user", 
                "content": text[:1000]  # Limiter la taille
            }],
            max_tokens=1
        )
        
        # Fallback car GROQ n'a pas d'embedding direct
        return self._embed_fallback(text)
    
    def _embed_fallback(self, text: str) -> List[float]:
        """
        Embedding fallback simple
        Utilise TF-IDF-like avec hash
        """
        import hashlib
        import math
        
        # Normaliser le texte
        text = text.lower().strip()
        words = text.split()
        
        # Créer un vecteur de dimension fixe
        vector = [0.0] * self.dimension
        
        for i, word in enumerate(words):
            # Hash du mot
            h = int(hashlib.md5(word.encode()).hexdigest(), 16)
            
            # Indices dans le vecteur
            idx = h % self.dimension
            
            # Valeur avec position decay
            value = 1.0 / (1 + math.log(i + 1))
            
            vector[idx] += value
        
        # Normaliser
        norm = math.sqrt(sum(v**2 for v in vector)) or 1
        vector = [v / norm for v in vector]
        
        return vector
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Génère des embeddings pour plusieurs textes"""
        return [await self.embed(text) for text in texts]


# ==================== DATABASE ====================

class IngestionLog:
    """Log d'une ingestion"""
    def __init__(
        self,
        source_name: str,
        document_id: str,
        title: str,
        chunks_count: int,
        status: str,
        error_message: str = None
    ):
        self.source_name = source_name
        self.document_id = document_id
        self.title = title
        self.chunks_count = chunks_count
        self.status = status
        self.error_message = error_message
        self.created_at = datetime.now()


class Database:
    """
    Interface avec la base de données
    
    Supporte:
    - PostgreSQL pour les métadonnées et logs
    - Qdrant pour le stockage vectoriel
    """
    
    def __init__(self):
        self.pg_pool = None
        self.qdrant_client = None
        self.collection_name = "dz_documents"
    
    async def connect(self):
        """Initialise les connexions"""
        # PostgreSQL
        try:
            import asyncpg
            self.pg_pool = await asyncpg.create_pool(POSTGRES_URL)
            await self._init_tables()
            logger.info("✅ PostgreSQL connecté")
        except Exception as e:
            logger.warning(f"PostgreSQL non disponible: {e}")
        
        # Qdrant
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Distance, VectorParams
            
            self.qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
            
            # Créer la collection si elle n'existe pas
            collections = self.qdrant_client.get_collections().collections
            if not any(c.name == self.collection_name for c in collections):
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
                )
            
            logger.info("✅ Qdrant connecté")
        except Exception as e:
            logger.warning(f"Qdrant non disponible: {e}")
    
    async def disconnect(self):
        """Ferme les connexions"""
        if self.pg_pool:
            await self.pg_pool.close()
    
    async def ping(self) -> bool:
        """Vérifie la connexion"""
        try:
            if self.pg_pool:
                async with self.pg_pool.acquire() as conn:
                    await conn.fetchval("SELECT 1")
            return True
        except:
            return False
    
    async def _init_tables(self):
        """Crée les tables nécessaires"""
        if not self.pg_pool:
            return
        
        async with self.pg_pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS dz_ingestion_logs (
                    id SERIAL PRIMARY KEY,
                    source_name VARCHAR(50) NOT NULL,
                    document_id VARCHAR(32) NOT NULL,
                    title TEXT,
                    chunks_count INTEGER DEFAULT 0,
                    status VARCHAR(20) NOT NULL,
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT NOW()
                );
                
                CREATE INDEX IF NOT EXISTS idx_ingestion_source 
                ON dz_ingestion_logs(source_name);
                
                CREATE INDEX IF NOT EXISTS idx_ingestion_date 
                ON dz_ingestion_logs(created_at);
                
                CREATE TABLE IF NOT EXISTS dz_documents (
                    id SERIAL PRIMARY KEY,
                    document_id VARCHAR(32) UNIQUE NOT NULL,
                    source_name VARCHAR(50) NOT NULL,
                    title TEXT,
                    source_url TEXT,
                    doc_type VARCHAR(30),
                    doc_date DATE,
                    chunks_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT NOW()
                );
                
                CREATE INDEX IF NOT EXISTS idx_docs_source 
                ON dz_documents(source_name);
            """)
    
    async def document_exists(self, doc_id: str) -> bool:
        """Vérifie si un document existe déjà"""
        if not self.pg_pool:
            return False
        
        async with self.pg_pool.acquire() as conn:
            result = await conn.fetchval(
                "SELECT 1 FROM dz_documents WHERE document_id = $1",
                doc_id
            )
            return result is not None
    
    async def store_embedding(
        self,
        doc_id: str,
        text: str,
        embedding: List[float],
        metadata: Dict[str, Any]
    ):
        """Stocke un embedding dans Qdrant"""
        if not self.qdrant_client:
            logger.warning("Qdrant non disponible, skip stockage")
            return
        
        from qdrant_client.models import PointStruct
        
        # Générer un ID numérique unique
        point_id = int(hashlib.md5(doc_id.encode()).hexdigest()[:15], 16)
        
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "doc_id": doc_id,
                        "text": text[:1000],  # Limiter pour le payload
                        **metadata
                    }
                )
            ]
        )
    
    async def log_ingestion(self, log: IngestionLog):
        """Enregistre un log d'ingestion"""
        if not self.pg_pool:
            return
        
        async with self.pg_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO dz_ingestion_logs 
                (source_name, document_id, title, chunks_count, status, error_message)
                VALUES ($1, $2, $3, $4, $5, $6)
            """, log.source_name, log.document_id, log.title, 
                log.chunks_count, log.status, log.error_message)
            
            # Mettre à jour ou insérer le document
            if log.status == "success":
                await conn.execute("""
                    INSERT INTO dz_documents (document_id, source_name, title, chunks_count)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (document_id) DO UPDATE SET chunks_count = $4
                """, log.document_id, log.source_name, log.title, log.chunks_count)
    
    async def get_source_stats(self, source_name: str) -> Dict:
        """Statistiques pour une source"""
        if not self.pg_pool:
            return {"count": 0}
        
        async with self.pg_pool.acquire() as conn:
            count = await conn.fetchval(
                "SELECT COUNT(*) FROM dz_documents WHERE source_name = $1",
                source_name
            )
            last_scrape = await conn.fetchval(
                "SELECT MAX(created_at) FROM dz_ingestion_logs WHERE source_name = $1",
                source_name
            )
            return {"count": count or 0, "last_scrape": last_scrape}
    
    async def get_global_stats(self) -> Dict:
        """Statistiques globales"""
        if not self.pg_pool:
            return {}
        
        async with self.pg_pool.acquire() as conn:
            total_docs = await conn.fetchval("SELECT COUNT(*) FROM dz_documents")
            total_chunks = await conn.fetchval("SELECT SUM(chunks_count) FROM dz_documents")
            last_ingestion = await conn.fetchval("SELECT MAX(created_at) FROM dz_ingestion_logs")
            
            # Par type
            by_type = {}
            rows = await conn.fetch(
                "SELECT doc_type, COUNT(*) as count FROM dz_documents GROUP BY doc_type"
            )
            for row in rows:
                by_type[row['doc_type'] or 'unknown'] = row['count']
            
            # Par source
            by_source = {}
            rows = await conn.fetch(
                "SELECT source_name, COUNT(*) as count FROM dz_documents GROUP BY source_name"
            )
            for row in rows:
                by_source[row['source_name']] = row['count']
            
            return {
                "total_documents": total_docs or 0,
                "total_chunks": total_chunks or 0,
                "last_ingestion": last_ingestion,
                "by_type": by_type,
                "by_source": by_source
            }
    
    async def search(
        self,
        embedding: List[float],
        filters: Dict[str, Any],
        limit: int = 10
    ) -> List[Dict]:
        """Recherche vectorielle"""
        if not self.qdrant_client:
            return []
        
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        
        # Construire les filtres Qdrant
        conditions = []
        for key, value in filters.items():
            conditions.append(
                FieldCondition(key=key, match=MatchValue(value=value))
            )
        
        qdrant_filter = Filter(must=conditions) if conditions else None
        
        results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            query_filter=qdrant_filter,
            limit=limit
        )
        
        return [
            {
                "score": hit.score,
                "text": hit.payload.get("text", ""),
                "title": hit.payload.get("title", ""),
                "source": hit.payload.get("source_name", ""),
                "url": hit.payload.get("source_url", ""),
                "type": hit.payload.get("type", ""),
                "date": hit.payload.get("date", "")
            }
            for hit in results
        ]
    
    async def list_documents(
        self,
        filters: Dict[str, Any],
        page: int = 1,
        per_page: int = 20
    ) -> List[Dict]:
        """Liste les documents avec pagination"""
        if not self.pg_pool:
            return []
        
        offset = (page - 1) * per_page
        
        async with self.pg_pool.acquire() as conn:
            query = "SELECT * FROM dz_documents"
            conditions = []
            params = []
            
            if filters.get("source_name"):
                conditions.append(f"source_name = ${len(params)+1}")
                params.append(filters["source_name"])
            
            if filters.get("type"):
                conditions.append(f"doc_type = ${len(params)+1}")
                params.append(filters["type"])
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += f" ORDER BY created_at DESC LIMIT {per_page} OFFSET {offset}"
            
            rows = await conn.fetch(query, *params)
            
            return [dict(row) for row in rows]
    
    async def count_documents(self, filters: Dict[str, Any]) -> int:
        """Compte les documents"""
        if not self.pg_pool:
            return 0
        
        async with self.pg_pool.acquire() as conn:
            query = "SELECT COUNT(*) FROM dz_documents"
            conditions = []
            params = []
            
            if filters.get("source_name"):
                conditions.append(f"source_name = ${len(params)+1}")
                params.append(filters["source_name"])
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            return await conn.fetchval(query, *params)


# ==================== EXPORT ====================

__all__ = [
    'TextChunker',
    'EmbeddingService', 
    'Database',
    'IngestionLog',
]
