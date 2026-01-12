# 📖 Guide d'Utilisation - Agents BMAD dans Bolt

**Date**: 2025-01-20
**Version**: 1.0

---

## 🎯 Comment utiliser les Agents BMAD

### Étape 1: Ouvrir Bolt.DIY

Ouvre dans ton navigateur:
```
http://localhost:5174
```

Tu verras la landing page avec **3 boutons**:
- 🔥 **BMAD Agents** (ouvre la liste JSON des agents)
- 🤖 **Archon UI** (ouvre Archon sur port 3737)
- 💾 **RAG.dz** (ouvre RAG UI sur port 5173)

---

### Étape 2: Configurer le Provider AI de Bolt

**IMPORTANT**: Avant de sélectionner un agent BMAD, configure d'abord le provider AI de Bolt.

#### Option A: Claude (Anthropic) - Recommandé ✅

1. Clique sur l'icône **Settings** (⚙️) dans le menu latéral gauche
2. Dans "**AI Provider**", sélectionne **Anthropic**
3. Dans "**Model**", sélectionne **Claude 3.5 Sonnet**
4. La clé API est déjà configurée dans `.env.local`
5. Ferme les settings

#### Option B: OpenAI (GPT-4o)

1. Settings → Provider: **OpenAI**
2. Model: **gpt-4o-mini** ou **gpt-4o**
3. Clé déjà configurée

#### Option C: Groq (Ultra rapide)

1. Settings → Provider: **Groq**
2. Model: **llama-3.3-70b-versatile**
3. Clé déjà configurée

**⚠️ NE PAS sélectionner "Deepseek" comme provider Bolt**
- Deepseek est utilisé par le **backend** pour les agents BMAD
- Si tu sélectionnes Deepseek dans Bolt, il va essayer de se connecter directement
- Cela crée un conflit

---

### Étape 3: Démarrer une Conversation

1. Clique dans la zone de chat
2. Tape un premier message, par exemple:
   ```
   Bonjour!
   ```
3. Envoie le message

**Le dropdown "Select BMAD Agent" va apparaître** ✅

---

### Étape 4: Sélectionner un Agent BMAD

1. Clique sur le dropdown **"🎯 Select BMAD Agent"**
2. Tu verras la liste des 20 agents disponibles:

#### Agents Développement (BMM)
- 🏗️ **Winston** - Architect
- 📋 **John** - Product Manager
- 💻 **Amelia** - Developer
- 🧪 **Murat** - Test Architect
- 📝 **Paige** - Technical Writer
- 📊 **Mary** - Business Analyst
- 🎯 **Bob** - Scrum Master
- 🎨 **Sally** - UX Designer
- 🖼️ **Saif** - Framework Expert

#### Agents Créatifs (CIS)
- 💡 **Carson** - Brainstorming Coach
- 🧩 **Dr. Quinn** - Problem Solver
- ✨ **Maya** - Design Thinking Coach
- 🚀 **Victor** - Innovation Strategist
- 📖 **Sophia** - Storyteller

#### Agents Game Dev (BMGD)
- 🎮 **Cloud Dragonborn** - Game Architect
- 🎲 **Samus Shepard** - Game Designer
- 👾 **Link Freeman** - Game Developer
- 🏃 **Max** - Game Scrum Master

#### Autres
- 🔨 **BMad Builder**
- 🎯 **Orchestrator**

3. Clique sur l'agent de ton choix (par exemple **Winston - Architect**)

---

### Étape 5: Converser avec l'Agent

1. L'agent sélectionné est maintenant actif
2. Tape ton message dans le chat:
   ```
   Je veux créer une application e-commerce moderne avec React et FastAPI
   ```
3. Envoie le message

**Ce qui se passe**:
- Message envoyé à `http://localhost:8180/api/bmad/chat`
- Backend charge la personnalité de Winston depuis le fichier YAML
- Backend appelle DeepSeek API avec la personnalité
- Winston répond en français avec son expertise

**Exemple de réponse de Winston**:
```
Bonjour ! Je suis Winston, architecte système senior spécialisé
dans les systèmes distribués, l'infrastructure cloud et la
conception d'API.

Pour votre application e-commerce avec React et FastAPI,
je recommande une architecture en 3 couches:

1. **Frontend React**
   - Next.js pour SSR et SEO
   - TailwindCSS pour le design
   - React Query pour state management

2. **Backend FastAPI**
   - API REST avec authentification JWT
   - PostgreSQL pour la base de données
   - Redis pour le caching

3. **Infrastructure**
   - Docker + Docker Compose
   - Nginx comme reverse proxy
   - CI/CD avec GitHub Actions

Que souhaitez-vous approfondir en premier?
```

---

### Étape 6: Workflow Multi-Agents

Tu peux changer d'agent en cours de conversation:

1. **Winston (Architect)** → Définit l'architecture globale
2. Change pour **John (PM)** → Définit le plan produit et roadmap
3. Change pour **Amelia (Dev)** → Implémente les features
4. Change pour **Murat (TEA)** → Crée la stratégie de tests
5. Change pour **Paige (Tech Writer)** → Documente le projet

**Historique conservé**: Tous les messages sont sauvegardés et accessibles à tous les agents.

---

### Étape 7: Créer un Projet Archon

Après **5+ messages** dans une conversation BMAD, un bouton apparaît:

```
🚀 Create Archon Project
```

1. Clique sur ce bouton
2. Le système analyse la conversation
3. Crée automatiquement un projet dans Archon
4. Stocke dans PostgreSQL:
   - Knowledge source (base de conversation)
   - Projet Archon avec métadonnées
   - Documents de chaque agent
5. Tu reçois un lien:
   ```
   ✅ Projet créé: http://localhost:3737/projects/{id}
   ```

---

## 🔧 Résolution de Problèmes

### Problème 1: "Authentication Error with Deepseek"

**Cause**: Tu as sélectionné "Deepseek" comme provider dans Bolt

**Solution**:
1. Ouvre Settings (⚙️)
2. Change provider pour **Anthropic** (Claude)
3. Sélectionne model **Claude 3.5 Sonnet**
4. Rafraîchis la page

---

### Problème 2: Dropdown "Select BMAD Agent" n'apparaît pas

**Cause**: Tu n'as pas encore envoyé de message

**Solution**:
1. Tape un message dans le chat (n'importe quoi)
2. Envoie-le
3. Le dropdown apparaît maintenant

---

### Problème 3: Agent ne répond pas

**Vérifications**:

1. **Backend up?**
   ```bash
   curl http://localhost:8180/api/bmad/chat/health
   ```
   Doit retourner: `"status": "healthy"`

2. **Logs backend**:
   ```bash
   docker logs ragdz-backend -f
   ```
   Cherche des erreurs

3. **Logs frontend**:
   ```bash
   docker logs ragdz-bolt-diy -f
   ```

4. **Console navigateur**:
   - F12 → Console
   - Cherche des erreurs réseau

---

### Problème 4: "Failed to fetch BMAD agents"

**Cause**: Backend pas accessible depuis frontend

**Solution**:
1. Vérifie que backend tourne:
   ```bash
   docker ps | grep backend
   ```

2. Teste l'API directement:
   ```bash
   curl http://localhost:8180/api/bmad/agents
   ```

3. Vérifie `.env.local` dans bolt-diy:
   ```env
   VITE_BMAD_AGENTS_URL=http://localhost:8180/api/bmad/agents
   VITE_BMAD_CHAT_URL=http://localhost:8180/api/bmad/chat
   ```

---

## 📊 Architecture du Système

```
┌─────────────────────────────────────────┐
│          Bolt.DIY (Port 5174)           │
│  - Landing page avec 3 boutons          │
│  - Chat avec AgentSelector dropdown     │
│  - Provider AI: Claude/OpenAI/Groq      │
└─────────────┬───────────────────────────┘
              │
              │ User sélectionne agent BMAD
              │
              ▼
┌─────────────────────────────────────────┐
│    POST /api/bmad/chat (Port 8180)      │
│  - Charge personnalité depuis YAML      │
│  - Appelle DeepSeek API                 │
│  - Retourne réponse en français         │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│         DeepSeek API (Cloud)            │
│  - Model: deepseek-chat                 │
│  - Génère réponse avec personnalité     │
└─────────────────────────────────────────┘
```

---

## 🎯 Exemples de Conversations

### Exemple 1: Architecture d'App

**User** → **Winston (Architect)**
```
Je veux créer une plateforme de streaming vidéo comme YouTube
```

**Winston répond**:
```
Excellent projet ! Pour une plateforme de streaming vidéo,
voici mon analyse architecturale:

1. **Frontend**
   - React avec Next.js
   - Video.js ou HLS.js pour le player
   - CDN (Cloudflare) pour delivery

2. **Backend**
   - Microservices avec FastAPI
   - Service Upload (gestion des vidéos)
   - Service Transcoding (FFmpeg)
   - Service Streaming (HLS/DASH)

3. **Storage**
   - S3 (AWS/MinIO) pour vidéos
   - PostgreSQL pour métadonnées
   - Redis pour cache + sessions

4. **Infrastructure**
   - Kubernetes pour orchestration
   - Message queue (RabbitMQ) pour jobs async
   - Monitoring (Prometheus + Grafana)

Budget estimé mensuel: $500-2000 selon trafic

Questions pour affiner:
- Audience cible (trafic attendu)?
- Besoin de modération de contenu?
- Monétisation prévue?
```

---

### Exemple 2: Plan Produit

**User** → **John (PM)**
```
Je veux lancer un SaaS de gestion de projets pour PME
```

**John répond**:
```
Super idée ! En tant que PM, voici mon analyse produit:

**1. Marché & Positionnement**
- Concurrents: Asana, Trello, Monday.com
- Niche: PME françaises/algériennes (trilingue)
- Différenciation: Simplicité + Prix compétitif

**2. MVP Features**
- Projets & Tasks
- Kanban board
- Calendrier
- Collaboration (commentaires)
- Notifications
- Export PDF

**3. Roadmap 6 mois**
- M1-M2: MVP (fonctionnalités core)
- M3: Intégrations (Slack, Email)
- M4-M5: Mobile apps (iOS/Android)
- M6: Analytics & Reporting

**4. Métriques clés**
- 100 signups beta (M1-M2)
- 20% conversion free → paid (M3)
- 1000 MAU (M6)

Budget R&D estimé: 60-80k€ pour 6 mois

Quel aspect voulez-vous approfondir?
```

---

## 🚀 Astuces Pro

### 1. Changer d'Agent en Cours de Route

Tu peux changer d'agent à tout moment:
- Winston termine l'architecture
- → Change pour **Amelia (Dev)**
- Amelia voit tout l'historique et continue sur le code

### 2. Combiner Plusieurs Experts

Pour un projet complet:
1. **Mary (Analyst)** → Analyse métier
2. **Winston (Architect)** → Architecture technique
3. **John (PM)** → Plan produit
4. **Sally (UX Designer)** → Design interface
5. **Amelia (Dev)** → Implémentation
6. **Murat (TEA)** → Tests
7. **Paige (Tech Writer)** → Documentation
8. **Bob (Scrum Master)** → Planification sprints

### 3. Utiliser l'Orchestrator

L'agent **Orchestrator** (🎯) peut coordonner plusieurs agents automatiquement.

---

**Bon développement avec les agents BMAD ! 🚀**

---

**Support**: Consulte `docs/WORKFLOW_BMAD_FONCTIONNEL.md` pour détails techniques
**Problèmes**: Vérifie `docker logs ragdz-backend` et `docker logs ragdz-bolt-diy`
