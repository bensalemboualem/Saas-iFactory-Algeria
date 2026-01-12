"""
IAFactory Conversations API - Chat Sessions & Messages
=======================================================
Endpoints pour gerer les conversations persistantes:
- Sessions de chat
- Messages
- Integration avec memoire utilisateur
- Extraction automatique de memoire

Endpoints:
- GET  /api/conversations/                 - Liste sessions
- GET  /api/conversations/{id}             - Detail session avec messages
- POST /api/conversations/                 - Creer session
- PUT  /api/conversations/{id}             - Modifier session (titre, star, archive)
- DELETE /api/conversations/{id}           - Supprimer session
- GET  /api/conversations/{id}/messages    - Messages d'une session
- POST /api/conversations/{id}/messages    - Envoyer message
- POST /api/conversations/send             - Envoyer message (cree session si necessaire)
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from app.dependencies import get_current_active_user
from app.models.user import UserInDB
from app.models.memory_models import (
    AppContext, MessageRole,
    ChatSession, ChatSessionCreate, ChatSessionUpdate, ChatSessionSummary,
    ChatMessage, ChatMessageCreate,
    SendMessageRequest, SendMessageResponse,
    GetConversationsResponse, GetMessagesResponse
)
from app.services.memory_service import get_memory_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


# ============================================
# Request/Response Schemas
# ============================================

class CreateSessionRequest(BaseModel):
    """Requete creation session"""
    title: Optional[str] = Field(None, description="Titre de la conversation")
    app_context: AppContext = Field(default=AppContext.CHAT, description="Contexte applicatif")
    language: str = Field(default="fr", description="Langue")
    agent_id: Optional[str] = Field(None, description="ID agent si specifique")
    model: str = Field(default="groq", description="Modele LLM")
    metadata: dict = Field(default_factory=dict, description="Metadata additionnelle")


class UpdateSessionRequest(BaseModel):
    """Requete modification session"""
    title: Optional[str] = None
    is_starred: Optional[bool] = None
    is_archived: Optional[bool] = None


class SendMessageToSessionRequest(BaseModel):
    """Requete envoi message a une session"""
    content: str = Field(..., min_length=1, description="Contenu du message")
    role: MessageRole = Field(default=MessageRole.USER, description="Role")
    metadata: dict = Field(default_factory=dict)


class QuickSendRequest(BaseModel):
    """Requete envoi rapide (cree session si besoin)"""
    content: str = Field(..., min_length=1, description="Contenu du message")
    session_id: Optional[str] = Field(None, description="ID session existante")
    app_context: AppContext = Field(default=AppContext.CHAT)
    model: str = Field(default="groq")
    include_memory: bool = Field(default=True, description="Inclure contexte memoire")
    extract_memories: bool = Field(default=True, description="Extraire memoires du message")


class ConversationListResponse(BaseModel):
    """Response liste conversations"""
    conversations: List[ChatSessionSummary]
    total: int
    has_more: bool
    page: int
    limit: int


class ConversationDetailResponse(BaseModel):
    """Response detail conversation avec messages"""
    session: ChatSession
    messages: List[ChatMessage]
    has_more_messages: bool


class MessageSentResponse(BaseModel):
    """Response message envoye"""
    success: bool
    session_id: str
    message: ChatMessage
    memories_extracted: int = 0


class DeleteResponse(BaseModel):
    """Response suppression"""
    success: bool
    message: str


# ============================================
# Session Endpoints
# ============================================

@router.get(
    "/",
    response_model=ConversationListResponse,
    summary="Liste conversations",
    description="Liste les conversations de l'utilisateur avec pagination"
)
async def list_conversations(
    app_context: Optional[AppContext] = Query(None, description="Filtrer par contexte"),
    is_starred: Optional[bool] = Query(None, description="Filtrer favoris"),
    is_archived: bool = Query(False, description="Inclure archives"),
    page: int = Query(1, ge=1, description="Page"),
    limit: int = Query(20, ge=1, le=100, description="Limite par page"),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Liste les conversations de l'utilisateur"""
    service = get_memory_service()

    offset = (page - 1) * limit

    sessions, total = await service.get_sessions(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        app_context=app_context,
        is_archived=is_archived,
        is_starred=is_starred,
        limit=limit,
        offset=offset
    )

    has_more = (offset + len(sessions)) < total

    return ConversationListResponse(
        conversations=sessions,
        total=total,
        has_more=has_more,
        page=page,
        limit=limit
    )


@router.post(
    "/",
    response_model=ChatSession,
    status_code=status.HTTP_201_CREATED,
    summary="Creer conversation",
    description="Cree une nouvelle session de conversation"
)
async def create_conversation(
    request: CreateSessionRequest,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Cree une nouvelle conversation"""
    service = get_memory_service()

    session_data = ChatSessionCreate(
        title=request.title,
        app_context=request.app_context,
        language=request.language,
        agent_id=request.agent_id,
        model=request.model,
        metadata=request.metadata
    )

    session = await service.create_session(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        session_data=session_data
    )

    logger.info(f"Session created: {session.id} for user {current_user.id}")

    return session


@router.get(
    "/{session_id}",
    response_model=ConversationDetailResponse,
    summary="Detail conversation",
    description="Recupere une conversation avec ses messages"
)
async def get_conversation(
    session_id: str,
    messages_limit: int = Query(50, ge=1, le=200, description="Nombre de messages"),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Detail d'une conversation avec messages"""
    service = get_memory_service()

    session = await service.get_session(session_id, current_user.tenant_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation non trouvee"
        )

    # Verify ownership
    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acces non autorise"
        )

    messages, has_more = await service.get_messages(
        session_id=session_id,
        tenant_id=current_user.tenant_id,
        limit=messages_limit
    )

    return ConversationDetailResponse(
        session=session,
        messages=messages,
        has_more_messages=has_more
    )


@router.put(
    "/{session_id}",
    response_model=ChatSession,
    summary="Modifier conversation",
    description="Modifie le titre, statut favori ou archive d'une conversation"
)
async def update_conversation(
    session_id: str,
    request: UpdateSessionRequest,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Modifie une conversation"""
    service = get_memory_service()

    # Verify ownership
    session = await service.get_session(session_id, current_user.tenant_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation non trouvee"
        )

    updates = ChatSessionUpdate(
        title=request.title,
        is_starred=request.is_starred,
        is_archived=request.is_archived
    )

    updated = await service.update_session(
        session_id=session_id,
        tenant_id=current_user.tenant_id,
        updates=updates
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur mise a jour"
        )

    return updated


@router.delete(
    "/{session_id}",
    response_model=DeleteResponse,
    summary="Supprimer conversation",
    description="Supprime une conversation et tous ses messages"
)
async def delete_conversation(
    session_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Supprime une conversation"""
    service = get_memory_service()

    # Verify ownership
    session = await service.get_session(session_id, current_user.tenant_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation non trouvee"
        )

    deleted = await service.delete_session(session_id, current_user.tenant_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur suppression"
        )

    logger.info(f"Session deleted: {session_id} by user {current_user.id}")

    return DeleteResponse(
        success=True,
        message="Conversation supprimee"
    )


# ============================================
# Message Endpoints
# ============================================

@router.get(
    "/{session_id}/messages",
    response_model=GetMessagesResponse,
    summary="Messages conversation",
    description="Recupere les messages d'une conversation avec pagination cursor"
)
async def get_messages(
    session_id: str,
    limit: int = Query(50, ge=1, le=200, description="Nombre de messages"),
    before_id: Optional[str] = Query(None, description="ID message pour pagination"),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Liste les messages d'une conversation"""
    service = get_memory_service()

    # Verify ownership
    session = await service.get_session(session_id, current_user.tenant_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation non trouvee"
        )

    messages, has_more = await service.get_messages(
        session_id=session_id,
        tenant_id=current_user.tenant_id,
        limit=limit,
        before_id=before_id
    )

    return GetMessagesResponse(
        session_id=session_id,
        messages=messages,
        has_more=has_more
    )


@router.post(
    "/{session_id}/messages",
    response_model=MessageSentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Envoyer message",
    description="Ajoute un message a une conversation existante"
)
async def send_message_to_session(
    session_id: str,
    request: SendMessageToSessionRequest,
    extract_memories: bool = Query(True, description="Extraire memoires"),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Envoie un message a une conversation"""
    service = get_memory_service()

    # Verify ownership
    session = await service.get_session(session_id, current_user.tenant_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation non trouvee"
        )

    message_data = ChatMessageCreate(
        role=request.role,
        content=request.content,
        metadata=request.metadata
    )

    message = await service.add_message(
        session_id=session_id,
        tenant_id=current_user.tenant_id,
        message=message_data
    )

    # Extract memories if user message
    memories_extracted = 0
    if extract_memories and request.role == MessageRole.USER:
        extracted = await service.extract_memories_from_message(
            tenant_id=current_user.tenant_id,
            user_id=current_user.id,
            message_id=message.id,
            content=request.content
        )
        memories_extracted = len(extracted)

    return MessageSentResponse(
        success=True,
        session_id=session_id,
        message=message,
        memories_extracted=memories_extracted
    )


# ============================================
# Quick Send (Create Session if needed)
# ============================================

@router.post(
    "/send",
    response_model=MessageSentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Envoi rapide",
    description="Envoie un message, cree une session si necessaire"
)
async def quick_send_message(
    request: QuickSendRequest,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Envoie un message avec creation automatique de session"""
    service = get_memory_service()

    session_id = request.session_id

    # Create session if not provided
    if not session_id:
        session_data = ChatSessionCreate(
            app_context=request.app_context,
            model=request.model
        )

        session = await service.create_session(
            tenant_id=current_user.tenant_id,
            user_id=current_user.id,
            session_data=session_data
        )
        session_id = session.id
        logger.info(f"Auto-created session: {session_id}")
    else:
        # Verify ownership
        session = await service.get_session(session_id, current_user.tenant_id)
        if not session or session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation non trouvee"
            )

    # Add message
    message_data = ChatMessageCreate(
        role=MessageRole.USER,
        content=request.content
    )

    message = await service.add_message(
        session_id=session_id,
        tenant_id=current_user.tenant_id,
        message=message_data
    )

    # Extract memories
    memories_extracted = 0
    if request.extract_memories:
        extracted = await service.extract_memories_from_message(
            tenant_id=current_user.tenant_id,
            user_id=current_user.id,
            message_id=message.id,
            content=request.content
        )
        memories_extracted = len(extracted)

    return MessageSentResponse(
        success=True,
        session_id=session_id,
        message=message,
        memories_extracted=memories_extracted
    )


# ============================================
# Starred/Archive Operations
# ============================================

@router.post(
    "/{session_id}/star",
    response_model=ChatSession,
    summary="Toggle favori",
    description="Ajoute/retire une conversation des favoris"
)
async def toggle_star(
    session_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Toggle favori"""
    service = get_memory_service()

    session = await service.get_session(session_id, current_user.tenant_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation non trouvee"
        )

    updates = ChatSessionUpdate(is_starred=not session.is_starred)

    return await service.update_session(session_id, current_user.tenant_id, updates)


@router.post(
    "/{session_id}/archive",
    response_model=ChatSession,
    summary="Archiver",
    description="Archive une conversation"
)
async def archive_conversation(
    session_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Archive une conversation"""
    service = get_memory_service()

    session = await service.get_session(session_id, current_user.tenant_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation non trouvee"
        )

    updates = ChatSessionUpdate(is_archived=True)

    return await service.update_session(session_id, current_user.tenant_id, updates)


@router.post(
    "/{session_id}/unarchive",
    response_model=ChatSession,
    summary="Desarchiver",
    description="Restore une conversation archivee"
)
async def unarchive_conversation(
    session_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Desarchive une conversation"""
    service = get_memory_service()

    session = await service.get_session(session_id, current_user.tenant_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation non trouvee"
        )

    updates = ChatSessionUpdate(is_archived=False)

    return await service.update_session(session_id, current_user.tenant_id, updates)


# ============================================
# Bulk Operations
# ============================================

class BulkArchiveRequest(BaseModel):
    """Requete archivage multiple"""
    session_ids: List[str]


class BulkArchiveResponse(BaseModel):
    """Response archivage multiple"""
    archived: int
    failed: int


@router.post(
    "/bulk/archive",
    response_model=BulkArchiveResponse,
    summary="Archivage multiple",
    description="Archive plusieurs conversations"
)
async def bulk_archive(
    request: BulkArchiveRequest,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Archive plusieurs conversations"""
    service = get_memory_service()

    archived = 0
    failed = 0

    for session_id in request.session_ids:
        try:
            session = await service.get_session(session_id, current_user.tenant_id)
            if session and session.user_id == current_user.id:
                updates = ChatSessionUpdate(is_archived=True)
                await service.update_session(session_id, current_user.tenant_id, updates)
                archived += 1
            else:
                failed += 1
        except Exception:
            failed += 1

    return BulkArchiveResponse(archived=archived, failed=failed)
