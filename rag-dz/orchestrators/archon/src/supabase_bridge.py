"""
Supabase Bridge - Connexion directe à Supabase pour KB et Tasks
Remplace le bridge Archon externe par une connexion directe
"""

import os
import uuid
from datetime import datetime, timedelta
from typing import Any, Optional

from pydantic import BaseModel, Field

# Supabase client
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = Any


class Document(BaseModel):
    """Document dans la Knowledge Base"""
    id: str
    content: str
    type: str
    metadata: dict = Field(default_factory=dict)
    tenant_id: str | None = None
    created_at: datetime | None = None


class SearchResult(BaseModel):
    """Résultat de recherche"""
    document: Document
    score: float
    highlights: list[str] = Field(default_factory=list)


class Project(BaseModel):
    """Projet Nexus"""
    id: str
    name: str
    description: str
    status: str = "active"
    tenant_id: str | None = None
    created_at: datetime | None = None
    metadata: dict = Field(default_factory=dict)


class Task(BaseModel):
    """Tâche dans un projet"""
    id: str
    project_id: str | None = None
    title: str
    description: str
    status: str = "todo"
    assignee: str | None = None
    priority: int = 0
    tenant_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    metadata: dict = Field(default_factory=dict)


class Lock(BaseModel):
    """Lock pour Single-Writer Rule"""
    id: str
    resource: str
    holder: str
    acquired_at: datetime
    expires_at: datetime


class SupabaseBridge:
    """
    Bridge direct vers Supabase pour KB et Task Management.
    Pas besoin d'Archon externe - connexion directe à la DB.
    """

    def __init__(
        self,
        supabase_url: str | None = None,
        supabase_key: str | None = None,
        default_tenant_id: str = "00000000-0000-0000-0000-000000000000"
    ):
        self.supabase_url = supabase_url or os.getenv("SUPABASE_URL", "")
        self.supabase_key = supabase_key or os.getenv("SUPABASE_SERVICE_KEY", "")
        self.default_tenant_id = default_tenant_id
        self._client: Client | None = None
        self._connected = False

    @property
    def client(self) -> Client:
        """Lazy client initialization"""
        if self._client is None:
            if not SUPABASE_AVAILABLE:
                raise RuntimeError("supabase-py not installed. Run: pip install supabase")
            if not self.supabase_url or not self.supabase_key:
                raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_KEY required")

            self._client = create_client(self.supabase_url, self.supabase_key)
            self._connected = True
        return self._client

    async def close(self):
        """Cleanup"""
        self._client = None
        self._connected = False

    def _set_tenant(self, tenant_id: str | None = None):
        """Configure le tenant_id pour RLS"""
        tid = tenant_id or self.default_tenant_id
        # Note: En production, utiliser RLS avec JWT
        # Pour l'instant on utilise le service key qui bypass RLS

    # ============ HEALTH ============

    async def health(self) -> dict:
        """Vérifie la connexion Supabase"""
        try:
            # Test simple query
            result = self.client.table("nexus_projects").select("id").limit(1).execute()
            self._connected = True
            return {
                "status": "healthy",
                "supabase": "connected",
                "url": self.supabase_url[:30] + "..." if len(self.supabase_url) > 30 else self.supabase_url
            }
        except Exception as e:
            self._connected = False
            return {
                "status": "degraded",
                "supabase": "error",
                "error": str(e)
            }

    # ============ KNOWLEDGE BASE ============

    async def search(
        self,
        query: str,
        filters: dict | None = None,
        limit: int = 10,
        tenant_id: str | None = None
    ) -> list[SearchResult]:
        """
        Recherche dans la Knowledge Base.
        Note: Pour la recherche sémantique, utiliser pgvector + embeddings.
        """
        try:
            self._set_tenant(tenant_id)

            # Construction de la requête
            q = self.client.table("nexus_knowledge").select("*")

            # Filtre par tenant
            tid = tenant_id or self.default_tenant_id
            q = q.eq("tenant_id", tid)

            # Filtres additionnels
            if filters:
                if "type" in filters:
                    q = q.eq("type", filters["type"])
                if "source" in filters:
                    q = q.ilike("source", f"%{filters['source']}%")

            # Recherche textuelle (simple ILIKE pour l'instant)
            q = q.ilike("content", f"%{query}%")
            q = q.limit(limit)

            result = q.execute()

            return [
                SearchResult(
                    document=Document(
                        id=str(row["id"]),
                        content=row["content"],
                        type=row["type"],
                        metadata=row.get("metadata", {}),
                        tenant_id=str(row.get("tenant_id", "")),
                        created_at=row.get("created_at")
                    ),
                    score=0.8,  # Score fixe sans embeddings
                    highlights=[query]
                )
                for row in result.data
            ]
        except Exception as e:
            print(f"Search error: {e}")
            return []

    async def ingest(
        self,
        content: str,
        doc_type: str,
        metadata: dict | None = None,
        tenant_id: str | None = None
    ) -> Document:
        """Ingère un document dans la KB"""
        tid = tenant_id or self.default_tenant_id

        doc_data = {
            "id": str(uuid.uuid4()),
            "content": content,
            "type": doc_type,
            "metadata": metadata or {},
            "tenant_id": tid
        }

        result = self.client.table("nexus_knowledge").insert(doc_data).execute()

        if result.data:
            row = result.data[0]
            return Document(
                id=str(row["id"]),
                content=row["content"],
                type=row["type"],
                metadata=row.get("metadata", {}),
                tenant_id=str(row.get("tenant_id", "")),
                created_at=row.get("created_at")
            )
        raise RuntimeError("Failed to ingest document")

    async def get_document(self, doc_id: str) -> Document | None:
        """Récupère un document par ID"""
        try:
            result = self.client.table("nexus_knowledge").select("*").eq("id", doc_id).single().execute()
            if result.data:
                row = result.data
                return Document(
                    id=str(row["id"]),
                    content=row["content"],
                    type=row["type"],
                    metadata=row.get("metadata", {}),
                    created_at=row.get("created_at")
                )
        except Exception:
            pass
        return None

    async def delete_document(self, doc_id: str) -> bool:
        """Supprime un document"""
        try:
            self.client.table("nexus_knowledge").delete().eq("id", doc_id).execute()
            return True
        except Exception:
            return False

    # ============ PROJECTS ============

    async def list_projects(
        self,
        status: str | None = None,
        tenant_id: str | None = None
    ) -> list[Project]:
        """Liste les projets"""
        tid = tenant_id or self.default_tenant_id

        q = self.client.table("nexus_projects").select("*").eq("tenant_id", tid)
        if status:
            q = q.eq("status", status)

        result = q.execute()

        return [
            Project(
                id=str(row["id"]),
                name=row["name"],
                description=row.get("description", ""),
                status=row.get("status", "active"),
                tenant_id=str(row.get("tenant_id", "")),
                created_at=row.get("created_at"),
                metadata=row.get("metadata", {})
            )
            for row in result.data
        ]

    async def create_project(
        self,
        name: str,
        description: str,
        metadata: dict | None = None,
        tenant_id: str | None = None
    ) -> Project:
        """Crée un projet"""
        tid = tenant_id or self.default_tenant_id

        project_data = {
            "id": str(uuid.uuid4()),
            "name": name,
            "description": description,
            "status": "active",
            "metadata": metadata or {},
            "tenant_id": tid
        }

        result = self.client.table("nexus_projects").insert(project_data).execute()

        if result.data:
            row = result.data[0]
            return Project(
                id=str(row["id"]),
                name=row["name"],
                description=row.get("description", ""),
                status=row.get("status", "active"),
                tenant_id=str(row.get("tenant_id", "")),
                created_at=row.get("created_at"),
                metadata=row.get("metadata", {})
            )
        raise RuntimeError("Failed to create project")

    async def get_project(self, project_id: str) -> Project | None:
        """Récupère un projet"""
        try:
            result = self.client.table("nexus_projects").select("*").eq("id", project_id).single().execute()
            if result.data:
                row = result.data
                return Project(
                    id=str(row["id"]),
                    name=row["name"],
                    description=row.get("description", ""),
                    status=row.get("status", "active"),
                    created_at=row.get("created_at"),
                    metadata=row.get("metadata", {})
                )
        except Exception:
            pass
        return None

    # ============ TASKS ============

    async def list_tasks(
        self,
        project_id: str | None = None,
        status: str | None = None,
        tenant_id: str | None = None
    ) -> list[Task]:
        """Liste les tâches"""
        tid = tenant_id or self.default_tenant_id

        q = self.client.table("nexus_tasks").select("*").eq("tenant_id", tid)
        if project_id:
            q = q.eq("project_id", project_id)
        if status:
            q = q.eq("status", status)

        result = q.order("priority", desc=True).execute()

        return [
            Task(
                id=str(row["id"]),
                project_id=str(row.get("project_id", "")),
                title=row["title"],
                description=row.get("description", ""),
                status=row.get("status", "todo"),
                assignee=row.get("assigned_to"),
                priority=row.get("priority", 0),
                tenant_id=str(row.get("tenant_id", "")),
                created_at=row.get("created_at"),
                updated_at=row.get("updated_at"),
                metadata=row.get("metadata", {})
            )
            for row in result.data
        ]

    async def create_task(
        self,
        title: str,
        description: str,
        project_id: str | None = None,
        assignee: str | None = None,
        priority: int = 0,
        metadata: dict | None = None,
        tenant_id: str | None = None
    ) -> Task:
        """Crée une tâche"""
        tid = tenant_id or self.default_tenant_id

        task_data = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "status": "todo",
            "assigned_to": assignee,
            "priority": priority,
            "metadata": metadata or {},
            "tenant_id": tid
        }
        if project_id:
            task_data["project_id"] = project_id

        result = self.client.table("nexus_tasks").insert(task_data).execute()

        if result.data:
            row = result.data[0]
            return Task(
                id=str(row["id"]),
                project_id=str(row.get("project_id", "")),
                title=row["title"],
                description=row.get("description", ""),
                status=row.get("status", "todo"),
                assignee=row.get("assigned_to"),
                priority=row.get("priority", 0),
                tenant_id=str(row.get("tenant_id", "")),
                created_at=row.get("created_at"),
                metadata=row.get("metadata", {})
            )
        raise RuntimeError("Failed to create task")

    async def get_task(self, task_id: str) -> Task | None:
        """Récupère une tâche"""
        try:
            result = self.client.table("nexus_tasks").select("*").eq("id", task_id).single().execute()
            if result.data:
                row = result.data
                return Task(
                    id=str(row["id"]),
                    project_id=str(row.get("project_id", "")),
                    title=row["title"],
                    description=row.get("description", ""),
                    status=row.get("status", "todo"),
                    assignee=row.get("assigned_to"),
                    priority=row.get("priority", 0),
                    created_at=row.get("created_at"),
                    updated_at=row.get("updated_at"),
                    metadata=row.get("metadata", {})
                )
        except Exception:
            pass
        return None

    async def update_task(self, task_id: str, **updates) -> Task | None:
        """Met à jour une tâche"""
        try:
            # Map field names
            if "assignee" in updates:
                updates["assigned_to"] = updates.pop("assignee")

            result = self.client.table("nexus_tasks").update(updates).eq("id", task_id).execute()
            if result.data:
                return await self.get_task(task_id)
        except Exception as e:
            print(f"Update task error: {e}")
        return None

    # ============ LOCKS ============

    async def acquire_lock(
        self,
        resource: str,
        holder: str,
        ttl_seconds: int = 300
    ) -> Lock | None:
        """
        Acquiert un lock sur une ressource.

        Args:
            resource: Chemin du fichier ou ressource
            holder: ID de l'agent qui acquiert le lock
            ttl_seconds: Durée de vie du lock

        Returns:
            Lock acquis ou None si déjà locké
        """
        try:
            # Nettoyer les locks expirés
            self.client.table("nexus_locks").delete().lt("expires_at", datetime.utcnow().isoformat()).execute()

            # Vérifier si déjà locké
            existing = self.client.table("nexus_locks").select("*").eq("resource", resource).execute()
            if existing.data:
                return None  # Déjà locké

            # Créer le lock
            lock_data = {
                "id": str(uuid.uuid4()),
                "resource": resource,
                "holder": holder,
                "acquired_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(seconds=ttl_seconds)).isoformat()
            }

            result = self.client.table("nexus_locks").insert(lock_data).execute()

            if result.data:
                row = result.data[0]
                return Lock(
                    id=str(row["id"]),
                    resource=row["resource"],
                    holder=row["holder"],
                    acquired_at=row["acquired_at"],
                    expires_at=row["expires_at"]
                )
        except Exception as e:
            print(f"Acquire lock error: {e}")
        return None

    async def release_lock(self, resource: str, holder: str) -> bool:
        """Libère un lock"""
        try:
            self.client.table("nexus_locks").delete().eq("resource", resource).eq("holder", holder).execute()
            return True
        except Exception:
            return False

    async def get_lock(self, resource: str) -> Lock | None:
        """Récupère un lock"""
        try:
            result = self.client.table("nexus_locks").select("*").eq("resource", resource).single().execute()
            if result.data:
                row = result.data
                return Lock(
                    id=str(row["id"]),
                    resource=row["resource"],
                    holder=row["holder"],
                    acquired_at=row["acquired_at"],
                    expires_at=row["expires_at"]
                )
        except Exception:
            pass
        return None

    async def list_locks(self) -> list[Lock]:
        """Liste tous les locks actifs"""
        try:
            result = self.client.table("nexus_locks").select("*").gt("expires_at", datetime.utcnow().isoformat()).execute()
            return [
                Lock(
                    id=str(row["id"]),
                    resource=row["resource"],
                    holder=row["holder"],
                    acquired_at=row["acquired_at"],
                    expires_at=row["expires_at"]
                )
                for row in result.data
            ]
        except Exception:
            return []
