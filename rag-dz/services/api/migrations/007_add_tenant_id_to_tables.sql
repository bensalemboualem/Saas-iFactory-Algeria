-- Migration 007: Add tenant_id to critical tables for multi-tenant isolation
-- Date: 2025-12-16
-- Purpose: Enable tenant isolation across all application tables

-- ============================================
-- CORE TABLES
-- ============================================

-- Add tenant_id to projects table
ALTER TABLE projects
    ADD COLUMN IF NOT EXISTS tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE;

-- Add tenant_id to knowledge_base table (documents)
ALTER TABLE knowledge_base
    ADD COLUMN IF NOT EXISTS tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE;

-- Add tenant_id to bolt_workflows table
ALTER TABLE bolt_workflows
    ADD COLUMN IF NOT EXISTS tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE;

-- Add tenant_id to orchestrator_state table
ALTER TABLE orchestrator_state
    ADD COLUMN IF NOT EXISTS tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE;

-- Add tenant_id to bmad_workflows table
ALTER TABLE bmad_workflows
    ADD COLUMN IF NOT EXISTS tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE;

-- ============================================
-- VOICE & TRANSCRIPTION TABLES
-- ============================================

-- Create voice_transcriptions table if not exists (for STT)
CREATE TABLE IF NOT EXISTS voice_transcriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,

    -- Audio file info
    filename VARCHAR(255),
    file_size_bytes INTEGER,
    duration_seconds REAL,
    audio_format VARCHAR(50),

    -- Transcription data
    text_raw TEXT,
    text_cleaned TEXT,
    text_normalized TEXT,

    -- Language & dialect
    language VARCHAR(10),
    language_confidence REAL,
    dialect VARCHAR(50),

    -- Model & backend used
    used_model VARCHAR(100),
    used_backend VARCHAR(50),

    -- Quality metrics
    confidence REAL,
    word_count INTEGER,

    -- Processing
    processing_time_ms INTEGER,
    status VARCHAR(50) DEFAULT 'completed',

    -- Metadata
    metadata JSONB DEFAULT '{}',

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,

    -- Constraints
    CONSTRAINT voice_transcriptions_status_valid CHECK (status IN ('pending', 'processing', 'completed', 'failed'))
);

-- Create voice_conversations table if not exists (for voice agent)
CREATE TABLE IF NOT EXISTS voice_conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,

    -- Conversation info
    title VARCHAR(255),
    context VARCHAR(50),  -- medical, legal, accounting, general

    -- Messages (stored as JSONB array)
    messages JSONB DEFAULT '[]',

    -- Stats
    message_count INTEGER DEFAULT 0,
    total_audio_seconds REAL DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,

    -- Status
    status VARCHAR(50) DEFAULT 'active',

    -- Metadata
    metadata JSONB DEFAULT '{}',

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,

    -- Constraints
    CONSTRAINT voice_conversations_status_valid CHECK (status IN ('active', 'archived', 'deleted'))
);

-- ============================================
-- CRM & BILLING TABLES
-- ============================================

-- Create crm_leads table if not exists
CREATE TABLE IF NOT EXISTS crm_leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,

    -- Lead info
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    company VARCHAR(255),

    -- Status & pipeline
    status VARCHAR(50) DEFAULT 'new',
    pipeline_stage VARCHAR(100),
    score INTEGER DEFAULT 0,

    -- Details
    source VARCHAR(100),
    notes TEXT,
    metadata JSONB DEFAULT '{}',

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    last_contacted_at TIMESTAMP WITH TIME ZONE,

    -- Constraints
    CONSTRAINT crm_leads_status_valid CHECK (status IN ('new', 'contacted', 'qualified', 'converted', 'lost'))
);

-- Create crm_deals table if not exists
CREATE TABLE IF NOT EXISTS crm_deals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    lead_id UUID REFERENCES crm_leads(id) ON DELETE SET NULL,

    -- Deal info
    name VARCHAR(255) NOT NULL,
    amount DECIMAL(15,2),
    currency VARCHAR(3) DEFAULT 'DZD',

    -- Status & pipeline
    status VARCHAR(50) DEFAULT 'pending',
    pipeline_stage VARCHAR(100),
    probability INTEGER DEFAULT 50,

    -- Dates
    expected_close_date DATE,
    actual_close_date DATE,

    -- Details
    notes TEXT,
    metadata JSONB DEFAULT '{}',

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,

    -- Constraints
    CONSTRAINT crm_deals_status_valid CHECK (status IN ('pending', 'won', 'lost', 'cancelled')),
    CONSTRAINT crm_deals_probability_valid CHECK (probability >= 0 AND probability <= 100)
);

-- Create billing_accounts table if not exists
CREATE TABLE IF NOT EXISTS billing_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,

    -- Balance & credits
    balance_credits INTEGER DEFAULT 0,
    balance_amount DECIMAL(15,2) DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'DZD',

    -- Usage this month
    usage_tokens_month INTEGER DEFAULT 0,
    usage_audio_seconds_month REAL DEFAULT 0,
    usage_ocr_pages_month INTEGER DEFAULT 0,

    -- Billing info
    billing_email VARCHAR(255),
    billing_address JSONB DEFAULT '{}',
    payment_method JSONB DEFAULT '{}',

    -- Status
    status VARCHAR(50) DEFAULT 'active',

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    last_invoice_at TIMESTAMP WITH TIME ZONE,

    -- Constraints
    CONSTRAINT billing_accounts_status_valid CHECK (status IN ('active', 'suspended', 'cancelled'))
);

-- Create credit_transactions table if not exists
CREATE TABLE IF NOT EXISTS credit_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    billing_account_id UUID REFERENCES billing_accounts(id) ON DELETE CASCADE,

    -- Transaction info
    type VARCHAR(50) NOT NULL,  -- purchase, usage, refund, bonus
    amount INTEGER NOT NULL,  -- Negative for usage, positive for purchase
    description TEXT,

    -- Related to
    usage_event_id UUID REFERENCES usage_events(id) ON DELETE SET NULL,

    -- Balance after transaction
    balance_after INTEGER,

    -- Metadata
    metadata JSONB DEFAULT '{}',

    -- Timestamp
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,

    -- Constraints
    CONSTRAINT credit_transactions_type_valid CHECK (type IN ('purchase', 'usage', 'refund', 'bonus', 'adjustment'))
);

-- ============================================
-- PME & BUSINESS ANALYZER TABLES
-- ============================================

-- Create pme_analyses table if not exists
CREATE TABLE IF NOT EXISTS pme_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,

    -- PME info
    company_name VARCHAR(255) NOT NULL,
    sector VARCHAR(100),
    region VARCHAR(50),

    -- Analysis data
    analysis_type VARCHAR(50),
    analysis_result JSONB DEFAULT '{}',
    score REAL,

    -- Status
    status VARCHAR(50) DEFAULT 'completed',

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,

    -- Constraints
    CONSTRAINT pme_analyses_status_valid CHECK (status IN ('pending', 'processing', 'completed', 'failed'))
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

-- Projects
CREATE INDEX IF NOT EXISTS idx_projects_tenant ON projects(tenant_id);
CREATE INDEX IF NOT EXISTS idx_projects_tenant_created ON projects(tenant_id, created_at DESC);

-- Knowledge Base (Documents)
CREATE INDEX IF NOT EXISTS idx_knowledge_base_tenant ON knowledge_base(tenant_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_tenant_created ON knowledge_base(tenant_id, created_at DESC);

-- Bolt Workflows
CREATE INDEX IF NOT EXISTS idx_bolt_workflows_tenant ON bolt_workflows(tenant_id);

-- Orchestrator State
CREATE INDEX IF NOT EXISTS idx_orchestrator_state_tenant ON orchestrator_state(tenant_id);

-- BMAD Workflows
CREATE INDEX IF NOT EXISTS idx_bmad_workflows_tenant ON bmad_workflows(tenant_id);

-- Voice Transcriptions
CREATE INDEX IF NOT EXISTS idx_voice_transcriptions_tenant ON voice_transcriptions(tenant_id);
CREATE INDEX IF NOT EXISTS idx_voice_transcriptions_tenant_created ON voice_transcriptions(tenant_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_voice_transcriptions_user ON voice_transcriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_voice_transcriptions_language ON voice_transcriptions(language);

-- Voice Conversations
CREATE INDEX IF NOT EXISTS idx_voice_conversations_tenant ON voice_conversations(tenant_id);
CREATE INDEX IF NOT EXISTS idx_voice_conversations_tenant_updated ON voice_conversations(tenant_id, updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_voice_conversations_user ON voice_conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_voice_conversations_status ON voice_conversations(status);

-- CRM Leads
CREATE INDEX IF NOT EXISTS idx_crm_leads_tenant ON crm_leads(tenant_id);
CREATE INDEX IF NOT EXISTS idx_crm_leads_tenant_created ON crm_leads(tenant_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_crm_leads_status ON crm_leads(status);
CREATE INDEX IF NOT EXISTS idx_crm_leads_email ON crm_leads(email);

-- CRM Deals
CREATE INDEX IF NOT EXISTS idx_crm_deals_tenant ON crm_deals(tenant_id);
CREATE INDEX IF NOT EXISTS idx_crm_deals_tenant_created ON crm_deals(tenant_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_crm_deals_status ON crm_deals(status);
CREATE INDEX IF NOT EXISTS idx_crm_deals_lead ON crm_deals(lead_id);

-- Billing Accounts
CREATE INDEX IF NOT EXISTS idx_billing_accounts_tenant ON billing_accounts(tenant_id);

-- Credit Transactions
CREATE INDEX IF NOT EXISTS idx_credit_transactions_tenant ON credit_transactions(tenant_id);
CREATE INDEX IF NOT EXISTS idx_credit_transactions_tenant_created ON credit_transactions(tenant_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_credit_transactions_billing_account ON credit_transactions(billing_account_id);

-- PME Analyses
CREATE INDEX IF NOT EXISTS idx_pme_analyses_tenant ON pme_analyses(tenant_id);
CREATE INDEX IF NOT EXISTS idx_pme_analyses_tenant_created ON pme_analyses(tenant_id, created_at DESC);

-- ============================================
-- UPDATE TRIGGERS
-- ============================================

-- Voice Conversations
CREATE TRIGGER update_voice_conversations_updated_at BEFORE UPDATE ON voice_conversations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- CRM Leads
CREATE TRIGGER update_crm_leads_updated_at BEFORE UPDATE ON crm_leads
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- CRM Deals
CREATE TRIGGER update_crm_deals_updated_at BEFORE UPDATE ON crm_deals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Billing Accounts
CREATE TRIGGER update_billing_accounts_updated_at BEFORE UPDATE ON billing_accounts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================

COMMENT ON COLUMN projects.tenant_id IS 'Tenant isolation - each project belongs to one tenant';
COMMENT ON COLUMN knowledge_base.tenant_id IS 'Tenant isolation - documents are isolated per tenant';
COMMENT ON TABLE voice_transcriptions IS 'Voice-to-text transcriptions with tenant isolation';
COMMENT ON TABLE voice_conversations IS 'Voice agent conversations with tenant isolation';
COMMENT ON TABLE crm_leads IS 'CRM leads management with tenant isolation';
COMMENT ON TABLE crm_deals IS 'CRM deals/opportunities with tenant isolation';
COMMENT ON TABLE billing_accounts IS 'Billing and credits per tenant';
COMMENT ON TABLE credit_transactions IS 'Credit transactions history per tenant';
COMMENT ON TABLE pme_analyses IS 'PME/Business analyses with tenant isolation';

-- ============================================
-- DATA MIGRATION: Assign existing data to default tenant
-- ============================================

-- Assign existing projects to default tenant (if no tenant_id)
UPDATE projects
SET tenant_id = '00000000-0000-0000-0000-000000000000'
WHERE tenant_id IS NULL;

-- Assign existing knowledge_base to default tenant
UPDATE knowledge_base
SET tenant_id = '00000000-0000-0000-0000-000000000000'
WHERE tenant_id IS NULL;

-- Assign existing workflows to default tenant
UPDATE bolt_workflows
SET tenant_id = '00000000-0000-0000-0000-000000000000'
WHERE tenant_id IS NULL;

UPDATE orchestrator_state
SET tenant_id = '00000000-0000-0000-0000-000000000000'
WHERE tenant_id IS NULL;

UPDATE bmad_workflows
SET tenant_id = '00000000-0000-0000-0000-000000000000'
WHERE tenant_id IS NULL;

-- ============================================
-- MAKE tenant_id NOT NULL (after migration)
-- ============================================

-- Projects
ALTER TABLE projects
    ALTER COLUMN tenant_id SET NOT NULL;

-- Knowledge Base
ALTER TABLE knowledge_base
    ALTER COLUMN tenant_id SET NOT NULL;

-- Bolt Workflows
ALTER TABLE bolt_workflows
    ALTER COLUMN tenant_id SET NOT NULL;

-- Orchestrator State
ALTER TABLE orchestrator_state
    ALTER COLUMN tenant_id SET NOT NULL;

-- BMAD Workflows
ALTER TABLE bmad_workflows
    ALTER COLUMN tenant_id SET NOT NULL;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Migration 007 completed: tenant_id added to all critical tables';
    RAISE NOTICE 'Indexes created for optimal query performance';
    RAISE NOTICE 'Existing data migrated to default tenant (00000000-0000-0000-0000-000000000000)';
END $$;
