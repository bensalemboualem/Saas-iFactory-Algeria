"""
IAFactory Chat Rooms API - Multi-User Chat
===========================================
Endpoints pour le chat collaboratif User↔User:
- Rooms (groupes, direct, projet, agent)
- Membres et rôles
- Messages temps réel
- Invitations
- Typing indicators
- Read receipts

Endpoints:
- GET    /api/chat/rooms                    - Liste mes rooms
- POST   /api/chat/rooms                    - Créer une room
- GET    /api/chat/rooms/{id}               - Détail room
- PUT    /api/chat/rooms/{id}               - Modifier room
- DELETE /api/chat/rooms/{id}               - Archiver room

- GET    /api/chat/rooms/{id}/members       - Liste membres
- POST   /api/chat/rooms/{id}/members       - Ajouter membre
- PUT    /api/chat/rooms/{id}/members/{uid} - Modifier membre
- DELETE /api/chat/rooms/{id}/members/{uid} - Retirer membre

- GET    /api/chat/rooms/{id}/messages      - Messages (paginés)
- POST   /api/chat/rooms/{id}/messages      - Envoyer message
- PUT    /api/chat/messages/{mid}           - Éditer message
- DELETE /api/chat/messages/{mid}           - Supprimer message
- POST   /api/chat/messages/{mid}/reactions - Réagir

- POST   /api/chat/rooms/{id}/invitations   - Inviter
- GET    /api/chat/invitations              - Mes invitations
- GET    /api/chat/invitations/{token}      - Info invitation (public)
- POST   /api/chat/invitations/{token}      - Accepter/Refuser

- POST   /api/chat/rooms/{id}/read          - Marquer comme lu
- POST   /api/chat/rooms/{id}/typing        - Indicateur frappe

- POST   /api/chat/direct                   - Créer chat direct
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional, List
from datetime import datetime
import logging
import secrets

from app.dependencies import get_current_active_user
from app.models.user import UserInDB
from app.models.chat_room_models import (
    RoomType, MemberRole, InvitationStatus, ContentType,
    ChatRoomCreate, ChatRoomUpdate, ChatRoom, ChatRoomWithMembers, ChatRoomListItem,
    ChatRoomMemberAdd, ChatRoomMemberUpdate, ChatRoomMember,
    ChatMessageCreate, ChatMessageUpdate, ChatRoomMessage, ChatMessageReaction, ChatMessageList,
    InvitationCreateByUser, InvitationCreateByEmail, InvitationResponse,
    ChatRoomInvitation, InvitationPublicInfo,
    ReadReceiptCreate, TypingIndicator,
    DirectChatCreate, DirectChatResponse,
    RoomOnlineStatus
)
from app.websocket import manager, WSEventType, ChatMessage as WSChatMessage
from app.db import get_db_connection
from app.services.notification_service import get_notification_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat-rooms"])


# ============================================
# Database Helpers
# ============================================

def get_room_or_404(conn, room_id: str, user_id: int):
    """Get room if user is member, else 404"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, m.role as user_role, m.unread_count
        FROM chat_rooms r
        JOIN chat_room_members m ON m.room_id = r.id
        WHERE r.id = %s AND m.user_id = %s AND r.is_archived = FALSE
    """, (room_id, user_id))
    room = cursor.fetchone()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


def check_room_permission(conn, room_id: str, user_id: int, required_roles: List[str]):
    """Check if user has required role in room"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role FROM chat_room_members
        WHERE room_id = %s AND user_id = %s
    """, (room_id, user_id))
    result = cursor.fetchone()
    if not result or result['role'] not in required_roles:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return result['role']


# ============================================
# Rooms Endpoints
# ============================================

@router.get("/rooms", response_model=List[ChatRoomListItem])
async def list_my_rooms(
    room_type: Optional[RoomType] = None,
    include_archived: bool = False,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Liste les rooms où je suis membre"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        query = """
            SELECT r.id, r.name, r.room_type, r.color, r.avatar_url,
                   r.member_count, r.last_message_at, r.last_message_preview,
                   m.unread_count
            FROM chat_rooms r
            JOIN chat_room_members m ON m.room_id = r.id
            WHERE m.user_id = %s
        """
        params = [current_user.id]

        if not include_archived:
            query += " AND r.is_archived = FALSE"

        if room_type:
            query += " AND r.room_type = %s"
            params.append(room_type.value)

        query += " ORDER BY r.last_message_at DESC NULLS LAST"

        cursor.execute(query, params)
        rooms = cursor.fetchall()

        return [ChatRoomListItem(**dict(r)) for r in rooms]
    finally:
        conn.close()


@router.post("/rooms", response_model=ChatRoom, status_code=status.HTTP_201_CREATED)
async def create_room(
    data: ChatRoomCreate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Créer une nouvelle room"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Créer la room
        cursor.execute("""
            INSERT INTO chat_rooms (tenant_id, name, description, room_type, color,
                                   is_private, allow_invites, max_members,
                                   project_id, agent_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            str(current_user.tenant_id), data.name, data.description,
            data.room_type.value, data.color, data.is_private, data.allow_invites,
            data.max_members, data.project_id, data.agent_id
        ))
        room = cursor.fetchone()
        room_id = room['id']

        # Ajouter le créateur comme owner
        cursor.execute("""
            INSERT INTO chat_room_members (room_id, user_id, role)
            VALUES (%s, %s, 'owner')
        """, (room_id, current_user.id))

        # Ajouter les membres initiaux
        member_count = 1
        for member_id in data.initial_members:
            if member_id != current_user.id:
                cursor.execute("""
                    INSERT INTO chat_room_members (room_id, user_id, role)
                    VALUES (%s, %s, 'member')
                    ON CONFLICT (room_id, user_id) DO NOTHING
                """, (room_id, member_id))
                if cursor.rowcount > 0:
                    member_count += 1

        # Mettre à jour le compteur
        cursor.execute("""
            UPDATE chat_rooms SET member_count = %s WHERE id = %s
        """, (member_count, room_id))

        conn.commit()

        # Récupérer la room complète
        cursor.execute("SELECT * FROM chat_rooms WHERE id = %s", (room_id,))
        room = cursor.fetchone()

        logger.info(f"Room created: {room_id} by user {current_user.id}")
        return ChatRoom(**dict(room))
    except Exception as e:
        conn.rollback()
        logger.error(f"Error creating room: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@router.get("/rooms/{room_id}", response_model=ChatRoomWithMembers)
async def get_room(
    room_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Détail d'une room avec ses membres"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Vérifier accès et récupérer room
        room = get_room_or_404(conn, room_id, current_user.id)

        # Récupérer membres avec infos user
        cursor.execute("""
            SELECT m.*, u.username, u.email
            FROM chat_room_members m
            JOIN users u ON u.id = m.user_id
            WHERE m.room_id = %s
            ORDER BY m.role, m.joined_at
        """, (room_id,))
        members = [ChatRoomMember(**dict(m)) for m in cursor.fetchall()]

        room_data = dict(room)
        room_data['members'] = members
        return ChatRoomWithMembers(**room_data)
    finally:
        conn.close()


@router.put("/rooms/{room_id}", response_model=ChatRoom)
async def update_room(
    room_id: str,
    data: ChatRoomUpdate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Modifier une room (owner/admin)"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Vérifier permissions
        check_room_permission(conn, room_id, current_user.id, ['owner', 'admin'])

        # Construire la mise à jour
        updates = []
        params = []
        for field, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                updates.append(f"{field} = %s")
                params.append(value)

        if not updates:
            raise HTTPException(status_code=400, detail="No fields to update")

        params.append(room_id)
        cursor.execute(f"""
            UPDATE chat_rooms SET {', '.join(updates)}, updated_at = NOW()
            WHERE id = %s
            RETURNING *
        """, params)

        room = cursor.fetchone()
        conn.commit()

        # Notifier les membres
        await manager.broadcast_to_room(
            room_id,
            WSChatMessage(
                event=WSEventType.ROOM_UPDATED,
                room_id=room_id,
                sender_id=current_user.id,
                data={"room": dict(room)}
            ).to_dict()
        )

        return ChatRoom(**dict(room))
    finally:
        conn.close()


@router.delete("/rooms/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def archive_room(
    room_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Archiver une room (owner seulement)"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Seul le owner peut archiver
        check_room_permission(conn, room_id, current_user.id, ['owner'])

        cursor.execute("""
            UPDATE chat_rooms
            SET is_archived = TRUE, archived_at = NOW()
            WHERE id = %s
        """, (room_id,))

        conn.commit()
        logger.info(f"Room archived: {room_id} by user {current_user.id}")
    finally:
        conn.close()


# ============================================
# Members Endpoints
# ============================================

@router.get("/rooms/{room_id}/members", response_model=List[ChatRoomMember])
async def list_room_members(
    room_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Liste des membres d'une room"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Vérifier accès
        get_room_or_404(conn, room_id, current_user.id)

        cursor.execute("""
            SELECT m.*, u.username, u.email
            FROM chat_room_members m
            JOIN users u ON u.id = m.user_id
            WHERE m.room_id = %s
            ORDER BY m.role, m.joined_at
        """, (room_id,))

        return [ChatRoomMember(**dict(m)) for m in cursor.fetchall()]
    finally:
        conn.close()


@router.post("/rooms/{room_id}/members", response_model=ChatRoomMember, status_code=status.HTTP_201_CREATED)
async def add_room_member(
    room_id: str,
    data: ChatRoomMemberAdd,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Ajouter un membre à une room"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Vérifier permissions (owner/admin ou allow_invites)
        cursor.execute("""
            SELECT r.allow_invites, r.max_members, r.member_count, m.role
            FROM chat_rooms r
            JOIN chat_room_members m ON m.room_id = r.id
            WHERE r.id = %s AND m.user_id = %s
        """, (room_id, current_user.id))
        room_info = cursor.fetchone()

        if not room_info:
            raise HTTPException(status_code=404, detail="Room not found")

        if room_info['role'] not in ['owner', 'admin'] and not room_info['allow_invites']:
            raise HTTPException(status_code=403, detail="You cannot add members")

        if room_info['member_count'] >= room_info['max_members']:
            raise HTTPException(status_code=400, detail="Room is full")

        # Ajouter le membre
        cursor.execute("""
            INSERT INTO chat_room_members (room_id, user_id, role)
            VALUES (%s, %s, %s)
            ON CONFLICT (room_id, user_id) DO NOTHING
            RETURNING *
        """, (room_id, data.user_id, data.role.value))

        member = cursor.fetchone()
        if not member:
            raise HTTPException(status_code=409, detail="User is already a member")

        # Mettre à jour le compteur
        cursor.execute("""
            UPDATE chat_rooms SET member_count = member_count + 1 WHERE id = %s
        """, (room_id,))

        conn.commit()

        # Joindre la room WebSocket
        await manager.join_room(data.user_id, room_id)

        # Notifier
        cursor.execute("SELECT username FROM users WHERE id = %s", (data.user_id,))
        user_info = cursor.fetchone()

        await manager.broadcast_to_room(
            room_id,
            WSChatMessage(
                event=WSEventType.ROOM_JOINED,
                room_id=room_id,
                sender_id=data.user_id,
                data={"user_id": data.user_id, "username": user_info['username'] if user_info else None}
            ).to_dict()
        )

        return ChatRoomMember(**dict(member))
    finally:
        conn.close()


@router.delete("/rooms/{room_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_room_member(
    room_id: str,
    user_id: int,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Retirer un membre d'une room"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # On peut se retirer soi-même, ou owner/admin peut retirer quelqu'un
        if user_id != current_user.id:
            check_room_permission(conn, room_id, current_user.id, ['owner', 'admin'])

        # Vérifier qu'on ne retire pas le owner
        cursor.execute("""
            SELECT role FROM chat_room_members WHERE room_id = %s AND user_id = %s
        """, (room_id, user_id))
        member = cursor.fetchone()

        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        if member['role'] == 'owner':
            raise HTTPException(status_code=400, detail="Cannot remove the owner")

        cursor.execute("""
            DELETE FROM chat_room_members WHERE room_id = %s AND user_id = %s
        """, (room_id, user_id))

        cursor.execute("""
            UPDATE chat_rooms SET member_count = member_count - 1 WHERE id = %s
        """, (room_id,))

        conn.commit()

        # Quitter la room WebSocket
        await manager.leave_room(user_id, room_id)
    finally:
        conn.close()


# ============================================
# Messages Endpoints
# ============================================

@router.get("/rooms/{room_id}/messages", response_model=ChatMessageList)
async def get_room_messages(
    room_id: str,
    before_id: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Récupérer les messages d'une room (pagination cursor)"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Vérifier accès
        get_room_or_404(conn, room_id, current_user.id)

        # Query avec pagination
        query = """
            SELECT m.*, u.username as sender_username
            FROM chat_room_messages m
            JOIN users u ON u.id = m.sender_id
            WHERE m.room_id = %s AND m.is_deleted = FALSE
        """
        params = [room_id]

        if before_id:
            query += " AND m.created_at < (SELECT created_at FROM chat_room_messages WHERE id = %s)"
            params.append(before_id)

        query += " ORDER BY m.created_at DESC LIMIT %s"
        params.append(limit + 1)  # +1 pour détecter has_more

        cursor.execute(query, params)
        messages = cursor.fetchall()

        has_more = len(messages) > limit
        if has_more:
            messages = messages[:-1]

        # Total count
        cursor.execute("""
            SELECT COUNT(*) as total FROM chat_room_messages
            WHERE room_id = %s AND is_deleted = FALSE
        """, (room_id,))
        total = cursor.fetchone()['total']

        return ChatMessageList(
            messages=[ChatRoomMessage(**dict(m)) for m in reversed(messages)],
            total=total,
            has_more=has_more,
            oldest_id=messages[-1]['id'] if messages else None
        )
    finally:
        conn.close()


@router.post("/rooms/{room_id}/messages", response_model=ChatRoomMessage, status_code=status.HTTP_201_CREATED)
async def send_room_message(
    room_id: str,
    data: ChatMessageCreate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Envoyer un message dans une room"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Vérifier accès (membre qui peut écrire)
        role = check_room_permission(conn, room_id, current_user.id, ['owner', 'admin', 'member'])

        # Créer le message
        cursor.execute("""
            INSERT INTO chat_room_messages (room_id, sender_id, content, content_type,
                                           reply_to_id, mentions, attachments)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            room_id, current_user.id, data.content, data.content_type.value,
            data.reply_to_id, data.mentions, data.attachments
        ))
        message = cursor.fetchone()

        # Preview pour la room
        preview = data.content[:50] + ('...' if len(data.content) > 50 else '')

        # Mettre à jour la room
        cursor.execute("""
            UPDATE chat_rooms
            SET message_count = message_count + 1,
                last_message_at = NOW(),
                last_message_preview = %s
            WHERE id = %s
        """, (preview, room_id))

        # Incrémenter unread pour les autres membres
        cursor.execute("""
            UPDATE chat_room_members
            SET unread_count = unread_count + 1
            WHERE room_id = %s AND user_id != %s
        """, (room_id, current_user.id))

        conn.commit()

        # Récupérer message complet avec username
        cursor.execute("""
            SELECT m.*, u.username as sender_username
            FROM chat_room_messages m
            JOIN users u ON u.id = m.sender_id
            WHERE m.id = %s
        """, (message['id'],))
        message = cursor.fetchone()

        # Clear typing indicator
        await manager.set_typing(current_user.id, room_id, False)

        # Broadcast via WebSocket
        message_data = dict(message)
        await manager.send_chat_message(room_id, current_user.id, message_data)

        return ChatRoomMessage(**message_data)
    finally:
        conn.close()


@router.put("/messages/{message_id}", response_model=ChatRoomMessage)
async def edit_message(
    message_id: str,
    data: ChatMessageUpdate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Éditer un de mes messages"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Vérifier propriété du message
        cursor.execute("""
            SELECT * FROM chat_room_messages WHERE id = %s
        """, (message_id,))
        message = cursor.fetchone()

        if not message:
            raise HTTPException(status_code=404, detail="Message not found")

        if message['sender_id'] != current_user.id:
            raise HTTPException(status_code=403, detail="You can only edit your own messages")

        if message['is_deleted']:
            raise HTTPException(status_code=400, detail="Cannot edit deleted message")

        # Sauvegarder l'original si première édition
        original_content = message['original_content'] or message['content']

        cursor.execute("""
            UPDATE chat_room_messages
            SET content = %s, is_edited = TRUE, edited_at = NOW(), original_content = %s
            WHERE id = %s
            RETURNING *
        """, (data.content, original_content, message_id))

        updated = cursor.fetchone()
        conn.commit()

        # Notifier via WebSocket
        await manager.send_message_edited(
            message['room_id'],
            current_user.id,
            message_id,
            data.content
        )

        return ChatRoomMessage(**dict(updated))
    finally:
        conn.close()


@router.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Supprimer un de mes messages (soft delete)"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT room_id, sender_id FROM chat_room_messages WHERE id = %s
        """, (message_id,))
        message = cursor.fetchone()

        if not message:
            raise HTTPException(status_code=404, detail="Message not found")

        # Peut supprimer ses propres messages ou owner/admin de la room
        if message['sender_id'] != current_user.id:
            check_room_permission(conn, message['room_id'], current_user.id, ['owner', 'admin'])

        cursor.execute("""
            UPDATE chat_room_messages
            SET is_deleted = TRUE, deleted_at = NOW(), content = '[Message supprimé]'
            WHERE id = %s
        """, (message_id,))

        conn.commit()

        await manager.send_message_deleted(message['room_id'], current_user.id, message_id)
    finally:
        conn.close()


@router.post("/messages/{message_id}/reactions")
async def react_to_message(
    message_id: str,
    data: ChatMessageReaction,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Ajouter/retirer une réaction à un message"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT room_id, reactions FROM chat_room_messages WHERE id = %s
        """, (message_id,))
        message = cursor.fetchone()

        if not message:
            raise HTTPException(status_code=404, detail="Message not found")

        # Vérifier accès à la room
        get_room_or_404(conn, message['room_id'], current_user.id)

        reactions = message['reactions'] or {}

        if data.action == 'add':
            if data.emoji not in reactions:
                reactions[data.emoji] = []
            if current_user.id not in reactions[data.emoji]:
                reactions[data.emoji].append(current_user.id)
        else:  # remove
            if data.emoji in reactions and current_user.id in reactions[data.emoji]:
                reactions[data.emoji].remove(current_user.id)
                if not reactions[data.emoji]:
                    del reactions[data.emoji]

        cursor.execute("""
            UPDATE chat_room_messages SET reactions = %s WHERE id = %s
        """, (reactions, message_id))

        conn.commit()

        await manager.send_reaction(
            message['room_id'],
            current_user.id,
            message_id,
            data.emoji,
            data.action
        )

        return {"reactions": reactions}
    finally:
        conn.close()


# ============================================
# Invitations Endpoints
# ============================================

@router.post("/rooms/{room_id}/invitations", response_model=ChatRoomInvitation)
async def create_invitation(
    room_id: str,
    data: InvitationCreateByUser | InvitationCreateByEmail,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Créer une invitation à rejoindre une room"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Vérifier permissions et récupérer infos room
        cursor.execute("""
            SELECT r.id, r.name, r.room_type, r.color, r.allow_invites, r.member_count,
                   m.role
            FROM chat_rooms r
            JOIN chat_room_members m ON m.room_id = r.id
            WHERE r.id = %s AND m.user_id = %s
        """, (room_id, current_user.id))
        room_info = cursor.fetchone()

        if not room_info:
            raise HTTPException(status_code=404, detail="Room not found")

        if room_info['role'] not in ['owner', 'admin'] and not room_info['allow_invites']:
            raise HTTPException(status_code=403, detail="You cannot invite members")

        # Générer token
        token = secrets.token_urlsafe(32)

        # Déterminer invitee
        invitee_id = getattr(data, 'invitee_id', None)
        invitee_email = getattr(data, 'invitee_email', None)

        cursor.execute("""
            INSERT INTO chat_room_invitations
            (room_id, inviter_id, invitee_id, invitee_email, invite_token, assigned_role, message)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            room_id, current_user.id, invitee_id, invitee_email,
            token, data.assigned_role.value, data.message
        ))

        invitation = cursor.fetchone()
        conn.commit()

        # Envoyer email si invitee_email est fourni
        if invitee_email:
            try:
                notification_service = get_notification_service()

                # Récupérer le username de l'inviter
                cursor.execute("SELECT username, full_name FROM users WHERE id = %s", (current_user.id,))
                inviter_info = cursor.fetchone()
                inviter_name = inviter_info['full_name'] or inviter_info['username'] if inviter_info else f"User {current_user.id}"

                email_result = notification_service.send_chat_invitation_email(
                    to_email=invitee_email,
                    inviter_name=inviter_name,
                    room_name=room_info['name'],
                    room_type=room_info['room_type'],
                    member_count=room_info['member_count'],
                    invite_token=token,
                    invite_message=data.message,
                    expires_at=invitation['expires_at'],
                    room_color=room_info['color'] or '#6366f1',
                )

                if email_result.get('success'):
                    logger.info(f"Invitation email sent to {invitee_email} for room {room_id}")
                else:
                    logger.warning(f"Failed to send invitation email: {email_result.get('error')}")
            except Exception as e:
                logger.error(f"Error sending invitation email: {e}")
                # Don't fail the invitation creation if email fails

        logger.info(f"Invitation created: {token} for room {room_id}")
        return ChatRoomInvitation(**dict(invitation))
    finally:
        conn.close()


@router.get("/invitations", response_model=List[ChatRoomInvitation])
async def list_my_invitations(
    status: Optional[InvitationStatus] = InvitationStatus.PENDING,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Liste mes invitations reçues"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT i.*, u.username as inviter_username, r.name as room_name
            FROM chat_room_invitations i
            JOIN users u ON u.id = i.inviter_id
            JOIN chat_rooms r ON r.id = i.room_id
            WHERE i.invitee_id = %s AND i.status = %s
            ORDER BY i.created_at DESC
        """, (current_user.id, status.value))

        return [ChatRoomInvitation(**dict(i)) for i in cursor.fetchall()]
    finally:
        conn.close()


@router.get("/invitations/{token}", response_model=InvitationPublicInfo)
async def get_invitation_info(token: str):
    """Info publique d'une invitation (pour landing page)"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT i.*, r.name as room_name, r.room_type, r.member_count,
                   u.username as inviter_username
            FROM chat_room_invitations i
            JOIN chat_rooms r ON r.id = i.room_id
            JOIN users u ON u.id = i.inviter_id
            WHERE i.invite_token = %s
        """, (token,))

        invitation = cursor.fetchone()
        if not invitation:
            raise HTTPException(status_code=404, detail="Invitation not found")

        is_valid = (
            invitation['status'] == 'pending' and
            invitation['expires_at'] > datetime.utcnow()
        )

        return InvitationPublicInfo(
            room_name=invitation['room_name'],
            room_type=invitation['room_type'],
            inviter_username=invitation['inviter_username'],
            member_count=invitation['member_count'],
            expires_at=invitation['expires_at'],
            is_valid=is_valid
        )
    finally:
        conn.close()


@router.post("/invitations/{token}", response_model=dict)
async def respond_to_invitation(
    token: str,
    data: InvitationResponse,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Accepter ou refuser une invitation"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM chat_room_invitations
            WHERE invite_token = %s AND status = 'pending' AND expires_at > NOW()
        """, (token,))
        invitation = cursor.fetchone()

        if not invitation:
            raise HTTPException(status_code=404, detail="Invalid or expired invitation")

        # Vérifier que l'invitation est pour cet user (si spécifié)
        if invitation['invitee_id'] and invitation['invitee_id'] != current_user.id:
            raise HTTPException(status_code=403, detail="This invitation is for another user")

        if data.accept:
            # Ajouter le membre
            cursor.execute("""
                INSERT INTO chat_room_members (room_id, user_id, role)
                VALUES (%s, %s, %s)
                ON CONFLICT (room_id, user_id) DO NOTHING
            """, (invitation['room_id'], current_user.id, invitation['assigned_role']))

            if cursor.rowcount > 0:
                cursor.execute("""
                    UPDATE chat_rooms SET member_count = member_count + 1 WHERE id = %s
                """, (invitation['room_id'],))

            status = 'accepted'

            # Join WebSocket room
            await manager.join_room(current_user.id, str(invitation['room_id']))
        else:
            status = 'declined'

        cursor.execute("""
            UPDATE chat_room_invitations
            SET status = %s, responded_at = NOW(), invitee_id = %s
            WHERE id = %s
        """, (status, current_user.id, invitation['id']))

        conn.commit()

        return {
            "status": status,
            "room_id": str(invitation['room_id']) if data.accept else None
        }
    finally:
        conn.close()


# ============================================
# Read Receipts & Typing
# ============================================

@router.post("/rooms/{room_id}/read")
async def mark_room_as_read(
    room_id: str,
    data: Optional[ReadReceiptCreate] = None,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Marquer les messages comme lus"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE chat_room_members
            SET last_read_at = NOW(), unread_count = 0
            WHERE room_id = %s AND user_id = %s
        """, (room_id, current_user.id))

        conn.commit()

        # Notifier via WebSocket
        if data and data.last_read_message_id:
            await manager.send_read_receipt(room_id, current_user.id, data.last_read_message_id)

        return {"status": "ok"}
    finally:
        conn.close()


@router.post("/rooms/{room_id}/typing")
async def set_typing_indicator(
    room_id: str,
    data: TypingIndicator,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Envoyer indicateur de frappe"""
    await manager.set_typing(current_user.id, room_id, data.is_typing)
    return {"status": "ok"}


@router.get("/rooms/{room_id}/status", response_model=RoomOnlineStatus)
async def get_room_status(
    room_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Obtenir le status en ligne de la room"""
    conn = get_db_connection()
    try:
        get_room_or_404(conn, room_id, current_user.id)

        return RoomOnlineStatus(
            room_id=room_id,
            online_users=manager.get_online_users_in_room(room_id),
            typing_users=manager.get_typing_users(room_id)
        )
    finally:
        conn.close()


# ============================================
# Direct Chat
# ============================================

@router.post("/direct", response_model=DirectChatResponse)
async def create_direct_chat(
    data: DirectChatCreate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Créer ou récupérer un chat direct avec un utilisateur"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Vérifier que l'utilisateur cible existe
        cursor.execute("SELECT id FROM users WHERE id = %s", (data.target_user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")

        # Chercher un chat direct existant
        cursor.execute("""
            SELECT r.id
            FROM chat_rooms r
            JOIN chat_room_members m1 ON m1.room_id = r.id AND m1.user_id = %s
            JOIN chat_room_members m2 ON m2.room_id = r.id AND m2.user_id = %s
            WHERE r.room_type = 'direct' AND r.tenant_id = %s
            LIMIT 1
        """, (current_user.id, data.target_user_id, str(current_user.tenant_id)))

        existing = cursor.fetchone()
        if existing:
            return DirectChatResponse(room_id=str(existing['id']), is_new=False)

        # Créer le chat direct
        cursor.execute("""
            INSERT INTO chat_rooms (tenant_id, name, room_type, member_count)
            VALUES (%s, 'Direct Chat', 'direct', 2)
            RETURNING id
        """, (str(current_user.tenant_id),))
        room_id = cursor.fetchone()['id']

        # Ajouter les deux membres
        cursor.execute("""
            INSERT INTO chat_room_members (room_id, user_id, role)
            VALUES (%s, %s, 'member'), (%s, %s, 'member')
        """, (room_id, current_user.id, room_id, data.target_user_id))

        conn.commit()

        return DirectChatResponse(room_id=str(room_id), is_new=True)
    finally:
        conn.close()
