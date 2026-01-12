-- ==============================================
-- INSTALLATION PROPRE SUPABASE (Clean Install)
-- ==============================================
-- Cette version nettoie d'abord puis réinstalle tout
-- Utilisez cette version si vous avez des erreurs de "already exists"

-- ==============================================
-- PARTIE 1: NETTOYAGE (peut générer des erreurs, c'est normal)
-- ==============================================

-- Supprimer les triggers existants
DROP TRIGGER IF EXISTS update_document_embeddings_updated_at ON document_embeddings;

-- Supprimer les vues
DROP VIEW IF EXISTS embedding_stats;

-- Supprimer les fonctions
DROP FUNCTION IF EXISTS search_documents_hybrid(vector, uuid, float, int, text);
DROP FUNCTION IF EXISTS search_code_examples(vector, uuid, float, int, text);
DROP FUNCTION IF EXISTS update_updated_at_column();

-- Supprimer les tables (dans l'ordre pour éviter les contraintes FK)
DROP TABLE IF EXISTS usage_events CASCADE;
DROP TABLE IF EXISTS code_examples CASCADE;
DROP TABLE IF EXISTS document_embeddings CASCADE;
DROP TABLE IF EXISTS api_keys CASCADE;
DROP TABLE IF EXISTS tenants CASCADE;

-- Supprimer les types
DROP TYPE IF EXISTS tenant_status CASCADE;
DROP TYPE IF EXISTS tenant_plan CASCADE;

-- ==============================================
-- PARTIE 2: INSTALLATION FRAÎCHE
-- ==============================================

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- Types
CREATE TYPE tenant_plan AS ENUM ('free', 'pro', 'enterprise');
CREATE TYPE tenant_status AS ENUM ('active', 'suspended', 'deleted');

-- Table Tenants
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    plan tenant_plan NOT NULL DEFAULT 'free',
    status tenant_status NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table API Keys
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    key_hash TEXT UNIQUE NOT NULL,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name TEXT NOT NULL DEFAULT 'Default Key',
    plan tenant_plan NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    revoked BOOLEAN DEFAULT FALSE
);

-- Index pour API Keys
CREATE INDEX idx_api_keys_tenant ON api_keys(tenant_id) WHERE NOT revoked;

-- Table Document Embeddings (CŒUR DU SYSTÈME)
CREATE TABLE document_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    document_id TEXT NOT NULL,
    chunk_index INTEGER DEFAULT 0,
    text TEXT NOT NULL,
    embedding vector(768),
    metadata JSONB DEFAULT '{}'::jsonb,
    language VARCHAR(10) DEFAULT 'fr',
    title TEXT,
    source_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index Vectoriel (CRITIQUE pour performance)
CREATE INDEX document_embeddings_vector_idx
ON document_embeddings
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Index de recherche
CREATE INDEX document_embeddings_tenant_idx ON document_embeddings(tenant_id);
CREATE INDEX document_embeddings_language_idx ON document_embeddings(language);
CREATE INDEX document_embeddings_metadata_idx ON document_embeddings USING gin(metadata);

-- Table Code Examples
CREATE TABLE code_examples (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    code TEXT NOT NULL,
    language VARCHAR(50),
    description TEXT,
    embedding vector(768),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour Code
CREATE INDEX code_examples_vector_idx
ON code_examples
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 50);

CREATE INDEX code_examples_tenant_idx ON code_examples(tenant_id);

-- Table Usage Events (optionnel)
CREATE TABLE usage_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    request_id TEXT,
    route TEXT NOT NULL,
    method TEXT NOT NULL,
    tokens_input INTEGER DEFAULT 0,
    tokens_output INTEGER DEFAULT 0,
    latency_ms INTEGER NOT NULL,
    model_used TEXT,
    status_code INTEGER NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_usage_tenant_timestamp ON usage_events(tenant_id, timestamp);

-- ==============================================
-- PARTIE 3: FONCTIONS DE RECHERCHE
-- ==============================================

-- Fonction: Recherche Documents
CREATE FUNCTION search_documents_hybrid(
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
    created_at TIMESTAMPTZ
)
LANGUAGE plpgsql
AS $$
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
        AND (1 - (de.embedding <=> query_embedding)) > match_threshold
    ORDER BY de.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Fonction: Recherche Code
CREATE FUNCTION search_code_examples(
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
)
LANGUAGE plpgsql
AS $$
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
        AND (1 - (ce.embedding <=> query_embedding)) > match_threshold
    ORDER BY ce.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- ==============================================
-- PARTIE 4: TRIGGERS ET AUTOMATISATIONS
-- ==============================================

-- Fonction pour updated_at
CREATE FUNCTION update_updated_at_column()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

-- Trigger
CREATE TRIGGER update_document_embeddings_updated_at
BEFORE UPDATE ON document_embeddings
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==============================================
-- PARTIE 5: VUE STATISTIQUES
-- ==============================================

CREATE VIEW embedding_stats AS
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
-- PARTIE 6: DONNÉES DE DÉMO
-- ==============================================

-- Tenant de démo
INSERT INTO tenants (id, name, plan, status)
VALUES ('00000000-0000-0000-0000-000000000001', 'Demo Tenant', 'pro', 'active');

-- API Key de démo (hash de "ragdz_demo_key_2024")
INSERT INTO api_keys (key_hash, tenant_id, name, plan)
VALUES (
    'e8c4f7b8d9e6c8a5f3b2d1a9e7c6b5a4d3c2b1a0f9e8d7c6b5a4d3c2b1a0f9e8',
    '00000000-0000-0000-0000-000000000001',
    'Demo API Key',
    'pro'
);

-- ==============================================
-- PARTIE 7: VÉRIFICATIONS
-- ==============================================

-- Test PGVector
DO $$
DECLARE
    test_vec vector(3);
BEGIN
    test_vec := '[0.1, 0.2, 0.3]'::vector(3);
    RAISE NOTICE '✅ PGVector fonctionne: %', test_vec;
END $$;

-- Compter les tables
SELECT
    'Tables créées' as status,
    COUNT(*) as count
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN ('tenants', 'api_keys', 'document_embeddings', 'code_examples', 'usage_events');

-- Vérifier les fonctions
SELECT
    'Fonctions créées' as status,
    COUNT(*) as count
FROM information_schema.routines
WHERE routine_schema = 'public'
AND routine_name IN ('search_documents_hybrid', 'search_code_examples', 'update_updated_at_column');

-- Afficher le tenant de démo
SELECT
    '✅ Tenant de démo' as status,
    id,
    name,
    plan,
    status
FROM tenants
WHERE id = '00000000-0000-0000-0000-000000000001';

-- Message final
DO $$
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '╔═══════════════════════════════════════════════════════╗';
    RAISE NOTICE '║  ✅ INSTALLATION TERMINÉE AVEC SUCCÈS !              ║';
    RAISE NOTICE '║                                                       ║';
    RAISE NOTICE '║  📊 Tables: tenants, api_keys, document_embeddings  ║';
    RAISE NOTICE '║  🔍 Fonctions: search_documents_hybrid()            ║';
    RAISE NOTICE '║  🧪 Tenant démo: 00000000-0000-0000-0000-000000000001║';
    RAISE NOTICE '║                                                       ║';
    RAISE NOTICE '║  Prochaine étape: Tester depuis votre application   ║';
    RAISE NOTICE '╚═══════════════════════════════════════════════════════╝';
END $$;
