# schemas.py - Pydantic schemas and Enums for CRM IA

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


# ============================================================================
# ENUMS (seulement pour Case, pas pour Client)
# ============================================================================

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
# SCHEMAS - CLIENTS
# ============================================================================

class ClientCreate(BaseModel):
    first_name: str = Field(..., min_length=1)  # Prénom (obligatoire)
    last_name: Optional[str] = None              # Nom de famille
    company_name: Optional[str] = None           # Raison sociale
    email: Optional[str] = None
    phone: Optional[str] = None
    client_type: Optional[str] = None            # LIBRE: PME, Freelance, Startup, etc.
    activity_sector: Optional[str] = None        # LIBRE: Commerce, IT, Juridique, etc.
    address: Optional[str] = None
    notes: Optional[str] = None
    extra_fields: Optional[Dict[str, Any]] = None

class Client(BaseModel):
    id: str
    first_name: str
    last_name: Optional[str] = None
    company_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    client_type: Optional[str] = None
    activity_sector: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    user_id: Optional[str] = None
    extra_fields: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    cases_count: int = 0

    class Config:
        orm_mode = True

class ClientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    client_type: Optional[str] = None
    activity_sector: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    extra_fields: Optional[Dict[str, Any]] = None

# Pour ajouter un champ personnalisé
class AddFieldRequest(BaseModel):
    field_name: str = Field(..., min_length=1)
    field_value: Any


# ============================================================================
# SCHEMAS - CASES (DOSSIERS)
# ============================================================================

class CaseCreate(BaseModel):
    client_id: str
    title: str = Field(..., min_length=3)
    description: Optional[str] = None
    status: CaseStatus = CaseStatus.OUVERT
    priority: CasePriority = CasePriority.MOYENNE
    category: CaseCategory = CaseCategory.AUTRE
    tags: Optional[List[str]] = None

class Case(BaseModel):
    id: str
    client_id: str
    title: str
    description: Optional[str] = None
    status: CaseStatus
    priority: CasePriority
    category: CaseCategory
    tags: Optional[List[str]] = None
    last_ai_update: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    notes_count: int = 0
    files_count: int = 0
    client_name: Optional[str] = None

    class Config:
        orm_mode = True

class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CaseStatus] = None
    priority: Optional[CasePriority] = None
    category: Optional[CaseCategory] = None
    tags: Optional[List[str]] = None


# ============================================================================
# SCHEMAS - NOTES
# ============================================================================

class NoteCreate(BaseModel):
    content: str = Field(..., min_length=1)
    author_type: NoteAuthor = NoteAuthor.USER

class Note(BaseModel):
    id: str
    case_id: str
    content: str
    author_type: NoteAuthor
    created_at: datetime

    class Config:
        orm_mode = True


# ============================================================================
# SCHEMAS - FILES
# ============================================================================

class FileModel(BaseModel):
    id: str
    case_id: str
    file_name: str
    file_url: str
    file_type: str
    file_size: int
    uploaded_at: datetime

    class Config:
        orm_mode = True
