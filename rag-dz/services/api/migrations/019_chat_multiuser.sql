-- Migration 019: Chat Multi-User System
-- ================================================================
-- Système de chat collaboratif User↔User avec rooms et invitations
-- Compatible multi-tenant avec RLS
-- ================================================================

BEGIN;

-- ============================================================
-- ENUM TYPES
-- ============================================================

-- Types de rooms
CREATE TYPE chat_room_type AS ENUM (
    'direct',       -- Chat 1:1 entre 2 users
    'group',        -- Groupe privé avec invitations
    'project',      -- Room liée à un projet
    'agent'         -- Room avec agent BMAD
);

-- Rôles des membres
CREATE TYPE chat_member_role AS ENUM (
    'owner',        -- Créateur, tous les droits
    'admin',        -- Peut inviter/supprimer membres
    'member',       -- Peut lire/écrire
    'readonly'      -- Peut seulement lire
);

-- Status des invitations
CREATE TYPE invitation_status AS ENUM (
    'pending',
    'accepted',
    'declined',
    'expired'
);

-- ============================================================
-- Table: chat_rooms
-- ============================================================
-- Rooms de conversation multi-user

CREATE TABLE IF NOT EXISTS chat_rooms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,

    -- Metadata room
    name VARCHAR(255) NOT NULL,
    description TEXT,
    room_type chat_room_type NOT NULL DEFAULT 'group',

    -- Avatar/Couleur pour l'UI
    avatar_url TEXT,
    color VARCHAR(7) DEFAULT '#6366f1', -- Hex color

    -- Settings
    is_private BOOLEAN DEFAULT TRUE,
    allow_invites BOOLEAN DEFAULT TRUE,  -- Members peuvent inviter
    max_members INTEGER DEFAULT 50,

    -- Lien vers projet si room_type = 'project'
    project_id INTEGER REFERENCES projects(id) ON DELETE SET NULL,

    -- Agent BMAD si room_type = 'agent'
    agent_id VARCHAR(100),

    -- Stats
    member_count INTEGER DEFAULT 1,
    message_count INTEGER DEFAULT 0,

    -- Dernier message pour preview
    last_message_at TIMESTAMPTZ,
    last_message_preview TEXT,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    -- Soft delete
    is_archived BOOLEAN DEFAULT FALSE,
    archived_at TIMESTAMPTZ
);

-- Index
CREATE INDEX idx_rooms_tenant ON chat_rooms(tenant_id);
CREATE INDEX idx_rooms_type ON chat_rooms(tenant_id, room_type);
CREATE INDEX idx_rooms_project ON chat_rooms(project_id) WHERE project_id IS NOT NULL;
CREATE INDEX idx_rooms_last_msg ON chat_rooms(last_message_at DESC NULLS LAST);
CREATE INDEX idx_rooms_active ON chat_rooms(tenant_id, is_archived) WHERE is_archived = FALSE;

COMMENT ON TABLE chat_rooms IS 'Rooms de chat multi-user';
COMMENT ON COLUMN chat_rooms.room_type IS 'direct=1:1, group=privé, project=lié projet, agent=avec BMAD';


-- ============================================================
-- Table: chat_room_members
-- ============================================================
-- Membres des rooms

CREATE TABLE IF NOT EXISTS chat_room_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID NOT NULL REFERENCES chat_rooms(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Rôle dans la room
    role chat_member_role NOT NULL DEFAULT 'member',

    -- Notifications
    notifications_enabled BOOLEAN DEFAULT TRUE,
    muted_until TIMESTAMPTZ,  -- Mute temporaire

    -- Read tracking
    last_read_at TIMESTAMPTZ DEFAULT NOW(),
    unread_count INTEGER DEFAULT 0,

    -- Timestamps
    joined_at TIMESTAMPTZ DEFAULT NOW(),

    -- Contrainte unique
    CONSTRAINT unique_room_member UNIQUE (room_id, user_id)
);

-- Index
CREATE INDEX idx_members_room ON chat_room_members(room_id);
CREATE INDEX idx_members_user ON chat_room_members(user_id);
CREATE INDEX idx_members_unread ON chat_room_members(user_id, unread_count) WHERE unread_count > 0;

COMMENT ON TABLE chat_room_members IS 'Membres des rooms de chat';


-- ============================================================
-- Table: chat_room_messages
-- ============================================================
-- Messages dans les rooms

CREATE TABLE IF NOT EXISTS chat_room_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID NOT NULL REFERENCES chat_rooms(id) ON DELETE CASCADE,
    sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Contenu
    content TEXT NOT NULL,
    content_type VARCHAR(20) DEFAULT 'text', -- text, code, file, image

    -- Réponse à un message
    reply_to_id UUID REFERENCES chat_room_messages(id) ON DELETE SET NULL,

    -- Mentions @user
    mentions INTEGER[] DEFAULT '{}',  -- Array of user_ids mentionnés

    -- Fichiers attachés
    attachments JSONB DEFAULT '[]',  -- [{name, url, type, size}]

    -- Reactions (emoji counts)
    reactions JSONB DEFAULT '{}',  -- {"👍": [user_ids], "❤️": [user_ids]}

    -- Edit history
    is_edited BOOLEAN DEFAULT FALSE,
    edited_at TIMESTAMPTZ,
    original_content TEXT,  -- Contenu avant edit

    -- Status
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMPTZ,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX idx_room_messages_room ON chat_room_messages(room_id);
CREATE INDEX idx_room_messages_sender ON chat_room_messages(sender_id);
CREATE INDEX idx_room_messages_created ON chat_room_messages(room_id, created_at DESC);
CREATE INDEX idx_room_messages_reply ON chat_room_messages(reply_to_id) WHERE reply_to_id IS NOT NULL;
CREATE INDEX idx_room_messages_mentions ON chat_room_messages USING GIN(mentions);

COMMENT ON TABLE chat_room_messages IS 'Messages dans les rooms de chat';


-- ============================================================
-- Table: chat_room_invitations
-- ============================================================
-- Invitations aux rooms

CREATE TABLE IF NOT EXISTS chat_room_invitations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID NOT NULL REFERENCES chat_rooms(id) ON DELETE CASCADE,

    -- Qui invite
    inviter_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Invité (soit user_id soit email)
    invitee_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    invitee_email VARCHAR(255),

    -- Token pour lien d'invitation
    invite_token VARCHAR(64) UNIQUE NOT NULL,

    -- Status
    status invitation_status DEFAULT 'pending',

    -- Rôle attribué à l'acceptation
    assigned_role chat_member_role DEFAULT 'member',

    -- Message personnalisé
    message TEXT,

    -- Expiration (7 jours par défaut)
    expires_at TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '7 days'),

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    responded_at TIMESTAMPTZ,

    -- Contrainte: soit user_id soit email
    CONSTRAINT invitation_target CHECK (
        (invitee_id IS NOT NULL AND invitee_email IS NULL) OR
        (invitee_id IS NULL AND invitee_email IS NOT NULL)
    )
);

-- Index
CREATE INDEX idx_invitations_room ON chat_room_invitations(room_id);
CREATE INDEX idx_invitations_invitee ON chat_room_invitations(invitee_id) WHERE invitee_id IS NOT NULL;
CREATE INDEX idx_invitations_email ON chat_room_invitations(invitee_email) WHERE invitee_email IS NOT NULL;
CREATE INDEX idx_invitations_token ON chat_room_invitations(invite_token);
CREATE INDEX idx_invitations_pending ON chat_room_invitations(status) WHERE status = 'pending';

COMMENT ON TABLE chat_room_invitations IS 'Invitations aux rooms de chat';


-- ============================================================
-- Table: chat_read_receipts
-- ============================================================
-- Accusés de lecture par message (optionnel, pour rooms petites)

CREATE TABLE IF NOT EXISTS chat_read_receipts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID NOT NULL REFERENCES chat_room_messages(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    read_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT unique_read_receipt UNIQUE (message_id, user_id)
);

-- Index
CREATE INDEX idx_receipts_message ON chat_read_receipts(message_id);
CREATE INDEX idx_receipts_user ON chat_read_receipts(user_id);

COMMENT ON TABLE chat_read_receipts IS 'Accusés de lecture des messages';


-- ============================================================
-- Table: chat_typing_indicators (volatile, peut être en Redis)
-- ============================================================
-- Pour le "X is typing..." - optionnel en SQL, mieux en Redis

CREATE TABLE IF NOT EXISTS chat_typing_indicators (
    room_id UUID NOT NULL REFERENCES chat_rooms(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    started_at TIMESTAMPTZ DEFAULT NOW(),

    PRIMARY KEY (room_id, user_id)
);

COMMENT ON TABLE chat_typing_indicators IS 'Indicateurs de frappe (peut être migré vers Redis)';


-- ============================================================
-- RLS POLICIES
-- ============================================================

ALTER TABLE chat_rooms ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_room_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_room_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_room_invitations ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_read_receipts ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_typing_indicators ENABLE ROW LEVEL SECURITY;

-- Force RLS pour tous les utilisateurs
ALTER TABLE chat_rooms FORCE ROW LEVEL SECURITY;
ALTER TABLE chat_room_members FORCE ROW LEVEL SECURITY;
ALTER TABLE chat_room_messages FORCE ROW LEVEL SECURITY;
ALTER TABLE chat_room_invitations FORCE ROW LEVEL SECURITY;
ALTER TABLE chat_read_receipts FORCE ROW LEVEL SECURITY;
ALTER TABLE chat_typing_indicators FORCE ROW LEVEL SECURITY;

-- Policies pour chat_rooms (via membership)
CREATE POLICY rooms_select ON chat_rooms FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM chat_room_members m
            WHERE m.room_id = chat_rooms.id
            AND m.user_id = current_setting('app.current_user_id')::INTEGER
        )
    );

CREATE POLICY rooms_insert ON chat_rooms FOR INSERT
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id')::UUID);

CREATE POLICY rooms_update ON chat_rooms FOR UPDATE
    USING (
        EXISTS (
            SELECT 1 FROM chat_room_members m
            WHERE m.room_id = chat_rooms.id
            AND m.user_id = current_setting('app.current_user_id')::INTEGER
            AND m.role IN ('owner', 'admin')
        )
    );

-- Policies pour chat_room_members
CREATE POLICY members_select ON chat_room_members FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM chat_room_members m2
            WHERE m2.room_id = chat_room_members.room_id
            AND m2.user_id = current_setting('app.current_user_id')::INTEGER
        )
    );

CREATE POLICY members_insert ON chat_room_members FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM chat_room_members m
            WHERE m.room_id = chat_room_members.room_id
            AND m.user_id = current_setting('app.current_user_id')::INTEGER
            AND m.role IN ('owner', 'admin')
        )
        OR user_id = current_setting('app.current_user_id')::INTEGER
    );

-- Policies pour chat_room_messages
CREATE POLICY messages_select ON chat_room_messages FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM chat_room_members m
            WHERE m.room_id = chat_room_messages.room_id
            AND m.user_id = current_setting('app.current_user_id')::INTEGER
        )
    );

CREATE POLICY messages_insert ON chat_room_messages FOR INSERT
    WITH CHECK (
        sender_id = current_setting('app.current_user_id')::INTEGER
        AND EXISTS (
            SELECT 1 FROM chat_room_members m
            WHERE m.room_id = chat_room_messages.room_id
            AND m.user_id = current_setting('app.current_user_id')::INTEGER
            AND m.role IN ('owner', 'admin', 'member')
        )
    );

CREATE POLICY messages_update ON chat_room_messages FOR UPDATE
    USING (sender_id = current_setting('app.current_user_id')::INTEGER);

-- Policies pour invitations
CREATE POLICY invitations_select ON chat_room_invitations FOR SELECT
    USING (
        inviter_id = current_setting('app.current_user_id')::INTEGER
        OR invitee_id = current_setting('app.current_user_id')::INTEGER
    );

CREATE POLICY invitations_insert ON chat_room_invitations FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM chat_room_members m
            WHERE m.room_id = chat_room_invitations.room_id
            AND m.user_id = current_setting('app.current_user_id')::INTEGER
            AND m.role IN ('owner', 'admin')
        )
        OR EXISTS (
            SELECT 1 FROM chat_rooms r
            JOIN chat_room_members m ON m.room_id = r.id
            WHERE r.id = chat_room_invitations.room_id
            AND m.user_id = current_setting('app.current_user_id')::INTEGER
            AND r.allow_invites = TRUE
        )
    );


-- ============================================================
-- FUNCTIONS
-- ============================================================

-- Fonction: Créer une room et ajouter le créateur comme owner
CREATE OR REPLACE FUNCTION create_chat_room(
    p_tenant_id UUID,
    p_creator_id INTEGER,
    p_name VARCHAR(255),
    p_room_type chat_room_type DEFAULT 'group',
    p_description TEXT DEFAULT NULL,
    p_project_id INTEGER DEFAULT NULL,
    p_agent_id VARCHAR(100) DEFAULT NULL
)
RETURNS UUID
LANGUAGE plpgsql
AS $$
DECLARE
    v_room_id UUID;
BEGIN
    -- Créer la room
    INSERT INTO chat_rooms (tenant_id, name, description, room_type, project_id, agent_id)
    VALUES (p_tenant_id, p_name, p_description, p_room_type, p_project_id, p_agent_id)
    RETURNING id INTO v_room_id;

    -- Ajouter le créateur comme owner
    INSERT INTO chat_room_members (room_id, user_id, role)
    VALUES (v_room_id, p_creator_id, 'owner');

    RETURN v_room_id;
END;
$$;

-- Fonction: Créer un chat direct entre 2 users
CREATE OR REPLACE FUNCTION create_direct_chat(
    p_tenant_id UUID,
    p_user1_id INTEGER,
    p_user2_id INTEGER
)
RETURNS UUID
LANGUAGE plpgsql
AS $$
DECLARE
    v_room_id UUID;
    v_existing_room UUID;
BEGIN
    -- Vérifier si un chat direct existe déjà
    SELECT r.id INTO v_existing_room
    FROM chat_rooms r
    JOIN chat_room_members m1 ON m1.room_id = r.id AND m1.user_id = p_user1_id
    JOIN chat_room_members m2 ON m2.room_id = r.id AND m2.user_id = p_user2_id
    WHERE r.room_type = 'direct'
    AND r.tenant_id = p_tenant_id
    LIMIT 1;

    IF v_existing_room IS NOT NULL THEN
        RETURN v_existing_room;
    END IF;

    -- Créer la room
    INSERT INTO chat_rooms (tenant_id, name, room_type, member_count)
    VALUES (p_tenant_id, 'Direct Chat', 'direct', 2)
    RETURNING id INTO v_room_id;

    -- Ajouter les 2 membres
    INSERT INTO chat_room_members (room_id, user_id, role)
    VALUES
        (v_room_id, p_user1_id, 'member'),
        (v_room_id, p_user2_id, 'member');

    RETURN v_room_id;
END;
$$;

-- Fonction: Ajouter un message et mettre à jour les compteurs
CREATE OR REPLACE FUNCTION add_room_message(
    p_room_id UUID,
    p_sender_id INTEGER,
    p_content TEXT,
    p_content_type VARCHAR(20) DEFAULT 'text',
    p_reply_to_id UUID DEFAULT NULL,
    p_mentions INTEGER[] DEFAULT '{}'
)
RETURNS UUID
LANGUAGE plpgsql
AS $$
DECLARE
    v_message_id UUID;
    v_preview TEXT;
BEGIN
    -- Créer le message
    INSERT INTO chat_room_messages (room_id, sender_id, content, content_type, reply_to_id, mentions)
    VALUES (p_room_id, p_sender_id, p_content, p_content_type, p_reply_to_id, p_mentions)
    RETURNING id INTO v_message_id;

    -- Preview (50 premiers caractères)
    v_preview := LEFT(p_content, 50);
    IF LENGTH(p_content) > 50 THEN
        v_preview := v_preview || '...';
    END IF;

    -- Mettre à jour la room
    UPDATE chat_rooms
    SET message_count = message_count + 1,
        last_message_at = NOW(),
        last_message_preview = v_preview,
        updated_at = NOW()
    WHERE id = p_room_id;

    -- Incrémenter unread_count pour tous les membres sauf l'expéditeur
    UPDATE chat_room_members
    SET unread_count = unread_count + 1
    WHERE room_id = p_room_id
    AND user_id != p_sender_id;

    RETURN v_message_id;
END;
$$;

-- Fonction: Marquer les messages comme lus
CREATE OR REPLACE FUNCTION mark_room_as_read(
    p_room_id UUID,
    p_user_id INTEGER
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE chat_room_members
    SET last_read_at = NOW(),
        unread_count = 0
    WHERE room_id = p_room_id
    AND user_id = p_user_id;
END;
$$;

-- Fonction: Générer un token d'invitation
CREATE OR REPLACE FUNCTION generate_invite_token()
RETURNS VARCHAR(64)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN encode(gen_random_bytes(32), 'hex');
END;
$$;

-- Fonction: Accepter une invitation
CREATE OR REPLACE FUNCTION accept_invitation(
    p_token VARCHAR(64),
    p_user_id INTEGER
)
RETURNS UUID
LANGUAGE plpgsql
AS $$
DECLARE
    v_invitation RECORD;
    v_room_id UUID;
BEGIN
    -- Récupérer l'invitation
    SELECT * INTO v_invitation
    FROM chat_room_invitations
    WHERE invite_token = p_token
    AND status = 'pending'
    AND expires_at > NOW();

    IF v_invitation IS NULL THEN
        RAISE EXCEPTION 'Invalid or expired invitation';
    END IF;

    -- Vérifier que c'est le bon user (si invitee_id spécifié)
    IF v_invitation.invitee_id IS NOT NULL AND v_invitation.invitee_id != p_user_id THEN
        RAISE EXCEPTION 'This invitation is for another user';
    END IF;

    v_room_id := v_invitation.room_id;

    -- Ajouter le membre
    INSERT INTO chat_room_members (room_id, user_id, role)
    VALUES (v_room_id, p_user_id, v_invitation.assigned_role)
    ON CONFLICT (room_id, user_id) DO NOTHING;

    -- Mettre à jour le compteur
    UPDATE chat_rooms
    SET member_count = member_count + 1
    WHERE id = v_room_id;

    -- Marquer l'invitation comme acceptée
    UPDATE chat_room_invitations
    SET status = 'accepted',
        responded_at = NOW(),
        invitee_id = p_user_id
    WHERE id = v_invitation.id;

    RETURN v_room_id;
END;
$$;


-- ============================================================
-- TRIGGERS
-- ============================================================

-- Trigger: Auto-update updated_at
CREATE OR REPLACE FUNCTION update_chat_room_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_chat_rooms_updated
    BEFORE UPDATE ON chat_rooms
    FOR EACH ROW
    EXECUTE FUNCTION update_chat_room_timestamp();

-- Trigger: Expirer les invitations automatiquement
CREATE OR REPLACE FUNCTION expire_old_invitations()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE chat_room_invitations
    SET status = 'expired'
    WHERE status = 'pending'
    AND expires_at < NOW();
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Scheduler pour expirer (à activer via pg_cron si disponible)
-- SELECT cron.schedule('expire-invitations', '0 * * * *', 'SELECT expire_old_invitations()');


COMMIT;

-- ============================================================
-- GRANTS (adapter selon vos rôles)
-- ============================================================

-- GRANT SELECT, INSERT, UPDATE, DELETE ON chat_rooms TO app_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON chat_room_members TO app_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON chat_room_messages TO app_user;
-- GRANT SELECT, INSERT, UPDATE ON chat_room_invitations TO app_user;
-- GRANT SELECT, INSERT ON chat_read_receipts TO app_user;
-- GRANT SELECT, INSERT, DELETE ON chat_typing_indicators TO app_user;
