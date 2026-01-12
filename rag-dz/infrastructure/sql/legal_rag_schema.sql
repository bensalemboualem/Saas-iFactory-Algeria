-- =============================================================================
-- IA FACTORY - LEGAL RAG SCHEMA
-- Architecture optimisee pour documents juridiques (Algerie/Suisse)
-- =============================================================================

-- Extensions requises
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- =============================================================================
-- TABLE: legal_sources (Codes, Lois, Decrets)
-- =============================================================================
CREATE TABLE IF NOT EXISTS legal_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Identification
    code VARCHAR(50) NOT NULL,
    title TEXT NOT NULL,
    short_title VARCHAR(100),

    -- Juridiction
    jurisdiction VARCHAR(50) NOT NULL,
    legal_type VARCHAR(50) NOT NULL,

    -- Dates
    publication_date DATE,
    effective_date DATE,
    last_amendment_date DATE,

    -- Metadonnees
    source_url TEXT,
    language VARCHAR(10) DEFAULT 'fr',
    is_active BOOLEAN DEFAULT true,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_legal_sources_jurisdiction ON legal_sources(jurisdiction);
CREATE INDEX IF NOT EXISTS idx_legal_sources_type ON legal_sources(legal_type);

-- =============================================================================
-- TABLE: legal_documents (Articles, Alineas)
-- =============================================================================
CREATE TABLE IF NOT EXISTS legal_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID REFERENCES legal_sources(id) ON DELETE CASCADE,

    -- Hierarchie structurelle
    parent_id UUID REFERENCES legal_documents(id),
    hierarchy_level INTEGER NOT NULL,
    hierarchy_path TEXT[],

    -- Identification article
    article_number VARCHAR(50),
    article_title TEXT,

    -- Contenu
    content TEXT NOT NULL,
    content_html TEXT,

    -- Full-Text Search
    content_tsv TSVECTOR GENERATED ALWAYS AS (
        setweight(to_tsvector('french', COALESCE(article_title, '')), 'A') ||
        setweight(to_tsvector('french', content), 'B')
    ) STORED,

    -- Metadonnees
    word_count INTEGER,
    is_amended BOOLEAN DEFAULT false,
    amendment_date DATE,
    amendment_ref TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_legal_docs_source ON legal_documents(source_id);
CREATE INDEX IF NOT EXISTS idx_legal_docs_parent ON legal_documents(parent_id);
CREATE INDEX IF NOT EXISTS idx_legal_docs_article ON legal_documents(article_number);
CREATE INDEX IF NOT EXISTS idx_legal_docs_tsv ON legal_documents USING GIN(content_tsv);

-- =============================================================================
-- TABLE: document_chunks (Vecteurs pour RAG)
-- =============================================================================
CREATE TABLE IF NOT EXISTS document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES legal_documents(id) ON DELETE CASCADE,
    source_id UUID REFERENCES legal_sources(id) ON DELETE CASCADE,

    -- Contenu du chunk
    content TEXT NOT NULL,
    content_with_context TEXT,

    -- Embedding vectoriel (OpenAI ada-002 = 1536)
    embedding vector(1536),

    -- Position
    chunk_index INTEGER NOT NULL,
    char_start INTEGER,
    char_end INTEGER,

    -- Contexte enrichi
    context_prefix TEXT,

    -- Full-Text Search
    content_tsv TSVECTOR GENERATED ALWAYS AS (
        to_tsvector('french', content)
    ) STORED,

    -- Metadonnees pour filtrage
    metadata JSONB DEFAULT '{}',

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index HNSW pour recherche vectorielle rapide
CREATE INDEX IF NOT EXISTS idx_chunks_embedding ON document_chunks
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

CREATE INDEX IF NOT EXISTS idx_chunks_document ON document_chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_chunks_source ON document_chunks(source_id);
CREATE INDEX IF NOT EXISTS idx_chunks_tsv ON document_chunks USING GIN(content_tsv);
CREATE INDEX IF NOT EXISTS idx_chunks_metadata ON document_chunks USING GIN(metadata);

-- =============================================================================
-- TABLE: legal_references (Citations croisees)
-- =============================================================================
CREATE TABLE IF NOT EXISTS legal_references (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_document_id UUID REFERENCES legal_documents(id) ON DELETE CASCADE,
    target_document_id UUID REFERENCES legal_documents(id) ON DELETE CASCADE,
    reference_type VARCHAR(50),
    reference_text TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_refs_source ON legal_references(source_document_id);
CREATE INDEX IF NOT EXISTS idx_refs_target ON legal_references(target_document_id);

-- =============================================================================
-- FONCTION: Recherche Hybride (Vecteurs + BM25 avec RRF)
-- =============================================================================
CREATE OR REPLACE FUNCTION hybrid_legal_search(
    query_text TEXT,
    query_embedding vector(1536),
    match_count INTEGER DEFAULT 20,
    jurisdiction_filter TEXT DEFAULT NULL,
    source_filter UUID DEFAULT NULL,
    vector_weight FLOAT DEFAULT 0.3,
    keyword_weight FLOAT DEFAULT 0.7
)
RETURNS TABLE (
    chunk_id UUID,
    document_id UUID,
    content TEXT,
    context_prefix TEXT,
    article_number VARCHAR(50),
    source_title TEXT,
    combined_score FLOAT,
    vector_score FLOAT,
    keyword_score FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    WITH vector_search AS (
        SELECT
            dc.id,
            dc.document_id,
            dc.content,
            dc.context_prefix,
            1 - (dc.embedding <=> query_embedding) AS similarity,
            ROW_NUMBER() OVER (ORDER BY dc.embedding <=> query_embedding) AS rank
        FROM document_chunks dc
        JOIN legal_documents ld ON dc.document_id = ld.id
        JOIN legal_sources ls ON dc.source_id = ls.id
        WHERE
            (jurisdiction_filter IS NULL OR ls.jurisdiction = jurisdiction_filter)
            AND (source_filter IS NULL OR dc.source_id = source_filter)
        ORDER BY dc.embedding <=> query_embedding
        LIMIT match_count * 2
    ),
    keyword_search AS (
        SELECT
            dc.id,
            dc.document_id,
            dc.content,
            dc.context_prefix,
            ts_rank_cd(dc.content_tsv, websearch_to_tsquery('french', query_text)) AS rank_score,
            ROW_NUMBER() OVER (ORDER BY ts_rank_cd(dc.content_tsv, websearch_to_tsquery('french', query_text)) DESC) AS rank
        FROM document_chunks dc
        JOIN legal_documents ld ON dc.document_id = ld.id
        JOIN legal_sources ls ON dc.source_id = ls.id
        WHERE
            dc.content_tsv @@ websearch_to_tsquery('french', query_text)
            AND (jurisdiction_filter IS NULL OR ls.jurisdiction = jurisdiction_filter)
            AND (source_filter IS NULL OR dc.source_id = source_filter)
        ORDER BY rank_score DESC
        LIMIT match_count * 2
    ),
    rrf_combined AS (
        SELECT
            COALESCE(v.id, k.id) AS chunk_id,
            COALESCE(v.document_id, k.document_id) AS doc_id,
            COALESCE(v.content, k.content) AS content,
            COALESCE(v.context_prefix, k.context_prefix) AS ctx_prefix,
            COALESCE(v.similarity, 0) AS vec_score,
            COALESCE(k.rank_score, 0) AS kw_score,
            (vector_weight * COALESCE(1.0 / (60 + v.rank), 0)) +
            (keyword_weight * COALESCE(1.0 / (60 + k.rank), 0)) AS rrf_score
        FROM vector_search v
        FULL OUTER JOIN keyword_search k ON v.id = k.id
    )
    SELECT
        r.chunk_id,
        r.doc_id,
        r.content,
        r.ctx_prefix,
        ld.article_number,
        ls.title,
        r.rrf_score,
        r.vec_score,
        r.kw_score
    FROM rrf_combined r
    JOIN legal_documents ld ON r.doc_id = ld.id
    JOIN legal_sources ls ON ld.source_id = ls.id
    ORDER BY r.rrf_score DESC
    LIMIT match_count;
END;
$$;

-- =============================================================================
-- FONCTION: Recherche par similarite simple
-- =============================================================================
CREATE OR REPLACE FUNCTION match_legal_chunks(
    query_embedding vector(1536),
    match_threshold FLOAT DEFAULT 0.7,
    match_count INTEGER DEFAULT 10,
    jurisdiction_filter TEXT DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    content TEXT,
    context_prefix TEXT,
    article_number VARCHAR(50),
    source_title TEXT,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        dc.id,
        dc.content,
        dc.context_prefix,
        ld.article_number,
        ls.title,
        1 - (dc.embedding <=> query_embedding) AS similarity
    FROM document_chunks dc
    JOIN legal_documents ld ON dc.document_id = ld.id
    JOIN legal_sources ls ON ld.source_id = ls.id
    WHERE
        1 - (dc.embedding <=> query_embedding) > match_threshold
        AND (jurisdiction_filter IS NULL OR ls.jurisdiction = jurisdiction_filter)
    ORDER BY dc.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Trigger pour updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_legal_sources_updated ON legal_sources;
CREATE TRIGGER trigger_legal_sources_updated
    BEFORE UPDATE ON legal_sources
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

DROP TRIGGER IF EXISTS trigger_legal_documents_updated ON legal_documents;
CREATE TRIGGER trigger_legal_documents_updated
    BEFORE UPDATE ON legal_documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- COMMENTAIRES
-- =============================================================================
COMMENT ON TABLE legal_sources IS 'Codes, lois et decrets (sources juridiques)';
COMMENT ON TABLE legal_documents IS 'Articles et alineas avec hierarchie structurelle';
COMMENT ON TABLE document_chunks IS 'Chunks vectorises pour RAG avec HNSW index';
COMMENT ON FUNCTION hybrid_legal_search IS 'Recherche hybride RRF (70% BM25 + 30% vecteurs)';
