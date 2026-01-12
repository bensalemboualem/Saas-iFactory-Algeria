"""
Reranking Strategy - Adapté d'Archon

Utilise CrossEncoder pour améliorer l'ordre des résultats de recherche.
Le reranking re-score les résultats basés sur la pertinence query-document.

Utilise le modèle cross-encoder/ms-marco-MiniLM-L-6-v2 par défaut.
"""

import os
import logging
from typing import Any, List, Dict, Optional

try:
    from sentence_transformers import CrossEncoder
    CROSSENCODER_AVAILABLE = True
except ImportError:
    CrossEncoder = None
    CROSSENCODER_AVAILABLE = False

logger = logging.getLogger(__name__)

DEFAULT_RERANKING_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class RerankingStrategy:
    """Stratégie de reranking utilisant CrossEncoder"""

    def __init__(
        self,
        model_name: str = DEFAULT_RERANKING_MODEL,
        model_instance: Any = None
    ):
        """
        Initialise la stratégie de reranking.

        Args:
            model_name: Nom/chemin du modèle CrossEncoder
            model_instance: Instance pré-chargée (optionnel)
        """
        self.model_name = model_name
        self.model = model_instance or self._load_model()

    @classmethod
    def from_model(cls, model: Any, model_name: str = "custom_model") -> "RerankingStrategy":
        """
        Crée une RerankingStrategy depuis n'importe quel modèle avec predict().

        Args:
            model: Objet avec méthode predict(pairs)
            model_name: Nom optionnel du modèle

        Returns:
            Instance RerankingStrategy
        """
        return cls(model_name=model_name, model_instance=model)

    def _load_model(self) -> Optional[CrossEncoder]:
        """Charge le modèle CrossEncoder pour le reranking."""
        if not CROSSENCODER_AVAILABLE:
            logger.warning("sentence-transformers non disponible - reranking désactivé")
            return None

        try:
            logger.info(f"Chargement du modèle de reranking: {self.model_name}")
            return CrossEncoder(self.model_name)
        except Exception as e:
            logger.error(f"Échec du chargement du modèle {self.model_name}: {e}")
            return None

    def is_available(self) -> bool:
        """Vérifie si le reranking est disponible."""
        return self.model is not None

    def build_query_document_pairs(
        self,
        query: str,
        results: List[Dict[str, Any]],
        content_key: str = "text"
    ) -> tuple[List[List[str]], List[int]]:
        """
        Construit les paires query-document pour le reranking.

        Args:
            query: La requête de recherche
            results: Liste des résultats
            content_key: Clé contenant le texte ('text' pour votre système)

        Returns:
            Tuple (paires query-doc, indices valides)
        """
        texts = []
        valid_indices = []

        for i, result in enumerate(results):
            content = result.get(content_key, "")
            if content and isinstance(content, str):
                texts.append(content)
                valid_indices.append(i)
            else:
                logger.warning(f"Résultat {i} n'a pas de contenu valide pour reranking")

        query_doc_pairs = [[query, text] for text in texts]
        return query_doc_pairs, valid_indices

    def apply_rerank_scores(
        self,
        results: List[Dict[str, Any]],
        scores: List[float],
        valid_indices: List[int],
        top_k: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Applique les scores de reranking aux résultats et les trie.

        Args:
            results: Résultats originaux
            scores: Scores de reranking
            valid_indices: Indices des résultats scorés
            top_k: Limite optionnelle de résultats

        Returns:
            Liste réordonnée et triée
        """
        # Ajouter les scores de rerank
        for i, valid_idx in enumerate(valid_indices):
            results[valid_idx]["rerank_score"] = float(scores[i])

        # Trier par rerank score (descendant - plus pertinent d'abord)
        reranked_results = sorted(
            results,
            key=lambda x: x.get("rerank_score", -1.0),
            reverse=True
        )

        # Appliquer limite top_k
        if top_k is not None and top_k > 0:
            reranked_results = reranked_results[:top_k]

        return reranked_results

    async def rerank_results(
        self,
        query: str,
        results: List[Dict[str, Any]],
        content_key: str = "text",
        top_k: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Rerank les résultats de recherche avec CrossEncoder.

        Args:
            query: Requête de recherche
            results: Résultats à reranker
            content_key: Clé contenant le texte (défaut: 'text')
            top_k: Limite optionnelle de résultats

        Returns:
            Liste réordonnée par rerank_score (plus haut d'abord)
        """
        if not self.model or not results:
            logger.debug("Reranking ignoré - pas de modèle ou pas de résultats")
            return results

        try:
            # Construire les paires query-document
            query_doc_pairs, valid_indices = self.build_query_document_pairs(
                query, results, content_key
            )

            if not query_doc_pairs:
                logger.warning("Aucun texte valide trouvé pour reranking")
                return results

            # Obtenir les scores de reranking
            scores = self.model.predict(query_doc_pairs)

            # Appliquer scores et trier
            reranked_results = self.apply_rerank_scores(
                results, scores, valid_indices, top_k
            )

            if len(scores) > 0:
                logger.info(
                    f"Reranked {len(query_doc_pairs)} résultats, "
                    f"score range: {min(scores):.3f}-{max(scores):.3f}"
                )

            return reranked_results

        except Exception as e:
            logger.error(f"Erreur durant le reranking: {e}")
            return results

    def get_model_info(self) -> Dict[str, Any]:
        """Obtient les informations sur le modèle de reranking."""
        return {
            "model_name": self.model_name,
            "available": self.is_available(),
            "crossencoder_available": CROSSENCODER_AVAILABLE,
            "model_loaded": self.model is not None,
        }


# Configuration helper
def load_reranking_config() -> Dict[str, Any]:
    """Charge la configuration de reranking depuis les variables d'env."""
    use_reranking = os.getenv("USE_RERANKING", "false").lower() in ("true", "1", "yes", "on")
    model_name = os.getenv("RERANKING_MODEL", DEFAULT_RERANKING_MODEL)
    top_k = int(os.getenv("RERANKING_TOP_K", "0")) or None

    return {
        "enabled": use_reranking,
        "model_name": model_name,
        "top_k": top_k,
    }
