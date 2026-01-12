from fastapi import APIRouter, UploadFile, File, Request
import uuid
from ..clients.embeddings import embed_documents
from ..clients.qdrant_client import create_collection, client as qdrant_client
from qdrant_client.http import models as qm

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), req: Request = None):
    tenant = req.state.tenant
    collection_name = f"docs_{tenant['id']}"
    
    create_collection(collection_name)
    
    # Lire contenu fichier
    content = await file.read()
    text_content = content.decode('utf-8', errors='ignore')
    
    # Chunking plus flexible - essayer plusieurs séparateurs
    chunks = []
    
    # Essayer d'abord par double retour
    if '\n\n' in text_content:
        chunks = [chunk.strip() for chunk in text_content.split('\n\n') if chunk.strip()]
    # Sinon par retour simple
    elif '\n' in text_content:
        chunks = [chunk.strip() for chunk in text_content.split('\n') if chunk.strip()]
    # Sinon prendre tout le contenu
    else:
        chunks = [text_content.strip()] if text_content.strip() else []
    
    # Filtrer chunks trop courts
    chunks = [chunk for chunk in chunks if len(chunk) > 20]  # Seuil réduit
    
    if not chunks:
        return {"error": "No valid content found in file", "raw_content": text_content[:200]}
    
    # Générer embeddings
    embeddings = embed_documents(chunks)
    
    # Créer points Qdrant
    points = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        points.append(qm.PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "title": f"{file.filename} - Part {i+1}",
                "text": chunk,
                "tenant_id": tenant["id"]
            }
        ))
    
    # Insérer dans Qdrant
    qdrant_client.upsert(collection_name=collection_name, points=points)
    
    return {
        "success": True,
        "file_name": file.filename,
        "chunks_created": len(chunks),
        "collection": collection_name,
        "chunks": chunks  # Debug info
    }
