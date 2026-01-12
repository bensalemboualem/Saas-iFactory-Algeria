# 🗄️ Configuration Supabase pour RAG.dz

Votre clé Supabase a été configurée. Voici comment finaliser l'intégration.

## ✅ Déjà Configuré

```env
SUPABASE_URL=https://qyxqxudebrarогprrnnpz.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 📋 Étapes de Configuration

### 1. Activer PGVector dans Supabase

Dans le **SQL Editor** de votre dashboard Supabase (https://supabase.com/dashboard), exécutez :

```sql
-- Activer l'extension PGVector
CREATE EXTENSION IF NOT EXISTS vector;

-- Vérifier l'installation
SELECT * FROM pg_extension WHERE extname='vector';
```

### 2. Créer les Tables

Exécutez le contenu du fichier `sql/pgvector_migration.sql` dans votre SQL Editor Supabase :

```sql
-- Table pour les embeddings de documents
CREATE TABLE IF NOT EXISTS document_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID,
    document_id TEXT NOT NULL,
    chunk_index INTEGER DEFAULT 0,
    text TEXT NOT NULL,
    embedding vector(768),
    metadata JSONB DEFAULT '{}'::jsonb,
    language VARCHAR(10) DEFAULT 'fr',
    title TEXT,
    source_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour recherche vectorielle
CREATE INDEX IF NOT EXISTS document_embeddings_vector_idx
ON document_embeddings
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Table pour code examples
CREATE TABLE IF NOT EXISTS code_examples (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID,
    source_id TEXT,
    code TEXT NOT NULL,
    language VARCHAR(50),
    description TEXT,
    embedding vector(768),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index vectoriel pour code
CREATE INDEX IF NOT EXISTS code_examples_vector_idx
ON code_examples
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 50);

-- Fonction de recherche
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

-- Fonction pour recherche de code
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
```

### 3. Tester la Configuration

Dans votre SQL Editor :

```sql
-- Vérifier que PGVector fonctionne
SELECT '[0.1,0.2,0.3]'::vector(3);

-- Devrait retourner: [0.1,0.2,0.3]
```

## 🚀 Utilisation dans le Code

### Insertion d'Embeddings

```python
from app.clients.supabase_client import supabase_client

# Insérer un document avec embedding
success = await supabase_client.insert_document_embedding(
    tenant_id="00000000-0000-0000-0000-000000000001",
    document_id="doc_123",
    text="Ceci est un document de test",
    embedding=[0.1, 0.2, 0.3, ...],  # 768 dimensions
    language="fr",
    title="Document de test",
    metadata={"source": "test"}
)
```

### Recherche Vectorielle

```python
from app.clients.embeddings import embed_queries

# Créer l'embedding de la query
query_embedding = embed_queries(["comment fonctionne le système ?"])[0]

# Rechercher
results = await supabase_client.search_documents(
    query_embedding=query_embedding,
    tenant_id="00000000-0000-0000-0000-000000000001",
    match_threshold=0.3,
    match_count=10,
    filter_language="fr"
)

for result in results:
    print(f"Score: {result['similarity']:.3f}")
    print(f"Text: {result['text'][:100]}...")
```

### Statistiques

```python
stats = await supabase_client.get_tenant_stats(
    tenant_id="00000000-0000-0000-0000-000000000001"
)

print(f"Total embeddings: {stats.get('total_embeddings', 0)}")
print(f"Documents uniques: {stats.get('unique_documents', 0)}")
```

## 🔄 Architecture Hybride

Vous avez maintenant **3 options** pour le stockage vectoriel :

### 1. **Qdrant** (existant)
- Service dédié ultra-rapide
- Meilleur pour très gros volumes (millions de vecteurs)
- Scalable horizontalement

### 2. **PGVector Local** (nouveau)
- Dans votre PostgreSQL Docker local
- Bon pour dev et petits/moyens volumes
- Tout dans une seule DB

### 3. **Supabase + PGVector** (nouveau)
- PostgreSQL cloud avec PGVector
- Géré, backups automatiques, scaling facile
- Parfait pour production sans gérer l'infra

## 💡 Recommandation

**Pour Démarrer**: Utilisez **Supabase** car :
- ✅ Déjà configuré
- ✅ Pas besoin de gérer Docker/infra
- ✅ Backups automatiques
- ✅ Interface web pour visualiser les données
- ✅ Gratuit jusqu'à 500 MB + 2GB transfer

**Pour Scale**: Gardez **Qdrant** si vous avez besoin de :
- Millions de vecteurs
- Latence ultra-basse (<10ms)
- Features avancées (quantization, sharding)

## 🔧 Changer de Backend Vectoriel

Dans votre code, créez un wrapper pour choisir dynamiquement :

```python
# Dans votre config
VECTOR_BACKEND = os.getenv("VECTOR_BACKEND", "supabase")  # ou "qdrant" ou "pgvector"

async def search_vectors(query_embedding, tenant_id, **kwargs):
    if VECTOR_BACKEND == "supabase":
        return await supabase_client.search_documents(query_embedding, tenant_id, **kwargs)
    elif VECTOR_BACKEND == "pgvector":
        return await pgvector_client.search_documents(query_embedding, tenant_id, **kwargs)
    else:
        # Qdrant existant
        from app.clients.qdrant_client import search_vectors
        return search_vectors(...)
```

## 📊 Monitoring Supabase

Depuis le dashboard Supabase :

1. **Database** → Voir vos tables
2. **Table Editor** → Visualiser `document_embeddings`
3. **SQL Editor** → Requêtes custom
4. **Logs** → Monitoring des requêtes
5. **Settings** → Usage et limites

## 🆘 Troubleshooting

### Erreur "extension vector does not exist"
```sql
-- Se connecter en tant que superuser et exécuter :
CREATE EXTENSION vector;
```

### Erreur "function search_documents_hybrid does not exist"
Ré-exécutez les fonctions SQL du fichier `pgvector_migration.sql`.

### Performance lente
```sql
-- Vérifier que les index sont créés
SELECT * FROM pg_indexes WHERE tablename = 'document_embeddings';

-- Re-créer l'index si nécessaire
DROP INDEX IF EXISTS document_embeddings_vector_idx;
CREATE INDEX document_embeddings_vector_idx
ON document_embeddings
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

## 🎯 Next Steps

1. **Exécuter les migrations SQL** dans Supabase
2. **Tester l'insertion** d'un embedding
3. **Tester la recherche** vectorielle
4. **Comparer performances** Supabase vs Qdrant pour votre use case

---

**Questions ?** Consultez la [documentation Supabase](https://supabase.com/docs) ou [PGVector](https://github.com/pgvector/pgvector)
