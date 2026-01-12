# Architecture Intégrée Bolt-DIY ↔ BMAD ↔ Archon

## 🎯 Vision du Système

Un système unifié où **Bolt-DIY** devient l'interface utilisateur principale, permettant deux modes de travail :

1. **Mode Direct** : L'utilisateur a déjà son prompt → Génération immédiate
2. **Mode Orchestré BMAD** : Pas de prompt clair → Les agents BMAD construisent le projet étape par étape

À la fin, **SuperPower Orchestrator** synchronise tout dans **Archon** et génère le produit final en **ZIP**.

---

## 🏗️ Architecture Globale

```
┌─────────────────────────────────────────────────────────────────┐
│                      BOLT-DIY Frontend                           │
│                    (Interface Principale)                        │
│                         Port: 5174                               │
│                                                                  │
│  ┌────────────────┐              ┌─────────────────────┐       │
│  │  Mode Direct   │              │  Mode BMAD Agents   │       │
│  │                │              │                     │       │
│  │ • Prompt ready │              │ • Agent Architect   │       │
│  │ • Generate now │              │ • Agent PM          │       │
│  │ • Quick start  │              │ • Agent Backend Dev │       │
│  └────────┬───────┘              │ • Agent Frontend    │       │
│           │                      │ • Agent DevOps      │       │
│           │                      │ • Agent QA          │       │
│           │                      └──────────┬──────────┘       │
│           │                                 │                   │
│           └─────────────┬───────────────────┘                   │
│                         │                                       │
│                    [User Input]                                 │
└────────────────────────┼─────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │   SuperPower Orchestrator API      │
        │   Backend: Port 8180               │
        │                                    │
        │ Endpoints:                         │
        │ • POST /api/bolt/direct            │
        │ • POST /api/bolt/bmad-workflow     │
        │ • GET  /api/bolt/status/{id}       │
        │ • POST /api/bolt/export-zip        │
        └────────────┬───────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
    ┌────────┐  ┌────────┐  ┌─────────┐
    │  BMAD  │  │ Archon │  │ Qdrant  │
    │ Agents │  │   KB   │  │ Vectors │
    │  Node  │  │  API   │  │         │
    └────────┘  └────────┘  └─────────┘
         │           │           │
         └───────────┴───────────┘
                     │
                     ▼
            ┌────────────────┐
            │  Final Product │
            │   (ZIP Export) │
            └────────────────┘
```

---

## 📊 Workflow Détaillé

### Mode 1 : Direct (Prompt déjà prêt)

```
User → Bolt-DIY → Backend Direct API → Generate Code → ZIP
                                                          ↓
                                                    Save to Archon (KB)
```

**Exemple d'utilisation** :
```json
POST /api/bolt/direct
{
  "prompt": "Create a React e-commerce app with Stripe integration",
  "tech_stack": ["React", "TypeScript", "Stripe", "TailwindCSS"],
  "save_to_archon": true
}
```

**Réponse** :
```json
{
  "workflow_id": "uuid-xxx",
  "status": "generating",
  "archon_project_id": 123,
  "estimated_time": "2-5 minutes"
}
```

---

### Mode 2 : Orchestré BMAD (Construction par agents)

```
User → Bolt-DIY → Backend BMAD API → Agents BMAD (séquentiel)
                                           ↓
                                    Agent #1: Architect
                                           ↓
                                    Agent #2: PM
                                           ↓
                                    Agent #3: Backend Dev
                                           ↓
                                    Agent #4: Frontend Dev
                                           ↓
                                    Agent #5: DevOps
                                           ↓
                                    Agent #6: QA Tester
                                           ↓
                                    SuperPower Orchestrator
                                           ↓
                                    Save to Archon (Knowledge Base + Project)
                                           ↓
                                    Generate Final Code → ZIP
```

**Exemple d'utilisation** :
```json
POST /api/bolt/bmad-workflow
{
  "user_description": "Je veux créer une plateforme de gestion de tâches collaborative",
  "constraints": {
    "budget": "low",
    "timeline": "2 weeks",
    "team_size": 1
  },
  "preferences": {
    "tech_stack": "modern",
    "deployment": "cloud"
  }
}
```

**Processus** :

1. **Agent Architect (Winston)** :
   - Analyse les besoins
   - Propose architecture (Monolithic vs Microservices)
   - Définit tech stack optimal
   - Output: `architecture.md`

2. **Agent PM (John)** :
   - Crée user stories
   - Priorise features (MVP)
   - Définit sprints
   - Output: `requirements.md`, `user-stories.md`

3. **Agent Backend Dev (Amelia)** :
   - Design API endpoints
   - Database schema
   - Authentication/Authorization
   - Output: `api-design.md`, `schema.sql`

4. **Agent Frontend Dev (Sara)** :
   - UI/UX wireframes
   - Component architecture
   - State management
   - Output: `ui-components.md`, `routes.md`

5. **Agent DevOps (Carlos)** :
   - CI/CD pipeline
   - Infrastructure as Code
   - Deployment strategy
   - Output: `docker-compose.yml`, `.github/workflows/`

6. **Agent QA (Murat)** :
   - Test strategy
   - Test cases
   - Quality gates
   - Output: `test-plan.md`, `test-cases.md`

7. **SuperPower Orchestrator** :
   - Synthétise tous les outputs
   - Crée Knowledge Base dans Archon
   - Crée Project dans Archon
   - Génère instructions de production pour Bolt
   - Déclenche génération finale

---

## 🔌 API SuperPower Orchestrator

### Endpoint 1 : Mode Direct

```http
POST /api/bolt/direct
Content-Type: application/json
X-API-Key: ragdz_dev_demo_key_12345678901234567890

{
  "prompt": "string (required)",
  "tech_stack": ["string"],
  "save_to_archon": boolean,
  "export_format": "zip" | "github" | "gitlab"
}
```

**Réponse** :
```json
{
  "workflow_id": "uuid",
  "status": "generating" | "completed" | "failed",
  "archon_project_id": 123,
  "archon_url": "http://localhost:3737/projects/123",
  "download_url": "/api/bolt/download/{workflow_id}",
  "estimated_time_seconds": 120
}
```

---

### Endpoint 2 : Mode BMAD Orchestré

```http
POST /api/bolt/bmad-workflow
Content-Type: application/json
X-API-Key: ragdz_dev_demo_key_12345678901234567890

{
  "user_description": "string (required)",
  "constraints": {
    "budget": "low" | "medium" | "high",
    "timeline": "string",
    "team_size": number
  },
  "preferences": {
    "tech_stack": "modern" | "stable" | "custom",
    "deployment": "cloud" | "on-premise" | "hybrid"
  },
  "agents_to_use": ["architect", "pm", "backend", "frontend", "devops", "qa"]
}
```

**Réponse** :
```json
{
  "workflow_id": "uuid",
  "status": "orchestrating",
  "current_agent": "architect",
  "agents_completed": [],
  "agents_pending": ["pm", "backend", "frontend", "devops", "qa"],
  "estimated_time_seconds": 600,
  "live_updates_url": "/api/bolt/status/{workflow_id}"
}
```

---

### Endpoint 3 : Status en Temps Réel

```http
GET /api/bolt/status/{workflow_id}
X-API-Key: ragdz_dev_demo_key_12345678901234567890
```

**Réponse** :
```json
{
  "workflow_id": "uuid",
  "status": "orchestrating" | "generating" | "completed" | "failed",
  "progress_percent": 75,
  "current_step": "Agent Backend Dev en cours...",
  "agents_completed": [
    {
      "agent": "architect",
      "completed_at": "2025-01-19T10:30:00Z",
      "output_summary": "Architecture définie: Monolithic FastAPI + React"
    },
    {
      "agent": "pm",
      "completed_at": "2025-01-19T10:35:00Z",
      "output_summary": "15 user stories créées, MVP défini"
    }
  ],
  "agents_pending": ["frontend", "devops", "qa"],
  "archon_project_id": 123,
  "errors": []
}
```

---

### Endpoint 4 : Export ZIP

```http
POST /api/bolt/export-zip/{workflow_id}
X-API-Key: ragdz_dev_demo_key_12345678901234567890

{
  "include_docs": true,
  "include_tests": true,
  "include_deployment": true
}
```

**Réponse** :
```http
Content-Type: application/zip
Content-Disposition: attachment; filename="project-{workflow_id}.zip"

[Binary ZIP file]
```

**Structure du ZIP** :
```
project-uuid/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── REQUIREMENTS.md
│   ├── API_DESIGN.md
│   └── USER_STORIES.md
├── src/
│   ├── backend/
│   │   ├── app/
│   │   ├── tests/
│   │   └── requirements.txt
│   └── frontend/
│       ├── src/
│       ├── public/
│       └── package.json
├── infrastructure/
│   ├── docker-compose.yml
│   └── .github/workflows/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── README.md
└── .env.example
```

---

## 🧠 Intégration Archon

### Synchronisation Automatique

À chaque workflow (Direct ou BMAD), le système :

1. **Crée un Knowledge Source** :
```python
# Dans Qdrant
knowledge_id = create_knowledge_source(
    name=f"Project {workflow_id}",
    type="project",
    content=synthesis_of_all_agents,
    embeddings=generate_embeddings(content),
    metadata={
        "workflow_id": workflow_id,
        "agents_used": agents_list,
        "tech_stack": tech_stack,
        "created_at": datetime.now()
    }
)
```

2. **Crée un Project dans Archon** (si activé) :
```http
POST http://localhost:8181/api/projects
{
  "name": "Project from Bolt Workflow",
  "description": "Generated via BMAD orchestration",
  "features": ["feature1", "feature2"],
  "knowledge_source_id": knowledge_id
}
```

3. **Lie les Documents** :
   - `architecture.md` → Knowledge Base
   - `requirements.md` → Project Docs
   - `api-design.md` → Code Examples
   - Etc.

---

## 🎨 Interface Bolt-DIY Modifiée

### Nouvelle Interface d'Accueil

```tsx
// bolt-diy/app/routes/_index.tsx

export default function Index() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1>Bolt-DIY + BMAD SuperPower</h1>

      {/* Choix du mode */}
      <div className="flex gap-4 mt-8">

        {/* Mode Direct */}
        <Card onClick={() => navigate('/direct')}>
          <h2>⚡ Mode Direct</h2>
          <p>Vous avez déjà votre prompt ?</p>
          <p>Génération immédiate !</p>
        </Card>

        {/* Mode BMAD */}
        <Card onClick={() => navigate('/bmad-agents')}>
          <h2>🤖 Mode BMAD Agents</h2>
          <p>Besoin d'aide pour structurer ?</p>
          <p>Nos agents construisent avec vous !</p>
        </Card>

      </div>
    </div>
  );
}
```

### Page Mode BMAD

```tsx
// bolt-diy/app/routes/bmad-agents.tsx

export default function BMADAgentsMode() {
  const [step, setStep] = useState(1);
  const [agentResults, setAgentResults] = useState({});

  return (
    <div className="workflow-container">

      {/* Progress Bar */}
      <ProgressBar
        steps={['Architect', 'PM', 'Backend', 'Frontend', 'DevOps', 'QA']}
        currentStep={step}
      />

      {/* Current Agent Display */}
      <AgentCard
        agent={currentAgent}
        onComplete={handleAgentComplete}
      />

      {/* User Can Review and Edit */}
      <AgentOutputEditor
        content={agentResults[currentAgent]}
        onChange={handleEdit}
      />

      {/* Navigation */}
      <div className="flex justify-between mt-8">
        <Button onClick={handlePrevious}>← Précédent</Button>
        <Button onClick={handleNext}>Suivant →</Button>
      </div>

      {/* Final Button */}
      {step === 6 && (
        <Button onClick={handleGenerateProject} className="btn-primary">
          🚀 Générer le Projet Final
        </Button>
      )}

    </div>
  );
}
```

---

## 💾 Base de Données PostgreSQL

### Nouvelle Table : `bolt_workflows`

```sql
CREATE TABLE bolt_workflows (
    id SERIAL PRIMARY KEY,
    workflow_id UUID UNIQUE NOT NULL,
    mode VARCHAR(20) NOT NULL, -- 'direct' or 'bmad'
    user_description TEXT,
    status VARCHAR(20) NOT NULL, -- 'pending', 'orchestrating', 'generating', 'completed', 'failed'
    current_agent VARCHAR(50),
    agents_completed JSONB DEFAULT '[]',
    tech_stack JSONB,
    archon_project_id INTEGER REFERENCES archon_projects(id),
    knowledge_source_id VARCHAR(100),
    zip_file_path TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    metadata JSONB
);

CREATE INDEX idx_workflow_id ON bolt_workflows(workflow_id);
CREATE INDEX idx_status ON bolt_workflows(status);
CREATE INDEX idx_archon_project ON bolt_workflows(archon_project_id);
```

### Nouvelle Table : `agent_executions`

```sql
CREATE TABLE agent_executions (
    id SERIAL PRIMARY KEY,
    workflow_id UUID NOT NULL REFERENCES bolt_workflows(workflow_id),
    agent_name VARCHAR(100) NOT NULL,
    agent_id VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL, -- 'pending', 'running', 'completed', 'failed'
    input_context JSONB,
    output_result TEXT,
    output_summary TEXT,
    execution_time_seconds INTEGER,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT
);

CREATE INDEX idx_workflow_agent ON agent_executions(workflow_id, agent_name);
```

---

## 🔄 Flux de Données Complet

### Scénario Complet : Mode BMAD

1. **User ouvre Bolt-DIY** (http://localhost:5174)
2. **Choisit "Mode BMAD Agents"**
3. **Remplit le formulaire** :
   - Description : "Plateforme de gestion de tâches collaborative"
   - Contraintes : Budget low, Timeline 2 weeks
   - Préférences : Tech moderne, Cloud deployment

4. **Backend reçoit la requête** :
   ```python
   @router.post("/bolt/bmad-workflow")
   async def create_bmad_workflow(request: BMADWorkflowRequest):
       workflow_id = str(uuid.uuid4())

       # Créer le workflow
       workflow = create_workflow_record(workflow_id, request)

       # Lancer orchestration asynchrone
       background_tasks.add_task(run_bmad_orchestration, workflow_id)

       return {"workflow_id": workflow_id, "status": "orchestrating"}
   ```

5. **Orchestration BMAD démarre** :
   ```python
   async def run_bmad_orchestration(workflow_id: str):
       agents = ["architect", "pm", "backend", "frontend", "devops", "qa"]

       results = {}
       for agent_id in agents:
           # Exécuter agent
           result = await execute_agent(
               agent_id=agent_id,
               context=previous_results,
               user_input=workflow.user_description
           )
           results[agent_id] = result

           # Sauvegarder résultat
           save_agent_execution(workflow_id, agent_id, result)

           # Mettre à jour status
           update_workflow_status(workflow_id, current_agent=agent_id)
   ```

6. **SuperPower Orchestrator synthétise** :
   ```python
   synthesis = orchestrator_service.synthesize_knowledge(
       messages=all_agent_results,
       agents_used=agents
   )
   ```

7. **Création dans Archon** :
   ```python
   # Knowledge Base
   knowledge_id = create_knowledge_source_in_qdrant(synthesis)

   # Project
   archon_project = create_project_in_archon(
       name=f"Workflow {workflow_id}",
       knowledge_source_id=knowledge_id,
       tech_stack=detected_tech_stack
   )
   ```

8. **Génération du code final** :
   ```python
   production_command = orchestrator_service.order_bolt_production(
       project_id=archon_project["id"],
       synthesis=synthesis,
       tech_stack=tech_stack
   )

   # Appeler le générateur de code de Bolt
   generated_code = bolt_code_generator.generate(production_command)
   ```

9. **Création du ZIP** :
   ```python
   zip_path = create_project_zip(
       workflow_id=workflow_id,
       generated_code=generated_code,
       documentation=all_agent_docs,
       tests=test_files
   )

   update_workflow(workflow_id, zip_file_path=zip_path, status="completed")
   ```

10. **User reçoit notification** :
    - Frontend poll `/api/bolt/status/{workflow_id}`
    - Status = "completed"
    - Affiche bouton "📥 Télécharger le Projet"
    - User clique → Download ZIP

---

## 🚀 Plan d'Implémentation

### Phase 1 : Backend SuperPower API (2-3 jours)

- [ ] Créer `/api/bolt/direct` endpoint
- [ ] Créer `/api/bolt/bmad-workflow` endpoint
- [ ] Créer `/api/bolt/status/{id}` endpoint
- [ ] Créer `/api/bolt/export-zip/{id}` endpoint
- [ ] Implémenter orchestration séquentielle des agents
- [ ] Créer service de synthèse de connaissance
- [ ] Intégrer avec Archon API
- [ ] Créer générateur de ZIP

### Phase 2 : Intégration Archon (2 jours)

- [ ] Déplacer `Archon/archon-ui-main/` → `frontend/archon-ui/`
- [ ] Configurer Supabase ou adapter pour PostgreSQL
- [ ] Rebuilder service Archon frontend
- [ ] Tester création automatique de projets
- [ ] Tester synchronisation knowledge base

### Phase 3 : Interface Bolt-DIY (3-4 jours)

- [ ] Créer page d'accueil avec choix de mode
- [ ] Créer page Mode Direct
- [ ] Créer page Mode BMAD avec workflow agents
- [ ] Implémenter progress bar temps réel
- [ ] Créer composants AgentCard
- [ ] Créer éditeur de résultats d'agents
- [ ] Intégrer download ZIP
- [ ] WebSocket pour live updates (optionnel)

### Phase 4 : Tests & Optimisation (2 jours)

- [ ] Tests end-to-end workflow complet
- [ ] Tests de performance (temps de génération)
- [ ] Tests de qualité du code généré
- [ ] Optimisation des prompts agents
- [ ] Documentation utilisateur
- [ ] Démo vidéo

---

## 📈 Métriques de Succès

### Performance

- **Mode Direct** : < 3 minutes de génération
- **Mode BMAD** : < 10 minutes pour orchestration complète
- **Export ZIP** : < 30 secondes

### Qualité

- **Code généré** : Lint sans erreurs
- **Tests** : Couverture > 70%
- **Documentation** : Complète et à jour
- **Architecture** : Scalable et maintenable

### Expérience Utilisateur

- **Clarté du workflow** : User comprend où il en est
- **Feedback temps réel** : Pas d'attente sans information
- **Flexibilité** : User peut éditer les résultats agents
- **Simplicité** : 3 clics maximum pour démarrer

---

## 🎯 Exemple Concret d'Utilisation

### Scénario : Créer une app de todo list collaborative

**Étape 1** : User ouvre Bolt-DIY → Choisit "Mode BMAD"

**Étape 2** : Remplit formulaire :
```
Description: "Créer une todo list collaborative avec partage en temps réel,
notifications, et intégration calendrier"

Contraintes:
- Budget: Low
- Timeline: 1 semaine
- Team: 1 développeur

Préférences:
- Tech: Moderne et simple
- Deployment: Cloud (Vercel/Netlify)
```

**Étape 3** : Agents s'exécutent

**Agent Architect** :
```markdown
# Architecture Recommandée

## Tech Stack
- Frontend: React 18 + TypeScript + Vite
- Backend: Supabase (Auth + Realtime DB + Storage)
- Styling: TailwindCSS + shadcn/ui
- State: Zustand
- Deployment: Vercel (frontend) + Supabase Cloud

## Justification
Budget low → Pas de backend custom → Supabase BaaS
Timeline court → Stack moderne avec boilerplate rapide
1 développeur → Pas de microservices, monolithic simple
Collaborative → Supabase Realtime out-of-the-box
```

**Agent PM** :
```markdown
# User Stories (MVP)

## Epic 1: Authentication
- [ ] User peut s'inscrire avec email/password
- [ ] User peut se connecter
- [ ] User peut se déconnecter

## Epic 2: Task Management
- [ ] User peut créer une tâche
- [ ] User peut voir ses tâches
- [ ] User peut marquer tâche comme complétée
- [ ] User peut supprimer une tâche

## Epic 3: Collaboration
- [ ] User peut partager une liste avec un autre user
- [ ] User peut voir les modifications en temps réel
- [ ] User reçoit notifications lors d'un partage

## Out of Scope (v2)
- Calendrier intégration
- Sous-tâches
- Tags et filtres avancés
```

**Agent Backend Dev** :
```sql
-- Supabase Schema

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    owner_id UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE shared_tasks (
    task_id UUID REFERENCES tasks(id),
    user_id UUID REFERENCES users(id),
    permission VARCHAR(10) DEFAULT 'read', -- 'read', 'write'
    PRIMARY KEY (task_id, user_id)
);

-- Row Level Security
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can see their own tasks"
    ON tasks FOR SELECT
    USING (auth.uid() = owner_id OR auth.uid() IN (
        SELECT user_id FROM shared_tasks WHERE task_id = tasks.id
    ));
```

**Agent Frontend Dev** :
```tsx
// Component Architecture

src/
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   └── SignupForm.tsx
│   ├── tasks/
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── CreateTaskForm.tsx
│   │   └── ShareTaskDialog.tsx
│   └── layout/
│       ├── Header.tsx
│       └── Sidebar.tsx
├── stores/
│   ├── authStore.ts
│   └── tasksStore.ts
├── lib/
│   └── supabase.ts
└── App.tsx

// State Management: Zustand
// Realtime: Supabase subscriptions
// UI: shadcn/ui components
```

**Agent DevOps** :
```yaml
# .github/workflows/deploy.yml

name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run build
      - uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID}}
          vercel-project-id: ${{ secrets.PROJECT_ID}}
```

**Agent QA** :
```markdown
# Test Plan

## Unit Tests (Vitest)
- [ ] Task CRUD operations
- [ ] Auth flows
- [ ] Zustand stores

## Integration Tests (Playwright)
- [ ] User signup → Create task → Complete task → Logout
- [ ] User A creates task → Share with User B → User B sees task
- [ ] Realtime sync: User A edits → User B sees update

## Test Coverage Target: 70%
```

**Étape 4** : SuperPower Orchestrator synthétise

**Étape 5** : Création dans Archon
- Knowledge Base créée avec tous les docs
- Project "Todo Collaborative" créé avec features

**Étape 6** : Génération du code final par Bolt

**Étape 7** : Création du ZIP

**Étape 8** : User télécharge :
```
todo-collaborative-app/
├── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── USER_STORIES.md
│   └── DEPLOYMENT.md
├── src/
│   ├── components/ (code React complet)
│   ├── stores/
│   ├── lib/
│   └── App.tsx
├── tests/
├── .github/workflows/
├── package.json
├── vite.config.ts
└── .env.example
```

**Résultat** : App complète, documentée, testable, déployable en 1 commande !

---

## 🔐 Sécurité

### API Keys

Toutes les requêtes nécessitent :
```http
X-API-Key: ragdz_dev_demo_key_12345678901234567890
```

### Rate Limiting

- 10 workflows / heure par user (Mode Direct)
- 3 workflows / heure par user (Mode BMAD)
- Burst protection : 5 requêtes max en parallèle

### Validation

- Inputs sanitisés (XSS, SQL injection)
- Code généré linted avant export
- Dependencies vérifiées (npm audit)

---

## 📝 Conclusion

Ce système unifié offre :

✅ **Flexibilité** : 2 modes selon les besoins
✅ **Intelligence** : Agents BMAD construisent avec l'utilisateur
✅ **Traçabilité** : Tout sauvegardé dans Archon
✅ **Qualité** : Code généré professionnel et documenté
✅ **Simplicité** : Interface intuitive Bolt-DIY
✅ **Scalabilité** : Architecture modulaire et extensible

**Prochaine étape** : Commencer l'implémentation Phase 1 ! 🚀
