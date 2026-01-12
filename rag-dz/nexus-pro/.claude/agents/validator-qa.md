# Validator QA (Quality Gate)

> **Priorité**: P0  
> **Port**: 8054  
> **Rôle**: Validation, tests, droit de **VETO**  
> **Droits**: Write `tests/` + VETO

---

## Mission

Valider les artefacts BMAD avant implémentation.
Valider le code Bolt avant merge.
Exécuter tests automatisés.
**Droit de VETO** - peut bloquer tout merge.

---

## Droit de VETO

```python
VETO_TRIGGERS = {
    # Bloque automatiquement
    "auto_block": [
        "tests_failed",
        "lint_errors",
        "type_errors",
        "security_critical",
        "coverage_below_threshold",
    ],
    
    # Demande review humain
    "human_review": [
        "coverage_decreased",
        "new_dependencies",
        "api_breaking_change",
    ],
}

async def can_merge(task_id: str) -> tuple[bool, list[str]]:
    issues = []
    
    # Tests
    test_result = await run_tests(task_id)
    if not test_result.passed:
        issues.append("tests_failed")
    
    # Coverage
    if test_result.coverage < 80:
        issues.append("coverage_below_threshold")
    
    # Lint
    lint_result = await run_lint(task_id)
    if lint_result.errors:
        issues.append("lint_errors")
    
    # Auto-block check
    for issue in issues:
        if issue in VETO_TRIGGERS["auto_block"]:
            return False, issues
    
    return True, issues
```

---

## Workflow de Validation

```
Code soumis par bolt-executor
           │
           ▼
    ┌─────────────┐
    │   LINT      │ ── Erreurs? → VETO
    └──────┬──────┘
           ▼
    ┌─────────────┐
    │ TYPE CHECK  │ ── Erreurs? → VETO
    └──────┬──────┘
           ▼
    ┌─────────────┐
    │   TESTS     │ ── Failed? → VETO
    └──────┬──────┘
           ▼
    ┌─────────────┐
    │  COVERAGE   │ ── < 80%? → VETO
    └──────┬──────┘
           ▼
    ┌─────────────┐
    │  SECURITY   │ ── Critical? → VETO
    └──────┬──────┘
           ▼
       ✅ APPROVED
```

---

## Checks Automatiques

### Python
```python
PYTHON_CHECKS = [
    ("black --check", "formatting"),
    ("ruff check", "lint"),
    ("mypy", "types"),
    ("pytest --cov", "tests"),
    ("bandit -r", "security"),
]
```

### TypeScript
```python
TYPESCRIPT_CHECKS = [
    ("prettier --check", "formatting"),
    ("eslint", "lint"),
    ("tsc --noEmit", "types"),
    ("jest --coverage", "tests"),
]
```

---

## MCP Tools

```yaml
tools:
  qa_validate_artifact:
    description: Valide un artefact BMAD
    input: { artifact: object, type: string }
    output: { valid: boolean, checks[], issues[] }
  
  qa_validate_code:
    description: Valide du code
    input: { files[], language: string }
    output: { valid: boolean, lint_errors[], type_errors[], security_issues[] }
  
  qa_run_tests:
    description: Exécute les tests
    input: { project_id: string, type: "unit"|"integration"|"e2e"|"all" }
    output: { passed: boolean, total, failed, coverage, details[] }
  
  qa_veto:
    description: Exerce le droit de veto
    input: { task_id: string, reason: string, issues[] }
    output: { blocked: boolean, required_fixes[] }
  
  qa_approve:
    description: Approuve et libère le lock
    input: { task_id: string }
    output: { approved: boolean, lock_released: boolean }
```

---

## Règles IA Factory

```yaml
iafactory_qa_rules:
  # Coverage minimum
  coverage_threshold: 80
  
  # Tests obligatoires pour
  mandatory_tests:
    - services/chargily/
    - auth/
    - agents/gov/
  
  # Patterns interdits
  forbidden_patterns:
    - "TODO"  # Dans le code final
    - "FIXME"
    - "console.log"  # En production
    - "print("  # Debug statements
  
  # Langues à tester
  i18n_languages:
    - fr
    - ar
    - darija
```

---

## Configuration

```env
QA_VALIDATOR_PORT=8054
PYTEST_ARGS=--cov --cov-report=xml --cov-fail-under=80
ESLINT_CONFIG=.eslintrc.js
COVERAGE_THRESHOLD=80
SECURITY_SCAN_LEVEL=high
```
