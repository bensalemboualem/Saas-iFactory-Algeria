"""
IA Factory - Brand Models
Phase 1: Brand Configuration & Team Management
"""

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ToneType(str, Enum):
    """Brand tone types"""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    ENERGETIC = "energetic"
    INSPIRATIONAL = "inspirational"
    EDUCATIONAL = "educational"
    HUMOROUS = "humorous"


class UserRole(str, Enum):
    """User roles in the platform"""
    ADMIN = "admin"
    MANAGER = "manager"
    CREATOR = "creator"
    VIEWER = "viewer"


class Language(str, Enum):
    """Supported languages"""
    EN = "en"
    FR = "fr"
    AR = "ar"


class BrandVoice(BaseModel):
    """Brand voice configuration - defines how content sounds"""
    
    brand_name: str = Field(..., min_length=1, max_length=100, description="Brand name")
    tone: ToneType = Field(..., description="Overall tone of content")
    tone_description: str = Field(..., max_length=500, description="Detailed tone description")
    key_values: List[str] = Field(..., min_length=2, max_length=5, description="Core brand values")
    target_audience: str = Field(..., max_length=200, description="Target audience description")
    audience_description: str = Field(..., max_length=500, description="Detailed audience profile")
    language: Language = Field(default=Language.EN, description="Primary language")
    local_market: str = Field(default="Global", description="Target market/region")
    unique_selling_points: List[str] = Field(default=[], description="USPs")
    brand_story: Optional[str] = Field(None, max_length=2000, description="Brand story/narrative")
    
    class Config:
        json_schema_extra = {
            "example": {
                "brand_name": "IA Factory Algeria",
                "tone": "energetic",
                "tone_description": "Fast-paced, innovative, forward-thinking with local authenticity",
                "key_values": ["Innovation", "Authenticité", "Qualité", "Excellence"],
                "target_audience": "18-35 year old Algerian entrepreneurs",
                "audience_description": "Tech-savvy individuals interested in AI and automation",
                "language": "fr",
                "local_market": "Algeria",
                "unique_selling_points": ["First AI video factory in Algeria", "Trilingual content"],
                "brand_story": "IA Factory started in 2024..."
            }
        }


class ContentPillar(BaseModel):
    """Content pillar - defines content categories and distribution"""
    
    id: Optional[str] = Field(None, description="Pillar ID")
    brand_id: Optional[str] = Field(None, description="Associated brand ID")
    name: str = Field(..., max_length=50, description="Pillar name")
    description: str = Field(..., max_length=300, description="Pillar description")
    percentage_of_content: int = Field(..., ge=0, le=100, description="% of total content")
    content_examples: List[str] = Field(default=[], description="Example content ideas")
    target_metrics: Dict[str, Any] = Field(default={}, description="Target KPIs for this pillar")
    posting_frequency: int = Field(default=1, ge=1, le=10, description="Posts per week")
    hashtags: List[str] = Field(default=[], description="Default hashtags for this pillar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Education",
                "description": "Educational content about AI and automation",
                "percentage_of_content": 40,
                "content_examples": ["AI tutorials", "Tool reviews", "How-to guides"],
                "target_metrics": {"engagement_rate": 5, "saves": 100},
                "posting_frequency": 3,
                "hashtags": ["#AIEducation", "#LearnAI", "#TechTips"]
            }
        }


class VisualGuidelines(BaseModel):
    """Visual brand guidelines"""
    
    primary_color: str = Field(default="#000000", description="Primary brand color (hex)")
    secondary_color: str = Field(default="#FFFFFF", description="Secondary color (hex)")
    accent_color: str = Field(default="#FF6B00", description="Accent color (hex)")
    font_family: str = Field(default="Inter", description="Primary font family")
    logo_url: Optional[str] = Field(None, description="Logo URL")
    watermark_url: Optional[str] = Field(None, description="Watermark URL")
    visual_style: str = Field(default="modern", description="Overall visual style")
    overlay_style: str = Field(default="minimal", description="Text overlay style")


class PostingSchedule(BaseModel):
    """Posting schedule configuration"""
    
    timezone: str = Field(default="Africa/Algiers", description="Timezone")
    optimal_hours: List[int] = Field(default=[19, 20, 21], description="Best posting hours")
    posting_days: List[int] = Field(default=[0, 1, 2, 3, 4, 5, 6], description="Days to post (0=Mon)")
    posts_per_day: int = Field(default=1, ge=1, le=5, description="Max posts per day")


class BrandGuidelines(BaseModel):
    """Complete brand guidelines document"""
    
    id: Optional[str] = Field(None, description="Brand ID")
    brand_name: str = Field(..., description="Brand name")
    brand_voice: BrandVoice
    content_pillars: List[ContentPillar] = Field(default=[])
    visual_guidelines: VisualGuidelines = Field(default_factory=VisualGuidelines)
    messaging_guidelines: str = Field(default="", max_length=2000)
    hashtag_strategy: List[str] = Field(default=[])
    posting_schedule: PostingSchedule = Field(default_factory=PostingSchedule)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    created_by: Optional[str] = Field(None)
    is_active: bool = Field(default=True)
    
    # AI Configuration
    featured_topic: Optional[str] = Field(None, description="Current featured topic for content")
    niche: str = Field(default="Technology", description="Industry niche")


class UserPermissions(BaseModel):
    """User permissions mapping"""
    
    can_create_content: bool = False
    can_edit_content: bool = False
    can_delete_content: bool = False
    can_publish: bool = False
    can_schedule: bool = False
    can_invite_users: bool = False
    can_manage_settings: bool = False
    can_view_analytics: bool = False
    can_manage_billing: bool = False


class UserProfile(BaseModel):
    """User profile for team management"""
    
    id: Optional[str] = Field(None)
    email: EmailStr = Field(..., description="User email")
    name: str = Field(..., min_length=1, max_length=100)
    role: UserRole = Field(..., description="User role")
    brand_id: str = Field(..., description="Associated brand")
    permissions: UserPermissions = Field(default_factory=UserPermissions)
    
    # Status
    date_joined: datetime = Field(default_factory=datetime.now)
    last_active: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    
    # Preferences
    notification_preferences: Dict[str, bool] = Field(default={
        "email_notifications": True,
        "push_notifications": True,
        "weekly_digest": True
    })


def get_permissions_for_role(role: UserRole) -> UserPermissions:
    """Get default permissions for a role"""
    
    permissions_map = {
        UserRole.ADMIN: UserPermissions(
            can_create_content=True,
            can_edit_content=True,
            can_delete_content=True,
            can_publish=True,
            can_schedule=True,
            can_invite_users=True,
            can_manage_settings=True,
            can_view_analytics=True,
            can_manage_billing=True
        ),
        UserRole.MANAGER: UserPermissions(
            can_create_content=True,
            can_edit_content=True,
            can_delete_content=False,
            can_publish=True,
            can_schedule=True,
            can_invite_users=True,
            can_manage_settings=False,
            can_view_analytics=True,
            can_manage_billing=False
        ),
        UserRole.CREATOR: UserPermissions(
            can_create_content=True,
            can_edit_content=True,
            can_delete_content=False,
            can_publish=False,
            can_schedule=False,
            can_invite_users=False,
            can_manage_settings=False,
            can_view_analytics=True,
            can_manage_billing=False
        ),
        UserRole.VIEWER: UserPermissions(
            can_create_content=False,
            can_edit_content=False,
            can_delete_content=False,
            can_publish=False,
            can_schedule=False,
            can_invite_users=False,
            can_manage_settings=False,
            can_view_analytics=True,
            can_manage_billing=False
        )
    }
    
    return permissions_map.get(role, UserPermissions())
