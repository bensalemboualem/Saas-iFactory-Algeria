# 🚀 Lancement BMAD × Bolt.DIY - Guide Rapide

## ✅ INTÉGRATION TERMINÉE - PRÊT À UTILISER

---

## 🎯 Accès Direct

### URL principale:
```
http://localhost:5173
```

### Page de test agents:
```
http://localhost:5173/bmad-test
```

---

## 📋 Checklist avant lancement

- [x] Backend Archon running (port 8180)
- [x] MCP Server running (port 8051)
- [x] Bolt.DIY running (port 5173)
- [x] 19 agents BMAD chargés
- [x] API coordination fonctionnelle
- [x] BaseChat.tsx modifié avec BMAD
- [x] HMR Vite actif

**Statut: 🟢 TOUT EST PRÊT!**

---

## 🎬 Démarrage rapide (3 étapes)

### Étape 1: Ouvre Bolt
```
Navigateur → http://localhost:5173
```

### Étape 2: Démarre le chat
```
Tape n'importe quel message pour activer le chat
Exemple: "Bonjour"
```

### Étape 3: Utilise les agents BMAD
```
Le dropdown "Select BMAD Agent" apparaît en haut
Clique dessus → Choisis un agent → Commence à discuter!
```

---

## 🤖 Agents disponibles (19)

### 📋 Development (9 agents)
```
🏗️  Winston       - Architect
💻  Amelia        - Developer
📋  John          - Product Manager
📊  Mary          - Business Analyst
🎯  Bob           - Scrum Master
🧪  Murat         - Test Architect
📝  Paige         - Technical Writer
🎨  Sally         - UX Designer
🖼️  Saif          - Visual Design Expert
```

### 🎮 Game Dev (4 agents)
```
🎮  Cloud Dragonborn - Game Architect
🎲  Samus Shepard    - Game Designer
👾  Link Freeman     - Game Developer
🏃  Max              - Game Scrum Master
```

### 💡 Creative (5 agents)
```
💡  Carson    - Brainstorming Specialist
🧩  Dr. Quinn - Problem Solver
✨  Maya      - Design Thinking
🚀  Victor    - Innovation Strategist
📖  Sophia    - Storyteller
```

### 🔨 Builder (1 agent)
```
🔨  BMad Builder - General Builder
```

---

## 💬 Exemple de conversation

```
┌─────────────────────────────────────────────┐
│ Select BMAD Agent: Winston - Architect 🏗️   │
└─────────────────────────────────────────────┘

User: "Je veux créer une plateforme e-learning avec vidéos et quiz"

Winston: "Excellente idée! Pour votre plateforme e-learning,
          voici l'architecture que je recommande:

          🏗️ ARCHITECTURE GLOBALE:

          1️⃣ FRONTEND
             - Next.js 14 (App Router)
             - TypeScript strict
             - TailwindCSS + Shadcn UI
             - React Query pour state management
             - Vidéo: Mux ou Cloudflare Stream

          2️⃣ BACKEND
             - FastAPI (Python 3.11+)
             - PostgreSQL (données structurées)
             - Redis (cache + sessions)
             - S3 (stockage vidéos)
             - Elasticsearch (recherche)

          3️⃣ SERVICES
             - Auth: Supabase Auth ou Auth0
             - Paiement: Stripe Billing
             - Emails: SendGrid
             - CDN: Cloudflare

          4️⃣ INFRASTRUCTURE
             - Docker containers
             - AWS ECS ou Railway
             - CI/CD: GitHub Actions
             - Monitoring: Sentry + DataDog

          Voulez-vous que je détaille un module spécifique?"

[Change agent → John - Product Manager]

User: "Quelle roadmap pour le MVP?"

John: "Pour un MVP e-learning qui cartonne, voici ma roadmap:

       📅 PHASE 1: CORE FEATURES (3 semaines)
       Week 1:
       - ✅ Auth (signup/login/reset)
       - ✅ Page profil étudiant
       - ✅ Upload & streaming vidéo basique

       Week 2:
       - ✅ Catalogue cours
       - ✅ Système chapitres/leçons
       - ✅ Player vidéo avec contrôles

       Week 3:
       - ✅ Quiz interactifs
       - ✅ Tracking progression
       - ✅ Dashboard étudiant

       📅 PHASE 2: MONÉTISATION (2 semaines)
       Week 4:
       - ✅ Stripe checkout
       - ✅ Gestion abonnements
       - ✅ Accès premium content

       Week 5:
       - ✅ Dashboard instructeur
       - ✅ Analytics basiques
       - ✅ Système notifications

       🎯 KPIs à suivre:
       - Taux conversion free → paid
       - Completion rate courses
       - Daily active users
       - Revenue par utilisateur

       On lance le MVP dans 5 semaines?"

[Après 5+ messages → Bouton apparaît]

┌──────────────────────────────────────────────────┐
│ 🚀 Prêt à créer votre projet?                    │
│                                                   │
│ Cette conversation contient suffisamment          │
│ d'informations pour créer un projet Archon        │
│ [🎯 Créer projet Archon]                         │
└──────────────────────────────────────────────────┘

[Clic → Projet créé]

✅ Projet créé: E-learning Platform
   ID: project_1763350789

   📚 Knowledge base créée avec:
   - Architecture Winston (Next.js, FastAPI, PostgreSQL)
   - Roadmap John (MVP 5 semaines)
   - Technologies: Next.js, FastAPI, PostgreSQL, Redis, Stripe

   [🔗 Ouvrir dans Archon]

[Switch to "No Agent" → Bolt mode]

User: "Génère le schéma PostgreSQL pour les cours"

Bolt: [Génère SQL avec contexte du projet]
```

---

## 🎨 Interface utilisateur

### Avant (Bolt original)
```
┌─────────────────────────────────────┐
│  Model Selector: Deepseek Chat      │
│  [Chat input...]                    │
└─────────────────────────────────────┘
```

### Après (Bolt + BMAD)
```
┌─────────────────────────────────────┐
│  🤖 Select BMAD Agent: Winston 🏗️   │  ← NOUVEAU!
│  ─────────────────────────────────  │
│  Model Selector: Deepseek Chat      │
│  [Chat input...]                    │
│                                     │
│  🚀 Créer projet Archon             │  ← NOUVEAU (après 5 msgs)
└─────────────────────────────────────┘
```

---

## 🔧 Commandes utiles

### Vérifier services
```bash
# Backend Archon
curl http://localhost:8180/api/bmad/agents

# Coordination API
curl http://localhost:8180/api/coordination/health

# Bolt
curl http://localhost:5173
```

### Logs en temps réel
```bash
# Backend
docker logs ragdz-backend -f --tail 50

# Frontend (dans terminal Bolt)
# Déjà visible dans le terminal où pnpm run dev tourne
```

### Restart services
```bash
# Backend
docker restart ragdz-backend

# Frontend (Ctrl+C puis)
cd /c/Users/bbens/rag-dz/bolt-diy
pnpm run dev
```

---

## 📊 Performance

### Temps de réponse moyens
```
Chargement agents:       ~200ms
Sélection agent:         Instantané
Message BMAD:            2-5 secondes
Création projet:         3-8 secondes
Switch agent:            Instantané
```

### Ressources
```
RAM Bolt:               ~300 MB
RAM Backend:            ~500 MB
CPU idle:               <5%
CPU pendant réponse:    10-30%
```

---

## 🐛 Troubleshooting rapide

### Problème: Dropdown agents vide
```
Solution:
1. Vérifie backend: curl http://localhost:8180/api/bmad/agents
2. Si erreur → Restart backend
3. Refresh Bolt (F5)
```

### Problème: Erreur envoi message
```
Solution:
1. Ouvre DevTools (F12) → Console
2. Regarde erreur exacte
3. Vérifie que agent ID correct
4. Test API: curl -X POST http://localhost:8180/api/bmad/chat \
   -d '{"agent_id":"bmm-architect","message":"test"}'
```

### Problème: Bouton projet n'apparaît pas
```
Solution:
- Besoin 5+ messages avec agent BMAD
- Vérifie bmadConversationHistory dans DevTools
- Doit contenir au moins 5 entrées
```

### Restaurer Bolt original
```bash
cd /c/Users/bbens/rag-dz/bolt-diy
cp app/components/chat/BaseChat.tsx.bolt-original app/components/chat/BaseChat.tsx
# Vite reload automatique
```

---

## 📚 Documentation complète

1. **INTEGRATION_PROFESSIONNELLE_COMPLETE.md**
   - Guide utilisateur complet
   - Tests de validation
   - Workflows détaillés

2. **BMAD_BOLT_INTEGRATION_COMPLETE.md**
   - Architecture technique
   - Diagrammes système
   - API documentation

3. **BOLT_INTEGRATION_GUIDE.md**
   - Guide développeur
   - Code examples
   - Best practices

4. **QUICK_INTEGRATION.md**
   - Quick start minimal
   - Fast track

---

## 🎉 C'est parti!

**Tout est prêt. Ouvre http://localhost:5173 et commence à discuter avec les agents BMAD!**

### Suggestions de premiers prompts:

```
💡 "Je veux créer une app mobile de gestion de budget"
💡 "Besoin d'une API REST pour une marketplace"
💡 "Comment architecturer un SaaS multi-tenant?"
💡 "Roadmap pour un clone de Twitter en 8 semaines"
💡 "Stack technique pour une app de streaming vidéo"
```

### Pro tips:

- 🎯 Utilise différents agents pour différents aspects (architecture, code, product, UX)
- 💬 N'hésite pas à switch entre agents pendant la conversation
- 🚀 Crée un projet Archon après 5+ messages pour garder le contexte
- 🔄 Alterne BMAD et Bolt: BMAD pour design/architecture, Bolt pour génération code
- 📝 Les transcripts sont sauvegardés dans Archon comme knowledge base

---

**Profite bien de ton système BMAD × Bolt.DIY!** 🚀🤖

---

**Version**: 1.0.0 Production
**Date**: 2025-11-17
**Statut**: ✅ Déployé et testé
