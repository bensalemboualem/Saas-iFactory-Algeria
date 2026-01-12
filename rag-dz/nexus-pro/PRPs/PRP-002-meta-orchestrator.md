# PRP-002: Meta-Orchestrator Complet

> **Priorité**: P0  
> **Effort**: 4-5 heures  
> **Dépendances**: PRP-001

---

## Objectif

Implémenter le Meta-Orchestrator complet avec routage, sessions, locks et conflits.

---

## Tâches

### T1: Router Intelligent (1h)

Créer `orchestrators/meta/src/router.py`:

```python
import re
from enum import Enum
from pydantic import BaseModel

class Target(str, Enum):
    BMAD = "bmad"
    ARCHON = "archon"
    BOLT = "bolt"
    META = "meta"

class RouteResult(BaseModel):
    target: Target
    action: str
    confidence: float
    reasoning: str

PATTERNS = {
    Target.BMAD: [
        (r"\b(workflow|prd|architecture|story|sprint)\b", 0.9),
        (r"\b(plan|design|spec)\b", 0.8),
    ],
    Target.ARCHON: [
        (r"\b(search|find|query|knowledge)\b", 0.9),
        (r"\b(task|project)\b", 0.85),
    ],
    Target.BOLT: [
        (r"\b(code|generate|implement)\b", 0.9),
        (r"\b(deploy|git)\b", 0.85),
    ],
}

def route(request: str, context: dict = None) -> RouteResult:
    scores = {t: 0.0 for t in Target}
    
    for target, patterns in PATTERNS.items():
        for pattern, weight in patterns:
            if re.search(pattern, request.lower()):
                scores[target] = max(scores[target], weight)
    
    best = max(scores, key=scores.get)
    
    if scores[best] < 0.5:
        return RouteResult(target=Target.META, action="clarify", confidence=0.3, reasoning="Ambigu")
    
    return RouteResult(target=best, action="process", confidence=scores[best], reasoning=f"Match {best}")
```

**Validation**: Tests unitaires passent.

---

### T2: Session Manager (1h)

Créer `orchestrators/meta/src/sessions.py`:

```python
import redis.asyncio as redis
import json
import uuid
from datetime import datetime
from pydantic import BaseModel

class Session(BaseModel):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    context: dict = {}
    current_project: str | None = None
    current_task: str | None = None
    history: list = []

class SessionManager:
    def __init__(self, redis_url: str, ttl: int = 3600):
        self.redis = redis.from_url(redis_url)
        self.ttl = ttl
    
    async def create(self, user_id: str) -> Session:
        session = Session(
            id=str(uuid.uuid4()),
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        await self._save(session)
        return session
    
    async def get(self, session_id: str) -> Session | None:
        data = await self.redis.get(f"session:{session_id}")
        return Session(**json.loads(data)) if data else None
    
    async def update(self, session_id: str, **kwargs) -> Session | None:
        session = await self.get(session_id)
        if not session:
            return None
        for k, v in kwargs.items():
            if hasattr(session, k):
                setattr(session, k, v)
        session.updated_at = datetime.utcnow()
        await self._save(session)
        return session
    
    async def _save(self, session: Session):
        await self.redis.setex(f"session:{session.id}", self.ttl, session.model_dump_json())
```

**Validation**: CRUD fonctionne avec Redis.

---

### T3: Lock Manager (45min)

Créer `orchestrators/meta/src/locks.py`:

```python
import redis.asyncio as redis
from datetime import datetime, timedelta
from pydantic import BaseModel

class Lock(BaseModel):
    resource: str
    holder: str
    acquired_at: datetime
    expires_at: datetime

class LockError(Exception):
    pass

class LockManager:
    def __init__(self, redis_url: str, default_ttl: int = 300):
        self.redis = redis.from_url(redis_url)
        self.default_ttl = default_ttl
    
    async def acquire(self, resource: str, holder: str, ttl: int = None) -> Lock:
        ttl = ttl or self.default_ttl
        key = f"lock:{resource}"
        
        existing = await self.redis.get(key)
        if existing and existing.decode() != holder:
            raise LockError(f"Locked by {existing.decode()}")
        
        await self.redis.setex(key, ttl, holder)
        now = datetime.utcnow()
        return Lock(resource=resource, holder=holder, acquired_at=now, expires_at=now + timedelta(seconds=ttl))
    
    async def release(self, resource: str, holder: str) -> bool:
        key = f"lock:{resource}"
        existing = await self.redis.get(key)
        if existing and existing.decode() == holder:
            await self.redis.delete(key)
            return True
        return False
    
    async def is_locked(self, resource: str) -> tuple[bool, str | None]:
        key = f"lock:{resource}"
        existing = await self.redis.get(key)
        return (True, existing.decode()) if existing else (False, None)
```

**Validation**: Acquire/Release fonctionnent, conflit détecté.

---

### T4: Conflict Resolver (30min)

Créer `orchestrators/meta/src/conflicts.py`:

```python
from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class ConflictType(str, Enum):
    FILE_CREATION = "file_creation"
    DOCUMENTATION = "documentation"
    KNOWLEDGE_UPDATE = "knowledge_update"
    TASK_STATUS = "task_status"
    CODE_VALIDATION = "code_validation"

PRIORITY_RULES = {
    ConflictType.FILE_CREATION: ["bolt", "bmad", "archon"],
    ConflictType.DOCUMENTATION: ["bmad", "archon", "bolt"],
    ConflictType.KNOWLEDGE_UPDATE: ["archon", "bolt", "bmad"],
    ConflictType.TASK_STATUS: ["archon"],
    ConflictType.CODE_VALIDATION: ["bmad", "archon"],
}

class Resolution(BaseModel):
    conflict_type: ConflictType
    winner: str
    losers: list[str]
    timestamp: datetime

class ConflictResolver:
    def resolve(self, conflict_type: ConflictType, contestants: list[str]) -> Resolution:
        priority = PRIORITY_RULES.get(conflict_type, contestants)
        winner = next((c for c in priority if c in contestants), contestants[0])
        return Resolution(
            conflict_type=conflict_type,
            winner=winner,
            losers=[c for c in contestants if c != winner],
            timestamp=datetime.utcnow()
        )
```

**Validation**: Résolutions correctes selon la matrice.

---

### T5: API Endpoints (1h)

Mettre à jour `orchestrators/meta/src/main.py` avec tous les endpoints.

**Validation**: Tous les endpoints répondent correctement.

---

### T6: Tests (45min)

Créer `orchestrators/meta/tests/test_*.py` pour chaque module.

**Validation**: `pytest` passe avec coverage > 80%.

---

## Critères de Complétion

- [ ] T1: Router fonctionnel
- [ ] T2: Sessions Redis
- [ ] T3: Lock Manager
- [ ] T4: Conflict Resolver
- [ ] T5: API complète
- [ ] T6: Tests > 80%

---

## Prochaine étape

→ **PRP-003**: Archon Integration
