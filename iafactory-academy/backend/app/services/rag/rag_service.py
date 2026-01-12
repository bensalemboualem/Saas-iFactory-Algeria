"""
RAG Service - Main orchestration service
Combines document processing, vector store, and LLM for RAG pipeline
"""

import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from .embedding_service import EmbeddingService
from .vector_store import VectorStoreService, SearchResult
from .llm_service import LLMService, LLMProvider
from .document_processor import DocumentProcessor, DocumentType


@dataclass
class RAGResponse:
    """Response from RAG query"""
    answer: str
    sources: List[Dict[str, Any]]
    query: str
    timestamp: str
    tokens_used: Optional[int] = None
    processing_time_ms: Optional[float] = None


@dataclass
class IngestionResult:
    """Result of document ingestion"""
    success: bool
    document_count: int
    chunk_count: int
    collection: str
    errors: List[str]
    processing_time_ms: float


class RAGService:
    """
    Main RAG orchestration service for BBC School IA Program

    Handles:
    - Document ingestion and processing
    - Semantic search
    - Answer generation with citations
    - Multi-language support
    """

    def __init__(
        self,
        persist_directory: str = "./data/chromadb",
        default_provider: LLMProvider = LLMProvider.OPENAI
    ):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService(
            persist_directory=persist_directory,
            embedding_service=self.embedding_service
        )
        self.llm_service = LLMService(default_provider=default_provider)
        self.document_processor = DocumentProcessor(
            chunk_size=512,
            chunk_overlap=50
        )

    def ingest_file(
        self,
        file_content: str,
        file_name: str,
        file_type: str = "auto",
        collection_name: Optional[str] = None
    ) -> IngestionResult:
        """
        Ingest a single file into the vector store

        Args:
            file_content: Raw file content
            file_name: Name of the file
            file_type: Type (html, md, json, auto)
            collection_name: Target collection (auto-detected if None)

        Returns:
            IngestionResult with statistics
        """
        import time
        start_time = time.time()
        errors = []

        try:
            # Process document
            if "structure" in file_name.lower() and file_type in ["json", "auto"]:
                documents = self.document_processor.process_bbc_structure(file_content)
            else:
                documents = self.document_processor.process_file(
                    file_content, file_name, file_type
                )

            if not documents:
                return IngestionResult(
                    success=False,
                    document_count=0,
                    chunk_count=0,
                    collection="",
                    errors=["No documents extracted from file"],
                    processing_time_ms=(time.time() - start_time) * 1000
                )

            # Determine collection
            if not collection_name:
                language = documents[0].metadata.get("language", "fr")
                collection_name = f"bbc_school_{language}"

            # Add to vector store
            ids = self.vector_store.add_documents(
                documents,
                collection_name,
                documents[0].metadata.get("language", "fr")
            )

            processing_time = (time.time() - start_time) * 1000

            return IngestionResult(
                success=True,
                document_count=1,
                chunk_count=len(documents),
                collection=collection_name,
                errors=[],
                processing_time_ms=processing_time
            )

        except Exception as e:
            errors.append(str(e))
            return IngestionResult(
                success=False,
                document_count=0,
                chunk_count=0,
                collection=collection_name or "",
                errors=errors,
                processing_time_ms=(time.time() - start_time) * 1000
            )

    def query(
        self,
        question: str,
        language: str = "fr",
        n_results: int = 5,
        provider: Optional[LLMProvider] = None,
        filter_level: Optional[str] = None,
        filter_module: Optional[str] = None,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> RAGResponse:
        """
        Query the RAG system

        Args:
            question: User's question
            language: Language code (fr, ar, en)
            n_results: Number of context documents to retrieve
            provider: LLM provider to use
            filter_level: Filter by education level
            filter_module: Filter by module ID
            chat_history: Previous conversation for context

        Returns:
            RAGResponse with answer and sources
        """
        import time
        start_time = time.time()

        # Build metadata filter
        metadata_filter = {}
        if filter_level:
            metadata_filter["level"] = filter_level
        if filter_module:
            metadata_filter["module"] = filter_module

        # Search vector store
        collection_name = f"bbc_school_{language}"
        search_results = self.vector_store.search(
            query=question,
            collection_name=collection_name,
            language=language,
            n_results=n_results,
            filter_metadata=metadata_filter if metadata_filter else None
        )

        # Also search all collections for comprehensive results
        if not search_results:
            search_results = self.vector_store.search_all_collections(
                query=question,
                language=language,
                n_results=n_results
            )

        # Build context from search results
        context_parts = []
        sources = []
        for i, result in enumerate(search_results):
            context_parts.append(f"[Source {i+1}] {result.content}")
            sources.append({
                "content": result.content[:200] + "..." if len(result.content) > 200 else result.content,
                "metadata": result.metadata,
                "score": result.score
            })

        context = "\n\n".join(context_parts) if context_parts else "Aucun contexte trouvé."

        # Generate response
        answer = self.llm_service.generate_response(
            query=question,
            context=context,
            provider=provider,
            chat_history=chat_history
        )

        processing_time = (time.time() - start_time) * 1000

        return RAGResponse(
            answer=answer,
            sources=sources,
            query=question,
            timestamp=datetime.now().isoformat(),
            processing_time_ms=processing_time
        )

    def search_only(
        self,
        query: str,
        language: str = "fr",
        n_results: int = 10,
        filter_type: Optional[str] = None
    ) -> List[SearchResult]:
        """
        Search without generating a response

        Useful for browsing and exploration
        """
        collection_name = f"bbc_school_{language}"

        metadata_filter = None
        if filter_type:
            metadata_filter = {"doc_type": filter_type}

        return self.vector_store.search(
            query=query,
            collection_name=collection_name,
            language=language,
            n_results=n_results,
            filter_metadata=metadata_filter
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the RAG system"""
        return {
            "collections": self.vector_store.get_all_stats(),
            "embedding_model": self.embedding_service.model_name,
            "llm_provider": self.llm_service.default_provider.value,
            "llm_model": self.llm_service.default_model
        }

    def validate_knowledge_base(self) -> Dict[str, Any]:
        """
        Validate the knowledge base with test queries

        Returns success/failure for expected answers
        """
        test_cases = [
            {
                "query": "Combien de modules dans le programme lycée?",
                "expected_contains": "8",
                "language": "fr"
            },
            {
                "query": "Durée formation enseignants Niveau 1?",
                "expected_contains": "40",
                "language": "fr"
            },
            {
                "query": "Budget total pilote?",
                "expected_contains": "12,5",
                "language": "fr"
            },
            {
                "query": "Objectifs Module L2?",
                "expected_contains": "Transformers",
                "language": "fr"
            },
            {
                "query": "Quand commence le programme?",
                "expected_contains": "2026",
                "language": "fr"
            }
        ]

        results = []
        for test in test_cases:
            try:
                response = self.query(
                    question=test["query"],
                    language=test["language"],
                    n_results=3
                )
                success = test["expected_contains"].lower() in response.answer.lower()
                results.append({
                    "query": test["query"],
                    "expected": test["expected_contains"],
                    "success": success,
                    "answer_preview": response.answer[:200]
                })
            except Exception as e:
                results.append({
                    "query": test["query"],
                    "expected": test["expected_contains"],
                    "success": False,
                    "error": str(e)
                })

        passed = sum(1 for r in results if r.get("success", False))
        return {
            "total_tests": len(test_cases),
            "passed": passed,
            "failed": len(test_cases) - passed,
            "success_rate": f"{(passed / len(test_cases)) * 100:.1f}%",
            "results": results
        }


# Singleton instance
_rag_service: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """Get or create the RAG service singleton"""
    global _rag_service
    if _rag_service is None:
        persist_dir = os.getenv("CHROMADB_PERSIST_DIR", "./data/chromadb")
        _rag_service = RAGService(persist_directory=persist_dir)
    return _rag_service
