CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Types énumérés
CREATE TYPE tenant_plan AS ENUM ('free', 'pro', 'enterprise');
CREATE TYPE tenant_status AS ENUM ('active', 'suspended', 'deleted');

-- Tenants
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    plan tenant_plan NOT NULL DEFAULT 'free',
    status tenant_status NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- API Keys
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    key_hash TEXT UNIQUE NOT NULL,
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    name TEXT NOT NULL DEFAULT 'Default Key',
    plan tenant_plan NOT NULL,
    quota_tokens_monthly BIGINT NOT NULL DEFAULT 100000,
    quota_audio_seconds_monthly INTEGER NOT NULL DEFAULT 1800,
    quota_ocr_pages_monthly INTEGER NOT NULL DEFAULT 50,
    rate_limit_per_minute INTEGER NOT NULL DEFAULT 10,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    revoked BOOLEAN DEFAULT FALSE
);

-- Usage events
CREATE TABLE usage_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    request_id TEXT,
    route TEXT NOT NULL,
    method TEXT NOT NULL,
    tokens_input INTEGER DEFAULT 0,
    tokens_output INTEGER DEFAULT 0,
    audio_seconds DECIMAL(10,2) DEFAULT 0,
    ocr_pages INTEGER DEFAULT 0,
    latency_ms INTEGER NOT NULL,
    model_used TEXT,
    status_code INTEGER NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour performance
CREATE INDEX idx_usage_tenant_month ON usage_events (tenant_id, date_trunc('month', timestamp));
CREATE INDEX idx_api_keys_tenant ON api_keys (tenant_id) WHERE NOT revoked;
