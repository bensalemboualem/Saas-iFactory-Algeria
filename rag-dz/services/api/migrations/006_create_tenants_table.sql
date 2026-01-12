-- Migration 006: Create tenants table for multi-tenant isolation
-- Date: 2025-12-16
-- Purpose: Enable data isolation per tenant (schools, medical offices, law firms)

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tenants table
CREATE TABLE IF NOT EXISTS tenants (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Basic info
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,

    -- Geographic region (DZ = Algeria, CH = Switzerland, FR = France)
    region VARCHAR(2) NOT NULL DEFAULT 'DZ',

    -- Subscription info
    plan VARCHAR(50) DEFAULT 'free' NOT NULL,  -- free, pro, enterprise
    status VARCHAR(50) DEFAULT 'active' NOT NULL,  -- active, suspended, trial, cancelled

    -- Contact
    admin_email VARCHAR(255) NOT NULL,
    admin_phone VARCHAR(50),

    -- Settings and metadata
    settings JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    trial_ends_at TIMESTAMP WITH TIME ZONE,

    -- Constraints
    CONSTRAINT tenants_region_valid CHECK (region IN ('DZ', 'CH', 'FR', 'BE', 'CA')),
    CONSTRAINT tenants_plan_valid CHECK (plan IN ('free', 'pro', 'enterprise')),
    CONSTRAINT tenants_status_valid CHECK (status IN ('active', 'suspended', 'trial', 'cancelled'))
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_tenants_slug ON tenants(slug);
CREATE INDEX IF NOT EXISTS idx_tenants_region ON tenants(region);
CREATE INDEX IF NOT EXISTS idx_tenants_status ON tenants(status);
CREATE INDEX IF NOT EXISTS idx_tenants_plan ON tenants(plan);
CREATE INDEX IF NOT EXISTS idx_tenants_created_at ON tenants(created_at DESC);

-- Trigger to auto-update updated_at
CREATE TRIGGER update_tenants_updated_at BEFORE UPDATE ON tenants
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create tenant_users junction table (many-to-many: users ↔ tenants)
CREATE TABLE IF NOT EXISTS tenant_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Role within tenant
    role VARCHAR(50) DEFAULT 'member' NOT NULL,  -- owner, admin, member, viewer

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,

    -- Constraints
    UNIQUE(tenant_id, user_id),
    CONSTRAINT tenant_users_role_valid CHECK (role IN ('owner', 'admin', 'member', 'viewer'))
);

-- Indexes for tenant_users
CREATE INDEX IF NOT EXISTS idx_tenant_users_tenant ON tenant_users(tenant_id);
CREATE INDEX IF NOT EXISTS idx_tenant_users_user ON tenant_users(user_id);
CREATE INDEX IF NOT EXISTS idx_tenant_users_role ON tenant_users(role);

-- Create API keys table for tenant authentication
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,

    -- Key info
    key_hash VARCHAR(64) UNIQUE NOT NULL,  -- SHA256 hash of the actual key
    key_prefix VARCHAR(20) NOT NULL,  -- First chars for identification (e.g., "sk_dz_abc...")
    name VARCHAR(255),  -- User-friendly name

    -- Permissions
    plan VARCHAR(50) DEFAULT 'free' NOT NULL,

    -- Rate limits & quotas
    rate_limit_per_minute INTEGER DEFAULT 60,
    quota_tokens_monthly INTEGER,
    quota_audio_seconds_monthly INTEGER,
    quota_ocr_pages_monthly INTEGER,

    -- Status
    revoked BOOLEAN DEFAULT FALSE NOT NULL,
    last_used_at TIMESTAMP WITH TIME ZONE,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE,

    -- Constraints
    CONSTRAINT api_keys_plan_valid CHECK (plan IN ('free', 'pro', 'enterprise'))
);

-- Indexes for api_keys
CREATE INDEX IF NOT EXISTS idx_api_keys_tenant ON api_keys(tenant_id);
CREATE INDEX IF NOT EXISTS idx_api_keys_hash ON api_keys(key_hash);
CREATE INDEX IF NOT EXISTS idx_api_keys_revoked ON api_keys(revoked) WHERE revoked = FALSE;

-- Create usage_events table for tracking API usage per tenant
CREATE TABLE IF NOT EXISTS usage_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,

    -- Request info
    request_id VARCHAR(255),
    route VARCHAR(255),
    method VARCHAR(10),

    -- Usage metrics
    tokens_input INTEGER DEFAULT 0,
    tokens_output INTEGER DEFAULT 0,
    audio_seconds REAL DEFAULT 0,
    ocr_pages INTEGER DEFAULT 0,

    -- Performance
    latency_ms INTEGER,
    model_used VARCHAR(100),
    status_code INTEGER,

    -- Timestamp
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Indexes for usage_events (optimized for analytics)
CREATE INDEX IF NOT EXISTS idx_usage_events_tenant ON usage_events(tenant_id);
CREATE INDEX IF NOT EXISTS idx_usage_events_created_at ON usage_events(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_usage_events_tenant_date ON usage_events(tenant_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_usage_events_route ON usage_events(route);

-- Partitioning for usage_events (optional, for high volume)
-- Note: Uncomment when usage grows beyond 10M rows
-- ALTER TABLE usage_events PARTITION BY RANGE (created_at);

-- Comments for documentation
COMMENT ON TABLE tenants IS 'Tenants for multi-tenant isolation (schools, medical offices, law firms)';
COMMENT ON COLUMN tenants.region IS 'Geographic region: DZ (Algeria), CH (Switzerland), FR (France)';
COMMENT ON COLUMN tenants.slug IS 'URL-friendly identifier (e.g., ecole-ibn-khaldoun-alger)';
COMMENT ON TABLE tenant_users IS 'Many-to-many relationship: users can belong to multiple tenants';
COMMENT ON TABLE api_keys IS 'API keys for tenant authentication and rate limiting';
COMMENT ON TABLE usage_events IS 'API usage events for billing and analytics per tenant';

-- Create default system tenant for testing
INSERT INTO tenants (id, name, slug, region, plan, status, admin_email)
VALUES (
    '00000000-0000-0000-0000-000000000000',
    'System Default',
    'system-default',
    'DZ',
    'enterprise',
    'active',
    'admin@rag.dz'
)
ON CONFLICT (id) DO NOTHING;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Migration 006 completed: tenants table created successfully';
END $$;
