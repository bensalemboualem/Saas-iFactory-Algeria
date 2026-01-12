# PRP-003: Archon Integration

> **Priorité**: P0  
> **Effort**: 4-5 heures  
> **Dépendances**: PRP-002

---

## Objectif

Intégrer Archon comme source de vérité pour Knowledge Base et Task Management.

---

## Tâches

### T1: Setup Supabase (1h)

1. Créer projet Supabase (ou local)
2. Exécuter `archon/migration/complete_setup.sql`
3. Configurer `.env` avec credentials

**Validation**: Tables créées, connexion OK.

---

### T2: Knowledge Orchestrator Bridge (1.5h)

Créer `orchestrators/archon/src/bridge.py`:

```python
import httpx
from typing import Optional

class ArchonBridge:
    def __init__(self, base_url: str = "http://localhost:8181"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url, timeout=30.0)
    
    async def search(self, query: str, filters: dict = None) -> list:
        response = await self.client.post("/search", json={"query": query, "filters": filters})
        return response.json()
    
    async def ingest(self, content: str, type: str, metadata: dict = None) -> dict:
        response = await self.client.post("/ingest", json={
            "content": content, "type": type, "metadata": metadata or {}
        })
        return response.json()
    
    async def create_project(self, name: str, description: str) -> dict:
        response = await self.client.post("/projects", json={"name": name, "description": description})
        return response.json()
    
    async def create_task(self, project_id: str, title: str, description: str) -> dict:
        response = await self.client.post(f"/projects/{project_id}/tasks", json={
            "title": title, "description": description, "status": "todo"
        })
        return response.json()
    
    async def update_task_status(self, task_id: str, status: str) -> dict:
        response = await self.client.patch(f"/tasks/{task_id}", json={"status": status})
        return response.json()
```

**Validation**: CRUD Knowledge + Tasks fonctionnel.

---

### T3: MCP Server Extension (1h)

Étendre `archon/python/src/mcp/` avec tools supplémentaires pour Nexus.

**Validation**: MCP tools accessibles via port 8051.

---

### T4: Sync avec BMAD (1h)

Créer auto-indexation des artefacts BMAD vers Archon KB.

```python
async def sync_bmad_artifacts(bmad_path: str, archon: ArchonBridge):
    from pathlib import Path
    for artifact in Path(bmad_path).glob("**/*.md"):
        await archon.ingest(
            content=artifact.read_text(),
            type="doc",
            metadata={"source": "bmad", "path": str(artifact)}
        )
```

**Validation**: Artefacts BMAD indexés dans Archon.

---

### T5: Sync avec Bolt (30min)

Créer hook post-commit pour indexer code.

**Validation**: Code pushé vers KB après commit.

---

### T6: Tests Integration (30min)

Tests end-to-end Archon Bridge.

**Validation**: Tests passent.

---

## Critères de Complétion

- [ ] T1: Supabase configuré
- [ ] T2: Bridge fonctionnel
- [ ] T3: MCP étendu
- [ ] T4: Sync BMAD
- [ ] T5: Sync Bolt
- [ ] T6: Tests

---

## Prochaine étape

→ **PRP-004**: BMAD Integration
