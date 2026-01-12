-- Migration 005: Billing & Tiers System
-- Créé le: 2024-12-23
-- Description: Tables pour abonnements, tiers et tracking usage LLM

-- Table user_tiers: Abonnements utilisateurs
CREATE TABLE IF NOT EXISTS user_tiers (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    tier VARCHAR(20) NOT NULL DEFAULT 'free',
    subscribed_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    auto_renew BOOLEAN DEFAULT TRUE,
    chargily_checkout_id VARCHAR(255),
    chargily_payment_id VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT valid_tier CHECK (tier IN ('free', 'student', 'pro', 'enterprise'))
);

-- Index pour queries fréquentes
CREATE INDEX IF NOT EXISTS idx_user_tiers_tier ON user_tiers(tier);
CREATE INDEX IF NOT EXISTS idx_user_tiers_expires_at ON user_tiers(expires_at);
CREATE INDEX IF NOT EXISTS idx_user_tiers_chargily_checkout ON user_tiers(chargily_checkout_id);

-- Table llm_usage_logs: Tracking usage LLM pour billing et analytics
CREATE TABLE IF NOT EXISTS llm_usage_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,
    model VARCHAR(100),
    tokens_input INTEGER NOT NULL DEFAULT 0,
    tokens_output INTEGER NOT NULL DEFAULT 0,
    cost_usd DECIMAL(10, 6) NOT NULL DEFAULT 0,
    latency_ms INTEGER,
    endpoint VARCHAR(100),
    error_flag BOOLEAN DEFAULT FALSE,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT positive_tokens CHECK (tokens_input >= 0 AND tokens_output >= 0),
    CONSTRAINT positive_cost CHECK (cost_usd >= 0)
);

-- Index pour queries fréquentes (analytics)
CREATE INDEX IF NOT EXISTS idx_llm_usage_user_date ON llm_usage_logs(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_llm_usage_created_at ON llm_usage_logs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_llm_usage_provider ON llm_usage_logs(provider);
CREATE INDEX IF NOT EXISTS idx_llm_usage_cost ON llm_usage_logs(cost_usd DESC);

-- Index composite pour dashboard admin (optimisation queries)
CREATE INDEX IF NOT EXISTS idx_llm_usage_date_provider ON llm_usage_logs(DATE(created_at), provider);

-- Table payment_transactions: Historique paiements Chargily
CREATE TABLE IF NOT EXISTS payment_transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tier VARCHAR(20) NOT NULL,
    amount_dzd INTEGER NOT NULL,
    amount_usd DECIMAL(10, 2),
    currency VARCHAR(3) DEFAULT 'dzd',
    status VARCHAR(20) NOT NULL,
    chargily_checkout_id VARCHAR(255),
    chargily_payment_id VARCHAR(255),
    payment_method VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    paid_at TIMESTAMPTZ,

    CONSTRAINT valid_status CHECK (status IN ('pending', 'paid', 'failed', 'expired', 'refunded'))
);

CREATE INDEX IF NOT EXISTS idx_payment_transactions_user ON payment_transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_payment_transactions_status ON payment_transactions(status);
CREATE INDEX IF NOT EXISTS idx_payment_transactions_checkout ON payment_transactions(chargily_checkout_id);

-- Trigger pour update updated_at automatiquement
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_tiers_updated_at
    BEFORE UPDATE ON user_tiers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Vue matérialisée pour analytics (performance)
CREATE MATERIALIZED VIEW IF NOT EXISTS daily_usage_stats AS
SELECT
    DATE(created_at) as date,
    provider,
    COUNT(*) as requests_count,
    SUM(tokens_input + tokens_output) as total_tokens,
    SUM(cost_usd) as total_cost,
    AVG(latency_ms) as avg_latency_ms,
    SUM(CASE WHEN error_flag THEN 1 ELSE 0 END)::FLOAT / COUNT(*)::FLOAT * 100 as error_rate
FROM llm_usage_logs
GROUP BY DATE(created_at), provider
ORDER BY date DESC, total_cost DESC;

CREATE UNIQUE INDEX IF NOT EXISTS idx_daily_usage_stats_date_provider ON daily_usage_stats(date, provider);

-- Fonction pour refresh automatique de la vue matérialisée (à appeler via cron ou trigger)
CREATE OR REPLACE FUNCTION refresh_daily_usage_stats()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY daily_usage_stats;
END;
$$ LANGUAGE plpgsql;

-- Commentaires pour documentation
COMMENT ON TABLE user_tiers IS 'Abonnements et tiers des utilisateurs (FREE, STUDENT, PRO, ENTERPRISE)';
COMMENT ON TABLE llm_usage_logs IS 'Logs détaillés de chaque appel LLM pour billing et analytics';
COMMENT ON TABLE payment_transactions IS 'Historique complet des transactions Chargily';
COMMENT ON MATERIALIZED VIEW daily_usage_stats IS 'Stats agrégées par jour et par provider (performance dashboard)';

-- Données de test (UNIQUEMENT pour environnement DEV)
-- Décommenter si besoin pour tests locaux
/*
INSERT INTO user_tiers (user_id, tier, subscribed_at, expires_at)
VALUES
    (1, 'free', NULL, NULL),
    (2, 'student', NOW(), NOW() + INTERVAL '30 days'),
    (3, 'pro', NOW() - INTERVAL '15 days', NOW() + INTERVAL '15 days')
ON CONFLICT (user_id) DO NOTHING;
*/
