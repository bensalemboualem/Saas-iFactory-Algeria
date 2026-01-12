-- ============================================
-- Migration: Multi-LLM + Team Seats
-- Version: 1.0.0
-- Date: 2025-11-29
-- Description: Tables pour Multi-LLM Credit Manager et Team Seats
-- ============================================

-- ============================================
-- AI PROVIDERS
-- ============================================

CREATE TABLE IF NOT EXISTS ai_providers (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL, -- openai, anthropic, groq, google, mistral, openrouter
    base_url VARCHAR(255),
    api_key_env_var VARCHAR(100) NOT NULL, -- Nom de la variable d'env (jamais la clé!)
    is_active BOOLEAN DEFAULT TRUE,
    supports_streaming BOOLEAN DEFAULT TRUE,
    rate_limit_rpm INTEGER DEFAULT 60,
    rate_limit_tpm INTEGER DEFAULT 100000,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_ai_providers_type ON ai_providers(type);
CREATE INDEX IF NOT EXISTS idx_ai_providers_active ON ai_providers(is_active);

-- ============================================
-- AI MODELS
-- ============================================

CREATE TABLE IF NOT EXISTS ai_models (
    id VARCHAR(50) PRIMARY KEY,
    provider_id VARCHAR(50) REFERENCES ai_providers(id),
    code VARCHAR(100) NOT NULL UNIQUE, -- Ex: openai.gpt-4o, anthropic.claude-3-5-sonnet
    display_name VARCHAR(100) NOT NULL,
    type VARCHAR(50) DEFAULT 'chat', -- chat, completion, embedding, image_gen, vision, audio
    tier VARCHAR(50) DEFAULT 'standard', -- free, basic, standard, premium, ultra
    
    -- Coûts USD (pour calcul interne)
    cost_usd_input_per_1k DECIMAL(10, 6) DEFAULT 0.01,
    cost_usd_output_per_1k DECIMAL(10, 6) DEFAULT 0.03,
    
    -- Prix IAFactory (en crédits)
    cost_credits_per_1k INTEGER DEFAULT 1,
    
    -- Limites
    max_tokens INTEGER DEFAULT 4096,
    context_window INTEGER DEFAULT 128000,
    supports_vision BOOLEAN DEFAULT FALSE,
    supports_tools BOOLEAN DEFAULT TRUE,
    supports_streaming BOOLEAN DEFAULT TRUE,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    is_default BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_ai_models_provider ON ai_models(provider_id);
CREATE INDEX IF NOT EXISTS idx_ai_models_code ON ai_models(code);
CREATE INDEX IF NOT EXISTS idx_ai_models_tier ON ai_models(tier);
CREATE INDEX IF NOT EXISTS idx_ai_models_active ON ai_models(is_active);

-- ============================================
-- AI USAGE LOG
-- ============================================

CREATE TABLE IF NOT EXISTS ai_usage_log (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    model_id VARCHAR(50) REFERENCES ai_models(id),
    model_code VARCHAR(100) NOT NULL,
    
    -- Tokens
    tokens_input INTEGER NOT NULL,
    tokens_output INTEGER NOT NULL,
    tokens_total INTEGER NOT NULL,
    
    -- Coûts
    credits_consumed INTEGER NOT NULL,
    cost_usd_estimated DECIMAL(10, 6) NOT NULL,
    
    -- Request info
    request_type VARCHAR(50) DEFAULT 'chat',
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    latency_ms INTEGER DEFAULT 0,
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    ip_address VARCHAR(50),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_ai_usage_user ON ai_usage_log(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_usage_model ON ai_usage_log(model_code);
CREATE INDEX IF NOT EXISTS idx_ai_usage_created ON ai_usage_log(created_at);
CREATE INDEX IF NOT EXISTS idx_ai_usage_user_created ON ai_usage_log(user_id, created_at);

-- ============================================
-- TEAM SEATS
-- ============================================

CREATE TABLE IF NOT EXISTS team_seats (
    id VARCHAR(50) PRIMARY KEY,
    
    -- Utilisateur
    user_id VARCHAR(100) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    user_name VARCHAR(255),
    
    -- Provider & Plan
    provider VARCHAR(50) NOT NULL, -- openai_team, github_copilot, cursor_pro, notion_ai
    plan_name VARCHAR(100) NOT NULL,
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending', -- pending, payment_pending, processing, active, suspended, canceled, expired
    status_reason TEXT,
    
    -- Prix
    price_dzd_month DECIMAL(12, 2) NOT NULL,
    cost_usd_month DECIMAL(12, 2) NOT NULL,
    margin_percentage DECIMAL(5, 2) DEFAULT 20.0,
    
    -- Facturation
    billing_cycle_day INTEGER DEFAULT 1,
    next_billing_date DATE,
    last_payment_date DATE,
    
    -- Metadata
    notes TEXT,
    admin_notes TEXT,
    metadata JSONB DEFAULT '{}',
    
    -- External
    external_seat_id VARCHAR(100),
    external_email VARCHAR(255),
    
    -- Timestamps
    requested_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    activated_at TIMESTAMP WITH TIME ZONE,
    suspended_at TIMESTAMP WITH TIME ZONE,
    canceled_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_team_seats_user ON team_seats(user_id);
CREATE INDEX IF NOT EXISTS idx_team_seats_email ON team_seats(user_email);
CREATE INDEX IF NOT EXISTS idx_team_seats_provider ON team_seats(provider);
CREATE INDEX IF NOT EXISTS idx_team_seats_status ON team_seats(status);
CREATE INDEX IF NOT EXISTS idx_team_seats_billing ON team_seats(next_billing_date);

-- ============================================
-- SEAT REQUESTS
-- ============================================

CREATE TABLE IF NOT EXISTS seat_requests (
    id VARCHAR(50) PRIMARY KEY,
    
    -- Demandeur
    user_id VARCHAR(100) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    user_name VARCHAR(255),
    phone VARCHAR(50),
    
    -- Demande
    provider VARCHAR(50) NOT NULL,
    plan_requested VARCHAR(100) NOT NULL,
    priority VARCHAR(20) DEFAULT 'normal', -- low, normal, high, urgent
    
    -- Message
    message TEXT,
    reason TEXT,
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending', -- pending, approved, rejected, converted
    admin_response TEXT,
    
    -- Résultat
    seat_id VARCHAR(50) REFERENCES team_seats(id),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE
);

-- Index
CREATE INDEX IF NOT EXISTS idx_seat_requests_user ON seat_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_seat_requests_status ON seat_requests(status);
CREATE INDEX IF NOT EXISTS idx_seat_requests_created ON seat_requests(created_at);

-- ============================================
-- DEFAULT DATA: Providers
-- ============================================

INSERT INTO ai_providers (id, name, type, base_url, api_key_env_var, rate_limit_rpm, rate_limit_tpm)
VALUES 
    ('prov_openai', 'OpenAI', 'openai', 'https://api.openai.com/v1', 'OPENAI_API_KEY', 500, 200000),
    ('prov_anthropic', 'Anthropic', 'anthropic', 'https://api.anthropic.com/v1', 'ANTHROPIC_API_KEY', 50, 100000),
    ('prov_groq', 'Groq', 'groq', 'https://api.groq.com/openai/v1', 'GROQ_API_KEY', 30, 15000),
    ('prov_google', 'Google AI', 'google', 'https://generativelanguage.googleapis.com/v1beta', 'GOOGLE_API_KEY', 60, 100000),
    ('prov_mistral', 'Mistral AI', 'mistral', 'https://api.mistral.ai/v1', 'MISTRAL_API_KEY', 120, 100000),
    ('prov_openrouter', 'OpenRouter', 'openrouter', 'https://openrouter.ai/api/v1', 'OPENROUTER_API_KEY', 200, 500000)
ON CONFLICT (id) DO NOTHING;

-- ============================================
-- DEFAULT DATA: Models
-- ============================================

INSERT INTO ai_models (id, provider_id, code, display_name, tier, cost_usd_input_per_1k, cost_usd_output_per_1k, cost_credits_per_1k, max_tokens, context_window, supports_vision, is_default, description)
VALUES
    -- OpenAI
    ('model_gpt4o', 'prov_openai', 'openai.gpt-4o', 'GPT-4o', 'standard', 0.005, 0.015, 2, 16384, 128000, TRUE, TRUE, 'Modèle phare OpenAI, rapide et intelligent'),
    ('model_gpt4omini', 'prov_openai', 'openai.gpt-4o-mini', 'GPT-4o Mini', 'basic', 0.00015, 0.0006, 1, 16384, 128000, TRUE, FALSE, 'Économique et efficace pour tâches courantes'),
    ('model_o1', 'prov_openai', 'openai.o1-preview', 'O1 Preview', 'ultra', 0.015, 0.060, 5, 32768, 128000, FALSE, FALSE, 'Raisonnement avancé pour problèmes complexes'),
    
    -- Anthropic
    ('model_claude35sonnet', 'prov_anthropic', 'anthropic.claude-3-5-sonnet', 'Claude 3.5 Sonnet', 'standard', 0.003, 0.015, 2, 8192, 200000, TRUE, FALSE, 'Excellent équilibre performance/coût'),
    ('model_claude3haiku', 'prov_anthropic', 'anthropic.claude-3-haiku', 'Claude 3 Haiku', 'basic', 0.00025, 0.00125, 1, 4096, 200000, TRUE, FALSE, 'Ultra-rapide et économique'),
    ('model_claudeopus', 'prov_anthropic', 'anthropic.claude-3-opus', 'Claude 3 Opus', 'premium', 0.015, 0.075, 4, 4096, 200000, TRUE, FALSE, 'Le plus puissant de Claude'),
    
    -- Groq (Free tier)
    ('model_llama31_70b', 'prov_groq', 'groq.llama-3.1-70b', 'Llama 3.1 70B (Groq)', 'free', 0.0005, 0.0008, 1, 8000, 131072, FALSE, FALSE, 'Open-source, ultra-rapide via Groq'),
    ('model_llama31_8b', 'prov_groq', 'groq.llama-3.1-8b', 'Llama 3.1 8B (Groq)', 'free', 0.00005, 0.00008, 1, 8000, 131072, FALSE, FALSE, 'Petit, rapide, idéal pour tests'),
    ('model_mixtral', 'prov_groq', 'groq.mixtral-8x7b', 'Mixtral 8x7B (Groq)', 'free', 0.00027, 0.00027, 1, 32768, 32768, FALSE, FALSE, 'Mixture of Experts, bon rapport qualité/prix'),
    
    -- Google
    ('model_gemini15pro', 'prov_google', 'google.gemini-1.5-pro', 'Gemini 1.5 Pro', 'standard', 0.00125, 0.005, 2, 8192, 1000000, TRUE, FALSE, 'Contexte massif, multimodal'),
    ('model_gemini15flash', 'prov_google', 'google.gemini-1.5-flash', 'Gemini 1.5 Flash', 'basic', 0.000075, 0.0003, 1, 8192, 1000000, TRUE, FALSE, 'Ultra économique avec grand contexte'),
    
    -- Mistral
    ('model_mistral_large', 'prov_mistral', 'mistral.mistral-large', 'Mistral Large', 'standard', 0.002, 0.006, 2, 32768, 128000, FALSE, FALSE, 'Flagship Mistral, excellent en français'),
    ('model_mistral_small', 'prov_mistral', 'mistral.mistral-small', 'Mistral Small', 'basic', 0.0002, 0.0006, 1, 32768, 128000, FALSE, FALSE, 'Rapide et économique')
ON CONFLICT (id) DO NOTHING;

-- ============================================
-- FUNCTIONS
-- ============================================

-- Fonction pour mettre à jour updated_at automatiquement
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers
DROP TRIGGER IF EXISTS update_ai_providers_updated_at ON ai_providers;
CREATE TRIGGER update_ai_providers_updated_at
    BEFORE UPDATE ON ai_providers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_ai_models_updated_at ON ai_models;
CREATE TRIGGER update_ai_models_updated_at
    BEFORE UPDATE ON ai_models
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_team_seats_updated_at ON team_seats;
CREATE TRIGGER update_team_seats_updated_at
    BEFORE UPDATE ON team_seats
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- VIEWS
-- ============================================

-- Vue pour les statistiques d'usage par utilisateur
CREATE OR REPLACE VIEW v_user_llm_stats AS
SELECT 
    user_id,
    COUNT(*) as total_requests,
    SUM(tokens_total) as total_tokens,
    SUM(credits_consumed) as total_credits,
    SUM(cost_usd_estimated) as total_cost_usd,
    AVG(latency_ms) as avg_latency_ms,
    DATE_TRUNC('month', created_at) as month
FROM ai_usage_log
GROUP BY user_id, DATE_TRUNC('month', created_at);

-- Vue pour les seats actifs avec revenue
CREATE OR REPLACE VIEW v_active_seats_revenue AS
SELECT 
    provider,
    COUNT(*) as active_seats,
    SUM(price_dzd_month) as monthly_revenue_dzd,
    SUM(cost_usd_month) as monthly_cost_usd
FROM team_seats
WHERE status = 'active'
GROUP BY provider;

-- ============================================
-- DONE
-- ============================================

SELECT 'Multi-LLM + Team Seats migration completed successfully!' as status;
