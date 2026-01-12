# Matrice de Permissions et Locks

> **Principe fondamental**: Single-Writer Rule  
> **Un seul agent peut écrire du code à la fois**

---

## 1. Droits par Agent

| Agent | Priorité | Read | Write | Lock | Veto | Scope d'écriture |
|-------|:--------:|:----:|:-----:|:----:|:----:|------------------|
| meta-orchestrator | P0 | ✅ | ❌ | ✅ | ❌ | - |
| intake-triage | P0 | ✅ | 📁 | ❌ | ❌ | `requirements/*.md` |
| archon-sync | P0 | ✅ | 🔗 | ❌ | ❌ | Tasks Archon (externe) |
| **bolt-executor** | P0 | ✅ | ✅ | ✅ | ❌ | **Code source** |
| validator-qa | P0 | ✅ | 📁 | ❌ | ✅ | `tests/` |
| bmad-runner | P1 | ✅ | 📁 | ❌ | ❌ | `PRPs/`, `docs/` |
| context-curator | P1 | ✅ | 📁 | ❌ | ❌ | `project-context.md`, `.conventions.json` |
| security-auditor | P1 | ✅ | ❌ | ❌ | ✅ | - |
| cost-model-router | P2 | ✅ | ❌ | ❌ | ❌ | - |

**Légende**: ✅ Complet | 📁 Scope limité | 🔗 Externe | ❌ Aucun

---

## 2. Dossiers Protégés

### 🔴 CRITICAL (Validation obligatoire avant modification)

| Dossier | Validateurs requis | Raison |
|---------|-------------------|--------|
| `migrations/` | security-auditor, validator-qa | Schéma DB - impact production |
| `auth/` | security-auditor | Système d'authentification |
| `services/chargily/` | security-auditor, validator-qa | Paiement - risque financier |
| `agents/gov/` | security-auditor | APIs gouvernementales sensibles |
| `middleware/tenant.py` | security-auditor | Multi-tenant isolation |

### 🟠 IMPORTANT (Review recommandé)

| Dossier | Validateurs | Raison |
|---------|-------------|--------|
| `config/` | validator-qa | Configuration système |
| `middleware/` | validator-qa | Middleware global |
| `models/` | validator-qa | Modèles de données |
| `routers/` | validator-qa | Points d'entrée API |

### 🟢 STANDARD (Lock normal)

| Dossier |
|---------|
| `services/` |
| `utils/` |
| `components/` |
| `pages/` |

---

## 3. Fichiers Immutables

**Ces fichiers ne peuvent JAMAIS être modifiés par les agents:**

```
.env
.env.production
.env.local
docker-compose.prod.yml
secrets/
*.pem
*.key
```

---

## 4. Droits par Type de Fichier

| Extension | Writers autorisés | Validators |
|-----------|-------------------|------------|
| `*.py` | bolt-executor | validator-qa, security-auditor |
| `*.ts`, `*.tsx` | bolt-executor | validator-qa |
| `*.sql` | bolt-executor | security-auditor, validator-qa |
| `*.env*` | **AUCUN** | security-auditor |
| `*.json` | bolt-executor, context-curator | validator-qa |
| `*.md` | bmad-runner, intake-triage, context-curator | - |
| `test_*.py`, `*.test.ts` | bolt-executor, validator-qa | validator-qa |

---

## 5. Workflow de Lock

### Acquisition
```python
# Avant d'écrire, bolt-executor DOIT acquérir un lock
lock = await lock_manager.acquire(
    resource="src/services/payment.py",
    holder="bolt-executor",
    ttl=300  # 5 minutes max
)
```

### Validation pré-écriture
```python
# Meta-orchestrator vérifie:
async def can_write(agent: str, file: str) -> bool:
    # 1. Agent a les droits?
    if not has_write_permission(agent, file):
        return False
    
    # 2. Fichier pas déjà locké?
    if await is_locked(file) and lock_holder != agent:
        return False
    
    # 3. Fichier protégé sans validation?
    if is_protected(file) and not has_validation(file):
        return False
    
    return True
```

### Libération
```python
# Immédiatement après la modification
await lock_manager.release(
    resource="src/services/payment.py",
    holder="bolt-executor"
)
```

---

## 6. Résolution de Conflits

### Qui gagne en cas de conflit?

| Type de conflit | Priorité | Gagnant → Perdants |
|-----------------|----------|-------------------|
| Création fichier code | P0 | bolt-executor → bmad-runner |
| Documentation | P1 | bmad-runner → bolt-executor |
| Knowledge Base | P0 | archon-sync → bolt-executor |
| Status Task | P0 | archon-sync → tous |
| Validation code | P0 | validator-qa → bolt-executor |
| Sécurité | P0 | security-auditor → **TOUS** |

### Règle de Veto

Les agents avec droit de **VETO** peuvent bloquer un merge:
- `security-auditor`: Bloque si vulnérabilité critique
- `validator-qa`: Bloque si tests échouent

---

## 7. Audit Trail

Chaque écriture est loggée:

```json
{
  "timestamp": "2025-01-15T14:32:00Z",
  "agent": "bolt-executor",
  "action": "update",
  "file": "src/services/payment.py",
  "lock_id": "lock-abc123",
  "approved_by": ["validator-qa"],
  "changes_hash": "sha256:...",
  "task_id": "task-xyz789"
}
```

---

## 8. Escalade

Si un agent a besoin d'écrire hors de son scope:

```
1. Agent → demande escalade à meta-orchestrator
2. Meta vérifie la justification
3. Si approuvé:
   - Lock temporaire accordé (TTL court)
   - Validation OBLIGATOIRE après écriture
4. Si refusé:
   - Task renvoyée à l'agent approprié
```

---

## 9. Configuration IA Factory Algérie

```yaml
iafactory_locks:
  # Fichiers spécifiques Algérie - protection maximale
  algeria_critical:
    - services/chargily/
    - agents/gov/cnas.py
    - agents/gov/sonelgaz.py
    - agents/gov/casnos.py
    - config/algeria.py
    - i18n/darija/
  
  # Double validation obligatoire
  double_validation:
    - migrations/*.sql
    - auth/
    - middleware/tenant.py
    - services/chargily/webhook.py
```

---

*Document de référence pour la gestion des droits Nexus AI Platform*
