"""
IAFactory Video Studio Pro - Database Models
Modèles SQLAlchemy pour PostgreSQL
"""

from datetime import datetime
from typing import Optional, List
from enum import Enum as PyEnum

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text, 
    ForeignKey, JSON, Enum, BigInteger, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
import uuid

Base = declarative_base()


# ============================================
# ENUMS
# ============================================

class TemplateCategory(str, PyEnum):
    ECOMMERCE = "e-commerce"
    SOCIAL_MEDIA = "social-media"
    YOUTUBE = "youtube"
    SPORT = "sport"
    IMMOBILIER = "immobilier"
    FOOD = "food"
    EDUCATION = "education"
    CORPORATE = "corporate"
    EVENTS = "events"
    CUSTOM = "custom"


class TemplatePlatform(str, PyEnum):
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    YOUTUBE_SHORTS = "youtube-shorts"
    FACEBOOK = "facebook"
    ALL = "all"


class TransactionType(str, PyEnum):
    PURCHASE = "purchase"
    GENERATION = "generation"
    VOICE = "voice"
    TEMPLATE = "template"
    REFUND = "refund"
    BONUS = "bonus"
    SUBSCRIPTION = "subscription"


class TransactionStatus(str, PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class SubscriptionPlan(str, PyEnum):
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"
    BUSINESS = "business"
    ENTERPRISE = "enterprise"


# ============================================
# USER & AUTH
# ============================================

class User(Base):
    """Utilisateur de la plateforme."""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    
    # Profile
    company = Column(String(200))
    phone = Column(String(20))
    country = Column(String(2), default="DZ")  # ISO code
    language = Column(String(5), default="fr")
    
    # Credits
    credit_balance = Column(Integer, default=0)
    lifetime_credits = Column(BigInteger, default=0)
    
    # Subscription
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE)
    subscription_expires_at = Column(DateTime)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime)
    
    # Relations
    transactions = relationship("CreditTransaction", back_populates="user")
    projects = relationship("Project", back_populates="user")
    custom_templates = relationship("Template", back_populates="creator")
    custom_voices = relationship("CustomVoice", back_populates="user")


# ============================================
# TEMPLATES
# ============================================

class Template(Base):
    """Template vidéo réutilisable."""
    __tablename__ = "templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic info (multilingue)
    name_fr = Column(String(200), nullable=False)
    name_ar = Column(String(200))
    name_en = Column(String(200))
    
    description_fr = Column(Text)
    description_ar = Column(Text)
    description_en = Column(Text)
    
    # Categorization
    category = Column(Enum(TemplateCategory), nullable=False, index=True)
    subcategory = Column(String(50))
    tags = Column(ARRAY(String), default=[])
    
    # Platform optimization
    platforms = Column(ARRAY(String), default=["all"])  # ["tiktok", "instagram"]
    aspect_ratio = Column(String(10), default="9:16")  # 9:16, 16:9, 1:1
    
    # Media
    thumbnail_url = Column(String(500))
    preview_video_url = Column(String(500))
    
    # Template config
    duration = Column(Integer, nullable=False)  # seconds
    credits_cost = Column(Integer, nullable=False)
    parameters = Column(JSONB, default={})  # Paramètres personnalisables
    default_values = Column(JSONB, default={})
    
    # Script template
    script_template = Column(Text)  # Template de script avec variables
    
    # AI hints
    ai_prompt_hint = Column(Text)  # Hint pour la génération IA
    visual_style = Column(String(100))  # "cinematic", "minimal", "dynamic"
    
    # Popularity & stats
    use_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    
    # Custom template
    is_custom = Column(Boolean, default=False)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_public = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    creator = relationship("User", back_populates="custom_templates")


class TemplateUsage(Base):
    """Historique d'utilisation des templates."""
    __tablename__ = "template_usage"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_id = Column(UUID(as_uuid=True), ForeignKey("templates.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)
    
    parameters_used = Column(JSONB, default={})
    credits_spent = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)


# ============================================
# CREDITS & TRANSACTIONS
# ============================================

class CreditPack(Base):
    """Packs de crédits disponibles à l'achat."""
    __tablename__ = "credit_packs"
    
    id = Column(String(50), primary_key=True)  # "starter", "pro", "business"
    
    # Info (multilingue)
    name_fr = Column(String(100), nullable=False)
    name_ar = Column(String(100))
    name_en = Column(String(100))
    
    description_fr = Column(Text)
    description_ar = Column(Text)
    description_en = Column(Text)
    
    # Pricing
    credits = Column(Integer, nullable=False)
    price_dzd = Column(Integer, nullable=False)  # Prix en Dinars
    price_eur = Column(Float)  # Prix en Euros
    price_usd = Column(Float)  # Prix en USD
    
    # Stripe
    stripe_price_id = Column(String(100))
    stripe_product_id = Column(String(100))
    
    # Features
    features = Column(JSONB, default=[])  # Liste des avantages
    
    # Status
    is_active = Column(Boolean, default=True)
    is_popular = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CreditTransaction(Base):
    """Transaction de crédits (achat, usage, refund)."""
    __tablename__ = "credit_transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Transaction type
    type = Column(Enum(TransactionType), nullable=False, index=True)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    
    # Amount
    amount = Column(Integer, nullable=False)  # + for credit, - for debit
    balance_before = Column(Integer)
    balance_after = Column(Integer)
    
    # Description
    description = Column(String(500))
    description_fr = Column(String(500))
    description_ar = Column(String(500))
    
    # Reference
    reference_type = Column(String(50))  # "pack", "project", "voice", etc.
    reference_id = Column(String(100))  # ID of the referenced entity
    
    # Payment info (for purchases)
    payment_method = Column(String(50))  # "stripe", "ccp", "baridimob"
    payment_reference = Column(String(200))  # External payment ID
    amount_paid = Column(Float)  # Amount in currency
    currency = Column(String(3))  # "DZD", "EUR", "USD"
    
    # Metadata
    metadata = Column(JSONB, default={})
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime)
    
    # Relations
    user = relationship("User", back_populates="transactions")


class StripeEvent(Base):
    """Log des événements Stripe pour idempotence."""
    __tablename__ = "stripe_events"
    
    id = Column(String(100), primary_key=True)  # Stripe event ID
    event_type = Column(String(100), nullable=False)
    processed = Column(Boolean, default=False)
    data = Column(JSONB)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)


# ============================================
# PROJECTS
# ============================================

class Project(Base):
    """Projet vidéo de l'utilisateur."""
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Basic info
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Source
    template_id = Column(UUID(as_uuid=True), ForeignKey("templates.id"), nullable=True)
    source_type = Column(String(50))  # "template", "scratch", "pipeline"
    
    # Input
    prompt = Column(Text)
    parameters = Column(JSONB, default={})
    
    # Generated content
    script = Column(JSONB)  # Script généré
    storyboard = Column(JSONB)  # Storyboard généré
    
    # Output
    video_url = Column(String(500))
    thumbnail_url = Column(String(500))
    audio_url = Column(String(500))
    
    # Specs
    duration = Column(Integer)
    aspect_ratio = Column(String(10), default="9:16")
    resolution = Column(String(20), default="1080p")
    
    # Status
    status = Column(String(20), default="draft")  # draft, processing, completed, failed
    progress = Column(Integer, default=0)
    error_message = Column(Text)
    
    # Credits
    credits_estimated = Column(Integer, default=0)
    credits_used = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relations
    user = relationship("User", back_populates="projects")


# ============================================
# CUSTOM VOICES
# ============================================

class CustomVoice(Base):
    """Voix personnalisée clonée."""
    __tablename__ = "custom_voices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Voice config
    dialect = Column(String(20), default="darija_dz")
    gender = Column(String(10))
    
    # Service reference
    service = Column(String(20), default="rime")  # "rime", "elevenlabs"
    external_voice_id = Column(String(100))  # ID from the service
    
    # Status
    status = Column(String(20), default="processing")  # processing, ready, failed
    
    # Samples
    sample_urls = Column(ARRAY(String), default=[])
    preview_url = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    ready_at = Column(DateTime)
    
    # Relations
    user = relationship("User", back_populates="custom_voices")


# ============================================
# ANALYTICS
# ============================================

class UsageStats(Base):
    """Statistiques d'utilisation agrégées par jour."""
    __tablename__ = "usage_stats"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(DateTime, nullable=False, index=True)
    
    # User stats
    new_users = Column(Integer, default=0)
    active_users = Column(Integer, default=0)
    
    # Generation stats
    videos_generated = Column(Integer, default=0)
    audio_generated = Column(Integer, default=0)
    templates_used = Column(Integer, default=0)
    
    # Credits
    credits_purchased = Column(BigInteger, default=0)
    credits_used = Column(BigInteger, default=0)
    
    # Revenue
    revenue_dzd = Column(BigInteger, default=0)
    revenue_eur = Column(Float, default=0)
    
    __table_args__ = (
        UniqueConstraint('date', name='unique_date_stats'),
    )
