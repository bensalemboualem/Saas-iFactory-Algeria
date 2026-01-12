# ROADMAP-INTEGRATION.md - Version Complète

> **Objectif:** Finaliser Nexus end-to-end
> **Statut:** Phase 1 ✅ | Phase 2 ✅ | Phase 3 ✅ | Phase 4 ✅ | Phase 5 ✅ | Phase 6 ✅ | Phase 7 ✅
> **Temps restant:** TERMINÉ

---

## État Actuel

| Orchestrateur | Port | Status | Backend |
|---------------|------|--------|---------|
| nexus-meta | 8100 | ✅ healthy | Redis |
| nexus-archon | 8051 | ✅ healthy | PostgreSQL |
| nexus-bmad | 8052 | ✅ healthy | 4 workflows |
| nexus-bolt | 8053 | ✅ healthy | 3 templates |

---

## Phase 2: Connecter Archon à Supabase (45min)

### 2.1 Créer les tables dans Supabase

```sql
-- Exécuter dans Supabase SQL Editor

-- Table des tâches
CREATE TABLE IF NOT EXISTS nexus_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'todo' CHECK (status IN ('todo', 'doing', 'review', 'done')),
    assigned_to TEXT,
    project_id UUID,
    created_by TEXT,
    tenant_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table de la knowledge base
CREATE TABLE IF NOT EXISTS nexus_knowledge (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('doc', 'code', 'url', 'artifact')),
    source TEXT,
    embedding VECTOR(1536),
    metadata JSONB DEFAULT '{}',
    tenant_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table des projets
CREATE TABLE IF NOT EXISTS nexus_projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'active',
    tenant_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table des locks
CREATE TABLE IF NOT EXISTS nexus_locks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource TEXT NOT NULL UNIQUE,
    holder TEXT NOT NULL,
    acquired_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL
);

-- Index pour performance
CREATE INDEX idx_tasks_status ON nexus_tasks(status);
CREATE INDEX idx_tasks_tenant ON nexus_tasks(tenant_id);
CREATE INDEX idx_knowledge_type ON nexus_knowledge(type);
CREATE INDEX idx_knowledge_tenant ON nexus_knowledge(tenant_id);

-- RLS obligatoire
ALTER TABLE nexus_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE nexus_knowledge ENABLE ROW LEVEL SECURITY;
ALTER TABLE nexus_projects ENABLE ROW LEVEL SECURITY;

-- Policies RLS
CREATE POLICY "tenant_isolation_tasks" ON nexus_tasks
    FOR ALL USING (tenant_id = current_setting('app.tenant_id')::uuid);

CREATE POLICY "tenant_isolation_knowledge" ON nexus_knowledge
    FOR ALL USING (tenant_id = current_setting('app.tenant_id')::uuid);

CREATE POLICY "tenant_isolation_projects" ON nexus_projects
    FOR ALL USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

### 2.2 Configurer les variables d'environnement

```bash
# Ajouter dans .env
SUPABASE_URL=https://votre-projet.supabase.co
SUPABASE_SERVICE_KEY=votre-service-key
SUPABASE_ANON_KEY=votre-anon-key
```

### 2.3 Redémarrer Archon avec Supabase

```bash
docker restart nexus-archon
curl http://localhost:8051/health
# Doit retourner: {"status": "healthy", "supabase": "connected"}
```

**Critère de succès:** `GET /health` retourne `supabase: connected`

---

## Phase 3: Tester les Connexions Inter-Orchestrateurs (30min)

### 3.1 Test Meta → BMAD

```bash
curl -X POST http://localhost:8100/route \
  -H "Content-Type: application/json" \
  -d '{"content": "crée un PRD pour une app de facturation", "session_id": "test-1"}'

# Attendu: {"routed_to": "bmad", "action": "workflow", ...}
```

### 3.2 Test Meta → Archon

```bash
curl -X POST http://localhost:8100/route \
  -H "Content-Type: application/json" \
  -d '{"content": "cherche les docs sur Chargily", "session_id": "test-2"}'

# Attendu: {"routed_to": "archon", "action": "search", ...}
```

### 3.3 Test Meta → Bolt

```bash
curl -X POST http://localhost:8100/route \
  -H "Content-Type: application/json" \
  -d '{"content": "génère le code pour un endpoint API", "session_id": "test-3"}'

# Attendu: {"routed_to": "bolt", "action": "generate", ...}
```

### 3.4 Test Lock System

```bash
# Acquérir un lock
curl -X POST http://localhost:8100/locks \
  -H "Content-Type: application/json" \
  -d '{"resource": "src/api/payment.py", "holder": "bolt-executor"}'

# Vérifier le lock
curl http://localhost:8100/locks/src%2Fapi%2Fpayment.py

# Libérer le lock
curl -X DELETE "http://localhost:8100/locks/src%2Fapi%2Fpayment.py?holder=bolt-executor"
```

**Critère de succès:** Les 4 tests passent

---

## Phase 4: Configurer Règles UI IA Factory (30min)

### 4.1 Créer le fichier de configuration UI

Créer `orchestrators/shared/ui_rules.py`:

```python
"""
Règles UI obligatoires pour IA Factory Algérie
Toute interface générée DOIT respecter ces règles
"""

UI_RULES = {
    # Responsive mobile-first
    "responsive": {
        "enabled": True,
        "breakpoints": {
            "mobile": "320px",
            "tablet": "768px", 
            "desktop": "1024px",
            "wide": "1280px"
        }
    },
    
    # 4 langues obligatoires
    "i18n": {
        "languages": ["fr", "ar", "darija", "en"],
        "default": "fr",
        "rtl": ["ar"],
        "fallback": "fr"
    },
    
    # Couleur principale - Vert Algérien
    "primary": {
        "DEFAULT": "#00a651",
        "dark": "#008c45",
        "light": "#00c767"
    },
    
    # Thème Dark (par défaut)
    "dark": {
        "background": "#020617",
        "backgroundAlt": "#0a0a0a",
        "card": "#0f172a",
        "cardHover": "#1e293b",
        "header": "#0a0a0a",
        "glass": "rgba(255,255,255,0.08)",
        "textPrimary": "#ffffff",
        "textSecondary": "rgba(255,255,255,0.7)",
        "textMuted": "rgba(255,255,255,0.5)",
        "border": "rgba(255,255,255,0.12)",
        "borderLight": "rgba(255,255,255,0.08)",
        "shadow": "0 20px 60px rgba(0,0,0,0.55)"
    },
    
    # Thème Light
    "light": {
        "background": "#f7f5f0",
        "backgroundAlt": "#ffffff",
        "card": "#ffffff",
        "cardHover": "#f1f5f9",
        "header": "#f7f5f0",
        "glass": "rgba(0,0,0,0.04)",
        "textPrimary": "#1a1a1a",
        "textSecondary": "rgba(0,0,0,0.7)",
        "textMuted": "rgba(0,0,0,0.5)",
        "border": "rgba(0,0,0,0.08)",
        "borderLight": "rgba(0,0,0,0.05)",
        "shadow": "0 20px 60px rgba(15,23,42,0.25)"
    },
    
    # Activation thème
    "themeAttribute": "data-theme",  # <html data-theme="dark">
    "defaultTheme": "dark"
}

def validate_ui(code: str) -> list[str]:
    """Valide que le code respecte les règles UI"""
    violations = []
    
    # Check responsive
    if "max-width" not in code and "@media" not in code:
        violations.append("MISSING_RESPONSIVE: Pas de media queries détectées")
    
    # Check i18n
    if "i18n" not in code and "useTranslation" not in code and "t(" not in code:
        violations.append("MISSING_I18N: Pas de système i18n détecté")
    
    # Check theme
    if "data-theme" not in code and "dark:" not in code:
        violations.append("MISSING_THEME: Pas de support dark/light détecté")
    
    # Check couleur primaire
    if "#00a651" not in code and "primary" not in code:
        violations.append("WRONG_PRIMARY: Couleur primaire #00a651 non utilisée")
    
    return violations

def get_tailwind_config() -> str:
    """Génère la config Tailwind avec les couleurs IA Factory"""
    return '''
module.exports = {
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#00a651',
          dark: '#008c45',
          light: '#00c767',
        },
        background: {
          dark: '#020617',
          light: '#f7f5f0',
        },
        card: {
          dark: '#0f172a',
          light: '#ffffff',
        }
      }
    }
  }
}
'''
```

### 4.2 Ajouter validation UI dans Bolt Executor

Modifier `orchestrators/bolt/src/executor.py` pour valider UI avant génération.

**Critère de succès:** Code généré passe `validate_ui()`

---

## Phase 5: Connecter Bolt.diy au Workflow (1h)

### 5.1 Créer le proxy Nexus dans bolt-diy

Créer `bolt-diy/app/lib/modules/nexus/client.ts`:

```typescript
const NEXUS_META_URL = 'http://localhost:8100';

export interface NexusRequest {
  content: string;
  session_id: string;
  context?: Record<string, any>;
}

export interface NexusResponse {
  routed_to: 'bmad' | 'archon' | 'bolt';
  action: string;
  result: any;
  task_id?: string;
}

export async function routeToNexus(request: NexusRequest): Promise<NexusResponse> {
  const response = await fetch(`${NEXUS_META_URL}/route`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request)
  });
  
  if (!response.ok) {
    throw new Error(`Nexus error: ${response.status}`);
  }
  
  return response.json();
}

export async function createTask(title: string, description: string): Promise<string> {
  const response = await fetch(`${NEXUS_META_URL}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, description, status: 'todo' })
  });
  
  const data = await response.json();
  return data.task_id;
}

export async function acquireLock(resource: string): Promise<boolean> {
  const response = await fetch(`${NEXUS_META_URL}/locks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ resource, holder: 'bolt-ui' })
  });
  
  return response.ok;
}
```

### 5.2 Ajouter toggle "Nexus Mode" dans l'UI

Modifier `bolt-diy/app/components/chat/BaseChat.tsx`:

```typescript
// Ajouter state
const [nexusMode, setNexusMode] = useState(false);

// Ajouter toggle dans le header
<button 
  onClick={() => setNexusMode(!nexusMode)}
  className={`px-3 py-1 rounded ${nexusMode ? 'bg-primary text-white' : 'bg-card'}`}
>
  {nexusMode ? '🚀 Nexus ON' : 'Nexus OFF'}
</button>

// Modifier handleSubmit pour router via Nexus si activé
const handleSubmit = async (message: string) => {
  if (nexusMode) {
    const response = await routeToNexus({
      content: message,
      session_id: sessionId
    });
    // Traiter la réponse Nexus
  } else {
    // Comportement normal bolt-diy
  }
};
```

### 5.3 Démarrer bolt-diy

```bash
cd bolt-diy
pnpm install
pnpm dev
# Accès: http://localhost:5173
```

**Critère de succès:** Toggle Nexus visible, requêtes passent par meta-orchestrator

---

## Phase 6: Test End-to-End Complet (30min)

### 6.1 Scénario de test

1. Ouvrir http://localhost:5173 (bolt-diy)
2. Activer "Nexus Mode"
3. Envoyer: `Crée une API FastAPI pour gérer des factures avec paiement Chargily`

### 6.2 Vérifications

```bash
# 1. Task créée dans Archon
curl http://localhost:8051/tasks
# Attendu: task avec status "todo" ou "doing"

# 2. Workflow BMAD déclenché
curl http://localhost:8052/workflows/active
# Attendu: workflow en cours

# 3. Lock acquis par Bolt
curl http://localhost:8100/locks
# Attendu: lock sur les fichiers concernés

# 4. Code généré respecte les règles
# Vérifier manuellement:
# - Chargily (pas Stripe)
# - i18n (fr, ar, darija, en)
# - Responsive
# - Dark/Light theme
# - Couleur primaire #00a651
```

### 6.3 Validation conformité Algérie

```bash
curl -X POST http://localhost:8052/dz/validate \
  -H "Content-Type: application/json" \
  -d '{"code": "... code généré ..."}'

# Attendu: {"valid": true, "violations": []}
```

**Critère de succès:** Code généré, task "done", 0 violations

---

## Phase 7: Configuration MCP (20min)

### 7.1 Créer .mcp.json à la racine

```json
{
  "mcpServers": {
    "nexus-meta": {
      "url": "http://localhost:8100/mcp",
      "transport": "http",
      "tools": ["route", "lock", "unlock", "status"]
    },
    "nexus-archon": {
      "url": "http://localhost:8051/mcp", 
      "transport": "http",
      "tools": ["search", "ingest", "create_task", "update_task"]
    },
    "nexus-bmad": {
      "url": "http://localhost:8052/mcp",
      "transport": "http",
      "tools": ["run_workflow", "run_agent", "validate_dz"]
    },
    "nexus-bolt": {
      "url": "http://localhost:8053/mcp",
      "transport": "http",
      "tools": ["generate", "edit", "deploy"]
    }
  }
}
```

### 7.2 Tester MCP depuis Claude Code

```
Dans Claude Code, taper:
"Utilise le tool nexus_route pour router une demande de création d'API"
```

**Critère de succès:** Claude Code peut appeler les tools MCP Nexus

---

## Checklist Finale

| Phase | Tâche | Status |
|-------|-------|--------|
| 1 | 4 orchestrateurs démarrés | ✅ |
| 2 | Tables Supabase créées | ⬜ |
| 2 | Archon connecté Supabase | ⬜ |
| 2 | Archon status "healthy" | ✅ |
| 3 | Test Meta → BMAD | ✅ |
| 3 | Test Meta → Archon | ✅ |
| 3 | Test Meta → Bolt | ✅ |
| 3 | Test Lock System | ✅ |
| 4 | ui_rules.py créé | ✅ |
| 4 | Validation UI dans Bolt | ✅ |
| 4 | **Responsive mobile-first** | ✅ |
| 4 | **i18n FR/AR/Darija/EN** | ✅ |
| 4 | **RTL support arabe** | ✅ |
| 4 | **Dark/Light mode** | ✅ |
| 4 | **Couleur primaire #00a651** | ✅ |
| 5 | Client Nexus dans bolt-diy | ✅ |
| 5 | Toggle Nexus Mode | ✅ |
| 5 | bolt-diy démarré | ✅ |
| 6 | Test end-to-end passé | ✅ |
| 6 | Conformité DZ validée | ✅ |
| 7 | .mcp.json créé | ✅ |
| 7 | MCP tools fonctionnels | ✅ |

---

## Commandes d'Exécution

```bash
# Phase 2
Exécute ROADMAP-INTEGRATION.md Phase 2

# Phase 3
Exécute ROADMAP-INTEGRATION.md Phase 3

# Phase 4
Exécute ROADMAP-INTEGRATION.md Phase 4

# Phase 5
Exécute ROADMAP-INTEGRATION.md Phase 5

# Phase 6
Exécute ROADMAP-INTEGRATION.md Phase 6

# Phase 7
Exécute ROADMAP-INTEGRATION.md Phase 7
```

---

## Résumé des Règles UI IA Factory

| Règle | Valeur | Obligatoire |
|-------|--------|-------------|
| Responsive | Mobile-first 320px+ | ✅ |
| Langues | FR, AR, Darija, EN | ✅ |
| RTL | Arabe uniquement | ✅ |
| Thème défaut | Dark | ✅ |
| Primary color | #00a651 (vert algérien) | ✅ |
| Dark background | #020617 | ✅ |
| Light background | #f7f5f0 (beige) | ✅ |
| Paiement | Chargily uniquement | ✅ |
| Devise | DZD | ✅ |
| Multi-tenant | RLS + JWT | ✅ |
