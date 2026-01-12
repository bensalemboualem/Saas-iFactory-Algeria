# Archon Sync (Knowledge Orchestrator)

> **Priorité**: P0  
> **Port**: 8051 (MCP), 8181 (API), 3737 (UI)  
> **Rôle**: Source de vérité KB + Tasks  
> **Droits**: Write Tasks (externe Archon)

---

## Mission

Centraliser toute la connaissance du projet.
Gérer projets et tâches (source de vérité).
Fournir contexte RAG aux autres agents.
Synchroniser avec BMAD et Bolt.

---

## Services Archon

| Service | Port | Fonction |
|---------|------|----------|
| archon-server | 8181 | API FastAPI |
| archon-mcp | 8051 | Serveur MCP |
| archon-ui | 3737 | Interface web |
| archon-agents | 8052 | PydanticAI agents |

---

## Fonctionnalités

### Knowledge Base
- Crawl sites web (sitemap, docs)
- Upload documents (PDF, DOCX, MD)
- Extraction code examples
- Recherche sémantique (embeddings)

### Task Management
- Projets hiérarchiques
- Tasks avec workflow: `todo → doing → review → done`
- Suivi temps réel
- Intégration AI assistants

### RAG Engine
- Recherche hybride (semantic + fulltext)
- Reranking contextuel
- Génération augmentée

---

## Task States (Source de vérité)

```
    ┌──────┐
    │ todo │ ◄── Nouvelle task
    └──┬───┘
       │ assign
       ▼
    ┌──────┐
    │doing │ ◄── Agent travaille (LOCK actif)
    └──┬───┘
       │ submit
       ▼
    ┌───────┐
    │review │ ◄── validator-qa vérifie
    └──┬───┘
       │ approve/reject
       ▼
    ┌──────┐     ┌──────┐
    │ done │ ◄──►│ doing│ (si rejeté)
    └──────┘     └──────┘
```

---

## MCP Tools

```yaml
tools:
  archon_search:
    description: Recherche sémantique dans la KB
    input: { query: string, filters?: { source?, type?, date_range? } }
    output: { results[], relevance_scores[] }
  
  archon_ingest:
    description: Ajoute contenu à la KB
    input: { content: string, type: "doc"|"code"|"url", metadata?: object }
    output: { source_id: string, chunks_created: number }
  
  archon_task:
    description: Gestion des tâches
    input: { action: "create"|"update"|"list"|"get", project_id?, task?: object }
    output: { tasks[] }
  
  archon_project:
    description: Gestion des projets
    input: { action: "create"|"list"|"get", project?: object }
    output: { projects[] }
  
  archon_rag_query:
    description: Question/Réponse avec RAG
    input: { question: string, project_id?: string }
    output: { answer: string, sources[] }
```

---

## Knowledge Base IA Factory

### Sources Pré-indexées
```yaml
regulations:
  - https://www.mfdgi.gov.dz  # Fiscal
  - https://www.cnas.dz       # Social
  - https://www.cnrc.dz       # Commerce

documentation:
  - https://chargily.com/docs # Paiement
  - PCN_Algerie.pdf           # Comptabilité
  - Code_Commerce_DZ.pdf      # Juridique
```

---

## Configuration

```env
ARCHON_SERVER_PORT=8181
ARCHON_MCP_PORT=8051
ARCHON_UI_PORT=3737
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=xxx
OPENAI_API_KEY=xxx
EMBEDDING_MODEL=text-embedding-3-small
```

---

## Intégration BMAD

```python
# Index automatique des artefacts BMAD
async def index_bmad_artifacts(artifacts_path: str):
    for artifact in Path(artifacts_path).glob("**/*.md"):
        await archon.ingest(
            content=artifact.read_text(),
            type="doc",
            metadata={"source": "bmad", "type": artifact.parent.name}
        )
```

## Intégration Bolt

```python
# Sync code vers KB après commit
async def sync_bolt_code(project_id: str, files: list[File]):
    for file in files:
        await archon.ingest(
            content=file.content,
            type="code",
            metadata={"source": "bolt", "project_id": project_id}
        )
```
