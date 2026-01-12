"""
Test du systeme RAG Legal avec le Code Civil Algerien
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "http://localhost:8000")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

async def insert_test_data():
    """Insere les donnees de test directement via SQL"""

    # Donnees de test - Articles cles du Code Civil
    articles = [
        {
            "article_number": "Art. 124",
            "content": "Tout fait quelconque de l'homme qui cause a autrui un dommage oblige celui par la faute duquel il est arrive a le reparer.",
            "hierarchy_path": ["LIVRE II", "TITRE I", "CHAPITRE III", "Section 1"],
            "context": "[Code Civil Algerien - LIVRE II > TITRE I > CHAPITRE III - Art. 124]"
        },
        {
            "article_number": "Art. 125",
            "content": "Ne donne pas lieu a reparation le dommage qui resulte de l'exercice normal d'un droit, notamment lorsque cet exercice n'a pour but que de nuire a autrui.",
            "hierarchy_path": ["LIVRE II", "TITRE I", "CHAPITRE III", "Section 1"],
            "context": "[Code Civil Algerien - Art. 125]"
        },
        {
            "article_number": "Art. 134",
            "content": "Le pere, et la mere apres le deces du pere, sont responsables du dommage cause par leurs enfants mineurs habitant avec eux. Les maitres et commettants sont responsables du dommage cause par leurs domestiques et preposes lorsque le fait dommageable a ete accompli par ceux-ci dans leurs fonctions.",
            "hierarchy_path": ["LIVRE II", "TITRE I", "CHAPITRE III", "Section 2"],
            "context": "[Code Civil Algerien - Art. 134]"
        },
        {
            "article_number": "Art. 138",
            "content": "Toute personne qui a la garde d'une chose et qui en assure le pouvoir d'usage, de direction et de controle est responsable du dommage cause par cette chose.",
            "hierarchy_path": ["LIVRE II", "TITRE I", "CHAPITRE III", "Section 3"],
            "context": "[Code Civil Algerien - Art. 138]"
        },
        {
            "article_number": "Art. 182",
            "content": "En cas d'inexecution totale ou partielle de l'obligation ou de retard dans son execution, le juge condamne le debiteur a des dommages-interets a raison du prejudice subi par le creancier.",
            "hierarchy_path": ["LIVRE II", "TITRE II", "CHAPITRE II"],
            "context": "[Code Civil Algerien - Art. 182]"
        }
    ]

    print("=== Insertion des donnees de test ===\n")

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Creer la source
        print("1. Creation de la source juridique...")
        try:
            resp = await client.post(
                f"{SUPABASE_URL}/rest/v1/legal_sources",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation"
                },
                json={
                    "code": "CODE_CIVIL_DZ",
                    "title": "Code Civil Algerien",
                    "short_title": "CC-DZ",
                    "jurisdiction": "DZ",
                    "legal_type": "code",
                    "language": "fr"
                }
            )
            resp.raise_for_status()
            source = resp.json()[0]
            source_id = source["id"]
            print(f"   Source creee: {source_id}")
        except httpx.HTTPStatusError as e:
            print(f"   Erreur: {e.response.text}")
            return

        # 2. Inserer les articles
        print("\n2. Insertion des articles...")
        doc_ids = []
        for art in articles:
            try:
                resp = await client.post(
                    f"{SUPABASE_URL}/rest/v1/legal_documents",
                    headers={
                        "apikey": SUPABASE_KEY,
                        "Authorization": f"Bearer {SUPABASE_KEY}",
                        "Content-Type": "application/json",
                        "Prefer": "return=representation"
                    },
                    json={
                        "source_id": source_id,
                        "article_number": art["article_number"],
                        "content": art["content"],
                        "hierarchy_path": art["hierarchy_path"],
                        "hierarchy_level": 5,
                        "word_count": len(art["content"].split())
                    }
                )
                resp.raise_for_status()
                doc = resp.json()[0]
                doc_ids.append((doc["id"], art))
                print(f"   {art['article_number']} insere")
            except httpx.HTTPStatusError as e:
                print(f"   Erreur {art['article_number']}: {e.response.text}")

        # 3. Inserer les chunks (sans embeddings pour le test)
        print("\n3. Insertion des chunks...")
        for doc_id, art in doc_ids:
            try:
                # Generer un embedding factice (zeros) pour le test
                fake_embedding = [0.0] * 1536

                resp = await client.post(
                    f"{SUPABASE_URL}/rest/v1/document_chunks",
                    headers={
                        "apikey": SUPABASE_KEY,
                        "Authorization": f"Bearer {SUPABASE_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "document_id": doc_id,
                        "source_id": source_id,
                        "content": art["content"],
                        "content_with_context": f"{art['context']}\n{art['content']}",
                        "context_prefix": art["context"],
                        "embedding": fake_embedding,
                        "chunk_index": 0,
                        "char_start": 0,
                        "char_end": len(art["content"]),
                        "metadata": {
                            "source_code": "CODE_CIVIL_DZ",
                            "jurisdiction": "DZ"
                        }
                    }
                )
                resp.raise_for_status()
                print(f"   Chunk {art['article_number']} insere")
            except httpx.HTTPStatusError as e:
                print(f"   Erreur chunk: {e.response.text}")

    print("\n=== Donnees de test inserees ===")


async def test_keyword_search(query: str):
    """Test de recherche par mots-cles (BM25)"""
    print(f"\n=== Test Recherche BM25: '{query}' ===\n")

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Recherche full-text via Supabase
        resp = await client.get(
            f"{SUPABASE_URL}/rest/v1/document_chunks",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
            },
            params={
                "content_tsv": f"fts.{query}",
                "select": "content,context_prefix",
                "limit": "5"
            }
        )

        if resp.status_code == 200:
            results = resp.json()
            if results:
                for i, r in enumerate(results, 1):
                    print(f"{i}. {r['context_prefix']}")
                    print(f"   {r['content'][:100]}...\n")
            else:
                print("   Aucun resultat")
        else:
            print(f"   Erreur: {resp.text}")


async def test_sql_search(query: str):
    """Test de recherche SQL directe"""
    print(f"\n=== Test Recherche SQL: '{query}' ===\n")

    sql = f"""
    SELECT
        dc.context_prefix,
        dc.content,
        ts_rank_cd(dc.content_tsv, websearch_to_tsquery('french', '{query}')) as score
    FROM document_chunks dc
    WHERE dc.content_tsv @@ websearch_to_tsquery('french', '{query}')
    ORDER BY score DESC
    LIMIT 5;
    """

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{SUPABASE_URL}/rest/v1/rpc/",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json"
            },
            json={"query": sql}
        )
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text[:500]}")


async def verify_data():
    """Verifie les donnees inserees"""
    print("\n=== Verification des donnees ===\n")

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Compter les sources
        resp = await client.get(
            f"{SUPABASE_URL}/rest/v1/legal_sources",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Prefer": "count=exact"
            },
            params={"select": "id,code,title"}
        )
        sources = resp.json()
        print(f"Sources: {len(sources)}")
        for s in sources:
            print(f"  - {s['code']}: {s['title']}")

        # Compter les documents
        resp = await client.get(
            f"{SUPABASE_URL}/rest/v1/legal_documents",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Prefer": "count=exact"
            },
            params={"select": "id,article_number"}
        )
        docs = resp.json()
        print(f"\nDocuments: {len(docs)}")
        for d in docs[:5]:
            print(f"  - {d['article_number']}")

        # Compter les chunks
        resp = await client.get(
            f"{SUPABASE_URL}/rest/v1/document_chunks",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Prefer": "count=exact"
            },
            params={"select": "id"}
        )
        chunks = resp.json()
        print(f"\nChunks: {len(chunks)}")


async def main():
    print("=" * 60)
    print("TEST DU SYSTEME RAG LEGAL - CODE CIVIL ALGERIEN")
    print("=" * 60)

    # 1. Inserer les donnees de test
    await insert_test_data()

    # 2. Verifier les donnees
    await verify_data()

    # 3. Test de recherche
    await test_keyword_search("dommage reparer faute")
    await test_keyword_search("responsabilite enfants mineurs")
    await test_keyword_search("garde chose")

    print("\n" + "=" * 60)
    print("TEST TERMINE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
