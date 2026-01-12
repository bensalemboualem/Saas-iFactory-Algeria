"""
CRM IA - Gestion de Dossiers Clients pour iaFactory Algeria
============================================================
Backend API for CRM with PostgreSQL persistence and AI automation.

Auteur: iaFactory Algeria
Date: Décembre 2025
"""

import os
import uuid
import asyncio
import httpx
from datetime import datetime
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import logging
import json
import aiofiles

# --- Local Imports ---
import models, crud
from database import SessionLocal, engine, get_db, Base
from schemas import (
    CaseStatus, CasePriority, CaseCategory, NoteAuthor,
    ClientCreate, Client, ClientUpdate, AddFieldRequest,
    CaseCreate, Case, CaseUpdate,
    NoteCreate, Note
)

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("crm-ia")

# ============================================================================
# CONFIGURATION
# ============================================================================

# URLs des services internes
LEGAL_API_URL = os.getenv("LEGAL_API_URL", "http://iaf-dz-legal-prod:8200")
FISCAL_API_URL = os.getenv("FISCAL_API_URL", "http://iaf-dz-fiscal-prod:8201")
RAG_API_URL = os.getenv("RAG_API_URL", "http://iaf-rag-api-prod:8180")
PARK_API_URL = os.getenv("PARK_API_URL", "http://iaf-park-prod:8195")
BILLING_API_URL = os.getenv("BILLING_API_URL", "http://iaf-billing-prod:8207")

# Stockage fichiers
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads") # Relative path now
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Crédits par analyse IA
CRM_AI_ANALYSIS_CREDITS = int(os.getenv("CRM_AI_ANALYSIS_CREDITS", "8"))

# --- Files (local schema, not in schemas.py) ---
class FileInfo(BaseModel):
    id: str
    case_id: str
    file_name: str
    file_url: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    uploaded_at: datetime

    class Config:
        orm_mode = True


# --- AI Analysis ---
class AIAnalysisResponse(BaseModel):
    success: bool = True
    summary: str
    action_items: List[str] = []
    risks: List[str] = []
    recommended_docs: List[str] = []
    next_steps: List[str] = []
    legal_insights: Optional[str] = None
    fiscal_insights: Optional[str] = None
    references: List[Dict[str, str]] = []
    analysis_timestamp: datetime
    credits_used: int = 0


# ============================================================================
# APPLICATION FASTAPI
# ============================================================================

app = FastAPI(
    title="CRM IA - iaFactory Algeria",
    description="Mini CRM avec automatisation IA pour gestion de dossiers clients",
    version="1.0.0",
    on_startup=[lambda: Base.metadata.create_all(bind=engine)] # Create tables on startup
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# ENDPOINTS - HEALTH
# ============================================================================

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        db.execute("SELECT 1") # Test DB connection
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {
        "status": "healthy",
        "service": "crm-ia",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "stats": {
            "clients": db.query(models.Client).count(),
            "cases": db.query(models.Case).count(),
            "notes": db.query(models.Note).count(),
            "files": db.query(models.File).count(),
            "db_status": db_status
        }
    }

# ============================================================================
# ENDPOINTS - CLIENTS
# ============================================================================

@app.post("/api/crm/client", response_model=Client)
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    """Créer un nouveau client"""
    db_client = crud.create_client(db=db, client=client)
    logger.info(f"Client créé: {db_client.id} - {db_client.first_name}")
    return db_client

@app.get("/api/crm/clients", response_model=List[Client])
async def list_clients(
    db: Session = Depends(get_db),
    skip: int = 0, limit: int = 100,
    client_type: Optional[str] = None,  # LIBRE maintenant
    search: Optional[str] = None
):
    """Lister tous les clients"""
    clients = crud.get_clients(db, skip=skip, limit=limit, client_type=client_type, search=search)

    # Populate cases_count et parser extra_fields
    for client in clients:
        client.cases_count = db.query(models.Case).filter(models.Case.client_id == client.id).count()
        if client.extra_fields and isinstance(client.extra_fields, str):
            client.extra_fields = json.loads(client.extra_fields)

    return clients

@app.get("/api/crm/client/{client_id}", response_model=Client)
async def get_client(client_id: str, db: Session = Depends(get_db)):
    """Obtenir un client par ID"""
    db_client = crud.get_client(db, client_id=client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    db_client.cases_count = db.query(models.Case).filter(models.Case.client_id == db_client.id).count()
    if db_client.extra_fields and isinstance(db_client.extra_fields, str):
        db_client.extra_fields = json.loads(db_client.extra_fields)
    return db_client

@app.patch("/api/crm/client/{client_id}", response_model=Client)
async def update_client(client_id: str, update: ClientUpdate, db: Session = Depends(get_db)):
    """Mettre à jour un client"""
    db_client = crud.update_client(db, client_id=client_id, client_update=update)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    logger.info(f"Client mis à jour: {client_id}")
    if db_client.extra_fields and isinstance(db_client.extra_fields, str):
        db_client.extra_fields = json.loads(db_client.extra_fields)
    return db_client

@app.post("/api/crm/client/{client_id}/field", response_model=Client)
async def add_client_field(client_id: str, field: AddFieldRequest, db: Session = Depends(get_db)):
    """
    Ajouter un champ personnalisé à un client (le bouton +)

    Exemple: {"field_name": "nif", "field_value": "123456789"}
    """
    db_client = crud.add_client_field(db, client_id=client_id, field_name=field.field_name, field_value=field.field_value)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    logger.info(f"Champ ajouté au client {client_id}: {field.field_name}")
    if db_client.extra_fields and isinstance(db_client.extra_fields, str):
        db_client.extra_fields = json.loads(db_client.extra_fields)
    return db_client

@app.delete("/api/crm/client/{client_id}/field/{field_name}")
async def delete_client_field(client_id: str, field_name: str, db: Session = Depends(get_db)):
    """Supprimer un champ personnalisé d'un client"""
    db_client = crud.delete_client_field(db, client_id=client_id, field_name=field_name)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    logger.info(f"Champ supprimé du client {client_id}: {field_name}")
    return {"success": True, "message": f"Champ {field_name} supprimé"}

@app.delete("/api/crm/client/{client_id}")
async def delete_client(client_id: str, db: Session = Depends(get_db)):
    """Supprimer un client"""
    db_client = crud.delete_client(db, client_id=client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    logger.info(f"Client supprimé: {client_id}")
    return {"success": True, "message": "Client supprimé"}


# ============================================================================
# IMPORT CSV/EXCEL - Clients
# ============================================================================

@app.post("/api/crm/clients/import")
async def import_clients(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Importer des clients depuis un fichier CSV ou Excel (.xlsx)

    Colonnes reconnues:
    - first_name / prenom (obligatoire)
    - last_name / nom
    - company_name / raison_sociale / societe
    - email
    - phone / telephone / tel
    - client_type / type (texte libre: PME, Freelance, etc.)
    - activity_sector / secteur (texte libre)
    - address / adresse
    - notes

    Toutes les autres colonnes sont automatiquement stockées dans extra_fields
    (ex: NIF, NIS, RC, capital, date_creation, etc.)
    """
    import pandas as pd
    import io

    # Vérifier le type de fichier
    filename = file.filename.lower()
    if not (filename.endswith('.csv') or filename.endswith('.xlsx') or filename.endswith('.xls')):
        raise HTTPException(status_code=400, detail="Format non supporté. Utilisez CSV ou Excel (.xlsx)")

    # Lire le contenu du fichier
    content = await file.read()

    try:
        # Parser selon le type
        if filename.endswith('.csv'):
            # Essayer différents encodages
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    df = pd.read_csv(io.BytesIO(content), encoding=encoding)
                    break
                except:
                    continue
            else:
                raise HTTPException(status_code=400, detail="Impossible de lire le fichier CSV")
        else:
            df = pd.read_excel(io.BytesIO(content))

        # Normaliser les noms de colonnes (minuscules, sans espaces)
        df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')

        # Mapping des colonnes connues
        column_mapping = {
            'prenom': 'first_name',
            'prénom': 'first_name',
            'nom': 'last_name',
            'raison_sociale': 'company_name',
            'societe': 'company_name',
            'société': 'company_name',
            'telephone': 'phone',
            'tel': 'phone',
            'type': 'client_type',
            'secteur': 'activity_sector',
            'adresse': 'address'
        }
        df.rename(columns=column_mapping, inplace=True)

        # Vérifier colonne obligatoire (first_name ou on parse 'name' si présent)
        if 'first_name' not in df.columns:
            # Fallback: si colonne 'name' existe, l'utiliser comme first_name
            if 'name' in df.columns:
                df['first_name'] = df['name']
            else:
                raise HTTPException(status_code=400, detail="Colonne 'first_name' ou 'prenom' obligatoire")

        # Colonnes standard du CRM
        standard_columns = {'first_name', 'last_name', 'company_name', 'name', 'email', 'phone', 'client_type', 'activity_sector', 'address', 'notes'}

        # Importer les clients
        imported = 0
        errors = []
        extra_columns_found = set()

        for idx, row in df.iterrows():
            try:
                first_name = str(row.get('first_name', '')).strip()
                if not first_name or first_name == 'nan':
                    continue

                # client_type est maintenant du texte libre
                client_type = str(row.get('client_type', '')).strip() if pd.notna(row.get('client_type')) else None

                # Collecter les colonnes supplémentaires
                extra_fields = {}
                for col in df.columns:
                    if col not in standard_columns and pd.notna(row.get(col)):
                        value = row.get(col)
                        # Convertir en string si nécessaire
                        if pd.notna(value):
                            extra_fields[col] = str(value).strip() if not isinstance(value, (int, float)) else value
                            extra_columns_found.add(col)

                # Créer le client
                client_data = ClientCreate(
                    first_name=first_name,
                    last_name=str(row.get('last_name', '')).strip() if pd.notna(row.get('last_name')) else None,
                    company_name=str(row.get('company_name', '')).strip() if pd.notna(row.get('company_name')) else None,
                    email=str(row.get('email', '')).strip() if pd.notna(row.get('email')) else None,
                    phone=str(row.get('phone', '')).strip() if pd.notna(row.get('phone')) else None,
                    client_type=client_type,
                    activity_sector=str(row.get('activity_sector', '')).strip() if pd.notna(row.get('activity_sector')) else None,
                    address=str(row.get('address', '')).strip() if pd.notna(row.get('address')) else None,
                    notes=str(row.get('notes', '')).strip() if pd.notna(row.get('notes')) else None,
                    extra_fields=extra_fields if extra_fields else None
                )

                crud.create_client(db=db, client=client_data)
                imported += 1

            except Exception as e:
                errors.append(f"Ligne {idx + 2}: {str(e)}")

        logger.info(f"Import terminé: {imported} clients importés, colonnes extra: {list(extra_columns_found)}")

        return {
            "success": True,
            "imported": imported,
            "total_rows": len(df),
            "extra_columns": list(extra_columns_found),  # Colonnes personnalisées détectées
            "errors": errors[:10] if errors else []
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur import: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'import: {str(e)}")


# ============================================================================
# ENDPOINTS - CASES (DOSSIERS)
# ============================================================================

@app.post("/api/crm/case", response_model=Case)
async def create_case(case: CaseCreate, db: Session = Depends(get_db)):
    """Créer un nouveau dossier"""
    client = crud.get_client(db, client_id=case.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    
    db_case = crud.create_case(db=db, case=case)
    logger.info(f"Dossier créé: {db_case.id} - {db_case.title}")
    return db_case

@app.get("/api/crm/cases", response_model=List[Case])
async def list_cases(
    db: Session = Depends(get_db),
    client_id: Optional[str] = None,
    status: Optional[CaseStatus] = None,
    category: Optional[CaseCategory] = None,
    priority: Optional[CasePriority] = None,
    skip: int = 0, limit: int = 100
):
    """Lister les dossiers"""
    cases = crud.get_cases(db, client_id=client_id, status=status, category=category, priority=priority, skip=skip, limit=limit)
    
    for case in cases:
        case.notes_count = db.query(models.Note).filter(models.Note.case_id == case.id).count()
        case.files_count = db.query(models.File).filter(models.File.case_id == case.id).count()
        client = crud.get_client(db, client_id=case.client_id)
        if client:
            # Construire le nom complet: prénom + nom
            case.client_name = f"{client.first_name} {client.last_name or ''}".strip()

    return cases

@app.get("/api/crm/case/{case_id}", response_model=Case)
async def get_case(case_id: str, db: Session = Depends(get_db)):
    """Obtenir un dossier par ID"""
    db_case = crud.get_case(db, case_id=case_id)
    if not db_case:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    
    db_case.notes_count = db.query(models.Note).filter(models.Note.case_id == db_case.id).count()
    db_case.files_count = db.query(models.File).filter(models.File.case_id == db_case.id).count()
    client = crud.get_client(db, client_id=db_case.client_id)
    if client:
        db_case.client_name = f"{client.first_name} {client.last_name or ''}".strip()

    return db_case

@app.patch("/api/crm/case/{case_id}", response_model=Case)
async def update_case(case_id: str, update: CaseUpdate, db: Session = Depends(get_db)):
    """Mettre à jour un dossier"""
    db_case = crud.update_case(db, case_id=case_id, case_update=update)
    if not db_case:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    
    logger.info(f"Dossier mis à jour: {case_id}")
    return db_case

@app.delete("/api/crm/case/{case_id}")
async def delete_case(case_id: str, db: Session = Depends(get_db)):
    """Supprimer un dossier"""
    db_case = crud.delete_case(db, case_id=case_id)
    if not db_case:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    
    logger.info(f"Dossier supprimé: {case_id}")
    return {"success": True, "message": "Dossier supprimé"}

# ============================================================================
# ENDPOINTS - NOTES
# ============================================================================

@app.post("/api/crm/case/{case_id}/note", response_model=Note)
async def create_note(case_id: str, note: NoteCreate, db: Session = Depends(get_db)):
    """Ajouter une note à un dossier"""
    if not crud.get_case(db, case_id=case_id):
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    
    db_note = crud.create_note(db=db, note=note, case_id=case_id)
    logger.info(f"Note créée pour le dossier {case_id}: {db_note.id}")
    
    # Update case's updated_at timestamp
    db_case = crud.get_case(db, case_id=case_id)
    if db_case:
        db_case.updated_at = datetime.utcnow()
        db.add(db_case)
        db.commit()
    
    return db_note

@app.get("/api/crm/case/{case_id}/notes", response_model=List[Note])
async def list_notes(case_id: str, db: Session = Depends(get_db)):
    """Lister les notes d'un dossier"""
    if not crud.get_case(db, case_id=case_id):
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    
    notes = crud.get_notes_for_case(db, case_id=case_id)
    return notes

# ============================================================================
# ENDPOINTS - FILES
# ============================================================================

@app.post("/api/crm/case/{case_id}/file", response_model=FileInfo)
async def upload_file(case_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Uploader un fichier sur un dossier"""
    if not crud.get_case(db, case_id=case_id):
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    
    file_id = str(uuid.uuid4())
    
    # Déterminer le type de fichier
    file_ext = file.filename.split(".")[-1].lower() if "." in file.filename else "unknown"
    file_type_map = {
        "pdf": "pdf", "doc": "doc", "docx": "doc", "xls": "excel", "xlsx": "excel",
        "jpg": "image", "jpeg": "image", "png": "image", "gif": "image", "txt": "text"
    }
    file_type = file_type_map.get(file_ext, "other")
    
    # Sauvegarder le fichier
    safe_filename = f"{file_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while content := await file.read(1024):
                await f.write(content)
    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise HTTPException(status_code=500, detail="Échec de la sauvegarde du fichier.")

    file_size = os.path.getsize(file_path) # Get actual size
    
    db_file = crud.create_file(db, file_name=file.filename, file_url=f"/api/crm/files/{file_id}", file_type=file_type, file_size=file_size, case_id=case_id)
    
    # Update case's updated_at timestamp
    db_case = crud.get_case(db, case_id=case_id)
    if db_case:
        db_case.updated_at = datetime.utcnow()
        db.add(db_case)
        db.commit()

    logger.info(f"Fichier uploadé: {db_file.file_name} sur dossier {case_id}")
    
    return FileInfo.from_orm(db_file)

@app.get("/api/crm/case/{case_id}/files", response_model=List[FileInfo])
async def list_files(case_id: str, db: Session = Depends(get_db)):
    """Lister les fichiers d'un dossier"""
    if not crud.get_case(db, case_id=case_id):
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    
    files = crud.get_files_for_case(db, case_id=case_id)
    return [FileInfo.from_orm(f) for f in files]


@app.get("/api/crm/files/{file_id}")
async def download_file(file_id: str, db: Session = Depends(get_db)):
    """Télécharger un fichier"""
    file_info = crud.get_file(db, file_id=file_id)
    if not file_info:
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    file_path = os.path.join(UPLOAD_DIR, f"{file_info.id}_{file_info.file_name}") # Reconstruct path
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé sur le disque")
    
    return FileResponse(path=file_path, filename=file_info.file_name)


# ============================================================================
# ENDPOINTS - AI ANALYSIS
# ============================================================================

async def call_legal_api(context: str, category: str) -> Dict[str, Any]:
    """Appelle DZ-LegalAssistant"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{LEGAL_API_URL}/api/dz-legal/answer",
                json={"question": context, "category": category, "include_references": True}
            )
            if response.status_code == 200:
                return response.json()
    except Exception as e:
        logger.error(f"Legal API error: {e}")
    return {}

async def call_fiscal_api(context: str) -> Dict[str, Any]:
    """Appelle DZ-FiscalAssistant"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{FISCAL_API_URL}/api/dz-fiscal/simulate",
                json={"question_context": context, "regime_fiscal": "microentreprise"}
            )
            if response.status_code == 200:
                return response.json()
    except Exception as e:
        logger.error(f"Fiscal API error: {e}")
    return {}

async def call_rag_api(query: str) -> Dict[str, Any]:
    """Appelle RAG DZ"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{RAG_API_URL}/api/rag/query",
                json={"query": query, "top_k": 5}
            )
            if response.status_code == 200:
                return response.json()
    except Exception as e:
        logger.error(f"RAG API error: {e}")
    return {}

@app.post("/api/crm/case/{case_id}/ai-analyze", response_model=AIAnalysisResponse)
async def ai_analyze_case(case_id: str, user_id: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Analyser un dossier avec l'IA
    """
    db_case = crud.get_case(db, case_id=case_id)
    if not db_case:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    
    db_client = crud.get_client(db, client_id=db_case.client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client du dossier non trouvé")
    
    # Construire le contexte
    notes = crud.get_notes_for_case(db, case_id=case_id)
    notes_text = "\n".join([f"- {n.content}" for n in notes[:10]])
    client_full_name = f"{db_client.first_name} {db_client.last_name or ''}".strip()

    context = f"""
Dossier: {db_case.title}
Catégorie: {db_case.category}
Description: {db_case.description}
Client: {client_full_name} ({db_client.client_type or 'Non spécifié'})
Secteur: {db_client.activity_sector or 'Non spécifié'}
Notes précédentes:
{notes_text}
"""
    
    logger.info(f"Analyse IA du dossier {case_id}")
    
    tasks = [call_rag_api(context)]
    
    if db_case.category in [CaseCategory.JURIDIQUE, CaseCategory.ADMINISTRATIF]:
        tasks.append(call_legal_api(context, "droit_des_affaires"))
    if db_case.category in [CaseCategory.FISCAL, CaseCategory.BUSINESS]:
        tasks.append(call_fiscal_api(context))
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    rag_data = results[0] if not isinstance(results[0], Exception) else {}
    legal_data = results[1] if len(results) > 1 and not isinstance(results[1], Exception) else {}
    fiscal_data = results[2] if len(results) > 2 and not isinstance(results[2], Exception) else {}
    
    # Générer l'analyse - Simplifié pour l'exemple
    summary = f"Analyse IA pour le dossier {db_case.title} du client {client_full_name}."
    action_items = ["Action 1", "Action 2"]
    risks = ["Risque 1"]
    recommended_docs = ["Doc A", "Doc B"]
    next_steps = ["Étape suivante 1"]
    
    # Créer une note IA automatique
    ai_note_content = f"""
🤖 **Analyse IA automatique**

**Résumé :**
{summary[:500]}

**Actions suggérées :**
{chr(10).join(['• ' + a for a in action_items])}

**Risques identifiés :**
{chr(10).join(['⚠️ ' + r for r in risks])}

---
_Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}_
"""
    
    db_note = crud.create_note(db, NoteCreate(content=ai_note_content, author_type=NoteAuthor.AI), case_id=case_id)
    
    # Update case's last_ai_update and updated_at timestamp
    db_case.last_ai_update = datetime.utcnow()
    db_case.updated_at = datetime.utcnow()
    db.add(db_case)
    db.commit()
    
    # Références
    references = []
    rag_sources = rag_data.get("sources", rag_data.get("documents", []))
    for source in rag_sources[:3]:
        references.append({
            "title": source.get("title", "Document"),
            "source": source.get("source", "Base documentaire")
        })
    
    return AIAnalysisResponse(
        success=True,
        summary=summary,
        action_items=action_items,
        risks=risks,
        recommended_docs=recommended_docs,
        next_steps=next_steps,
        analysis_timestamp=datetime.utcnow(),
        credits_used=CRM_AI_ANALYSIS_CREDITS,
        references=references
    )

# ============================================================================
# ENDPOINTS - STATS
# ============================================================================

@app.get("/api/crm/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Obtenir les statistiques du CRM"""
    return {
        "total_clients": db.query(models.Client).count(),
        "total_cases": db.query(models.Case).count(),
        "total_notes": db.query(models.Note).count(),
        "total_files": db.query(models.File).count(),
        # Further stats can be calculated here
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8212)