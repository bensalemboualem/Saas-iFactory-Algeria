"""
PostgreSQL Bridge - Connexion directe à PostgreSQL local pour KB et Tasks
Alternative à Supabase pour le développement local
"""

import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Any, Optional

from pydantic import BaseModel, Field

# PostgreSQL async client
try:
    import asyncpg
    PG_AVAILABLE = True
except ImportError:
    PG_AVAILABLE = False


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


class PostgresBridge:
    """
    Bridge direct vers PostgreSQL local pour KB et Task Management.
    Alternative à Supabase pour le développement local.
    """

    def __init__(
        self,
        postgres_url: str | None = None,
        default_tenant_id: str = "00000000-0000-0000-0000-000000000000"
    ):
        self.postgres_url = postgres_url or os.getenv("POSTGRES_URL", "")
        self.default_tenant_id = default_tenant_id
        self._pool: asyncpg.Pool | None = None
        self._connected = False
        self._tables_created = False

    async def _get_pool(self) -> asyncpg.Pool:
        """Get or create connection pool"""
        if self._pool is None:
            if not PG_AVAILABLE:
                raise RuntimeError("asyncpg not installed. Run: pip install asyncpg")
            if not self.postgres_url:
                raise RuntimeError("POSTGRES_URL required")

            self._pool = await asyncpg.create_pool(self.postgres_url, min_size=2, max_size=10)
            self._connected = True

            # Créer les tables si nécessaire
            if not self._tables_created:
                await self._ensure_tables()
                self._tables_created = True

        return self._pool

    async def _ensure_tables(self):
        """Crée les tables si elles n'existent pas"""
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS nexus_tasks (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'todo',
                    assigned_to TEXT,
                    project_id UUID,
                    priority INTEGER DEFAULT 0,
                    created_by TEXT,
                    tenant_id UUID NOT NULL,
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );

                CREATE TABLE IF NOT EXISTS nexus_knowledge (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    content TEXT NOT NULL,
                    type TEXT NOT NULL,
                    source TEXT,
                    metadata JSONB DEFAULT '{}',
                    tenant_id UUID NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );

                CREATE TABLE IF NOT EXISTS nexus_projects (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'active',
                    tenant_id UUID NOT NULL,
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );

                CREATE TABLE IF NOT EXISTS nexus_locks (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    resource TEXT NOT NULL,
                    holder TEXT NOT NULL,
                    lock_type TEXT DEFAULT 'exclusive',
                    acquired_at TIMESTAMPTZ DEFAULT NOW(),
                    expires_at TIMESTAMPTZ NOT NULL,
                    metadata JSONB DEFAULT '{}',
                    UNIQUE(resource, holder)
                );

                CREATE INDEX IF NOT EXISTS idx_nexus_tasks_status ON nexus_tasks(status);
                CREATE INDEX IF NOT EXISTS idx_nexus_tasks_tenant ON nexus_tasks(tenant_id);
                CREATE INDEX IF NOT EXISTS idx_nexus_knowledge_type ON nexus_knowledge(type);
                CREATE INDEX IF NOT EXISTS idx_nexus_locks_resource ON nexus_locks(resource);
            """)

    async def close(self):
        """Cleanup"""
        if self._pool:
            await self._pool.close()
            self._pool = None
        self._connected = False

    # ============ HEALTH ============

    async def health(self) -> dict:
        """Vérifie la connexion PostgreSQL"""
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            self._connected = True
            return {
                "status": "healthy",
                "postgres": "connected",
                "tables_ready": self._tables_created
            }
        except Exception as e:
            self._connected = False
            return {
                "status": "degraded",
                "postgres": "error",
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
        """Recherche dans la Knowledge Base"""
        try:
            pool = await self._get_pool()
            tid = tenant_id or self.default_tenant_id

            async with pool.acquire() as conn:
                # Recherche textuelle simple
                sql = """
                    SELECT * FROM nexus_knowledge
                    WHERE tenant_id = $1 AND content ILIKE $2
                """
                params = [uuid.UUID(tid), f"%{query}%"]

                if filters and "type" in filters:
                    sql += " AND type = $3"
                    params.append(filters["type"])

                sql += f" LIMIT {limit}"

                rows = await conn.fetch(sql, *params)

                return [
                    SearchResult(
                        document=Document(
                            id=str(row["id"]),
                            content=row["content"],
                            type=row["type"],
                            metadata=self._parse_metadata(row.get("metadata")),
                            tenant_id=str(row.get("tenant_id", "")),
                            created_at=row.get("created_at")
                        ),
                        score=0.8,
                        highlights=[query]
                    )
                    for row in rows
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
        pool = await self._get_pool()
        tid = tenant_id or self.default_tenant_id
        doc_id = uuid.uuid4()

        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO nexus_knowledge (id, content, type, metadata, tenant_id)
                VALUES ($1, $2, $3, $4::jsonb, $5)
            """, doc_id, content, doc_type, json.dumps(metadata or {}), uuid.UUID(tid))

            return Document(
                id=str(doc_id),
                content=content,
                type=doc_type,
                metadata=metadata or {},
                tenant_id=tid
            )

    async def get_document(self, doc_id: str) -> Document | None:
        """Récupère un document par ID"""
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT * FROM nexus_knowledge WHERE id = $1",
                    uuid.UUID(doc_id)
                )
                if row:
                    return Document(
                        id=str(row["id"]),
                        content=row["content"],
                        type=row["type"],
                        metadata=self._parse_metadata(row.get("metadata")),
                        created_at=row.get("created_at")
                    )
        except Exception:
            pass
        return None

    async def delete_document(self, doc_id: str) -> bool:
        """Supprime un document"""
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                await conn.execute(
                    "DELETE FROM nexus_knowledge WHERE id = $1",
                    uuid.UUID(doc_id)
                )
            return True
        except Exception:
            return False

    # ============ PROJECTS ============

    def _parse_metadata(self, value: Any) -> dict:
        """Parse metadata from DB (might be string or dict)"""
        if value is None:
            return {}
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            try:
                return json.loads(value)
            except:
                return {}
        return {}

    async def list_projects(
        self,
        status: str | None = None,
        tenant_id: str | None = None
    ) -> list[Project]:
        """Liste les projets"""
        pool = await self._get_pool()
        tid = tenant_id or self.default_tenant_id

        async with pool.acquire() as conn:
            sql = "SELECT * FROM nexus_projects WHERE tenant_id = $1"
            params = [uuid.UUID(tid)]

            if status:
                sql += " AND status = $2"
                params.append(status)

            rows = await conn.fetch(sql, *params)

            return [
                Project(
                    id=str(row["id"]),
                    name=row["name"],
                    description=row.get("description", ""),
                    status=row.get("status", "active"),
                    tenant_id=str(row.get("tenant_id", "")),
                    created_at=row.get("created_at"),
                    metadata=self._parse_metadata(row.get("metadata"))
                )
                for row in rows
            ]

    async def create_project(
        self,
        name: str,
        description: str,
        metadata: dict | None = None,
        tenant_id: str | None = None
    ) -> Project:
        """Crée un projet"""
        pool = await self._get_pool()
        tid = tenant_id or self.default_tenant_id
        project_id = uuid.uuid4()

        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO nexus_projects (id, name, description, status, metadata, tenant_id)
                VALUES ($1, $2, $3, 'active', $4::jsonb, $5)
            """, project_id, name, description, json.dumps(metadata or {}), uuid.UUID(tid))

            return Project(
                id=str(project_id),
                name=name,
                description=description,
                status="active",
                tenant_id=tid,
                metadata=metadata or {}
            )

    async def get_project(self, project_id: str) -> Project | None:
        """Récupère un projet"""
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT * FROM nexus_projects WHERE id = $1",
                    uuid.UUID(project_id)
                )
                if row:
                    return Project(
                        id=str(row["id"]),
                        name=row["name"],
                        description=row.get("description", ""),
                        status=row.get("status", "active"),
                        created_at=row.get("created_at"),
                        metadata=self._parse_metadata(row.get("metadata"))
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
        pool = await self._get_pool()
        tid = tenant_id or self.default_tenant_id

        async with pool.acquire() as conn:
            sql = "SELECT * FROM nexus_tasks WHERE tenant_id = $1"
            params = [uuid.UUID(tid)]

            if project_id:
                sql += f" AND project_id = ${len(params) + 1}"
                params.append(uuid.UUID(project_id))
            if status:
                sql += f" AND status = ${len(params) + 1}"
                params.append(status)

            sql += " ORDER BY priority DESC"

            rows = await conn.fetch(sql, *params)

            return [
                Task(
                    id=str(row["id"]),
                    project_id=str(row.get("project_id", "")) if row.get("project_id") else None,
                    title=row["title"],
                    description=row.get("description", ""),
                    status=row.get("status", "todo"),
                    assignee=row.get("assigned_to"),
                    priority=row.get("priority", 0),
                    tenant_id=str(row.get("tenant_id", "")),
                    created_at=row.get("created_at"),
                    updated_at=row.get("updated_at"),
                    metadata=self._parse_metadata(row.get("metadata"))
                )
                for row in rows
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
        pool = await self._get_pool()
        tid = tenant_id or self.default_tenant_id
        task_id = uuid.uuid4()

        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO nexus_tasks (id, title, description, status, assigned_to, priority, metadata, tenant_id, project_id)
                VALUES ($1, $2, $3, 'todo', $4, $5, $6::jsonb, $7, $8)
            """, task_id, title, description, assignee, priority, json.dumps(metadata or {}),
                uuid.UUID(tid), uuid.UUID(project_id) if project_id else None
            )

            return Task(
                id=str(task_id),
                project_id=project_id,
                title=title,
                description=description,
                status="todo",
                assignee=assignee,
                priority=priority,
                tenant_id=tid,
                metadata=metadata or {}
            )

    async def get_task(self, task_id: str) -> Task | None:
        """Récupère une tâche"""
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT * FROM nexus_tasks WHERE id = $1",
                    uuid.UUID(task_id)
                )
                if row:
                    return Task(
                        id=str(row["id"]),
                        project_id=str(row.get("project_id", "")) if row.get("project_id") else None,
                        title=row["title"],
                        description=row.get("description", ""),
                        status=row.get("status", "todo"),
                        assignee=row.get("assigned_to"),
                        priority=row.get("priority", 0),
                        created_at=row.get("created_at"),
                        updated_at=row.get("updated_at"),
                        metadata=self._parse_metadata(row.get("metadata"))
                    )
        except Exception:
            pass
        return None

    async def update_task(self, task_id: str, **updates) -> Task | None:
        """Met à jour une tâche"""
        try:
            pool = await self._get_pool()
            if "assignee" in updates:
                updates["assigned_to"] = updates.pop("assignee")

            set_clauses = []
            params = []
            for i, (key, value) in enumerate(updates.items(), start=1):
                set_clauses.append(f"{key} = ${i}")
                params.append(value)

            params.append(uuid.UUID(task_id))

            async with pool.acquire() as conn:
                await conn.execute(
                    f"UPDATE nexus_tasks SET {', '.join(set_clauses)}, updated_at = NOW() WHERE id = ${len(params)}",
                    *params
                )
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
        """Acquiert un lock sur une ressource"""
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                # Nettoyer les locks expirés
                await conn.execute(
                    "DELETE FROM nexus_locks WHERE expires_at < NOW()"
                )

                # Vérifier si déjà locké
                existing = await conn.fetchrow(
                    "SELECT * FROM nexus_locks WHERE resource = $1",
                    resource
                )
                if existing:
                    return None

                # Créer le lock
                lock_id = uuid.uuid4()
                expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)

                await conn.execute("""
                    INSERT INTO nexus_locks (id, resource, holder, acquired_at, expires_at)
                    VALUES ($1, $2, $3, NOW(), $4)
                """, lock_id, resource, holder, expires_at)

                return Lock(
                    id=str(lock_id),
                    resource=resource,
                    holder=holder,
                    acquired_at=datetime.utcnow(),
                    expires_at=expires_at
                )
        except Exception as e:
            print(f"Acquire lock error: {e}")
        return None

    async def release_lock(self, resource: str, holder: str) -> bool:
        """Libère un lock"""
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                await conn.execute(
                    "DELETE FROM nexus_locks WHERE resource = $1 AND holder = $2",
                    resource, holder
                )
            return True
        except Exception:
            return False

    async def get_lock(self, resource: str) -> Lock | None:
        """Récupère un lock"""
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT * FROM nexus_locks WHERE resource = $1",
                    resource
                )
                if row:
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
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                rows = await conn.fetch(
                    "SELECT * FROM nexus_locks WHERE expires_at > NOW()"
                )
                return [
                    Lock(
                        id=str(row["id"]),
                        resource=row["resource"],
                        holder=row["holder"],
                        acquired_at=row["acquired_at"],
                        expires_at=row["expires_at"]
                    )
                    for row in rows
                ]
        except Exception:
            return []
