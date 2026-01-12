# Context Curator (Dependency Manager)

> **Priorité**: P1  
> **Rôle**: Qualité du contexte et conventions  
> **Droits**: Write `project-context.md`, `.conventions.json`

---

## Mission

Extraire et maintenir les conventions du projet.
Analyser les patterns du codebase existant.
Fournir un contexte cohérent à tous les agents.

---

## Outputs

| Fichier | Description |
|---------|-------------|
| `project-context.md` | Contexte complet pour les agents |
| `.conventions.json` | Conventions machine-readable |
| `PATTERNS.md` | Documentation des patterns |

---

## Extraction des Conventions

```python
class ConventionExtractor:
    async def extract(self, project_path: str) -> Conventions:
        return Conventions(
            stack=await self._detect_stack(project_path),
            naming=await self._extract_naming(project_path),
            structure=await self._extract_structure(project_path),
            patterns=await self._extract_patterns(project_path),
            dependencies=await self._list_dependencies(project_path),
        )
```

### Stack Detection
```python
STACK_INDICATORS = {
    "fastapi": ["requirements.txt:fastapi", "main.py:FastAPI"],
    "django": ["requirements.txt:django", "manage.py"],
    "nextjs": ["package.json:next", "next.config.js"],
    "react": ["package.json:react", "src/App.tsx"],
}
```

### Pattern Extraction
```python
PATTERN_INDICATORS = {
    "service-layer": "services/*.py > 2 files",
    "repository": "repositories/*.py",
    "router-pattern": "routers/*.py",
    "hooks": "hooks/*.ts",
    "components": "components/**/*.tsx",
}
```

---

## project-context.md Template

```markdown
# Project Context - IA Factory

## Stack
- Backend: FastAPI (Python 3.11)
- Frontend: Next.js 14
- Database: PostgreSQL + Supabase
- Cache: Redis
- Search: Qdrant + Meilisearch

## Structure
[Tree structure]

## Conventions
### Naming
- Files: snake_case (Python), kebab-case (TS)
- Classes: PascalCase
- Functions: snake_case (Python), camelCase (TS)
- Constants: UPPER_SNAKE

### Style
- Python: black, ruff, mypy
- TypeScript: prettier, eslint

## Patterns
[Extracted patterns with examples]

## Dependencies
[Key dependencies list]

## IA Factory Rules
- Chargily uniquement (pas Stripe)
- RLS obligatoire
- i18n: fr, ar, darija
- tenant_id via JWT uniquement
```

---

## MCP Tools

```yaml
tools:
  context_extract:
    description: Extrait les conventions du projet
    input: { project_path: string }
    output: Conventions
  
  context_generate:
    description: Génère project-context.md
    input: { project_path: string }
    output: { content: string, path: string }
  
  context_validate:
    description: Valide la cohérence du code
    input: { files[], conventions: Conventions }
    output: { valid: boolean, violations[] }
  
  context_get_patterns:
    description: Récupère patterns pour une tâche
    input: { task_type: string }
    output: { patterns[], examples[] }
```

---

## Intégration

```
1. Nouveau projet → Context Curator analyse
2. Génère project-context.md
3. Tous les agents reçoivent ce contexte
4. bolt-executor suit les conventions
5. validator-qa vérifie la cohérence
```

---

## Configuration

```env
CONTEXT_CURATOR_ENABLED=true
PROJECT_CONTEXT_PATH=project-context.md
CONVENTIONS_PATH=.conventions.json
```
