-- Migration 016: FORCE Row-Level Security on ALL tenant-aware tables
-- Date: 2025-12-30
-- Author: Claude (Lead Engineer)
--
-- SÉCURITÉ CRITIQUE:
-- ENABLE RLS vs FORCE RLS:
--   - ENABLE RLS: Le table owner (postgres) contourne les policies
--   - FORCE RLS: PERSONNE ne contourne les policies, même postgres
--
-- Sans FORCE, si l'application se connecte en tant que postgres (ou owner),
-- toutes les policies RLS sont ignorées = FAILLE MAJEURE
--
-- Cette migration ajoute FORCE ROW LEVEL SECURITY à TOUTES les tables
-- qui ont tenant_id pour garantir l'isolation même avec le user postgres.
--
-- NOTE: Pas de transaction globale pour tolérer les tables manquantes.
-- Chaque table est traitée individuellement avec IF EXISTS.

-- ============================================
-- PART 1: FORCE RLS ON CORE TABLES
-- ============================================

-- Core multi-tenant tables
DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'tenants') THEN
        ALTER TABLE tenants FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to tenants';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'tenant_users') THEN
        ALTER TABLE tenant_users FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to tenant_users';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'api_keys') THEN
        ALTER TABLE api_keys FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to api_keys';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'usage_events') THEN
        ALTER TABLE usage_events FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to usage_events';
    END IF;
END $$;

-- ============================================
-- PART 2: FORCE RLS ON BUSINESS TABLES
-- ============================================

-- Projects & Knowledge
DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'projects') THEN
        ALTER TABLE projects FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to projects';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'knowledge_base') THEN
        ALTER TABLE knowledge_base FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to knowledge_base';
    END IF;
END $$;

-- Workflows
DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'bolt_workflows') THEN
        ALTER TABLE bolt_workflows FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to bolt_workflows';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'orchestrator_state') THEN
        ALTER TABLE orchestrator_state FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to orchestrator_state';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'bmad_workflows') THEN
        ALTER TABLE bmad_workflows FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to bmad_workflows';
    END IF;
END $$;

-- Voice
DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'voice_transcriptions') THEN
        ALTER TABLE voice_transcriptions FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to voice_transcriptions';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'voice_conversations') THEN
        ALTER TABLE voice_conversations FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to voice_conversations';
    END IF;
END $$;

-- CRM
DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'crm_leads') THEN
        ALTER TABLE crm_leads FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to crm_leads';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'crm_deals') THEN
        ALTER TABLE crm_deals FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to crm_deals';
    END IF;
END $$;

-- Billing
DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'billing_accounts') THEN
        ALTER TABLE billing_accounts FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to billing_accounts';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'credit_transactions') THEN
        ALTER TABLE credit_transactions FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to credit_transactions';
    END IF;
END $$;

-- Analytics
DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'pme_analyses') THEN
        ALTER TABLE pme_analyses FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to pme_analyses';
    END IF;
END $$;

-- ============================================
-- PART 3: FORCE RLS ON NEW TABLES (014+)
-- ============================================

-- IAFactory Memory System (migration 014)
DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'user_memories') THEN
        ALTER TABLE user_memories FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to user_memories';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'memory_tags') THEN
        ALTER TABLE memory_tags FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to memory_tags';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'memory_associations') THEN
        ALTER TABLE memory_associations FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to memory_associations';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'chat_sessions') THEN
        ALTER TABLE chat_sessions FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to chat_sessions';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'chat_messages') THEN
        ALTER TABLE chat_messages FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to chat_messages';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'memory_corrections') THEN
        ALTER TABLE memory_corrections FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to memory_corrections';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'message_embeddings') THEN
        ALTER TABLE message_embeddings FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to message_embeddings';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'memory_embeddings') THEN
        ALTER TABLE memory_embeddings FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to memory_embeddings';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'conversation_summaries') THEN
        ALTER TABLE conversation_summaries FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to conversation_summaries';
    END IF;
END $$;

-- Conversations (migration 015)
DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'conversations') THEN
        ALTER TABLE conversations FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to conversations';
    END IF;
END $$;

-- ============================================
-- PART 4: FORCE RLS ON TOKEN TABLES
-- ============================================

-- Token System (migration 009)
DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'token_balances') THEN
        ALTER TABLE token_balances FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to token_balances';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'token_transactions') THEN
        ALTER TABLE token_transactions FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to token_transactions';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'tenant_token_balances') THEN
        ALTER TABLE tenant_token_balances FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to tenant_token_balances';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'token_usage_logs') THEN
        ALTER TABLE token_usage_logs FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to token_usage_logs';
    END IF;
END $$;

-- Token Packs (migration 013)
DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'token_purchases') THEN
        ALTER TABLE token_purchases FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to token_purchases';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'token_packs') THEN
        ALTER TABLE token_packs FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to token_packs';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'provider_rates') THEN
        ALTER TABLE provider_rates FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to provider_rates';
    END IF;
END $$;

-- ============================================
-- PART 5: FORCE RLS ON LEXICON & LIFE OPS
-- ============================================

-- Personal Lexicon (migration 010)
DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'personal_lexicon') THEN
        ALTER TABLE personal_lexicon FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to personal_lexicon';
    END IF;
END $$;

-- Life Operations (migration 012)
DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'life_operations') THEN
        ALTER TABLE life_operations FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to life_operations';
    END IF;
END $$;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'life_categories') THEN
        ALTER TABLE life_categories FORCE ROW LEVEL SECURITY;
        RAISE NOTICE 'FORCE RLS applied to life_categories';
    END IF;
END $$;

-- ============================================
-- PART 6: CATCH-ALL FOR ANY MISSED TABLES
-- ============================================

-- Dynamically find and force RLS on any table with tenant_id that doesn't have FORCE
DO $$
DECLARE
    tbl_name TEXT;
    force_enabled BOOLEAN;
BEGIN
    FOR tbl_name IN
        SELECT c.relname
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        JOIN pg_attribute a ON a.attrelid = c.oid
        WHERE n.nspname = 'public'
        AND c.relkind = 'r'  -- regular table
        AND a.attname = 'tenant_id'
        AND c.relrowsecurity = true  -- RLS enabled
    LOOP
        -- Check if FORCE is already enabled
        SELECT c.relforcerowsecurity INTO force_enabled
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = 'public' AND c.relname = tbl_name;

        IF NOT force_enabled THEN
            EXECUTE format('ALTER TABLE %I FORCE ROW LEVEL SECURITY', tbl_name);
            RAISE NOTICE 'FORCE RLS applied to: %', tbl_name;
        END IF;
    END LOOP;
END $$;

-- ============================================
-- PART 7: VERIFICATION QUERY
-- ============================================

-- Create a view to easily check RLS status
CREATE OR REPLACE VIEW rls_status AS
SELECT
    c.relname AS table_name,
    c.relrowsecurity AS rls_enabled,
    c.relforcerowsecurity AS rls_forced,
    CASE
        WHEN c.relrowsecurity AND c.relforcerowsecurity THEN 'SECURE'
        WHEN c.relrowsecurity AND NOT c.relforcerowsecurity THEN 'PARTIAL (owner bypass)'
        ELSE 'DISABLED'
    END AS security_status,
    EXISTS (
        SELECT 1 FROM pg_attribute a
        WHERE a.attrelid = c.oid AND a.attname = 'tenant_id'
    ) AS has_tenant_id
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public'
AND c.relkind = 'r'
ORDER BY
    CASE WHEN c.relrowsecurity AND c.relforcerowsecurity THEN 0
         WHEN c.relrowsecurity THEN 1
         ELSE 2 END,
    c.relname;

COMMENT ON VIEW rls_status IS 'View to check RLS status of all tables - verify all tenant tables show SECURE';

-- ============================================
-- PART 8: FINAL VERIFICATION
-- ============================================

DO $$
DECLARE
    insecure_count INTEGER;
    insecure_tables TEXT;
BEGIN
    -- Count tables with tenant_id that don't have FORCE RLS
    SELECT
        COUNT(*),
        string_agg(c.relname, ', ')
    INTO insecure_count, insecure_tables
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    JOIN pg_attribute a ON a.attrelid = c.oid
    WHERE n.nspname = 'public'
    AND c.relkind = 'r'
    AND a.attname = 'tenant_id'
    AND (NOT c.relrowsecurity OR NOT c.relforcerowsecurity);

    IF insecure_count > 0 THEN
        RAISE WARNING 'INSECURE TABLES DETECTED: % tables without FORCE RLS: %',
            insecure_count, insecure_tables;
    ELSE
        RAISE NOTICE '';
        RAISE NOTICE '╔════════════════════════════════════════════════════════════╗';
        RAISE NOTICE '║  MIGRATION 016 COMPLETE - FORCE RLS APPLIED               ║';
        RAISE NOTICE '║                                                            ║';
        RAISE NOTICE '║  ALL tenant-aware tables now have FORCE RLS               ║';
        RAISE NOTICE '║  Even postgres user respects RLS policies                 ║';
        RAISE NOTICE '║                                                            ║';
        RAISE NOTICE '║  To verify: SELECT * FROM rls_status;                     ║';
        RAISE NOTICE '║  Expected: All tenant tables show "SECURE"                ║';
        RAISE NOTICE '╚════════════════════════════════════════════════════════════╝';
        RAISE NOTICE '';
    END IF;
END $$;
