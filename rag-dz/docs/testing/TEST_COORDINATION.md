# 🚀 Test du Système de Coordination BMAD → Archon → Bolt.DIY

## ✅ Nouveau système mis en place

### Architecture
```
Bolt.DIY Chat ──┐
                ├──> BMAD Agents (19 agents)
                │         │
                │         ▼
                │    Coordination API
                │         │
                │         ├──> Analyse conversation
                │         ├──> Création projet Archon
                │         ├──> Knowledge base depuis transcript
                │         └──> Lancement Bolt.DIY avec contexte
                │
                └──> Archon MCP (Port 8051)
                         │
                         └──> RAG Knowledge Base
```

## 🧪 Test Manual avec cURL

### 1. Test simple - Analyser une conversation

```bash
curl -X POST http://localhost:8180/api/coordination/analyze-conversation \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Je veux créer une application de chat en temps réel avec React et Node.js",
        "agent": "User"
      },
      {
        "role": "assistant",
        "content": "Excellente idée! Pour une app de chat temps réel, je recommande: 1) Frontend React avec TypeScript 2) Backend Node.js + Socket.io 3) Base de données MongoDB 4) Redis pour le cache",
        "agent": "Winston (Architect)"
      },
      {
        "role": "user",
        "content": "Ok parfait. Il faut aussi ajouter authentification JWT et stockage des messages",
        "agent": "User"
      }
    ],
    "agents_used": ["bmm-architect", "bmm-dev"],
    "auto_create_project": false
  }' | python -m json.tool
```

**Résultat attendu:**
- `is_project`: true
- `project_name`: "Chat" (ou similaire)
- `technologies`: ["react", "node", "mongodb", "redis"]
- `requirements`: Liste des exigences détectées

### 2. Test complet - Créer projet automatiquement

```bash
curl -X POST http://localhost:8180/api/coordination/create-project \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Je veux développer une plateforme e-commerce avec panier, paiement Stripe et gestion produits",
        "agent": "User"
      },
      {
        "role": "assistant",
        "content": "Pour votre plateforme e-commerce, voici l'\''architecture: 1) Frontend: React + TailwindCSS 2) Backend: FastAPI Python 3) Base: PostgreSQL 4) Paiement: Stripe API",
        "agent": "Winston"
      },
      {
        "role": "user",
        "content": "Besoin aussi de recherche produits performante et système de recommandations",
        "agent": "User"
      },
      {
        "role": "assistant",
        "content": "Pour la recherche, j'\''intègre Elasticsearch. Pour les recommandations, algorithme collaborative filtering avec Redis cache",
        "agent": "Amelia"
      }
    ],
    "agents_used": ["bmm-architect", "bmm-dev", "bmm-analyst"],
    "auto_create_project": true
  }' | python -m json.tool
```

**Résultat attendu:**
```json
{
  "success": true,
  "project_id": "project_1234567890",
  "knowledge_source_id": "source_project_1234567890",
  "bolt_url": "http://localhost:5173?project_id=project_1234567890&knowledge_source=source_project_1234567890",
  "archon_project_url": "http://localhost:8180/projects/project_1234567890",
  "analysis": {
    "is_project": true,
    "project_name": "E-commerce",
    "technologies": ["react", "python", "postgresql", "redis", "stripe"]
  }
}
```

### 3. Test finalisation - Générer commande Bolt

```bash
curl -X POST "http://localhost:8180/api/coordination/finalize-and-launch?project_id=project_123&knowledge_source_id=source_123" \
  | python -m json.tool
```

**Résultat:**
- `bolt_url`: URL directe pour Bolt.DIY
- `bolt_command`: Commande shell pour lancer
- `instructions`: Liste des étapes suivantes

## 📊 Workflow Complet Utilisateur

### Scénario: Créer une app depuis zéro avec BMAD → Bolt

1. **L'utilisateur ouvre Bolt.DIY**
   - URL: http://localhost:5173
   - Interface chat avec sélecteur d'agents BMAD

2. **Conversation avec agents BMAD**
   ```
   User: "Je veux créer une app de gestion de tâches collaborative"

   [Sélectionne Winston - Architect]
   Winston: "Parfait! Voici l'architecture que je propose..."

   [Sélectionne John - Product Manager]
   John: "Voici les features prioritaires et la roadmap..."

   [Sélectionne Amelia - Developer]
   Amelia: "Je commence par le backend FastAPI avec..."
   ```

3. **Détection automatique du projet**
   - Le système détecte qu'un projet se dessine
   - Proposition: "Voulez-vous créer un projet Archon depuis cette conversation?"

4. **Création automatique**
   - ✅ Projet créé dans Archon
   - ✅ Knowledge base peuplée avec transcript
   - ✅ Contexte technique extrait
   - ✅ URL Bolt.DIY générée avec contexte

5. **Lancement Bolt.DIY avec contexte**
   - Bolt s'ouvre avec le projet pré-configuré
   - Accès aux agents BMAD via MCP
   - Accès à la knowledge base Archon via RAG
   - Peut commencer à coder directement

## 🔧 Configuration Requise

### Variables d'environnement backend (.env)

```bash
# Coordination
ARCHON_API_URL=http://localhost:8180
BOLT_DIY_URL=http://localhost:5173

# DeepSeek pour agents BMAD
DEEPSEEK_API_KEY=sk-e2d7d214600946479856ffafbe1ce392

# Archon MCP
MCP_SERVER_URL=http://localhost:8051
```

## 🎯 Prochaines Étapes

### À implémenter dans Bolt.DIY:

1. **Sélecteur d'agents BMAD dans UI**
   ```tsx
   <AgentSelector
     agents={bmadAgents}
     onSelect={(agent) => setCurrentAgent(agent)}
   />
   ```

2. **Client MCP dans Bolt**
   ```typescript
   // Connexion MCP pour accès Archon
   const mcpClient = new MCPClient('http://localhost:8051');

   // Recherche RAG depuis chat
   const results = await mcpClient.call('archon:rag_search_knowledge_base', {
     query: userMessage
   });
   ```

3. **Intégration coordination API**
   ```typescript
   // Quand projet détecté, créer dans Archon
   const result = await fetch('/api/coordination/create-project', {
     method: 'POST',
     body: JSON.stringify({
       messages: conversationHistory,
       agents_used: usedAgents,
       auto_create_project: true
     })
   });
   ```

## 📝 Exemples de conversations qui créent un projet

### Exemple 1: Application mobile
```
User: "Je veux une app mobile pour suivi de fitness"
Agent: "React Native + Firebase + Stripe"
→ Projet créé: "Fitness Tracker"
→ Technologies: react-native, firebase, stripe
```

### Exemple 2: API backend
```
User: "Besoin d'une API REST pour gestion d'inventaire"
Agent: "FastAPI + PostgreSQL + Redis cache"
→ Projet créé: "Inventory API"
→ Technologies: python, fastapi, postgresql, redis
```

### Exemple 3: Dashboard analytics
```
User: "Dashboard temps réel pour analytics business"
Agent: "Next.js + Chart.js + WebSocket + TimescaleDB"
→ Projet créé: "Analytics Dashboard"
→ Technologies: nextjs, websocket, timescaledb
```

## 🚨 Notes importantes

- ✅ **Backend coordination**: Port 8180, route `/api/coordination/*`
- ✅ **MCP Archon**: Port 8051, outils disponibles
- ⏳ **Bolt.DIY**: À configurer avec client MCP
- ⏳ **UI sélection agents**: À ajouter dans Bolt
- ✅ **DeepSeek API**: Fonctionnel pour tous agents BMAD

## 📊 Monitoring

### Vérifier santé du système:

```bash
# Backend coordination
curl http://localhost:8180/api/coordination/health

# Agents BMAD
curl http://localhost:8180/api/bmad/agents | python -m json.tool

# Chat BMAD
curl http://localhost:8180/api/bmad/chat/health

# MCP Archon
curl http://localhost:8051/health
```

---

**🎉 Le système de coordination est prêt!**

Les agents BMAD peuvent maintenant créer automatiquement des projets Archon avec knowledge base, prêts à être développés dans Bolt.DIY.
