-- =============================================
-- MIGRATION 015: Optimistic locking + RLS renforce
-- =============================================
-- Decisions verrouillees:
-- - Max 100 messages par conversation
-- - Optimistic lock via version field (pas de FOR UPDATE)
-- - tenant_id depuis JWT uniquement
-- - RLS FORCE (pas de bypass)
-- =============================================

-- 1. Ajouter colonne version si absente
ALTER TABLE conversations
ADD COLUMN IF NOT EXISTS version INTEGER DEFAULT 1;

-- 2. Ajouter app_context si absent
ALTER TABLE conversations
ADD COLUMN IF NOT EXISTS app_context VARCHAR(50) DEFAULT 'chat';

-- 3. Forcer default JSONB (eviter NULL)
ALTER TABLE conversations
ALTER COLUMN messages SET DEFAULT '[]'::jsonb;

-- 4. Fix NULL existants
UPDATE conversations
SET messages = '[]'::jsonb
WHERE messages IS NULL;

-- 5. S'assurer que version n'est pas NULL
UPDATE conversations
SET version = 1
WHERE version IS NULL;

-- 6. Index performance
CREATE INDEX IF NOT EXISTS idx_conversations_tenant_user
ON conversations(tenant_id, user_id);

CREATE INDEX IF NOT EXISTS idx_conversations_updated
ON conversations(updated_at DESC);

CREATE INDEX IF NOT EXISTS idx_conversations_app_context
ON conversations(tenant_id, app_context);

-- 7. Trigger auto-increment version
CREATE OR REPLACE FUNCTION increment_conversation_version()
RETURNS TRIGGER AS $$
BEGIN
    NEW.version := COALESCE(OLD.version, 0) + 1;
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_conversation_version ON conversations;
CREATE TRIGGER trg_conversation_version
    BEFORE UPDATE ON conversations
    FOR EACH ROW
    EXECUTE FUNCTION increment_conversation_version();

-- 8. RLS FORCE (pas de bypass possible)
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations FORCE ROW LEVEL SECURITY;

-- 9. Policy RLS
DROP POLICY IF EXISTS tenant_isolation_conversations ON conversations;
CREATE POLICY tenant_isolation_conversations ON conversations
    USING (tenant_id::text = current_setting('app.current_tenant', true))
    WITH CHECK (tenant_id::text = current_setting('app.current_tenant', true));

-- 10. Fonction helper pour archivage
CREATE OR REPLACE FUNCTION archive_conversation(
    p_conversation_id UUID,
    p_tenant_id UUID,
    p_summary TEXT
) RETURNS UUID AS $$
DECLARE
    v_old_conv RECORD;
    v_new_id UUID;
    v_summary_msg JSONB;
BEGIN
    -- Configurer RLS
    PERFORM set_config('app.current_tenant', p_tenant_id::text, true);

    -- Recuperer ancienne conversation
    SELECT user_id, title, model, app_context
    INTO v_old_conv
    FROM conversations
    WHERE id = p_conversation_id AND tenant_id = p_tenant_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Conversation % not found for tenant %', p_conversation_id, p_tenant_id;
    END IF;

    -- Marquer comme archivee
    UPDATE conversations
    SET app_context = app_context || '_archived',
        title = COALESCE(title, 'Conversation') || ' (archivee)'
    WHERE id = p_conversation_id AND tenant_id = p_tenant_id;

    -- Creer message resume
    v_summary_msg := jsonb_build_object(
        'role', 'system',
        'content', '[Resume conversation precedente]' || E'\n' || p_summary,
        'timestamp', NOW()::text
    );

    -- Creer nouvelle conversation avec resume
    INSERT INTO conversations
        (tenant_id, user_id, title, model, app_context, messages, version)
    VALUES (
        p_tenant_id,
        v_old_conv.user_id,
        v_old_conv.title,
        v_old_conv.model,
        v_old_conv.app_context,
        jsonb_build_array(v_summary_msg),
        1
    )
    RETURNING id INTO v_new_id;

    RETURN v_new_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 11. Commentaires
COMMENT ON COLUMN conversations.version IS 'Version pour optimistic locking - auto-incremente par trigger';
COMMENT ON COLUMN conversations.app_context IS 'Contexte applicatif: chat, pme, rag, crm, bolt, voice, etc.';
COMMENT ON FUNCTION increment_conversation_version() IS 'Auto-increment version a chaque UPDATE';
COMMENT ON FUNCTION archive_conversation(UUID, UUID, TEXT) IS 'Archive conversation pleine et cree nouvelle avec resume';
