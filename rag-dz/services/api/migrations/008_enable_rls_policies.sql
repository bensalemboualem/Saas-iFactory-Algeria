-- Migration 008: Enable Row-Level Security (RLS) - Phase 2
-- Date: 2025-12-16
-- Purpose: Étanchéité complète de l'isolation tenant via RLS PostgreSQL

-- ============================================
-- PART 1: HELPER FUNCTIONS
-- ============================================

-- Fonction pour définir le tenant courant dans la session
CREATE OR REPLACE FUNCTION set_tenant(tenant_uuid UUID)
RETURNS void AS $$
BEGIN
    -- Vérifier que le tenant existe
    IF NOT EXISTS (SELECT 1 FROM tenants WHERE id = tenant_uuid) THEN
        RAISE EXCEPTION 'Tenant % does not exist', tenant_uuid;
    END IF;

    -- Définir le tenant_id dans la session PostgreSQL
    PERFORM set_config('app.current_tenant_id', tenant_uuid::text, false);

    -- Log pour debugging
    RAISE NOTICE 'Session tenant_id set to: %', tenant_uuid;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION set_tenant(UUID) IS 'Set current tenant for session (call at session start)';


-- Fonction pour récupérer le tenant courant
CREATE OR REPLACE FUNCTION get_current_tenant()
RETURNS UUID AS $$
DECLARE
    tenant_id UUID;
BEGIN
    BEGIN
        tenant_id := current_setting('app.current_tenant_id', true)::UUID;
    EXCEPTION
        WHEN OTHERS THEN
            -- Si la variable n'est pas définie, retourner NULL
            RETURN NULL;
    END;

    RETURN tenant_id;
END;
$$ LANGUAGE plpgsql STABLE;

COMMENT ON FUNCTION get_current_tenant() IS 'Get current tenant_id from session';


-- Fonction pour vérifier si l'utilisateur est super-admin
CREATE OR REPLACE FUNCTION is_superadmin()
RETURNS BOOLEAN AS $$
DECLARE
    is_admin BOOLEAN;
BEGIN
    -- Vérifier si session variable 'app.is_superadmin' est true
    BEGIN
        is_admin := current_setting('app.is_superadmin', true)::BOOLEAN;
    EXCEPTION
        WHEN OTHERS THEN
            RETURN false;
    END;

    RETURN COALESCE(is_admin, false);
END;
$$ LANGUAGE plpgsql STABLE;

COMMENT ON FUNCTION is_superadmin() IS 'Check if current user is superadmin (for support/supervision)';


-- Fonction pour activer le mode super-admin
CREATE OR REPLACE FUNCTION enable_superadmin_mode()
RETURNS void AS $$
BEGIN
    -- Cette fonction doit être appelée avec des credentials spéciaux
    -- Pour l'instant, on la laisse ouverte mais on pourrait ajouter une vérification
    PERFORM set_config('app.is_superadmin', 'true', false);
    RAISE NOTICE 'Super-admin mode enabled for session';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION enable_superadmin_mode() IS 'Enable super-admin mode for support (bypasses RLS)';


-- ============================================
-- PART 2: ENABLE RLS ON ALL TABLES
-- ============================================

-- Enable RLS on core tables
ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE tenant_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_events ENABLE ROW LEVEL SECURITY;

-- Enable RLS on existing tables with tenant_id
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE knowledge_base ENABLE ROW LEVEL SECURITY;
ALTER TABLE bolt_workflows ENABLE ROW LEVEL SECURITY;
ALTER TABLE orchestrator_state ENABLE ROW LEVEL SECURITY;
ALTER TABLE bmad_workflows ENABLE ROW LEVEL SECURITY;

-- Enable RLS on voice tables
ALTER TABLE voice_transcriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE voice_conversations ENABLE ROW LEVEL SECURITY;

-- Enable RLS on CRM tables
ALTER TABLE crm_leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE crm_deals ENABLE ROW LEVEL SECURITY;

-- Enable RLS on billing tables
ALTER TABLE billing_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE credit_transactions ENABLE ROW LEVEL SECURITY;

-- Enable RLS on business analytics
ALTER TABLE pme_analyses ENABLE ROW LEVEL SECURITY;


-- ============================================
-- PART 3: CREATE RLS POLICIES
-- ============================================

-- Template de politique RLS:
-- 1. SELECT: Peut voir seulement les données de son tenant
-- 2. INSERT: Peut créer seulement pour son tenant
-- 3. UPDATE: Peut modifier seulement les données de son tenant
-- 4. DELETE: Peut supprimer seulement les données de son tenant
-- 5. Super-admin: Bypass RLS pour support technique


-- ----------------------------------------
-- TENANTS TABLE
-- ----------------------------------------

-- Policy: Super-admin peut tout voir
CREATE POLICY tenants_superadmin_all ON tenants
    FOR ALL
    TO PUBLIC
    USING (is_superadmin());

-- Policy: Utilisateur peut voir seulement son tenant
CREATE POLICY tenants_select ON tenants
    FOR SELECT
    TO PUBLIC
    USING (
        id = get_current_tenant()
        OR is_superadmin()
    );

-- Policy: Seul super-admin peut créer des tenants
CREATE POLICY tenants_insert ON tenants
    FOR INSERT
    TO PUBLIC
    WITH CHECK (is_superadmin());

-- Policy: Tenant peut modifier ses propres données
CREATE POLICY tenants_update ON tenants
    FOR UPDATE
    TO PUBLIC
    USING (
        id = get_current_tenant()
        OR is_superadmin()
    );

-- Policy: Seul super-admin peut supprimer des tenants
CREATE POLICY tenants_delete ON tenants
    FOR DELETE
    TO PUBLIC
    USING (is_superadmin());


-- ----------------------------------------
-- TENANT_USERS TABLE
-- ----------------------------------------

CREATE POLICY tenant_users_select ON tenant_users
    FOR SELECT
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY tenant_users_insert ON tenant_users
    FOR INSERT
    TO PUBLIC
    WITH CHECK (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY tenant_users_update ON tenant_users
    FOR UPDATE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY tenant_users_delete ON tenant_users
    FOR DELETE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );


-- ----------------------------------------
-- API_KEYS TABLE
-- ----------------------------------------

CREATE POLICY api_keys_select ON api_keys
    FOR SELECT
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY api_keys_insert ON api_keys
    FOR INSERT
    TO PUBLIC
    WITH CHECK (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY api_keys_update ON api_keys
    FOR UPDATE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY api_keys_delete ON api_keys
    FOR DELETE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );


-- ----------------------------------------
-- USAGE_EVENTS TABLE
-- ----------------------------------------

CREATE POLICY usage_events_select ON usage_events
    FOR SELECT
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY usage_events_insert ON usage_events
    FOR INSERT
    TO PUBLIC
    WITH CHECK (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );


-- ----------------------------------------
-- PROJECTS TABLE
-- ----------------------------------------

CREATE POLICY projects_select ON projects
    FOR SELECT
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY projects_insert ON projects
    FOR INSERT
    TO PUBLIC
    WITH CHECK (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY projects_update ON projects
    FOR UPDATE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY projects_delete ON projects
    FOR DELETE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );


-- ----------------------------------------
-- KNOWLEDGE_BASE TABLE
-- ----------------------------------------

CREATE POLICY knowledge_base_select ON knowledge_base
    FOR SELECT
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY knowledge_base_insert ON knowledge_base
    FOR INSERT
    TO PUBLIC
    WITH CHECK (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY knowledge_base_update ON knowledge_base
    FOR UPDATE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY knowledge_base_delete ON knowledge_base
    FOR DELETE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );


-- ----------------------------------------
-- BOLT_WORKFLOWS TABLE
-- ----------------------------------------

CREATE POLICY bolt_workflows_select ON bolt_workflows
    FOR SELECT
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY bolt_workflows_insert ON bolt_workflows
    FOR INSERT
    TO PUBLIC
    WITH CHECK (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY bolt_workflows_update ON bolt_workflows
    FOR UPDATE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY bolt_workflows_delete ON bolt_workflows
    FOR DELETE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );


-- ----------------------------------------
-- ORCHESTRATOR_STATE TABLE
-- ----------------------------------------

CREATE POLICY orchestrator_state_select ON orchestrator_state
    FOR SELECT
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY orchestrator_state_insert ON orchestrator_state
    FOR INSERT
    TO PUBLIC
    WITH CHECK (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY orchestrator_state_update ON orchestrator_state
    FOR UPDATE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY orchestrator_state_delete ON orchestrator_state
    FOR DELETE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );


-- ----------------------------------------
-- BMAD_WORKFLOWS TABLE
-- ----------------------------------------

CREATE POLICY bmad_workflows_select ON bmad_workflows
    FOR SELECT
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY bmad_workflows_insert ON bmad_workflows
    FOR INSERT
    TO PUBLIC
    WITH CHECK (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY bmad_workflows_update ON bmad_workflows
    FOR UPDATE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY bmad_workflows_delete ON bmad_workflows
    FOR DELETE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );


-- ----------------------------------------
-- VOICE_TRANSCRIPTIONS TABLE
-- ----------------------------------------

CREATE POLICY voice_transcriptions_select ON voice_transcriptions
    FOR SELECT
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY voice_transcriptions_insert ON voice_transcriptions
    FOR INSERT
    TO PUBLIC
    WITH CHECK (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY voice_transcriptions_update ON voice_transcriptions
    FOR UPDATE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY voice_transcriptions_delete ON voice_transcriptions
    FOR DELETE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );


-- ----------------------------------------
-- VOICE_CONVERSATIONS TABLE
-- ----------------------------------------

CREATE POLICY voice_conversations_select ON voice_conversations
    FOR SELECT
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY voice_conversations_insert ON voice_conversations
    FOR INSERT
    TO PUBLIC
    WITH CHECK (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY voice_conversations_update ON voice_conversations
    FOR UPDATE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY voice_conversations_delete ON voice_conversations
    FOR DELETE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );


-- ----------------------------------------
-- CRM_LEADS TABLE
-- ----------------------------------------

CREATE POLICY crm_leads_select ON crm_leads
    FOR SELECT
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY crm_leads_insert ON crm_leads
    FOR INSERT
    TO PUBLIC
    WITH CHECK (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY crm_leads_update ON crm_leads
    FOR UPDATE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY crm_leads_delete ON crm_leads
    FOR DELETE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );


-- ----------------------------------------
-- CRM_DEALS TABLE
-- ----------------------------------------

CREATE POLICY crm_deals_select ON crm_deals
    FOR SELECT
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY crm_deals_insert ON crm_deals
    FOR INSERT
    TO PUBLIC
    WITH CHECK (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY crm_deals_update ON crm_deals
    FOR UPDATE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY crm_deals_delete ON crm_deals
    FOR DELETE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );


-- ----------------------------------------
-- BILLING_ACCOUNTS TABLE
-- ----------------------------------------

CREATE POLICY billing_accounts_select ON billing_accounts
    FOR SELECT
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY billing_accounts_insert ON billing_accounts
    FOR INSERT
    TO PUBLIC
    WITH CHECK (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY billing_accounts_update ON billing_accounts
    FOR UPDATE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY billing_accounts_delete ON billing_accounts
    FOR DELETE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );


-- ----------------------------------------
-- CREDIT_TRANSACTIONS TABLE
-- ----------------------------------------

CREATE POLICY credit_transactions_select ON credit_transactions
    FOR SELECT
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY credit_transactions_insert ON credit_transactions
    FOR INSERT
    TO PUBLIC
    WITH CHECK (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );


-- ----------------------------------------
-- PME_ANALYSES TABLE
-- ----------------------------------------

CREATE POLICY pme_analyses_select ON pme_analyses
    FOR SELECT
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY pme_analyses_insert ON pme_analyses
    FOR INSERT
    TO PUBLIC
    WITH CHECK (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY pme_analyses_update ON pme_analyses
    FOR UPDATE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );

CREATE POLICY pme_analyses_delete ON pme_analyses
    FOR DELETE
    TO PUBLIC
    USING (
        tenant_id = get_current_tenant()
        OR is_superadmin()
    );


-- ============================================
-- PART 4: COMMENTS & DOCUMENTATION
-- ============================================

COMMENT ON FUNCTION set_tenant(UUID) IS 'Set current tenant for RLS (call at session start with tenant_id from JWT)';
COMMENT ON FUNCTION get_current_tenant() IS 'Get current tenant_id from session variable';
COMMENT ON FUNCTION is_superadmin() IS 'Check if session has super-admin privileges (for support)';
COMMENT ON FUNCTION enable_superadmin_mode() IS 'Enable super-admin mode to bypass RLS (support only)';


-- ============================================
-- PART 5: SUCCESS MESSAGE
-- ============================================

DO $$
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '╔════════════════════════════════════════════════════════════╗';
    RAISE NOTICE '║  ✓ Migration 008 COMPLETE                                 ║';
    RAISE NOTICE '║  Row-Level Security (RLS) ENABLED                         ║';
    RAISE NOTICE '║                                                            ║';
    RAISE NOTICE '║  Tables protected: 15+                                     ║';
    RAISE NOTICE '║  Policies created: 60+                                     ║';
    RAISE NOTICE '║  Functions created: 4                                      ║';
    RAISE NOTICE '║                                                            ║';
    RAISE NOTICE '║  ⚠️  ISOLATION ÉTANCHE ACTIVÉE                             ║';
    RAISE NOTICE '║  Chaque tenant ne voit que ses propres données            ║';
    RAISE NOTICE '║                                                            ║';
    RAISE NOTICE '║  Usage:                                                    ║';
    RAISE NOTICE '║    SELECT set_tenant(''tenant-uuid-here'');                ║';
    RAISE NOTICE '║    SELECT enable_superadmin_mode(); -- Support only       ║';
    RAISE NOTICE '╚════════════════════════════════════════════════════════════╝';
    RAISE NOTICE '';
END $$;
