"""
Client Supabase pour RAG.dz
Intégration avec Supabase (PostgreSQL cloud + PGVector)
"""

import os
import logging
from typing import List, Dict, Any, Optional
from supabase import create_client, Client

logger = logging.getLogger(__name__)


class SupabaseClient:
    """Client pour interagir avec Supabase"""

    def __init__(self):
        """Initialise le client Supabase"""
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_SERVICE_KEY")

        if not self.url or not self.key:
            logger.warning("SUPABASE_URL ou SUPABASE_SERVICE_KEY non configurés")
            self.client = None
        else:
            try:
                self.client: Client = create_client(self.url, self.key)
                logger.info(f"Client Supabase initialisé: {self.url}")
            except Exception as e:
                logger.error(f"Erreur initialisation Supabase: {e}")
                self.client = None

    def is_available(self) -> bool:
        """Vérifie si Supabase est configuré et disponible"""
        return self.client is not None

    async def insert_document_embedding(
        self,
        tenant_id: str,
        document_id: str,
        text: str,
        embedding: List[float],
        metadata: Optional[Dict] = None,
        language: str = "fr",
        title: Optional[str] = None,
        source_url: Optional[str] = None,
        chunk_index: int = 0
    ) -> bool:
        """
        Insère un embedding de document dans Supabase

        Args:
            tenant_id: ID du tenant
            document_id: ID du document
            text: Texte du chunk
            embedding: Vecteur embedding (768 dimensions)
            metadata: Métadonnées additionnelles
            language: Langue du texte
            title: Titre du document
            source_url: URL source
            chunk_index: Index du chunk

        Returns:
            True si succès
        """
        if not self.is_available():
            logger.error("Supabase non disponible")
            return False

        try:
            data = {
                "tenant_id": tenant_id,
                "document_id": document_id,
                "chunk_index": chunk_index,
                "text": text,
                "embedding": embedding,
                "metadata": metadata or {},
                "language": language,
                "title": title or "",
                "source_url": source_url or ""
            }

            result = self.client.table("document_embeddings").insert(data).execute()

            if result.data:
                logger.info(f"Embedding inséré: {document_id} chunk {chunk_index}")
                return True
            else:
                logger.error(f"Échec insertion embedding: {result}")
                return False

        except Exception as e:
            logger.error(f"Erreur insertion Supabase: {e}")
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
        Recherche documents par similarité vectorielle dans Supabase

        Args:
            query_embedding: Vecteur de la query
            tenant_id: ID du tenant
            match_threshold: Seuil de similarité (0-1)
            match_count: Nombre de résultats
            filter_language: Filtrer par langue

        Returns:
            Liste de documents avec scores
        """
        if not self.is_available():
            logger.error("Supabase non disponible")
            return []

        try:
            # Utiliser la fonction RPC Supabase pour recherche vectorielle
            params = {
                "query_embedding": query_embedding,
                "p_tenant_id": tenant_id,
                "match_threshold": match_threshold,
                "match_count": match_count,
                "filter_language": filter_language
            }

            result = self.client.rpc("search_documents_hybrid", params).execute()

            if result.data:
                logger.info(f"Recherche Supabase: {len(result.data)} résultats")
                return result.data
            else:
                return []

        except Exception as e:
            logger.error(f"Erreur recherche Supabase: {e}")
            return []

    async def get_tenant_stats(self, tenant_id: str) -> Dict[str, Any]:
        """
        Obtient les statistiques d'embeddings pour un tenant

        Args:
            tenant_id: ID du tenant

        Returns:
            Statistiques
        """
        if not self.is_available():
            return {}

        try:
            result = self.client.table("embedding_stats").select("*").eq("tenant_id", tenant_id).execute()

            if result.data and len(result.data) > 0:
                return result.data[0]
            return {}

        except Exception as e:
            logger.error(f"Erreur stats Supabase: {e}")
            return {}

    async def delete_tenant_data(self, tenant_id: str) -> bool:
        """
        Supprime toutes les données d'un tenant

        Args:
            tenant_id: ID du tenant

        Returns:
            True si succès
        """
        if not self.is_available():
            return False

        try:
            # Supprimer les embeddings
            self.client.table("document_embeddings").delete().eq("tenant_id", tenant_id).execute()

            # Supprimer les code examples si la table existe
            try:
                self.client.table("code_examples").delete().eq("tenant_id", tenant_id).execute()
            except:
                pass  # Table peut ne pas exister encore

            logger.info(f"Données Supabase supprimées pour tenant {tenant_id}")
            return True

        except Exception as e:
            logger.error(f"Erreur suppression Supabase: {e}")
            return False

    async def insert_code_example(
        self,
        tenant_id: str,
        code: str,
        language: str,
        embedding: List[float],
        description: Optional[str] = None,
        metadata: Optional[Dict] = None,
        source_id: Optional[str] = None
    ) -> bool:
        """
        Insère un exemple de code avec embedding

        Args:
            tenant_id: ID du tenant
            code: Code source
            language: Langage (Python, JavaScript, etc.)
            embedding: Vecteur embedding
            description: Description
            metadata: Métadonnées
            source_id: ID de la source

        Returns:
            True si succès
        """
        if not self.is_available():
            return False

        try:
            data = {
                "tenant_id": tenant_id,
                "source_id": source_id,
                "code": code,
                "language": language,
                "description": description or "",
                "embedding": embedding,
                "metadata": metadata or {}
            }

            result = self.client.table("code_examples").insert(data).execute()

            if result.data:
                logger.info(f"Code example inséré: {language}")
                return True
            return False

        except Exception as e:
            logger.error(f"Erreur insertion code example: {e}")
            return False

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
            filter_language: Filtrer par langage

        Returns:
            Liste d'exemples de code
        """
        if not self.is_available():
            return []

        try:
            params = {
                "query_embedding": query_embedding,
                "p_tenant_id": tenant_id,
                "match_threshold": match_threshold,
                "match_count": match_count,
                "filter_language": filter_language
            }

            result = self.client.rpc("search_code_examples", params).execute()

            if result.data:
                logger.info(f"Code search: {len(result.data)} exemples trouvés")
                return result.data
            return []

        except Exception as e:
            logger.error(f"Erreur recherche code: {e}")
            return []


# Instance globale
supabase_client = SupabaseClient()
