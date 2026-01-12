-- ==============================================
-- CONFIGURATION COMPLÈTE SUPABASE POUR RAG.DZ
-- ==============================================
-- Copier-coller ce fichier dans le SQL Editor de Supabase
-- https://supabase.com/dashboard -> SQL Editor -> New Query

-- ==============================================
-- ÉTAPE 1: Extensions
-- ==============================================

-- Extension UUID (si pas déjà activée)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Extension PGVector pour recherche vectorielle
CREATE EXTENSION IF NOT EXISTS vector;

-- Vérifier que PGVector est installé
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') THEN
        RAISE EXCEPTION 'PGVector extension non installée. Contactez le support Supabase.';
    END IF;
END $$;

-- ==============================================
-- ÉTAPE 2: Types et Tables de Base
-- ==============================================

-- Types énumérés
DO $$ BEGIN
    CREATE TYPE tenant_plan AS ENUM ('free', 'pro', 'enterprise');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE tenant_status AS ENUM ('active', 'suspended', 'deleted');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Table Tenants
CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    plan tenant_plan NOT NULL DEFAULT 'free',
    status tenant_status NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table API Keys
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    key_hash TEXT UNIQUE NOT NULL,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name TEXT NOT NULL DEFAULT 'Default Key',
    plan tenant_plan NOT NULL,
    quota_tokens_monthly BIGINT NOT NULL DEFAULT 100000,
    quota_audio_seconds_monthly INTEGER NOT NULL DEFAULT 1800,
    quota_ocr_pages_monthly INTEGER NOT NULL DEFAULT 50,
    rate_limit_per_minute INTEGER NOT NULL DEFAULT 10,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    revoked BOOLEAN DEFAULT FALSE
);

-- Table Usage Events
CREATE TABLE IF NOT EXISTS usage_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
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

-- Index de performance pour tables de base
CREATE INDEX IF NOT EXISTS idx_usage_tenant_timestamp
ON usage_events (tenant_id, timestamp);

CREATE INDEX IF NOT EXISTS idx_api_keys_tenant
ON api_keys (tenant_id) WHERE NOT revoked;

-- ==============================================
-- ÉTAPE 3: Tables PGVector pour RAG
-- ==============================================

-- Table pour embeddings de documents
CREATE TABLE IF NOT EXISTS document_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    document_id TEXT NOT NULL,
    chunk_index INTEGER DEFAULT 0,
    text TEXT NOT NULL,
    embedding vector(768),  -- 768 dimensions pour paraphrase-multilingual-mpnet-base-v2
    metadata JSONB DEFAULT '{}'::jsonb,
    language VARCHAR(10) DEFAULT 'fr',
    title TEXT,
    source_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index vectoriel pour recherche sémantique rapide
CREATE INDEX IF NOT EXISTS document_embeddings_vector_idx
ON document_embeddings
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Index pour recherches par tenant
CREATE INDEX IF NOT EXISTS document_embeddings_tenant_idx
ON document_embeddings(tenant_id);

-- Index pour recherches par langue
CREATE INDEX IF NOT EXISTS document_embeddings_language_idx
ON document_embeddings(language);

-- Index pour métadonnées JSONB
CREATE INDEX IF NOT EXISTS document_embeddings_metadata_idx
ON document_embeddings USING gin(metadata);

-- Index composite pour filtres fréquents
CREATE INDEX IF NOT EXISTS document_embeddings_tenant_lang_idx
ON document_embeddings(tenant_id, language);

-- Table pour exemples de code avec embeddings
CREATE TABLE IF NOT EXISTS code_examples (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    source_id TEXT,
    code TEXT NOT NULL,
    language VARCHAR(50),  -- Python, JavaScript, Go, etc.
    description TEXT,
    embedding vector(768),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index vectoriel pour code examples
CREATE INDEX IF NOT EXISTS code_examples_vector_idx
ON code_examples
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 50);

-- Index par tenant et langage
CREATE INDEX IF NOT EXISTS code_examples_tenant_lang_idx
ON code_examples(tenant_id, language);

-- ==============================================
-- ÉTAPE 4: Fonctions de Recherche Vectorielle
-- ==============================================

-- Fonction de recherche hybride pour documents
CREATE OR REPLACE FUNCTION search_documents_hybrid(
    query_embedding vector(768),
    p_tenant_id UUID,
    match_threshold FLOAT DEFAULT 0.3,
    match_count INT DEFAULT 10,
    filter_language TEXT DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    document_id TEXT,
    text TEXT,
    title TEXT,
    language VARCHAR(10),
    similarity FLOAT,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        de.id,
        de.document_id,
        de.text,
        de.title,
        de.language,
        1 - (de.embedding <=> query_embedding) AS similarity,
        de.metadata,
        de.created_at
    FROM document_embeddings de
    WHERE (p_tenant_id IS NULL OR de.tenant_id = p_tenant_id)
        AND (filter_language IS NULL OR de.language = filter_language)
        AND 1 - (de.embedding <=> query_embedding) > match_threshold
    ORDER BY de.embedding <=> query_embedding
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql;

-- Fonction de recherche pour code examples
CREATE OR REPLACE FUNCTION search_code_examples(
    query_embedding vector(768),
    p_tenant_id UUID,
    match_threshold FLOAT DEFAULT 0.3,
    match_count INT DEFAULT 5,
    filter_language TEXT DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    code TEXT,
    language VARCHAR(50),
    description TEXT,
    similarity FLOAT,
    metadata JSONB
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        ce.id,
        ce.code,
        ce.language,
        ce.description,
        1 - (ce.embedding <=> query_embedding) AS similarity,
        ce.metadata
    FROM code_examples ce
    WHERE (p_tenant_id IS NULL OR ce.tenant_id = p_tenant_id)
        AND (filter_language IS NULL OR ce.language = filter_language)
        AND 1 - (ce.embedding <=> query_embedding) > match_threshold
    ORDER BY ce.embedding <=> query_embedding
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql;

-- ==============================================
-- ÉTAPE 5: Triggers et Automatisations
-- ==============================================

-- Fonction pour auto-update de updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger pour document_embeddings
DROP TRIGGER IF EXISTS update_document_embeddings_updated_at ON document_embeddings;
CREATE TRIGGER update_document_embeddings_updated_at
BEFORE UPDATE ON document_embeddings
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==============================================
-- ÉTAPE 6: Vues pour Statistiques
-- ==============================================

-- Vue pour statistiques d'embeddings
CREATE OR REPLACE VIEW embedding_stats AS
SELECT
    tenant_id,
    language,
    COUNT(*) as total_embeddings,
    COUNT(DISTINCT document_id) as unique_documents,
    AVG(LENGTH(text))::INTEGER as avg_text_length,
    MIN(created_at) as first_embedding,
    MAX(created_at) as last_embedding
FROM document_embeddings
GROUP BY tenant_id, language;

-- ==============================================
-- ÉTAPE 7: Données de Test (Optionnel)
-- ==============================================

-- Créer un tenant de démo
INSERT INTO tenants (id, name, plan, status)
VALUES ('00000000-0000-0000-0000-000000000001', 'Demo Tenant', 'pro', 'active')
ON CONFLICT (id) DO NOTHING;

-- Créer une API key de démo (hash de "ragdz_demo_key_2024")
INSERT INTO api_keys (key_hash, tenant_id, name, plan)
VALUES (
    'e8c4f7b8d9e6c8a5f3b2d1a9e7c6b5a4d3c2b1a0f9e8d7c6b5a4d3c2b1a0f9e8',
    '00000000-0000-0000-0000-000000000001',
    'Demo API Key',
    'pro'
)
ON CONFLICT (key_hash) DO NOTHING;

-- ==============================================
-- ÉTAPE 8: Commentaires pour Documentation
-- ==============================================

COMMENT ON TABLE document_embeddings IS 'Stockage des embeddings de documents avec PGVector pour recherche sémantique rapide';
COMMENT ON TABLE code_examples IS 'Stockage des exemples de code avec embeddings pour recherche sémantique';
COMMENT ON FUNCTION search_documents_hybrid IS 'Recherche vectorielle hybride avec filtrage par tenant et langue';
COMMENT ON FUNCTION search_code_examples IS 'Recherche d''exemples de code par similarité sémantique';
COMMENT ON VIEW embedding_stats IS 'Statistiques agrégées des embeddings par tenant et langue';

-- ==============================================
-- ÉTAPE 9: Test de Vérification
-- ==============================================

-- Vérifier que PGVector fonctionne
DO $$
DECLARE
    test_vector vector(3);
BEGIN
    test_vector := '[0.1,0.2,0.3]'::vector(3);
    RAISE NOTICE 'PGVector fonctionne ! Test vector: %', test_vector;
END $$;

-- Compter les tables créées
SELECT
    'Tables créées:' as status,
    COUNT(*) as count
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN ('tenants', 'api_keys', 'usage_events', 'document_embeddings', 'code_examples');

-- Vérifier les extensions
SELECT
    'Extensions actives:' as status,
    extname as extension_name,
    extversion as version
FROM pg_extension
WHERE extname IN ('uuid-ossp', 'vector');

-- ==============================================
-- ✅ CONFIGURATION TERMINÉE !
-- ==============================================
--
-- Prochaines étapes:
-- 1. Vérifier que les tables sont créées dans l'onglet "Table Editor"
-- 2. Tester l'insertion d'un embedding depuis votre application
-- 3. Utiliser la fonction search_documents_hybrid() pour rechercher
--
-- Support: https://supabase.com/docs
-- ==============================================
