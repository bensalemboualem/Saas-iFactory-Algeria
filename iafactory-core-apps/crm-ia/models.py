# models.py - SQLAlchemy ORM models for CRM IA

from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import uuid

# --- Client Model ---
class Client(Base):
    __tablename__ = "clients"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String, index=True, nullable=False)  # Prénom
    last_name = Column(String, index=True, nullable=True)    # Nom de famille
    company_name = Column(String, index=True, nullable=True) # Raison sociale (pour entreprises)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, nullable=True)
    client_type = Column(String, nullable=True)  # Libre: PME, Freelance, ou ce que le client veut
    activity_sector = Column(String, nullable=True)  # Libre: Commerce, Juridique, ou ce que le client veut
    address = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    user_id = Column(String, nullable=True)
    extra_fields = Column(Text, nullable=True)  # JSON pour colonnes personnalisées

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cases = relationship("Case", back_populates="client")

# --- Case Model ---
class Case(Base):
    __tablename__ = "cases"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"))
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False) # e.g., "ouvert", "ferme"
    priority = Column(String, nullable=False) # e.g., "haute", "basse"
    category = Column(String, nullable=False) # e.g., "juridique", "fiscal"
    tags = Column(String, nullable=True) # Stored as comma-separated string or JSON string
    
    last_ai_update = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client = relationship("Client", back_populates="cases")
    notes = relationship("Note", back_populates="case", cascade="all, delete-orphan")
    files = relationship("File", back_populates="case", cascade="all, delete-orphan")

# --- Note Model ---
class Note(Base):
    __tablename__ = "notes"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    case_id = Column(String, ForeignKey("cases.id"))
    content = Column(String, nullable=False)
    author_type = Column(String, nullable=False) # "user" or "ai"
    
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="notes")

# --- File Model ---
class File(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    case_id = Column(String, ForeignKey("cases.id"))
    file_name = Column(String, nullable=False)
    file_url = Column(String, nullable=False) # Path or URL to file
    file_type = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="files")
