# crud.py - CRUD operations for CRM IA with SQLAlchemy

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Any
import json

import models
from schemas import (
    ClientCreate, ClientUpdate, CaseCreate, CaseUpdate, CaseStatus, CaseCategory, CasePriority, NoteCreate
)
from datetime import datetime

# --- Client Operations ---
def get_client(db: Session, client_id: str) -> Optional[models.Client]:
    return db.query(models.Client).filter(models.Client.id == client_id).first()

def get_clients(db: Session, skip: int = 0, limit: int = 100, client_type: Optional[str] = None, search: Optional[str] = None) -> List[models.Client]:
    query = db.query(models.Client)
    if client_type:
        query = query.filter(models.Client.client_type == client_type)
    if search:
        search_lower = f"%{search.lower()}%"
        query = query.filter(
            (models.Client.first_name.ilike(search_lower)) |
            (models.Client.last_name.ilike(search_lower)) |
            (models.Client.company_name.ilike(search_lower)) |
            (models.Client.email.ilike(search_lower))
        )
    return query.offset(skip).limit(limit).all()

def create_client(db: Session, client: ClientCreate) -> models.Client:
    client_data = client.dict()
    # Convertir extra_fields en JSON string pour stockage
    if client_data.get('extra_fields'):
        client_data['extra_fields'] = json.dumps(client_data['extra_fields'])
    db_client = models.Client(**client_data)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def update_client(db: Session, client_id: str, client_update: ClientUpdate) -> Optional[models.Client]:
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if db_client:
        update_data = client_update.dict(exclude_unset=True)
        # Gérer extra_fields
        if 'extra_fields' in update_data and update_data['extra_fields']:
            update_data['extra_fields'] = json.dumps(update_data['extra_fields'])
        for key, value in update_data.items():
            setattr(db_client, key, value)
        db_client.updated_at = datetime.utcnow()
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
    return db_client

def add_client_field(db: Session, client_id: str, field_name: str, field_value: Any) -> Optional[models.Client]:
    """Ajouter un champ personnalisé à un client"""
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if db_client:
        # Parser les extra_fields existants
        extra = {}
        if db_client.extra_fields:
            extra = json.loads(db_client.extra_fields)
        # Ajouter le nouveau champ
        extra[field_name] = field_value
        db_client.extra_fields = json.dumps(extra)
        db_client.updated_at = datetime.utcnow()
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
    return db_client

def delete_client_field(db: Session, client_id: str, field_name: str) -> Optional[models.Client]:
    """Supprimer un champ personnalisé d'un client"""
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if db_client and db_client.extra_fields:
        extra = json.loads(db_client.extra_fields)
        if field_name in extra:
            del extra[field_name]
            db_client.extra_fields = json.dumps(extra) if extra else None
            db_client.updated_at = datetime.utcnow()
            db.add(db_client)
            db.commit()
            db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: str):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if db_client:
        db.delete(db_client)
        db.commit()
    return db_client


# --- Case Operations ---
def get_case(db: Session, case_id: str) -> Optional[models.Case]:
    return db.query(models.Case).filter(models.Case.id == case_id).first()

def get_cases(db: Session, skip: int = 0, limit: int = 100, client_id: Optional[str] = None, status: Optional[CaseStatus] = None, category: Optional[CaseCategory] = None, priority: Optional[CasePriority] = None) -> List[models.Case]:
    query = db.query(models.Case)
    if client_id:
        query = query.filter(models.Case.client_id == client_id)
    if status:
        query = query.filter(models.Case.status == status.value)
    if category:
        query = query.filter(models.Case.category == category.value)
    if priority:
        query = query.filter(models.Case.priority == priority.value)
    return query.offset(skip).limit(limit).order_by(models.Case.updated_at.desc()).all()

def create_case(db: Session, case: CaseCreate) -> models.Case:
    db_case = models.Case(**case.dict())
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case

def update_case(db: Session, case_id: str, case_update: CaseUpdate) -> Optional[models.Case]:
    db_case = db.query(models.Case).filter(models.Case.id == case_id).first()
    if db_case:
        update_data = case_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_case, key, value)
        db_case.updated_at = datetime.utcnow()
        db.add(db_case)
        db.commit()
        db.refresh(db_case)
    return db_case

def delete_case(db: Session, case_id: str):
    db_case = db.query(models.Case).filter(models.Case.id == case_id).first()
    if db_case:
        db.delete(db_case)
        db.commit()
    return db_case


# --- Note Operations ---
def get_note(db: Session, note_id: str) -> Optional[models.Note]:
    return db.query(models.Note).filter(models.Note.id == note_id).first()

def get_notes_for_case(db: Session, case_id: str, skip: int = 0, limit: int = 100) -> List[models.Note]:
    return db.query(models.Note).filter(models.Note.case_id == case_id).offset(skip).limit(limit).order_by(models.Note.created_at.desc()).all()

def create_note(db: Session, note: NoteCreate, case_id: str) -> models.Note:
    db_note = models.Note(**note.dict(), case_id=case_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


# --- File Operations ---
def get_file(db: Session, file_id: str) -> Optional[models.File]:
    return db.query(models.File).filter(models.File.id == file_id).first()

def get_files_for_case(db: Session, case_id: str, skip: int = 0, limit: int = 100) -> List[models.File]:
    return db.query(models.File).filter(models.File.case_id == case_id).offset(skip).limit(limit).order_by(models.File.uploaded_at.desc()).all()

def create_file(db: Session, file_name: str, file_url: str, file_type: str, file_size: int, case_id: str) -> models.File:
    db_file = models.File(file_name=file_name, file_url=file_url, file_type=file_type, file_size=file_size, case_id=case_id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file
