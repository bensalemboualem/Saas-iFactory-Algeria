"""
Client PGVector pour PostgreSQL
Alternative/Complément à Qdrant pour recherche vectorielle
Inspiré d'Archon - utilise pgvector natif dans Postgres
"""

import logging
from typing import List, Dict, Any, Optional
import asyncpg
from asyncpg.pool import Pool
import os

logger = logging.getLogger(__name__)


class PGVectorClient:
    """Client pour recherche vectorielle avec PostgreSQL + pgvector"""

    def __init__(self, connection_pool: Optional[Pool] = None):
        """
        Initialise le client PGVector

        Args:
            connection_pool: Pool de connexions asyncpg (optionnel)
        """
        self.pool = connection_pool
        self._connection_string = os.getenv("POSTGRES_URL")
        if not self._connection_string:
            raise ValueError("POSTGRES_URL environment variable is required")

    async def get_pool(self) -> Pool:
        """Obtient ou crée un pool de connexions"""
        if not self.pool:
            try:
                self.pool = await asyncpg.create_pool(
                    self._connection_string,
                    min_size=2,
                    max_size=10,
                    command_timeout=60
                )
                logger.info("Pool de connexions PGVector créé")
            except Exception as e:
                logger.error(f"Erreur création pool PGVector: {e}")
                raise
        return self.pool

    async def close(self):
        """Ferme le pool de connexions"""
        if self.pool:
            await self.pool.close()
            logger.info("Pool PGVector fermé")

    async def insert_embeddings(
        self,
        embeddings: List[Dict[str, Any]],
        tenant_id: str
    ) -> bool:
        """
        Insère des embeddings dans la base

        Args:
            embeddings: Liste de dicts avec text, embedding, metadata, etc.
            tenant_id: ID du tenant

        Returns:
            True si succès
        """
        pool = await self.get_pool()

        try:
            async with pool.acquire() as conn:
                # Préparer les données pour insertion batch
                records = [
                    (
                        tenant_id,
                        emb.get('document_id', ''),
                        emb.get('chunk_index', 0),
                        emb['text'],
                        emb['embedding'],  # Liste de floats
                        emb.get('metadata', {}),
                        emb.get('language', 'fr'),
                        emb.get('title', ''),
                        emb.get('source_url', '')
                    )
                    for emb in embeddings
                ]

                # Insertion batch
                await conn.executemany(
                    """
                    INSERT INTO document_embeddings
                    (tenant_id, document_id, chunk_index, text, embedding,
                     metadata, language, title, source_url)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                    """,
                    records
                )

                logger.info(f"Inséré {len(embeddings)} embeddings pour tenant {tenant_id}")
                return True

        except Exception as e:
            logger.error(f"Erreur insertion embeddings: {e}")
            return False

    async def search_documents(
        self,
        query_embedding: List[float],
        tenant_id: str,
        match_threshold: float = 0.3,
        match_count: int = 10,
        filter_language: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Recherche documents par similarité vectorielle

        Args:
            query_embedding: Vecteur de la query
            tenant_id: ID du tenant
            match_threshold: Seuil de similarité minimum
            match_count: Nombre max de résultats
            filter_language: Filtrer par langue (optionnel)

        Returns:
            Liste de documents avec scores
        """
        pool = await self.get_pool()

        try:
            async with pool.acquire() as conn:
                # Utiliser la fonction SQL définie dans la migration
                rows = await conn.fetch(
                    """
                    SELECT * FROM search_documents_hybrid(
                        $1::vector, $2::uuid, $3, $4, $5
                    )
                    """,
                    query_embedding,
                    tenant_id,
                    match_threshold,
                    match_count,
                    filter_language
                )

                results = []
                for row in rows:
                    results.append({
                        'id': str(row['id']),
                        'document_id': row['document_id'],
                        'text': row['text'],
                        'title': row['title'],
                        'language': row['language'],
                        'score': float(row['similarity']),
                        'metadata': row['metadata'],
                        'created_at': row['created_at'].isoformat() if row['created_at'] else None
                    })

                logger.info(f"Recherche PGVector: {len(results)} résultats trouvés")
                return results

        except Exception as e:
            logger.error(f"Erreur recherche PGVector: {e}")
            return []

    async def search_code_examples(
        self,
        query_embedding: List[float],
        tenant_id: str,
        match_threshold: float = 0.3,
        match_count: int = 5,
        filter_language: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Recherche exemples de code par similarité

        Args:
            query_embedding: Vecteur de la query
            tenant_id: ID du tenant
            match_threshold: Seuil de similarité
            match_count: Nombre de résultats
            filter_language: Langage de prog (Python, JS, etc.)

        Returns:
            Liste d'exemples de code
        """
        pool = await self.get_pool()

        try:
            async with pool.acquire() as conn:
                rows = await conn.fetch(
                    """
                    SELECT * FROM search_code_examples(
                        $1::vector, $2::uuid, $3, $4, $5
                    )
                    """,
                    query_embedding,
                    tenant_id,
                    match_threshold,
                    match_count,
                    filter_language
                )

                results = []
                for row in rows:
                    results.append({
                        'id': str(row['id']),
                        'code': row['code'],
                        'language': row['language'],
                        'description': row['description'],
                        'score': float(row['similarity']),
                        'metadata': row['metadata']
                    })

                logger.info(f"Recherche code: {len(results)} exemples trouvés")
                return results

        except Exception as e:
            logger.error(f"Erreur recherche code PGVector: {e}")
            return []

    async def insert_code_example(
        self,
        code: str,
        language: str,
        embedding: List[float],
        tenant_id: str,
        description: Optional[str] = None,
        metadata: Optional[Dict] = None,
        source_id: Optional[str] = None
    ) -> bool:
        """
        Insère un exemple de code avec embedding

        Args:
            code: Code source
            language: Langage (Python, JavaScript, etc.)
            embedding: Vecteur embedding
            tenant_id: ID du tenant
            description: Description (optionnel)
            metadata: Métadonnées (optionnel)
            source_id: ID de la source (optionnel)

        Returns:
            True si succès
        """
        pool = await self.get_pool()

        try:
            async with pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO code_examples
                    (tenant_id, source_id, code, language, description, embedding, metadata)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                    """,
                    tenant_id,
                    source_id,
                    code,
                    language,
                    description,
                    embedding,
                    metadata or {}
                )

                logger.info(f"Code example inséré: {language}")
                return True

        except Exception as e:
            logger.error(f"Erreur insertion code example: {e}")
            return False

    async def delete_tenant_data(self, tenant_id: str) -> bool:
        """
        Supprime toutes les données d'un tenant

        Args:
            tenant_id: ID du tenant

        Returns:
            True si succès
        """
        pool = await self.get_pool()

        try:
            async with pool.acquire() as conn:
                async with conn.transaction():
                    # Supprimer embeddings
                    await conn.execute(
                        "DELETE FROM document_embeddings WHERE tenant_id = $1",
                        tenant_id
                    )
                    # Supprimer code examples
                    await conn.execute(
                        "DELETE FROM code_examples WHERE tenant_id = $1",
                        tenant_id
                    )

                logger.info(f"Données PGVector supprimées pour tenant {tenant_id}")
                return True

        except Exception as e:
            logger.error(f"Erreur suppression données tenant: {e}")
            return False

    async def get_stats(self, tenant_id: str) -> Dict[str, Any]:
        """
        Obtient les statistiques d'embeddings pour un tenant

        Args:
            tenant_id: ID du tenant

        Returns:
            Dict avec statistiques
        """
        pool = await self.get_pool()

        try:
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    """
                    SELECT
                        COUNT(*) as total_embeddings,
                        COUNT(DISTINCT document_id) as unique_documents,
                        AVG(LENGTH(text))::int as avg_text_length,
                        MIN(created_at) as first_embedding,
                        MAX(created_at) as last_embedding
                    FROM document_embeddings
                    WHERE tenant_id = $1
                    """,
                    tenant_id
                )

                if row:
                    return {
                        'total_embeddings': row['total_embeddings'],
                        'unique_documents': row['unique_documents'],
                        'avg_text_length': row['avg_text_length'],
                        'first_embedding': row['first_embedding'].isoformat() if row['first_embedding'] else None,
                        'last_embedding': row['last_embedding'].isoformat() if row['last_embedding'] else None
                    }
                return {}

        except Exception as e:
            logger.error(f"Erreur récupération stats: {e}")
            return {}


# Instance globale (similaire à qdrant_client)
pgvector_client = PGVectorClient()
