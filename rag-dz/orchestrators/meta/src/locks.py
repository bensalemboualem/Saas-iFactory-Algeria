"""
Lock Manager - Gestion des verrous pour le Single-Writer Rule
"""

from datetime import datetime, timedelta

import redis.asyncio as redis
from pydantic import BaseModel


class Lock(BaseModel):
    """Modèle de verrou"""
    resource: str
    holder: str
    acquired_at: datetime
    expires_at: datetime

    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at

    @property
    def remaining_seconds(self) -> int:
        delta = self.expires_at - datetime.utcnow()
        return max(0, int(delta.total_seconds()))


class LockError(Exception):
    """Exception levée lors d'un conflit de verrou"""
    def __init__(self, resource: str, holder: str):
        self.resource = resource
        self.holder = holder
        super().__init__(f"Resource '{resource}' is locked by '{holder}'")


class LockManager:
    """Gestionnaire de verrous distribués avec Redis"""

    # Dossiers protégés nécessitant validation
    PROTECTED_PATHS = {
        "critical": [
            "migrations/",
            "auth/",
            "services/chargily/",
            "agents/gov/",
        ],
        "important": [
            "config/",
            "middleware/",
            "models/",
        ]
    }

    def __init__(self, redis_url: str, default_ttl: int = 300):
        """
        Args:
            redis_url: URL de connexion Redis
            default_ttl: TTL par défaut des locks en secondes (défaut: 5min)
        """
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.default_ttl = default_ttl

    async def acquire(
        self,
        resource: str,
        holder: str,
        ttl: int | None = None,
        force: bool = False
    ) -> Lock:
        """
        Acquiert un verrou sur une ressource.

        Args:
            resource: Chemin ou identifiant de la ressource
            holder: Identifiant du détenteur (agent)
            ttl: Time-to-live en secondes
            force: Force l'acquisition même si déjà verrouillé par un autre

        Returns:
            Lock object

        Raises:
            LockError: Si la ressource est déjà verrouillée par un autre
        """
        ttl = ttl or self.default_ttl
        key = f"lock:{resource}"

        # Vérifier si déjà verrouillé
        existing = await self.redis.get(key)
        if existing and existing != holder and not force:
            raise LockError(resource, existing)

        # Acquérir le verrou
        await self.redis.setex(key, ttl, holder)

        now = datetime.utcnow()
        return Lock(
            resource=resource,
            holder=holder,
            acquired_at=now,
            expires_at=now + timedelta(seconds=ttl)
        )

    async def release(self, resource: str, holder: str) -> bool:
        """
        Libère un verrou.

        Args:
            resource: Ressource à déverrouiller
            holder: Détenteur qui libère

        Returns:
            True si libéré avec succès, False sinon
        """
        key = f"lock:{resource}"
        existing = await self.redis.get(key)

        if existing == holder:
            await self.redis.delete(key)
            return True

        return False

    async def extend(self, resource: str, holder: str, additional_ttl: int) -> Lock | None:
        """Étend la durée d'un verrou"""
        key = f"lock:{resource}"
        existing = await self.redis.get(key)

        if existing != holder:
            return None

        ttl = await self.redis.ttl(key)
        new_ttl = ttl + additional_ttl
        await self.redis.expire(key, new_ttl)

        now = datetime.utcnow()
        return Lock(
            resource=resource,
            holder=holder,
            acquired_at=now - timedelta(seconds=(self.default_ttl - ttl)),
            expires_at=now + timedelta(seconds=new_ttl)
        )

    async def is_locked(self, resource: str) -> tuple[bool, str | None]:
        """
        Vérifie si une ressource est verrouillée.

        Returns:
            Tuple (is_locked, holder_or_none)
        """
        key = f"lock:{resource}"
        existing = await self.redis.get(key)
        return (True, existing) if existing else (False, None)

    async def get_lock_info(self, resource: str) -> Lock | None:
        """Récupère les informations d'un verrou"""
        key = f"lock:{resource}"
        existing = await self.redis.get(key)

        if not existing:
            return None

        ttl = await self.redis.ttl(key)
        now = datetime.utcnow()

        return Lock(
            resource=resource,
            holder=existing,
            acquired_at=now - timedelta(seconds=(self.default_ttl - ttl)),
            expires_at=now + timedelta(seconds=ttl)
        )

    async def list_locks(self, pattern: str = "*") -> list[Lock]:
        """Liste tous les verrous actifs"""
        keys = await self.redis.keys(f"lock:{pattern}")
        locks = []

        for key in keys:
            resource = key.replace("lock:", "")
            lock = await self.get_lock_info(resource)
            if lock:
                locks.append(lock)

        return locks

    def is_protected(self, path: str) -> tuple[bool, str | None]:
        """
        Vérifie si un chemin est protégé.

        Returns:
            Tuple (is_protected, protection_level)
        """
        for level, paths in self.PROTECTED_PATHS.items():
            for protected_path in paths:
                if path.startswith(protected_path):
                    return True, level
        return False, None

    async def close(self):
        """Ferme la connexion Redis"""
        await self.redis.close()
