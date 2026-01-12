# Bolt Executor (Code Orchestrator)

> **Priorité**: P0  
> **Port**: 8053  
> **Rôle**: **SEUL WRITER** - Génération et exécution de code  
> **Droits**: Write **CODE SOURCE**

---

## ⚠️ RÈGLE CRITIQUE

**Cet agent est le SEUL autorisé à écrire du code source.**

Tout autre agent voulant modifier du code DOIT passer par bolt-executor.

---

## Mission

Recevoir les specs BMAD et générer le code.
Exécuter dans un environnement isolé.
Déployer sur Netlify/Vercel/GitHub Pages.
Respecter le file locking system.

---

## Workflow d'Écriture

```
1. Recevoir task de archon-sync (status: doing)
2. Acquérir LOCK sur les fichiers concernés
3. Vérifier permissions (voir PERMISSIONS.md)
4. Générer/modifier le code
5. Exécuter tests locaux
6. Soumettre pour review (validator-qa)
7. Si OK → libérer LOCK → task done
8. Si KO → corriger → re-soumettre
```

---

## Providers LLM Supportés

| Provider | Modèles | Usage |
|----------|---------|-------|
| Anthropic | Claude 3.5 Sonnet | Code complexe |
| OpenAI | GPT-4o, GPT-5 | Architecture |
| DeepSeek | deepseek-coder | Code économique |
| Groq | Llama 3.1 | Tâches simples |
| Google | Gemini 2.0 | Multimodal |
| Ollama | Local models | Offline |

---

## File Locking System

```python
class FileLockManager:
    """
    OBLIGATOIRE avant toute modification.
    """
    
    async def lock(self, files: list[str]) -> list[Lock]:
        locks = []
        for file in files:
            lock = await meta.acquire_lock(
                resource=file,
                holder="bolt-executor",
                ttl=300  # 5 min max
            )
            locks.append(lock)
        return locks
    
    async def unlock(self, locks: list[Lock]):
        for lock in locks:
            await meta.release_lock(lock.resource, "bolt-executor")
```

---

## MCP Tools

```yaml
tools:
  bolt_create_project:
    description: Crée un nouveau projet
    input: { name: string, template: string, specs?: object }
    output: { project_id: string, files[] }
  
  bolt_generate:
    description: Génère du code via LLM
    input: { prompt: string, context: object, provider?: string }
    output: { code: string, files: FileChange[] }
  
  bolt_execute:
    description: Exécute une commande terminal
    input: { command: string, project_id: string }
    output: { stdout, stderr, exit_code }
  
  bolt_deploy:
    description: Déploie le projet
    input: { project_id: string, target: "netlify"|"vercel"|"github-pages" }
    output: { url: string, status: string }
  
  bolt_git:
    description: Opérations Git
    input: { action: string, project_id: string, params?: object }
    output: { success: boolean, message: string }
  
  bolt_lock_file:
    description: Verrouille un fichier
    input: { project_id: string, file_path: string, action: "lock"|"unlock" }
    output: { locked: boolean, holder?: string }
```

---

## Templates IA Factory

```yaml
templates:
  iafactory-fastapi:
    description: Backend FastAPI + Chargily + Supabase
    includes:
      - Chargily payment service
      - Supabase client avec RLS
      - JWT auth multi-tenant
      - i18n (fr, ar, darija)
  
  iafactory-nextjs:
    description: Frontend Next.js + i18n + RTL
    includes:
      - i18n setup (fr, ar, darija)
      - RTL support arabe
      - Tailwind config Algeria
      - Chargily checkout component
  
  iafactory-gov-agent:
    description: Agent browser automation GOV
    includes:
      - Playwright setup
      - Session management
      - Error recovery
      - Captcha handling patterns
```

---

## Règles de Génération

### AVANT chaque génération
```python
async def pre_generate(files: list[str]):
    # 1. Acquérir locks
    locks = await lock_manager.lock(files)
    
    # 2. Vérifier permissions
    for file in files:
        if not can_write("bolt-executor", file):
            raise PermissionError(f"Cannot write {file}")
    
    # 3. Vérifier si dossier protégé
    for file in files:
        if is_protected(file):
            await request_validation(file)
    
    return locks
```

### APRÈS chaque génération
```python
async def post_generate(locks: list[Lock], files: list[str]):
    # 1. Lint
    await run_linter(files)
    
    # 2. Type check
    await run_type_check(files)
    
    # 3. Tests unitaires
    await run_tests(files)
    
    # 4. Soumettre pour review
    await submit_for_review(files)
    
    # 5. Libérer locks (après validation)
    # await lock_manager.unlock(locks)  # Fait par validator-qa
```

---

## Configuration

```env
BOLT_EXECUTOR_PORT=8053
BOLT_PATH=/app/bolt-diy
DEFAULT_LLM_PROVIDER=anthropic
DEFAULT_MODEL=claude-3-5-sonnet
ARCHON_API_URL=http://localhost:8181
NETLIFY_TOKEN=xxx
VERCEL_TOKEN=xxx
```

---

## Sécurité

- Sandbox execution (WebContainers)
- No filesystem access outside project
- Network restrictions
- Timeout: 5 min default
- Memory limit: 512MB default
