"""
CRM IA - Gestion de Dossiers Clients pour iaFactory Algeria
============================================================
Mini CRM intégré avec automatisation IA pour cabinets, freelances, PME.

Auteur: iaFactory Algeria
Date: Novembre 2025
"""

import os
import uuid
import asyncio
import httpx
from datetime import datetime
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import logging
import json
import aiofiles

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
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/app/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Crédits par analyse IA
CRM_AI_ANALYSIS_CREDITS = int(os.getenv("CRM_AI_ANALYSIS_CREDITS", "8"))

# ============================================================================
# ENUMS
# ============================================================================

class ClientType(str, Enum):
    FREELANCE = "freelance"
    PME = "pme"
    PARTICULIER = "particulier"
    ENTREPRISE = "entreprise"
    CABINET = "cabinet"

class CaseStatus(str, Enum):
    OUVERT = "ouvert"
    EN_COURS = "en_cours"
    EN_ATTENTE = "en_attente"
    FERME = "ferme"

class CasePriority(str, Enum):
    BASSE = "basse"
    MOYENNE = "moyenne"
    HAUTE = "haute"
    URGENTE = "urgente"

class CaseCategory(str, Enum):
    JURIDIQUE = "juridique"
    FISCAL = "fiscal"
    ADMINISTRATIF = "administratif"
    BUSINESS = "business"
    RH = "rh"
    AUTRE = "autre"

class NoteAuthor(str, Enum):
    USER = "user"
    AI = "ai"

# ============================================================================
# MODÈLES DE DONNÉES
# ============================================================================

# --- Clients ---
class ClientCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: Optional[str] = None
    phone: Optional[str] = None
    type: ClientType = ClientType.PME
    activity_sector: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None

class Client(ClientCreate):
    id: str
    user_id: Optional[str] = None
    created_at: str
    updated_at: str
    cases_count: int = 0

# --- Cases (Dossiers) ---
class CaseCreate(BaseModel):
    client_id: str
    title: str = Field(..., min_length=3)
    description: Optional[str] = None
    status: CaseStatus = CaseStatus.OUVERT
    priority: CasePriority = CasePriority.MOYENNE
    category: CaseCategory = CaseCategory.AUTRE
    tags: List[str] = []

class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CaseStatus] = None
    priority: Optional[CasePriority] = None
    category: Optional[CaseCategory] = None
    tags: Optional[List[str]] = None

class Case(CaseCreate):
    id: str
    created_at: str
    updated_at: str
    last_ai_update: Optional[str] = None
    notes_count: int = 0
    files_count: int = 0
    client_name: Optional[str] = None

# --- Notes ---
class NoteCreate(BaseModel):
    content: str = Field(..., min_length=1)
    author_type: NoteAuthor = NoteAuthor.USER

class Note(NoteCreate):
    id: str
    case_id: str
    created_at: str

# --- Files ---
class FileInfo(BaseModel):
    id: str
    case_id: str
    file_name: str
    file_url: str
    file_type: str
    file_size: int
    uploaded_at: str

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
    analysis_timestamp: str
    credits_used: int = 0

# ============================================================================
# STORAGE (In-Memory pour démo - remplacer par PostgreSQL en prod)
# ============================================================================

# Stockage en mémoire (à remplacer par DB)
clients_db: Dict[str, Dict] = {}
cases_db: Dict[str, Dict] = {}
notes_db: Dict[str, Dict] = {}
files_db: Dict[str, Dict] = {}

def generate_id() -> str:
    return str(uuid.uuid4())[:12]

# ============================================================================
# APPLICATION FASTAPI
# ============================================================================

app = FastAPI(
    title="CRM IA - iaFactory Algeria",
    description="Mini CRM avec automatisation IA pour gestion de dossiers clients",
    version="1.0.0"
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
async def health_check():
    return {
        "status": "healthy",
        "service": "crm-ia",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "stats": {
            "clients": len(clients_db),
            "cases": len(cases_db),
            "notes": len(notes_db),
            "files": len(files_db)
        }
    }

# ============================================================================
# ENDPOINTS - CLIENTS
# ============================================================================

@app.post("/api/crm/client", response_model=Client)
async def create_client(client: ClientCreate):
    """Créer un nouveau client"""
    client_id = generate_id()
    now = datetime.now().isoformat()
    
    client_data = {
        **client.dict(),
        "id": client_id,
        "user_id": None,
        "created_at": now,
        "updated_at": now,
        "cases_count": 0
    }
    
    clients_db[client_id] = client_data
    logger.info(f"Client créé: {client_id} - {client.name}")
    
    return Client(**client_data)

@app.get("/api/crm/clients", response_model=List[Client])
async def list_clients(
    type: Optional[ClientType] = None,
    search: Optional[str] = None
):
    """Lister tous les clients"""
    clients = list(clients_db.values())
    
    if type:
        clients = [c for c in clients if c.get("type") == type]
    
    if search:
        search_lower = search.lower()
        clients = [c for c in clients if 
                   search_lower in c.get("name", "").lower() or 
                   search_lower in c.get("email", "").lower()]
    
    # Compter les dossiers par client
    for client in clients:
        client["cases_count"] = len([
            c for c in cases_db.values() 
            if c.get("client_id") == client["id"]
        ])
    
    return [Client(**c) for c in sorted(clients, key=lambda x: x["created_at"], reverse=True)]

@app.get("/api/crm/client/{client_id}", response_model=Client)
async def get_client(client_id: str):
    """Obtenir un client par ID"""
    if client_id not in clients_db:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    
    client = clients_db[client_id]
    client["cases_count"] = len([
        c for c in cases_db.values() 
        if c.get("client_id") == client_id
    ])
    
    return Client(**client)

@app.delete("/api/crm/client/{client_id}")
async def delete_client(client_id: str):
    """Supprimer un client"""
    if client_id not in clients_db:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    
    # Supprimer les dossiers associés
    cases_to_delete = [cid for cid, c in cases_db.items() if c.get("client_id") == client_id]
    for case_id in cases_to_delete:
        # Supprimer notes et fichiers du dossier
        notes_to_delete = [nid for nid, n in notes_db.items() if n.get("case_id") == case_id]
        for nid in notes_to_delete:
            del notes_db[nid]
        files_to_delete = [fid for fid, f in files_db.items() if f.get("case_id") == case_id]
        for fid in files_to_delete:
            del files_db[fid]
        del cases_db[case_id]
    
    del clients_db[client_id]
    
    return {"success": True, "message": "Client supprimé"}

# ============================================================================
# ENDPOINTS - CASES (DOSSIERS)
# ============================================================================

@app.post("/api/crm/case", response_model=Case)
async def create_case(case: CaseCreate):
    """Créer un nouveau dossier"""
    if case.client_id not in clients_db:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    
    case_id = generate_id()
    now = datetime.now().isoformat()
    
    case_data = {
        **case.dict(),
        "id": case_id,
        "created_at": now,
        "updated_at": now,
        "last_ai_update": None,
        "notes_count": 0,
        "files_count": 0,
        "client_name": clients_db[case.client_id].get("name")
    }
    
    cases_db[case_id] = case_data
    logger.info(f"Dossier créé: {case_id} - {case.title}")
    
    return Case(**case_data)

@app.get("/api/crm/cases", response_model=List[Case])
async def list_cases(
    client_id: Optional[str] = None,
    status: Optional[CaseStatus] = None,
    category: Optional[CaseCategory] = None,
    priority: Optional[CasePriority] = None
):
    """Lister les dossiers"""
    cases = list(cases_db.values())
    
    if client_id:
        cases = [c for c in cases if c.get("client_id") == client_id]
    if status:
        cases = [c for c in cases if c.get("status") == status]
    if category:
        cases = [c for c in cases if c.get("category") == category]
    if priority:
        cases = [c for c in cases if c.get("priority") == priority]
    
    # Enrichir avec compteurs
    for case in cases:
        case["notes_count"] = len([n for n in notes_db.values() if n.get("case_id") == case["id"]])
        case["files_count"] = len([f for f in files_db.values() if f.get("case_id") == case["id"]])
        if case.get("client_id") in clients_db:
            case["client_name"] = clients_db[case["client_id"]].get("name")
    
    return [Case(**c) for c in sorted(cases, key=lambda x: x["updated_at"], reverse=True)]

@app.get("/api/crm/case/{case_id}", response_model=Case)
async def get_case(case_id: str):
    """Obtenir un dossier par ID"""
    if case_id not in cases_db:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    
    case = cases_db[case_id]
    case["notes_count"] = len([n for n in notes_db.values() if n.get("case_id") == case_id])
    case["files_count"] = len([f for f in files_db.values() if f.get("case_id") == case_id])
    if case.get("client_id") in clients_db:
        case["client_name"] = clients_db[case["client_id"]].get("name")
    
    return Case(**case)

@app.patch("/api/crm/case/{case_id}", response_model=Case)
async def update_case(case_id: str, update: CaseUpdate):
    """Mettre à jour un dossier"""
    if case_id not in cases_db:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    
    case = cases_db[case_id]
    update_data = update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        if value is not None:
            case[key] = value
    
    case["updated_at"] = datetime.now().isoformat()
    cases_db[case_id] = case
    
    return Case(**case)

@app.delete("/api/crm/case/{case_id}")
async def delete_case(case_id: str):
    """Supprimer un dossier"""
    if case_id not in cases_db:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    
    # Supprimer notes et fichiers
    notes_to_delete = [nid for nid, n in notes_db.items() if n.get("case_id") == case_id]
    for nid in notes_to_delete:
        del notes_db[nid]
    
    files_to_delete = [fid for fid, f in files_db.items() if f.get("case_id") == case_id]
    for fid in files_to_delete:
        del files_db[fid]
    
    del cases_db[case_id]
    
    return {"success": True, "message": "Dossier supprimé"}

# ============================================================================
# ENDPOINTS - NOTES
# ============================================================================

@app.post("/api/crm/case/{case_id}/note", response_model=Note)
async def create_note(case_id: str, note: NoteCreate):
    """Ajouter une note à un dossier"""
    if case_id not in cases_db:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    
    note_id = generate_id()
    now = datetime.now().isoformat()
    
    note_data = {
        **note.dict(),
        "id": note_id,
        "case_id": case_id,
        "created_at": now
    }
    
    notes_db[note_id] = note_data
    
    # Mettre à jour le dossier
    cases_db[case_id]["updated_at"] = now
    
    return Note(**note_data)

@app.get("/api/crm/case/{case_id}/notes", response_model=List[Note])
async def list_notes(case_id: str):
    """Lister les notes d'un dossier"""
    if case_id not in cases_db:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    
    notes = [n for n in notes_db.values() if n.get("case_id") == case_id]
    return [Note(**n) for n in sorted(notes, key=lambda x: x["created_at"], reverse=True)]

# ============================================================================
# ENDPOINTS - FILES
# ============================================================================

@app.post("/api/crm/case/{case_id}/file", response_model=FileInfo)
async def upload_file(case_id: str, file: UploadFile = File(...)):
    """Uploader un fichier sur un dossier"""
    if case_id not in cases_db:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    
    file_id = generate_id()
    now = datetime.now().isoformat()
    
    # Déterminer le type de fichier
    file_ext = file.filename.split(".")[-1].lower() if "." in file.filename else "unknown"
    file_type_map = {
        "pdf": "pdf",
        "doc": "doc", "docx": "doc",
        "xls": "excel", "xlsx": "excel",
        "jpg": "image", "jpeg": "image", "png": "image", "gif": "image",
        "txt": "text"
    }
    file_type = file_type_map.get(file_ext, "other")
    
    # Sauvegarder le fichier
    safe_filename = f"{file_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    file_data = {
        "id": file_id,
        "case_id": case_id,
        "file_name": file.filename,
        "file_url": f"/api/crm/files/{file_id}",
        "file_type": file_type,
        "file_size": len(content),
        "uploaded_at": now,
        "_path": file_path
    }
    
    files_db[file_id] = file_data
    
    # Mettre à jour le dossier
    cases_db[case_id]["updated_at"] = now
    
    logger.info(f"Fichier uploadé: {file.filename} sur dossier {case_id}")
    
    return FileInfo(**{k: v for k, v in file_data.items() if not k.startswith("_")})

@app.get("/api/crm/case/{case_id}/files", response_model=List[FileInfo])
async def list_files(case_id: str):
    """Lister les fichiers d'un dossier"""
    if case_id not in cases_db:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    
    files = [f for f in files_db.values() if f.get("case_id") == case_id]
    return [FileInfo(**{k: v for k, v in f.items() if not k.startswith("_")}) 
            for f in sorted(files, key=lambda x: x["uploaded_at"], reverse=True)]

@app.get("/api/crm/files/{file_id}")
async def download_file(file_id: str):
    """Télécharger un fichier"""
    if file_id not in files_db:
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    file_info = files_db[file_id]
    file_path = file_info.get("_path")
    
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé sur le disque")
    
    return FileResponse(file_path, filename=file_info["file_name"])

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
async def ai_analyze_case(case_id: str, user_id: Optional[str] = None):
    """
    Analyser un dossier avec l'IA
    
    Orchestre les appels vers Legal, Fiscal, RAG pour générer:
    - Un résumé
    - Des tâches à faire
    - Des risques identifiés
    - Des documents recommandés
    - Des prochaines étapes
    """
    if case_id not in cases_db:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    
    case = cases_db[case_id]
    client = clients_db.get(case.get("client_id"), {})
    
    # Construire le contexte
    notes = [n for n in notes_db.values() if n.get("case_id") == case_id]
    notes_text = "\n".join([f"- {n.get('content', '')}" for n in notes[:10]])
    
    context = f"""
Dossier: {case.get('title', '')}
Catégorie: {case.get('category', '')}
Description: {case.get('description', '')}
Client: {client.get('name', '')} ({client.get('type', '')})
Secteur: {client.get('activity_sector', '')}
Notes précédentes:
{notes_text}
"""
    
    logger.info(f"Analyse IA du dossier {case_id}")
    
    # Appeler les services en parallèle selon la catégorie
    tasks = [call_rag_api(context)]
    
    category = case.get("category", "autre")
    if category in ["juridique", "administratif"]:
        tasks.append(call_legal_api(context, "droit_des_affaires"))
    if category in ["fiscal", "business"]:
        tasks.append(call_fiscal_api(context))
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    rag_data = results[0] if not isinstance(results[0], Exception) else {}
    legal_data = results[1] if len(results) > 1 and not isinstance(results[1], Exception) else {}
    fiscal_data = results[2] if len(results) > 2 and not isinstance(results[2], Exception) else {}
    
    # Générer l'analyse
    summary = f"""
📋 **Analyse du dossier : {case.get('title', '')}**

**Client :** {client.get('name', 'Non spécifié')}
**Catégorie :** {category}
**Priorité :** {case.get('priority', 'moyenne')}

{legal_data.get('summary', legal_data.get('answer', '')) if legal_data else ''}
{fiscal_data.get('summary', '') if fiscal_data else ''}

Ce dossier nécessite une attention particulière selon les éléments collectés.
""".strip()
    
    # Actions suggérées selon la catégorie
    action_items = []
    if category == "juridique":
        action_items = [
            "Vérifier la conformité des documents légaux",
            "Consulter un avocat si nécessaire",
            "Préparer les pièces justificatives",
            "Respecter les délais légaux"
        ]
    elif category == "fiscal":
        action_items = [
            "Vérifier les obligations déclaratives",
            "Calculer les montants dus",
            "Préparer les justificatifs comptables",
            "Respecter les échéances fiscales"
        ]
    elif category == "administratif":
        action_items = [
            "Rassembler les documents requis",
            "Vérifier les formulaires à remplir",
            "Identifier les guichets concernés",
            "Planifier les rendez-vous"
        ]
    else:
        action_items = [
            "Analyser les besoins du client",
            "Identifier les prochaines étapes",
            "Planifier les actions prioritaires"
        ]
    
    # Risques
    risks = [
        "Délais à respecter impérativement",
        "Documents à fournir sous peine de rejet",
        "Vérifier les informations avant soumission"
    ]
    
    # Documents recommandés
    recommended_docs = []
    if category == "juridique":
        recommended_docs = ["Statuts", "Registre de commerce", "Contrats types"]
    elif category == "fiscal":
        recommended_docs = ["Déclaration G50", "Bilan comptable", "Relevés bancaires"]
    elif category == "administratif":
        recommended_docs = ["Pièce d'identité", "Justificatif de domicile", "Attestations"]
    
    # Next steps
    next_steps = [
        "Compléter les informations manquantes",
        "Valider avec le client",
        "Préparer les documents",
        "Soumettre le dossier"
    ]
    
    # Créer une note IA automatique
    ai_note_content = f"""🤖 **Analyse IA automatique**

**Résumé :**
{summary[:500]}

**Actions suggérées :**
{chr(10).join(['• ' + a for a in action_items])}

**Risques identifiés :**
{chr(10).join(['⚠️ ' + r for r in risks])}

---
_Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}_
"""
    
    note_id = generate_id()
    now = datetime.now().isoformat()
    
    notes_db[note_id] = {
        "id": note_id,
        "case_id": case_id,
        "content": ai_note_content,
        "author_type": "ai",
        "created_at": now
    }
    
    # Mettre à jour le dossier
    cases_db[case_id]["last_ai_update"] = now
    cases_db[case_id]["updated_at"] = now
    
    # Références
    references = []
    rag_sources = rag_data.get("sources", rag_data.get("documents", []))
    for source in rag_sources[:3]:
        references.append({
            "title": source.get("title", "Document"),
            "source": source.get("source", "Base documentaire DZ")
        })
    
    return AIAnalysisResponse(
        success=True,
        summary=summary,
        action_items=action_items,
        risks=risks,
        recommended_docs=recommended_docs,
        next_steps=next_steps,
        legal_insights=legal_data.get("summary", legal_data.get("answer")) if legal_data else None,
        fiscal_insights=fiscal_data.get("summary") if fiscal_data else None,
        references=references,
        analysis_timestamp=now,
        credits_used=CRM_AI_ANALYSIS_CREDITS
    )

# ============================================================================
# ENDPOINTS - STATS
# ============================================================================

@app.get("/api/crm/stats")
async def get_stats():
    """Obtenir les statistiques du CRM"""
    cases_list = list(cases_db.values())
    
    # Stats par statut
    status_stats = {}
    for status in CaseStatus:
        status_stats[status.value] = len([c for c in cases_list if c.get("status") == status.value])
    
    # Stats par catégorie
    category_stats = {}
    for category in CaseCategory:
        category_stats[category.value] = len([c for c in cases_list if c.get("category") == category.value])
    
    # Stats par priorité
    priority_stats = {}
    for priority in CasePriority:
        priority_stats[priority.value] = len([c for c in cases_list if c.get("priority") == priority.value])
    
    return {
        "total_clients": len(clients_db),
        "total_cases": len(cases_db),
        "total_notes": len(notes_db),
        "total_files": len(files_db),
        "by_status": status_stats,
        "by_category": category_stats,
        "by_priority": priority_stats,
        "cases_with_ai_analysis": len([c for c in cases_list if c.get("last_ai_update")])
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8212)
