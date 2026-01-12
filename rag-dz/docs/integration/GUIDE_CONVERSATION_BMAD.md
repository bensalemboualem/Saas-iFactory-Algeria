# Guide: Converser avec les Agents BMAD

## 🎯 3 Méthodes pour Interagir avec BMAD

---

## Méthode 1: Via Claude Code (Slash Commands) ⭐ RECOMMANDÉ

### Installation
```bash
cd C:\Users\bbens\rag-dz\bmad
npx bmad-method@alpha install
```

L'installeur va créer des slash commands dans `.claude/commands/bmad/`

### Utilisation dans Claude Code

#### Charger un Agent
```
/bmad:bmm:agents:architect    → Charge Winston (Architect)
/bmad:bmm:agents:dev          → Charge le Developer
/bmad:bmm:agents:pm           → Charge le Product Manager
/bmad:bmm:agents:tea          → Charge le Test Architect
```

#### Exemple de Conversation
```
Utilisateur: /bmad:bmm:agents:architect

Claude: 👋 Salut! Je suis Winston, l'architecte système de ton équipe BMAD.

        Je suis là pour t'aider avec:
        🏗️  Architecture système et design technique
        ☁️  Infrastructure cloud et patterns distribués
        📊 Sélection de technologies et décisions techniques

        Voici ce que je peux faire pour toi:

        1. *workflow-status - Vérifier le statut du workflow
        2. *create-architecture - Créer une architecture scale-adaptive
        3. *validate-architecture - Valider un document d'architecture
        4. *implementation-readiness - Vérifier la readiness
        5. *party-mode - Collaboration multi-agents

        Qu'est-ce que tu veux qu'on fasse ensemble?

Utilisateur: Je veux créer l'architecture pour une application de chat en temps réel.

Winston: Excellent choix! 💬 Avant de plonger dans l'architecture, j'ai quelques
         questions pour m'assurer qu'on construit la bonne chose:

         1. **Échelle attendue**: Combien d'utilisateurs simultanés?
         2. **Features principales**: Audio/vidéo ou juste texte?
         3. **Contraintes**: Budget cloud, compliance, latence?

         [... conversation continue ...]
```

#### Lancer un Workflow Directement
```
/bmad:bmm:workflows:workflow-init    → Initialise le projet
/bmad:bmm:workflows:prd              → Crée un PRD
/bmad:bmm:workflows:architecture     → Génère l'architecture
/bmad:bmm:workflows:dev-story        → Développe une story
/bmad:bmm:workflows:code-review      → Revue de code
```

### Agents Disponibles

| Commande | Agent | Rôle |
|----------|-------|------|
| `/bmad:bmm:agents:architect` | Winston 🏗️ | Architecture système |
| `/bmad:bmm:agents:dev` | Developer 💻 | Implémentation code |
| `/bmad:bmm:agents:pm` | Product Manager 📋 | Gestion produit |
| `/bmad:bmm:agents:sm` | Scrum Master 🎯 | Agile, sprints |
| `/bmad:bmm:agents:tea` | Test Architect 🧪 | Stratégie de tests |
| `/bmad:bmm:agents:ux-designer` | UX Designer 🎨 | Design UX/UI |
| `/bmad:bmm:agents:analyst` | Analyst 📊 | Analyse business |
| `/bmad:bmm:agents:tech-writer` | Tech Writer 📝 | Documentation |
| `/bmad:cis:agents:ideator` | Ideator 💡 | Créativité |
| `/bmad:cis:agents:strategist` | Strategist 🎯 | Stratégie business |

---

## Méthode 2: Via l'Interface Web (Frontend Archon)

### Accès
**URL:** http://localhost:3737/bmad

### Utilisation

1. **Sélectionner un Agent**
   - Clique sur une carte d'agent (ex: BMM Architect 🏗️)
   - L'agent est mis en surbrillance

2. **Choisir un Workflow**
   - Clique sur "Execute" d'un workflow
   - Ex: "Workflow Init 🚀", "Code Review 🔍"

3. **Suivre l'Exécution**
   - Barre latérale droite montre les workflows actifs
   - Mise à jour en temps réel (polling 2s)
   - Status: queued → running → completed/failed

4. **Voir les Résultats**
   - Output s'affiche dans la carte d'exécution
   - Erreurs en rouge si échec

### Exemple d'Usage

```
1. Ouvrir http://localhost:3737/bmad

2. Cliquer sur "BMM Architect 🏗️"

3. Cliquer "Execute" sur "Workflow Init"

4. Observer dans la barre de droite:
   ┌─────────────────────────────────┐
   │ Active Workflows (1)            │
   ├─────────────────────────────────┤
   │ ⏳ Workflow Init                │
   │    bmm-architect                │
   │    Running...                   │
   │    11:30:45                     │
   └─────────────────────────────────┘

5. Quand terminé:
   ┌─────────────────────────────────┐
   │ ✅ Workflow Init                │
   │    bmm-architect                │
   │    11:31:02                     │
   │                                 │
   │ ✅ PRD created successfully     │
   │ 📄 ./bmad/prd.md               │
   └─────────────────────────────────┘
```

---

## Méthode 3: Via MCP Protocol (Archon MCP Server)

### Prérequis
1. Démarrer le serveur MCP Archon:
```bash
cd C:\Users\bbens\rag-dz\Archon\python
set ARCHON_MCP_PORT=8051
set ARCHON_API_URL=http://localhost:8180
python -m src.mcp_server.mcp_server
```

2. Configurer Claude Code (`.claude/claude_code_config.json`):
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

### Utilisation dans Claude Code

Claude Code aura accès à ces outils MCP:

```
Utilisateur: Liste les agents BMAD disponibles

Claude: [Appelle bmad_list_agents()]

        Voici les 8 agents BMAD disponibles:

        Development (5):
        🏗️  bmm-architect    - Architecture système
        💻 bmm-coder        - Implémentation code
        🧪 bmm-tester       - Tests et QA
        🐛 bmm-debugger     - Debug et résolution
        📝 bmm-documenter   - Documentation technique

        Builder (1):
        🔨 bmb-builder      - Création agents custom

        Creative (2):
        💡 cis-ideator      - Idéation créative
        🎯 cis-strategist   - Planification stratégique

---

Utilisateur: Lance le workflow workflow-init avec l'architecte

Claude: [Appelle bmad_execute_workflow(
          workflow_name="workflow-init",
          agent_id="bmm-architect",
          context_data='{}'
        )]

        ✅ Workflow lancé avec succès!

        📋 Workflow: workflow-init
        🏗️  Agent: BMM Architect (Winston)
        🆔 Execution ID: 7f3a9b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
        ⏱️  Status: queued

        Je surveille l'exécution...

---

Utilisateur: Quel est le statut du workflow?

Claude: [Appelle bmad_get_workflow_status(
          execution_id="7f3a9b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c"
        )]

        📊 Status actuel: running

        📤 Output partiel:
        ```
        🏗️  Winston (Architect) is analyzing your project...

        ✓ Project type identified: Web Application
        ✓ Technology stack detected: React + FastAPI
        ✓ Generating architecture recommendations...

        [En cours...]
        ```

---

Utilisateur: [Après 2 minutes]

Claude: [Appelle bmad_get_workflow_status(...)]

        ✅ Workflow terminé!

        📤 Résultat final:
        ```
        🏗️  Architecture Document Generated

        ✅ System architecture created
        ✅ Technology stack validated
        ✅ Scalability patterns defined
        ✅ Infrastructure requirements documented

        📄 Documents créés:
        - ./bmad/architecture.md (Architecture complète)
        - ./bmad/tech-decisions.md (Décisions techniques)
        - ./bmad/diagrams/ (Diagrammes C4)

        🎯 Next Steps:
        1. Review architecture document
        2. Run implementation-readiness workflow
        3. Start dev-story for first feature
        ```
```

### Outils MCP Disponibles

| Outil MCP | Description |
|-----------|-------------|
| `bmad_list_agents()` | Liste tous les agents |
| `bmad_list_workflows(agent?)` | Liste les workflows (filtrés par agent) |
| `bmad_execute_workflow(workflow, agent, context)` | Lance un workflow |
| `bmad_get_workflow_status(execution_id)` | Vérifie le statut |
| `bmad_cancel_workflow(execution_id)` | Annule un workflow |
| `bmad_get_active_workflows()` | Liste les workflows actifs |

---

## 🎭 Personnalités des Agents

### Winston (Architect) 🏗️
- **Style:** Pragmatique, balance idéalisme et réalité
- **Focus:** Scalabilité, patterns éprouvés, "boring tech"
- **Phrases typiques:**
  - "Let's design simple solutions that scale when needed"
  - "User journeys should drive technical decisions"
  - "I prefer boring technology that works"

### Developer 💻
- **Style:** Pratique, orienté code, aime les exemples
- **Focus:** Implémentation propre, patterns, refactoring
- **Phrases typiques:**
  - "Let me show you with code"
  - "Here's a cleaner approach"
  - "We can refactor this to make it more maintainable"

### Product Manager 📋
- **Style:** Business-oriented, user-centric
- **Focus:** Requirements, user stories, priorités
- **Phrases typiques:**
  - "What's the user value here?"
  - "Let's prioritize based on impact"
  - "How does this align with business goals?"

### Test Architect (TEA) 🧪
- **Style:** Méthodique, orienté qualité
- **Focus:** Couverture tests, stratégie QA
- **Phrases typiques:**
  - "Let's ensure we have proper test coverage"
  - "We need integration tests for this"
  - "What edge cases should we test?"

---

## 💡 Conseils d'Utilisation

### Quand Utiliser Chaque Méthode?

**Claude Code Slash Commands** ✅ Meilleur pour:
- Conversations interactives avec agents
- Ajustements en temps réel
- Workflows guidés avec questions/réponses
- Apprentissage initial de BMAD

**Interface Web Frontend** ✅ Meilleur pour:
- Visualisation de workflows actifs
- Monitoring de plusieurs workflows
- Démonstrations/présentations
- Overview rapide des agents

**MCP Protocol** ✅ Meilleur pour:
- Automatisation de workflows
- Intégration dans scripts
- Orchestration complexe multi-agents
- CI/CD pipelines

### Workflows Typiques

#### Nouveau Projet
```
1. /bmad:bmm:agents:pm
   → "Je veux créer une app mobile de fitness"
   → Génère PRD

2. /bmad:bmm:agents:architect
   → "Crée l'architecture pour ce PRD"
   → Génère architecture.md

3. /bmad:bmm:agents:dev
   → "Développe la feature d'authentification"
   → Code + tests
```

#### Debug d'un Bug
```
1. /bmad:bmm:agents:debugger
   → "L'auth échoue avec 401 sur /api/login"
   → Analyse le problème

2. Debugger propose des hypothèses
   → Vérifie les logs
   → Identifie la cause

3. /bmad:bmm:workflows:bug-fix
   → Fix + tests de régression
```

#### Refactoring
```
1. /bmad:bmm:agents:architect
   → "Notre monolithe est trop lent"
   → Propose architecture microservices

2. /bmad:bmm:agents:dev
   → "Refactor le module payment en microservice"
   → Code de migration

3. /bmad:bmm:agents:tea
   → "Crée les tests de migration"
   → Suite de tests complète
```

---

## 🚀 Quick Start

### Pour Commencer Maintenant

1. **Installer BMAD**
```bash
cd C:\Users\bbens\rag-dz\bmad
npx bmad-method@alpha install
```

2. **Dans Claude Code**
```
/bmad:bmm:agents:pm

Puis: "Je veux créer une app de [ton idée]"
```

3. **L'Agent PM va:**
   - Te poser des questions sur l'app
   - Créer un PRD complet
   - Te guider vers les prochaines étapes

4. **Suivre les Recommandations**
```
*workflow-status   → Pour voir où tu en es
*create-architecture   → Si prêt pour l'architecture
```

---

## 📚 Documentation Complète

- **BMAD README:** `bmad/README.md`
- **Guides Workflows:** `bmad/src/modules/bmm/docs/`
- **Configuration Agents:** `bmad/_cfg/agents/`
- **Exemples:** `bmad/examples/`

---

## 🆘 Troubleshooting

### Agent ne répond pas
```bash
# Vérifier installation
ls .claude/commands/bmad/

# Réinstaller si nécessaire
cd bmad
npx bmad-method@alpha install
```

### Workflow échoue
```bash
# Vérifier logs backend
docker logs ragdz-backend

# Vérifier BMAD path
ls C:\Users\bbens\rag-dz\bmad
```

### MCP ne connecte pas
```bash
# Vérifier serveur MCP
curl http://localhost:8051/health

# Redémarrer si nécessaire
cd Archon/python
python -m src.mcp_server.mcp_server
```

---

**Prêt à converser avec les agents BMAD! 🚀**

Commence par `/bmad:bmm:agents:pm` dans Claude Code et dis-lui ce que tu veux créer!
