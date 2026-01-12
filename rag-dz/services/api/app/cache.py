"""
Redis caching layer pour embeddings et queries
"""
import json
import hashlib
import logging
from typing import Optional, List, Any
from redis import Redis
from redis.exceptions import RedisError
from .config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class RedisCache:
    """Wrapper pour Redis avec gestion d'erreurs"""

    def __init__(self):
        self.redis_client: Optional[Redis] = None
        self._connect()

    def _connect(self):
        """Connexion à Redis"""
        try:
            self.redis_client = Redis.from_url(
                settings.redis_url,
                password=settings.redis_password or None,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True
            )
            # Test de connexion
            self.redis_client.ping()
            logger.info("Redis connection established")
        except RedisError as e:
            logger.warning(f"Redis connection failed: {e}. Cache disabled.")
            self.redis_client = None

    def _generate_key(self, prefix: str, data: Any) -> str:
        """Génère une clé de cache consistante"""
        data_str = json.dumps(data, sort_keys=True)
        hash_value = hashlib.sha256(data_str.encode()).hexdigest()[:16]
        return f"{prefix}:{hash_value}"

    def get(self, key: str) -> Optional[Any]:
        """Récupère une valeur du cache"""
        if not self.redis_client:
            return None

        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except (RedisError, json.JSONDecodeError) as e:
            logger.warning(f"Cache get error for key {key}: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Stocke une valeur dans le cache"""
        if not self.redis_client:
            return False

        try:
            value_str = json.dumps(value)
            self.redis_client.setex(key, ttl, value_str)
            return True
        except (RedisError, TypeError) as e:
            logger.warning(f"Cache set error for key {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Supprime une clé du cache"""
        if not self.redis_client:
            return False

        try:
            self.redis_client.delete(key)
            return True
        except RedisError as e:
            logger.warning(f"Cache delete error for key {key}: {e}")
            return False

    def invalidate_pattern(self, pattern: str) -> int:
        """Invalide toutes les clés matchant le pattern"""
        if not self.redis_client:
            return 0

        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except RedisError as e:
            logger.warning(f"Cache invalidate error for pattern {pattern}: {e}")
            return 0

    def get_stats(self) -> dict:
        """Récupère les statistiques Redis"""
        if not self.redis_client:
            return {"status": "disconnected"}

        try:
            info = self.redis_client.info()
            return {
                "status": "connected",
                "used_memory": info.get("used_memory_human"),
                "total_keys": self.redis_client.dbsize(),
                "connected_clients": info.get("connected_clients"),
                "uptime_seconds": info.get("uptime_in_seconds")
            }
        except RedisError as e:
            logger.warning(f"Failed to get Redis stats: {e}")
            return {"status": "error", "error": str(e)}


# Instance globale
cache = RedisCache()


class EmbeddingCache:
    """Cache spécialisé pour les embeddings"""

    def __init__(self, redis_cache: RedisCache):
        self.cache = redis_cache
        self.prefix = "emb"
        self.ttl = 86400  # 24 heures

    def get_embeddings(self, queries: List[str]) -> Optional[List[List[float]]]:
        """Récupère les embeddings depuis le cache"""
        key = self.cache._generate_key(self.prefix, queries)
        return self.cache.get(key)

    def set_embeddings(self, queries: List[str], embeddings: List[List[float]]) -> bool:
        """Stocke les embeddings dans le cache"""
        key = self.cache._generate_key(self.prefix, queries)
        return self.cache.set(key, embeddings, self.ttl)

    def invalidate_all(self) -> int:
        """Invalide tous les embeddings en cache"""
        return self.cache.invalidate_pattern(f"{self.prefix}:*")


class QueryCache:
    """Cache pour les résultats de requêtes"""

    def __init__(self, redis_cache: RedisCache):
        self.cache = redis_cache
        self.prefix = "query"
        self.ttl = 300  # 5 minutes

    def get_query_result(self, query: str, collection: str, filters: dict = None) -> Optional[dict]:
        """Récupère le résultat d'une query depuis le cache"""
        cache_key = {
            "query": query,
            "collection": collection,
            "filters": filters or {}
        }
        key = self.cache._generate_key(self.prefix, cache_key)
        return self.cache.get(key)

    def set_query_result(self, query: str, collection: str, result: dict, filters: dict = None) -> bool:
        """Stocke le résultat d'une query dans le cache"""
        cache_key = {
            "query": query,
            "collection": collection,
            "filters": filters or {}
        }
        key = self.cache._generate_key(self.prefix, cache_key)
        return self.cache.set(key, result, self.ttl)

    def invalidate_collection(self, collection: str) -> int:
        """Invalide toutes les queries d'une collection"""
        return self.cache.invalidate_pattern(f"{self.prefix}:*{collection}*")


# Instances globales
embedding_cache = EmbeddingCache(cache)
query_cache = QueryCache(cache)
