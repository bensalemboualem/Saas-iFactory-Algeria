# BMAD Runner (Workflow Orchestrator)

> **Priorité**: P1  
> **Port**: 8052  
> **Rôle**: Exécution des workflows BMAD Method  
> **Droits**: Write `PRPs/`, `docs/`

---

## Mission

Transformer les demandes en workflows BMAD structurés.
Coordonner les 21 agents spécialisés.
Produire les artefacts agile (PRD, Architecture, Stories).

---

## 21 Agents BMAD

| Catégorie | Agents |
|-----------|--------|
| **Product** | pm-agent, analyst-agent |
| **Design** | ux-agent, ui-agent |
| **Architecture** | architect-agent, data-architect-agent, api-architect-agent |
| **Development** | frontend-agent, backend-agent, fullstack-agent, devops-agent |
| **Quality** | test-agent, qa-agent, security-agent |
| **Documentation** | tech-writer-agent, doc-agent |
| **Management** | scrum-agent, po-agent |

---

## Workflows par Scope

| Scope | Workflow | Agents impliqués | Artefacts |
|-------|----------|-----------------|-----------|
| BUGFIX | quick-flow | developer, test | Fix + Tests |
| FEATURE | feature-flow | analyst, developer, test | Story + Code + Tests |
| REFACTOR | method-flow | architect, developer, test | Spec + Code + Tests |
| GREENFIELD | enterprise-flow | pm, architect, ux, dev, test | PRD + Arch + Stories + Code |

---

## Artefacts Produits

```yaml
artefacts:
  PRD:
    agent: pm-agent
    output: PRPs/[project]-prd.md
    template: prd-template.md
  
  Architecture:
    agent: architect-agent
    output: PRPs/[project]-architecture.md
    includes: [system-design, api-contracts, db-schema]
  
  Stories:
    agent: po-agent
    output: PRPs/[project]-stories.md
    format: Given/When/Then + Acceptance Criteria
  
  Tech Spec:
    agent: tech-writer-agent
    output: docs/[project]-spec.md
```

---

## MCP Tools

```yaml
tools:
  bmad_workflow_init:
    description: Initialise un workflow adaptatif
    input: { goal: string, complexity: string }
    output: { track: string, steps[], agents[] }
  
  bmad_run_agent:
    description: Exécute un agent spécifique
    input: { agent: string, task: string, context?: object }
    output: { result: string, artifacts[] }
  
  bmad_generate_doc:
    description: Génère un document agile
    input: { type: string, input: object }
    output: { document: string, path: string }
  
  bmad_validate:
    description: Validation par Test Architect
    input: { artifact: string, type: string }
    output: { valid: boolean, issues[] }
```

---

## Agents Custom IA Factory

```yaml
custom_agents:
  conformity-dz-agent:
    description: Vérifie conformité réglementaire Algérie
    checks: [fiscale, sociale, commerciale, RGPD-DZ]
  
  darija-content-agent:
    description: Génère/valide contenu en Darija
    capabilities: [translation, validation, tone-check]
  
  gov-integration-agent:
    description: Spécialiste intégrations CNAS/Sonelgaz/etc
    knowledge: [api-patterns, auth-flows, error-handling]
```

---

## Intégration

### → Archon
```python
# Push artefacts vers KB
async def push_to_archon(artifact: Artifact):
    await archon.ingest(
        content=artifact.content,
        type="doc",
        metadata={"source": "bmad", "type": artifact.type}
    )
```

### → Bolt
```python
# Envoie stories pour implémentation
async def send_to_bolt(stories: list[Story]):
    for story in stories:
        await archon.create_task(
            title=story.title,
            description=story.description,
            acceptance_criteria=story.criteria
        )
```

---

## Configuration

```env
BMAD_RUNNER_PORT=8052
BMAD_PATH=/app/bmad
ARCHON_API_URL=http://localhost:8181
```
