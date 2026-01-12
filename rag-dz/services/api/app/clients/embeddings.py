from sentence_transformers import SentenceTransformer
import threading
import logging
from ..config import get_settings
from ..cache import embedding_cache

logger = logging.getLogger(__name__)
settings = get_settings()

MODEL_NAME = settings.embedding_model
_model = None
_lock = threading.Lock()

def get_embedding_model():
    """Récupère le modèle d'embeddings (singleton thread-safe)"""
    global _model
    if _model is None:
        with _lock:
            if _model is None:
                logger.info(f"Loading embedding model: {MODEL_NAME}")
                _model = SentenceTransformer(
                    MODEL_NAME,
                    device=settings.embedding_device
                )
                logger.info("Embedding model loaded successfully")
    return _model

def embed_queries(queries: list[str], use_cache: bool = True) -> list[list[float]]:
    """
    Génère des embeddings pour les queries avec cache Redis

    Args:
        queries: Liste des queries
        use_cache: Utiliser le cache (défaut: True)

    Returns:
        Liste des vecteurs embeddings
    """
    # Vérifier le cache si activé
    if use_cache:
        cached = embedding_cache.get_embeddings(queries)
        if cached:
            logger.debug(f"Cache hit for {len(queries)} queries")
            return cached

    # Générer les embeddings
    model = get_embedding_model()
    prefixed = [f"query: {q}" for q in queries]
    embeddings = model.encode(
        prefixed,
        normalize_embeddings=True,
        batch_size=settings.embedding_batch_size,
        show_progress_bar=False
    ).tolist()

    # Stocker dans le cache
    if use_cache:
        embedding_cache.set_embeddings(queries, embeddings)
        logger.debug(f"Cached embeddings for {len(queries)} queries")

    return embeddings

def embed_documents(texts: list[str], use_cache: bool = False) -> list[list[float]]:
    """
    Génère des embeddings pour les documents

    Args:
        texts: Liste des documents
        use_cache: Utiliser le cache (défaut: False pour documents)

    Returns:
        Liste des vecteurs embeddings
    """
    model = get_embedding_model()
    prefixed = [f"passage: {text[:2000]}" for text in texts]
    embeddings = model.encode(
        prefixed,
        normalize_embeddings=True,
        batch_size=settings.embedding_batch_size,
        show_progress_bar=len(texts) > 10
    ).tolist()

    return embeddings
