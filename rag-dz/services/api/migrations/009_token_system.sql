-- Migration 009: Système de Tokens (Carburant) pour Monétisation
-- ================================================================
-- Permet aux clients Suisse/Algérie d'acheter des tokens (prepaid)
-- et de consommer selon usage réel des LLM (Groq, OpenAI, Claude)

BEGIN;

-- ============================================================
-- Table: tenant_token_balances
-- ============================================================
-- Solde de tokens par tenant (isolation stricte)

CREATE TABLE IF NOT EXISTS tenant_token_balances (
    tenant_id UUID PRIMARY KEY REFERENCES tenants(id) ON DELETE CASCADE,
    balance_tokens INTEGER NOT NULL DEFAULT 0 CHECK (balance_tokens >= 0),
    total_purchased INTEGER NOT NULL DEFAULT 0,
    total_consumed INTEGER NOT NULL DEFAULT 0,
    last_purchase_at TIMESTAMPTZ,
    last_usage_at TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_token_balances_tenant ON tenant_token_balances(tenant_id);

COMMENT ON TABLE tenant_token_balances IS 'Solde de tokens par tenant (1 token = ~1000 tokens LLM)';
COMMENT ON COLUMN tenant_token_balances.balance_tokens IS 'Solde actuel disponible';
COMMENT ON COLUMN tenant_token_balances.total_purchased IS 'Total acheté (historique)';
COMMENT ON COLUMN tenant_token_balances.total_consumed IS 'Total consommé (historique)';


-- ============================================================
-- Table: licence_codes
-- ============================================================
-- Codes de recharge (redeem codes) pour créditer tokens

CREATE TABLE IF NOT EXISTS licence_codes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) NOT NULL UNIQUE,
    amount_tokens INTEGER NOT NULL CHECK (amount_tokens > 0),

    -- Status et usage
    is_used BOOLEAN NOT NULL DEFAULT FALSE,
    used_by_tenant_id UUID REFERENCES tenants(id) ON DELETE SET NULL,
    used_at TIMESTAMPTZ,

    -- Contraintes commerciales
    expires_at TIMESTAMPTZ,
    max_uses INTEGER DEFAULT 1 CHECK (max_uses > 0),
    current_uses INTEGER DEFAULT 0 CHECK (current_uses >= 0),

    -- Métadonnées
    offer_type VARCHAR(50),  -- 'promotional', 'trial', 'prepaid', 'enterprise'
    source VARCHAR(100),      -- 'direct_sale', 'partner_xyz', 'promo_campaign'
    metadata JSONB DEFAULT '{}',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by VARCHAR(100)
);

CREATE INDEX idx_licence_codes_code ON licence_codes(code);
CREATE INDEX idx_licence_codes_used ON licence_codes(is_used);
CREATE INDEX idx_licence_codes_tenant ON licence_codes(used_by_tenant_id);

COMMENT ON TABLE licence_codes IS 'Codes de recharge pour créditer tokens (comme cartes iTunes)';
COMMENT ON COLUMN licence_codes.code IS 'Code unique (ex: IAFACTORY-2025-ABCD1234)';
COMMENT ON COLUMN licence_codes.amount_tokens IS 'Nombre de tokens à créditer';
COMMENT ON COLUMN licence_codes.max_uses IS 'Nombre max d''utilisations (1 = usage unique)';


-- ============================================================
-- Table: token_usage_logs
-- ============================================================
-- Logs détaillés de consommation tokens (audit trail)

CREATE TABLE IF NOT EXISTS token_usage_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,

    -- Context de l'appel
    request_id VARCHAR(100),
    route VARCHAR(200),
    method VARCHAR(10),

    -- LLM utilisé
    provider VARCHAR(50),  -- 'openai', 'groq', 'anthropic', 'google'
    model VARCHAR(100),    -- 'gpt-4o', 'llama-3.3-70b', 'claude-3.5-sonnet'

    -- Consommation tokens
    tokens_input INTEGER NOT NULL DEFAULT 0,
    tokens_output INTEGER NOT NULL DEFAULT 0,
    tokens_total INTEGER GENERATED ALWAYS AS (tokens_input + tokens_output) STORED,

    -- Coût et solde
    cost_tokens INTEGER NOT NULL,  -- Tokens déduits du solde
    balance_before INTEGER NOT NULL,
    balance_after INTEGER NOT NULL,

    -- Timing
    latency_ms INTEGER,

    -- Métadonnées
    user_agent TEXT,
    ip_address INET,
    metadata JSONB DEFAULT '{}',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_token_usage_tenant ON token_usage_logs(tenant_id);
CREATE INDEX idx_token_usage_created ON token_usage_logs(created_at DESC);
CREATE INDEX idx_token_usage_provider ON token_usage_logs(provider);
CREATE INDEX idx_token_usage_tenant_created ON token_usage_logs(tenant_id, created_at DESC);

COMMENT ON TABLE token_usage_logs IS 'Logs détaillés consommation tokens (audit trail)';
COMMENT ON COLUMN token_usage_logs.cost_tokens IS 'Tokens déduits (peut inclure majoration)';


-- ============================================================
-- Row-Level Security (RLS)
-- ============================================================

-- Enable RLS
ALTER TABLE tenant_token_balances ENABLE ROW LEVEL SECURITY;
ALTER TABLE licence_codes ENABLE ROW LEVEL SECURITY;
ALTER TABLE token_usage_logs ENABLE ROW LEVEL SECURITY;

-- Policies: tenant_token_balances
CREATE POLICY tenant_token_balances_select ON tenant_token_balances
    FOR SELECT USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY tenant_token_balances_update ON tenant_token_balances
    FOR UPDATE USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY tenant_token_balances_insert ON tenant_token_balances
    FOR INSERT WITH CHECK (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

-- Policies: licence_codes (lecture seule pour tenants)
CREATE POLICY licence_codes_select ON licence_codes
    FOR SELECT USING (
        used_by_tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY licence_codes_update ON licence_codes
    FOR UPDATE USING (is_superadmin());

-- Policies: token_usage_logs
CREATE POLICY token_usage_logs_select ON token_usage_logs
    FOR SELECT USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY token_usage_logs_insert ON token_usage_logs
    FOR INSERT WITH CHECK (
        tenant_id = get_current_tenant() OR is_superadmin()
    );


-- ============================================================
-- Fonctions Helpers
-- ============================================================

-- Fonction: Créditer tokens depuis licence code
CREATE OR REPLACE FUNCTION redeem_licence_code(
    p_code VARCHAR(50),
    p_tenant_id UUID
) RETURNS JSONB
LANGUAGE plpgsql
AS $$
DECLARE
    v_licence RECORD;
    v_balance RECORD;
    v_result JSONB;
BEGIN
    -- Vérifier code existe et non utilisé
    SELECT * INTO v_licence FROM licence_codes
    WHERE code = p_code
    FOR UPDATE;

    IF NOT FOUND THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', 'Code invalide ou inexistant'
        );
    END IF;

    IF v_licence.is_used THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', 'Code déjà utilisé',
            'used_by', v_licence.used_by_tenant_id,
            'used_at', v_licence.used_at
        );
    END IF;

    IF v_licence.expires_at IS NOT NULL AND v_licence.expires_at < NOW() THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', 'Code expiré',
            'expires_at', v_licence.expires_at
        );
    END IF;

    -- Marquer comme utilisé
    UPDATE licence_codes
    SET
        is_used = true,
        used_by_tenant_id = p_tenant_id,
        used_at = NOW(),
        current_uses = current_uses + 1
    WHERE id = v_licence.id;

    -- Créditer le solde
    INSERT INTO tenant_token_balances (tenant_id, balance_tokens, total_purchased, last_purchase_at)
    VALUES (p_tenant_id, v_licence.amount_tokens, v_licence.amount_tokens, NOW())
    ON CONFLICT (tenant_id) DO UPDATE SET
        balance_tokens = tenant_token_balances.balance_tokens + v_licence.amount_tokens,
        total_purchased = tenant_token_balances.total_purchased + v_licence.amount_tokens,
        last_purchase_at = NOW(),
        updated_at = NOW()
    RETURNING * INTO v_balance;

    -- Log l'événement
    INSERT INTO token_usage_logs (
        tenant_id, route, method, provider, model,
        tokens_input, tokens_output, cost_tokens,
        balance_before, balance_after,
        metadata
    ) VALUES (
        p_tenant_id, '/api/licences/redeem', 'POST', 'redeem', 'licence_code',
        0, 0, -v_licence.amount_tokens,  -- Négatif = crédit
        COALESCE(v_balance.balance_tokens - v_licence.amount_tokens, 0),
        v_balance.balance_tokens,
        jsonb_build_object('licence_code', p_code, 'offer_type', v_licence.offer_type)
    );

    RETURN jsonb_build_object(
        'success', true,
        'tokens_credited', v_licence.amount_tokens,
        'new_balance', v_balance.balance_tokens,
        'total_purchased', v_balance.total_purchased
    );
END;
$$;

COMMENT ON FUNCTION redeem_licence_code IS 'Échanger un code licence contre des tokens';


-- Fonction: Déduire tokens (atomique)
CREATE OR REPLACE FUNCTION deduct_tokens(
    p_tenant_id UUID,
    p_tokens INTEGER,
    p_provider VARCHAR(50),
    p_model VARCHAR(100),
    p_tokens_input INTEGER,
    p_tokens_output INTEGER,
    p_metadata JSONB DEFAULT '{}'
) RETURNS JSONB
LANGUAGE plpgsql
AS $$
DECLARE
    v_balance RECORD;
BEGIN
    -- Lock et récupérer solde
    SELECT * INTO v_balance FROM tenant_token_balances
    WHERE tenant_id = p_tenant_id
    FOR UPDATE;

    IF NOT FOUND THEN
        -- Créer solde à 0 si inexistant
        INSERT INTO tenant_token_balances (tenant_id, balance_tokens)
        VALUES (p_tenant_id, 0)
        RETURNING * INTO v_balance;
    END IF;

    -- Vérifier solde suffisant
    IF v_balance.balance_tokens < p_tokens THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', 'Solde insuffisant',
            'balance', v_balance.balance_tokens,
            'required', p_tokens
        );
    END IF;

    -- Déduire tokens
    UPDATE tenant_token_balances
    SET
        balance_tokens = balance_tokens - p_tokens,
        total_consumed = total_consumed + p_tokens,
        last_usage_at = NOW(),
        updated_at = NOW()
    WHERE tenant_id = p_tenant_id
    RETURNING * INTO v_balance;

    -- Log consommation
    INSERT INTO token_usage_logs (
        tenant_id, provider, model,
        tokens_input, tokens_output, cost_tokens,
        balance_before, balance_after,
        metadata
    ) VALUES (
        p_tenant_id, p_provider, p_model,
        p_tokens_input, p_tokens_output, p_tokens,
        v_balance.balance_tokens + p_tokens,
        v_balance.balance_tokens,
        p_metadata
    );

    RETURN jsonb_build_object(
        'success', true,
        'tokens_deducted', p_tokens,
        'new_balance', v_balance.balance_tokens
    );
END;
$$;

COMMENT ON FUNCTION deduct_tokens IS 'Déduire tokens du solde (atomique avec lock)';


-- ============================================================
-- Données de test (codes promotionnels)
-- ============================================================

INSERT INTO licence_codes (code, amount_tokens, offer_type, source, expires_at, created_by) VALUES
    ('IAFACTORY-WELCOME-1000', 1000, 'promotional', 'onboarding', NOW() + INTERVAL '1 year', 'system'),
    ('SUISSE-PRO-5000', 5000, 'prepaid', 'direct_sale', NOW() + INTERVAL '1 year', 'system'),
    ('ALGERIE-STARTER-500', 500, 'trial', 'partner_dz', NOW() + INTERVAL '6 months', 'system'),
    ('ENTERPRISE-UNLIMITED-50000', 50000, 'enterprise', 'direct_sale', NOW() + INTERVAL '1 year', 'system')
ON CONFLICT (code) DO NOTHING;

COMMIT;
