# PRP-005: Bolt Integration

> **Priorité**: P0  
> **Effort**: 3-4 heures  
> **Dépendances**: PRP-004

---

## Objectif

Intégrer bolt.diy comme moteur de génération de code avec file locking.

---

## Tâches

### T1: Bolt Bridge Setup (1h)

Créer `orchestrators/bolt/src/bridge.py`:

```python
import httpx
from pathlib import Path

class BoltBridge:
    def __init__(self, base_url: str = "http://localhost:5173"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url, timeout=60.0)
    
    async def create_project(self, name: str, template: str) -> dict:
        response = await self.client.post("/api/projects", json={
            "name": name, "template": template
        })
        return response.json()
    
    async def generate_code(self, prompt: str, context: dict, provider: str = "anthropic") -> dict:
        response = await self.client.post("/api/generate", json={
            "prompt": prompt,
            "context": context,
            "provider": provider
        })
        return response.json()
    
    async def execute_command(self, project_id: str, command: str) -> dict:
        response = await self.client.post(f"/api/projects/{project_id}/execute", json={
            "command": command
        })
        return response.json()
    
    async def deploy(self, project_id: str, target: str) -> dict:
        response = await self.client.post(f"/api/projects/{project_id}/deploy", json={
            "target": target
        })
        return response.json()
```

**Validation**: Bridge communique avec Bolt.

---

### T2: File Lock Integration (1h)

Intégrer le système de lock de Bolt avec Meta-Orchestrator.

```python
class BoltExecutor:
    def __init__(self, bolt: BoltBridge, lock_manager: LockManager):
        self.bolt = bolt
        self.locks = lock_manager
    
    async def execute_task(self, task: Task) -> dict:
        # 1. Acquire locks
        locks = []
        for file in task.affected_files:
            lock = await self.locks.acquire(file, "bolt-executor")
            locks.append(lock)
        
        try:
            # 2. Generate code
            result = await self.bolt.generate_code(
                prompt=task.description,
                context={"specs": task.specs, "files": task.affected_files}
            )
            
            # 3. Run tests
            test_result = await self.bolt.execute_command(
                task.project_id, 
                "npm test" if task.is_frontend else "pytest"
            )
            
            return {"code": result, "tests": test_result}
        
        finally:
            # 4. Release locks (ou attendre validation)
            pass  # Locks released by validator-qa
```

**Validation**: Locks acquis avant écriture, libérés après.

---

### T3: Templates IA Factory (1h)

Créer templates personnalisés:
- `iafactory-fastapi`: Backend avec Chargily
- `iafactory-nextjs`: Frontend avec i18n
- `iafactory-gov-agent`: Agent browser

**Validation**: Templates génèrent du code valide.

---

### T4: MCP Tools Bolt (30min)

Exposer tools Bolt via MCP.

**Validation**: Tools accessibles.

---

### T5: Tests (30min)

Tests d'intégration.

**Validation**: Tests passent.

---

## Critères de Complétion

- [ ] T1: Bridge fonctionnel
- [ ] T2: Lock Integration
- [ ] T3: Templates custom
- [ ] T4: MCP Tools
- [ ] T5: Tests

---

## Prochaine étape

→ **PRP-006**: IA Factory Adaptation
