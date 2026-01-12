-- ═══════════════════════════════════════════════════════════════════
-- SYSTÈME DE CRÉDITS IA FACTORY ALGERIA
-- À exécuter après init.sql
-- ═══════════════════════════════════════════════════════════════════

-- 1. Table des crédits utilisateur
CREATE TABLE IF NOT EXISTS user_credits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    balance INTEGER DEFAULT 100,  -- Current balance (renamed from total - used)
    total_purchased INTEGER DEFAULT 0,  -- Total credits ever purchased
    total_consumed INTEGER DEFAULT 0,  -- Total credits ever consumed (was used_credits)
    total_credits INTEGER DEFAULT 0,  -- Legacy: monthly allocation
    used_credits INTEGER DEFAULT 0,  -- Legacy: for tenant-based tracking
    plan VARCHAR(20) DEFAULT 'free',
    credits_reset_at TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '1 month'),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_user_credits UNIQUE (user_id),
    CONSTRAINT unique_tenant_credits UNIQUE (tenant_id)
);

-- 2. Table des transactions de crédits
CREATE TABLE IF NOT EXISTS credit_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    amount INTEGER NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,  -- purchase, consumption, refund, bonus
    type VARCHAR(50),  -- Legacy alias for transaction_type
    service_type VARCHAR(50),  -- rag_query, image_gen, video_gen, etc.
    service VARCHAR(100),  -- Legacy: detailed service name
    description TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Table de pricing des services
CREATE TABLE IF NOT EXISTS service_pricing (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_name VARCHAR(100) UNIQUE NOT NULL,
    service_type VARCHAR(50) NOT NULL,
    credits_per_unit INTEGER NOT NULL,
    is_unlimited BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Plans d'abonnement
CREATE TABLE IF NOT EXISTS subscription_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) UNIQUE NOT NULL,
    credits_monthly INTEGER NOT NULL,
    price_chf DECIMAL(10,2),
    price_dzd DECIMAL(10,2),
    features JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE
);

-- ═══════════════════════════════════════════════════════════════════
-- INDEX POUR PERFORMANCE
-- ═══════════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_user_credits_tenant ON user_credits(tenant_id);
CREATE INDEX IF NOT EXISTS idx_user_credits_user ON user_credits(user_id);
CREATE INDEX IF NOT EXISTS idx_credit_transactions_tenant ON credit_transactions(tenant_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_credit_transactions_user ON credit_transactions(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_credit_transactions_type ON credit_transactions(transaction_type);
CREATE INDEX IF NOT EXISTS idx_credit_transactions_type_legacy ON credit_transactions(type);
CREATE INDEX IF NOT EXISTS idx_service_pricing_type ON service_pricing(service_type);

-- ═══════════════════════════════════════════════════════════════════
-- DONNÉES INITIALES : Plans d'abonnement
-- ═══════════════════════════════════════════════════════════════════

INSERT INTO subscription_plans (name, credits_monthly, price_chf, price_dzd, features) VALUES
('free', 1000, 0, 0, '{"llm_limited": true, "image": false, "video": false, "support": "community"}'),
('starter', 10000, 9.90, 1500, '{"llm_limited": false, "image": true, "video": false, "support": "email"}'),
('pro', 30000, 24.90, 4000, '{"llm_limited": false, "image": true, "video": true, "support": "priority"}'),
('enterprise', 100000, 99.90, 15000, '{"llm_limited": false, "image": true, "video": true, "support": "dedicated", "priority": true}')
ON CONFLICT (name) DO UPDATE SET
    credits_monthly = EXCLUDED.credits_monthly,
    price_chf = EXCLUDED.price_chf,
    price_dzd = EXCLUDED.price_dzd,
    features = EXCLUDED.features;

-- ═══════════════════════════════════════════════════════════════════
-- DONNÉES INITIALES : Pricing des services
-- ═══════════════════════════════════════════════════════════════════

INSERT INTO service_pricing (service_name, service_type, credits_per_unit, is_unlimited) VALUES
-- LLMs GRATUITS (illimités) - Tier FREE
('groq-llama', 'llm', 0, true),
('gemini-flash', 'llm', 0, true),

-- LLMs PREMIUM - Tier PAYANT
('claude-sonnet', 'llm', 5, false),
('claude-opus', 'llm', 15, false),
('gpt-4o', 'llm', 5, false),
('gpt-4-turbo', 'llm', 8, false),
('gpt-4o-mini', 'llm', 2, false),
('grok-2', 'llm', 6, false),
('mistral-large', 'llm', 4, false),
('mistral-medium', 'llm', 2, false),
('deepseek', 'llm', 3, false),
('deepseek-reasoner', 'llm', 5, false),
('qwen', 'llm', 3, false),
('qwen-coder', 'llm', 4, false),
('perplexity', 'llm', 5, false),
('kimi', 'llm', 3, false),

-- IMAGES
('flux-image', 'image', 40, false),
('flux-pro', 'image', 60, false),
('dalle-3', 'image', 50, false),
('stable-diffusion', 'image', 30, false),
('midjourney', 'image', 80, false),

-- VIDÉOS
('luma-video', 'video', 500, false),
('runway-video', 'video', 800, false),
('minimax-video', 'video', 400, false),
('kling-video', 'video', 600, false),

-- VOICE (TTS/STT)
('tts-standard', 'voice', 10, false),
('tts-premium', 'voice', 20, false),
('stt-whisper', 'voice', 15, false),
('stt-realtime', 'voice', 25, false),

-- AGENTS & RAG
('agent-task', 'agent', 100, false),
('agent-research', 'agent', 200, false),
('rag-query', 'rag', 5, false),
('rag-ingest', 'rag', 20, false),

-- OCR & DOCUMENTS
('ocr-page', 'document', 10, false),
('pdf-extract', 'document', 15, false)

ON CONFLICT (service_name) DO UPDATE SET
    credits_per_unit = EXCLUDED.credits_per_unit,
    is_unlimited = EXCLUDED.is_unlimited,
    service_type = EXCLUDED.service_type;

-- ═══════════════════════════════════════════════════════════════════
-- FONCTIONS UTILITAIRES
-- ═══════════════════════════════════════════════════════════════════

-- Fonction pour reset mensuel des crédits
CREATE OR REPLACE FUNCTION reset_monthly_credits()
RETURNS void AS $$
BEGIN
    UPDATE user_credits
    SET
        used_credits = 0,
        credits_reset_at = NOW() + INTERVAL '1 month',
        updated_at = NOW()
    WHERE credits_reset_at <= NOW();

    -- Log les resets
    INSERT INTO credit_transactions (tenant_id, amount, type, description)
    SELECT tenant_id, total_credits, 'reset', 'Reset mensuel automatique'
    FROM user_credits
    WHERE credits_reset_at <= NOW();
END;
$$ LANGUAGE plpgsql;

-- Fonction pour obtenir le solde restant
CREATE OR REPLACE FUNCTION get_remaining_credits(p_tenant_id UUID)
RETURNS INTEGER AS $$
DECLARE
    remaining INTEGER;
BEGIN
    SELECT (total_credits - used_credits) INTO remaining
    FROM user_credits
    WHERE tenant_id = p_tenant_id;

    RETURN COALESCE(remaining, 0);
END;
$$ LANGUAGE plpgsql;

-- ═══════════════════════════════════════════════════════════════════
-- TRIGGERS
-- ═══════════════════════════════════════════════════════════════════

-- Trigger pour updated_at automatique
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_user_credits_updated_at ON user_credits;
CREATE TRIGGER trigger_user_credits_updated_at
    BEFORE UPDATE ON user_credits
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ═══════════════════════════════════════════════════════════════════
-- VUES UTILES
-- ═══════════════════════════════════════════════════════════════════

-- Vue du solde avec détails
CREATE OR REPLACE VIEW v_credit_balances AS
SELECT
    uc.tenant_id,
    t.name as tenant_name,
    uc.total_credits,
    uc.used_credits,
    (uc.total_credits - uc.used_credits) as remaining_credits,
    uc.plan,
    uc.credits_reset_at,
    sp.credits_monthly as plan_credits,
    sp.price_dzd as plan_price_dzd
FROM user_credits uc
JOIN tenants t ON uc.tenant_id = t.id
JOIN subscription_plans sp ON uc.plan = sp.name;

-- Vue usage par service
CREATE OR REPLACE VIEW v_usage_by_service AS
SELECT
    tenant_id,
    service,
    COUNT(*) as usage_count,
    SUM(ABS(amount)) as total_credits_used,
    DATE_TRUNC('day', created_at) as usage_date
FROM credit_transactions
WHERE type = 'usage'
GROUP BY tenant_id, service, DATE_TRUNC('day', created_at)
ORDER BY usage_date DESC;
