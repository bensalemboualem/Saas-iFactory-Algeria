"""
Citation Models - Source tracking and attribution
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class SourceMetadata(BaseModel):
    """Metadata about a source document"""
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    page_number: Optional[int] = None
    chunk_id: Optional[str] = None
    doc_type: Optional[str] = None  # pdf, docx, txt, web, etc.
    created_at: Optional[datetime] = None
    author: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None


class Citation(BaseModel):
    """Individual citation with source information"""
    id: int = Field(..., description="Citation number [1], [2], etc.")
    text: str = Field(..., description="Exact text from source")
    source_id: str = Field(..., description="Unique source identifier")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Relevance score 0-1")
    metadata: SourceMetadata

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "text": "RAG systems combine retrieval and generation...",
                "source_id": "doc_abc123_chunk_5",
                "confidence": 0.95,
                "metadata": {
                    "file_name": "rag_overview.pdf",
                    "page_number": 3,
                    "author": "John Doe",
                    "title": "Introduction to RAG"
                }
            }
        }


class CitedResponse(BaseModel):
    """Response with citations"""
    answer: str = Field(..., description="Generated answer with citation markers [1], [2]")
    citations: List[Citation] = Field(default_factory=list)
    total_sources: int = Field(default=0, description="Total number of sources used")

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "RAG systems combine retrieval and generation [1]. They are particularly effective for knowledge-intensive tasks [2].",
                "citations": [
                    {
                        "id": 1,
                        "text": "RAG systems combine retrieval and generation by first retrieving relevant documents...",
                        "source_id": "doc_abc123",
                        "confidence": 0.95,
                        "metadata": {"file_name": "rag_overview.pdf", "page_number": 3}
                    },
                    {
                        "id": 2,
                        "text": "Knowledge-intensive tasks benefit greatly from RAG...",
                        "source_id": "doc_xyz789",
                        "confidence": 0.89,
                        "metadata": {"file_name": "ai_applications.pdf", "page_number": 12}
                    }
                ],
                "total_sources": 2
            }
        }


class CitationService:
    """Service for managing citations in responses"""

    @staticmethod
    def format_citation_markers(text: str, citations: List[Citation]) -> str:
        """
        Add citation markers [1], [2] to text

        Args:
            text: Original text
            citations: List of citations with their IDs

        Returns:
            Text with citation markers inserted
        """
        # For now, return text as-is
        # In production, you'd use NLP to match citations to text segments
        return text

    @staticmethod
    def extract_citations_from_rag_context(
        contexts: List[Dict[str, Any]],
        min_confidence: float = 0.5
    ) -> List[Citation]:
        """
        Extract citations from RAG retrieval contexts

        Args:
            contexts: List of retrieved context dicts with metadata
            min_confidence: Minimum confidence score to include

        Returns:
            List of Citation objects
        """
        citations = []

        for idx, ctx in enumerate(contexts, start=1):
            # Skip low-confidence results
            score = ctx.get('score', ctx.get('confidence', 0.0))
            if score < min_confidence:
                continue

            # Extract metadata
            metadata_dict = ctx.get('metadata', {})
            source_metadata = SourceMetadata(
                file_name=metadata_dict.get('file_name'),
                file_path=metadata_dict.get('file_path'),
                page_number=metadata_dict.get('page_number'),
                chunk_id=metadata_dict.get('chunk_id'),
                doc_type=metadata_dict.get('doc_type'),
                author=metadata_dict.get('author'),
                title=metadata_dict.get('title'),
                url=metadata_dict.get('url')
            )

            citation = Citation(
                id=idx,
                text=ctx.get('text', ctx.get('content', '')),
                source_id=ctx.get('id', f"source_{idx}"),
                confidence=float(score),
                metadata=source_metadata
            )

            citations.append(citation)

        return citations

    @staticmethod
    def create_cited_response(
        answer: str,
        rag_contexts: List[Dict[str, Any]],
        min_confidence: float = 0.5
    ) -> CitedResponse:
        """
        Create a response with citations from RAG contexts

        Args:
            answer: Generated answer text
            rag_contexts: Retrieved contexts from RAG
            min_confidence: Minimum confidence for citations

        Returns:
            CitedResponse with answer and citations
        """
        citations = CitationService.extract_citations_from_rag_context(
            rag_contexts,
            min_confidence=min_confidence
        )

        # Add citation markers to answer (simple version)
        # In production, use smarter matching
        formatted_answer = CitationService.format_citation_markers(answer, citations)

        return CitedResponse(
            answer=formatted_answer,
            citations=citations,
            total_sources=len(citations)
        )


# Global instance
citation_service = CitationService()
