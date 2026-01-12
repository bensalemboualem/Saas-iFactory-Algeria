# AUDIT COMPLET IAFactory
## Plateforme SaaS Collaborative B2B

**Date:** 9 janvier 2026
**Auditeur:** Claude Code
**Version:** 1.0

---

# TABLE DES MATIÈRES

1. [Résumé Exécutif](#1-résumé-exécutif)
2. [Architecture Actuelle](#2-architecture-actuelle)
3. [Diagnostic des Bugs](#3-diagnostic-des-bugs)
4. [Architecture Chat Multi-Utilisateurs](#4-architecture-chat-multi-utilisateurs)
5. [Conformité RGPD & Stockage](#5-conformité-rgpd--stockage)
6. [Intégration Agents + Chat](#6-intégration-agents--chat)
7. [Optimisations & Best Practices](#7-optimisations--best-practices)
8. [Roadmap Technique](#8-roadmap-technique)

---

# 1. RÉSUMÉ EXÉCUTIF

## Vue d'Ensemble

IAFactory est un **écosystème SaaS complexe** composé de 4 applications majeures et 27+ micro-applications, intégrant Bolt.diy, Archon et BMAD.

### ✅ Points Forts
- Architecture microservices mature avec 40+ providers IA intégrés
- Multi-tenant avec RLS PostgreSQL
- Infrastructure WebSocket/SSE existante
- Système de crédits et billing complet
- BMAD, Archon et Bolt.diy déjà intégrés dans rag-dz
- Support multi-langue (FR, AR, Darija, EN)

### ❌ Points Critiques
- Complexité élevée (225+ variables d'environnement)
- Pas de chat multi-utilisateurs temps réel complet
- WebContainer potentiellement désactivé de manière non-propre
- Conformité RGPD non documentée
- Tests automatisés insuffisants

### 💡 Priorités Recommandées
1. **URGENT**: Fix bug IDE/WebContainer
2. **HIGH**: Implémenter chat multi-utilisateurs
3. **HIGH**: Conformité RGPD basique
4. **MEDIUM**: Toggle modes WebContainer
5. **MEDIUM**: Intégration agents @mention

---

# 2. ARCHITECTURE ACTUELLE

## 2.1 Cartographie des Projets

```
d:\IAFactory/
├── iafactory-academy/          # Plateforme e-learning (FastAPI + React)
├── iafactory-video-platform/   # Génération vidéo IA (FastAPI + Next.js)
├── iafactory-gateway/          # Gateway API multi-providers (Fastify + Prisma)
├── rag-dz/                     # Meta-orchestrateur IA Nexus (PRINCIPAL)
│   ├── apps/                   # 27+ applications
│   ├── bolt-diy/              # ★ Bolt.diy intégré
│   ├── bmad/                  # ★ BMAD Method intégré
│   ├── services/api/          # API FastAPI principale
│   └── infrastructure/        # Docker, n8n, monitoring
├── iafactory-chat-bolt/        # Interface chat alternative
├── onestschooled/              # Gestion scolaire (Laravel)
├── landing-*/                  # Landing pages
└── docker-compose/             # Configs multi-environnements
```

## 2.2 Diagramme ASCII de l'Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENTS                                       │
│   [Web Browser]    [Mobile]    [API Clients]                        │
└─────────┬───────────────┬───────────────┬───────────────────────────┘
          │               │               │
          ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   GATEWAY LAYER (port 3001)                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  iafactory-gateway (Fastify + Prisma)                       │   │
│  │  ├── Multi-Provider Routing (OpenAI-compatible)             │   │
│  │  ├── Credit Management                                       │   │
│  │  ├── Rate Limiting (Redis)                                   │   │
│  │  └── JWT Authentication                                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────┬───────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   API LAYER (FastAPI)                               │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐        │
│  │  RAG-DZ API    │  │  Academy API   │  │  Video API     │        │
│  │  (port 8100)   │  │  (port 8000)   │  │  (port 8001)   │        │
│  │                │  │                │  │                │        │
│  │  30+ routers:  │  │  - Courses     │  │  - Projects    │        │
│  │  - BigRAG      │  │  - Users       │  │  - Assets      │        │
│  │  - BMAD        │  │  - Payments    │  │  - Render      │        │
│  │  - Bolt        │  │  - Certs       │  │  - Publish     │        │
│  │  - Voice       │  │                │  │                │        │
│  │  - WebSocket   │  │                │  │                │        │
│  └────────────────┘  └────────────────┘  └────────────────┘        │
└─────────┬───────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   DATA LAYER                                        │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐       │
│  │ PostgreSQL │ │  Qdrant    │ │   Redis    │ │   MinIO    │       │
│  │ (5432/33)  │ │  (6333)    │ │  (6379)    │ │  (9000)    │       │
│  │            │ │            │ │            │ │            │       │
│  │ - Users    │ │ - Vectors  │ │ - Cache    │ │ - Objects  │       │
│  │ - Orgs     │ │ - RAG      │ │ - Sessions │ │ - Files    │       │
│  │ - Credits  │ │ - Search   │ │ - Queue    │ │ - Media    │       │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘       │
└─────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   AI/ML PROVIDERS (40+)                             │
│  LLMs: OpenAI, Anthropic, Groq, DeepSeek, Google, Mistral, Ollama  │
│  Images: DALL-E, Flux, SDXL, Leonardo, Ideogram                    │
│  Video: Runway, Pika, Luma, Kling                                  │
│  Audio: ElevenLabs, Suno, Udio, Whisper                            │
│  Avatars: HeyGen, D-ID, Synthesia                                  │
└─────────────────────────────────────────────────────────────────────┘
```

## 2.3 Stack Technique Détaillé

### Frontend
| Technologie | Version | Usage |
|-------------|---------|-------|
| React | 18.3 - 19.x | UI principale |
| Next.js | 14-15 | Video platform |
| Vite | 5-7 | Build & dev server |
| TypeScript | 5.3+ | Type safety |
| TailwindCSS | 3.4 | Styling |
| Zustand | 4.5 | State management |
| TanStack Query | 5.17 | Server state |
| Nanostores | latest | Bolt.diy stores |
| Framer Motion | 11 | Animations |

### Backend
| Technologie | Version | Usage |
|-------------|---------|-------|
| FastAPI | 0.109 | API REST principale |
| Fastify | 5.6 | Gateway Node.js |
| Pydantic | 2.5 | Validation Python |
| SQLAlchemy | 2.0 | ORM Python |
| Prisma | 5.22 | ORM Node.js |
| Uvicorn | 0.27 | ASGI server |
| Celery | latest | Task queue |

### Base de Données
| Technologie | Port | Usage |
|-------------|------|-------|
| PostgreSQL | 5432/5433 | BD principale |
| Qdrant | 6333 | Vector search |
| Redis | 6379/6380 | Cache & queues |
| Meilisearch | 7700 | Full-text search |

## 2.4 Points d'Entrée de l'Application

### Backend Entry Points
| Projet | Fichier | Port |
|--------|---------|------|
| rag-dz | `services/api/app/main.py` | 8100 |
| academy | `backend/app/main.py` | 8000 |
| video | `backend/app/main.py` | 8001 |
| gateway | `src/index.ts` | 3001 |

### Frontend Entry Points
| Projet | Port | Framework |
|--------|------|-----------|
| Bolt.diy | 5173 | Remix + Vite |
| Archon UI | 8181 | React |
| Academy | 3000 | React + Vite |
| Video | 3000 | Next.js |

## 2.5 Intégrations Existantes

### Bolt.diy
**Localisation:** `d:\IAFactory\rag-dz\bolt-diy\`

```
Composants clés:
├── app/components/chat/
│   ├── BaseChat.tsx        # Conteneur principal
│   ├── Chat.client.tsx     # Orchestration chat
│   ├── ChatBox.tsx         # Zone de saisie
│   ├── Artifact.tsx        # Affichage artifacts
│   └── Messages.client.tsx # Liste messages
├── app/components/workbench/
│   ├── Workbench.client.tsx  # IDE complet
│   ├── EditorPanel.tsx       # Éditeur code
│   ├── Preview.tsx           # Preview app
│   └── Terminal.tsx          # Terminal web
├── app/lib/stores/
│   └── workbench.ts        # État global (nanostores)
└── app/lib/webcontainer/
    └── index.ts            # WebContainer bootstrap
```

**Points de communication:**
- API: `/api/bolt/*`, `/webcontainer.*`
- Deploiement: Netlify, Vercel via API

### Archon
**Localisation:** `d:\IAFactory\rag-dz\` (services + frontend)

```
Services:
├── services/api/app/services/
│   ├── archon_integration_service.py
│   ├── knowledge_item_service.py
│   ├── knowledge_summary_service.py
│   ├── crawling_service.py
│   ├── embedding_service.py
│   └── rag_service.py
└── frontend/archon-ui/  # Interface React
```

**Endpoints:**
- `/api/knowledge/*` - Gestion KB
- `/api/rag/*` - Requêtes RAG
- `/api/crawl/*` - Web crawling

### BMAD Method
**Localisation:** `d:\IAFactory\rag-dz\bmad\`

```
Structure:
├── src/core/           # Core BMAD
├── bmb/                # Builders
│   ├── agent-builder/  # Bond agent
│   ├── workflow-builder/ # Wendy agent
│   └── module-builder/
└── tools/cli/          # CLI BMAD
```

**Routers API:**
- `bmad.py` - CRUD agents
- `bmad_chat.py` - Chat avec agents
- `bmad_openai.py` - SSE streaming
- `bmad_orchestration.py` - Workflows

---

# 3. DIAGNOSTIC DES BUGS

## 3.1 Bug Principal: Désactivation IDE/WebContainer

### Symptômes Rapportés
- Interface chat cassée (boutons disparus)
- Micro non fonctionnel
- Artifacts se lancent même avec "Hi"

### Analyse des Fichiers Critiques

#### a) WebContainer Bootstrap
**Fichier:** `d:\IAFactory\rag-dz\bolt-diy\app\lib\webcontainer\index.ts`

```typescript
// Le WebContainer est un singleton avec support HMR
export const webcontainer: Promise<WebContainer>

// Configuration boot:
WebContainer.boot({
  coep: 'credentialless',
  workdirName: WORK_DIR_NAME,
  forwardPreviewErrors: true
})

// Context tracking:
export const webcontainerContext: WebContainerContext = {
  loaded: boolean
}
```

**💡 Problème potentiel:** Si le boot échoue ou est désactivé, `webcontainerContext.loaded` reste `false`, ce qui peut casser les composants dépendants.

#### b) État du Workbench
**Fichier:** `d:\IAFactory\rag-dz\bolt-diy\app\lib\stores\workbench.ts`

```typescript
// Stores critiques:
workbenchStore = {
  artifacts: MapStore,
  showWorkbench: WritableAtom,  // ★ TOGGLE PRINCIPAL
  currentView: WritableAtom,    // 'code' | 'diff' | 'preview'
  unsavedFiles: WritableAtom,
  // ...
}
```

**💡 Problème potentiel:** Si `showWorkbench` est forcé à `false` sans désactiver proprement les listeners, les composants enfants peuvent crasher.

#### c) Artifact Component
**Fichier:** `d:\IAFactory\rag-dz\bolt-diy\app\components\chat\Artifact.tsx`

```typescript
// Dépendances critiques:
const artifacts = useStore(workbenchStore.artifacts)
const actions = useStore(computed(...))

// Si artifacts est undefined, crash potentiel
```

### Zones à Investiguer

1. **Fichiers probablement modifiés:**
   - `app/lib/stores/workbench.ts` - toggle showWorkbench
   - `app/components/chat/BaseChat.tsx` - rendu conditionnel
   - `app/components/workbench/Workbench.client.tsx` - composant IDE

2. **Recherche de modifications récentes:**
```bash
cd d:\IAFactory\rag-dz\bolt-diy
git log --oneline -20 --all -- app/lib/stores/
git log --oneline -20 --all -- app/components/workbench/
git diff HEAD~10 -- app/lib/stores/workbench.ts
```

3. **Vérifier les erreurs console:**
   - Erreurs React: "Cannot read property of undefined"
   - Erreurs nanostores: MapStore access
   - Erreurs WebContainer: boot failure

### Plan de Fix Proposé

#### Étape 1: Diagnostic
```bash
# Rechercher les modifications récentes
cd d:\IAFactory\rag-dz\bolt-diy

# Chercher les toggles/masquages ajoutés
grep -r "showWorkbench" app/components/
grep -r "display.*none" app/components/
grep -r "visibility.*hidden" app/components/
```

#### Étape 2: Vérifier l'état du store
```typescript
// Dans BaseChat.tsx ou Chat.client.tsx, ajouter:
console.log('workbench state:', {
  showWorkbench: workbenchStore.showWorkbench.get(),
  artifactsCount: Object.keys(workbenchStore.artifacts.get()).length,
  webcontainerLoaded: webcontainerContext.loaded
})
```

#### Étape 3: Rollback propre
```typescript
// Option A: Toggle propre dans workbench.ts
export function setWorkbenchVisibility(visible: boolean) {
  // Désactiver les listeners avant de masquer
  if (!visible) {
    // Cleanup artifacts runners
    const artifacts = workbenchStore.artifacts.get()
    Object.values(artifacts).forEach(a => a.runner?.abort?.())
  }
  workbenchStore.showWorkbench.set(visible)
}
```

#### Étape 4: Protection des composants
```typescript
// Dans Artifact.tsx, ajouter des guards:
const artifact = artifacts[artifactId]
if (!artifact || !artifact.runner) {
  return null // Safe fallback
}
```

### Tests de Validation
1. Ouvrir la console browser avant toute action
2. Taper "Hi" dans le chat
3. Vérifier qu'aucun artifact ne démarre
4. Vérifier que les boutons sont visibles
5. Tester le micro (si applicable)

---

# 4. ARCHITECTURE CHAT MULTI-UTILISATEURS

## 4.1 Infrastructure Existante

### WebSocket Backend Actuel
**Fichier:** `d:\IAFactory\rag-dz\services\api\app\websocket.py`

```python
class ConnectionManager:
    """Gestion des connexions WebSocket par tenant"""

    async def connect(self, websocket: WebSocket, tenant_id: str)
    async def disconnect(self, websocket: WebSocket, tenant_id: str)
    async def broadcast(self, message: dict, tenant_id: str)
```

### SSE Streaming Existant
- `/v1/chat/completions` (OpenAI-compatible)
- `/api/ithy/stream` (Mixture-of-Agents)
- `/api/bmad/v1/chat/completions` (BMAD agents)

### ✅ Ce qui Existe Déjà
- WebSocket avec gestion multi-tenant
- Système de sessions (ChatSession)
- Stockage messages (ChatMessage)
- Redis pour cache/sessions

### ❌ Ce qui Manque
- Rooms de chat entre utilisateurs
- Invitations/partage de conversations
- Présence en temps réel
- Typing indicators
- Read receipts

## 4.2 Architecture Proposée pour Chat Multi-Utilisateurs

### Diagramme de Flux

```
┌─────────────────────────────────────────────────────────────────┐
│                     CHAT MULTI-UTILISATEURS                     │
└─────────────────────────────────────────────────────────────────┘

   User A                    User B                    User C
     │                         │                         │
     ▼                         ▼                         ▼
┌─────────┐               ┌─────────┐               ┌─────────┐
│ Browser │               │ Browser │               │ Browser │
│  React  │               │  React  │               │  React  │
└────┬────┘               └────┬────┘               └────┬────┘
     │                         │                         │
     │    WebSocket (wss://)   │                         │
     ▼                         ▼                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   WebSocket Server (FastAPI)                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  ConnectionManager                                         │ │
│  │  ├── rooms: Dict[room_id, Set[WebSocket]]                 │ │
│  │  ├── user_sessions: Dict[user_id, Set[WebSocket]]         │ │
│  │  └── presence: Dict[room_id, Dict[user_id, status]]       │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Redis Pub/Sub                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ channel:room:1  │  │ channel:room:2  │  │ channel:typing  │ │
│  │ channel:presence│  │ channel:notify  │  │ channel:invites │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PostgreSQL                                 │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │ rooms   │  │ messages │  │ members  │  │ invitations      │ │
│  └─────────┘  └──────────┘  └──────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Structure Base de Données Proposée

```sql
-- Rooms de chat (conversations privées ou groupes)
CREATE TABLE chat_rooms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100),
    type VARCHAR(20) NOT NULL, -- 'direct', 'group', 'project'
    org_id UUID REFERENCES orgs(id),
    project_id UUID, -- Lien optionnel vers un projet Bolt
    created_by UUID REFERENCES users(id),
    is_archived BOOLEAN DEFAULT false,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Membres des rooms
CREATE TABLE chat_room_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID REFERENCES chat_rooms(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member', -- 'owner', 'admin', 'member'
    joined_at TIMESTAMP DEFAULT NOW(),
    last_read_at TIMESTAMP DEFAULT NOW(),
    is_muted BOOLEAN DEFAULT false,
    UNIQUE(room_id, user_id)
);

-- Messages
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID REFERENCES chat_rooms(id) ON DELETE CASCADE,
    sender_id UUID REFERENCES users(id) ON DELETE SET NULL,
    content TEXT NOT NULL,
    type VARCHAR(20) DEFAULT 'text', -- 'text', 'file', 'code', 'artifact', 'system'
    reply_to_id UUID REFERENCES chat_messages(id),
    metadata JSONB DEFAULT '{}', -- fichiers attachés, mentions, etc.
    is_edited BOOLEAN DEFAULT false,
    edited_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_room_created (room_id, created_at DESC)
);

-- Invitations
CREATE TABLE chat_invitations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID REFERENCES chat_rooms(id) ON DELETE CASCADE,
    invited_by UUID REFERENCES users(id),
    email VARCHAR(255) NOT NULL,
    token VARCHAR(100) UNIQUE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'accepted', 'expired'
    expires_at TIMESTAMP NOT NULL,
    accepted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Read receipts
CREATE TABLE message_read_receipts (
    message_id UUID REFERENCES chat_messages(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    read_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (message_id, user_id)
);
```

### Composants React à Créer

```
app/components/chat-multi/
├── ChatRoom.tsx              # Container principal d'une room
├── ChatRoomList.tsx          # Liste des conversations
├── ChatRoomHeader.tsx        # Header avec membres, settings
├── ChatMessageList.tsx       # Liste des messages avec virtualisation
├── ChatMessageItem.tsx       # Un message individuel
├── ChatInput.tsx             # Zone de saisie multi-ligne
├── ChatTypingIndicator.tsx   # "User is typing..."
├── ChatMemberList.tsx        # Liste des membres
├── ChatInviteModal.tsx       # Modal d'invitation
├── ChatPresenceIndicator.tsx # Online/offline status
├── hooks/
│   ├── useWebSocket.ts       # Hook WebSocket
│   ├── useChatRoom.ts        # État d'une room
│   ├── usePresence.ts        # Présence utilisateurs
│   └── useTyping.ts          # Typing indicator
└── stores/
    └── chatStore.ts          # État global chat (Zustand)
```

### API Endpoints Nécessaires

```python
# Rooms
POST   /api/chat/rooms                    # Créer une room
GET    /api/chat/rooms                    # Lister mes rooms
GET    /api/chat/rooms/{id}               # Détails d'une room
PUT    /api/chat/rooms/{id}               # Modifier une room
DELETE /api/chat/rooms/{id}               # Archiver une room

# Messages
GET    /api/chat/rooms/{id}/messages      # Paginer les messages
POST   /api/chat/rooms/{id}/messages      # Envoyer un message
PUT    /api/chat/messages/{id}            # Éditer un message
DELETE /api/chat/messages/{id}            # Supprimer un message

# Membres
GET    /api/chat/rooms/{id}/members       # Lister les membres
POST   /api/chat/rooms/{id}/members       # Ajouter un membre
DELETE /api/chat/rooms/{id}/members/{uid} # Retirer un membre

# Invitations
POST   /api/chat/rooms/{id}/invite        # Inviter par email
GET    /api/chat/invitations/{token}      # Vérifier invitation
POST   /api/chat/invitations/{token}/accept # Accepter invitation

# Présence (WebSocket)
WS     /ws/chat                           # Connexion temps réel
```

### Événements WebSocket

```typescript
// Client → Server
interface ClientMessage {
  type: 'join_room' | 'leave_room' | 'send_message' |
        'typing_start' | 'typing_stop' | 'mark_read'
  room_id: string
  content?: string
  metadata?: object
}

// Server → Client
interface ServerMessage {
  type: 'message' | 'typing' | 'presence' | 'room_update' | 'error'
  room_id: string
  sender_id?: string
  data: object
  timestamp: string
}

// Événements spécifiques
type Events = {
  'message:new': { message: Message }
  'message:edit': { message: Message }
  'message:delete': { message_id: string }
  'typing:start': { user_id: string }
  'typing:stop': { user_id: string }
  'presence:join': { user_id: string, status: 'online' }
  'presence:leave': { user_id: string }
  'member:add': { user: User }
  'member:remove': { user_id: string }
}
```

## 4.3 Système d'Invitation (Viralité)

### Flow d'Invitation

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   User A     │      │   Backend    │      │   User B     │
│  (inviteur)  │      │              │      │  (invité)    │
└──────┬───────┘      └──────┬───────┘      └──────┬───────┘
       │                     │                     │
       │ POST /invite        │                     │
       │ {email, room_id}    │                     │
       │────────────────────>│                     │
       │                     │                     │
       │                     │ Generate token      │
       │                     │ Store invitation    │
       │                     │                     │
       │                     │ Send email          │
       │                     │─────────────────────>
       │                     │                     │
       │  201 Created        │                     │
       │<────────────────────│                     │
       │                     │                     │
       │                     │                     │ Click link
       │                     │<────────────────────│
       │                     │ GET /invite/{token} │
       │                     │                     │
       │                     │ Validate token      │
       │                     │                     │
       │                     │ If new user:        │
       │                     │   Show signup       │
       │                     │ Else:               │
       │                     │   Add to room       │
       │                     │                     │
       │                     │ Redirect to room    │
       │                     │─────────────────────>
       │                     │                     │
       │ Notification        │                     │
       │<────────────────────│                     │
       │ "User B joined"     │                     │
```

### Landing Page Invités

```
URL: https://app.iafactory.io/invite/{token}

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│     🎉 You're invited to collaborate on IAFactory!          │
│                                                             │
│     [User Name] invited you to join:                        │
│     "[Project Name]" workspace                              │
│                                                             │
│     ┌───────────────────────────────────────────────────┐  │
│     │  💬 Chat in real-time with your team              │  │
│     │  🚀 Build apps together with AI assistance        │  │
│     │  📊 Share and review code instantly               │  │
│     └───────────────────────────────────────────────────┘  │
│                                                             │
│     [    Accept Invitation    ]                             │
│                                                             │
│     Already have an account? [Sign In]                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Système de Parrainage

```sql
-- Crédits bonus pour parrainage
CREATE TABLE referral_rewards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    referrer_id UUID REFERENCES users(id),
    referred_id UUID REFERENCES users(id),
    invitation_id UUID REFERENCES chat_invitations(id),
    reward_credits INTEGER DEFAULT 100,
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'granted', 'expired'
    granted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Trigger: Accorder crédits après 1ère action du nouvel utilisateur
```

---

# 5. CONFORMITÉ RGPD & STOCKAGE

## 5.1 État Actuel

### ❌ Points Non Conformes
- Pas de politique de confidentialité documentée
- Pas de système d'export de données utilisateur
- Pas de mécanisme de "droit à l'oubli"
- Localisation serveurs non documentée
- Pas de consentement explicite aux cookies/tracking

### ✅ Points Existants
- Authentification JWT sécurisée
- Stockage passwords hashé (bcrypt)
- Multi-tenant avec isolation des données

## 5.2 Checklist RGPD

| Exigence | Statut | Action Requise |
|----------|--------|----------------|
| Base légale du traitement | ❌ | Documenter |
| Consentement explicite | ❌ | Banner cookies |
| Politique de confidentialité | ❌ | Rédiger document |
| Droit d'accès (Art. 15) | ❌ | API export |
| Droit de rectification (Art. 16) | ⚠️ | Améliorer UI |
| Droit à l'effacement (Art. 17) | ❌ | Implémenter |
| Droit à la portabilité (Art. 20) | ❌ | Export JSON/CSV |
| Privacy by design | ⚠️ | Audit données |
| Registre des traitements | ❌ | Documenter |
| DPO (si >250 employés) | N/A | - |
| Notification de faille | ❌ | Procédure |

## 5.3 Actions Requises

### a) Documents Légaux à Créer

```
/legal/
├── privacy-policy.md        # Politique de confidentialité
├── terms-of-service.md      # CGU/CGV
├── cookie-policy.md         # Politique cookies
├── data-processing.md       # Traitement des données
└── dpa-template.md          # Data Processing Agreement (B2B)
```

### b) API RGPD à Implémenter

```python
# Endpoints RGPD
GET  /api/user/data-export           # Export toutes les données
POST /api/user/delete-account        # Demande suppression
GET  /api/user/data-export/status    # Statut de l'export
GET  /api/user/consents              # Liste des consentements
PUT  /api/user/consents              # Modifier consentements
```

### c) Export de Données

```python
# Structure export utilisateur
{
    "export_date": "2026-01-09T12:00:00Z",
    "user": {
        "id": "uuid",
        "email": "user@example.com",
        "name": "...",
        "created_at": "..."
    },
    "profile": {...},
    "conversations": [...],
    "messages": [...],
    "projects": [...],
    "files": [...],
    "billing": {...},
    "activity_log": [...]
}
```

### d) Suppression de Compte

```python
async def delete_user_data(user_id: str):
    """
    Suppression complète des données utilisateur (RGPD Art. 17)
    """
    # 1. Anonymiser les données publiques (messages, projets partagés)
    await anonymize_shared_content(user_id)

    # 2. Supprimer les données privées
    await delete_conversations(user_id)
    await delete_files(user_id)
    await delete_api_keys(user_id)

    # 3. Annuler les abonnements actifs
    await cancel_subscriptions(user_id)

    # 4. Supprimer le compte
    await delete_user_account(user_id)

    # 5. Log de conformité (garder 3 ans pour audit)
    await log_deletion_event(user_id)
```

## 5.4 Stockage Local (IndexedDB)

### Infrastructure Existante
**Fichier:** `d:\IAFactory\rag-dz\bolt-diy\app\lib\hooks\useIndexedDB.ts`

```typescript
// Hook existant pour IndexedDB
// Utilisé pour l'historique des chats
```

### Améliorations Proposées

```typescript
// Nouvelle structure IndexedDB
const DB_SCHEMA = {
  name: 'iafactory-local',
  version: 2,
  stores: {
    // Conversations locales (draft, non synchronisées)
    drafts: {
      keyPath: 'id',
      indexes: ['room_id', 'updated_at']
    },
    // Cache des messages récents
    messages_cache: {
      keyPath: 'id',
      indexes: ['room_id', 'created_at']
    },
    // Fichiers en attente d'upload
    pending_uploads: {
      keyPath: 'id',
      indexes: ['status', 'created_at']
    },
    // Préférences utilisateur
    preferences: {
      keyPath: 'key'
    }
  }
}
```

### Bibliothèque Recommandée: Dexie.js

```typescript
// Installation: npm install dexie

import Dexie, { Table } from 'dexie'

interface Draft {
  id: string
  room_id: string
  content: string
  updated_at: Date
}

class IAFactoryDB extends Dexie {
  drafts!: Table<Draft>
  messages_cache!: Table<Message>
  preferences!: Table<{key: string, value: any}>

  constructor() {
    super('iafactory-local')
    this.version(1).stores({
      drafts: 'id, room_id, updated_at',
      messages_cache: 'id, room_id, created_at',
      preferences: 'key'
    })
  }
}

export const db = new IAFactoryDB()
```

## 5.5 Intégration Google Drive (Optionnel)

### Architecture OAuth

```typescript
// Configuration OAuth Google
const GOOGLE_CONFIG = {
  clientId: process.env.GOOGLE_CLIENT_ID,
  scopes: [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.appdata'
  ]
}

// Flow OAuth
async function connectGoogleDrive() {
  // 1. Redirect vers Google OAuth
  // 2. Callback avec code
  // 3. Échanger code contre tokens
  // 4. Stocker refresh_token en DB (crypté)
}

// Auto-save vers Drive
async function syncToGoogleDrive(projectId: string) {
  const project = await getProject(projectId)
  const tokens = await getUserGoogleTokens()

  // Créer/mettre à jour fichier dans appDataFolder
  await drive.files.update({
    fileId: project.drive_file_id,
    media: {
      mimeType: 'application/json',
      body: JSON.stringify(project)
    }
  })
}
```

---

# 6. INTÉGRATION AGENTS + CHAT

## 6.1 Flow Actuel des Agents BMAD

### Agents Disponibles (19)
| Agent | Rôle | Fichier |
|-------|------|---------|
| bmm-architect | Architecture système | `bmad_chat.py` |
| bmm-pm | Product management | `bmad_chat.py` |
| bmm-developer | Développement code | `bmad_chat.py` |
| bmm-tester | Tests & QA | `bmad_chat.py` |
| bmm-tech-writer | Documentation | `bmad_chat.py` |
| ... | ... | ... |

### Routing Actuel
**Fichier:** `d:\IAFactory\rag-dz\services\api\app\routers\bmad_chat.py`

```python
# Sélection d'agent par paramètre
@router.post("/chat/{agent_type}")
async def chat_with_agent(agent_type: str, request: ChatRequest):
    # Mapping vers le bon system prompt
    # Appel LLM avec contexte agent
```

## 6.2 Intégration Proposée: @mentions dans le Chat

### Parser de Mentions

```typescript
// Détection des mentions dans le texte
const MENTION_REGEX = /@([\w-]+)/g

interface ParsedMessage {
  text: string
  mentions: Mention[]
}

interface Mention {
  type: 'user' | 'agent' | 'channel'
  id: string
  name: string
  startIndex: number
  endIndex: number
}

function parseMessage(content: string): ParsedMessage {
  const mentions: Mention[] = []
  let match

  while ((match = MENTION_REGEX.exec(content)) !== null) {
    const name = match[1]

    // Vérifier si c'est un agent BMAD
    if (BMAD_AGENTS.includes(name)) {
      mentions.push({
        type: 'agent',
        id: name,
        name: `@${name}`,
        startIndex: match.index,
        endIndex: match.index + match[0].length
      })
    }
    // Sinon vérifier si c'est un utilisateur
    // ...
  }

  return { text: content, mentions }
}
```

### Liste des Agents Mentionnables

```typescript
const BMAD_AGENTS = [
  { id: 'architect', name: 'Architect', description: 'System design & architecture' },
  { id: 'pm', name: 'PM', description: 'Product management & planning' },
  { id: 'developer', name: 'Developer', description: 'Code implementation' },
  { id: 'tester', name: 'Tester', description: 'Testing & QA' },
  { id: 'writer', name: 'Writer', description: 'Documentation' },
  { id: 'analyst', name: 'Analyst', description: 'Business analysis' },
  { id: 'designer', name: 'Designer', description: 'UI/UX design' },
  // ... autres agents
]
```

### Auto-complétion des Mentions

```tsx
// Composant Autocomplete pour mentions
function MentionAutocomplete({
  query,
  onSelect
}: {
  query: string
  onSelect: (agent: Agent) => void
}) {
  const filteredAgents = BMAD_AGENTS.filter(a =>
    a.id.includes(query) || a.name.toLowerCase().includes(query)
  )

  return (
    <div className="mention-dropdown">
      {filteredAgents.map(agent => (
        <div
          key={agent.id}
          onClick={() => onSelect(agent)}
          className="mention-option"
        >
          <span className="agent-icon">🤖</span>
          <span className="agent-name">@{agent.id}</span>
          <span className="agent-desc">{agent.description}</span>
        </div>
      ))}
    </div>
  )
}
```

### Routing vers l'Agent

```python
# Backend: Router les mentions vers les agents
@router.post("/chat/rooms/{room_id}/messages")
async def send_message(room_id: str, request: MessageRequest):
    # 1. Parser le message
    parsed = parse_mentions(request.content)

    # 2. Sauvegarder le message utilisateur
    message = await save_message(room_id, request)

    # 3. Si mention d'agent, router vers l'agent
    for mention in parsed.mentions:
        if mention.type == 'agent':
            # Appeler l'agent en background
            asyncio.create_task(
                invoke_agent(
                    agent_id=mention.id,
                    room_id=room_id,
                    context=request.content,
                    reply_to=message.id
                )
            )

    return message
```

## 6.3 Context Awareness pour les Agents

### Gestion du Contexte

```python
class AgentContextBuilder:
    """Construit le contexte pour un agent basé sur le chat"""

    def __init__(self, room_id: str, user_id: str):
        self.room_id = room_id
        self.user_id = user_id

    async def build(self, max_messages: int = 20) -> dict:
        # 1. Récupérer l'historique récent
        messages = await get_recent_messages(self.room_id, max_messages)

        # 2. Récupérer le contexte projet (si lié à Bolt)
        project = await get_room_project(self.room_id)

        # 3. Récupérer les mémoires utilisateur (Archon)
        memories = await get_user_memories(self.user_id)

        return {
            "conversation_history": messages,
            "project_context": project,
            "user_memories": memories,
            "room_members": await get_room_members(self.room_id)
        }
```

### Intégration avec Archon

```python
# Enrichir le contexte avec la base de connaissance
async def enrich_with_knowledge(query: str, project_id: str):
    """
    Utilise Archon pour enrichir le contexte avec des infos pertinentes
    """
    # 1. Recherche sémantique dans la KB du projet
    results = await rag_service.search(
        query=query,
        project_id=project_id,
        limit=5
    )

    # 2. Formater pour injection dans le prompt
    context_chunks = [
        f"[Source: {r.source}]\n{r.content}"
        for r in results
    ]

    return "\n\n".join(context_chunks)
```

## 6.4 Auto-Routing Intelligent

```python
# Détection automatique de l'agent approprié
class IntentRouter:
    """Route automatiquement vers le bon agent basé sur l'intent"""

    INTENT_PATTERNS = {
        'architecture': ['design', 'structure', 'system', 'scalab'],
        'code': ['implement', 'code', 'function', 'bug', 'error'],
        'test': ['test', 'coverage', 'qa', 'quality'],
        'doc': ['document', 'readme', 'explain', 'how to'],
        'plan': ['plan', 'roadmap', 'timeline', 'sprint'],
    }

    AGENT_MAP = {
        'architecture': 'bmm-architect',
        'code': 'bmm-developer',
        'test': 'bmm-tester',
        'doc': 'bmm-tech-writer',
        'plan': 'bmm-pm',
    }

    async def route(self, message: str) -> Optional[str]:
        # 1. Détection basique par mots-clés
        message_lower = message.lower()
        for intent, keywords in self.INTENT_PATTERNS.items():
            if any(kw in message_lower for kw in keywords):
                return self.AGENT_MAP[intent]

        # 2. Si ambiguë, utiliser un LLM léger pour classifier
        if self.is_ambiguous(message):
            return await self.classify_with_llm(message)

        return None  # Pas d'agent spécifique
```

---

# 7. OPTIMISATIONS & BEST PRACTICES

## 7.1 Performance

### ✅ Points Positifs
- Vite pour le bundling (rapide)
- Code splitting avec Remix
- Lazy loading des routes

### ❌ Points à Améliorer

#### Bundle Size
```bash
# Analyser le bundle
cd d:\IAFactory\rag-dz\bolt-diy
npm run build
npx vite-bundle-visualizer
```

#### Recommandations
1. **Lazy load WebContainer** seulement quand nécessaire
2. **Virtualiser** les listes de messages (react-window)
3. **Optimiser** les re-renders avec `memo` et `useMemo`
4. **Compresser** les assets (images, fonts)

## 7.2 Sécurité

### Audit de Sécurité

```bash
# Vérifier les vulnérabilités npm
cd d:\IAFactory\rag-dz\bolt-diy
npm audit

# Vérifier les dépendances Python
cd d:\IAFactory\rag-dz\services\api
pip-audit
```

### Points à Vérifier
| Risque | Statut | Mitigation |
|--------|--------|------------|
| XSS | ⚠️ | Sanitizer le markdown |
| CSRF | ✅ | Tokens CSRF actifs |
| SQL Injection | ✅ | ORM avec paramètres |
| Rate Limiting | ⚠️ | Configurer limites |
| API Keys exposure | ⚠️ | Audit .env files |

### Recommandations
```python
# Rate limiting sur les endpoints sensibles
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/chat/messages")
@limiter.limit("60/minute")
async def send_message():
    ...
```

## 7.3 Code Quality

### Tests Existants
```bash
# Vérifier la couverture
cd d:\IAFactory\rag-dz\bolt-diy
npm run test:coverage
```

### Recommandations
1. **Unit tests** pour les stores nanostores
2. **Integration tests** pour les APIs
3. **E2E tests** avec Playwright pour les flows critiques

```typescript
// Exemple test E2E
test('user can send message in chat', async ({ page }) => {
  await page.goto('/chat/room/123')
  await page.fill('[data-testid="chat-input"]', 'Hello world')
  await page.click('[data-testid="send-button"]')
  await expect(page.locator('.message-content')).toContainText('Hello world')
})
```

## 7.4 DevOps

### CI/CD Recommandé

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run test:coverage
      - uses: codecov/codecov-action@v3

  build:
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run build

  deploy:
    if: github.ref == 'refs/heads/main'
    needs: [build]
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploy to production"
```

---

# 8. ROADMAP TECHNIQUE

## Phase 1: Stabilisation (Quick Wins)

### Objectifs
- Fix bug IDE/WebContainer
- Stabiliser l'interface chat existante
- Préparer l'infrastructure pour le chat multi-user

### Tâches

| Tâche | Priorité | Complexité |
|-------|----------|------------|
| Diagnostiquer le bug WebContainer | 🔴 URGENT | Moyenne |
| Corriger les composants cassés | 🔴 URGENT | Moyenne |
| Ajouter guards null dans Artifact.tsx | 🔴 URGENT | Faible |
| Créer toggle mode propre | 🟠 HIGH | Moyenne |
| Setup Redis pour sessions | 🟠 HIGH | Faible |
| Documenter l'architecture | 🟡 MEDIUM | Moyenne |

## Phase 2: Chat Multi-Utilisateurs

### Objectifs
- Implémenter le chat privé entre utilisateurs
- Système d'invitation fonctionnel
- Présence et typing indicators

### Tâches

| Tâche | Priorité | Complexité |
|-------|----------|------------|
| Créer tables BD chat_rooms, messages | 🔴 HIGH | Moyenne |
| Implémenter WebSocket multi-room | 🔴 HIGH | Haute |
| Créer composants React chat | 🔴 HIGH | Haute |
| Système d'invitation email | 🟠 HIGH | Moyenne |
| Typing indicators | 🟡 MEDIUM | Faible |
| Read receipts | 🟡 MEDIUM | Faible |
| Landing page invités | 🟡 MEDIUM | Moyenne |

## Phase 3: Intégration Agents

### Objectifs
- Mentions @agent dans le chat
- Auto-routing intelligent
- Context awareness avec Archon

### Tâches

| Tâche | Priorité | Complexité |
|-------|----------|------------|
| Parser de mentions | 🔴 HIGH | Moyenne |
| Autocomplete UI | 🔴 HIGH | Moyenne |
| Router vers agents BMAD | 🔴 HIGH | Moyenne |
| Context builder | 🟠 HIGH | Haute |
| Intégration Archon KB | 🟡 MEDIUM | Haute |
| Auto-routing par intent | 🟡 MEDIUM | Haute |

## Phase 4: RGPD & Polish

### Objectifs
- Conformité RGPD complète
- Optimisations performance
- Tests automatisés

### Tâches

| Tâche | Priorité | Complexité |
|-------|----------|------------|
| Rédiger politique confidentialité | 🔴 HIGH | Moyenne |
| API export données utilisateur | 🔴 HIGH | Haute |
| Suppression de compte | 🔴 HIGH | Haute |
| Banner cookies | 🟠 MEDIUM | Faible |
| Optimiser bundle size | 🟡 MEDIUM | Moyenne |
| Tests E2E | 🟡 MEDIUM | Haute |
| CI/CD pipeline | 🟡 MEDIUM | Moyenne |

---

# ANNEXES

## A. Fichiers Clés par Fonctionnalité

### Chat/Bolt.diy
```
d:\IAFactory\rag-dz\bolt-diy\app\components\chat\BaseChat.tsx
d:\IAFactory\rag-dz\bolt-diy\app\components\chat\Chat.client.tsx
d:\IAFactory\rag-dz\bolt-diy\app\components\chat\ChatBox.tsx
d:\IAFactory\rag-dz\bolt-diy\app\components\chat\Artifact.tsx
d:\IAFactory\rag-dz\bolt-diy\app\lib\stores\workbench.ts
d:\IAFactory\rag-dz\bolt-diy\app\lib\webcontainer\index.ts
```

### WebSocket/Temps Réel
```
d:\IAFactory\rag-dz\services\api\app\websocket.py
d:\IAFactory\rag-dz\services\api\app\routers\websocket_router.py
d:\IAFactory\rag-dz\services\api\app\mcp\server.py
```

### Base de Données
```
d:\IAFactory\iafactory-gateway\prisma\schema.prisma
d:\IAFactory\rag-dz\services\api\app\models\user.py
d:\IAFactory\rag-dz\services\api\app\models\memory_models.py
```

### BMAD/Agents
```
d:\IAFactory\rag-dz\services\api\app\routers\bmad_chat.py
d:\IAFactory\rag-dz\services\api\app\routers\bmad_openai.py
d:\IAFactory\rag-dz\bmad\src\core\
```

## B. Variables d'Environnement Critiques

```bash
# API Keys (obligatoires)
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GROQ_API_KEY=

# Database
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
QDRANT_HOST=localhost:6333

# Auth
JWT_SECRET=
API_SECRET_KEY=

# Services
N8N_HOST=http://localhost:5678
MEILISEARCH_URL=http://localhost:7700
```

## C. Ports Réseau

| Service | Port | Description |
|---------|------|-------------|
| Gateway | 3001 | API Gateway |
| RAG-DZ API | 8100 | API principale |
| Academy API | 8000 | E-learning |
| Video API | 8001 | Video platform |
| Bolt.diy | 5173 | IDE web |
| Archon UI | 8181 | KB management |
| PostgreSQL | 5432/5433 | Base de données |
| Redis | 6379 | Cache |
| Qdrant | 6333 | Vector DB |
| n8n | 5678 | Workflows |

---

**Fin du rapport d'audit**

*Généré par Claude Code le 9 janvier 2026*
