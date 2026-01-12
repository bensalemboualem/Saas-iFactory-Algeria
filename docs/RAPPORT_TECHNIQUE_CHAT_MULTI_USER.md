# RAPPORT TECHNIQUE CHAT MULTI-USER

**Date:** 9 janvier 2026
**Projet:** IAFactory
**Objectif:** Implémentation Chat User↔User avec rooms et invitations

---

# 1. ÉTAT ACTUEL

## 1.1 Chat IA Existant - Backend

### Fichiers Principaux

| Fichier | Chemin | Lignes | Rôle |
|---------|--------|--------|------|
| conversations.py | `rag-dz/services/api/app/routers/conversations.py` | ~450 | API REST conversations |
| memory_service.py | `rag-dz/services/api/app/services/memory_service.py` | ~750 | Service mémoire IA |
| websocket.py | `rag-dz/services/api/app/websocket.py` | 106 | ConnectionManager WebSocket |
| websocket_router.py | `rag-dz/services/api/app/routers/websocket_router.py` | 77 | Endpoint /ws |
| bmad_chat.py | `rag-dz/services/api/app/routers/bmad_chat.py` | 319 | Chat agents BMAD |

### Routes API Actuelles

```python
# Conversations (conversations.py)
POST   /api/conversations                    # Créer session
GET    /api/conversations                    # Lister sessions
GET    /api/conversations/{session_id}       # Détails session
DELETE /api/conversations/{session_id}       # Supprimer session
POST   /api/conversations/{session_id}/messages  # Ajouter message
GET    /api/conversations/{session_id}/messages  # Historique messages

# BMAD Agents (bmad_chat.py)
POST   /api/bmad/chat                        # Chat avec agent
GET    /api/bmad/agents/{agent_id}/personality  # Personnalité agent
GET    /api/bmad/chat/health                 # Health check

# WebSocket (websocket_router.py)
WS     /ws?api_key=xxx                       # Connexion temps réel
```

### WebSocket - Code Actuel

**Fichier:** `d:\IAFactory\rag-dz\services\api\app\websocket.py`

```python
class ConnectionManager:
    """Manage WebSocket connections"""

    def __init__(self):
        # tenant_id -> Set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, tenant_id: str):
        await websocket.accept()
        if tenant_id not in self.active_connections:
            self.active_connections[tenant_id] = set()
        self.active_connections[tenant_id].add(websocket)

    def disconnect(self, websocket: WebSocket, tenant_id: str):
        if tenant_id in self.active_connections:
            self.active_connections[tenant_id].discard(websocket)

    async def broadcast_to_tenant(self, tenant_id: str, message: dict):
        if tenant_id not in self.active_connections:
            return
        for connection in self.active_connections[tenant_id]:
            await connection.send_json(message)

    async def send_progress_update(self, tenant_id: str, operation_id: str,
                                   status: str, progress: int, message: str, data: Dict = None):
        update = ProgressUpdate(operation_id, status, progress, message, data)
        await self.broadcast_to_tenant(tenant_id, update.to_dict())
```

**Limitation:** Le WebSocket actuel est organisé par `tenant_id` uniquement, pas par `room_id` ni `user_id`.

---

## 1.2 Chat IA Existant - Frontend (Bolt.diy)

### Composants Principaux

| Fichier | Chemin | Lignes | Rôle |
|---------|--------|--------|------|
| Chat.client.tsx | `rag-dz/bolt-diy/app/components/chat/Chat.client.tsx` | 722 | Orchestration chat |
| ChatBox.tsx | `rag-dz/bolt-diy/app/components/chat/ChatBox.tsx` | ~200 | Zone de saisie |
| Artifact.tsx | `rag-dz/bolt-diy/app/components/chat/Artifact.tsx` | 297 | Affichage artifacts |
| workbench.ts | `rag-dz/bolt-diy/app/lib/stores/workbench.ts` | 1111 | Store Workbench |

### Chat.client.tsx - Structure

```typescript
// Imports clés
import { useChat } from '@ai-sdk/react';
import { workbenchStore } from '~/lib/stores/workbench';

// Hook principal
const {
  messages,
  isLoading,
  input,
  handleInputChange,
  setInput,
  stop,
  append,
  setMessages,
} = useChat({
  api: '/api/chat',
  body: { apiKeys, files, promptId, contextOptimization, chatMode, designScheme },
});

// BMAD integration
const [bmadMessages, setBmadMessages] = useState<Message[]>([]);

// Merge messages pour affichage
messages={[...messages, ...bmadMessages].map((message, i) => {
  const isBmadMessage = message.id?.startsWith('bmad-') ||
                        message.id?.startsWith('archon-') ||
                        message.id?.startsWith('nexus-');
  return {
    ...message,
    content: isBmadMessage ? message.content : (parsedMessages[i] || message.content),
  };
})}
```

### State Management - nanostores

**Fichier:** `d:\IAFactory\rag-dz\bolt-diy\app\lib\stores\workbench.ts`

```typescript
export class WorkbenchStore {
  artifacts: Artifacts = map({});
  showWorkbench: WritableAtom<boolean> = atom(false);
  currentView: WritableAtom<WorkbenchViewType> = atom('code');
  unsavedFiles: WritableAtom<Set<string>> = atom(new Set<string>());
  actionAlert: WritableAtom<ActionAlert | undefined> = atom(undefined);
  // ...

  setShowWorkbench(show: boolean) {
    this.showWorkbench.set(show);
  }

  addArtifact({ messageId, title, id, type }: ArtifactCallbackData) {
    const artifact = this.#getArtifact(id);
    if (artifact) return;

    this.artifacts.setKey(id, {
      id, title, closed: false, type,
      runner: new ActionRunner(webcontainer, /*...*/)
    });
  }
}

export const workbenchStore = new WorkbenchStore();
```

---

## 1.3 Database Schema Chat - Actuel

**Fichier:** `d:\IAFactory\rag-dz\services\api\migrations\014_iafactory_memory.sql`

### Tables Existantes

```sql
-- ENUM Types
CREATE TYPE memory_category AS ENUM ('profile', 'preference', 'business', 'fact', 'goal');
CREATE TYPE message_role AS ENUM ('user', 'assistant', 'system', 'tool');

-- Sessions de conversation (chat USER↔IA seulement)
CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    app_context VARCHAR(50) DEFAULT 'chat',  -- 'rag', 'academy', 'video', 'gov', 'crm'
    language VARCHAR(10) DEFAULT 'fr',
    agent_id VARCHAR(100),                    -- BMAD agent ID si applicable
    model VARCHAR(50) DEFAULT 'groq',
    message_count INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    last_message_at TIMESTAMPTZ DEFAULT NOW(),
    is_archived BOOLEAN DEFAULT FALSE,
    is_starred BOOLEAN DEFAULT FALSE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Messages individuels
CREATE TABLE IF NOT EXISTS chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role message_role NOT NULL,
    content TEXT NOT NULL,
    tokens_input INTEGER DEFAULT 0,
    tokens_output INTEGER DEFAULT 0,
    tokens_total INTEGER GENERATED ALWAYS AS (tokens_input + tokens_output) STORED,
    model VARCHAR(50),
    provider VARCHAR(30),
    latency_ms INTEGER,
    attachments JSONB DEFAULT '[]',
    tools_used JSONB DEFAULT '[]',
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    feedback TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'
);

-- Mémoires utilisateur (pour persistance IA)
CREATE TABLE IF NOT EXISTS user_memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category memory_category NOT NULL,
    key VARCHAR(100) NOT NULL,
    value TEXT NOT NULL,
    value_type VARCHAR(20) DEFAULT 'text',
    confidence DECIMAL(3,2) DEFAULT 0.80,
    source VARCHAR(50) DEFAULT 'extracted',
    extracted_from UUID REFERENCES chat_messages(id) ON DELETE SET NULL,
    language VARCHAR(10) DEFAULT 'fr',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    metadata JSONB DEFAULT '{}',
    UNIQUE(user_id, category, key)
);

-- RLS Enabled sur toutes les tables
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_memories ENABLE ROW LEVEL SECURITY;
```

### Ce qui MANQUE pour Chat Multi-User

```
❌ Table chat_rooms (rooms/conversations multi-user)
❌ Table chat_room_members (participants par room)
❌ Table chat_invitations (invitations par email)
❌ Table message_read_receipts (accusés de lecture)
❌ Champs: sender_id, room_id dans messages
❌ WebSocket events: typing, presence, join_room, leave_room
```

---

## 1.4 Bug WebContainer - Analyse

### Fichiers Clés

| Fichier | Chemin | Statut |
|---------|--------|--------|
| webcontainer/index.ts | `rag-dz/bolt-diy/app/lib/webcontainer/index.ts` | ✅ OK |
| workbench.ts | `rag-dz/bolt-diy/app/lib/stores/workbench.ts` | ✅ OK |
| Artifact.tsx | `rag-dz/bolt-diy/app/components/chat/Artifact.tsx` | ⚠️ Potentiel bug |

### WebContainer Boot Sequence

**Fichier:** `d:\IAFactory\rag-dz\bolt-diy\app\lib\webcontainer\index.ts`

```typescript
export const webcontainerContext: WebContainerContext = { loaded: false };

export let webcontainer: Promise<WebContainer> = new Promise(() => {});

if (!import.meta.env.SSR) {
  webcontainer = Promise.resolve()
    .then(() => {
      console.log('[WebContainer] Starting boot process...');
      const bootPromise = WebContainer.boot({
        coep: 'credentialless',
        workdirName: WORK_DIR_NAME,
        forwardPreviewErrors: true,
      });

      const timeoutPromise = new Promise<never>((_, reject) => {
        setTimeout(() => reject(new Error('WebContainer boot timeout')), 60000);
      });

      return Promise.race([bootPromise, timeoutPromise]);
    })
    .then(async (webcontainer) => {
      console.log('[WebContainer] Boot successful!');
      webcontainerContext.loaded = true;
      // ...
      return webcontainer;
    })
    .catch((error) => {
      console.error('[WebContainer] Boot failed:', error);
      webcontainerContext.loaded = false;
      // Affiche erreur visuelle
      throw error;
    });
}
```

### Artifact.tsx - Bug Potentiel Identifié

**Fichier:** `d:\IAFactory\rag-dz\bolt-diy\app\components\chat\Artifact.tsx`

```typescript
// Ligne 34-37: Accès direct sans guard
const artifacts = useStore(workbenchStore.artifacts);
const artifact = artifacts[artifactId];

const actions = useStore(
  computed(artifact.runner.actions, (actions) => {  // ⚠️ artifact.runner peut être undefined!
    return Object.values(actions).filter(/*...*/);
  }),
);
```

**Problème:** Si `artifact` est `undefined` (parce que l'artifactId n'existe pas encore dans le store), l'accès à `artifact.runner.actions` va crasher.

### Fix Recommandé pour Artifact.tsx

```typescript
// AVANT (buggy)
const artifact = artifacts[artifactId];
const actions = useStore(
  computed(artifact.runner.actions, (actions) => { /*...*/ }),
);

// APRÈS (safe)
const artifact = artifacts[artifactId];

// Guard: retourner null si artifact n'existe pas encore
if (!artifact || !artifact.runner) {
  return (
    <div className="artifact border border-bolt-elements-borderColor p-4 rounded-lg">
      <div className="text-bolt-elements-textSecondary">Loading artifact...</div>
    </div>
  );
}

const actions = useStore(
  computed(artifact.runner.actions, (actions) => { /*...*/ }),
);
```

### Workbench Toggle - Code Existant

**Fichier:** `d:\IAFactory\rag-dz\bolt-diy\app\lib\stores\workbench.ts` (ligne 285-287)

```typescript
setShowWorkbench(show: boolean) {
  this.showWorkbench.set(show);
}
```

**Statut:** ✅ Le toggle existe et fonctionne correctement. Le bug n'est pas dans le toggle lui-même mais dans les composants qui accèdent aux artifacts avant qu'ils soient initialisés.

---

## 1.5 Intégrations Bolt/Archon/BMAD

### Bolt.diy

**Localisation:** `d:\IAFactory\rag-dz\bolt-diy\`

**Statut:** ✅ **INTÉGRÉ** (submodule Git)

| Composant | Fichier | Statut |
|-----------|---------|--------|
| Chat UI | `app/components/chat/` | ✅ Fonctionnel |
| Workbench | `app/components/workbench/` | ✅ Fonctionnel |
| WebContainer | `app/lib/webcontainer/` | ✅ Fonctionnel |
| Stores | `app/lib/stores/` | ✅ Fonctionnel |

**Routes Bolt API:**
```
POST /api/chat              # Chat principal
POST /api.netlify-deploy    # Deploy Netlify
POST /api.vercel-deploy     # Deploy Vercel
GET  /api.github-*          # GitHub integration
```

### Archon

**Localisation:** `d:\IAFactory\rag-dz\` (services intégrés)

**Statut:** ✅ **INTÉGRÉ** (submodule Git)

**Services:**
| Service | Fichier | Fonction |
|---------|---------|----------|
| knowledge_item_service.py | services/api/app/services/ | Gestion items KB |
| rag_service.py | services/api/app/services/ | Recherche RAG |
| crawling_service.py | services/api/app/services/ | Web crawling |
| embedding_service.py | services/api/app/services/ | Embeddings |

**Routes Archon:**
```
/api/knowledge/*    # Knowledge base management
/api/rag/*          # RAG queries
/api/crawl/*        # Web crawling
```

### BMAD Method

**Localisation:** `d:\IAFactory\rag-dz\bmad\`

**Statut:** ✅ **INTÉGRÉ** (npm + API)

**Agents Disponibles:**
| Agent ID | Fichier YAML | Rôle |
|----------|--------------|------|
| bmm-architect | architect.agent.yaml | Architecture système |
| bmm-pm | pm.agent.yaml | Product management |
| bmm-developer | dev.agent.yaml | Développement |
| bmm-tester | tea.agent.yaml | Testing |
| bmm-documenter | tech-writer.agent.yaml | Documentation |

**Routes BMAD:**
```python
POST /api/bmad/chat                           # Chat avec agent
GET  /api/bmad/agents/{agent_id}/personality  # Personnalité agent
GET  /api/bmad/chat/health                    # Health check

# SSE Streaming (bmad_openai.py)
POST /api/bmad/v1/chat/completions            # OpenAI-compatible streaming
```

---

# 2. IMPLÉMENTATION CHAT USER↔USER

## 2.1 Database - Nouvelles Tables

**Fichier à créer:** `d:\IAFactory\rag-dz\services\api\migrations\015_chat_multiuser.sql`

```sql
-- Migration 015: Chat Multi-User System
-- ================================================================
-- Tables pour chat temps réel entre utilisateurs
-- Compatible avec le système existant (chat_sessions, chat_messages)

BEGIN;

-- ============================================================
-- ENUM TYPES
-- ============================================================

CREATE TYPE room_type AS ENUM ('direct', 'group', 'project', 'support');
CREATE TYPE member_role AS ENUM ('owner', 'admin', 'member', 'guest');
CREATE TYPE invitation_status AS ENUM ('pending', 'accepted', 'declined', 'expired');

-- ============================================================
-- Table: chat_rooms
-- ============================================================
-- Rooms de conversation (1-to-1, groupes, ou liées à un projet)

CREATE TABLE IF NOT EXISTS chat_rooms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,

    -- Metadata room
    name VARCHAR(100),                          -- NULL pour direct messages
    description TEXT,
    type room_type NOT NULL DEFAULT 'direct',

    -- Lien optionnel vers un projet Bolt
    project_id UUID,                            -- Référence externe (Bolt project)

    -- Créateur
    created_by INTEGER NOT NULL REFERENCES users(id) ON DELETE SET NULL,

    -- Stats
    member_count INTEGER DEFAULT 0,
    message_count INTEGER DEFAULT 0,

    -- Settings
    is_archived BOOLEAN DEFAULT FALSE,
    is_private BOOLEAN DEFAULT TRUE,            -- Visible seulement aux membres
    allow_invites BOOLEAN DEFAULT TRUE,         -- Membres peuvent inviter

    -- Metadata
    avatar_url VARCHAR(500),
    metadata JSONB DEFAULT '{}',

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_activity_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_rooms_tenant ON chat_rooms(tenant_id);
CREATE INDEX idx_rooms_created_by ON chat_rooms(created_by);
CREATE INDEX idx_rooms_project ON chat_rooms(project_id) WHERE project_id IS NOT NULL;
CREATE INDEX idx_rooms_last_activity ON chat_rooms(tenant_id, last_activity_at DESC);
CREATE INDEX idx_rooms_type ON chat_rooms(tenant_id, type);

COMMENT ON TABLE chat_rooms IS 'Rooms de chat multi-utilisateurs';


-- ============================================================
-- Table: chat_room_members
-- ============================================================
-- Membres des rooms avec leurs rôles

CREATE TABLE IF NOT EXISTS chat_room_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID NOT NULL REFERENCES chat_rooms(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Rôle et permissions
    role member_role NOT NULL DEFAULT 'member',
    can_send_messages BOOLEAN DEFAULT TRUE,
    can_invite BOOLEAN DEFAULT FALSE,
    can_remove_members BOOLEAN DEFAULT FALSE,

    -- Notifications
    is_muted BOOLEAN DEFAULT FALSE,
    muted_until TIMESTAMPTZ,

    -- Lecture
    last_read_at TIMESTAMPTZ DEFAULT NOW(),
    last_read_message_id UUID,
    unread_count INTEGER DEFAULT 0,

    -- Timestamps
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    left_at TIMESTAMPTZ,                        -- NULL si toujours membre

    -- Metadata
    nickname VARCHAR(50),                        -- Surnom dans cette room
    metadata JSONB DEFAULT '{}',

    -- Contrainte unique
    UNIQUE(room_id, user_id)
);

-- Indexes
CREATE INDEX idx_members_room ON chat_room_members(room_id);
CREATE INDEX idx_members_user ON chat_room_members(user_id);
CREATE INDEX idx_members_active ON chat_room_members(user_id, left_at) WHERE left_at IS NULL;
CREATE INDEX idx_members_unread ON chat_room_members(user_id, unread_count) WHERE unread_count > 0;

COMMENT ON TABLE chat_room_members IS 'Membres des rooms de chat';


-- ============================================================
-- Table: chat_room_messages
-- ============================================================
-- Messages dans les rooms (distinct de chat_messages qui est USER↔IA)

CREATE TABLE IF NOT EXISTS chat_room_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID NOT NULL REFERENCES chat_rooms(id) ON DELETE CASCADE,
    sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE SET NULL,

    -- Contenu
    content TEXT NOT NULL,
    content_type VARCHAR(20) DEFAULT 'text',     -- 'text', 'file', 'image', 'code', 'artifact', 'system'

    -- Reply
    reply_to_id UUID REFERENCES chat_room_messages(id) ON DELETE SET NULL,

    -- Fichiers/médias
    attachments JSONB DEFAULT '[]',              -- [{url, type, name, size}]

    -- Artifact Bolt (si type='artifact')
    artifact_data JSONB,                         -- {artifact_id, title, type, preview_url}

    -- Mentions
    mentions JSONB DEFAULT '[]',                 -- [{user_id, username, type: 'user'|'agent'}]

    -- Agent BMAD (si mentionné)
    agent_response JSONB,                        -- {agent_id, response, timestamp}

    -- Édition
    is_edited BOOLEAN DEFAULT FALSE,
    edited_at TIMESTAMPTZ,
    original_content TEXT,                       -- Contenu avant édition

    -- Suppression (soft delete)
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMPTZ,
    deleted_by INTEGER REFERENCES users(id),

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),

    -- Metadata
    metadata JSONB DEFAULT '{}'
);

-- Indexes
CREATE INDEX idx_room_messages_room ON chat_room_messages(room_id);
CREATE INDEX idx_room_messages_sender ON chat_room_messages(sender_id);
CREATE INDEX idx_room_messages_created ON chat_room_messages(room_id, created_at DESC);
CREATE INDEX idx_room_messages_reply ON chat_room_messages(reply_to_id) WHERE reply_to_id IS NOT NULL;
CREATE INDEX idx_room_messages_mentions ON chat_room_messages USING GIN (mentions);

COMMENT ON TABLE chat_room_messages IS 'Messages dans les rooms multi-utilisateurs';


-- ============================================================
-- Table: chat_invitations
-- ============================================================
-- Invitations par email pour rejoindre une room

CREATE TABLE IF NOT EXISTS chat_invitations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID NOT NULL REFERENCES chat_rooms(id) ON DELETE CASCADE,

    -- Inviteur
    invited_by INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Invité
    email VARCHAR(255) NOT NULL,
    user_id INTEGER REFERENCES users(id),        -- Rempli si l'email correspond à un user existant

    -- Token
    token VARCHAR(100) UNIQUE NOT NULL,

    -- Status
    status invitation_status DEFAULT 'pending',

    -- Expiration
    expires_at TIMESTAMPTZ NOT NULL,

    -- Message personnalisé
    message TEXT,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    accepted_at TIMESTAMPTZ,

    -- Metadata
    metadata JSONB DEFAULT '{}'
);

-- Indexes
CREATE INDEX idx_invitations_room ON chat_invitations(room_id);
CREATE INDEX idx_invitations_email ON chat_invitations(email);
CREATE INDEX idx_invitations_token ON chat_invitations(token);
CREATE INDEX idx_invitations_status ON chat_invitations(status) WHERE status = 'pending';

COMMENT ON TABLE chat_invitations IS 'Invitations à rejoindre des rooms';


-- ============================================================
-- Table: message_read_receipts
-- ============================================================
-- Accusés de lecture par message

CREATE TABLE IF NOT EXISTS message_read_receipts (
    message_id UUID NOT NULL REFERENCES chat_room_messages(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    read_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (message_id, user_id)
);

-- Index
CREATE INDEX idx_receipts_user ON message_read_receipts(user_id);

COMMENT ON TABLE message_read_receipts IS 'Accusés de lecture des messages';


-- ============================================================
-- Table: typing_indicators (Redis preferred, but DB fallback)
-- ============================================================
-- Indicateurs de frappe (optionnel, Redis est préférable)

CREATE TABLE IF NOT EXISTS typing_indicators (
    room_id UUID NOT NULL REFERENCES chat_rooms(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (room_id, user_id)
);

COMMENT ON TABLE typing_indicators IS 'Indicateurs de frappe (fallback si pas Redis)';


-- ============================================================
-- Table: referral_rewards
-- ============================================================
-- Récompenses pour parrainage

CREATE TABLE IF NOT EXISTS referral_rewards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    referrer_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    referred_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    invitation_id UUID REFERENCES chat_invitations(id) ON DELETE SET NULL,

    -- Reward
    reward_credits INTEGER DEFAULT 100,

    -- Status
    status VARCHAR(20) DEFAULT 'pending',        -- 'pending', 'granted', 'expired'

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    granted_at TIMESTAMPTZ,

    UNIQUE(referrer_id, referred_id)
);

COMMENT ON TABLE referral_rewards IS 'Récompenses de parrainage';


-- ============================================================
-- Row-Level Security (RLS)
-- ============================================================

ALTER TABLE chat_rooms ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_room_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_room_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_invitations ENABLE ROW LEVEL SECURITY;
ALTER TABLE message_read_receipts ENABLE ROW LEVEL SECURITY;

-- Policies: Users can only see rooms they're members of
CREATE POLICY rooms_member_access ON chat_rooms
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM chat_room_members m
            WHERE m.room_id = chat_rooms.id
            AND m.user_id = get_current_user_id()
            AND m.left_at IS NULL
        )
        OR is_superadmin()
    );

-- Policies: Users can see messages in their rooms
CREATE POLICY messages_member_access ON chat_room_messages
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM chat_room_members m
            WHERE m.room_id = chat_room_messages.room_id
            AND m.user_id = get_current_user_id()
            AND m.left_at IS NULL
        )
        OR is_superadmin()
    );

-- Policies: Users can only insert messages in rooms they're members of
CREATE POLICY messages_insert ON chat_room_messages
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM chat_room_members m
            WHERE m.room_id = chat_room_messages.room_id
            AND m.user_id = get_current_user_id()
            AND m.left_at IS NULL
            AND m.can_send_messages = TRUE
        )
    );


-- ============================================================
-- Functions
-- ============================================================

-- Fonction: Créer une room direct message (1-to-1)
CREATE OR REPLACE FUNCTION create_direct_room(
    p_tenant_id UUID,
    p_user1_id INTEGER,
    p_user2_id INTEGER
) RETURNS UUID
LANGUAGE plpgsql
AS $$
DECLARE
    v_room_id UUID;
    v_existing_room_id UUID;
BEGIN
    -- Vérifier si une room DM existe déjà entre ces 2 users
    SELECT r.id INTO v_existing_room_id
    FROM chat_rooms r
    JOIN chat_room_members m1 ON m1.room_id = r.id AND m1.user_id = p_user1_id
    JOIN chat_room_members m2 ON m2.room_id = r.id AND m2.user_id = p_user2_id
    WHERE r.type = 'direct'
    AND r.tenant_id = p_tenant_id
    AND r.member_count = 2
    LIMIT 1;

    IF v_existing_room_id IS NOT NULL THEN
        RETURN v_existing_room_id;
    END IF;

    -- Créer nouvelle room
    INSERT INTO chat_rooms (tenant_id, type, created_by, member_count, is_private)
    VALUES (p_tenant_id, 'direct', p_user1_id, 2, TRUE)
    RETURNING id INTO v_room_id;

    -- Ajouter les 2 membres
    INSERT INTO chat_room_members (room_id, user_id, role)
    VALUES
        (v_room_id, p_user1_id, 'owner'),
        (v_room_id, p_user2_id, 'member');

    RETURN v_room_id;
END;
$$;

-- Fonction: Ajouter un membre à une room
CREATE OR REPLACE FUNCTION add_room_member(
    p_room_id UUID,
    p_user_id INTEGER,
    p_role member_role DEFAULT 'member'
) RETURNS UUID
LANGUAGE plpgsql
AS $$
DECLARE
    v_member_id UUID;
BEGIN
    -- Vérifier si déjà membre
    SELECT id INTO v_member_id
    FROM chat_room_members
    WHERE room_id = p_room_id AND user_id = p_user_id;

    IF v_member_id IS NOT NULL THEN
        -- Réactiver si avait quitté
        UPDATE chat_room_members
        SET left_at = NULL, role = p_role
        WHERE id = v_member_id;
        RETURN v_member_id;
    END IF;

    -- Ajouter nouveau membre
    INSERT INTO chat_room_members (room_id, user_id, role)
    VALUES (p_room_id, p_user_id, p_role)
    RETURNING id INTO v_member_id;

    -- Mettre à jour le compteur
    UPDATE chat_rooms SET member_count = member_count + 1 WHERE id = p_room_id;

    RETURN v_member_id;
END;
$$;

-- Fonction: Envoyer un message
CREATE OR REPLACE FUNCTION send_room_message(
    p_room_id UUID,
    p_sender_id INTEGER,
    p_content TEXT,
    p_content_type VARCHAR DEFAULT 'text',
    p_reply_to_id UUID DEFAULT NULL,
    p_attachments JSONB DEFAULT '[]',
    p_mentions JSONB DEFAULT '[]'
) RETURNS UUID
LANGUAGE plpgsql
AS $$
DECLARE
    v_message_id UUID;
BEGIN
    -- Vérifier que l'user est membre
    IF NOT EXISTS (
        SELECT 1 FROM chat_room_members
        WHERE room_id = p_room_id
        AND user_id = p_sender_id
        AND left_at IS NULL
        AND can_send_messages = TRUE
    ) THEN
        RAISE EXCEPTION 'User is not a member of this room or cannot send messages';
    END IF;

    -- Insérer le message
    INSERT INTO chat_room_messages (
        room_id, sender_id, content, content_type,
        reply_to_id, attachments, mentions
    ) VALUES (
        p_room_id, p_sender_id, p_content, p_content_type,
        p_reply_to_id, p_attachments, p_mentions
    )
    RETURNING id INTO v_message_id;

    -- Mettre à jour la room
    UPDATE chat_rooms
    SET message_count = message_count + 1,
        last_activity_at = NOW(),
        updated_at = NOW()
    WHERE id = p_room_id;

    -- Incrémenter unread_count pour tous les autres membres
    UPDATE chat_room_members
    SET unread_count = unread_count + 1
    WHERE room_id = p_room_id
    AND user_id != p_sender_id
    AND left_at IS NULL;

    RETURN v_message_id;
END;
$$;

-- Fonction: Marquer les messages comme lus
CREATE OR REPLACE FUNCTION mark_messages_read(
    p_room_id UUID,
    p_user_id INTEGER,
    p_up_to_message_id UUID DEFAULT NULL
) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_count INTEGER;
BEGIN
    -- Si pas de message_id spécifié, prendre le dernier
    IF p_up_to_message_id IS NULL THEN
        SELECT id INTO p_up_to_message_id
        FROM chat_room_messages
        WHERE room_id = p_room_id
        ORDER BY created_at DESC
        LIMIT 1;
    END IF;

    -- Mettre à jour le membre
    UPDATE chat_room_members
    SET last_read_at = NOW(),
        last_read_message_id = p_up_to_message_id,
        unread_count = 0
    WHERE room_id = p_room_id
    AND user_id = p_user_id
    RETURNING 1 INTO v_count;

    RETURN COALESCE(v_count, 0);
END;
$$;


-- ============================================================
-- Views
-- ============================================================

-- Vue: Rooms avec dernier message
CREATE OR REPLACE VIEW room_previews AS
SELECT
    r.id,
    r.tenant_id,
    r.name,
    r.type,
    r.member_count,
    r.message_count,
    r.last_activity_at,
    r.is_archived,
    r.avatar_url,
    m.user_id as current_user_id,
    m.unread_count,
    m.is_muted,
    (
        SELECT content
        FROM chat_room_messages msg
        WHERE msg.room_id = r.id AND msg.is_deleted = FALSE
        ORDER BY msg.created_at DESC
        LIMIT 1
    ) as last_message_content,
    (
        SELECT sender_id
        FROM chat_room_messages msg
        WHERE msg.room_id = r.id AND msg.is_deleted = FALSE
        ORDER BY msg.created_at DESC
        LIMIT 1
    ) as last_message_sender_id,
    (
        SELECT created_at
        FROM chat_room_messages msg
        WHERE msg.room_id = r.id AND msg.is_deleted = FALSE
        ORDER BY msg.created_at DESC
        LIMIT 1
    ) as last_message_at
FROM chat_rooms r
JOIN chat_room_members m ON m.room_id = r.id AND m.left_at IS NULL;

COMMENT ON VIEW room_previews IS 'Aperçu des rooms avec dernier message et unread count';


-- ============================================================
-- Triggers
-- ============================================================

-- Trigger: Auto-update updated_at pour chat_rooms
CREATE TRIGGER tr_rooms_updated
    BEFORE UPDATE ON chat_rooms
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();


COMMIT;
```

---

## 2.2 Backend - Routes FastAPI

**Fichier à créer:** `d:\IAFactory\rag-dz\services\api\app\routers\chat_rooms.py`

```python
"""
Chat Rooms Router - API pour chat multi-utilisateurs temps réel
"""

import os
import logging
import secrets
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from pydantic import BaseModel, EmailStr, Field
from asyncpg import Pool

from ..dependencies import get_current_user, get_db_pool
from ..models.user import UserInDB
from ..websocket import manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat/rooms", tags=["chat-rooms"])


# ============================================================
# Pydantic Models
# ============================================================

class RoomCreate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    type: str = Field(default="group", pattern="^(direct|group|project|support)$")
    project_id: Optional[UUID] = None
    description: Optional[str] = None
    is_private: bool = True
    member_ids: List[int] = Field(default_factory=list)


class RoomResponse(BaseModel):
    id: UUID
    name: Optional[str]
    type: str
    member_count: int
    message_count: int
    is_archived: bool
    is_private: bool
    created_at: datetime
    last_activity_at: datetime
    unread_count: Optional[int] = 0


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)
    content_type: str = Field(default="text")
    reply_to_id: Optional[UUID] = None
    attachments: List[dict] = Field(default_factory=list)
    mentions: List[dict] = Field(default_factory=list)


class MessageResponse(BaseModel):
    id: UUID
    room_id: UUID
    sender_id: int
    sender_name: Optional[str]
    content: str
    content_type: str
    reply_to_id: Optional[UUID]
    attachments: List[dict]
    mentions: List[dict]
    is_edited: bool
    created_at: datetime


class MemberResponse(BaseModel):
    id: UUID
    user_id: int
    user_name: Optional[str]
    user_email: str
    role: str
    joined_at: datetime
    is_muted: bool
    unread_count: int


class InvitationCreate(BaseModel):
    email: EmailStr
    message: Optional[str] = None


class InvitationResponse(BaseModel):
    id: UUID
    email: str
    status: str
    token: str
    expires_at: datetime
    created_at: datetime


# ============================================================
# Room Endpoints
# ============================================================

@router.post("", response_model=RoomResponse)
async def create_room(
    room: RoomCreate,
    db: Pool = Depends(get_db_pool),
    current_user: UserInDB = Depends(get_current_user)
):
    """Créer une nouvelle room de chat"""
    async with db.acquire() as conn:
        # Créer la room
        row = await conn.fetchrow("""
            INSERT INTO chat_rooms (tenant_id, name, type, description, project_id,
                                    created_by, is_private, member_count)
            VALUES ($1, $2, $3, $4, $5, $6, $7, 1)
            RETURNING id, name, type, member_count, message_count, is_archived,
                      is_private, created_at, last_activity_at
        """, current_user.tenant_id, room.name, room.type, room.description,
             room.project_id, current_user.id, room.is_private)

        room_id = row['id']

        # Ajouter le créateur comme owner
        await conn.execute("""
            INSERT INTO chat_room_members (room_id, user_id, role, can_invite, can_remove_members)
            VALUES ($1, $2, 'owner', TRUE, TRUE)
        """, room_id, current_user.id)

        # Ajouter les autres membres
        for member_id in room.member_ids:
            if member_id != current_user.id:
                await conn.execute("""
                    SELECT add_room_member($1, $2, 'member')
                """, room_id, member_id)

        return RoomResponse(**dict(row), unread_count=0)


@router.get("", response_model=List[RoomResponse])
async def list_rooms(
    archived: bool = False,
    limit: int = Query(default=50, le=100),
    offset: int = 0,
    db: Pool = Depends(get_db_pool),
    current_user: UserInDB = Depends(get_current_user)
):
    """Lister les rooms de l'utilisateur"""
    async with db.acquire() as conn:
        rows = await conn.fetch("""
            SELECT r.id, r.name, r.type, r.member_count, r.message_count,
                   r.is_archived, r.is_private, r.created_at, r.last_activity_at,
                   m.unread_count
            FROM chat_rooms r
            JOIN chat_room_members m ON m.room_id = r.id
            WHERE m.user_id = $1
            AND m.left_at IS NULL
            AND r.is_archived = $2
            ORDER BY r.last_activity_at DESC
            LIMIT $3 OFFSET $4
        """, current_user.id, archived, limit, offset)

        return [RoomResponse(**dict(row)) for row in rows]


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: UUID,
    db: Pool = Depends(get_db_pool),
    current_user: UserInDB = Depends(get_current_user)
):
    """Obtenir les détails d'une room"""
    async with db.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT r.id, r.name, r.type, r.member_count, r.message_count,
                   r.is_archived, r.is_private, r.created_at, r.last_activity_at,
                   m.unread_count
            FROM chat_rooms r
            JOIN chat_room_members m ON m.room_id = r.id
            WHERE r.id = $1 AND m.user_id = $2 AND m.left_at IS NULL
        """, room_id, current_user.id)

        if not row:
            raise HTTPException(status_code=404, detail="Room not found")

        return RoomResponse(**dict(row))


@router.post("/direct/{user_id}", response_model=RoomResponse)
async def create_or_get_direct_room(
    user_id: int,
    db: Pool = Depends(get_db_pool),
    current_user: UserInDB = Depends(get_current_user)
):
    """Créer ou récupérer une room de message direct"""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot create DM with yourself")

    async with db.acquire() as conn:
        # Utiliser la fonction SQL
        room_id = await conn.fetchval("""
            SELECT create_direct_room($1, $2, $3)
        """, current_user.tenant_id, current_user.id, user_id)

        # Récupérer les détails
        row = await conn.fetchrow("""
            SELECT r.id, r.name, r.type, r.member_count, r.message_count,
                   r.is_archived, r.is_private, r.created_at, r.last_activity_at,
                   m.unread_count
            FROM chat_rooms r
            JOIN chat_room_members m ON m.room_id = r.id
            WHERE r.id = $1 AND m.user_id = $2
        """, room_id, current_user.id)

        return RoomResponse(**dict(row))


# ============================================================
# Message Endpoints
# ============================================================

@router.get("/{room_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    room_id: UUID,
    limit: int = Query(default=50, le=100),
    before: Optional[datetime] = None,
    db: Pool = Depends(get_db_pool),
    current_user: UserInDB = Depends(get_current_user)
):
    """Récupérer les messages d'une room (pagination)"""
    async with db.acquire() as conn:
        # Vérifier membership
        is_member = await conn.fetchval("""
            SELECT 1 FROM chat_room_members
            WHERE room_id = $1 AND user_id = $2 AND left_at IS NULL
        """, room_id, current_user.id)

        if not is_member:
            raise HTTPException(status_code=403, detail="Not a member of this room")

        # Query messages
        if before:
            rows = await conn.fetch("""
                SELECT m.id, m.room_id, m.sender_id, u.full_name as sender_name,
                       m.content, m.content_type, m.reply_to_id, m.attachments,
                       m.mentions, m.is_edited, m.created_at
                FROM chat_room_messages m
                LEFT JOIN users u ON u.id = m.sender_id
                WHERE m.room_id = $1 AND m.is_deleted = FALSE AND m.created_at < $2
                ORDER BY m.created_at DESC
                LIMIT $3
            """, room_id, before, limit)
        else:
            rows = await conn.fetch("""
                SELECT m.id, m.room_id, m.sender_id, u.full_name as sender_name,
                       m.content, m.content_type, m.reply_to_id, m.attachments,
                       m.mentions, m.is_edited, m.created_at
                FROM chat_room_messages m
                LEFT JOIN users u ON u.id = m.sender_id
                WHERE m.room_id = $1 AND m.is_deleted = FALSE
                ORDER BY m.created_at DESC
                LIMIT $2
            """, room_id, limit)

        return [MessageResponse(**dict(row)) for row in reversed(rows)]


@router.post("/{room_id}/messages", response_model=MessageResponse)
async def send_message(
    room_id: UUID,
    message: MessageCreate,
    background_tasks: BackgroundTasks,
    db: Pool = Depends(get_db_pool),
    current_user: UserInDB = Depends(get_current_user)
):
    """Envoyer un message dans une room"""
    async with db.acquire() as conn:
        try:
            # Utiliser la fonction SQL pour validation + insertion
            message_id = await conn.fetchval("""
                SELECT send_room_message($1, $2, $3, $4, $5, $6, $7)
            """, room_id, current_user.id, message.content, message.content_type,
                 message.reply_to_id,
                 message.attachments if message.attachments else [],
                 message.mentions if message.mentions else [])
        except Exception as e:
            if "not a member" in str(e).lower():
                raise HTTPException(status_code=403, detail="Not a member of this room")
            raise HTTPException(status_code=500, detail=str(e))

        # Récupérer le message créé
        row = await conn.fetchrow("""
            SELECT m.id, m.room_id, m.sender_id, u.full_name as sender_name,
                   m.content, m.content_type, m.reply_to_id, m.attachments,
                   m.mentions, m.is_edited, m.created_at
            FROM chat_room_messages m
            LEFT JOIN users u ON u.id = m.sender_id
            WHERE m.id = $1
        """, message_id)

        response = MessageResponse(**dict(row))

        # Broadcast via WebSocket (background task)
        background_tasks.add_task(
            broadcast_message,
            room_id,
            response.dict(),
            current_user.tenant_id
        )

        # Traiter les mentions d'agents BMAD (background task)
        agent_mentions = [m for m in message.mentions if m.get('type') == 'agent']
        if agent_mentions:
            background_tasks.add_task(
                process_agent_mentions,
                room_id, message_id, message.content, agent_mentions, db
            )

        return response


@router.post("/{room_id}/read")
async def mark_as_read(
    room_id: UUID,
    message_id: Optional[UUID] = None,
    db: Pool = Depends(get_db_pool),
    current_user: UserInDB = Depends(get_current_user)
):
    """Marquer les messages comme lus"""
    async with db.acquire() as conn:
        count = await conn.fetchval("""
            SELECT mark_messages_read($1, $2, $3)
        """, room_id, current_user.id, message_id)

        return {"marked_read": count}


# ============================================================
# Member Endpoints
# ============================================================

@router.get("/{room_id}/members", response_model=List[MemberResponse])
async def get_members(
    room_id: UUID,
    db: Pool = Depends(get_db_pool),
    current_user: UserInDB = Depends(get_current_user)
):
    """Lister les membres d'une room"""
    async with db.acquire() as conn:
        rows = await conn.fetch("""
            SELECT m.id, m.user_id, u.full_name as user_name, u.email as user_email,
                   m.role, m.joined_at, m.is_muted, m.unread_count
            FROM chat_room_members m
            JOIN users u ON u.id = m.user_id
            WHERE m.room_id = $1 AND m.left_at IS NULL
            ORDER BY m.joined_at
        """, room_id)

        return [MemberResponse(**dict(row)) for row in rows]


@router.post("/{room_id}/members/{user_id}")
async def add_member(
    room_id: UUID,
    user_id: int,
    db: Pool = Depends(get_db_pool),
    current_user: UserInDB = Depends(get_current_user)
):
    """Ajouter un membre à une room"""
    async with db.acquire() as conn:
        # Vérifier permissions
        can_invite = await conn.fetchval("""
            SELECT can_invite FROM chat_room_members
            WHERE room_id = $1 AND user_id = $2 AND left_at IS NULL
        """, room_id, current_user.id)

        if not can_invite:
            raise HTTPException(status_code=403, detail="No permission to invite")

        # Ajouter le membre
        member_id = await conn.fetchval("""
            SELECT add_room_member($1, $2, 'member')
        """, room_id, user_id)

        return {"member_id": str(member_id)}


@router.delete("/{room_id}/members/{user_id}")
async def remove_member(
    room_id: UUID,
    user_id: int,
    db: Pool = Depends(get_db_pool),
    current_user: UserInDB = Depends(get_current_user)
):
    """Retirer un membre d'une room"""
    async with db.acquire() as conn:
        # Vérifier permissions (ou self-leave)
        if user_id != current_user.id:
            can_remove = await conn.fetchval("""
                SELECT can_remove_members FROM chat_room_members
                WHERE room_id = $1 AND user_id = $2 AND left_at IS NULL
            """, room_id, current_user.id)

            if not can_remove:
                raise HTTPException(status_code=403, detail="No permission to remove members")

        # Marquer comme parti
        await conn.execute("""
            UPDATE chat_room_members
            SET left_at = NOW()
            WHERE room_id = $1 AND user_id = $2
        """, room_id, user_id)

        # Décrémenter le compteur
        await conn.execute("""
            UPDATE chat_rooms SET member_count = member_count - 1 WHERE id = $1
        """, room_id)

        return {"removed": True}


# ============================================================
# Invitation Endpoints
# ============================================================

@router.post("/{room_id}/invite", response_model=InvitationResponse)
async def invite_by_email(
    room_id: UUID,
    invitation: InvitationCreate,
    background_tasks: BackgroundTasks,
    db: Pool = Depends(get_db_pool),
    current_user: UserInDB = Depends(get_current_user)
):
    """Inviter un utilisateur par email"""
    async with db.acquire() as conn:
        # Vérifier permissions
        can_invite = await conn.fetchval("""
            SELECT can_invite FROM chat_room_members
            WHERE room_id = $1 AND user_id = $2 AND left_at IS NULL
        """, room_id, current_user.id)

        if not can_invite:
            raise HTTPException(status_code=403, detail="No permission to invite")

        # Vérifier si l'email est déjà invité
        existing = await conn.fetchval("""
            SELECT id FROM chat_invitations
            WHERE room_id = $1 AND email = $2 AND status = 'pending'
        """, room_id, invitation.email)

        if existing:
            raise HTTPException(status_code=400, detail="User already invited")

        # Générer token
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=7)

        # Vérifier si l'email correspond à un user existant
        user_id = await conn.fetchval("""
            SELECT id FROM users WHERE email = $1
        """, invitation.email)

        # Créer l'invitation
        row = await conn.fetchrow("""
            INSERT INTO chat_invitations (room_id, invited_by, email, user_id, token, expires_at, message)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id, email, status, token, expires_at, created_at
        """, room_id, current_user.id, invitation.email, user_id, token, expires_at, invitation.message)

        # Envoyer l'email (background)
        background_tasks.add_task(
            send_invitation_email,
            invitation.email, token, current_user.full_name, invitation.message
        )

        return InvitationResponse(**dict(row))


@router.get("/invitations/{token}")
async def get_invitation_by_token(
    token: str,
    db: Pool = Depends(get_db_pool)
):
    """Vérifier une invitation par token (public)"""
    async with db.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT i.id, i.room_id, i.email, i.status, i.expires_at,
                   r.name as room_name, r.type as room_type,
                   u.full_name as inviter_name
            FROM chat_invitations i
            JOIN chat_rooms r ON r.id = i.room_id
            JOIN users u ON u.id = i.invited_by
            WHERE i.token = $1
        """, token)

        if not row:
            raise HTTPException(status_code=404, detail="Invitation not found")

        if row['status'] != 'pending':
            raise HTTPException(status_code=400, detail=f"Invitation already {row['status']}")

        if row['expires_at'] < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Invitation expired")

        return dict(row)


@router.post("/invitations/{token}/accept")
async def accept_invitation(
    token: str,
    db: Pool = Depends(get_db_pool),
    current_user: UserInDB = Depends(get_current_user)
):
    """Accepter une invitation"""
    async with db.acquire() as conn:
        # Récupérer l'invitation
        inv = await conn.fetchrow("""
            SELECT id, room_id, email, invited_by FROM chat_invitations
            WHERE token = $1 AND status = 'pending' AND expires_at > NOW()
        """, token)

        if not inv:
            raise HTTPException(status_code=404, detail="Invalid or expired invitation")

        # Vérifier que l'email correspond
        if inv['email'].lower() != current_user.email.lower():
            raise HTTPException(status_code=403, detail="Invitation is for a different email")

        # Accepter l'invitation
        await conn.execute("""
            UPDATE chat_invitations
            SET status = 'accepted', accepted_at = NOW()
            WHERE id = $1
        """, inv['id'])

        # Ajouter comme membre
        await conn.fetchval("""
            SELECT add_room_member($1, $2, 'member')
        """, inv['room_id'], current_user.id)

        # Créer récompense parrainage
        await conn.execute("""
            INSERT INTO referral_rewards (referrer_id, referred_id, invitation_id, reward_credits)
            VALUES ($1, $2, $3, 100)
            ON CONFLICT (referrer_id, referred_id) DO NOTHING
        """, inv['invited_by'], current_user.id, inv['id'])

        return {"accepted": True, "room_id": str(inv['room_id'])}


# ============================================================
# Typing Indicator Endpoint
# ============================================================

@router.post("/{room_id}/typing")
async def send_typing_indicator(
    room_id: UUID,
    is_typing: bool = True,
    current_user: UserInDB = Depends(get_current_user)
):
    """Envoyer un indicateur de frappe"""
    # Broadcast via WebSocket
    await manager.broadcast_to_tenant(
        str(current_user.tenant_id),
        {
            "type": "typing",
            "room_id": str(room_id),
            "user_id": current_user.id,
            "user_name": current_user.full_name,
            "is_typing": is_typing
        }
    )
    return {"sent": True}


# ============================================================
# Helper Functions
# ============================================================

async def broadcast_message(room_id: UUID, message: dict, tenant_id: UUID):
    """Broadcast un message via WebSocket"""
    await manager.broadcast_to_tenant(
        str(tenant_id),
        {
            "type": "message",
            "room_id": str(room_id),
            "message": message
        }
    )


async def send_invitation_email(email: str, token: str, inviter_name: str, message: str = None):
    """Envoyer un email d'invitation"""
    # TODO: Intégrer avec service email (SendGrid, etc.)
    base_url = os.getenv("APP_URL", "https://app.iafactory.io")
    invite_url = f"{base_url}/invite/{token}"

    logger.info(f"Invitation email to {email}: {invite_url}")
    # email_service.send(to=email, template="invitation", data={...})


async def process_agent_mentions(
    room_id: UUID,
    message_id: UUID,
    content: str,
    mentions: List[dict],
    db: Pool
):
    """Traiter les mentions d'agents BMAD dans un message"""
    from .bmad_chat import load_agent_personality, get_llm_client

    for mention in mentions:
        agent_id = mention.get('id')
        if not agent_id:
            continue

        try:
            # Charger la personnalité de l'agent
            system_prompt = load_agent_personality(agent_id)
            client, model = get_llm_client()

            # Générer la réponse
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ],
                max_tokens=1024,
                temperature=0.7
            )

            agent_response = response.choices[0].message.content

            # Sauvegarder la réponse de l'agent dans le message original
            async with db.acquire() as conn:
                await conn.execute("""
                    UPDATE chat_room_messages
                    SET agent_response = $1
                    WHERE id = $2
                """, {"agent_id": agent_id, "response": agent_response}, message_id)

                # Créer un nouveau message de l'agent
                await conn.fetchval("""
                    INSERT INTO chat_room_messages (
                        room_id, sender_id, content, content_type, reply_to_id, metadata
                    ) VALUES (
                        $1, NULL, $2, 'agent', $3, $4
                    )
                """, room_id, agent_response, message_id,
                     {"agent_id": agent_id, "agent_name": agent_id.replace("bmm-", "")})

            logger.info(f"Agent {agent_id} responded in room {room_id}")

        except Exception as e:
            logger.error(f"Error processing agent mention {agent_id}: {e}")
```

---

## 2.3 Backend - WebSocket Étendu

**Fichier à modifier:** `d:\IAFactory\rag-dz\services\api\app\websocket.py`

```python
"""
WebSocket support for real-time updates - Extended for Multi-User Chat
"""
import logging
import json
from typing import Dict, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect
from dataclasses import dataclass, asdict, field
from datetime import datetime
from uuid import UUID

logger = logging.getLogger(__name__)


@dataclass
class ProgressUpdate:
    """Progress update message"""
    operation_id: str
    status: str
    progress: int
    message: str
    data: Dict = None
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self):
        result = asdict(self)
        if result['data'] is None:
            result['data'] = {}
        return result


@dataclass
class UserConnection:
    """Représente une connexion utilisateur"""
    websocket: WebSocket
    user_id: int
    tenant_id: str
    rooms: Set[str] = field(default_factory=set)
    connected_at: datetime = field(default_factory=datetime.utcnow)


class ConnectionManager:
    """Manage WebSocket connections - Extended for rooms"""

    def __init__(self):
        # tenant_id -> Set of WebSocket connections
        self.tenant_connections: Dict[str, Set[WebSocket]] = {}

        # room_id -> Set of WebSocket connections
        self.room_connections: Dict[str, Set[WebSocket]] = {}

        # websocket -> UserConnection (for reverse lookup)
        self.connections: Dict[WebSocket, UserConnection] = {}

        # user_id -> Set of WebSocket connections (multi-device support)
        self.user_connections: Dict[int, Set[WebSocket]] = {}

    async def connect(
        self,
        websocket: WebSocket,
        tenant_id: str,
        user_id: Optional[int] = None
    ):
        """Accept and store WebSocket connection"""
        await websocket.accept()

        # Tenant connections
        if tenant_id not in self.tenant_connections:
            self.tenant_connections[tenant_id] = set()
        self.tenant_connections[tenant_id].add(websocket)

        # User connections
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = set()
            self.user_connections[user_id].add(websocket)

            # Store connection info
            self.connections[websocket] = UserConnection(
                websocket=websocket,
                user_id=user_id,
                tenant_id=tenant_id
            )

        logger.info(f"WebSocket connected: tenant={tenant_id}, user={user_id}")

    def disconnect(self, websocket: WebSocket, tenant_id: str):
        """Remove WebSocket connection"""
        # Remove from tenant
        if tenant_id in self.tenant_connections:
            self.tenant_connections[tenant_id].discard(websocket)
            if not self.tenant_connections[tenant_id]:
                del self.tenant_connections[tenant_id]

        # Remove from user connections
        conn = self.connections.get(websocket)
        if conn:
            if conn.user_id in self.user_connections:
                self.user_connections[conn.user_id].discard(websocket)
                if not self.user_connections[conn.user_id]:
                    del self.user_connections[conn.user_id]

            # Remove from all rooms
            for room_id in conn.rooms:
                if room_id in self.room_connections:
                    self.room_connections[room_id].discard(websocket)

            del self.connections[websocket]

        logger.info(f"WebSocket disconnected: tenant={tenant_id}")

    async def join_room(self, websocket: WebSocket, room_id: str):
        """Ajouter une connexion à une room"""
        if room_id not in self.room_connections:
            self.room_connections[room_id] = set()
        self.room_connections[room_id].add(websocket)

        conn = self.connections.get(websocket)
        if conn:
            conn.rooms.add(room_id)

        logger.debug(f"WebSocket joined room {room_id}")

    async def leave_room(self, websocket: WebSocket, room_id: str):
        """Retirer une connexion d'une room"""
        if room_id in self.room_connections:
            self.room_connections[room_id].discard(websocket)
            if not self.room_connections[room_id]:
                del self.room_connections[room_id]

        conn = self.connections.get(websocket)
        if conn:
            conn.rooms.discard(room_id)

        logger.debug(f"WebSocket left room {room_id}")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific connection"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {e}")

    async def send_to_user(self, user_id: int, message: dict):
        """Send message to all connections of a user"""
        if user_id not in self.user_connections:
            return

        disconnected = set()
        for connection in self.user_connections[user_id]:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)

        # Clean up
        for connection in disconnected:
            conn = self.connections.get(connection)
            if conn:
                self.disconnect(connection, conn.tenant_id)

    async def broadcast_to_tenant(self, tenant_id: str, message: dict):
        """Broadcast message to all connections of a tenant"""
        if tenant_id not in self.tenant_connections:
            return

        disconnected = set()
        for connection in self.tenant_connections[tenant_id]:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected.add(connection)
            except Exception as e:
                logger.error(f"Error broadcasting to tenant {tenant_id}: {e}")
                disconnected.add(connection)

        for connection in disconnected:
            self.disconnect(connection, tenant_id)

    async def broadcast_to_room(self, room_id: str, message: dict, exclude: WebSocket = None):
        """Broadcast message to all connections in a room"""
        if room_id not in self.room_connections:
            return

        disconnected = set()
        for connection in self.room_connections[room_id]:
            if connection == exclude:
                continue
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to room {room_id}: {e}")
                disconnected.add(connection)

        # Clean up
        for connection in disconnected:
            conn = self.connections.get(connection)
            if conn:
                self.disconnect(connection, conn.tenant_id)

    async def send_progress_update(
        self,
        tenant_id: str,
        operation_id: str,
        status: str,
        progress: int,
        message: str,
        data: Dict = None
    ):
        """Send progress update to tenant"""
        update = ProgressUpdate(
            operation_id=operation_id,
            status=status,
            progress=progress,
            message=message,
            data=data or {}
        )
        await self.broadcast_to_tenant(tenant_id, update.to_dict())

    def get_room_members_online(self, room_id: str) -> Set[int]:
        """Get online user IDs in a room"""
        if room_id not in self.room_connections:
            return set()

        user_ids = set()
        for connection in self.room_connections[room_id]:
            conn = self.connections.get(connection)
            if conn:
                user_ids.add(conn.user_id)
        return user_ids

    def is_user_online(self, user_id: int) -> bool:
        """Check if a user has any active connections"""
        return user_id in self.user_connections and len(self.user_connections[user_id]) > 0


# Global connection manager
manager = ConnectionManager()
```

---

## 2.4 Frontend - Composants React

**Fichiers à créer dans:** `d:\IAFactory\rag-dz\bolt-diy\app\components\chat-multi\`

### Types TypeScript

**Fichier:** `types.ts`

```typescript
// Types pour le chat multi-utilisateurs

export interface ChatRoom {
  id: string;
  name: string | null;
  type: 'direct' | 'group' | 'project' | 'support';
  memberCount: number;
  messageCount: number;
  isArchived: boolean;
  isPrivate: boolean;
  createdAt: string;
  lastActivityAt: string;
  unreadCount: number;
}

export interface ChatMessage {
  id: string;
  roomId: string;
  senderId: number;
  senderName: string | null;
  content: string;
  contentType: 'text' | 'file' | 'image' | 'code' | 'artifact' | 'system' | 'agent';
  replyToId: string | null;
  attachments: Attachment[];
  mentions: Mention[];
  isEdited: boolean;
  createdAt: string;
  agentResponse?: AgentResponse;
}

export interface Attachment {
  url: string;
  type: string;
  name: string;
  size: number;
}

export interface Mention {
  id: string;
  name: string;
  type: 'user' | 'agent';
}

export interface AgentResponse {
  agentId: string;
  response: string;
  timestamp: string;
}

export interface RoomMember {
  id: string;
  userId: number;
  userName: string | null;
  userEmail: string;
  role: 'owner' | 'admin' | 'member' | 'guest';
  joinedAt: string;
  isMuted: boolean;
  unreadCount: number;
}

export interface Invitation {
  id: string;
  email: string;
  status: 'pending' | 'accepted' | 'declined' | 'expired';
  token: string;
  expiresAt: string;
  createdAt: string;
}

export interface TypingUser {
  userId: number;
  userName: string;
  startedAt: number;
}

export interface WebSocketMessage {
  type: 'message' | 'typing' | 'presence' | 'room_update' | 'error';
  roomId?: string;
  data: any;
}

// BMAD Agents disponibles pour @mention
export const BMAD_AGENTS: Mention[] = [
  { id: 'bmm-architect', name: 'Architect', type: 'agent' },
  { id: 'bmm-pm', name: 'PM', type: 'agent' },
  { id: 'bmm-developer', name: 'Developer', type: 'agent' },
  { id: 'bmm-tester', name: 'Tester', type: 'agent' },
  { id: 'bmm-documenter', name: 'Writer', type: 'agent' },
];
```

### Store Zustand

**Fichier:** `store.ts`

```typescript
import { create } from 'zustand';
import type { ChatRoom, ChatMessage, RoomMember, TypingUser } from './types';

interface ChatState {
  // Rooms
  rooms: ChatRoom[];
  currentRoomId: string | null;

  // Messages
  messagesByRoom: Record<string, ChatMessage[]>;

  // Members
  membersByRoom: Record<string, RoomMember[]>;

  // Typing
  typingByRoom: Record<string, TypingUser[]>;

  // WebSocket
  wsConnected: boolean;

  // Actions
  setRooms: (rooms: ChatRoom[]) => void;
  addRoom: (room: ChatRoom) => void;
  setCurrentRoom: (roomId: string | null) => void;
  setMessages: (roomId: string, messages: ChatMessage[]) => void;
  addMessage: (roomId: string, message: ChatMessage) => void;
  setMembers: (roomId: string, members: RoomMember[]) => void;
  setTyping: (roomId: string, users: TypingUser[]) => void;
  addTypingUser: (roomId: string, user: TypingUser) => void;
  removeTypingUser: (roomId: string, userId: number) => void;
  setWsConnected: (connected: boolean) => void;
  markRoomAsRead: (roomId: string) => void;
}

export const useChatStore = create<ChatState>((set) => ({
  rooms: [],
  currentRoomId: null,
  messagesByRoom: {},
  membersByRoom: {},
  typingByRoom: {},
  wsConnected: false,

  setRooms: (rooms) => set({ rooms }),

  addRoom: (room) => set((state) => ({
    rooms: [room, ...state.rooms.filter(r => r.id !== room.id)]
  })),

  setCurrentRoom: (roomId) => set({ currentRoomId: roomId }),

  setMessages: (roomId, messages) => set((state) => ({
    messagesByRoom: { ...state.messagesByRoom, [roomId]: messages }
  })),

  addMessage: (roomId, message) => set((state) => ({
    messagesByRoom: {
      ...state.messagesByRoom,
      [roomId]: [...(state.messagesByRoom[roomId] || []), message]
    },
    rooms: state.rooms.map(r =>
      r.id === roomId
        ? { ...r, messageCount: r.messageCount + 1, lastActivityAt: message.createdAt }
        : r
    )
  })),

  setMembers: (roomId, members) => set((state) => ({
    membersByRoom: { ...state.membersByRoom, [roomId]: members }
  })),

  setTyping: (roomId, users) => set((state) => ({
    typingByRoom: { ...state.typingByRoom, [roomId]: users }
  })),

  addTypingUser: (roomId, user) => set((state) => ({
    typingByRoom: {
      ...state.typingByRoom,
      [roomId]: [...(state.typingByRoom[roomId] || []).filter(u => u.userId !== user.userId), user]
    }
  })),

  removeTypingUser: (roomId, userId) => set((state) => ({
    typingByRoom: {
      ...state.typingByRoom,
      [roomId]: (state.typingByRoom[roomId] || []).filter(u => u.userId !== userId)
    }
  })),

  setWsConnected: (connected) => set({ wsConnected: connected }),

  markRoomAsRead: (roomId) => set((state) => ({
    rooms: state.rooms.map(r =>
      r.id === roomId ? { ...r, unreadCount: 0 } : r
    )
  })),
}));
```

### Hook WebSocket

**Fichier:** `hooks/useWebSocket.ts`

```typescript
import { useEffect, useRef, useCallback } from 'react';
import { useChatStore } from '../store';
import type { ChatMessage, WebSocketMessage } from '../types';

export function useWebSocket(apiKey: string) {
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();

  const {
    setWsConnected,
    addMessage,
    addTypingUser,
    removeTypingUser,
    currentRoomId
  } = useChatStore();

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    const wsUrl = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws?api_key=${apiKey}`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log('[WebSocket] Connected');
      setWsConnected(true);

      // Join current room if any
      if (currentRoomId) {
        ws.send(JSON.stringify({ type: 'join_room', room_id: currentRoomId }));
      }
    };

    ws.onmessage = (event) => {
      try {
        const data: WebSocketMessage = JSON.parse(event.data);
        handleMessage(data);
      } catch (e) {
        console.error('[WebSocket] Parse error:', e);
      }
    };

    ws.onclose = () => {
      console.log('[WebSocket] Disconnected');
      setWsConnected(false);

      // Reconnect after 3 seconds
      reconnectTimeoutRef.current = setTimeout(connect, 3000);
    };

    ws.onerror = (error) => {
      console.error('[WebSocket] Error:', error);
    };

    wsRef.current = ws;
  }, [apiKey, currentRoomId, setWsConnected]);

  const handleMessage = useCallback((data: WebSocketMessage) => {
    switch (data.type) {
      case 'message':
        if (data.roomId && data.data) {
          addMessage(data.roomId, data.data as ChatMessage);
        }
        break;

      case 'typing':
        if (data.roomId && data.data) {
          if (data.data.is_typing) {
            addTypingUser(data.roomId, {
              userId: data.data.user_id,
              userName: data.data.user_name,
              startedAt: Date.now()
            });
          } else {
            removeTypingUser(data.roomId, data.data.user_id);
          }
        }
        break;

      case 'presence':
        // Handle user online/offline status
        break;

      case 'room_update':
        // Handle room updates (member joined/left, etc.)
        break;
    }
  }, [addMessage, addTypingUser, removeTypingUser]);

  const send = useCallback((message: object) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  }, []);

  const joinRoom = useCallback((roomId: string) => {
    send({ type: 'join_room', room_id: roomId });
  }, [send]);

  const leaveRoom = useCallback((roomId: string) => {
    send({ type: 'leave_room', room_id: roomId });
  }, [send]);

  const sendTyping = useCallback((roomId: string, isTyping: boolean) => {
    send({ type: isTyping ? 'typing_start' : 'typing_stop', room_id: roomId });
  }, [send]);

  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      wsRef.current?.close();
    };
  }, [connect]);

  return { send, joinRoom, leaveRoom, sendTyping };
}
```

### Composant RoomList

**Fichier:** `ChatRoomList.tsx`

```typescript
import { useEffect } from 'react';
import { useChatStore } from './store';
import type { ChatRoom } from './types';

interface ChatRoomListProps {
  onSelectRoom: (roomId: string) => void;
  onCreateRoom: () => void;
}

export function ChatRoomList({ onSelectRoom, onCreateRoom }: ChatRoomListProps) {
  const { rooms, currentRoomId, setRooms } = useChatStore();

  useEffect(() => {
    // Fetch rooms on mount
    fetchRooms();
  }, []);

  const fetchRooms = async () => {
    try {
      const response = await fetch('/api/chat/rooms');
      if (response.ok) {
        const data = await response.json();
        setRooms(data);
      }
    } catch (error) {
      console.error('Failed to fetch rooms:', error);
    }
  };

  const formatTime = (dateStr: string) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now.getTime() - date.getTime();

    if (diff < 60000) return 'now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h`;
    return date.toLocaleDateString();
  };

  return (
    <div className="flex flex-col h-full bg-bolt-elements-background-depth-1">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-bolt-elements-borderColor">
        <h2 className="text-lg font-semibold text-bolt-elements-textPrimary">Messages</h2>
        <button
          onClick={onCreateRoom}
          className="p-2 rounded-lg bg-bolt-elements-button-primary-background hover:bg-bolt-elements-button-primary-backgroundHover"
        >
          <div className="i-ph:plus text-white" />
        </button>
      </div>

      {/* Room List */}
      <div className="flex-1 overflow-y-auto">
        {rooms.length === 0 ? (
          <div className="p-4 text-center text-bolt-elements-textSecondary">
            No conversations yet
          </div>
        ) : (
          rooms.map((room) => (
            <RoomItem
              key={room.id}
              room={room}
              isActive={room.id === currentRoomId}
              onClick={() => onSelectRoom(room.id)}
            />
          ))
        )}
      </div>
    </div>
  );
}

function RoomItem({ room, isActive, onClick }: { room: ChatRoom; isActive: boolean; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`w-full p-4 text-left border-b border-bolt-elements-borderColor hover:bg-bolt-elements-background-depth-2 transition-colors ${
        isActive ? 'bg-bolt-elements-background-depth-2' : ''
      }`}
    >
      <div className="flex items-center gap-3">
        {/* Avatar */}
        <div className="w-10 h-10 rounded-full bg-bolt-elements-button-primary-background flex items-center justify-center">
          {room.type === 'direct' ? (
            <div className="i-ph:user text-white text-lg" />
          ) : (
            <div className="i-ph:users-three text-white text-lg" />
          )}
        </div>

        {/* Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <span className="font-medium text-bolt-elements-textPrimary truncate">
              {room.name || 'Direct Message'}
            </span>
            <span className="text-xs text-bolt-elements-textTertiary">
              {formatTime(room.lastActivityAt)}
            </span>
          </div>

          <div className="flex items-center justify-between mt-0.5">
            <span className="text-sm text-bolt-elements-textSecondary truncate">
              {room.memberCount} members
            </span>
            {room.unreadCount > 0 && (
              <span className="px-2 py-0.5 text-xs font-medium bg-bolt-elements-button-primary-background text-white rounded-full">
                {room.unreadCount}
              </span>
            )}
          </div>
        </div>
      </div>
    </button>
  );
}

function formatTime(dateStr: string): string {
  const date = new Date(dateStr);
  const now = new Date();
  const diff = now.getTime() - date.getTime();

  if (diff < 60000) return 'now';
  if (diff < 3600000) return `${Math.floor(diff / 60000)}m`;
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}h`;
  return date.toLocaleDateString();
}
```

---

## 2.5 Système d'Invitations - Landing Page

**Fichier:** `d:\IAFactory\rag-dz\bolt-diy\app\routes\invite.$token.tsx`

```typescript
import { json, redirect, type LoaderFunctionArgs, type ActionFunctionArgs } from '@remix-run/node';
import { useLoaderData, Form, useActionData, useNavigation } from '@remix-run/react';

interface InvitationData {
  id: string;
  room_id: string;
  email: string;
  room_name: string;
  room_type: string;
  inviter_name: string;
  expires_at: string;
}

export async function loader({ params }: LoaderFunctionArgs) {
  const { token } = params;

  if (!token) {
    throw new Response('Invalid invitation', { status: 400 });
  }

  // Fetch invitation details
  const response = await fetch(`${process.env.API_URL}/api/chat/invitations/${token}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Response(error.detail || 'Invalid invitation', { status: response.status });
  }

  const invitation: InvitationData = await response.json();

  return json({ invitation, token });
}

export async function action({ request, params }: ActionFunctionArgs) {
  const formData = await request.formData();
  const token = params.token;

  // Get session/auth token from cookies
  const cookieHeader = request.headers.get('Cookie');

  // Accept invitation
  const response = await fetch(`${process.env.API_URL}/api/chat/invitations/${token}/accept`, {
    method: 'POST',
    headers: {
      'Cookie': cookieHeader || '',
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    return json({ error: error.detail || 'Failed to accept invitation' }, { status: 400 });
  }

  const result = await response.json();

  // Redirect to the room
  return redirect(`/chat/${result.room_id}`);
}

export default function InvitePage() {
  const { invitation, token } = useLoaderData<typeof loader>();
  const actionData = useActionData<typeof action>();
  const navigation = useNavigation();

  const isSubmitting = navigation.state === 'submitting';

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-bolt-elements-background-depth-1 to-bolt-elements-background-depth-3 p-4">
      <div className="w-full max-w-md">
        <div className="bg-bolt-elements-background-depth-2 rounded-2xl shadow-2xl p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-bolt-elements-button-primary-background flex items-center justify-center">
              <div className="i-ph:chat-circle-dots text-white text-3xl" />
            </div>
            <h1 className="text-2xl font-bold text-bolt-elements-textPrimary">
              You're invited!
            </h1>
            <p className="mt-2 text-bolt-elements-textSecondary">
              {invitation.inviter_name} invited you to collaborate
            </p>
          </div>

          {/* Room Info */}
          <div className="bg-bolt-elements-background-depth-3 rounded-xl p-4 mb-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-bolt-elements-item-backgroundAccent flex items-center justify-center">
                {invitation.room_type === 'direct' ? (
                  <div className="i-ph:user text-bolt-elements-textPrimary text-xl" />
                ) : invitation.room_type === 'project' ? (
                  <div className="i-ph:folder-simple text-bolt-elements-textPrimary text-xl" />
                ) : (
                  <div className="i-ph:users-three text-bolt-elements-textPrimary text-xl" />
                )}
              </div>
              <div>
                <div className="font-semibold text-bolt-elements-textPrimary">
                  {invitation.room_name || 'Private Conversation'}
                </div>
                <div className="text-sm text-bolt-elements-textSecondary capitalize">
                  {invitation.room_type} chat
                </div>
              </div>
            </div>
          </div>

          {/* Features */}
          <div className="space-y-3 mb-6">
            <Feature icon="i-ph:chat-circle" text="Chat in real-time with your team" />
            <Feature icon="i-ph:code" text="Share code and artifacts instantly" />
            <Feature icon="i-ph:robot" text="Collaborate with AI agents" />
          </div>

          {/* Error Message */}
          {actionData?.error && (
            <div className="mb-4 p-3 rounded-lg bg-red-500/10 text-red-400 text-sm">
              {actionData.error}
            </div>
          )}

          {/* Accept Button */}
          <Form method="post">
            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full py-3 px-4 rounded-xl font-semibold text-white bg-bolt-elements-button-primary-background hover:bg-bolt-elements-button-primary-backgroundHover disabled:opacity-50 transition-colors"
            >
              {isSubmitting ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="i-svg-spinners:90-ring-with-bg" />
                  Accepting...
                </span>
              ) : (
                'Accept Invitation'
              )}
            </button>
          </Form>

          {/* Sign In Link */}
          <div className="mt-4 text-center text-sm text-bolt-elements-textSecondary">
            Don't have an account?{' '}
            <a href={`/signup?invite=${token}`} className="text-bolt-elements-textPrimary hover:underline">
              Sign up
            </a>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 text-center text-sm text-bolt-elements-textTertiary">
          Powered by IAFactory
        </div>
      </div>
    </div>
  );
}

function Feature({ icon, text }: { icon: string; text: string }) {
  return (
    <div className="flex items-center gap-3">
      <div className={`${icon} text-bolt-elements-textSecondary text-lg`} />
      <span className="text-sm text-bolt-elements-textSecondary">{text}</span>
    </div>
  );
}
```

---

# 3. PLAN DÉPLOIEMENT

## 3.1 Ordre des Migrations

```bash
# 1. Backup de la base de données
pg_dump -h localhost -U postgres iafactory > backup_$(date +%Y%m%d).sql

# 2. Appliquer la migration
psql -h localhost -U postgres -d iafactory -f services/api/migrations/015_chat_multiuser.sql

# 3. Vérifier les tables créées
psql -h localhost -U postgres -d iafactory -c "\dt chat_*"
```

## 3.2 Deploy Backend

```bash
# 1. Copier les nouveaux fichiers
cp routers/chat_rooms.py services/api/app/routers/
cp websocket.py services/api/app/  # Version mise à jour

# 2. Ajouter le router dans main.py
# from app.routers import chat_rooms
# app.include_router(chat_rooms.router)

# 3. Restart le service
docker-compose restart api
# ou
systemctl restart iafactory-api
```

## 3.3 Deploy Frontend

```bash
# 1. Copier les composants
cp -r components/chat-multi bolt-diy/app/components/

# 2. Copier les routes
cp routes/invite.$token.tsx bolt-diy/app/routes/

# 3. Build
cd bolt-diy
npm run build

# 4. Restart
pm2 restart bolt-diy
```

## 3.4 Rollback Plan

```bash
# Si problème, restaurer le backup
psql -h localhost -U postgres -d iafactory < backup_YYYYMMDD.sql

# Revert les fichiers
git checkout HEAD~1 -- services/api/app/routers/
git checkout HEAD~1 -- bolt-diy/app/components/
```

---

# 4. TESTS

## 4.1 Backend - pytest

```python
# tests/test_chat_rooms.py
import pytest
from httpx import AsyncClient
from uuid import uuid4

@pytest.mark.asyncio
async def test_create_room(client: AsyncClient, auth_headers: dict):
    response = await client.post(
        "/api/chat/rooms",
        json={"name": "Test Room", "type": "group"},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Room"
    assert data["type"] == "group"
    assert data["memberCount"] == 1

@pytest.mark.asyncio
async def test_send_message(client: AsyncClient, auth_headers: dict, test_room: dict):
    response = await client.post(
        f"/api/chat/rooms/{test_room['id']}/messages",
        json={"content": "Hello, world!"},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Hello, world!"

@pytest.mark.asyncio
async def test_invite_user(client: AsyncClient, auth_headers: dict, test_room: dict):
    response = await client.post(
        f"/api/chat/rooms/{test_room['id']}/invite",
        json={"email": "test@example.com"},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"
    assert "token" in data
```

## 4.2 Frontend - Vitest

```typescript
// tests/chat-store.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { useChatStore } from '../app/components/chat-multi/store';

describe('ChatStore', () => {
  beforeEach(() => {
    useChatStore.setState({
      rooms: [],
      currentRoomId: null,
      messagesByRoom: {},
    });
  });

  it('should add a room', () => {
    const room = { id: '1', name: 'Test', type: 'group' as const, memberCount: 1 };
    useChatStore.getState().addRoom(room as any);
    expect(useChatStore.getState().rooms).toHaveLength(1);
  });

  it('should add a message to room', () => {
    const message = { id: '1', roomId: 'room1', content: 'Hello' };
    useChatStore.getState().addMessage('room1', message as any);
    expect(useChatStore.getState().messagesByRoom['room1']).toHaveLength(1);
  });
});
```

## 4.3 E2E - Playwright

```typescript
// e2e/chat.spec.ts
import { test, expect } from '@playwright/test';

test('user can send message in room', async ({ page }) => {
  await page.goto('/chat');

  // Select a room
  await page.click('[data-testid="room-item"]:first-child');

  // Type message
  await page.fill('[data-testid="chat-input"]', 'Hello from E2E test');
  await page.click('[data-testid="send-button"]');

  // Verify message appears
  await expect(page.locator('.message-content').last()).toContainText('Hello from E2E test');
});

test('user can invite by email', async ({ page }) => {
  await page.goto('/chat/room/test-room');

  // Open invite modal
  await page.click('[data-testid="invite-button"]');

  // Fill email
  await page.fill('[data-testid="invite-email"]', 'invite@test.com');
  await page.click('[data-testid="send-invite"]');

  // Verify success
  await expect(page.locator('.toast-success')).toBeVisible();
});
```

---

# 5. RÉSUMÉ

## Ce qui existe déjà

| Composant | Statut | Localisation |
|-----------|--------|--------------|
| Chat User↔IA | ✅ Complet | chat_sessions, chat_messages |
| WebSocket basique | ✅ Fonctionne | websocket.py, websocket_router.py |
| Agents BMAD | ✅ Intégrés | bmad_chat.py, 5 routers |
| Archon KB | ✅ Intégré | knowledge_item_service.py |
| Bolt.diy IDE | ✅ Intégré | bolt-diy/ |

## Ce qu'il faut implémenter

| Composant | Priorité | Effort |
|-----------|----------|--------|
| Migration BD chat_rooms | HIGH | 1 jour |
| API Routes chat_rooms.py | HIGH | 2 jours |
| WebSocket étendu (rooms) | HIGH | 1 jour |
| Frontend composants | HIGH | 3 jours |
| Système invitations | MEDIUM | 2 jours |
| @mentions agents | MEDIUM | 1 jour |
| Tests automatisés | MEDIUM | 2 jours |

## Estimation Totale

| Phase | Durée |
|-------|-------|
| Phase 1: Backend + DB | 4 jours |
| Phase 2: Frontend | 3 jours |
| Phase 3: Invitations | 2 jours |
| Phase 4: Tests | 2 jours |
| **TOTAL** | **11 jours** |

---

**Fin du rapport technique**
