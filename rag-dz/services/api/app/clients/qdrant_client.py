from qdrant_client import QdrantClient
import os

QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
client = QdrantClient(url=QDRANT_URL)

def create_collection(name: str, vector_size: int = 768):
    try:
        from qdrant_client.http import models as qm
        client.create_collection(
            collection_name=name,
            vectors_config=qm.VectorParams(size=vector_size, distance=qm.Distance.COSINE)
        )
        return True
    except Exception as e:
        print(f"Collection {name} may already exist: {e}")
        return False

def search_vectors(collection: str, vector: list[float], limit: int = 10):
    try:
        results = client.search(
            collection_name=collection,
            query_vector=vector,
            limit=limit,
            score_threshold=0.3
        )
        return [{"id": str(r.id), "score": r.score, "payload": r.payload} for r in results]
    except Exception as e:
        print(f"Search error: {e}")
        return []
