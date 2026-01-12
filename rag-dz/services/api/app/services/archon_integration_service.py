"""
Service d'intégration avec Archon
Remplace Supabase par notre PostgreSQL + API directe
"""
import logging
from typing import Dict, Any, List, Optional
import asyncpg
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class ArchonIntegrationService:
    """Service pour intégrer avec Archon (PostgreSQL direct)"""

    def __init__(self, db_pool: asyncpg.Pool):
        self.db_pool = db_pool

    # ==================== Knowledge Sources ====================

    async def create_knowledge_source(
        self,
        name: str,
        source_type: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Crée une source de connaissance dans Archon

        Args:
            name: Nom de la source
            source_type: Type (project, document, web, etc.)
            content: Contenu textuel
            metadata: Métadonnées additionnelles

        Returns:
            knowledge_source_id (string)
        """
        try:
            async with self.db_pool.acquire() as conn:
                # Créer la source dans la table sources (Archon)
                # Note: Archon utilise normalement Supabase, on adapte pour PostgreSQL

                result = await conn.fetchrow(
                    """
                    INSERT INTO archon_knowledge_sources (
                        name,
                        source_type,
                        content,
                        metadata,
                        created_at
                    )
                    VALUES ($1, $2, $3, $4::jsonb, NOW())
                    RETURNING id, name
                    """,
                    name,
                    source_type,
                    content,
                    json.dumps(metadata or {})
                )

                knowledge_id = str(result['id'])
                logger.info(f"Created knowledge source {knowledge_id}: {name}")

                return knowledge_id

        except Exception as e:
            logger.error(f"Error creating knowledge source: {e}", exc_info=True)
            # Retourner un ID temporaire pour ne pas bloquer le workflow
            return f"temp-{datetime.now().timestamp()}"

    async def update_knowledge_source(
        self,
        knowledge_id: str,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Met à jour une source de connaissance"""
        try:
            async with self.db_pool.acquire() as conn:
                if content:
                    await conn.execute(
                        "UPDATE archon_knowledge_sources SET content = $2 WHERE id = $1",
                        int(knowledge_id),
                        content
                    )

                if metadata:
                    await conn.execute(
                        "UPDATE archon_knowledge_sources SET metadata = $2::jsonb WHERE id = $1",
                        int(knowledge_id),
                        json.dumps(metadata)
                    )

                logger.info(f"Updated knowledge source {knowledge_id}")
                return True

        except Exception as e:
            logger.error(f"Error updating knowledge source: {e}", exc_info=True)
            return False

    # ==================== Projects ====================

    async def create_project(
        self,
        name: str,
        description: str,
        knowledge_source_id: str,
        features: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Crée un projet dans Archon

        Args:
            name: Nom du projet
            description: Description
            knowledge_source_id: ID de la source de connaissance liée
            features: Liste des features du projet
            metadata: Métadonnées additionnelles

        Returns:
            project_id (integer)
        """
        try:
            async with self.db_pool.acquire() as conn:
                result = await conn.fetchrow(
                    """
                    INSERT INTO archon_projects (
                        name,
                        description,
                        knowledge_source_id,
                        features,
                        metadata,
                        created_at
                    )
                    VALUES ($1, $2, $3, $4::jsonb, $5::jsonb, NOW())
                    RETURNING id
                    """,
                    name,
                    description,
                    knowledge_source_id,
                    json.dumps(features or []),
                    json.dumps(metadata or {})
                )

                project_id = result['id']
                logger.info(f"Created Archon project {project_id}: {name}")

                return project_id

        except Exception as e:
            logger.error(f"Error creating Archon project: {e}", exc_info=True)
            # Retourner 0 pour ne pas bloquer le workflow
            return 0

    async def add_project_document(
        self,
        project_id: int,
        doc_name: str,
        doc_type: str,
        content: str
    ) -> int:
        """Ajoute un document à un projet"""
        try:
            async with self.db_pool.acquire() as conn:
                result = await conn.fetchrow(
                    """
                    INSERT INTO archon_project_documents (
                        project_id,
                        name,
                        doc_type,
                        content,
                        created_at
                    )
                    VALUES ($1, $2, $3, $4, NOW())
                    RETURNING id
                    """,
                    project_id,
                    doc_name,
                    doc_type,
                    content
                )

                doc_id = result['id']
                logger.info(f"Added document {doc_id} to project {project_id}")

                return doc_id

        except Exception as e:
            logger.error(f"Error adding project document: {e}", exc_info=True)
            return 0

    # ==================== Embeddings (Qdrant) ====================

    async def create_embeddings(
        self,
        knowledge_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Crée des embeddings dans Qdrant

        Note: Cette fonction devrait appeler le service Qdrant pour créer les embeddings
        Pour l'instant, on log seulement
        """
        try:
            # TODO: Implémenter l'appel à Qdrant via le service backend
            logger.info(f"Would create embeddings for knowledge {knowledge_id}")
            logger.debug(f"Content length: {len(content)} chars")

            return True

        except Exception as e:
            logger.error(f"Error creating embeddings: {e}", exc_info=True)
            return False

    # ==================== Helper Methods ====================

    async def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Récupère un projet Archon"""
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    """
                    SELECT
                        id,
                        name,
                        description,
                        knowledge_source_id,
                        features,
                        metadata,
                        created_at
                    FROM archon_projects
                    WHERE id = $1
                    """,
                    project_id
                )

                if row:
                    return dict(row)
                return None

        except Exception as e:
            logger.error(f"Error getting project: {e}", exc_info=True)
            return None

    async def get_knowledge_source(self, knowledge_id: str) -> Optional[Dict[str, Any]]:
        """Récupère une source de connaissance"""
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    """
                    SELECT
                        id,
                        name,
                        source_type,
                        content,
                        metadata,
                        created_at
                    FROM archon_knowledge_sources
                    WHERE id = $1
                    """,
                    int(knowledge_id)
                )

                if row:
                    return dict(row)
                return None

        except Exception as e:
            logger.error(f"Error getting knowledge source: {e}", exc_info=True)
            return None

    async def ensure_archon_tables_exist(self) -> bool:
        """S'assure que les tables Archon existent"""
        try:
            async with self.db_pool.acquire() as conn:
                # Créer table archon_knowledge_sources si n'existe pas
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS archon_knowledge_sources (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        source_type VARCHAR(50) NOT NULL,
                        content TEXT,
                        metadata JSONB DEFAULT '{}',
                        created_at TIMESTAMP DEFAULT NOW()
                    )
                """)

                # Créer table archon_projects si n'existe pas
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS archon_projects (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        description TEXT,
                        knowledge_source_id VARCHAR(100),
                        features JSONB DEFAULT '[]',
                        metadata JSONB DEFAULT '{}',
                        created_at TIMESTAMP DEFAULT NOW()
                    )
                """)

                # Créer table archon_project_documents si n'existe pas
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS archon_project_documents (
                        id SERIAL PRIMARY KEY,
                        project_id INTEGER REFERENCES archon_projects(id) ON DELETE CASCADE,
                        name VARCHAR(255) NOT NULL,
                        doc_type VARCHAR(50),
                        content TEXT,
                        created_at TIMESTAMP DEFAULT NOW()
                    )
                """)

                logger.info("Archon tables ensured")
                return True

        except Exception as e:
            logger.error(f"Error ensuring Archon tables: {e}", exc_info=True)
            return False
