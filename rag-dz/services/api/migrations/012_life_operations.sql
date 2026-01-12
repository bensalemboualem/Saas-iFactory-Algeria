-- Migration 012: Life Operations Module
-- ======================================
-- Universal Life Assistant: Reminders, Travel, Workspace

BEGIN;

-- ============================================================
-- Table: user_reminders
-- ============================================================
-- Gestion rappels intelligents (Médicaments, RDV, Tâches)

CREATE TABLE IF NOT EXISTS user_reminders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,

    -- Type de rappel
    reminder_type VARCHAR(50) NOT NULL,  -- 'medication', 'appointment', 'task', 'birthday', 'custom'

    -- Contenu
    title VARCHAR(200) NOT NULL,
    description TEXT,

    -- Planification
    scheduled_time TIMESTAMPTZ NOT NULL,
    recurrence_rule VARCHAR(100),  -- 'daily', 'weekly', 'monthly', 'yearly', 'custom_cron'
    timezone VARCHAR(50) DEFAULT 'Europe/Zurich',

    -- Notifications
    notification_channels TEXT[],  -- ['voice', 'sms', 'email', 'push']
    advance_notice_minutes INTEGER DEFAULT 15,  -- Rappel X minutes avant

    -- Contexte (Médicament spécifique)
    medication_name VARCHAR(200),
    medication_dosage VARCHAR(100),
    medication_timing VARCHAR(50),  -- 'before_breakfast', 'after_lunch', 'before_sleep'

    -- Contexte (Rendez-vous)
    appointment_location TEXT,
    appointment_attendees TEXT[],
    calendar_event_id VARCHAR(200),  -- Lien Google Calendar

    -- Statut
    is_active BOOLEAN DEFAULT true,
    is_completed BOOLEAN DEFAULT false,
    completed_at TIMESTAMPTZ,
    snoozed_until TIMESTAMPTZ,

    -- Intelligence contextuelle
    context_triggers TEXT[],  -- ['after_breakfast', 'before_leaving_home', 'when_arriving_office']
    cultural_context VARCHAR(100),  -- 'ramadan_fasting', 'chinese_new_year', etc.

    -- Historique
    last_triggered_at TIMESTAMPTZ,
    trigger_count INTEGER DEFAULT 0,

    -- Métadonnées
    metadata JSONB DEFAULT '{}',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index
CREATE INDEX idx_reminders_tenant ON user_reminders(tenant_id);
CREATE INDEX idx_reminders_user ON user_reminders(user_id);
CREATE INDEX idx_reminders_type ON user_reminders(reminder_type);
CREATE INDEX idx_reminders_scheduled ON user_reminders(scheduled_time) WHERE is_active = true;
CREATE INDEX idx_reminders_active ON user_reminders(is_active) WHERE is_active = true;
CREATE INDEX idx_reminders_medication ON user_reminders(medication_name) WHERE reminder_type = 'medication';

COMMENT ON TABLE user_reminders IS 'Rappels intelligents (médicaments, RDV, tâches) - Geneva Life Assistant';
COMMENT ON COLUMN user_reminders.context_triggers IS 'Déclencheurs contextuels (ex: après petit-déjeuner)';
COMMENT ON COLUMN user_reminders.cultural_context IS 'Contexte culturel pour adaptations (Ramadan, fêtes, etc.)';


-- ============================================================
-- Table: travel_cache
-- ============================================================
-- Cache calculs de trajets (Google Maps/TPG)
-- Optimisation: évite appels API répétés pour mêmes trajets

CREATE TABLE IF NOT EXISTS travel_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,

    -- Trajet
    origin_address TEXT NOT NULL,
    destination_address TEXT NOT NULL,
    travel_mode VARCHAR(20) NOT NULL,  -- 'car', 'transit', 'walking', 'bicycling'

    -- Résultats calculés
    distance_meters INTEGER,
    duration_seconds INTEGER,
    duration_in_traffic_seconds INTEGER,  -- Avec trafic (si 'car')

    -- Détails itinéraire
    route_summary TEXT,  -- "Via Avenue de France, Rue du Rhône"
    steps JSONB,  -- Étapes détaillées
    polyline TEXT,  -- Encoded polyline Google Maps

    -- Transport en commun (si 'transit')
    transit_lines TEXT[],  -- ['Tram 15', 'Bus 8']
    departure_time TIMESTAMPTZ,
    arrival_time TIMESTAMPTZ,
    transit_fare_currency VARCHAR(10),
    transit_fare_amount NUMERIC(10, 2),

    -- Métadonnées
    provider VARCHAR(50) DEFAULT 'google_maps',  -- 'google_maps', 'tpg_geneva', 'here_maps'
    api_response JSONB,  -- Réponse API complète

    -- Cache invalidation
    cached_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ,  -- TTL: 15 min pour trafic, 24h pour transit
    is_stale BOOLEAN DEFAULT false,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index
CREATE INDEX idx_travel_cache_tenant ON travel_cache(tenant_id);
CREATE INDEX idx_travel_cache_route ON travel_cache(origin_address, destination_address, travel_mode);
CREATE INDEX idx_travel_cache_expires ON travel_cache(expires_at);
CREATE INDEX idx_travel_cache_fresh ON travel_cache(is_stale) WHERE is_stale = false;

COMMENT ON TABLE travel_cache IS 'Cache calculs trajets (Google Maps/TPG Geneva)';
COMMENT ON COLUMN travel_cache.expires_at IS 'TTL: 15min (trafic car), 24h (transit)';


-- ============================================================
-- Table: email_summaries
-- ============================================================
-- Résumés emails générés par LLM
-- Workspace Connector (Gmail integration)

CREATE TABLE IF NOT EXISTS email_summaries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,

    -- Email source
    email_id VARCHAR(200) NOT NULL,  -- Gmail Message ID
    email_thread_id VARCHAR(200),

    -- Métadonnées email
    sender_email VARCHAR(255),
    sender_name VARCHAR(255),
    subject TEXT,
    received_at TIMESTAMPTZ,

    -- Classification IA
    priority_level VARCHAR(20),  -- 'urgent', 'high', 'normal', 'low'
    category VARCHAR(50),  -- 'work', 'personal', 'newsletter', 'spam'
    requires_action BOOLEAN DEFAULT false,

    -- Résumé LLM
    summary_text TEXT,  -- Résumé concis (2-3 phrases)
    key_points TEXT[],  -- Points clés bullet points
    action_items TEXT[],  -- Actions à faire
    deadline_detected TIMESTAMPTZ,  -- Deadline détectée par LLM

    -- Intelligence contextuelle
    sentiment VARCHAR(20),  -- 'positive', 'negative', 'neutral', 'urgent'
    language_detected VARCHAR(10),  -- 'fr', 'en', 'de', etc.
    contains_attachments BOOLEAN DEFAULT false,
    attachment_types TEXT[],  -- ['pdf', 'docx', 'image']

    -- LLM utilisé
    llm_model VARCHAR(100),  -- 'grok-2', 'gemini-2.0-flash', 'gpt-4o'
    tokens_used INTEGER,
    processing_time_ms INTEGER,

    -- Métadonnées
    metadata JSONB DEFAULT '{}',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index
CREATE INDEX idx_email_summaries_tenant ON email_summaries(tenant_id);
CREATE INDEX idx_email_summaries_user ON email_summaries(user_id);
CREATE INDEX idx_email_summaries_email_id ON email_summaries(email_id);
CREATE INDEX idx_email_summaries_priority ON email_summaries(priority_level);
CREATE INDEX idx_email_summaries_action ON email_summaries(requires_action) WHERE requires_action = true;
CREATE INDEX idx_email_summaries_deadline ON email_summaries(deadline_detected) WHERE deadline_detected IS NOT NULL;
CREATE INDEX idx_email_summaries_received ON email_summaries(received_at DESC);

COMMENT ON TABLE email_summaries IS 'Résumés emails générés par LLM (Workspace Connector)';
COMMENT ON COLUMN email_summaries.action_items IS 'Actions détectées par LLM (signer, répondre, appeler)';


-- ============================================================
-- Table: mobile_device_pairings
-- ============================================================
-- Appairage sécurisé smartphones via QR Code

CREATE TABLE IF NOT EXISTS mobile_device_pairings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,

    -- Token d'appairage
    pairing_token VARCHAR(64) UNIQUE NOT NULL,  -- Token sécurisé temporaire
    qr_code_url TEXT,  -- URL du QR Code généré

    -- Informations device
    device_name VARCHAR(200),  -- 'iPhone 15 Pro', 'Samsung Galaxy S24'
    device_os VARCHAR(50),  -- 'iOS 17.2', 'Android 14'
    device_fingerprint VARCHAR(200),  -- Empreinte unique device

    -- Statut appairage
    pairing_status VARCHAR(20) DEFAULT 'pending',  -- 'pending', 'active', 'revoked'
    paired_at TIMESTAMPTZ,
    last_seen_at TIMESTAMPTZ,

    -- Sécurité
    ip_address INET,
    user_agent TEXT,
    expires_at TIMESTAMPTZ NOT NULL,  -- Token expire après 5 minutes
    revoked_at TIMESTAMPTZ,
    revoked_reason TEXT,

    -- Permissions
    allowed_features TEXT[] DEFAULT ARRAY['transcribe', 'reminders', 'briefing'],

    -- Métadonnées
    metadata JSONB DEFAULT '{}',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index
CREATE INDEX idx_mobile_pairing_tenant ON mobile_device_pairings(tenant_id);
CREATE INDEX idx_mobile_pairing_user ON mobile_device_pairings(user_id);
CREATE INDEX idx_mobile_pairing_token ON mobile_device_pairings(pairing_token);
CREATE INDEX idx_mobile_pairing_status ON mobile_device_pairings(pairing_status);
CREATE INDEX idx_mobile_pairing_expires ON mobile_device_pairings(expires_at);

COMMENT ON TABLE mobile_device_pairings IS 'Appairage sécurisé smartphones via QR Code (5 min TTL)';
COMMENT ON COLUMN mobile_device_pairings.pairing_token IS 'Token temporaire sécurisé (expire 5 min)';


-- ============================================================
-- Table: daily_briefings
-- ============================================================
-- Historique des briefings matinaux générés

CREATE TABLE IF NOT EXISTS daily_briefings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,

    -- Date du briefing
    briefing_date DATE NOT NULL,
    generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Contenu briefing
    briefing_text TEXT NOT NULL,  -- Texte complet du briefing
    briefing_audio_url TEXT,  -- URL audio TTS si généré

    -- Composants utilisés
    weather_summary TEXT,
    top_emails_count INTEGER DEFAULT 0,
    meetings_count INTEGER DEFAULT 0,
    reminders_count INTEGER DEFAULT 0,
    news_items_count INTEGER DEFAULT 0,

    -- Intelligence
    user_greeting VARCHAR(100),  -- Salutation personnalisée
    cultural_adaptation TEXT,  -- Adaptations culturelles appliquées

    -- Métadonnées
    generation_time_ms INTEGER,
    llm_model VARCHAR(100),
    tokens_used INTEGER,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Contrainte: 1 briefing par jour par utilisateur
    UNIQUE(user_id, briefing_date)
);

-- Index
CREATE INDEX idx_daily_briefings_tenant ON daily_briefings(tenant_id);
CREATE INDEX idx_daily_briefings_user ON daily_briefings(user_id);
CREATE INDEX idx_daily_briefings_date ON daily_briefings(briefing_date DESC);

COMMENT ON TABLE daily_briefings IS 'Historique briefings matinaux (Weather + Emails + Meetings + Reminders)';


-- ============================================================
-- Row-Level Security (RLS)
-- ============================================================

-- Enable RLS
ALTER TABLE user_reminders ENABLE ROW LEVEL SECURITY;
ALTER TABLE travel_cache ENABLE ROW LEVEL SECURITY;
ALTER TABLE email_summaries ENABLE ROW LEVEL SECURITY;
ALTER TABLE mobile_device_pairings ENABLE ROW LEVEL SECURITY;
ALTER TABLE daily_briefings ENABLE ROW LEVEL SECURITY;

-- Policies: user_reminders
CREATE POLICY user_reminders_select ON user_reminders
    FOR SELECT USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY user_reminders_insert ON user_reminders
    FOR INSERT WITH CHECK (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY user_reminders_update ON user_reminders
    FOR UPDATE USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

CREATE POLICY user_reminders_delete ON user_reminders
    FOR DELETE USING (
        tenant_id = get_current_tenant() OR is_superadmin()
    );

-- Policies: travel_cache (similaire)
CREATE POLICY travel_cache_select ON travel_cache FOR SELECT USING (tenant_id = get_current_tenant() OR is_superadmin());
CREATE POLICY travel_cache_insert ON travel_cache FOR INSERT WITH CHECK (tenant_id = get_current_tenant() OR is_superadmin());

-- Policies: email_summaries (similaire)
CREATE POLICY email_summaries_select ON email_summaries FOR SELECT USING (tenant_id = get_current_tenant() OR is_superadmin());
CREATE POLICY email_summaries_insert ON email_summaries FOR INSERT WITH CHECK (tenant_id = get_current_tenant() OR is_superadmin());

-- Policies: mobile_device_pairings (similaire)
CREATE POLICY mobile_pairing_select ON mobile_device_pairings FOR SELECT USING (tenant_id = get_current_tenant() OR is_superadmin());
CREATE POLICY mobile_pairing_insert ON mobile_device_pairings FOR INSERT WITH CHECK (tenant_id = get_current_tenant() OR is_superadmin());
CREATE POLICY mobile_pairing_update ON mobile_device_pairings FOR UPDATE USING (tenant_id = get_current_tenant() OR is_superadmin());

-- Policies: daily_briefings (similaire)
CREATE POLICY daily_briefings_select ON daily_briefings FOR SELECT USING (tenant_id = get_current_tenant() OR is_superadmin());
CREATE POLICY daily_briefings_insert ON daily_briefings FOR INSERT WITH CHECK (tenant_id = get_current_tenant() OR is_superadmin());


-- ============================================================
-- Fonctions Helpers
-- ============================================================

-- Fonction: Récupérer rappels actifs du jour
CREATE OR REPLACE FUNCTION get_active_reminders_today(
    p_tenant_id UUID,
    p_user_id INTEGER
) RETURNS TABLE (
    id UUID,
    reminder_type VARCHAR(50),
    title VARCHAR(200),
    scheduled_time TIMESTAMPTZ,
    medication_name VARCHAR(200),
    appointment_location TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        r.id,
        r.reminder_type,
        r.title,
        r.scheduled_time,
        r.medication_name,
        r.appointment_location
    FROM user_reminders r
    WHERE r.tenant_id = p_tenant_id
      AND r.user_id = p_user_id
      AND r.is_active = true
      AND r.is_completed = false
      AND DATE(r.scheduled_time AT TIME ZONE r.timezone) = CURRENT_DATE
    ORDER BY r.scheduled_time ASC;
END;
$$;

COMMENT ON FUNCTION get_active_reminders_today IS 'Récupère tous les rappels actifs d''aujourd''hui pour un utilisateur';


-- Fonction: Nettoyer pairings expirés
CREATE OR REPLACE FUNCTION cleanup_expired_pairings() RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    WITH deleted AS (
        DELETE FROM mobile_device_pairings
        WHERE expires_at < NOW()
          AND pairing_status = 'pending'
        RETURNING id
    )
    SELECT COUNT(*) INTO deleted_count FROM deleted;

    RETURN deleted_count;
END;
$$;

COMMENT ON FUNCTION cleanup_expired_pairings IS 'Supprime les tokens d''appairage expirés (cron job)';

COMMIT;
