-- Migration 014: IAFactory Memory System
-- ================================================================
-- Systeme de memoire IA + stockage conversations
-- Compatible multi-tenant avec RLS
-- Support multilingue: FR, AR, EN, Darija, Amazigh

BEGIN;

-- ============================================================
-- ENUM TYPES
-- ============================================================

-- Categories de memoire
CREATE TYPE memory_category AS ENUM (
    'profile',      -- Infos personnelles (nom, entreprise, role)
    'preference',   -- Preferences IA (langue, style reponse)
    'business',     -- Contexte metier (CA, employes, logiciels)
    'fact',         -- Faits appris (dates, evenements)
    'goal'          -- Objectifs utilisateur
);

-- Roles de message
CREATE TYPE message_role AS ENUM (
    'user',
    'assistant',
    'system',
    'tool'
);

-- ============================================================
-- Table: chat_sessions
-- ============================================================
-- Sessions de conversation

CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Metadata session
    title VARCHAR(255),
    app_context VARCHAR(50) DEFAULT 'chat', -- 'rag', 'academy', 'video', 'gov', 'crm', etc.
    language VARCHAR(10) DEFAULT 'fr', -- fr, ar, dz-ar, ber, en

    -- Agent/Model utilise
    agent_id VARCHAR(100), -- BMAD agent ID si applicable
    model VARCHAR(50) DEFAULT 'groq', -- groq, gpt-4, claude, etc.

    -- Stats
    message_count INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,

    -- Timestamps
    started_at TIMESTAMPTZ DEFAULT NOW(),
    last_message_at TIMESTAMPTZ DEFAULT NOW(),

    -- Status
    is_archived BOOLEAN DEFAULT FALSE,
    is_starred BOOLEAN DEFAULT FALSE,

    -- Metadata flexible
    metadata JSONB DEFAULT '{}',

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX idx_sessions_tenant ON chat_sessions(tenant_id);
CREATE INDEX idx_sessions_user ON chat_sessions(user_id);
CREATE INDEX idx_sessions_last_msg ON chat_sessions(last_message_at DESC);
CREATE INDEX idx_sessions_app ON chat_sessions(tenant_id, app_context);
CREATE INDEX idx_sessions_active ON chat_sessions(user_id, is_archived) WHERE is_archived = FALSE;

COMMENT ON TABLE chat_sessions IS 'Sessions de conversation IA';
COMMENT ON COLUMN chat_sessions.app_context IS 'Contexte app: rag, academy, video, gov, crm, etc.';
COMMENT ON COLUMN chat_sessions.language IS 'Langue: fr, ar, dz-ar (darija), ber (amazigh), en';


-- ============================================================
-- Table: chat_messages
-- ============================================================
-- Messages individuels

CREATE TABLE IF NOT EXISTS chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,

    -- Contenu
    role message_role NOT NULL,
    content TEXT NOT NULL,

    -- Usage tokens
    tokens_input INTEGER DEFAULT 0,
    tokens_output INTEGER DEFAULT 0,
    tokens_total INTEGER GENERATED ALWAYS AS (tokens_input + tokens_output) STORED,

    -- Model/Provider
    model VARCHAR(50),
    provider VARCHAR(30), -- groq, openai, anthropic, etc.
    latency_ms INTEGER,

    -- Attachments (fichiers, images)
    attachments JSONB DEFAULT '[]',

    -- Tools utilisés (function calling)
    tools_used JSONB DEFAULT '[]',

    -- Feedback
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    feedback TEXT,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),

    -- Metadata
    metadata JSONB DEFAULT '{}'
);

-- Index
CREATE INDEX idx_messages_session ON chat_messages(session_id);
CREATE INDEX idx_messages_created ON chat_messages(session_id, created_at DESC);
CREATE INDEX idx_messages_role ON chat_messages(session_id, role);

COMMENT ON TABLE chat_messages IS 'Messages dans les sessions de conversation';
COMMENT ON COLUMN chat_messages.tools_used IS 'Liste des tools/functions appelés';


-- ============================================================
-- Table: user_memories
-- ============================================================
-- Memoires extraites des conversations

CREATE TABLE IF NOT EXISTS user_memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Categorisation
    category memory_category NOT NULL,
    key VARCHAR(100) NOT NULL, -- 'company_name', 'monthly_revenue', etc.

    -- Valeur
    value TEXT NOT NULL,
    value_type VARCHAR(20) DEFAULT 'text', -- 'text', 'number', 'date', 'json', 'list'

    -- Confiance et source
    confidence DECIMAL(3,2) DEFAULT 0.80 CHECK (confidence BETWEEN 0 AND 1),
    source VARCHAR(50) DEFAULT 'extracted', -- 'extracted', 'user_input', 'corrected', 'imported'
    extracted_from UUID REFERENCES chat_messages(id) ON DELETE SET NULL,

    -- Langue
    language VARCHAR(10) DEFAULT 'fr',

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ, -- NULL = permanent

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE, -- User a confirme

    -- Metadata
    metadata JSONB DEFAULT '{}',

    -- Contrainte unique par user/category/key
    UNIQUE(user_id, category, key)
);

-- Index
CREATE INDEX idx_memories_tenant ON user_memories(tenant_id);
CREATE INDEX idx_memories_user ON user_memories(user_id);
CREATE INDEX idx_memories_category ON user_memories(user_id, category);
CREATE INDEX idx_memories_active ON user_memories(user_id, is_active) WHERE is_active = TRUE;
CREATE INDEX idx_memories_key ON user_memories(user_id, key);

COMMENT ON TABLE user_memories IS 'Memoires IA extraites des conversations';
COMMENT ON COLUMN user_memories.confidence IS 'Score de confiance 0.00 a 1.00';
COMMENT ON COLUMN user_memories.source IS 'Origine: extracted, user_input, corrected, imported';


-- ============================================================
-- Table: memory_corrections
-- ============================================================
-- Historique des corrections de memoire

CREATE TABLE IF NOT EXISTS memory_corrections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    memory_id UUID NOT NULL REFERENCES user_memories(id) ON DELETE CASCADE,

    -- Changement
    old_value TEXT,
    new_value TEXT,

    -- Qui a corrige
    corrected_by VARCHAR(50) DEFAULT 'user', -- 'user', 'system', 'admin'
    corrected_by_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,

    -- Raison (optionnel)
    reason TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX idx_corrections_memory ON memory_corrections(memory_id);

COMMENT ON TABLE memory_corrections IS 'Historique des corrections de memoire';


-- ============================================================
-- Table: message_embeddings
-- ============================================================
-- Embeddings pour recherche semantique (pgvector)

CREATE TABLE IF NOT EXISTS message_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID NOT NULL REFERENCES chat_messages(id) ON DELETE CASCADE,

    -- Embedding vector (OpenAI ada-002 = 1536, autres = 768/384)
    embedding vector(1536),

    -- Model utilise
    embedding_model VARCHAR(50) DEFAULT 'text-embedding-ada-002',

    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(message_id)
);

-- Index HNSW pour recherche rapide
CREATE INDEX idx_msg_embed_hnsw ON message_embeddings
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

COMMENT ON TABLE message_embeddings IS 'Embeddings des messages pour recherche semantique';


-- ============================================================
-- Table: memory_embeddings
-- ============================================================
-- Embeddings des memoires

CREATE TABLE IF NOT EXISTS memory_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    memory_id UUID NOT NULL REFERENCES user_memories(id) ON DELETE CASCADE,

    embedding vector(1536),
    embedding_model VARCHAR(50) DEFAULT 'text-embedding-ada-002',

    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(memory_id)
);

-- Index HNSW
CREATE INDEX idx_mem_embed_hnsw ON memory_embeddings
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

COMMENT ON TABLE memory_embeddings IS 'Embeddings des memoires pour recherche semantique';


-- ============================================================
-- Table: conversation_summaries
-- ============================================================
-- Resumes automatiques des conversations longues

CREATE TABLE IF NOT EXISTS conversation_summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,

    -- Resume
    summary TEXT NOT NULL,
    summary_type VARCHAR(30) DEFAULT 'auto', -- 'auto', 'manual', 'checkpoint'

    -- Couverture
    from_message_id UUID REFERENCES chat_messages(id),
    to_message_id UUID REFERENCES chat_messages(id),
    messages_covered INTEGER DEFAULT 0,

    -- Model utilise
    model VARCHAR(50),

    created_at TIMESTAMPTZ DEFAULT NOW(),

    -- Metadata
    metadata JSONB DEFAULT '{}'
);

-- Index
CREATE INDEX idx_summaries_session ON conversation_summaries(session_id);

COMMENT ON TABLE conversation_summaries IS 'Resumes automatiques des longues conversations';


-- ============================================================
-- Helper Function: get_current_user_id
-- ============================================================
-- Equivalent local de get_current_user_id() (Supabase Auth n'est pas utilisé)

CREATE OR REPLACE FUNCTION get_current_user_id()
RETURNS INTEGER AS $$
DECLARE
    user_id INTEGER;
BEGIN
    BEGIN
        user_id := current_setting('app.current_user_id', true)::INTEGER;
    EXCEPTION
        WHEN OTHERS THEN
            RETURN NULL;
    END;
    RETURN user_id;
END;
$$ LANGUAGE plpgsql STABLE;

COMMENT ON FUNCTION get_current_user_id() IS 'Get current user_id from session variable (set via middleware)';


-- ============================================================
-- Row-Level Security (RLS)
-- ============================================================

ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_memories ENABLE ROW LEVEL SECURITY;
ALTER TABLE memory_corrections ENABLE ROW LEVEL SECURITY;
ALTER TABLE message_embeddings ENABLE ROW LEVEL SECURITY;
ALTER TABLE memory_embeddings ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversation_summaries ENABLE ROW LEVEL SECURITY;

-- Policies chat_sessions
CREATE POLICY sessions_tenant ON chat_sessions
    FOR ALL USING (tenant_id = get_current_tenant() OR is_superadmin());

CREATE POLICY sessions_user ON chat_sessions
    FOR SELECT USING (user_id = get_current_user_id() OR is_superadmin());

-- Policies chat_messages (via session)
CREATE POLICY messages_select ON chat_messages
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM chat_sessions s
            WHERE s.id = chat_messages.session_id
            AND (s.user_id = get_current_user_id() OR is_superadmin())
        )
    );

CREATE POLICY messages_insert ON chat_messages
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM chat_sessions s
            WHERE s.id = chat_messages.session_id
            AND s.user_id = get_current_user_id()
        )
    );

-- Policies user_memories
CREATE POLICY memories_tenant ON user_memories
    FOR ALL USING (tenant_id = get_current_tenant() OR is_superadmin());

CREATE POLICY memories_user ON user_memories
    FOR ALL USING (user_id = get_current_user_id() OR is_superadmin());

-- Policies memory_corrections (via memory)
CREATE POLICY corrections_select ON memory_corrections
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM user_memories m
            WHERE m.id = memory_corrections.memory_id
            AND (m.user_id = get_current_user_id() OR is_superadmin())
        )
    );


-- ============================================================
-- Functions
-- ============================================================

-- Fonction: Ajouter un message et mettre a jour la session
CREATE OR REPLACE FUNCTION add_chat_message(
    p_session_id UUID,
    p_role message_role,
    p_content TEXT,
    p_model VARCHAR DEFAULT NULL,
    p_provider VARCHAR DEFAULT NULL,
    p_tokens_input INTEGER DEFAULT 0,
    p_tokens_output INTEGER DEFAULT 0,
    p_latency_ms INTEGER DEFAULT NULL,
    p_metadata JSONB DEFAULT '{}'
) RETURNS UUID
LANGUAGE plpgsql
AS $$
DECLARE
    v_message_id UUID;
BEGIN
    -- Insert message
    INSERT INTO chat_messages (
        session_id, role, content, model, provider,
        tokens_input, tokens_output, latency_ms, metadata
    ) VALUES (
        p_session_id, p_role, p_content, p_model, p_provider,
        p_tokens_input, p_tokens_output, p_latency_ms, p_metadata
    )
    RETURNING id INTO v_message_id;

    -- Update session stats
    UPDATE chat_sessions
    SET
        message_count = message_count + 1,
        total_tokens = total_tokens + p_tokens_input + p_tokens_output,
        last_message_at = NOW(),
        updated_at = NOW()
    WHERE id = p_session_id;

    RETURN v_message_id;
END;
$$;

COMMENT ON FUNCTION add_chat_message IS 'Ajoute un message et met a jour les stats session';


-- Fonction: Upsert memoire
CREATE OR REPLACE FUNCTION upsert_memory(
    p_tenant_id UUID,
    p_user_id INTEGER,
    p_category memory_category,
    p_key VARCHAR,
    p_value TEXT,
    p_source VARCHAR DEFAULT 'extracted',
    p_confidence DECIMAL DEFAULT 0.80,
    p_message_id UUID DEFAULT NULL
) RETURNS UUID
LANGUAGE plpgsql
AS $$
DECLARE
    v_memory_id UUID;
    v_old_value TEXT;
BEGIN
    -- Check existing
    SELECT id, value INTO v_memory_id, v_old_value
    FROM user_memories
    WHERE user_id = p_user_id
      AND category = p_category
      AND key = p_key;

    IF v_memory_id IS NOT NULL THEN
        -- Update existing
        UPDATE user_memories
        SET
            value = p_value,
            confidence = p_confidence,
            source = p_source,
            updated_at = NOW()
        WHERE id = v_memory_id;

        -- Log correction if value changed
        IF v_old_value IS DISTINCT FROM p_value THEN
            INSERT INTO memory_corrections (memory_id, old_value, new_value, corrected_by)
            VALUES (v_memory_id, v_old_value, p_value, 'system');
        END IF;
    ELSE
        -- Insert new
        INSERT INTO user_memories (
            tenant_id, user_id, category, key, value,
            source, confidence, extracted_from
        ) VALUES (
            p_tenant_id, p_user_id, p_category, p_key, p_value,
            p_source, p_confidence, p_message_id
        )
        RETURNING id INTO v_memory_id;
    END IF;

    RETURN v_memory_id;
END;
$$;

COMMENT ON FUNCTION upsert_memory IS 'Insere ou met a jour une memoire avec historique';


-- Fonction: Obtenir le contexte memoire pour prompt
CREATE OR REPLACE FUNCTION get_memory_context(
    p_user_id INTEGER
) RETURNS TEXT
LANGUAGE plpgsql
AS $$
DECLARE
    v_context TEXT := '';
    v_record RECORD;
BEGIN
    -- Profile
    SELECT string_agg(key || ': ' || value, E'\n')
    INTO v_context
    FROM user_memories
    WHERE user_id = p_user_id
      AND category = 'profile'
      AND is_active = TRUE;

    IF v_context IS NOT NULL THEN
        v_context := 'Profil utilisateur:' || E'\n' || v_context || E'\n\n';
    ELSE
        v_context := '';
    END IF;

    -- Preferences
    FOR v_record IN
        SELECT key, value FROM user_memories
        WHERE user_id = p_user_id AND category = 'preference' AND is_active = TRUE
    LOOP
        v_context := v_context || 'Preference ' || v_record.key || ': ' || v_record.value || E'\n';
    END LOOP;

    -- Business
    FOR v_record IN
        SELECT key, value FROM user_memories
        WHERE user_id = p_user_id AND category = 'business' AND is_active = TRUE
    LOOP
        v_context := v_context || 'Business ' || v_record.key || ': ' || v_record.value || E'\n';
    END LOOP;

    RETURN TRIM(v_context);
END;
$$;

COMMENT ON FUNCTION get_memory_context IS 'Genere le contexte memoire pour injection dans prompts';


-- ============================================================
-- Views
-- ============================================================

-- Vue: Resume memoire par user
CREATE OR REPLACE VIEW user_memory_summary AS
SELECT
    user_id,
    tenant_id,
    category,
    COUNT(*) as count,
    MAX(updated_at) as last_updated,
    AVG(confidence) as avg_confidence
FROM user_memories
WHERE is_active = TRUE
GROUP BY user_id, tenant_id, category;

COMMENT ON VIEW user_memory_summary IS 'Resume des memoires par utilisateur et categorie';


-- Vue: Conversations recentes
CREATE OR REPLACE VIEW recent_conversations AS
SELECT
    s.id,
    s.tenant_id,
    s.user_id,
    s.title,
    s.app_context,
    s.language,
    s.message_count,
    s.total_tokens,
    s.last_message_at,
    s.is_starred,
    (
        SELECT content
        FROM chat_messages
        WHERE session_id = s.id
        ORDER BY created_at DESC
        LIMIT 1
    ) as last_message
FROM chat_sessions s
WHERE s.is_archived = FALSE
ORDER BY s.last_message_at DESC;

COMMENT ON VIEW recent_conversations IS 'Conversations recentes non archivees';


-- ============================================================
-- Triggers
-- ============================================================

-- Trigger: Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_sessions_updated
    BEFORE UPDATE ON chat_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER tr_memories_updated
    BEFORE UPDATE ON user_memories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();


-- ============================================================
-- Donnees initiales: Cles memoire predefinies
-- ============================================================

-- Table de reference pour les cles memoire (documentation)
CREATE TABLE IF NOT EXISTS memory_keys_reference (
    category memory_category NOT NULL,
    key VARCHAR(100) NOT NULL,
    description TEXT,
    value_type VARCHAR(20) DEFAULT 'text',
    examples TEXT[],
    PRIMARY KEY (category, key)
);

INSERT INTO memory_keys_reference (category, key, description, value_type, examples) VALUES
    -- Profile
    ('profile', 'name', 'Nom complet', 'text', ARRAY['Mohamed', 'Fatima Zohra']),
    ('profile', 'first_name', 'Prenom', 'text', ARRAY['Yacine', 'Amina']),
    ('profile', 'company', 'Nom entreprise', 'text', ARRAY['IA Factory', 'Sonelgaz']),
    ('profile', 'role', 'Poste/Fonction', 'text', ARRAY['CEO', 'Developpeur', 'Comptable']),
    ('profile', 'sector', 'Secteur activite', 'text', ARRAY['Tech', 'Commerce', 'Sante']),
    ('profile', 'location', 'Ville/Wilaya', 'text', ARRAY['Alger', 'Oran', 'Constantine']),

    -- Preferences
    ('preference', 'language', 'Langue preferee', 'text', ARRAY['fr', 'ar', 'dz-ar', 'en']),
    ('preference', 'response_style', 'Style reponse', 'text', ARRAY['concis', 'detaille', 'technique']),
    ('preference', 'formality', 'Niveau formalite', 'text', ARRAY['formel', 'informel', 'mixte']),
    ('preference', 'expertise_level', 'Niveau expertise', 'text', ARRAY['debutant', 'intermediaire', 'expert']),

    -- Business
    ('business', 'company_size', 'Taille entreprise', 'text', ARRAY['TPE', 'PME', 'Grande entreprise']),
    ('business', 'employees', 'Nombre employes', 'number', ARRAY['5', '50', '500']),
    ('business', 'revenue', 'CA mensuel/annuel', 'text', ARRAY['5M DZD/mois', '100M DZD/an']),
    ('business', 'software', 'Logiciels utilises', 'list', ARRAY['Sage', 'Excel', 'Odoo']),
    ('business', 'challenges', 'Defis principaux', 'text', ARRAY['Facturation', 'RH', 'Marketing']),

    -- Facts
    ('fact', 'important_date', 'Date importante', 'date', ARRAY['2025-01-01', 'Ramadan 2025']),
    ('fact', 'event', 'Evenement', 'text', ARRAY['Lancement produit', 'Reunion partenaire']),

    -- Goals
    ('goal', 'objective', 'Objectif', 'text', ARRAY['Automatiser facturation', 'Former equipe IA']),
    ('goal', 'project', 'Projet en cours', 'text', ARRAY['Migration cloud', 'App mobile'])

ON CONFLICT (category, key) DO NOTHING;

COMMENT ON TABLE memory_keys_reference IS 'Reference des cles memoire disponibles (documentation)';


COMMIT;
