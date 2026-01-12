"""
Archon Bridge - Interface pour Knowledge Base et Task Management
Source de vérité pour les données du projet
"""

import httpx
from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Document(BaseModel):
    """Document dans la Knowledge Base"""
    id: str
    content: str
    type: str  # doc, code, spec, prd, etc.
    metadata: dict = Field(default_factory=dict)
    embedding: list[float] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SearchResult(BaseModel):
    """Résultat de recherche"""
    document: Document
    score: float
    highlights: list[str] = Field(default_factory=list)


class Project(BaseModel):
    """Projet Archon"""
    id: str
    name: str
    description: str
    status: str = "active"
    created_at: datetime | None = None
    metadata: dict = Field(default_factory=dict)


class Task(BaseModel):
    """Tâche dans un projet"""
    id: str
    project_id: str
    title: str
    description: str
    status: str = "todo"  # todo, doing, done, blocked
    assignee: str | None = None
    priority: int = 0
    created_at: datetime | None = None
    updated_at: datetime | None = None
    metadata: dict = Field(default_factory=dict)


class ArchonBridge:
    """
    Bridge vers Archon pour KB et Task Management.
    Archon est la source de vérité pour toutes les données projet.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8181",
        timeout: float = 30.0
    ):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers={"Content-Type": "application/json"}
        )

    async def close(self):
        """Ferme le client HTTP"""
        await self.client.aclose()

    # ============ HEALTH ============

    async def health(self) -> dict:
        """Vérifie la santé d'Archon"""
        try:
            response = await self.client.get("/health")
            return response.json()
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # ============ KNOWLEDGE BASE ============

    async def search(
        self,
        query: str,
        filters: dict | None = None,
        limit: int = 10,
        threshold: float = 0.7
    ) -> list[SearchResult]:
        """
        Recherche sémantique dans la Knowledge Base.

        Args:
            query: Requête de recherche
            filters: Filtres optionnels (type, source, etc.)
            limit: Nombre max de résultats
            threshold: Score minimum de pertinence

        Returns:
            Liste de résultats triés par pertinence
        """
        response = await self.client.post("/api/search", json={
            "query": query,
            "filters": filters or {},
            "limit": limit,
            "threshold": threshold
        })
        response.raise_for_status()

        data = response.json()
        return [
            SearchResult(
                document=Document(**r["document"]),
                score=r["score"],
                highlights=r.get("highlights", [])
            )
            for r in data.get("results", [])
        ]

    async def ingest(
        self,
        content: str,
        doc_type: str,
        metadata: dict | None = None,
        chunk: bool = True
    ) -> Document:
        """
        Ingère un document dans la Knowledge Base.

        Args:
            content: Contenu du document
            doc_type: Type (doc, code, spec, prd, etc.)
            metadata: Métadonnées additionnelles
            chunk: Découper en chunks pour embeddings

        Returns:
            Document créé
        """
        response = await self.client.post("/api/ingest", json={
            "content": content,
            "type": doc_type,
            "metadata": metadata or {},
            "chunk": chunk
        })
        response.raise_for_status()
        return Document(**response.json())

    async def ingest_file(
        self,
        file_path: str,
        doc_type: str | None = None,
        metadata: dict | None = None
    ) -> Document:
        """
        Ingère un fichier dans la Knowledge Base.

        Args:
            file_path: Chemin du fichier
            doc_type: Type (auto-détecté si None)
            metadata: Métadonnées additionnelles

        Returns:
            Document créé
        """
        from pathlib import Path
        path = Path(file_path)

        # Auto-détection du type
        if doc_type is None:
            ext_map = {
                ".py": "code",
                ".js": "code",
                ".ts": "code",
                ".md": "doc",
                ".txt": "doc",
                ".json": "config",
                ".yaml": "config",
                ".yml": "config",
            }
            doc_type = ext_map.get(path.suffix.lower(), "doc")

        content = path.read_text(encoding="utf-8")
        meta = {"source": "file", "path": str(path), "filename": path.name}
        if metadata:
            meta.update(metadata)

        return await self.ingest(content, doc_type, meta)

    async def get_document(self, doc_id: str) -> Document | None:
        """Récupère un document par ID"""
        try:
            response = await self.client.get(f"/api/documents/{doc_id}")
            response.raise_for_status()
            return Document(**response.json())
        except httpx.HTTPStatusError:
            return None

    async def delete_document(self, doc_id: str) -> bool:
        """Supprime un document"""
        try:
            response = await self.client.delete(f"/api/documents/{doc_id}")
            return response.status_code == 200
        except Exception:
            return False

    # ============ PROJECTS ============

    async def list_projects(self, status: str | None = None) -> list[Project]:
        """Liste tous les projets"""
        params = {}
        if status:
            params["status"] = status

        response = await self.client.get("/api/projects", params=params)
        response.raise_for_status()
        return [Project(**p) for p in response.json()]

    async def create_project(
        self,
        name: str,
        description: str,
        metadata: dict | None = None
    ) -> Project:
        """Crée un nouveau projet"""
        response = await self.client.post("/api/projects", json={
            "name": name,
            "description": description,
            "metadata": metadata or {}
        })
        response.raise_for_status()
        return Project(**response.json())

    async def get_project(self, project_id: str) -> Project | None:
        """Récupère un projet par ID"""
        try:
            response = await self.client.get(f"/api/projects/{project_id}")
            response.raise_for_status()
            return Project(**response.json())
        except httpx.HTTPStatusError:
            return None

    async def update_project(
        self,
        project_id: str,
        **updates
    ) -> Project | None:
        """Met à jour un projet"""
        try:
            response = await self.client.patch(
                f"/api/projects/{project_id}",
                json=updates
            )
            response.raise_for_status()
            return Project(**response.json())
        except httpx.HTTPStatusError:
            return None

    # ============ TASKS ============

    async def list_tasks(
        self,
        project_id: str,
        status: str | None = None
    ) -> list[Task]:
        """Liste les tâches d'un projet"""
        params = {}
        if status:
            params["status"] = status

        response = await self.client.get(
            f"/api/projects/{project_id}/tasks",
            params=params
        )
        response.raise_for_status()
        return [Task(**t) for t in response.json()]

    async def create_task(
        self,
        project_id: str,
        title: str,
        description: str,
        assignee: str | None = None,
        priority: int = 0,
        metadata: dict | None = None
    ) -> Task:
        """Crée une nouvelle tâche"""
        response = await self.client.post(
            f"/api/projects/{project_id}/tasks",
            json={
                "title": title,
                "description": description,
                "status": "todo",
                "assignee": assignee,
                "priority": priority,
                "metadata": metadata or {}
            }
        )
        response.raise_for_status()
        return Task(**response.json())

    async def get_task(self, task_id: str) -> Task | None:
        """Récupère une tâche par ID"""
        try:
            response = await self.client.get(f"/api/tasks/{task_id}")
            response.raise_for_status()
            return Task(**response.json())
        except httpx.HTTPStatusError:
            return None

    async def update_task(self, task_id: str, **updates) -> Task | None:
        """Met à jour une tâche"""
        try:
            response = await self.client.patch(
                f"/api/tasks/{task_id}",
                json=updates
            )
            response.raise_for_status()
            return Task(**response.json())
        except httpx.HTTPStatusError:
            return None

    async def update_task_status(
        self,
        task_id: str,
        status: str,
        comment: str | None = None
    ) -> Task | None:
        """
        Met à jour le statut d'une tâche.
        Seul Archon peut modifier les statuts (Single-Writer).

        Args:
            task_id: ID de la tâche
            status: Nouveau statut (todo, doing, done, blocked)
            comment: Commentaire optionnel

        Returns:
            Tâche mise à jour
        """
        updates: dict[str, Any] = {"status": status}
        if comment:
            updates["status_comment"] = comment

        return await self.update_task(task_id, **updates)

    async def assign_task(
        self,
        task_id: str,
        assignee: str
    ) -> Task | None:
        """Assigne une tâche à un agent"""
        return await self.update_task(task_id, assignee=assignee)

    # ============ BATCH OPERATIONS ============

    async def bulk_ingest(
        self,
        documents: list[dict]
    ) -> list[Document]:
        """
        Ingère plusieurs documents en batch.

        Args:
            documents: Liste de {content, type, metadata}

        Returns:
            Liste de documents créés
        """
        response = await self.client.post("/api/ingest/bulk", json={
            "documents": documents
        })
        response.raise_for_status()
        return [Document(**d) for d in response.json()]

    async def sync_directory(
        self,
        directory: str,
        patterns: list[str] | None = None,
        source_name: str = "sync"
    ) -> int:
        """
        Synchronise un répertoire vers la KB.

        Args:
            directory: Chemin du répertoire
            patterns: Patterns glob (défaut: *.md, *.py, *.txt)
            source_name: Nom de la source pour les métadonnées

        Returns:
            Nombre de documents ingérés
        """
        from pathlib import Path

        patterns = patterns or ["**/*.md", "**/*.py", "**/*.txt"]
        path = Path(directory)
        count = 0

        for pattern in patterns:
            for file_path in path.glob(pattern):
                if file_path.is_file():
                    try:
                        await self.ingest_file(
                            str(file_path),
                            metadata={"source": source_name}
                        )
                        count += 1
                    except Exception:
                        pass  # Skip failed files

        return count
