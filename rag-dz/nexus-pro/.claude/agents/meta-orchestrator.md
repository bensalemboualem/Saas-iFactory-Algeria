# Meta-Orchestrator

> **Priorité**: P0  
> **Port**: 8100  
> **Rôle**: Gouvernance globale de l'écosystème

---

## Mission

Coordination centrale de tous les orchestrateurs.
Point d'entrée unique pour toutes les requêtes.
Gestion des sessions, locks, et résolution de conflits.

---

## Responsabilités

| Fonction | Description |
|----------|-------------|
| **Routage** | Analyse et route vers BMAD/Archon/Bolt |
| **Sessions** | Maintient le contexte utilisateur cross-platform |
| **Locks** | Gère les verrous (single-writer) |
| **Conflits** | Arbitre entre agents |
| **Health** | Monitore tous les services |

---

## API Endpoints

```yaml
endpoints:
  # Health
  GET /health:
    response: { status, version }
  
  GET /status:
    response: { services: { bmad, archon, bolt }, all_healthy }
  
  # Routing
  POST /route:
    body: { request, session_id?, context? }
    response: { target, action, confidence }
  
  # Sessions
  POST /sessions:
    body: { user_id }
    response: Session
  
  GET /sessions/{id}:
    response: Session
  
  PATCH /sessions/{id}:
    body: { context?, current_project?, current_task? }
    response: Session
  
  # Locks
  POST /locks:
    body: { resource, holder, ttl? }
    response: Lock
  
  DELETE /locks/{resource}:
    query: { holder }
    response: { status }
  
  GET /locks/{resource}:
    response: { locked, holder }
  
  # Conflicts
  POST /conflicts/resolve:
    body: { conflict_type, contestants }
    response: Resolution
```

---

## Routing Logic

```python
ROUTING_PATTERNS = {
    "bmad": [
        r"\b(workflow|prd|architecture|story|sprint|backlog)\b",
        r"\b(pm|architect|developer|tester)\b",
        r"\b(plan|design|spec)\b",
    ],
    "archon": [
        r"\b(search|find|query|knowledge|kb)\b",
        r"\b(task|project|documentation)\b",
        r"\b(index|ingest|crawl)\b",
    ],
    "bolt": [
        r"\b(code|generate|implement)\b",
        r"\b(deploy|git|file)\b",
        r"\b(terminal|run|execute)\b",
    ],
}

def route(request: str) -> str:
    # Score each target
    # Return highest confidence match
    # If ambiguous → return "clarify"
```

---

## Session Schema

```python
class Session(BaseModel):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    context: dict = {}
    current_project: str | None
    current_task: str | None
    history: list[dict] = []  # Max 100 entries
```

---

## Conflict Resolution Rules

```python
PRIORITY_RULES = {
    "file_creation": ["bolt", "bmad", "archon"],
    "documentation": ["bmad", "archon", "bolt"],
    "knowledge_update": ["archon", "bolt", "bmad"],
    "task_status": ["archon"],
    "code_validation": ["bmad", "archon"],
    "security": ["security-auditor"],  # Always wins
}
```

---

## Configuration

```env
META_ORCHESTRATOR_PORT=8100
REDIS_URL=redis://localhost:6379
BMAD_URL=http://localhost:8052
ARCHON_URL=http://localhost:8181
BOLT_URL=http://localhost:5173
SESSION_TTL=3600
LOCK_DEFAULT_TTL=300
```

---

## Dependencies

- FastAPI
- Redis (sessions, locks)
- httpx (health checks)
- pydantic

---

## MCP Tools

```yaml
tools:
  nexus_route:
    description: Route request to appropriate orchestrator
    input: { request: string, context?: object }
    output: { target: string, action: string, confidence: float }
  
  nexus_status:
    description: Get ecosystem health status
    input: {}
    output: { services: object, all_healthy: boolean }
  
  nexus_session:
    description: Manage user sessions
    input: { action: "create"|"get"|"update", session_id?: string, data?: object }
    output: Session
  
  nexus_lock:
    description: Manage resource locks
    input: { action: "acquire"|"release"|"check", resource: string, holder?: string }
    output: { success: boolean, lock?: Lock }
```
