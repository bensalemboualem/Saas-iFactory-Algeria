"""
IAFactory Chat Multi-User - Modèles Pydantic
=============================================
Rooms, Members, Messages, Invitations
Multi-tenant avec support temps réel
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Any, List
from pydantic import BaseModel, Field, EmailStr
import uuid


# ============================================
# Enums
# ============================================

class RoomType(str, Enum):
    """Types de rooms de chat"""
    DIRECT = "direct"       # Chat 1:1
    GROUP = "group"         # Groupe privé
    PROJECT = "project"     # Lié à un projet
    AGENT = "agent"         # Avec agent BMAD


class MemberRole(str, Enum):
    """Rôles des membres dans une room"""
    OWNER = "owner"         # Créateur
    ADMIN = "admin"         # Admin
    MEMBER = "member"       # Membre normal
    READONLY = "readonly"   # Lecture seule


class InvitationStatus(str, Enum):
    """Status des invitations"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"


class ContentType(str, Enum):
    """Types de contenu de message"""
    TEXT = "text"
    CODE = "code"
    FILE = "file"
    IMAGE = "image"


# ============================================
# Chat Rooms
# ============================================

class ChatRoomBase(BaseModel):
    """Base room de chat"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    room_type: RoomType = RoomType.GROUP
    color: str = "#6366f1"
    is_private: bool = True
    allow_invites: bool = True
    max_members: int = 50


class ChatRoomCreate(ChatRoomBase):
    """Création d'une room"""
    project_id: Optional[int] = None
    agent_id: Optional[str] = None
    initial_members: List[int] = Field(default_factory=list)


class ChatRoomUpdate(BaseModel):
    """Mise à jour d'une room"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    color: Optional[str] = None
    is_private: Optional[bool] = None
    allow_invites: Optional[bool] = None
    avatar_url: Optional[str] = None


class ChatRoom(ChatRoomBase):
    """Room complète"""
    id: str
    tenant_id: str
    avatar_url: Optional[str] = None
    project_id: Optional[int] = None
    agent_id: Optional[str] = None
    member_count: int = 1
    message_count: int = 0
    last_message_at: Optional[datetime] = None
    last_message_preview: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_archived: bool = False

    class Config:
        from_attributes = True


class ChatRoomWithMembers(ChatRoom):
    """Room avec liste des membres"""
    members: List["ChatRoomMember"] = []


class ChatRoomListItem(BaseModel):
    """Item pour liste des rooms (optimisé)"""
    id: str
    name: str
    room_type: RoomType
    color: str
    avatar_url: Optional[str] = None
    member_count: int
    unread_count: int = 0
    last_message_at: Optional[datetime] = None
    last_message_preview: Optional[str] = None


# ============================================
# Room Members
# ============================================

class ChatRoomMemberBase(BaseModel):
    """Base membre de room"""
    role: MemberRole = MemberRole.MEMBER
    notifications_enabled: bool = True


class ChatRoomMemberAdd(BaseModel):
    """Ajout d'un membre"""
    user_id: int
    role: MemberRole = MemberRole.MEMBER


class ChatRoomMemberUpdate(BaseModel):
    """Mise à jour d'un membre"""
    role: Optional[MemberRole] = None
    notifications_enabled: Optional[bool] = None
    muted_until: Optional[datetime] = None


class ChatRoomMember(ChatRoomMemberBase):
    """Membre complet"""
    id: str
    room_id: str
    user_id: int
    last_read_at: datetime
    unread_count: int = 0
    joined_at: datetime

    # Info utilisateur (jointure)
    username: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


# ============================================
# Room Messages
# ============================================

class ChatMessageBase(BaseModel):
    """Base message de chat"""
    content: str = Field(..., min_length=1)
    content_type: ContentType = ContentType.TEXT


class ChatMessageCreate(ChatMessageBase):
    """Création d'un message"""
    reply_to_id: Optional[str] = None
    mentions: List[int] = Field(default_factory=list)
    attachments: List[dict] = Field(default_factory=list)


class ChatMessageUpdate(BaseModel):
    """Mise à jour d'un message"""
    content: str = Field(..., min_length=1)


class ChatRoomMessage(ChatMessageBase):
    """Message complet"""
    id: str
    room_id: str
    sender_id: int
    reply_to_id: Optional[str] = None
    mentions: List[int] = []
    attachments: List[dict] = []
    reactions: dict = {}
    is_edited: bool = False
    edited_at: Optional[datetime] = None
    is_deleted: bool = False
    created_at: datetime

    # Info expéditeur (jointure)
    sender_username: Optional[str] = None
    sender_avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


class ChatMessageReaction(BaseModel):
    """Réaction à un message"""
    emoji: str = Field(..., min_length=1, max_length=10)
    action: str = Field(..., pattern="^(add|remove)$")


class ChatMessageList(BaseModel):
    """Liste paginée de messages"""
    messages: List[ChatRoomMessage]
    total: int
    has_more: bool
    oldest_id: Optional[str] = None


# ============================================
# Invitations
# ============================================

class InvitationBase(BaseModel):
    """Base invitation"""
    assigned_role: MemberRole = MemberRole.MEMBER
    message: Optional[str] = None


class InvitationCreateByUser(InvitationBase):
    """Invitation par user_id"""
    invitee_id: int


class InvitationCreateByEmail(InvitationBase):
    """Invitation par email"""
    invitee_email: EmailStr


class InvitationResponse(BaseModel):
    """Réponse à une invitation"""
    accept: bool


class ChatRoomInvitation(InvitationBase):
    """Invitation complète"""
    id: str
    room_id: str
    inviter_id: int
    invitee_id: Optional[int] = None
    invitee_email: Optional[str] = None
    invite_token: str
    status: InvitationStatus = InvitationStatus.PENDING
    expires_at: datetime
    created_at: datetime
    responded_at: Optional[datetime] = None

    # Info inviteur (jointure)
    inviter_username: Optional[str] = None

    # Info room (jointure)
    room_name: Optional[str] = None

    class Config:
        from_attributes = True


class InvitationPublicInfo(BaseModel):
    """Info publique d'une invitation (pour landing page)"""
    room_name: str
    room_type: RoomType
    inviter_username: str
    member_count: int
    expires_at: datetime
    is_valid: bool


# ============================================
# Read Receipts
# ============================================

class ReadReceiptCreate(BaseModel):
    """Marquer comme lu"""
    last_read_message_id: Optional[str] = None


class ReadReceipt(BaseModel):
    """Accusé de lecture"""
    message_id: str
    user_id: int
    read_at: datetime


# ============================================
# Typing Indicators
# ============================================

class TypingIndicator(BaseModel):
    """Indicateur de frappe"""
    room_id: str
    user_id: int
    is_typing: bool


# ============================================
# Direct Chat
# ============================================

class DirectChatCreate(BaseModel):
    """Créer un chat direct avec un utilisateur"""
    target_user_id: int


class DirectChatResponse(BaseModel):
    """Réponse création chat direct"""
    room_id: str
    is_new: bool


# ============================================
# Online Status
# ============================================

class UserOnlineStatus(BaseModel):
    """Status en ligne d'un utilisateur"""
    user_id: int
    is_online: bool
    last_seen: Optional[datetime] = None


class RoomOnlineStatus(BaseModel):
    """Status en ligne des membres d'une room"""
    room_id: str
    online_users: List[int]
    typing_users: List[int]


# Forward reference resolution
ChatRoomWithMembers.model_rebuild()
