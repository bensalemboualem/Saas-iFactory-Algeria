-- ==============================================
-- CONFIGURATION MINIMALE SUPABASE (Version Simple)
-- ==============================================
-- Si la version complète échoue, utilisez celle-ci
-- Copier-coller dans SQL Editor de Supabase

-- ÉTAPE 1: Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- ÉTAPE 2: Types
DO $$ BEGIN
    CREATE TYPE tenant_plan AS ENUM ('free', 'pro', 'enterprise');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE tenant_status AS ENUM ('active', 'suspended', 'deleted');
EXCEPTION WHEN duplicate_object THEN null; END $$;

-- ÉTAPE 3: Table Tenants
CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    plan tenant_plan NOT NULL DEFAULT 'free',
    status tenant_status NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ÉTAPE 4: Table API Keys
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    key_hash TEXT UNIQUE NOT NULL,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name TEXT NOT NULL DEFAULT 'Default Key',
    plan tenant_plan NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    revoked BOOLEAN DEFAULT FALSE
);

-- ÉTAPE 5: Table Document Embeddings (PRINCIPAL)
CREATE TABLE IF NOT EXISTS document_embeddings (
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

-- ÉTAPE 6: Index Vectoriel (IMPORTANT pour performance)
CREATE INDEX IF NOT EXISTS document_embeddings_vector_idx
ON document_embeddings
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- ÉTAPE 7: Index Simples
CREATE INDEX IF NOT EXISTS document_embeddings_tenant_idx ON document_embeddings(tenant_id);
CREATE INDEX IF NOT EXISTS document_embeddings_language_idx ON document_embeddings(language);

-- ÉTAPE 8: Table Code Examples
CREATE TABLE IF NOT EXISTS code_examples (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    code TEXT NOT NULL,
    language VARCHAR(50),
    description TEXT,
    embedding vector(768),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ÉTAPE 9: Index pour Code
CREATE INDEX IF NOT EXISTS code_examples_vector_idx
ON code_examples
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 50);

-- ÉTAPE 10: Fonction de Recherche Documents
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

-- ÉTAPE 11: Fonction de Recherche Code
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

-- ÉTAPE 12: Trigger pour updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS update_document_embeddings_updated_at ON document_embeddings;
CREATE TRIGGER update_document_embeddings_updated_at
BEFORE UPDATE ON document_embeddings
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ÉTAPE 13: Tenant de Démo
INSERT INTO tenants (id, name, plan, status)
VALUES ('00000000-0000-0000-0000-000000000001', 'Demo Tenant', 'pro', 'active')
ON CONFLICT (id) DO NOTHING;

-- ÉTAPE 14: API Key de Démo
INSERT INTO api_keys (key_hash, tenant_id, name, plan)
VALUES (
    'e8c4f7b8d9e6c8a5f3b2d1a9e7c6b5a4d3c2b1a0f9e8d7c6b5a4d3c2b1a0f9e8',
    '00000000-0000-0000-0000-000000000001',
    'Demo API Key',
    'pro'
)
ON CONFLICT (key_hash) DO NOTHING;

-- ÉTAPE 15: Test Final
DO $$
BEGIN
    RAISE NOTICE '✅ Configuration terminée avec succès !';
    RAISE NOTICE '📊 Tables créées: tenants, api_keys, document_embeddings, code_examples';
    RAISE NOTICE '🔍 Fonctions disponibles: search_documents_hybrid(), search_code_examples()';
END $$;

-- Vérification
SELECT
    'Tenant de démo créé' as status,
    id,
    name,
    plan
FROM tenants
WHERE id = '00000000-0000-0000-0000-000000000001';
