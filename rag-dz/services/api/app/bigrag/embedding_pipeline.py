"""
BIG RAG - Embedding Pipeline
=============================
Pipeline d'embeddings multi-provider
OpenAI, VoyageAI, Sentence Transformers
"""

import os
import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from enum import Enum
import httpx
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# ============================================
# ENUMS & MODELS
# ============================================

class EmbeddingProvider(str, Enum):
    """Providers d'embeddings supportés"""
    OPENAI = "openai"
    VOYAGE = "voyage"
    COHERE = "cohere"
    LOCAL = "local"  # Sentence Transformers


class EmbeddingModel(str, Enum):
    """Modèles d'embeddings"""
    # OpenAI
    OPENAI_SMALL = "text-embedding-3-small"      # 1536 dims
    OPENAI_LARGE = "text-embedding-3-large"      # 3072 dims
    OPENAI_ADA = "text-embedding-ada-002"        # 1536 dims
    
    # Voyage AI
    VOYAGE_2 = "voyage-2"                        # 1024 dims
    VOYAGE_LARGE = "voyage-large-2"              # 1536 dims
    VOYAGE_MULTILINGUAL = "voyage-multilingual-2"  # 1024 dims
    
    # Cohere
    COHERE_MULTILINGUAL = "embed-multilingual-v3.0"  # 1024 dims
    COHERE_ENGLISH = "embed-english-v3.0"            # 1024 dims
    
    # Local
    BGE_M3 = "BAAI/bge-m3"                       # 1024 dims
    MULTILINGUAL_E5 = "intfloat/multilingual-e5-large"  # 1024 dims


class EmbeddingResult(BaseModel):
    """Résultat d'embedding"""
    embeddings: List[List[float]] = Field(..., description="Vecteurs d'embeddings")
    model: str = Field(..., description="Modèle utilisé")
    dimensions: int = Field(..., description="Dimension des vecteurs")
    tokens_used: int = Field(0, description="Tokens consommés")
    provider: str = Field(..., description="Provider utilisé")


# ============================================
# ABSTRACT BASE
# ============================================

class BaseEmbedder(ABC):
    """Classe de base pour les embedders"""
    
    @abstractmethod
    async def embed(self, texts: List[str]) -> EmbeddingResult:
        """Générer les embeddings pour une liste de textes"""
        pass
    
    @abstractmethod
    def get_dimensions(self) -> int:
        """Retourne la dimension des vecteurs"""
        pass


# ============================================
# OPENAI EMBEDDER
# ============================================

class OpenAIEmbedder(BaseEmbedder):
    """Embedder OpenAI"""
    
    DIMENSIONS = {
        EmbeddingModel.OPENAI_SMALL: 1536,
        EmbeddingModel.OPENAI_LARGE: 3072,
        EmbeddingModel.OPENAI_ADA: 1536,
    }
    
    def __init__(
        self, 
        model: EmbeddingModel = EmbeddingModel.OPENAI_SMALL,
        api_key: Optional[str] = None,
    ):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1/embeddings"
        
    async def embed(self, texts: List[str]) -> EmbeddingResult:
        """Générer embeddings via OpenAI API"""
        if not texts:
            return EmbeddingResult(
                embeddings=[],
                model=self.model.value,
                dimensions=self.get_dimensions(),
                tokens_used=0,
                provider=EmbeddingProvider.OPENAI.value,
            )
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model.value,
                    "input": texts,
                    "encoding_format": "float",
                },
            )
            response.raise_for_status()
            data = response.json()
        
        embeddings = [item["embedding"] for item in data["data"]]
        tokens_used = data.get("usage", {}).get("total_tokens", 0)
        
        return EmbeddingResult(
            embeddings=embeddings,
            model=self.model.value,
            dimensions=len(embeddings[0]) if embeddings else self.get_dimensions(),
            tokens_used=tokens_used,
            provider=EmbeddingProvider.OPENAI.value,
        )
    
    def get_dimensions(self) -> int:
        return self.DIMENSIONS.get(self.model, 1536)


# ============================================
# VOYAGE AI EMBEDDER
# ============================================

class VoyageEmbedder(BaseEmbedder):
    """Embedder VoyageAI (recommandé pour multilingual)"""
    
    DIMENSIONS = {
        EmbeddingModel.VOYAGE_2: 1024,
        EmbeddingModel.VOYAGE_LARGE: 1536,
        EmbeddingModel.VOYAGE_MULTILINGUAL: 1024,
    }
    
    def __init__(
        self,
        model: EmbeddingModel = EmbeddingModel.VOYAGE_MULTILINGUAL,
        api_key: Optional[str] = None,
    ):
        self.model = model
        self.api_key = api_key or os.getenv("VOYAGE_API_KEY")
        self.base_url = "https://api.voyageai.com/v1/embeddings"
        
    async def embed(self, texts: List[str]) -> EmbeddingResult:
        """Générer embeddings via VoyageAI API"""
        if not texts:
            return EmbeddingResult(
                embeddings=[],
                model=self.model.value,
                dimensions=self.get_dimensions(),
                tokens_used=0,
                provider=EmbeddingProvider.VOYAGE.value,
            )
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model.value,
                    "input": texts,
                    "input_type": "document",
                },
            )
            response.raise_for_status()
            data = response.json()
        
        embeddings = [item["embedding"] for item in data["data"]]
        tokens_used = data.get("usage", {}).get("total_tokens", 0)
        
        return EmbeddingResult(
            embeddings=embeddings,
            model=self.model.value,
            dimensions=len(embeddings[0]) if embeddings else self.get_dimensions(),
            tokens_used=tokens_used,
            provider=EmbeddingProvider.VOYAGE.value,
        )
    
    def get_dimensions(self) -> int:
        return self.DIMENSIONS.get(self.model, 1024)


# ============================================
# COHERE EMBEDDER
# ============================================

class CohereEmbedder(BaseEmbedder):
    """Embedder Cohere"""
    
    DIMENSIONS = {
        EmbeddingModel.COHERE_MULTILINGUAL: 1024,
        EmbeddingModel.COHERE_ENGLISH: 1024,
    }
    
    def __init__(
        self,
        model: EmbeddingModel = EmbeddingModel.COHERE_MULTILINGUAL,
        api_key: Optional[str] = None,
    ):
        self.model = model
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        self.base_url = "https://api.cohere.ai/v1/embed"
        
    async def embed(self, texts: List[str]) -> EmbeddingResult:
        """Générer embeddings via Cohere API"""
        if not texts:
            return EmbeddingResult(
                embeddings=[],
                model=self.model.value,
                dimensions=self.get_dimensions(),
                tokens_used=0,
                provider=EmbeddingProvider.COHERE.value,
            )
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model.value,
                    "texts": texts,
                    "input_type": "search_document",
                    "embedding_types": ["float"],
                },
            )
            response.raise_for_status()
            data = response.json()
        
        embeddings = data.get("embeddings", {}).get("float", [])
        
        return EmbeddingResult(
            embeddings=embeddings,
            model=self.model.value,
            dimensions=len(embeddings[0]) if embeddings else self.get_dimensions(),
            tokens_used=0,
            provider=EmbeddingProvider.COHERE.value,
        )
    
    def get_dimensions(self) -> int:
        return self.DIMENSIONS.get(self.model, 1024)


# ============================================
# LOCAL EMBEDDER (Sentence Transformers)
# ============================================

class LocalEmbedder(BaseEmbedder):
    """
    Embedder local avec Sentence Transformers
    Nécessite: pip install sentence-transformers
    """
    
    DIMENSIONS = {
        EmbeddingModel.BGE_M3: 1024,
        EmbeddingModel.MULTILINGUAL_E5: 1024,
    }
    
    def __init__(
        self,
        model: EmbeddingModel = EmbeddingModel.MULTILINGUAL_E5,
    ):
        self.model = model
        self._embedder = None
        
    def _load_model(self):
        """Charger le modèle (lazy loading)"""
        if self._embedder is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._embedder = SentenceTransformer(self.model.value)
                logger.info(f"Loaded local embedding model: {self.model.value}")
            except ImportError:
                raise RuntimeError(
                    "sentence-transformers not installed. "
                    "Run: pip install sentence-transformers"
                )
        return self._embedder
    
    async def embed(self, texts: List[str]) -> EmbeddingResult:
        """Générer embeddings localement"""
        if not texts:
            return EmbeddingResult(
                embeddings=[],
                model=self.model.value,
                dimensions=self.get_dimensions(),
                tokens_used=0,
                provider=EmbeddingProvider.LOCAL.value,
            )
        
        model = self._load_model()
        embeddings = model.encode(texts, convert_to_numpy=True).tolist()
        
        return EmbeddingResult(
            embeddings=embeddings,
            model=self.model.value,
            dimensions=len(embeddings[0]) if embeddings else self.get_dimensions(),
            tokens_used=0,
            provider=EmbeddingProvider.LOCAL.value,
        )
    
    def get_dimensions(self) -> int:
        return self.DIMENSIONS.get(self.model, 1024)


# ============================================
# EMBEDDING PIPELINE
# ============================================

class EmbeddingPipeline:
    """
    Pipeline d'embeddings avec fallback automatique
    
    Ordre de priorité:
    1. OpenAI (si clé disponible)
    2. VoyageAI (si clé disponible)
    3. Cohere (si clé disponible)
    4. Local (fallback)
    """
    
    def __init__(
        self,
        primary_provider: EmbeddingProvider = EmbeddingProvider.OPENAI,
        primary_model: Optional[EmbeddingModel] = None,
        fallback_to_local: bool = True,
    ):
        self.primary_provider = primary_provider
        self.fallback_to_local = fallback_to_local
        self._embedder: Optional[BaseEmbedder] = None
        self._init_embedder(primary_provider, primary_model)
    
    def _init_embedder(
        self, 
        provider: EmbeddingProvider,
        model: Optional[EmbeddingModel] = None,
    ):
        """Initialiser l'embedder selon le provider"""
        
        if provider == EmbeddingProvider.OPENAI:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self._embedder = OpenAIEmbedder(
                    model=model or EmbeddingModel.OPENAI_SMALL,
                    api_key=api_key,
                )
                logger.info("Using OpenAI embeddings")
                return
        
        elif provider == EmbeddingProvider.VOYAGE:
            api_key = os.getenv("VOYAGE_API_KEY")
            if api_key:
                self._embedder = VoyageEmbedder(
                    model=model or EmbeddingModel.VOYAGE_MULTILINGUAL,
                    api_key=api_key,
                )
                logger.info("Using VoyageAI embeddings")
                return
        
        elif provider == EmbeddingProvider.COHERE:
            api_key = os.getenv("COHERE_API_KEY")
            if api_key:
                self._embedder = CohereEmbedder(
                    model=model or EmbeddingModel.COHERE_MULTILINGUAL,
                    api_key=api_key,
                )
                logger.info("Using Cohere embeddings")
                return
        
        # Fallback to local
        if self.fallback_to_local:
            logger.warning(f"No API key for {provider}, falling back to local embeddings")
            self._embedder = LocalEmbedder(
                model=model or EmbeddingModel.MULTILINGUAL_E5,
            )
        else:
            raise ValueError(f"No API key available for {provider}")
    
    async def embed_texts(self, texts: List[str]) -> EmbeddingResult:
        """
        Générer les embeddings pour une liste de textes
        
        Args:
            texts: Liste de textes à encoder
            
        Returns:
            EmbeddingResult avec les vecteurs
        """
        if not self._embedder:
            raise RuntimeError("No embedder configured")
        
        return await self._embedder.embed(texts)
    
    async def embed_query(self, query: str) -> List[float]:
        """
        Générer l'embedding pour une requête
        
        Args:
            query: Requête utilisateur
            
        Returns:
            Vecteur d'embedding
        """
        result = await self.embed_texts([query])
        if result.embeddings:
            return result.embeddings[0]
        return []
    
    async def embed_documents(
        self, 
        documents: List[Dict[str, Any]],
        text_key: str = "text",
    ) -> List[Dict[str, Any]]:
        """
        Ajouter les embeddings à une liste de documents
        
        Args:
            documents: Liste de documents
            text_key: Clé contenant le texte
            
        Returns:
            Documents enrichis avec embeddings
        """
        texts = [doc.get(text_key, "") for doc in documents]
        result = await self.embed_texts(texts)
        
        for doc, embedding in zip(documents, result.embeddings):
            doc["embedding"] = embedding
            doc["embedding_model"] = result.model
            doc["embedding_dims"] = result.dimensions
        
        return documents
    
    def get_dimensions(self) -> int:
        """Retourne la dimension des vecteurs"""
        if self._embedder:
            return self._embedder.get_dimensions()
        return 1536  # Default OpenAI
    
    @property
    def provider(self) -> str:
        """Retourne le provider actuel"""
        if self._embedder:
            if isinstance(self._embedder, OpenAIEmbedder):
                return EmbeddingProvider.OPENAI.value
            elif isinstance(self._embedder, VoyageEmbedder):
                return EmbeddingProvider.VOYAGE.value
            elif isinstance(self._embedder, CohereEmbedder):
                return EmbeddingProvider.COHERE.value
            elif isinstance(self._embedder, LocalEmbedder):
                return EmbeddingProvider.LOCAL.value
        return "unknown"


# ============================================
# SINGLETON
# ============================================

embedding_pipeline = EmbeddingPipeline(
    primary_provider=EmbeddingProvider.OPENAI,
    fallback_to_local=True,
)
