-- Migration pour ajouter PGVector support à PostgreSQL
-- Inspiré d'Archon pour améliorer les performances vectorielles

-- Activer l'extension PGVector
CREATE EXTENSION IF NOT EXISTS vector;

-- Table pour les embeddings de documents avec PGVector
CREATE TABLE IF NOT EXISTS document_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    document_id TEXT NOT NULL,
    chunk_index INTEGER DEFAULT 0,
    text TEXT NOT NULL,
    embedding vector(768),  -- Dimension pour paraphrase-multilingual-mpnet-base-v2
    metadata JSONB DEFAULT '{}'::jsonb,
    language VARCHAR(10) DEFAULT 'fr',
    title TEXT,
    source_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour recherche vectorielle rapide avec IVFFlat
-- IVFFlat divise l'espace vectoriel en "lists" pour recherche rapide
-- Plus de lists = recherche plus rapide mais moins précise
CREATE INDEX IF NOT EXISTS document_embeddings_vector_idx
ON document_embeddings
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Index pour les recherches par tenant
CREATE INDEX IF NOT EXISTS document_embeddings_tenant_idx
ON document_embeddings(tenant_id);

-- Index pour les recherches par langue
CREATE INDEX IF NOT EXISTS document_embeddings_language_idx
ON document_embeddings(language);

-- Index pour métadonnées JSONB
CREATE INDEX IF NOT EXISTS document_embeddings_metadata_idx
ON document_embeddings USING gin(metadata);

-- Index composite pour filtres fréquents
CREATE INDEX IF NOT EXISTS document_embeddings_tenant_lang_idx
ON document_embeddings(tenant_id, language);

-- Table pour code examples avec embeddings
CREATE TABLE IF NOT EXISTS code_examples (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    source_id TEXT,
    code TEXT NOT NULL,
    language VARCHAR(50),  -- Python, JavaScript, etc.
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

-- Index par tenant et langage de code
CREATE INDEX IF NOT EXISTS code_examples_tenant_lang_idx
ON code_examples(tenant_id, language);

-- Fonction pour recherche vectorielle hybride avec score threshold
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
    WHERE de.tenant_id = p_tenant_id
        AND (filter_language IS NULL OR de.language = filter_language)
        AND 1 - (de.embedding <=> query_embedding) > match_threshold
    ORDER BY de.embedding <=> query_embedding
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql;

-- Fonction pour recherche de code avec embeddings
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
    WHERE ce.tenant_id = p_tenant_id
        AND (filter_language IS NULL OR ce.language = filter_language)
        AND 1 - (ce.embedding <=> query_embedding) > match_threshold
    ORDER BY ce.embedding <=> query_embedding
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql;

-- Trigger pour update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_document_embeddings_updated_at
BEFORE UPDATE ON document_embeddings
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Vue pour statistiques d'embeddings
CREATE OR REPLACE VIEW embedding_stats AS
SELECT
    tenant_id,
    language,
    COUNT(*) as total_embeddings,
    COUNT(DISTINCT document_id) as unique_documents,
    AVG(LENGTH(text)) as avg_text_length,
    MIN(created_at) as first_embedding,
    MAX(created_at) as last_embedding
FROM document_embeddings
GROUP BY tenant_id, language;

-- Commentaires pour documentation
COMMENT ON TABLE document_embeddings IS 'Stockage des embeddings de documents avec PGVector pour recherche sémantique rapide';
COMMENT ON TABLE code_examples IS 'Stockage des exemples de code avec embeddings pour recherche sémantique';
COMMENT ON FUNCTION search_documents_hybrid IS 'Recherche vectorielle hybride avec filtrage par tenant et langue';
COMMENT ON FUNCTION search_code_examples IS 'Recherche d''exemples de code par similarité sémantique';

-- Grant permissions (ajuster selon vos besoins)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON document_embeddings TO your_app_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON code_examples TO your_app_user;
-- GRANT EXECUTE ON FUNCTION search_documents_hybrid TO your_app_user;
-- GRANT EXECUTE ON FUNCTION search_code_examples TO your_app_user;
