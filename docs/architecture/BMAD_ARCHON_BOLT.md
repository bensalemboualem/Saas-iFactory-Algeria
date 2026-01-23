# BMAD / ARCHON / BOLT - Etat dans RAG-DZ

**Date:** 30 Decembre 2025

---

## BMAD Method

### Statut: OUI - INTEGRE COMPLETEMENT

### Fichiers et Repertoires Trouves

| Type | Chemin | Description |
|------|--------|-------------|
| **Repertoire Principal** | `bmad/` | Installation complete BMAD Method |
| **Node Module** | `node_modules/bmad-method/` | Package npm installe |
| **Claude Commands** | `.claude/commands/bmad/` | 3 commandes (architect, dev, pm) |
| **CLI** | `bmad/tools/cli/bmad-cli.js` | CLI BMAD |
| **Scripts Demarrage** | `scripts/start-bolt-bmad.bat/.sh` | Scripts lancement |
| **API Routers** | `services/api/app/routers/bmad*.py` | 4 routers API |

### Niveau d'Integration

| Composant | Statut | Details |
|-----------|--------|---------|
| Core BMAD | Complet | `bmad/src/core/` avec agents, tasks, workflows |
| Modules BMB | Complet | Agent Builder, Workflow Builder, Module Builder |
| Modules BMM | Complet | Claude Code sub-agents, workflows |
| API Backend | Complet | 4 routers (bmad, bmad_chat, bmad_openai, bmad_orchestration) |
| Docker | Integre | Reference dans `docker-compose.yml` |
| Claude Integration | Complet | Commands dans `.claude/commands/bmad/` |

### Agents BMAD Builder Disponibles

| Agent | Fichier | Fonction |
|-------|---------|----------|
| Bond | `agent-builder.agent.yaml` | Agent Building Expert - Cree des agents |
| Wendy | `workflow-builder.agent.yaml` | Workflow Building Master - Cree des workflows |
| - | `module-builder.agent.yaml` | Module Builder - Cree des modules |

### Workflows BMAD

| Workflow | Chemin | Description |
|----------|--------|-------------|
| Create Agent | `bmb/workflows/create-agent/` | Workflow creation agent |
| Edit Agent | `bmb/workflows/edit-agent/` | Workflow edition agent |
| Create Workflow | `bmb/workflows/create-workflow/` | Workflow creation workflow |
| Brainstorming | `core/workflows/brainstorming/` | Workflow brainstorming |
| Party Mode | `core/workflows/party-mode/` | Workflow fun/creative |

---

## Archon

### Statut: OUI - INTEGRE COMPLETEMENT

### Fichiers et Repertoires Trouves

| Type | Chemin | Description |
|------|--------|-------------|
| **Repertoire Principal** | `frontend/archon-ui/` | Clone complet Archon UI |
| **Python Backend** | `frontend/archon-ui/python/` | Backend Python Archon |
| **UI Main** | `frontend/archon-ui/archon-ui-main/` | Frontend React Archon |
| **Claude Commands** | `frontend/archon-ui/.claude/commands/archon/` | 7 commandes |
| **Git Submodule** | `.git/modules/frontend/archon-ui/` | Submodule Git |
| **Scripts Deploy** | `scripts/deploy/deploy-archon-vps.sh` | Script deploiement |
| **Service Integration** | `services/api/app/services/archon_integration_service.py` | Service integration |

### Niveau d'Integration

| Composant | Statut | Details |
|-----------|--------|---------|
| Knowledge Base | Complet | `KnowledgeBasePage.tsx`, `knowledge_item_service.py` |
| RAG Engine | Complet | `rag_agent.py`, `rag_service.py`, `rag_tools.py` |
| Document Agent | Complet | `document_agent.py` |
| Crawling Service | Complet | `crawling_service.py`, `discovery_service.py` |
| MCP Server | Complet | `mcp_server.py` avec features RAG |
| Embeddings | Complet | Multi-dimensional embeddings, contextual |
| Search Strategies | Complet | Hybrid, Agentic RAG, Base search |
| Projects/Tasks | Complet | Project, document, task services |
| API Backend | Complet | Knowledge API, MCP API, etc. |

### Services Archon

| Service | Fichier | Fonction |
|---------|---------|----------|
| Knowledge Item | `knowledge_item_service.py` | Gestion items KB |
| Knowledge Summary | `knowledge_summary_service.py` | Resume KB |
| Crawling | `crawling_service.py` | Web crawling |
| Discovery | `discovery_service.py` | Decouverte sources |
| Embedding | `embedding_service.py` | Embeddings multi-provider |
| RAG | `rag_service.py` | Recherche augmentee |
| Project Creation | `project_creation_service.py` | Creation projets |

---

## Bolt.diy

### Statut: OUI - INTEGRE COMPLETEMENT

### Fichiers et Repertoires Trouves

| Type | Chemin | Description |
|------|--------|-------------|
| **Repertoire Principal** | `bolt-diy/` | Clone complet Bolt.diy |
| **Git Submodule** | `.git/modules/bolt-diy/` | Submodule Git |
| **Docker Compose** | `infrastructure/docker/docker-compose.bolt.yml` | Config Docker Bolt |
| **Scripts** | `scripts/start-bolt-bmad.bat/.sh` | Scripts demarrage |
| **API Routers** | `services/api/app/routers/bolt*.py` | 2 routers (bolt, bolt_auth) |
| **Services** | `services/api/app/services/bolt_*.py` | 3 services Bolt |
| **Models** | `services/api/app/models/bolt_workflow.py` | Model workflow |
| **Migrations** | `services/api/migrations/003_bolt_workflows.sql` | Schema DB |

### Niveau d'Integration

| Composant | Statut | Details |
|-----------|--------|---------|
| Bolt.diy Core | Complet | Clone complet avec webcontainer |
| WebContainer | Complet | Routes webcontainer.* |
| Git Integration | Complet | Github, Gitlab branches/projects |
| Deploy | Complet | Netlify, Vercel deploiement |
| Supabase Integration | Complet | Routes api.supabase.* |
| API Backend | Complet | Routers bolt, bolt_auth |
| Workflow Service | Complet | bolt_workflow_service.py |
| Orchestration | Complet | bolt_orchestration_service.py |
| ZIP Export | Complet | bolt_zip_service.py |
| DB Schema | Complet | Migration workflows |

### Services Bolt

| Service | Fichier | Fonction |
|---------|---------|----------|
| Bolt Workflow | `bolt_workflow_service.py` | Gestion workflows Bolt |
| Bolt Orchestration | `bolt_orchestration_service.py` | Orchestration multi-agent |
| Bolt ZIP | `bolt_zip_service.py` | Export projets en ZIP |
| Bolt Auth | `bolt_auth.py` | Authentification Bolt |

### Routes Bolt.diy

| Route | Fonction |
|-------|----------|
| `/api.netlify-deploy` | Deploy sur Netlify |
| `/api.vercel-deploy` | Deploy sur Vercel |
| `/api.github-*` | Integration GitHub |
| `/api.gitlab-*` | Integration GitLab |
| `/api.supabase-*` | Integration Supabase |
| `/webcontainer.*` | Preview/Connect WebContainer |

---

## Fonctionnalites "User Creates" Existantes

### Resume

| Fonctionnalite | Existe | Via | Statut |
|----------------|--------|-----|--------|
| User cree ses agents | OUI | BMAD Agent Builder | Fonctionnel |
| User cree ses workflows | OUI | BMAD Workflow Builder | Fonctionnel |
| User cree ses apps | OUI | Bolt.diy | Fonctionnel |
| User cree sa KB | OUI | Archon Knowledge Base | Fonctionnel |
| User cree ses prompts | OUI | Prompt Creator | Fonctionnel |

### Details par Fonctionnalite

#### 1. Creation d'Agents (BMAD)

| Element | Details |
|---------|---------|
| **Interface** | Agent Building Expert (Bond) |
| **Commande** | `CA` ou `create-agent` |
| **Workflow** | `bmb/workflows/create-agent/workflow.md` |
| **Output** | Fichier `.agent.yaml` conforme BMAD |
| **Statut** | Fonctionnel |

#### 2. Creation de Workflows (BMAD)

| Element | Details |
|---------|---------|
| **Interface** | Workflow Building Master (Wendy) |
| **Commande** | `CW` ou `create-workflow` |
| **Workflow** | `bmb/workflows/create-workflow/workflow.md` |
| **Output** | Fichier `workflow.md` conforme BMAD |
| **Statut** | Fonctionnel |

#### 3. Creation d'Apps (Bolt.diy)

| Element | Details |
|---------|---------|
| **Interface** | Bolt.diy WebContainer IDE |
| **Chemin** | `bolt-diy/` |
| **Features** | Editor, Preview, Deploy (Netlify/Vercel/GitHub) |
| **Stack Support** | React, Vue, Svelte, Node.js, etc. |
| **Statut** | Fonctionnel (submodule Git) |

#### 4. Creation de Knowledge Base (Archon)

| Element | Details |
|---------|---------|
| **Interface** | KnowledgeBasePage.tsx |
| **Backend** | knowledge_item_service.py |
| **Features** | CRUD documents, embeddings, search |
| **RAG** | Hybrid search, agentic RAG |
| **Statut** | Fonctionnel |

#### 5. Creation de Prompts

| Element | Details |
|---------|---------|
| **Interface** | Prompt Creator app |
| **API** | `/api/prompt-creator/generate` |
| **Backend** | `prompt_creator.py` |
| **LLM** | Claude/GPT pour optimisation |
| **Statut** | Fonctionnel |

### Studios/Editors Supplementaires

| Studio | Chemin | Fonction | Statut |
|--------|--------|----------|--------|
| Video Studio | `apps/video-studio/` | Creation videos IA | Fonctionnel |
| Workflow Studio | `apps/workflow-studio/` | Editeur visuel workflows | Partiel |
| Prompt Creator | `apps/prompt-creator/` | Generateur prompts | Fonctionnel |
| Pipeline Creator | `apps/_archived/pipeline-creator/` | Creation pipelines | Archive |
| Creative Studio | `apps/_archived/creative-studio/` | Studio creatif | Archive |

---

## Script Integration BMAD-Archon-Bolt

Un script existe pour l'integration des 3 outils:

```
scripts/bmad-to-archon-to-bolt.py
```

Ce script permet de:
1. Generer un agent/workflow via BMAD
2. Stocker la documentation dans Archon KB
3. Generer le code via Bolt.diy

---

## Conclusion

**Les 3 projets open-source (BMAD, Archon, Bolt.diy) sont DEJA INTEGRES dans RAG-DZ:**

| Projet | Integration | User Creates |
|--------|-------------|--------------|
| BMAD | Complet (npm + API + Claude commands) | Agents, Workflows, Modules |
| Archon | Complet (submodule Git + services) | Knowledge Base, Documents |
| Bolt.diy | Complet (submodule Git + API) | Apps, Code, Deploy |

**L'architecture "User Creates" est deja en place** avec des interfaces pour:
- Creer des agents personnalises (BMAD)
- Creer des workflows (BMAD)
- Creer des apps (Bolt.diy)
- Creer des KB (Archon)
- Creer des prompts optimises

**Recommandation:** Pas besoin de re-integrer ces outils. Il faut plutot:
1. **Documenter** les interfaces utilisateur existantes
2. **Unifier** l'UX entre les 3 outils
3. **Exposer** ces fonctionnalites dans l'UI principale (ia-factory-ui)

---

*Rapport genere le 30 decembre 2025 par Claude Code*
