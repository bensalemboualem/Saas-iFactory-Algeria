from fastapi import APIRouter, Request
from ..clients.embeddings import embed_queries
from ..clients.qdrant_client import create_collection

router = APIRouter()

@router.post("/test/embed")
async def test_embed(request: Request):
    tenant = request.state.tenant
    test_queries = ["Hello world", "Bonjour le monde", "مرحبا بالعالم"]
    embeddings = embed_queries(test_queries)
    
    # Créer collection de test
    collection_name = f"test_{tenant['id']}"
    create_collection(collection_name)
    
    return {
        "tenant": tenant["name"],
        "queries": test_queries,
        "embeddings_count": len(embeddings),
        "vector_size": len(embeddings[0]) if embeddings else 0,
        "collection_created": collection_name
    }
