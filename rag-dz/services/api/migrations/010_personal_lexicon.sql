-- Migration 010: Personal Lexicon & Emotional Intelligence
-- ==========================================================
-- Stocke le vocabulaire personnalisé de chaque professionnel
-- (médecins, avocats, experts-comptables)

BEGIN;

-- ============================================================
-- Table: user_preferences_lexicon
-- ============================================================
-- Dictionnaire privé de chaque utilisateur
-- Extrait automatiquement après chaque transcription

CREATE TABLE IF NOT EXISTS user_preferences_lexicon (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,

    -- Mot/Expression professionnelle
    term VARCHAR(200) NOT NULL,
    term_type VARCHAR(50),  -- 'abbreviation', 'medical_term', 'legal_jargon', 'accounting_term'

    -- Contexte et usage
    professional_domain VARCHAR(100),  -- 'medical', 'legal', 'accounting', 'engineering'
    frequency_count INTEGER NOT NULL DEFAULT 1,
    last_used_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    first_detected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Enrichissement sémantique
    definition TEXT,
    synonyms TEXT[],  -- Liste de synonymes
    context_example TEXT,  -- Exemple d'utilisation

    -- Intelligence émotionnelle & culturelle
    emotional_tag VARCHAR(50),  -- 'stress_indicator', 'calm', 'heritage_value', 'technical'
    cultural_context VARCHAR(50),  -- 'algerian_heritage', 'swiss_formal', 'universal'

    -- Métadonnées
    source_transcription_id UUID,  -- Lien vers la transcription d'origine
    confidence_score FLOAT CHECK (confidence_score >= 0 AND confidence_score <= 1),
    metadata JSONB DEFAULT '{}',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Contrainte unicité par utilisateur
    UNIQUE(user_id, term)
);

-- Index pour performance
CREATE INDEX idx_lexicon_tenant ON user_preferences_lexicon(tenant_id);
CREATE INDEX idx_lexicon_user ON user_preferences_lexicon(user_id);
CREATE INDEX idx_lexicon_domain ON user_preferences_lexicon(professional_domain);
CREATE INDEX idx_lexicon_term ON user_preferences_lexicon(term);
CREATE INDEX idx_lexicon_frequency ON user_preferences_lexicon(frequency_count DESC);
CREATE INDEX idx_lexicon_emotional ON user_preferences_lexicon(emotional_tag) WHERE emotional_tag IS NOT NULL;

COMMENT ON TABLE user_preferences_lexicon IS 'Lexique personnalisé de chaque professionnel (IA Double)';
COMMENT ON COLUMN user_preferences_lexicon.term IS 'Mot ou expression professionnelle';
COMMENT ON COLUMN user_preferences_lexicon.frequency_count IS 'Nombre d''utilisations détectées';
COMMENT ON COLUMN user_preferences_lexicon.emotional_tag IS 'Tag émotionnel: stress, calm, heritage, etc.';
COMMENT ON COLUMN user_preferences_lexicon.cultural_context IS 'Contexte culturel: algerian_heritage, swiss_formal, universal';


-- ============================================================
-- Table: emotion_analysis_logs
-- ============================================================
-- Log des analyses émotionnelles par transcription

CREATE TABLE IF NOT EXISTS emotion_analysis_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    transcription_id UUID,  -- Lien vers voice_transcriptions

    -- Analyse émotionnelle
    detected_emotion VARCHAR(50),  -- 'calm', 'stressed', 'neutral', 'confident', 'uncertain'
    stress_level INTEGER CHECK (stress_level >= 0 AND stress_level <= 10),  -- 0 = calme, 10 = très stressé
    cognitive_load INTEGER CHECK (cognitive_load >= 0 AND cognitive_load <= 10),  -- Charge cognitive

    -- Contexte culturel (Algérie)
    heritage_detected BOOLEAN DEFAULT FALSE,
    heritage_type VARCHAR(100),  -- 'proverb', 'historical_reference', 'cultural_wisdom', 'local_tradition'
    heritage_content TEXT,  -- Citation exacte du contenu patrimonial

    -- Recommandation IA
    recommended_summary_style VARCHAR(50),  -- 'calm_direct', 'empathetic', 'technical', 'heritage_enriched'
    ai_confidence FLOAT CHECK (ai_confidence >= 0 AND ai_confidence <= 1),

    -- Métadonnées
    analysis_model VARCHAR(100),  -- Modèle LLM utilisé
    processing_time_ms INTEGER,
    metadata JSONB DEFAULT '{}',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index
CREATE INDEX idx_emotion_tenant ON emotion_analysis_logs(tenant_id);
CREATE INDEX idx_emotion_user ON emotion_analysis_logs(user_id);
CREATE INDEX idx_emotion_transcription ON emotion_analysis_logs(transcription_id);
CREATE INDEX idx_emotion_stress ON emotion_analysis_logs(stress_level DESC);
CREATE INDEX idx_emotion_heritage ON emotion_analysis_logs(heritage_detected) WHERE heritage_detected = true;

COMMENT ON TABLE emotion_analysis_logs IS 'Logs d''analyse émotionnelle des transcriptions';
COMMENT ON COLUMN emotion_analysis_logs.stress_level IS 'Niveau de stress détecté (0-10)';
COMMENT ON COLUMN emotion_analysis_logs.heritage_detected IS 'TRUE si contenu patrimonial algérien détecté';


-- ============================================================
-- Table: tokens_saved_tracking
-- ============================================================
-- Track le ROI: Tokens économisés en utilisant Faster-Whisper
-- au lieu des APIs Cloud (OpenAI Whisper, Google, etc.)

CREATE TABLE IF NOT EXISTS tokens_saved_tracking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    transcription_id UUID,

    -- Audio transcrit
    audio_duration_seconds FLOAT NOT NULL,
    audio_format VARCHAR(20),

    -- Comparaison coûts
    local_cost_tokens INTEGER DEFAULT 0,  -- Coût local (généralement 0)
    cloud_equivalent_cost_tokens INTEGER NOT NULL,  -- Coût si utilisé OpenAI Whisper API
    tokens_saved INTEGER GENERATED ALWAYS AS (cloud_equivalent_cost_tokens - local_cost_tokens) STORED,

    -- Modèle utilisé
    local_model VARCHAR(50),  -- 'faster-whisper-large-v3'
    cloud_provider_compared VARCHAR(50) DEFAULT 'openai_whisper',  -- 'openai_whisper', 'google_speech'

    -- Métriques qualité
    transcription_quality_score FLOAT,  -- 0.0 à 1.0
    processing_time_ms INTEGER,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index
CREATE INDEX idx_tokens_saved_tenant ON tokens_saved_tracking(tenant_id);
CREATE INDEX idx_tokens_saved_user ON tokens_saved_tracking(user_id);
CREATE INDEX idx_tokens_saved_created ON tokens_saved_tracking(created_at DESC);

COMMENT ON TABLE tokens_saved_tracking IS 'ROI: Tokens économisés vs Cloud APIs';
COMMENT ON COLUMN tokens_saved_tracking.tokens_saved IS 'Tokens économisés (calculé automatiquement)';
COMMENT ON COLUMN tokens_saved_tracking.cloud_equivalent_cost_tokens IS 'Coût équivalent si utilisé API Cloud';


-- ============================================================
-- Row-Level Security (RLS)
-- ============================================================

-- Enable RLS
ALTER TABLE user_preferences_lexicon ENABLE ROW LEVEL SECURITY;
ALTER TABLE emotion_analysis_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE tokens_saved_tracking ENABLE ROW LEVEL SECURITY;

-- Policies: user_preferences_lexicon
CREATE POLICY user_lexicon_select ON user_preferences_lexicon
    FOR SELECT USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY user_lexicon_insert ON user_preferences_lexicon
    FOR INSERT WITH CHECK (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY user_lexicon_update ON user_preferences_lexicon
    FOR UPDATE USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY user_lexicon_delete ON user_preferences_lexicon
    FOR DELETE USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

-- Policies: emotion_analysis_logs
CREATE POLICY emotion_logs_select ON emotion_analysis_logs
    FOR SELECT USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY emotion_logs_insert ON emotion_analysis_logs
    FOR INSERT WITH CHECK (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

-- Policies: tokens_saved_tracking
CREATE POLICY tokens_saved_select ON tokens_saved_tracking
    FOR SELECT USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY tokens_saved_insert ON tokens_saved_tracking
    FOR INSERT WITH CHECK (
        tenant_id = get_current_tenant() OR is_superadmin()
    );


-- ============================================================
-- Fonctions Helpers
-- ============================================================

-- Fonction: Incrémenter fréquence d'un terme
CREATE OR REPLACE FUNCTION increment_term_frequency(
    p_user_id INTEGER,
    p_tenant_id UUID,
    p_term VARCHAR(200)
) RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO user_preferences_lexicon (tenant_id, user_id, term)
    VALUES (p_tenant_id, p_user_id, p_term)
    ON CONFLICT (user_id, term) DO UPDATE SET
        frequency_count = user_preferences_lexicon.frequency_count + 1,
        last_used_at = NOW(),
        updated_at = NOW();
END;
$$;

COMMENT ON FUNCTION increment_term_frequency IS 'Incrémente la fréquence d''un terme dans le lexique utilisateur';


-- Fonction: Calculer ROI total tokens saved
CREATE OR REPLACE FUNCTION get_total_tokens_saved(
    p_tenant_id UUID,
    p_start_date TIMESTAMPTZ DEFAULT NULL,
    p_end_date TIMESTAMPTZ DEFAULT NOW()
) RETURNS TABLE (
    total_saved INTEGER,
    total_transcriptions BIGINT,
    total_hours_transcribed FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        COALESCE(SUM(tokens_saved), 0)::INTEGER AS total_saved,
        COUNT(*)::BIGINT AS total_transcriptions,
        COALESCE(SUM(audio_duration_seconds) / 3600.0, 0.0)::FLOAT AS total_hours_transcribed
    FROM tokens_saved_tracking
    WHERE tenant_id = p_tenant_id
      AND (p_start_date IS NULL OR created_at >= p_start_date)
      AND created_at <= p_end_date;
END;
$$;

COMMENT ON FUNCTION get_total_tokens_saved IS 'Calcule le ROI total: tokens économisés par période';

COMMIT;
