# Écosystème MCP: BMAD ↔ Archon ↔ Claude Code

## Architecture Globale

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLAUDE CODE / IDE                            │
│                    (Cursor, Windsurf, VS Code)                      │
└────────────────────────────┬────────────────────────────────────────┘
                             │ MCP Protocol (SSE/HTTP)
                             ↓
┌─────────────────────────────────────────────────────────────────────┐
│                   ARCHON MCP SERVER (Port 8051)                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ MCP Tools Disponibles:                                         │  │
│  │  • bmad_list_agents()                                         │  │
│  │  • bmad_list_workflows(agent?)                                │  │
│  │  • bmad_execute_workflow(workflow, agent, context)            │  │
│  │  • bmad_get_workflow_status(execution_id)                     │  │
│  │  • bmad_cancel_workflow(execution_id)                         │  │
│  │  • bmad_get_active_workflows()                                │  │
│  │                                                                 │  │
│  │  + Outils Archon existants:                                   │  │
│  │    - rag_search_knowledge_base()                              │  │
│  │    - manage_project(), manage_task(), manage_document()       │  │
│  └───────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │ HTTP Calls
                             ↓
┌─────────────────────────────────────────────────────────────────────┐
│              BACKEND API RAG.DZ (Port 8180)                         │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ BMAD Router (/api/bmad/*)                                     │  │
│  │  • GET  /agents          → Liste des agents BMAD              │  │
│  │  • GET  /workflows       → Liste des workflows                │  │
│  │  • POST /workflows/execute → Lance un workflow                │  │
│  │  • GET  /workflows/{id}  → Status d'exécution                 │  │
│  │  • GET  /workflows/active → Workflows actifs                  │  │
│  └───────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │ Node.js Subprocess
                             ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    BMAD-METHOD (./bmad/)                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ 8 Agents Spécialisés:                                         │  │
│  │  🏗️  BMM Architect    → Architecture système                  │  │
│  │  💻 BMM Coder        → Implémentation code                    │  │
│  │  🧪 BMM Tester       → Tests et QA                            │  │
│  │  🐛 BMM Debugger     → Debug et résolution                    │  │
│  │  📝 BMM Documenter   → Documentation technique                │  │
│  │  🔨 BMB Builder      → Création agents custom                 │  │
│  │  💡 CIS Ideator      → Idéation créative                      │  │
│  │  🎯 CIS Strategist   → Planification stratégique              │  │
│  │                                                                 │  │
│  │ 9 Workflows Principaux:                                       │  │
│  │  🚀 workflow-init    → Initialisation projet                  │  │
│  │  📋 prd              → Product Requirements Document          │  │
│  │  🏗️  architecture     → Design architecture                    │  │
│  │  💻 dev-story        → Développement story                    │  │
│  │  🔍 code-review      → Revue de code                          │  │
│  │  🔧 bug-fix          → Correction de bugs                     │  │
│  │  ✅ test-generation  → Génération de tests                    │  │
│  │  📚 doc-generation   → Génération docs                        │  │
│  │  🌟 brainstorm       → Session de brainstorming               │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Flux de Données

### 1. Exécution d'un Workflow BMAD depuis Claude Code

```
1. Claude Code → MCP Request
   bmad_execute_workflow(
     workflow_name="workflow-init",
     agent_id="bmm-architect",
     context_data='{"project_type": "web_app"}'
   )

2. Archon MCP Server → Backend API
   POST http://localhost:8180/api/bmad/workflows/execute
   {
     "name": "workflow-init",
     "agent": "bmm-architect",
     "context": {"project_type": "web_app"}
   }

3. Backend → BMAD-METHOD
   subprocess.run([
     "npx", "bmad-method",
     "run", "workflow-init",
     "--agent", "bmm-architect"
   ])

4. BMAD-METHOD → Exécution
   - Charge l'agent BMM Architect
   - Exécute le workflow workflow-init
   - Génère PRD, architecture, etc.

5. Backend ← BMAD Output
   Capture stdout/stderr

6. Archon MCP ← Response
   {
     "execution_id": "uuid-123",
     "status": "queued",
     "created_at": "2025-11-16T..."
   }

7. Claude Code ← MCP Response
   Reçoit l'execution_id pour tracking
```

### 2. Monitoring de l'Exécution

```
1. Claude Code → Polling Request
   bmad_get_workflow_status(execution_id="uuid-123")

2. Backend → Vérification
   Consulte workflow_executions[uuid-123]

3. Response
   {
     "status": "running",
     "output": "Analyzing project requirements...\n",
     "error": null
   }

4. Status Final
   {
     "status": "completed",
     "output": "✅ PRD generated successfully\n📄 See ./bmad/prd.md",
     "error": null
   }
```

## Composants Créés

### 1. Outils MCP BMAD
**Fichiers:**
- `Archon/python/src/mcp_server/features/bmad/__init__.py`
- `Archon/python/src/mcp_server/features/bmad/bmad_tools.py`

**Outils exposés:**
```python
@mcp.tool()
async def bmad_list_agents(ctx) -> str
    """Liste tous les agents BMAD disponibles"""

@mcp.tool()
async def bmad_list_workflows(ctx, agent: str = None) -> str
    """Liste les workflows, filtrés par agent optionnellement"""

@mcp.tool()
async def bmad_execute_workflow(ctx, workflow_name, agent_id, context_data) -> str
    """Lance l'exécution d'un workflow BMAD"""

@mcp.tool()
async def bmad_get_workflow_status(ctx, execution_id) -> str
    """Récupère le status et l'output d'une exécution"""

@mcp.tool()
async def bmad_cancel_workflow(ctx, execution_id) -> str
    """Annule un workflow en cours"""

@mcp.tool()
async def bmad_get_active_workflows(ctx) -> str
    """Liste tous les workflows actifs"""
```

### 2. Backend BMAD Router
**Fichier:** `rag-compat/app/routers/bmad.py`

**Endpoints HTTP:**
```python
GET  /api/bmad/agents            # Liste des 8 agents
GET  /api/bmad/workflows         # Liste des 9 workflows
POST /api/bmad/workflows/execute # Lance un workflow
GET  /api/bmad/workflows/{id}    # Status d'exécution
GET  /api/bmad/workflows/active  # Workflows actifs
DELETE /api/bmad/workflows/{id}  # Annulation
GET  /api/bmad/health            # Health check
```

### 3. Interface Frontend BMAD
**Fichiers:**
- `Archon/archon-ui-main/src/features/bmad/*`
- `Archon/archon-ui-main/src/pages/BMADPage.tsx`

**UI Components:**
- `AgentCard` - Sélection d'agents avec gradients par catégorie
- `WorkflowCard` - Lancement de workflows
- `WorkflowExecutionCard` - Suivi en temps réel (polling 2s)

**Accès:** http://localhost:3737/bmad

## Configuration Requise

### 1. Variables d'Environnement

**.env actuel:**
```bash
# Backend
POSTGRES_URL=postgresql://postgres:password@localhost:5432/archon
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Frontend
VITE_API_URL=http://localhost:8180
VITE_SHOW_DEVTOOLS=true

# Archon MCP Server (à ajouter si démarré)
ARCHON_MCP_PORT=8051
ARCHON_API_URL=http://localhost:8180
```

### 2. Démarrage du Serveur MCP Archon

**Option A: Avec Docker (recommandé)**

Ajouter dans `docker-compose.yml`:
```yaml
  archon-mcp:
    build:
      context: ./Archon/python
      dockerfile: Dockerfile
    container_name: ragdz-archon-mcp
    depends_on:
      - backend
    environment:
      ARCHON_MCP_PORT: 8051
      ARCHON_API_URL: http://backend:8180
      SUPABASE_URL: ${SUPABASE_URL}
      SUPABASE_SERVICE_KEY: ${SUPABASE_SERVICE_KEY}
    ports:
      - "8051:8051"
    command: python -m src.mcp_server.mcp_server
    networks:
      - ragdz-network
```

**Option B: Local (développement)**
```bash
cd Archon/python
export ARCHON_MCP_PORT=8051
export ARCHON_API_URL=http://localhost:8180
python -m src.mcp_server.mcp_server
```

### 3. Configuration Claude Code

**claude_code_config.json:**
```json
{
  "mcpServers": {
    "archon-ragdz": {
      "url": "http://localhost:8051/mcp",
      "transport": "streamable-http"
    }
  }
}
```

Ou utiliser le format SSE:
```json
{
  "mcpServers": {
    "archon-ragdz": {
      "command": "curl",
      "args": ["-N", "http://localhost:8051/mcp/sse"]
    }
  }
}
```

## Cas d'Usage

### Exemple 1: Initialiser un Nouveau Projet

```bash
# Dans Claude Code
Utilise BMAD pour initialiser un nouveau projet web.

→ Claude Code appelle:
bmad_execute_workflow(
  workflow_name="workflow-init",
  agent_id="bmm-architect",
  context_data='{"project_type": "web_app", "tech_stack": "React + FastAPI"}'
)

→ BMAD génère:
- PRD complet
- Architecture système
- Plan de développement
- User stories

→ Résultats dans: ./bmad/output/
```

### Exemple 2: Revue de Code

```bash
# Dans Claude Code
Fais une revue de code du fichier auth.py avec BMAD.

→ Claude Code appelle:
bmad_execute_workflow(
  workflow_name="code-review",
  agent_id="bmm-coder",
  context_data='{"file": "auth.py", "focus": "security"}'
)

→ BMAD analyse:
- Qualité du code
- Sécurité
- Best practices
- Suggestions d'amélioration
```

### Exemple 3: Génération de Tests

```bash
# Dans Claude Code
Génère des tests pour le module de paiement.

→ Claude Code appelle:
bmad_execute_workflow(
  workflow_name="test-generation",
  agent_id="bmm-tester",
  context_data='{"module": "payment", "coverage_target": 90}'
)

→ BMAD crée:
- Tests unitaires
- Tests d'intégration
- Tests E2E
- Fixtures
```

## État Actuel

### ✅ Complété

1. **Backend BMAD Router** - Endpoints HTTP fonctionnels
2. **Outils MCP BMAD** - 6 outils exposés via MCP
3. **Interface Frontend BMAD** - UI complète avec polling temps réel
4. **Configuration BMAD** - 8 agents + 9 workflows définis
5. **Documentation** - Architecture et cas d'usage

### 🔄 En Cours

1. **Serveur MCP Archon** - À démarrer (port 8051)
2. **Exécution BMAD réelle** - Actuellement en simulation
3. **Configuration Claude Code** - À tester la connexion MCP

### 📋 À Faire

1. **Implémentation Subprocess**
   ```python
   async def run_bmad_workflow(workflow_id, request):
       # Remplacer la simulation par:
       process = await asyncio.create_subprocess_exec(
           "npx", "bmad-method", "run", request.name,
           "--agent", request.agent,
           cwd=str(BMAD_PATH),
           stdout=asyncio.subprocess.PIPE,
           stderr=asyncio.subprocess.PIPE
       )

       stdout, stderr = await process.communicate()
       workflow_executions[workflow_id]["output"] = stdout.decode()
   ```

2. **Gestion d'Erreurs BMAD**
   - Timeout après 5 minutes
   - Capture stderr
   - Retry logic

3. **Persistance Workflows**
   - Utiliser Redis au lieu de dict en mémoire
   - Historique des exécutions
   - Logs structurés

4. **Tests de Bout en Bout**
   - Backend → BMAD → Output
   - MCP Server → Backend → BMAD
   - Claude Code → MCP → Backend → BMAD

## Commandes Utiles

### Tester le Backend BMAD
```bash
# Liste des agents
curl http://localhost:8180/api/bmad/agents

# Liste des workflows
curl http://localhost:8180/api/bmad/workflows

# Lancer un workflow
curl -X POST http://localhost:8180/api/bmad/workflows/execute \
  -H "Content-Type: application/json" \
  -d '{
    "name": "workflow-init",
    "agent": "bmm-architect",
    "description": "Test workflow"
  }'

# Status d'un workflow
curl http://localhost:8180/api/bmad/workflows/{execution_id}

# Workflows actifs
curl http://localhost:8180/api/bmad/workflows/active

# Health check
curl http://localhost:8180/api/bmad/health
```

### Tester le Serveur MCP
```bash
# Health check MCP
curl http://localhost:8051/health

# Lister les outils MCP disponibles
# (Nécessite un client MCP - Claude Code, mcp-cli, etc.)
```

### Démarrer l'Écosystème
```bash
# 1. Démarrer Docker
docker-compose up -d

# 2. Vérifier les services
docker-compose ps
docker logs ragdz-backend
docker logs ragdz-frontend

# 3. Tester le frontend
open http://localhost:3737/bmad

# 4. Démarrer MCP Server (si pas dans Docker)
cd Archon/python
python -m src.mcp_server.mcp_server
```

## Bénéfices de l'Écosystème

### Pour le Développeur

1. **Agent Orchestration depuis IDE**
   - Pas besoin de quitter Claude Code
   - Workflows guidés pour chaque tâche
   - Context-aware avec accès au code

2. **Workflows Spécialisés**
   - Architecture → BMM Architect
   - Coding → BMM Coder
   - Testing → BMM Tester
   - Debug → BMM Debugger

3. **Connaissance Archon + BMAD**
   - RAG search dans docs Archon
   - BMAD workflows pour implémentation
   - Synergie entre connaissance et exécution

### Pour le Projet

1. **Consistance**
   - Tous les développeurs utilisent mêmes workflows
   - Standards de code cohérents
   - Documentation automatique

2. **Qualité**
   - Revues de code systématiques
   - Tests générés automatiquement
   - Architecture validée

3. **Productivité**
   - Workflows optimisés
   - Moins d'erreurs
   - Onboarding plus rapide

## Prochaines Étapes Recommandées

1. **Démarrer le MCP Server** (priorité haute)
   ```bash
   cd Archon/python
   python -m src.mcp_server.mcp_server
   ```

2. **Tester la Connexion MCP** (priorité haute)
   - Configurer Claude Code
   - Appeler `bmad_list_agents()`
   - Vérifier les outils disponibles

3. **Implémenter l'Exécution Réelle BMAD** (priorité moyenne)
   - Remplacer simulation par subprocess
   - Tester avec workflow-init
   - Capturer output réel

4. **Ajouter Persistance** (priorité basse)
   - Redis pour workflow_executions
   - PostgreSQL pour historique
   - Logs structurés

## Support et Documentation

- **Architecture Archon:** `Archon/CLAUDE.md`
- **BMAD Documentation:** `bmad/README.md`
- **Frontend BMAD:** http://localhost:3737/bmad
- **Backend API:** http://localhost:8180/api/bmad/*
- **MCP Health:** http://localhost:8051/health

---

**Note:** Cette intégration combine trois technologies majeures:
- **BMAD-METHOD** - Orchestration d'agents AI
- **Archon** - RAG knowledge base avec MCP
- **Claude Code** - IDE avec support MCP

L'écosystème permet de créer un workflow de développement AI-first complet.
