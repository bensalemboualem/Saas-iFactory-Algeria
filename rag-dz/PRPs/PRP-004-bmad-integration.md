# PRP-004: BMAD Integration

> **Priorité**: P1  
> **Effort**: 3-4 heures  
> **Dépendances**: PRP-003

---

## Objectif

Intégrer BMAD Method comme moteur de workflows agile.

---

## Tâches

### T1: BMAD Runner Setup (1h)

Créer `orchestrators/bmad/src/runner.py`:

```python
from pathlib import Path
from enum import Enum

class Workflow(str, Enum):
    QUICK = "quick-flow"
    FEATURE = "feature-flow"
    METHOD = "method-flow"
    ENTERPRISE = "enterprise-flow"

class BMADRunner:
    def __init__(self, bmad_path: str):
        self.bmad_path = Path(bmad_path)
        self.agents = self._load_agents()
    
    def _load_agents(self) -> dict:
        agents = {}
        agents_path = self.bmad_path / "src" / "agents"
        for agent_file in agents_path.glob("*.md"):
            agents[agent_file.stem] = agent_file.read_text()
        return agents
    
    def recommend_workflow(self, scope: str, complexity: str) -> Workflow:
        if scope == "BUGFIX":
            return Workflow.QUICK
        if scope == "FEATURE":
            return Workflow.FEATURE
        if scope in ["REFACTOR", "GREENFIELD"]:
            return Workflow.METHOD if complexity != "enterprise" else Workflow.ENTERPRISE
        return Workflow.FEATURE
    
    async def run_agent(self, agent_name: str, task: str, context: dict = None) -> str:
        # Load agent prompt
        agent_prompt = self.agents.get(agent_name)
        if not agent_prompt:
            raise ValueError(f"Agent {agent_name} not found")
        
        # Execute with LLM (via cost-model-router)
        # Return result
        pass
    
    async def generate_prd(self, requirements: str) -> str:
        return await self.run_agent("pm-agent", f"Generate PRD for: {requirements}")
    
    async def generate_architecture(self, prd: str) -> str:
        return await self.run_agent("architect-agent", f"Design architecture for: {prd}")
    
    async def generate_stories(self, architecture: str) -> list[str]:
        return await self.run_agent("po-agent", f"Create stories for: {architecture}")
```

**Validation**: Runner charge les agents BMAD.

---

### T2: Workflow Engine (1h)

Implémenter le moteur de workflow avec états.

```python
class WorkflowEngine:
    WORKFLOWS = {
        Workflow.QUICK: ["developer", "test"],
        Workflow.FEATURE: ["analyst", "developer", "test"],
        Workflow.METHOD: ["pm", "architect", "developer", "test"],
        Workflow.ENTERPRISE: ["pm", "architect", "ux", "developer", "test", "security"],
    }
    
    async def execute(self, workflow: Workflow, input_data: dict):
        agents = self.WORKFLOWS[workflow]
        results = {}
        
        for agent in agents:
            result = await self.runner.run_agent(agent, input_data, results)
            results[agent] = result
        
        return results
```

**Validation**: Workflows s'exécutent séquentiellement.

---

### T3: Custom Agents IA Factory (1h)

Créer agents custom:
- `conformity-dz-agent`: Conformité Algérie
- `darija-content-agent`: Contenu Darija
- `gov-integration-agent`: Intégrations GOV

**Validation**: Agents custom fonctionnels.

---

### T4: MCP Tools BMAD (30min)

Exposer les tools BMAD via MCP.

**Validation**: Tools accessibles.

---

### T5: Tests (30min)

Tests unitaires et intégration.

**Validation**: Tests passent.

---

## Critères de Complétion

- [ ] T1: Runner fonctionnel
- [ ] T2: Workflow Engine
- [ ] T3: Agents custom
- [ ] T4: MCP Tools
- [ ] T5: Tests

---

## Prochaine étape

→ **PRP-005**: Bolt Integration
