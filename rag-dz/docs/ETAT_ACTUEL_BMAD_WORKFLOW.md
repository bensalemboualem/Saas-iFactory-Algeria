# 📊 État Actuel - Workflow BMAD dans RAG.dz

**Date**: 2025-01-19
**Status**: ✅ **PARTIELLEMENT FONCTIONNEL**

---

## ✅ CE QUI EXISTE ET FONCTIONNE

### 1. **Agents BMAD** (21 agents) ✅

**Localisation**: `bmad/src/`

#### Core Agents (2)
1. 🧙 **bmad-master** - Master Executor
2. 🔨 **bmad-builder** - Builder Agent

#### Module BMM - Méthode BMAD (9)
3. 📊 **analyst** (Mary) - Business Analyst
4. 🏗️ **architect** (Winston) - System Architect
5. 💻 **dev** (Amelia) - Developer
6. 🖼️ **frame-expert** (Saif) - Framework Expert
7. 📋 **pm** (John) - Project Manager
8. 🎯 **sm** (Bob) - Scrum Master
9. 🧪 **tea** (Murat) - Technical Excellence Advocate
10. 📝 **tech-writer** (Paige) - Technical Writer
11. 🎨 **ux-designer** (Sally) - UX Designer

#### Module BMGD - Game Development (4)
12. 🎮 **game-architect** (Cloud Dragonborn)
13. 🎲 **game-designer** (Samus Shepard)
14. 👾 **game-dev** (Link Freeman)
15. 🏃 **game-scrum-master** (Max)

#### Module CIS - Creative Innovation (5)
16. 💡 **brainstorming-coach** (Carson)
17. 🧩 **creative-problem-solver** (Dr. Quinn)
18. ✨ **design-thinking-coach** (Maya)
19. 🚀 **innovation-strategist** (Victor)
20. 📖 **storyteller** (Sophia)

#### Module Orchestrator (1)
21. 🎯 **orchestrator** - Super Orchestrateur

**Tous les fichiers YAML sont présents** dans `bmad/src/modules/`

---

### 2. **Backend API BMAD** (Port 8180) ✅

**Routes fonctionnelles**:

#### GET `/api/bmad/agents`
Retourne la liste des 20 agents (bmad-master manquant dans l'API)

**Test réussi**:
```bash
curl http://localhost:8180/api/bmad/agents
# Retourne: 20 agents avec id, name, description, category, icon
```

#### POST `/api/bmad/chat`
Envoie un message à un agent spécifique

**Format**:
```json
{
  "agent_id": "bmm-architect",
  "messages": [
    {"role": "user", "content": "Message"}
  ]
}
```

#### POST `/api/coordination/analyze-conversation`
Analyse une conversation pour détecter si c'est un projet

#### POST `/api/coordination/create-project`
Crée un projet Archon depuis une conversation BMAD

**Fichiers backend**:
- `backend/rag-compat/app/routers/bmad.py` ✅
- `backend/rag-compat/app/services/bmad_orchestrator.py` ✅

---

### 3. **Frontend Bolt.DIY Integration** ✅

**Fichiers d'intégration**:

#### `bolt-diy/app/lib/bmad-client.ts` ✅
Client TypeScript pour communiquer avec l'API BMAD:
- `fetchBMADAgents()` - Récupère liste agents
- `sendMessageToBMADAgent()` - Envoie message à un agent
- `analyzeConversation()` - Analyse conversation
- `createProjectFromConversation()` - Crée projet Archon

#### `bolt-diy/app/components/chat/AgentSelector.tsx` ✅
Composant dropdown pour sélectionner un agent BMAD:
- Affiche les 20 agents avec icônes
- Catégories colorées (development, creative, game-dev, builder)
- Intégré dans BaseChat

#### `bolt-diy/app/components/chat/BaseChat.tsx` ✅
Chat principal avec intégration BMAD (ligne 40, 483):
```tsx
import { AgentSelector } from './AgentSelector';
// ...
<AgentSelector
  selectedAgent={selectedBMADAgent}
  onAgentSelect={setSelectedBMADAgent}
/>
```

#### `bolt-diy/.env.local` ✅
Configuration des URLs BMAD:
```env
VITE_BMAD_AGENTS_URL=http://localhost:8180/api/bmad/agents
VITE_BMAD_CHAT_URL=http://localhost:8180/api/bmad/chat
VITE_COORDINATION_URL=http://localhost:8180/api/coordination
```

---

### 4. **Services Docker** ✅

Tous les services sont UP:
```
✅ ragdz-backend       (port 8180) - API BMAD
✅ ragdz-bolt-diy      (port 5174) - Bolt avec agents
✅ ragdz-frontend      (port 3737) - Archon UI
✅ ragdz-postgres      (port 5432) - Base de données
✅ ragdz-qdrant        (port 6333) - Vector DB
✅ ragdz-redis         (port 6379) - Cache
```

---

## 🎯 WORKFLOW ACTUEL (Ce qui devrait fonctionner)

### User Journey dans Bolt.DIY

```
1. User ouvre Bolt.DIY (http://localhost:5174)
2. Dans le chat, User voit le dropdown "Select BMAD Agent"
3. User sélectionne un agent (ex: Winston - Architect)
4. User tape son message dans le chat
5. Message envoyé à http://localhost:8180/api/bmad/chat
6. Backend exécute l'agent BMAD et retourne la réponse
7. Réponse affichée dans le chat Bolt
8. Conversation continue avec l'agent sélectionné
```

### Création Projet Archon

```
9. Après plusieurs messages, système détecte un projet
10. Bouton "Create Archon Project" apparaît
11. User clique → Appel à /api/coordination/create-project
12. Projet créé dans PostgreSQL (tables Archon)
13. URL Archon retournée: http://localhost:3737/projects/{id}
14. User peut consulter le projet dans Archon
```

---

## ❌ CE QUI MANQUE

### 1. **BMAD-Master dans l'API** ❌
L'agent `bmad-master` existe dans `bmad/src/core/agents/` mais n'est pas retourné par l'API `/api/bmad/agents`.

**Solution**: Ajouter dans `backend/rag-compat/app/services/bmad_orchestrator.py`

### 2. **Installation BMAD Method** ❌
Le package BMAD n'est pas installé:
```bash
cd bmad && npm install
# Error: Cannot find module 'xml2js'
```

**Solution**: Installer les dépendances BMAD

### 3. **Exécution Réelle des Agents** ❓
Les agents BMAD sont-ils exécutés via:
- Claude Code API?
- Claude API directe?
- Un runner BMAD local?

**À clarifier**: Mécanisme d'exécution des agents YAML

### 4. **Interface Archon pour Agents** ❌
Archon (port 3737) devrait afficher:
- Les 21 agents avec chat individuel
- Historique des conversations par agent
- Projets créés par orchestration

**Actuellement**: Archon UI est vide (pas d'agents affichés)

### 5. **Orchestration Multi-Agents** ❓
Le workflow multi-agents séquentiel:
```
Architect → PM → Backend Dev → Frontend Dev → DevOps → QA
```

**À implémenter**: Service d'orchestration qui appelle les agents dans l'ordre

---

## 🔧 POINTS À VÉRIFIER

### Test 1: AgentSelector visible dans Bolt ❓
```bash
# Ouvrir http://localhost:5174
# Vérifier si dropdown "Select BMAD Agent" est visible
# Vérifier si 20 agents apparaissent
```

### Test 2: Communication Bolt → Backend BMAD ❓
```bash
# Sélectionner agent "Winston - Architect"
# Taper "Hello"
# Vérifier logs backend:
docker logs ragdz-backend --tail 20 -f
# Doit afficher: POST /api/bmad/chat
```

### Test 3: Création Projet Archon ❓
```bash
# Faire une conversation multi-agents
# Cliquer "Create Archon Project"
# Vérifier dans PostgreSQL:
docker exec -i ragdz-postgres psql -U postgres -d ragdz_db -c \
  "SELECT * FROM archon_projects;"
```

---

## 📋 QUESTIONS CRITIQUES À RÉPONDRE

1. **Comment les agents BMAD sont-ils exécutés?**
   - Via Claude Code?
   - Via Claude API directe?
   - Via un runner BMAD?

2. **Où est le prompt des agents?**
   - Dans les fichiers `.agent.yaml`?
   - Dans le code backend?
   - Généré dynamiquement?

3. **Comment fonctionne l'orchestration?**
   - Séquentielle (1 agent après l'autre)?
   - Parallèle (tous en même temps)?
   - Hybride?

4. **Archon doit-il afficher les agents?**
   - Oui, avec chat individuel?
   - Non, juste les projets?

5. **Quel est le rôle exact de l'Orchestrator?**
   - Coordonner les agents?
   - Synthétiser les résultats?
   - Créer les projets Archon?

---

## 🚀 PROCHAINES ÉTAPES RECOMMANDÉES

### Étape 1: Vérifier l'intégration Bolt → Backend
```bash
# Ouvrir Bolt
open http://localhost:5174

# Tester sélection agent et envoi message
# Vérifier logs en temps réel
docker logs ragdz-backend -f
```

### Étape 2: Installer BMAD Method
```bash
cd bmad
npm install
npm run bmad:status
```

### Étape 3: Tester un agent manuellement
```bash
# Test direct de l'API BMAD
curl -X POST http://localhost:8180/api/bmad/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "bmm-architect",
    "messages": [{"role": "user", "content": "Hello Winston"}]
  }'
```

### Étape 4: Implémenter Archon UI pour Agents
- Créer page `/agents` dans Archon
- Afficher les 21 agents avec chat individuel
- Connecter au backend BMAD

### Étape 5: Tester workflow complet
```
User dans Bolt
  → Sélectionne agent Winston
  → Décrit un projet e-commerce
  → Agent Winston analyse architecture
  → Sélectionne agent John (PM)
  → Agent John définit le plan
  → Etc.
  → Orchestrator synthétise
  → Projet créé dans Archon
  → Bolt génère le code
```

---

## 📊 POURCENTAGE DE COMPLÉTION

| Composant | Complétion | Status |
|-----------|-----------|--------|
| **Agents BMAD** | 100% | ✅ 21 agents présents |
| **Backend API** | 80% | ✅ Routes OK, ❌ Exécution agents |
| **Frontend Bolt** | 70% | ✅ UI OK, ❓ Fonctionnel? |
| **Archon UI** | 10% | ✅ Démarré, ❌ Pas d'agents |
| **Orchestration** | 50% | ✅ Code existe, ❓ Fonctionne? |
| **Workflow complet** | 40% | ❓ À tester end-to-end |

**TOTAL**: **~58% complet**

---

## 🎯 OBJECTIF FINAL

**Workflow complet Bolt → BMAD → Archon → Code**:

```
1. User dans Bolt.DIY chat
2. Sélectionne agents BMAD (Architect, PM, Dev, etc.)
3. Converse avec chaque agent
4. Agents travaillent et s'échangent contexte
5. Orchestrator synthétise tout
6. Projet auto-créé dans Archon avec base de données
7. Bolt reçoit instructions finales
8. Bolt génère code complet
9. User télécharge ZIP ou deploy
```

---

## 💡 RECOMMANDATION IMMÉDIATE

**Avant de continuer, il faut:**

1. ✅ Tester si AgentSelector est visible dans Bolt UI
2. ✅ Tester si l'envoi de message à un agent fonctionne
3. ✅ Vérifier comment les agents sont exécutés (logs backend)
4. ✅ Clarifier le mécanisme d'exécution des agents YAML

**Une fois clarifiés, on pourra:**
- Compléter l'orchestration multi-agents
- Implémenter Archon UI avec agents
- Tester workflow end-to-end

---

**Auteur**: Claude Code Assistant
**Version**: 1.0
**Date**: 2025-01-19
