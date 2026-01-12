"""
Session Manager - Gestion des sessions utilisateur avec Redis
"""

import json
import uuid
from datetime import datetime
from typing import Any

import redis.asyncio as redis
from pydantic import BaseModel, Field


class Session(BaseModel):
    """Modèle de session utilisateur"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    context: dict[str, Any] = Field(default_factory=dict)
    current_project: str | None = None
    current_task: str | None = None
    current_target: str | None = None  # bmad, archon, bolt
    history: list[dict] = Field(default_factory=list)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SessionManager:
    """Gestionnaire de sessions avec stockage Redis"""

    def __init__(self, redis_url: str, ttl: int = 3600):
        """
        Args:
            redis_url: URL de connexion Redis
            ttl: Time-to-live des sessions en secondes (défaut: 1h)
        """
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.ttl = ttl

    async def create(self, user_id: str, initial_context: dict | None = None) -> Session:
        """Crée une nouvelle session"""
        session = Session(
            user_id=user_id,
            context=initial_context or {}
        )
        await self._save(session)
        return session

    async def get(self, session_id: str) -> Session | None:
        """Récupère une session par son ID"""
        data = await self.redis.get(f"session:{session_id}")
        if not data:
            return None

        parsed = json.loads(data)
        # Convertir les dates
        parsed["created_at"] = datetime.fromisoformat(parsed["created_at"])
        parsed["updated_at"] = datetime.fromisoformat(parsed["updated_at"])
        return Session(**parsed)

    async def get_by_user(self, user_id: str) -> list[Session]:
        """Récupère toutes les sessions d'un utilisateur"""
        keys = await self.redis.keys(f"session:*")
        sessions = []
        for key in keys:
            session = await self.get(key.replace("session:", ""))
            if session and session.user_id == user_id:
                sessions.append(session)
        return sessions

    async def update(self, session_id: str, **kwargs) -> Session | None:
        """Met à jour une session"""
        session = await self.get(session_id)
        if not session:
            return None

        for key, value in kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)

        session.updated_at = datetime.utcnow()
        await self._save(session)
        return session

    async def add_to_history(self, session_id: str, entry: dict) -> Session | None:
        """Ajoute une entrée à l'historique de la session"""
        session = await self.get(session_id)
        if not session:
            return None

        entry["timestamp"] = datetime.utcnow().isoformat()
        session.history.append(entry)

        # Limiter l'historique à 100 entrées
        if len(session.history) > 100:
            session.history = session.history[-100:]

        session.updated_at = datetime.utcnow()
        await self._save(session)
        return session

    async def delete(self, session_id: str) -> bool:
        """Supprime une session"""
        result = await self.redis.delete(f"session:{session_id}")
        return result > 0

    async def refresh(self, session_id: str) -> bool:
        """Renouvelle le TTL d'une session"""
        return await self.redis.expire(f"session:{session_id}", self.ttl)

    async def _save(self, session: Session):
        """Sauvegarde une session dans Redis"""
        data = session.model_dump()
        data["created_at"] = session.created_at.isoformat()
        data["updated_at"] = session.updated_at.isoformat()
        await self.redis.setex(
            f"session:{session.id}",
            self.ttl,
            json.dumps(data)
        )

    async def close(self):
        """Ferme la connexion Redis"""
        await self.redis.close()
