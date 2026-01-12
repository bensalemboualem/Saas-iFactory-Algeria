"""
Vector Store Service for RAG
Handles ChromaDB operations for document storage and retrieval
"""

import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from .embedding_service import EmbeddingService


@dataclass
class SearchResult:
    """Search result with document and metadata"""
    content: str
    metadata: Dict[str, Any]
    score: float
    document_id: str


class VectorStoreService:
    """Service for vector database operations with ChromaDB"""

    # Collection names by language and type
    COLLECTIONS = {
        "fr": "bbc_school_fr",
        "ar": "bbc_school_ar",
        "en": "bbc_school_en",
        "courses": "bbc_school_courses",
        "quizzes": "bbc_school_quizzes",
        "guides": "bbc_school_guides",
    }

    def __init__(
        self,
        persist_directory: str = "./data/chromadb",
        embedding_service: Optional[EmbeddingService] = None
    ):
        self.persist_directory = persist_directory
        self.embedding_service = embedding_service or EmbeddingService()

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Cache for collections
        self._collections: Dict[str, Any] = {}

    def get_or_create_collection(
        self,
        name: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Get or create a ChromaDB collection"""
        if name not in self._collections:
            self._collections[name] = self.client.get_or_create_collection(
                name=name,
                metadata=metadata or {"description": f"Collection {name}"}
            )
        return self._collections[name]

    def add_documents(
        self,
        documents: List[Document],
        collection_name: str = "bbc_school_fr",
        language: str = "fr"
    ) -> List[str]:
        """
        Add documents to a collection

        Args:
            documents: List of LangChain Document objects
            collection_name: Name of the collection
            language: Language for embedding selection

        Returns:
            List of document IDs
        """
        collection = self.get_or_create_collection(collection_name)

        # Extract texts and metadata
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]

        # Generate embeddings
        embeddings = self.embedding_service.embed_documents(texts, language)

        # Generate IDs
        ids = [f"{collection_name}_{i}_{hash(text[:100])}" for i, text in enumerate(texts)]

        # Add to collection
        collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        return ids

    def search(
        self,
        query: str,
        collection_name: str = "bbc_school_fr",
        language: str = "fr",
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Search for similar documents

        Args:
            query: Search query
            collection_name: Collection to search
            language: Language for embedding
            n_results: Number of results to return
            filter_metadata: Optional metadata filter

        Returns:
            List of SearchResult objects
        """
        collection = self.get_or_create_collection(collection_name)

        # Generate query embedding
        query_embedding = self.embedding_service.embed_text(query, language)

        # Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_metadata
        )

        # Format results
        search_results = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                search_results.append(SearchResult(
                    content=doc,
                    metadata=results['metadatas'][0][i] if results['metadatas'] else {},
                    score=results['distances'][0][i] if results['distances'] else 0.0,
                    document_id=results['ids'][0][i] if results['ids'] else ""
                ))

        return search_results

    def search_all_collections(
        self,
        query: str,
        language: str = "fr",
        n_results: int = 5
    ) -> List[SearchResult]:
        """Search across all relevant collections"""
        all_results = []

        # Search language-specific collection
        lang_collection = self.COLLECTIONS.get(language, "bbc_school_fr")
        all_results.extend(self.search(query, lang_collection, language, n_results))

        # Search by type
        for type_name in ["courses", "quizzes", "guides"]:
            results = self.search(
                query,
                self.COLLECTIONS[type_name],
                language,
                n_results // 2
            )
            all_results.extend(results)

        # Sort by score and deduplicate
        seen = set()
        unique_results = []
        for r in sorted(all_results, key=lambda x: x.score):
            if r.content[:100] not in seen:
                seen.add(r.content[:100])
                unique_results.append(r)

        return unique_results[:n_results]

    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """Get statistics for a collection"""
        collection = self.get_or_create_collection(collection_name)
        return {
            "name": collection_name,
            "count": collection.count(),
            "metadata": collection.metadata
        }

    def get_all_stats(self) -> Dict[str, Any]:
        """Get statistics for all collections"""
        stats = {}
        for name in self.COLLECTIONS.values():
            try:
                stats[name] = self.get_collection_stats(name)
            except Exception:
                stats[name] = {"name": name, "count": 0, "error": "Collection not found"}
        return stats

    def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection"""
        try:
            self.client.delete_collection(collection_name)
            if collection_name in self._collections:
                del self._collections[collection_name]
            return True
        except Exception:
            return False

    def reset_all(self) -> bool:
        """Reset all collections (use with caution!)"""
        try:
            self.client.reset()
            self._collections.clear()
            return True
        except Exception:
            return False
