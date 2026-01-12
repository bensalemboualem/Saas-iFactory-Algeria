from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time
import uuid
import logging

from ..clients.embeddings import embed_documents
from ..clients.qdrant_client import create_collection, client as qdrant_client
from ..clients.document_parser import DocumentParser
from ..clients.hybrid_search import HybridSearchEngine
from qdrant_client.http import models as qm

logger = logging.getLogger(__name__)
router = APIRouter()
search_engine = HybridSearchEngine()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), req: Request = None):
    """Upload et indexation de document avec parsing avancé"""
    tenant = req.state.tenant
    collection_name = f"docs_{tenant['id']}"
    
    if not file.filename:
        raise HTTPException(400, "Nom de fichier requis")
    
    allowed_extensions = {'pdf', 'docx', 'txt', 'text'}
    file_extension = file.filename.split('.')[-1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(400, f"Type de fichier non supporté. Autorisés: {', '.join(allowed_extensions)}")
    
    try:
        file_content = await file.read()
        if len(file_content) == 0:
            raise HTTPException(400, "Fichier vide")
        
        if len(file_content) > 10 * 1024 * 1024:
            raise HTTPException(400, "Fichier trop volumineux (max 10MB)")
        
    except Exception as e:
        logger.error(f"File reading error: {e}")
        raise HTTPException(500, "Erreur lors de la lecture du fichier")
    
    try:
        parsed_doc = DocumentParser.parse_file(file.filename, file_content)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        logger.error(f"Document parsing error: {e}")
        raise HTTPException(500, "Erreur lors du parsing du document")
    
    create_collection(collection_name)
    
    documents = []
    chunk_metadatas = []
    
    for i, chunk in enumerate(parsed_doc['chunks']):
        doc_id = str(uuid.uuid4())
        doc_title = f"{parsed_doc['filename']} - Partie {i+1}"
        
        chunk_metadatas.append({
            'id': doc_id,
            'title': doc_title,
            'text': chunk,
            'language': parsed_doc['language'],
            'tenant_id': tenant['id'],
            'filename': parsed_doc['filename'],
            'extension': parsed_doc['extension'],
            'chunk_index': i,
            'created_at': time.time()
        })
    
    if not chunk_metadatas:
        raise HTTPException(400, "Aucun contenu textuel extractible du fichier")
    
    try:
        texts = [meta['text'] for meta in chunk_metadatas]
        embeddings = embed_documents(texts)
        
        if len(embeddings) != len(chunk_metadatas):
            raise HTTPException(500, "Erreur de génération des embeddings")
            
    except Exception as e:
        logger.error(f"Embedding generation error: {e}")
        raise HTTPException(500, "Erreur lors de la génération des embeddings")
    
    try:
        points = []
        for embedding, metadata in zip(embeddings, chunk_metadatas):
            points.append(qm.PointStruct(
                id=metadata['id'],
                vector=embedding,
                payload=metadata
            ))
        
        qdrant_client.upsert(collection_name=collection_name, points=points)
        
    except Exception as e:
        logger.error(f"Qdrant indexing error: {e}")
        raise HTTPException(500, "Erreur lors de l'indexation vectorielle")
    
    try:
        meili_docs = [
            {
                'id': meta['id'],
                'title': meta['title'],
                'text': meta['text'][:2000],
                'language': meta['language'],
                'tenant_id': meta['tenant_id'],
                'filename': meta['filename'],
                'created_at': meta['created_at']
            }
            for meta in chunk_metadatas
        ]
        
        search_engine.add_to_meilisearch(collection_name, meili_docs)
        
    except Exception as e:
        logger.warning(f"Meilisearch indexing warning: {e}")
    
    return {
        'success': True,
        'file_name': file.filename,
        'file_size_bytes': len(file_content),
        'language_detected': parsed_doc['language'],
        'total_chunks': len(parsed_doc['chunks']),
        'documents_indexed': len(chunk_metadatas),
        'collection': collection_name
    }
