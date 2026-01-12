-- Migration 013: Token Packs & Purchase System
-- ================================================================
-- Packs de tokens avec prix DZD/CHF pour achat via Chargily/Stripe
-- Integration avec le systeme de tokens existant (009_token_system.sql)

BEGIN;

-- ============================================================
-- Table: token_packs
-- ============================================================
-- Catalogue des packs de tokens disponibles a l'achat

CREATE TABLE IF NOT EXISTS token_packs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Identifiant unique du pack
    slug VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT,

    -- Tokens inclus
    tokens INTEGER NOT NULL CHECK (tokens > 0),
    bonus_tokens INTEGER NOT NULL DEFAULT 0,  -- Tokens bonus (promo)

    -- Prix
    price_dzd INTEGER NOT NULL CHECK (price_dzd > 0),  -- Prix en DZD
    price_chf DECIMAL(10, 2),  -- Prix en CHF (optionnel)
    price_usd DECIMAL(10, 2),  -- Prix en USD (optionnel)

    -- Metadata
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_featured BOOLEAN NOT NULL DEFAULT false,  -- Mise en avant
    sort_order INTEGER NOT NULL DEFAULT 0,

    -- Restrictions
    max_purchases_per_user INTEGER,  -- Limite par user (null = illimite)
    valid_from TIMESTAMPTZ,
    valid_until TIMESTAMPTZ,

    -- Tracking
    total_sold INTEGER NOT NULL DEFAULT 0,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_token_packs_active ON token_packs(is_active);
CREATE INDEX idx_token_packs_slug ON token_packs(slug);

COMMENT ON TABLE token_packs IS 'Catalogue des packs de tokens disponibles a l achat';
COMMENT ON COLUMN token_packs.tokens IS 'Nombre de tokens dans le pack';
COMMENT ON COLUMN token_packs.bonus_tokens IS 'Tokens bonus offerts (promo)';
COMMENT ON COLUMN token_packs.price_dzd IS 'Prix en DZD (Chargily)';
COMMENT ON COLUMN token_packs.price_chf IS 'Prix en CHF (Stripe)';


-- ============================================================
-- Table: token_purchases
-- ============================================================
-- Historique des achats de tokens

CREATE TABLE IF NOT EXISTS token_purchases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Acheteur
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,

    -- Pack achete
    pack_id UUID REFERENCES token_packs(id) ON DELETE SET NULL,
    pack_slug VARCHAR(50) NOT NULL,  -- Copie pour historique

    -- Montant
    tokens_amount INTEGER NOT NULL,
    bonus_amount INTEGER NOT NULL DEFAULT 0,
    total_tokens INTEGER GENERATED ALWAYS AS (tokens_amount + bonus_amount) STORED,

    -- Prix paye
    amount_dzd INTEGER,
    amount_chf DECIMAL(10, 2),
    currency VARCHAR(3) NOT NULL DEFAULT 'dzd',

    -- Payment provider
    payment_provider VARCHAR(20) NOT NULL,  -- 'chargily', 'stripe', 'licence_code'
    payment_status VARCHAR(20) NOT NULL DEFAULT 'pending',  -- 'pending', 'paid', 'failed', 'refunded'

    -- Chargily specifique
    chargily_checkout_id VARCHAR(100),
    chargily_payment_id VARCHAR(100),

    -- Stripe specifique
    stripe_session_id VARCHAR(100),
    stripe_payment_intent VARCHAR(100),

    -- Metadata
    metadata JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,

    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    paid_at TIMESTAMPTZ,
    refunded_at TIMESTAMPTZ
);

CREATE INDEX idx_token_purchases_tenant ON token_purchases(tenant_id);
CREATE INDEX idx_token_purchases_status ON token_purchases(payment_status);
CREATE INDEX idx_token_purchases_chargily ON token_purchases(chargily_checkout_id);
CREATE INDEX idx_token_purchases_stripe ON token_purchases(stripe_session_id);
CREATE INDEX idx_token_purchases_created ON token_purchases(created_at DESC);

COMMENT ON TABLE token_purchases IS 'Historique des achats de tokens';
COMMENT ON COLUMN token_purchases.payment_status IS 'pending=en attente, paid=paye, failed=echec, refunded=rembourse';


-- ============================================================
-- Table: provider_rates
-- ============================================================
-- Multiplicateurs de cout par provider LLM

CREATE TABLE IF NOT EXISTS provider_rates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    provider VARCHAR(50) NOT NULL,
    model_pattern VARCHAR(100),  -- Pattern regex pour matcher les modeles (null = tous)

    -- Multiplicateur: tokens_factures = tokens_reels * rate
    rate DECIMAL(5, 2) NOT NULL DEFAULT 1.0 CHECK (rate > 0),

    -- Description
    description TEXT,

    is_active BOOLEAN NOT NULL DEFAULT true,
    priority INTEGER NOT NULL DEFAULT 0,  -- Plus haut = plus prioritaire

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE(provider, model_pattern)
);

CREATE INDEX idx_provider_rates_provider ON provider_rates(provider);
CREATE INDEX idx_provider_rates_active ON provider_rates(is_active);

COMMENT ON TABLE provider_rates IS 'Multiplicateurs de cout par provider/model LLM';
COMMENT ON COLUMN provider_rates.rate IS 'Multiplicateur: 1.0 = 1:1, 2.0 = double, 0.5 = moitie';
COMMENT ON COLUMN provider_rates.model_pattern IS 'Pattern regex pour matcher les modeles (ex: gpt-4.*)';


-- ============================================================
-- Row-Level Security (RLS)
-- ============================================================

ALTER TABLE token_packs ENABLE ROW LEVEL SECURITY;
ALTER TABLE token_purchases ENABLE ROW LEVEL SECURITY;
ALTER TABLE provider_rates ENABLE ROW LEVEL SECURITY;

-- token_packs: Lecture publique, ecriture admin
CREATE POLICY token_packs_select ON token_packs
    FOR SELECT USING (is_active = true OR is_superadmin());

CREATE POLICY token_packs_admin ON token_packs
    FOR ALL USING (is_superadmin());

-- token_purchases: Lecture par tenant, ecriture systeme
CREATE POLICY token_purchases_select ON token_purchases
    FOR SELECT USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY token_purchases_insert ON token_purchases
    FOR INSERT WITH CHECK (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY token_purchases_update ON token_purchases
    FOR UPDATE USING (is_superadmin());

-- provider_rates: Lecture publique, ecriture admin
CREATE POLICY provider_rates_select ON provider_rates
    FOR SELECT USING (true);

CREATE POLICY provider_rates_admin ON provider_rates
    FOR ALL USING (is_superadmin());


-- ============================================================
-- Fonction: get_provider_rate
-- ============================================================
-- Recupere le rate applicable pour un provider/model

CREATE OR REPLACE FUNCTION get_provider_rate(
    p_provider VARCHAR(50),
    p_model VARCHAR(100)
) RETURNS DECIMAL(5, 2)
LANGUAGE plpgsql
AS $$
DECLARE
    v_rate DECIMAL(5, 2);
BEGIN
    -- Chercher rate specifique au modele
    SELECT rate INTO v_rate
    FROM provider_rates
    WHERE provider = p_provider
      AND is_active = true
      AND (model_pattern IS NULL OR p_model ~ model_pattern)
    ORDER BY
        CASE WHEN model_pattern IS NOT NULL THEN 0 ELSE 1 END,
        priority DESC
    LIMIT 1;

    -- Default 1.0 si pas trouve
    RETURN COALESCE(v_rate, 1.0);
END;
$$;

COMMENT ON FUNCTION get_provider_rate IS 'Retourne le multiplicateur de cout pour un provider/model';


-- ============================================================
-- Fonction: process_token_purchase
-- ============================================================
-- Traite un achat de tokens apres paiement confirme

CREATE OR REPLACE FUNCTION process_token_purchase(
    p_purchase_id UUID
) RETURNS JSONB
LANGUAGE plpgsql
AS $$
DECLARE
    v_purchase RECORD;
    v_balance RECORD;
BEGIN
    -- Lock et recuperer l'achat
    SELECT * INTO v_purchase
    FROM token_purchases
    WHERE id = p_purchase_id
    FOR UPDATE;

    IF NOT FOUND THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', 'Achat non trouve'
        );
    END IF;

    -- Verifier pas deja traite
    IF v_purchase.payment_status = 'paid' THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', 'Achat deja traite',
            'paid_at', v_purchase.paid_at
        );
    END IF;

    -- Marquer comme paye
    UPDATE token_purchases
    SET
        payment_status = 'paid',
        paid_at = NOW()
    WHERE id = p_purchase_id;

    -- Crediter les tokens
    INSERT INTO tenant_token_balances (tenant_id, balance_tokens, total_purchased, last_purchase_at)
    VALUES (v_purchase.tenant_id, v_purchase.total_tokens, v_purchase.total_tokens, NOW())
    ON CONFLICT (tenant_id) DO UPDATE SET
        balance_tokens = tenant_token_balances.balance_tokens + v_purchase.total_tokens,
        total_purchased = tenant_token_balances.total_purchased + v_purchase.total_tokens,
        last_purchase_at = NOW(),
        updated_at = NOW()
    RETURNING * INTO v_balance;

    -- Incrementer compteur du pack
    UPDATE token_packs
    SET total_sold = total_sold + 1
    WHERE id = v_purchase.pack_id;

    -- Log l'evenement
    INSERT INTO token_usage_logs (
        tenant_id, route, method, provider, model,
        tokens_input, tokens_output, cost_tokens,
        balance_before, balance_after,
        metadata
    ) VALUES (
        v_purchase.tenant_id, '/api/tokens/purchase', 'POST', 'purchase', v_purchase.pack_slug,
        0, 0, -v_purchase.total_tokens,  -- Negatif = credit
        v_balance.balance_tokens - v_purchase.total_tokens,
        v_balance.balance_tokens,
        jsonb_build_object(
            'purchase_id', p_purchase_id,
            'pack_slug', v_purchase.pack_slug,
            'amount_dzd', v_purchase.amount_dzd,
            'payment_provider', v_purchase.payment_provider
        )
    );

    RETURN jsonb_build_object(
        'success', true,
        'tokens_credited', v_purchase.total_tokens,
        'new_balance', v_balance.balance_tokens,
        'purchase_id', p_purchase_id
    );
END;
$$;

COMMENT ON FUNCTION process_token_purchase IS 'Traite un achat apres paiement confirme (credite tokens)';


-- ============================================================
-- Donnees initiales: Packs de tokens
-- ============================================================

INSERT INTO token_packs (slug, name, description, tokens, bonus_tokens, price_dzd, price_chf, is_featured, sort_order) VALUES
    ('starter', 'Pack Starter', 'Ideal pour decouvrir IA Factory', 100000, 0, 5000, 5.00, false, 1),
    ('pro', 'Pack Pro', 'Pour usage professionnel regulier', 500000, 50000, 20000, 20.00, true, 2),
    ('business', 'Pack Business', 'Pour equipes et PME', 2000000, 300000, 70000, 70.00, false, 3),
    ('dev', 'Pack Developpeur', 'Pour integration API et Claude Code', 5000000, 1000000, 150000, 150.00, false, 4),
    ('enterprise', 'Pack Enterprise', 'Volume illimite, support dedie', 20000000, 5000000, 500000, 500.00, false, 5)
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    tokens = EXCLUDED.tokens,
    bonus_tokens = EXCLUDED.bonus_tokens,
    price_dzd = EXCLUDED.price_dzd,
    price_chf = EXCLUDED.price_chf,
    is_featured = EXCLUDED.is_featured,
    sort_order = EXCLUDED.sort_order,
    updated_at = NOW();


-- ============================================================
-- Donnees initiales: Provider rates
-- ============================================================

INSERT INTO provider_rates (provider, model_pattern, rate, description, priority) VALUES
    -- Groq (economique)
    ('groq', NULL, 1.0, 'Groq - Tarif standard 1:1', 0),
    ('groq', 'llama-3.3.*', 0.8, 'Groq Llama 3.3 - Reduction 20%', 10),

    -- DeepSeek (economique)
    ('deepseek', NULL, 1.0, 'DeepSeek - Tarif standard 1:1', 0),
    ('deepseek', 'deepseek-chat', 0.9, 'DeepSeek Chat - Reduction 10%', 10),

    -- OpenRouter
    ('openrouter', NULL, 2.0, 'OpenRouter - Tarif standard x2', 0),
    ('openrouter', 'gpt-4.*', 5.0, 'OpenRouter GPT-4 - Premium x5', 10),
    ('openrouter', 'claude-3.*', 4.0, 'OpenRouter Claude 3 - Premium x4', 10),
    ('openrouter', 'llama.*', 1.5, 'OpenRouter Llama - x1.5', 10),

    -- OpenAI direct
    ('openai', NULL, 3.0, 'OpenAI - Tarif standard x3', 0),
    ('openai', 'gpt-4o-mini', 1.5, 'GPT-4o Mini - Economique x1.5', 10),
    ('openai', 'gpt-4o', 4.0, 'GPT-4o - Premium x4', 10),
    ('openai', 'gpt-4-turbo.*', 5.0, 'GPT-4 Turbo - Premium x5', 10),

    -- Anthropic direct
    ('anthropic', NULL, 3.5, 'Anthropic - Tarif standard x3.5', 0),
    ('anthropic', 'claude-3-haiku.*', 1.5, 'Claude Haiku - Economique x1.5', 10),
    ('anthropic', 'claude-3-sonnet.*', 3.0, 'Claude Sonnet - x3', 10),
    ('anthropic', 'claude-3-opus.*', 6.0, 'Claude Opus - Premium x6', 10),
    ('anthropic', 'claude-3-5-sonnet.*', 3.5, 'Claude 3.5 Sonnet - x3.5', 10),

    -- Google
    ('google', NULL, 2.5, 'Google - Tarif standard x2.5', 0),
    ('google', 'gemini-1.5-flash.*', 1.2, 'Gemini Flash - Economique x1.2', 10),
    ('google', 'gemini-1.5-pro.*', 3.0, 'Gemini Pro - x3', 10),

    -- Mistral
    ('mistral', NULL, 2.0, 'Mistral - Tarif standard x2', 0),
    ('mistral', 'mistral-small.*', 1.0, 'Mistral Small - Economique x1', 10),
    ('mistral', 'mistral-large.*', 3.0, 'Mistral Large - x3', 10)

ON CONFLICT (provider, model_pattern) DO UPDATE SET
    rate = EXCLUDED.rate,
    description = EXCLUDED.description,
    priority = EXCLUDED.priority,
    updated_at = NOW();


COMMIT;
