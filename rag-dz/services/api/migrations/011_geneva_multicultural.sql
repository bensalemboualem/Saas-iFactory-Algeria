-- Migration 011: Geneva Multi-Cultural Intelligence
-- =================================================
-- Support 110+ nationalités de Genève
-- Nuances culturelles + Multi-language detection

BEGIN;

-- ============================================================
-- Table: cultural_nuances
-- ============================================================
-- Stocke les significations d'expressions selon nationalité/culture
-- Ex: "Yes" (Japonais) = hésitation polie vs "Yes" (Américain) = confirmation forte

CREATE TABLE IF NOT EXISTS cultural_nuances (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,

    -- Expression et contexte
    expression TEXT NOT NULL,
    language_code VARCHAR(10) NOT NULL,  -- 'en', 'fr', 'es', 'ja', 'ar', etc.

    -- Origine culturelle
    nationality VARCHAR(100),  -- 'japanese', 'spanish', 'algerian', 'swiss', 'american'
    cultural_region VARCHAR(100),  -- 'east_asia', 'latin_america', 'middle_east', 'western_europe'

    -- Signification contextuelle
    literal_meaning TEXT,  -- Sens littéral
    cultural_meaning TEXT,  -- Sens culturel réel
    politeness_level VARCHAR(50),  -- 'very_formal', 'formal', 'neutral', 'informal', 'casual'

    -- Exemples et usage
    example_context TEXT,  -- Exemple d'utilisation
    common_misinterpretation TEXT,  -- Erreur fréquente d'interprétation

    -- Intelligence contextuelle
    emotional_connotation VARCHAR(50),  -- 'positive', 'negative', 'neutral', 'ambiguous'
    business_appropriate BOOLEAN DEFAULT true,  -- Approprié en contexte professionnel

    -- Métadonnées
    source VARCHAR(100),  -- 'user_feedback', 'expert_input', 'ai_detected'
    confidence_score FLOAT CHECK (confidence_score >= 0 AND confidence_score <= 1),
    usage_frequency INTEGER DEFAULT 0,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Contrainte unicité par expression + nationalité
    UNIQUE(expression, nationality, language_code)
);

-- Index pour performance
CREATE INDEX idx_cultural_nuances_tenant ON cultural_nuances(tenant_id);
CREATE INDEX idx_cultural_nuances_user ON cultural_nuances(user_id);
CREATE INDEX idx_cultural_nuances_expression ON cultural_nuances(expression);
CREATE INDEX idx_cultural_nuances_nationality ON cultural_nuances(nationality);
CREATE INDEX idx_cultural_nuances_language ON cultural_nuances(language_code);
CREATE INDEX idx_cultural_nuances_region ON cultural_nuances(cultural_region);

COMMENT ON TABLE cultural_nuances IS 'Nuances culturelles des expressions selon nationalité (Genève 110+ cultures)';
COMMENT ON COLUMN cultural_nuances.cultural_meaning IS 'Signification réelle selon contexte culturel';
COMMENT ON COLUMN cultural_nuances.common_misinterpretation IS 'Erreur typique d''interprétation interculturelle';


-- ============================================================
-- Table: multi_language_segments
-- ============================================================
-- Détection multi-langues dans un même fichier audio
-- Ex: Réunion Genève avec Français + Anglais + Espagnol

CREATE TABLE IF NOT EXISTS multi_language_segments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    transcription_id UUID NOT NULL,  -- Lien vers voice_transcriptions

    -- Détection langue par segment
    segment_index INTEGER NOT NULL,  -- Numéro du segment
    start_time FLOAT NOT NULL,  -- Début en secondes
    end_time FLOAT NOT NULL,  -- Fin en secondes

    -- Langue détectée
    detected_language VARCHAR(10) NOT NULL,  -- 'fr', 'en', 'es', 'ja', etc.
    language_confidence FLOAT,  -- 0.0 à 1.0

    -- Accent/Variante
    accent_type VARCHAR(100),  -- 'french_swiss', 'french_algerian', 'english_spanish_accent'
    non_native_speaker BOOLEAN DEFAULT false,  -- Détection accent non-natif

    -- Texte du segment
    text_content TEXT NOT NULL,

    -- Métadonnées
    speaker_id VARCHAR(50),  -- ID du locuteur si détection speaker
    metadata JSONB DEFAULT '{}',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index
CREATE INDEX idx_multi_lang_tenant ON multi_language_segments(tenant_id);
CREATE INDEX idx_multi_lang_transcription ON multi_language_segments(transcription_id);
CREATE INDEX idx_multi_lang_language ON multi_language_segments(detected_language);
CREATE INDEX idx_multi_lang_accent ON multi_language_segments(accent_type) WHERE accent_type IS NOT NULL;
CREATE INDEX idx_multi_lang_non_native ON multi_language_segments(non_native_speaker) WHERE non_native_speaker = true;

COMMENT ON TABLE multi_language_segments IS 'Segments multi-langues dans une même transcription (Genève)';
COMMENT ON COLUMN multi_language_segments.non_native_speaker IS 'TRUE si accent non-natif détecté (ex: Anglais parlé par Espagnol)';


-- ============================================================
-- Table: user_linguistic_profile
-- ============================================================
-- Profil linguistique de chaque utilisateur (Geneva Mode)

CREATE TABLE IF NOT EXISTS user_linguistic_profile (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,

    -- Langues maîtrisées
    native_language VARCHAR(10),  -- 'fr', 'ar', 'en', etc.
    secondary_languages TEXT[],  -- ['en', 'es', 'de']

    -- Origine culturelle
    nationality VARCHAR(100),  -- 'swiss', 'algerian', 'spanish', 'japanese'
    cultural_background TEXT[],  -- ['north_african', 'mediterranean']

    -- Préférences Geneva Mode
    geneva_mode_enabled BOOLEAN DEFAULT false,
    accent_sensitivity_level INTEGER CHECK (accent_sensitivity_level >= 1 AND accent_sensitivity_level <= 5) DEFAULT 3,
    -- 1 = Low (standard), 5 = Very High (maximum accuracy for non-native accents)

    -- Contexte professionnel
    professional_context VARCHAR(100),  -- 'medical', 'legal', 'finance', 'diplomatic'
    typical_meeting_languages TEXT[],  -- Langues fréquentes en réunion

    -- Intelligence adaptative
    preferred_transcription_model VARCHAR(50),  -- 'large-v3', 'distil-large-v3'
    auto_detect_language BOOLEAN DEFAULT true,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index
CREATE INDEX idx_user_profile_tenant ON user_linguistic_profile(tenant_id);
CREATE INDEX idx_user_profile_user ON user_linguistic_profile(user_id);
CREATE INDEX idx_user_profile_nationality ON user_linguistic_profile(nationality);
CREATE INDEX idx_user_profile_geneva_mode ON user_linguistic_profile(geneva_mode_enabled) WHERE geneva_mode_enabled = true;

COMMENT ON TABLE user_linguistic_profile IS 'Profil linguistique utilisateur (Geneva Multi-Cultural Mode)';
COMMENT ON COLUMN user_linguistic_profile.accent_sensitivity_level IS 'Niveau sensibilité accent: 1=Standard, 5=Max accuracy accents non-natifs';


-- ============================================================
-- Row-Level Security (RLS)
-- ============================================================

-- Enable RLS
ALTER TABLE cultural_nuances ENABLE ROW LEVEL SECURITY;
ALTER TABLE multi_language_segments ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_linguistic_profile ENABLE ROW LEVEL SECURITY;

-- Policies: cultural_nuances
CREATE POLICY cultural_nuances_select ON cultural_nuances
    FOR SELECT USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY cultural_nuances_insert ON cultural_nuances
    FOR INSERT WITH CHECK (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY cultural_nuances_update ON cultural_nuances
    FOR UPDATE USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY cultural_nuances_delete ON cultural_nuances
    FOR DELETE USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

-- Policies: multi_language_segments
CREATE POLICY multi_lang_select ON multi_language_segments
    FOR SELECT USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY multi_lang_insert ON multi_language_segments
    FOR INSERT WITH CHECK (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

-- Policies: user_linguistic_profile
CREATE POLICY user_profile_select ON user_linguistic_profile
    FOR SELECT USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY user_profile_insert ON user_linguistic_profile
    FOR INSERT WITH CHECK (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY user_profile_update ON user_linguistic_profile
    FOR UPDATE USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );


-- ============================================================
-- Fonctions Helpers
-- ============================================================

-- Fonction: Ajouter nuance culturelle
CREATE OR REPLACE FUNCTION add_cultural_nuance(
    p_tenant_id UUID,
    p_user_id INTEGER,
    p_expression TEXT,
    p_language_code VARCHAR(10),
    p_nationality VARCHAR(100),
    p_cultural_meaning TEXT,
    p_literal_meaning TEXT DEFAULT NULL
) RETURNS UUID
LANGUAGE plpgsql
AS $$
DECLARE
    v_nuance_id UUID;
BEGIN
    INSERT INTO cultural_nuances (
        tenant_id, user_id, expression, language_code,
        nationality, cultural_meaning, literal_meaning,
        source, confidence_score
    ) VALUES (
        p_tenant_id, p_user_id, p_expression, p_language_code,
        p_nationality, p_cultural_meaning, p_literal_meaning,
        'user_feedback', 0.8
    )
    ON CONFLICT (expression, nationality, language_code) DO UPDATE SET
        cultural_meaning = EXCLUDED.cultural_meaning,
        usage_frequency = cultural_nuances.usage_frequency + 1,
        updated_at = NOW()
    RETURNING id INTO v_nuance_id;

    RETURN v_nuance_id;
END;
$$;

COMMENT ON FUNCTION add_cultural_nuance IS 'Ajoute une nuance culturelle avec upsert (usage_frequency++)';


-- Fonction: Récupérer nuances par nationalité
CREATE OR REPLACE FUNCTION get_cultural_nuances_by_nationality(
    p_tenant_id UUID,
    p_nationality VARCHAR(100),
    p_language_code VARCHAR(10) DEFAULT NULL
) RETURNS TABLE (
    expression TEXT,
    cultural_meaning TEXT,
    literal_meaning TEXT,
    politeness_level VARCHAR(50),
    emotional_connotation VARCHAR(50),
    usage_frequency INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        cn.expression,
        cn.cultural_meaning,
        cn.literal_meaning,
        cn.politeness_level,
        cn.emotional_connotation,
        cn.usage_frequency
    FROM cultural_nuances cn
    WHERE cn.tenant_id = p_tenant_id
      AND cn.nationality = p_nationality
      AND (p_language_code IS NULL OR cn.language_code = p_language_code)
    ORDER BY cn.usage_frequency DESC, cn.expression ASC;
END;
$$;

COMMENT ON FUNCTION get_cultural_nuances_by_nationality IS 'Récupère toutes les nuances culturelles d''une nationalité';


-- ============================================================
-- Data Seed: Exemples Cultural Nuances (Geneva)
-- ============================================================

-- Exemples Japonais (politesse indirecte)
INSERT INTO cultural_nuances (
    tenant_id, expression, language_code, nationality,
    literal_meaning, cultural_meaning, politeness_level,
    common_misinterpretation, emotional_connotation,
    business_appropriate, source, confidence_score
) VALUES
(
    '814c132a-1cdd-4db6-bc1f-21abd21ec37d'::uuid,
    'Yes, but it might be difficult',
    'en',
    'japanese',
    'Oui, mais ce sera difficile',
    'Non poli - Je ne peux pas le faire',
    'very_formal',
    'Interprété comme "Oui" alors que signifie "Non"',
    'negative',
    true,
    'expert_input',
    0.95
),
(
    '814c132a-1cdd-4db6-bc1f-21abd21ec37d'::uuid,
    'I will consider it',
    'en',
    'japanese',
    'Je vais y réfléchir',
    'Refus poli - Pas intéressé',
    'formal',
    'Interprété comme indécision alors que signifie "Non merci"',
    'negative',
    true,
    'expert_input',
    0.9
);

-- Exemples Espagnol (emphase culturelle)
INSERT INTO cultural_nuances (
    tenant_id, expression, language_code, nationality,
    literal_meaning, cultural_meaning, politeness_level,
    common_misinterpretation, emotional_connotation, business_appropriate, source, confidence_score
) VALUES
(
    '814c132a-1cdd-4db6-bc1f-21abd21ec37d'::uuid,
    'Ahora mismo',
    'es',
    'spanish',
    'Maintenant',
    'Bientôt (pas forcément immédiat)',
    'informal',
    'Emphase culturelle',
    'neutral',
    true,
    'expert_input',
    0.85
),
(
    '814c132a-1cdd-4db6-bc1f-21abd21ec37d'::uuid,
    'Mañana',
    'es',
    'spanish',
    'Demain',
    'Dans un futur proche (pas forcément demain)',
    'informal',
    'Temps culturellement flexible',
    'neutral',
    false,
    'expert_input',
    0.8
);

-- Exemples Algérien/Arabe (expressions culturelles)
INSERT INTO cultural_nuances (
    tenant_id, expression, language_code, nationality,
    literal_meaning, cultural_meaning, politeness_level,
    common_misinterpretation, emotional_connotation, business_appropriate, source, confidence_score
) VALUES
(
    '814c132a-1cdd-4db6-bc1f-21abd21ec37d'::uuid,
    'Inchallah',
    'ar',
    'algerian',
    'Si Dieu le veut',
    'Peut-être / Espoir mais incertitude',
    'formal',
    'Expression de foi et humilité',
    'positive',
    true,
    'expert_input',
    0.95
),
(
    '814c132a-1cdd-4db6-bc1f-21abd21ec37d'::uuid,
    'Baraka Allahou fik',
    'ar',
    'algerian',
    'Que Dieu te bénisse',
    'Merci profondément',
    'very_formal',
    'Gratitude spirituelle forte',
    'positive',
    true,
    'expert_input',
    0.95
);

-- Exemples Suisse (précision et formalité)
INSERT INTO cultural_nuances (
    tenant_id, expression, language_code, nationality,
    literal_meaning, cultural_meaning, politeness_level,
    common_misinterpretation, emotional_connotation, business_appropriate, source, confidence_score
) VALUES
(
    '814c132a-1cdd-4db6-bc1f-21abd21ec37d'::uuid,
    'On pourrait peut-être',
    'fr',
    'swiss',
    'On pourrait peut-être',
    'Proposition ferme (politesse suisse)',
    'formal',
    'Politesse atténuée',
    'neutral',
    true,
    'expert_input',
    0.85
);

COMMIT;
