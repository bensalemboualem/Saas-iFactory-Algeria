"""
Embedding Service for RAG
Handles text vectorization with multiple embedding models
"""

import os
from typing import List, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
import tiktoken


class EmbeddingService:
    """Service for generating text embeddings"""

    def __init__(
        self,
        model_name: str = "text-embedding-3-large",
        multilingual_model: str = "intfloat/multilingual-e5-large"
    ):
        self.model_name = model_name
        self.multilingual_model = multilingual_model

        # OpenAI embeddings for FR/EN
        self.openai_embeddings = OpenAIEmbeddings(
            model=model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        # Multilingual embeddings for AR and other languages
        self._multilingual_embeddings = None

        # Tokenizer for counting tokens
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    @property
    def multilingual_embeddings(self):
        """Lazy load multilingual embeddings"""
        if self._multilingual_embeddings is None:
            self._multilingual_embeddings = HuggingFaceEmbeddings(
                model_name=self.multilingual_model,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        return self._multilingual_embeddings

    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.tokenizer.encode(text))

    def embed_text(self, text: str, language: str = "fr") -> List[float]:
        """
        Generate embedding for a single text

        Args:
            text: Text to embed
            language: Language code (fr, en, ar, de, it)

        Returns:
            List of floats representing the embedding
        """
        if language == "ar":
            return self.multilingual_embeddings.embed_query(text)
        return self.openai_embeddings.embed_query(text)

    def embed_documents(
        self,
        documents: List[str],
        language: str = "fr"
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple documents

        Args:
            documents: List of texts to embed
            language: Language code

        Returns:
            List of embeddings
        """
        if language == "ar":
            return self.multilingual_embeddings.embed_documents(documents)
        return self.openai_embeddings.embed_documents(documents)

    def get_embedding_dimension(self, language: str = "fr") -> int:
        """Get the dimension of embeddings for a language"""
        if language == "ar":
            return 1024  # multilingual-e5-large
        return 3072  # text-embedding-3-large
