-- ============================================
-- IAFactory Multi-Tenant RLS Migration
-- ============================================
-- Execute avec: psql -d archon -f multi_tenant_rls.sql
-- ============================================

-- 1. Extensions requises
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Types enum (si pas deja crees)
DO $$ BEGIN
    CREATE TYPE tenant_plan AS ENUM ('free', 'pro', 'enterprise');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE tenant_status AS ENUM ('active', 'suspended', 'deleted');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('owner', 'admin', 'member', 'viewer');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- ============================================
-- 3. TABLES PRINCIPALES
-- ============================================

-- Tenants (organisations/entreprises)
CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE,
    region TEXT DEFAULT 'DZ',  -- DZ, CH, FR, etc.
    plan tenant_plan NOT NULL DEFAULT 'free',
    status tenant_status NOT NULL DEFAULT 'active',
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Users (utilisateurs avec tenant)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT,
    role user_role DEFAULT 'member',
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- API Keys (cles API par tenant)
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    key_hash TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL DEFAULT 'Default Key',
    plan tenant_plan NOT NULL DEFAULT 'free',
    quota_tokens_monthly BIGINT NOT NULL DEFAULT 100000,
    quota_audio_seconds_monthly INTEGER NOT NULL DEFAULT 1800,
    quota_ocr_pages_monthly INTEGER NOT NULL DEFAULT 50,
    rate_limit_per_minute INTEGER NOT NULL DEFAULT 10,
    revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ
);

-- Usage Events (tracking par tenant)
CREATE TABLE IF NOT EXISTS usage_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    request_id TEXT,
    route TEXT NOT NULL,
    method TEXT NOT NULL DEFAULT 'POST',
    tokens_input INTEGER DEFAULT 0,
    tokens_output INTEGER DEFAULT 0,
    audio_seconds DECIMAL(10,2) DEFAULT 0,
    ocr_pages INTEGER DEFAULT 0,
    latency_ms INTEGER NOT NULL DEFAULT 0,
    model_used TEXT,
    status_code INTEGER NOT NULL DEFAULT 200,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Projects (projets par tenant)
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'active',
    settings JSONB DEFAULT '{}',
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Documents (documents par tenant)
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    name TEXT NOT NULL,
    file_path TEXT,
    file_type TEXT,
    file_size BIGINT,
    status TEXT DEFAULT 'pending',
    metadata JSONB DEFAULT '{}',
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Conversations (historique chat par tenant)
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    title TEXT,
    model TEXT DEFAULT 'claude-3-5-sonnet',
    messages JSONB DEFAULT '[]',
    tokens_used INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- 4. INDEXES POUR PERFORMANCE
-- ============================================

CREATE INDEX IF NOT EXISTS idx_users_tenant ON users(tenant_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_api_keys_tenant ON api_keys(tenant_id) WHERE NOT revoked;
CREATE INDEX IF NOT EXISTS idx_usage_tenant_month ON usage_events(tenant_id, date_trunc('month', timestamp));
CREATE INDEX IF NOT EXISTS idx_projects_tenant ON projects(tenant_id);
CREATE INDEX IF NOT EXISTS idx_documents_tenant ON documents(tenant_id);
CREATE INDEX IF NOT EXISTS idx_conversations_tenant ON conversations(tenant_id);

-- ============================================
-- 5. FONCTIONS RLS
-- ============================================

-- Variable de session pour tenant_id
CREATE OR REPLACE FUNCTION set_tenant(p_tenant_id UUID)
RETURNS VOID AS $$
BEGIN
    PERFORM set_config('app.current_tenant_id', p_tenant_id::TEXT, FALSE);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Recuperer tenant_id courant
CREATE OR REPLACE FUNCTION current_tenant_id()
RETURNS UUID AS $$
BEGIN
    RETURN NULLIF(current_setting('app.current_tenant_id', TRUE), '')::UUID;
EXCEPTION WHEN OTHERS THEN
    RETURN NULL;
END;
$$ LANGUAGE plpgsql STABLE;

-- Mode super-admin (bypass RLS)
CREATE OR REPLACE FUNCTION enable_superadmin_mode()
RETURNS VOID AS $$
BEGIN
    PERFORM set_config('app.superadmin_mode', 'true', FALSE);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Verifier si super-admin
CREATE OR REPLACE FUNCTION is_superadmin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN COALESCE(current_setting('app.superadmin_mode', TRUE), 'false') = 'true';
END;
$$ LANGUAGE plpgsql STABLE;

-- ============================================
-- 6. ROW LEVEL SECURITY (RLS)
-- ============================================

-- Activer RLS sur toutes les tables tenant-aware
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;

-- Policy: Users
DROP POLICY IF EXISTS tenant_isolation_users ON users;
CREATE POLICY tenant_isolation_users ON users
    FOR ALL
    USING (
        is_superadmin() OR
        tenant_id = current_tenant_id()
    )
    WITH CHECK (
        is_superadmin() OR
        tenant_id = current_tenant_id()
    );

-- Policy: API Keys
DROP POLICY IF EXISTS tenant_isolation_api_keys ON api_keys;
CREATE POLICY tenant_isolation_api_keys ON api_keys
    FOR ALL
    USING (
        is_superadmin() OR
        tenant_id = current_tenant_id()
    )
    WITH CHECK (
        is_superadmin() OR
        tenant_id = current_tenant_id()
    );

-- Policy: Usage Events
DROP POLICY IF EXISTS tenant_isolation_usage ON usage_events;
CREATE POLICY tenant_isolation_usage ON usage_events
    FOR ALL
    USING (
        is_superadmin() OR
        tenant_id = current_tenant_id()
    )
    WITH CHECK (
        is_superadmin() OR
        tenant_id = current_tenant_id()
    );

-- Policy: Projects
DROP POLICY IF EXISTS tenant_isolation_projects ON projects;
CREATE POLICY tenant_isolation_projects ON projects
    FOR ALL
    USING (
        is_superadmin() OR
        tenant_id = current_tenant_id()
    )
    WITH CHECK (
        is_superadmin() OR
        tenant_id = current_tenant_id()
    );

-- Policy: Documents
DROP POLICY IF EXISTS tenant_isolation_documents ON documents;
CREATE POLICY tenant_isolation_documents ON documents
    FOR ALL
    USING (
        is_superadmin() OR
        tenant_id = current_tenant_id()
    )
    WITH CHECK (
        is_superadmin() OR
        tenant_id = current_tenant_id()
    );

-- Policy: Conversations
DROP POLICY IF EXISTS tenant_isolation_conversations ON conversations;
CREATE POLICY tenant_isolation_conversations ON conversations
    FOR ALL
    USING (
        is_superadmin() OR
        tenant_id = current_tenant_id()
    )
    WITH CHECK (
        is_superadmin() OR
        tenant_id = current_tenant_id()
    );

-- ============================================
-- 7. TRIGGERS POUR updated_at
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_tenants_updated ON tenants;
CREATE TRIGGER trg_tenants_updated
    BEFORE UPDATE ON tenants
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

DROP TRIGGER IF EXISTS trg_users_updated ON users;
CREATE TRIGGER trg_users_updated
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

DROP TRIGGER IF EXISTS trg_projects_updated ON projects;
CREATE TRIGGER trg_projects_updated
    BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

DROP TRIGGER IF EXISTS trg_conversations_updated ON conversations;
CREATE TRIGGER trg_conversations_updated
    BEFORE UPDATE ON conversations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================
-- 8. SEED DATA - Tenant par defaut
-- ============================================

-- Creer tenant par defaut pour dev
INSERT INTO tenants (id, name, slug, region, plan, status)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'IAFactory Algeria',
    'iafactory-dz',
    'DZ',
    'enterprise',
    'active'
) ON CONFLICT (id) DO NOTHING;

-- Creer admin par defaut
INSERT INTO users (id, tenant_id, email, password_hash, name, role)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    '00000000-0000-0000-0000-000000000001',
    'admin@iafactoryalgeria.com',
    -- Password: admin123 (a changer en production!)
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4UQK.VvhJqsw.5Zy',
    'Admin IAFactory',
    'owner'
) ON CONFLICT (email) DO NOTHING;

-- ============================================
-- 9. VUES UTILES
-- ============================================

-- Vue: Usage mensuel par tenant
CREATE OR REPLACE VIEW v_tenant_monthly_usage AS
SELECT
    tenant_id,
    date_trunc('month', timestamp) as month,
    COUNT(*) as total_requests,
    SUM(tokens_input + tokens_output) as total_tokens,
    SUM(audio_seconds) as total_audio_seconds,
    SUM(ocr_pages) as total_ocr_pages,
    AVG(latency_ms)::INTEGER as avg_latency_ms
FROM usage_events
GROUP BY tenant_id, date_trunc('month', timestamp);

-- Vue: Tenants avec stats
CREATE OR REPLACE VIEW v_tenants_with_stats AS
SELECT
    t.id,
    t.name,
    t.slug,
    t.region,
    t.plan,
    t.status,
    t.created_at,
    COUNT(DISTINCT u.id) as user_count,
    COUNT(DISTINCT p.id) as project_count,
    COUNT(DISTINCT d.id) as document_count
FROM tenants t
LEFT JOIN users u ON u.tenant_id = t.id
LEFT JOIN projects p ON p.tenant_id = t.id
LEFT JOIN documents d ON d.tenant_id = t.id
GROUP BY t.id;

-- ============================================
-- 10. GRANTS (permissions)
-- ============================================

-- L'application utilise le role 'postgres' par defaut
-- En production, creer un role dedie avec permissions limitees

GRANT ALL ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO postgres;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO postgres;

-- ============================================
-- FIN MIGRATION MULTI-TENANT
-- ============================================

-- Pour verifier l'installation:
-- SELECT * FROM tenants;
-- SELECT * FROM users;
-- SELECT set_tenant('00000000-0000-0000-0000-000000000001');
-- SELECT current_tenant_id();
