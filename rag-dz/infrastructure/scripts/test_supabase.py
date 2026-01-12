"""
Script de test pour vérifier la connexion Supabase et PGVector
"""
import asyncio
import sys
import os

# Ajouter le chemin du projet
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'rag-compat'))

from app.clients.supabase_client import supabase_client
from app.clients.embeddings import embed_queries


async def test_supabase():
    """Test complet de Supabase"""

    print("="*60)
    print("🧪 TEST SUPABASE + PGVECTOR")
    print("="*60)

    # Test 1: Connexion
    print("\n1️⃣ Test de connexion...")
    if supabase_client.is_available():
        print("   ✅ Supabase connecté !")
    else:
        print("   ❌ Supabase non disponible")
        print("   Vérifiez SUPABASE_URL et SUPABASE_SERVICE_KEY dans .env")
        return

    # Test 2: Créer un embedding de test
    print("\n2️⃣ Génération d'un embedding de test...")
    test_texts = ["Ceci est un document de test pour vérifier PGVector"]

    try:
        embeddings = embed_queries(test_texts)
        print(f"   ✅ Embedding généré : {len(embeddings[0])} dimensions")
    except Exception as e:
        print(f"   ❌ Erreur génération embedding : {e}")
        return

    # Test 3: Insertion dans Supabase
    print("\n3️⃣ Insertion d'un document de test dans Supabase...")
    tenant_id = "00000000-0000-0000-0000-000000000001"

    try:
        success = await supabase_client.insert_document_embedding(
            tenant_id=tenant_id,
            document_id="test_doc_001",
            text=test_texts[0],
            embedding=embeddings[0],
            language="fr",
            title="Document de Test",
            metadata={"source": "test_script", "type": "demo"},
            chunk_index=0
        )

        if success:
            print("   ✅ Document inséré avec succès !")
        else:
            print("   ❌ Échec insertion document")
            return
    except Exception as e:
        print(f"   ❌ Erreur insertion : {e}")
        return

    # Test 4: Recherche vectorielle
    print("\n4️⃣ Test de recherche vectorielle...")

    try:
        # Générer un embedding pour la query
        query_texts = ["test document"]
        query_embeddings = embed_queries(query_texts)

        # Rechercher
        results = await supabase_client.search_documents(
            query_embedding=query_embeddings[0],
            tenant_id=tenant_id,
            match_threshold=0.0,  # Très bas pour être sûr de trouver
            match_count=5
        )

        print(f"   ✅ Recherche effectuée : {len(results)} résultats trouvés")

        if results:
            print("\n   📄 Premier résultat :")
            first = results[0]
            print(f"      • ID: {first.get('id')}")
            print(f"      • Score: {first.get('similarity', 0):.4f}")
            print(f"      • Texte: {first.get('text', '')[:80]}...")
            print(f"      • Langue: {first.get('language')}")
    except Exception as e:
        print(f"   ❌ Erreur recherche : {e}")
        return

    # Test 5: Statistiques
    print("\n5️⃣ Récupération des statistiques...")

    try:
        stats = await supabase_client.get_tenant_stats(tenant_id)

        if stats:
            print(f"   ✅ Statistiques récupérées :")
            print(f"      • Total embeddings: {stats.get('total_embeddings', 0)}")
            print(f"      • Documents uniques: {stats.get('unique_documents', 0)}")
            print(f"      • Longueur moyenne: {stats.get('avg_text_length', 0)} caractères")
        else:
            print("   ⚠️  Pas encore de statistiques (normal pour première utilisation)")
    except Exception as e:
        print(f"   ⚠️  Erreur stats (peut être normal) : {e}")

    # Test 6: Test de code example
    print("\n6️⃣ Test insertion code example...")

    try:
        code_text = """
def hello_world():
    print("Hello from RAG.dz!")
    return True
"""
        code_embedding = embed_queries([code_text])[0]

        success = await supabase_client.insert_code_example(
            tenant_id=tenant_id,
            code=code_text,
            language="python",
            embedding=code_embedding,
            description="Simple hello world function",
            metadata={"framework": "python", "complexity": "simple"}
        )

        if success:
            print("   ✅ Code example inséré !")
        else:
            print("   ⚠️  Échec insertion code (table peut ne pas exister)")
    except Exception as e:
        print(f"   ⚠️  Erreur code example (table peut ne pas exister) : {e}")

    # Résumé final
    print("\n" + "="*60)
    print("✅ TESTS TERMINÉS AVEC SUCCÈS !")
    print("="*60)
    print("\n🎯 Votre système Supabase + PGVector est opérationnel !")
    print("\nProchaines étapes :")
    print("1. Intégrer dans vos routes API")
    print("2. Uploader vos vrais documents")
    print("3. Tester avec votre frontend")
    print("\n" + "="*60)


async def cleanup_test_data():
    """Nettoie les données de test (optionnel)"""
    print("\n🧹 Nettoyage des données de test...")
    tenant_id = "00000000-0000-0000-0000-000000000001"

    try:
        success = await supabase_client.delete_tenant_data(tenant_id)
        if success:
            print("   ✅ Données de test supprimées")
    except Exception as e:
        print(f"   ⚠️  Erreur nettoyage : {e}")


if __name__ == "__main__":
    print("\n🚀 Démarrage des tests Supabase...\n")

    # Vérifier les variables d'environnement
    if not os.getenv("SUPABASE_URL"):
        print("❌ ERREUR: SUPABASE_URL non défini dans .env")
        print("   Ajoutez: SUPABASE_URL=https://your-project.supabase.co")
        sys.exit(1)

    if not os.getenv("SUPABASE_SERVICE_KEY"):
        print("❌ ERREUR: SUPABASE_SERVICE_KEY non défini dans .env")
        print("   Ajoutez: SUPABASE_SERVICE_KEY=your-service-key")
        sys.exit(1)

    # Lancer les tests
    try:
        asyncio.run(test_supabase())

        # Demander si on veut nettoyer
        print("\n❓ Voulez-vous supprimer les données de test ? (y/N): ", end="")
        response = input().strip().lower()

        if response == 'y':
            asyncio.run(cleanup_test_data())
        else:
            print("   ℹ️  Données de test conservées")

    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrompus par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ ERREUR INATTENDUE : {e}")
        import traceback
        traceback.print_exc()
