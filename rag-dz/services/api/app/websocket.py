"""
WebSocket support for real-time updates
Extended with chat room support for multi-user messaging
"""
import logging
import json
from typing import Dict, Set, Optional, List
from fastapi import WebSocket, WebSocketDisconnect
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================================
# WebSocket Event Types
# ============================================================

class WSEventType(str, Enum):
    """WebSocket event types for chat"""
    # Connection events
    CONNECTION = "connection"
    PONG = "pong"

    # Room events
    ROOM_JOINED = "room:joined"
    ROOM_LEFT = "room:left"
    ROOM_UPDATED = "room:updated"

    # Message events
    MESSAGE_NEW = "message:new"
    MESSAGE_EDITED = "message:edited"
    MESSAGE_DELETED = "message:deleted"
    MESSAGE_REACTION = "message:reaction"

    # Presence events
    USER_TYPING = "user:typing"
    USER_STOPPED_TYPING = "user:stopped_typing"
    USER_ONLINE = "user:online"
    USER_OFFLINE = "user:offline"

    # Read receipts
    MESSAGES_READ = "messages:read"

    # Progress (existing)
    PROGRESS = "progress"


@dataclass
class ChatMessage:
    """Chat message payload for WebSocket"""
    event: str
    room_id: str
    data: Dict
    sender_id: Optional[int] = None
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            "event": self.event,
            "room_id": self.room_id,
            "sender_id": self.sender_id,
            "data": self.data,
            "timestamp": self.timestamp
        }


@dataclass
class ProgressUpdate:
    """Progress update message"""
    operation_id: str
    status: str  # 'started', 'progress', 'completed', 'error'
    progress: int  # 0-100
    message: str
    data: Dict = None
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self):
        result = asdict(self)
        if result['data'] is None:
            result['data'] = {}
        return result


@dataclass
class UserConnection:
    """Represents a user's WebSocket connection with metadata"""
    websocket: WebSocket
    user_id: int
    tenant_id: str
    rooms: Set[str] = field(default_factory=set)
    connected_at: str = None

    def __post_init__(self):
        if self.connected_at is None:
            self.connected_at = datetime.utcnow().isoformat()

    def __hash__(self):
        return hash(id(self.websocket))

    def __eq__(self, other):
        if isinstance(other, UserConnection):
            return id(self.websocket) == id(other.websocket)
        return False


class ConnectionManager:
    """Manage WebSocket connections with room support"""

    def __init__(self):
        # tenant_id -> Set of WebSocket connections (legacy)
        self.active_connections: Dict[str, Set[WebSocket]] = {}

        # user_id -> UserConnection (new: tracks user's connection + rooms)
        self.user_connections: Dict[int, UserConnection] = {}

        # room_id -> Set of user_ids (who's in which room)
        self.room_members: Dict[str, Set[int]] = {}

        # Track typing indicators: room_id -> Set of user_ids
        self.typing_users: Dict[str, Set[int]] = {}

    async def connect(self, websocket: WebSocket, tenant_id: str, user_id: int = None):
        """Accept and store WebSocket connection"""
        await websocket.accept()

        # Legacy: tenant-based connections
        if tenant_id not in self.active_connections:
            self.active_connections[tenant_id] = set()
        self.active_connections[tenant_id].add(websocket)

        # New: user-based connections
        if user_id:
            self.user_connections[user_id] = UserConnection(
                websocket=websocket,
                user_id=user_id,
                tenant_id=tenant_id
            )
            logger.info(f"WebSocket connected for user {user_id} (tenant {tenant_id})")
        else:
            logger.info(f"WebSocket connected for tenant {tenant_id}")

    def disconnect(self, websocket: WebSocket, tenant_id: str, user_id: int = None):
        """Remove WebSocket connection"""
        # Legacy cleanup
        if tenant_id in self.active_connections:
            self.active_connections[tenant_id].discard(websocket)
            if not self.active_connections[tenant_id]:
                del self.active_connections[tenant_id]

        # New: user-based cleanup
        if user_id and user_id in self.user_connections:
            user_conn = self.user_connections[user_id]
            # Remove from all rooms
            for room_id in user_conn.rooms:
                if room_id in self.room_members:
                    self.room_members[room_id].discard(user_id)
                # Clear typing indicator
                if room_id in self.typing_users:
                    self.typing_users[room_id].discard(user_id)

            del self.user_connections[user_id]
            logger.info(f"WebSocket disconnected for user {user_id}")
        else:
            logger.info(f"WebSocket disconnected for tenant {tenant_id}")

    # ============================================================
    # Room Management
    # ============================================================

    async def join_room(self, user_id: int, room_id: str):
        """Add user to a chat room"""
        if user_id not in self.user_connections:
            logger.warning(f"User {user_id} not connected, cannot join room {room_id}")
            return False

        # Add to room_members
        if room_id not in self.room_members:
            self.room_members[room_id] = set()
        self.room_members[room_id].add(user_id)

        # Track in user's connection
        self.user_connections[user_id].rooms.add(room_id)

        logger.info(f"User {user_id} joined room {room_id}")

        # Notify room members
        await self.broadcast_to_room(
            room_id,
            ChatMessage(
                event=WSEventType.USER_ONLINE,
                room_id=room_id,
                sender_id=user_id,
                data={"user_id": user_id}
            ).to_dict(),
            exclude_user=user_id
        )
        return True

    async def leave_room(self, user_id: int, room_id: str):
        """Remove user from a chat room"""
        if room_id in self.room_members:
            self.room_members[room_id].discard(user_id)
            if not self.room_members[room_id]:
                del self.room_members[room_id]

        if user_id in self.user_connections:
            self.user_connections[user_id].rooms.discard(room_id)

        # Clear typing
        if room_id in self.typing_users:
            self.typing_users[room_id].discard(user_id)

        logger.info(f"User {user_id} left room {room_id}")

        # Notify room members
        await self.broadcast_to_room(
            room_id,
            ChatMessage(
                event=WSEventType.USER_OFFLINE,
                room_id=room_id,
                sender_id=user_id,
                data={"user_id": user_id}
            ).to_dict()
        )

    def get_room_users(self, room_id: str) -> List[int]:
        """Get list of connected users in a room"""
        return list(self.room_members.get(room_id, set()))

    def is_user_in_room(self, user_id: int, room_id: str) -> bool:
        """Check if user is in a room"""
        return room_id in self.room_members and user_id in self.room_members[room_id]

    # ============================================================
    # Typing Indicators
    # ============================================================

    async def set_typing(self, user_id: int, room_id: str, is_typing: bool):
        """Update typing indicator for user in room"""
        if room_id not in self.typing_users:
            self.typing_users[room_id] = set()

        event_type = WSEventType.USER_TYPING if is_typing else WSEventType.USER_STOPPED_TYPING

        if is_typing:
            self.typing_users[room_id].add(user_id)
        else:
            self.typing_users[room_id].discard(user_id)

        await self.broadcast_to_room(
            room_id,
            ChatMessage(
                event=event_type,
                room_id=room_id,
                sender_id=user_id,
                data={"user_id": user_id}
            ).to_dict(),
            exclude_user=user_id
        )

    def get_typing_users(self, room_id: str) -> List[int]:
        """Get list of users currently typing in a room"""
        return list(self.typing_users.get(room_id, set()))

    # ============================================================
    # Message Sending
    # ============================================================

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific connection"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {e}")

    async def send_to_user(self, user_id: int, message: dict):
        """Send message to a specific user"""
        if user_id not in self.user_connections:
            logger.debug(f"User {user_id} not connected, message not sent")
            return False

        try:
            await self.user_connections[user_id].websocket.send_json(message)
            return True
        except Exception as e:
            logger.error(f"Error sending to user {user_id}: {e}")
            return False

    async def broadcast_to_room(
        self,
        room_id: str,
        message: dict,
        exclude_user: int = None
    ):
        """Broadcast message to all users in a room"""
        if room_id not in self.room_members:
            return

        disconnected_users = []
        for user_id in self.room_members[room_id]:
            if exclude_user and user_id == exclude_user:
                continue

            if user_id not in self.user_connections:
                continue

            try:
                await self.user_connections[user_id].websocket.send_json(message)
            except WebSocketDisconnect:
                disconnected_users.append(user_id)
            except Exception as e:
                logger.error(f"Error broadcasting to user {user_id} in room {room_id}: {e}")
                disconnected_users.append(user_id)

        # Clean up disconnected users
        for user_id in disconnected_users:
            if user_id in self.user_connections:
                tenant_id = self.user_connections[user_id].tenant_id
                websocket = self.user_connections[user_id].websocket
                self.disconnect(websocket, tenant_id, user_id)

    async def broadcast_to_tenant(self, tenant_id: str, message: dict):
        """Broadcast message to all connections of a tenant (legacy)"""
        if tenant_id not in self.active_connections:
            return

        disconnected = set()
        for connection in self.active_connections[tenant_id]:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected.add(connection)
            except Exception as e:
                logger.error(f"Error broadcasting to tenant {tenant_id}: {e}")
                disconnected.add(connection)

        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection, tenant_id)

    async def send_progress_update(
        self,
        tenant_id: str,
        operation_id: str,
        status: str,
        progress: int,
        message: str,
        data: Dict = None
    ):
        """Send progress update to tenant"""
        update = ProgressUpdate(
            operation_id=operation_id,
            status=status,
            progress=progress,
            message=message,
            data=data or {}
        )
        await self.broadcast_to_tenant(tenant_id, update.to_dict())

    # ============================================================
    # Chat-specific helpers
    # ============================================================

    async def send_chat_message(
        self,
        room_id: str,
        sender_id: int,
        message_data: dict
    ):
        """Send a new chat message to room members"""
        await self.broadcast_to_room(
            room_id,
            ChatMessage(
                event=WSEventType.MESSAGE_NEW,
                room_id=room_id,
                sender_id=sender_id,
                data=message_data
            ).to_dict()
        )

    async def send_message_edited(
        self,
        room_id: str,
        sender_id: int,
        message_id: str,
        new_content: str
    ):
        """Notify room that a message was edited"""
        await self.broadcast_to_room(
            room_id,
            ChatMessage(
                event=WSEventType.MESSAGE_EDITED,
                room_id=room_id,
                sender_id=sender_id,
                data={
                    "message_id": message_id,
                    "new_content": new_content
                }
            ).to_dict()
        )

    async def send_message_deleted(
        self,
        room_id: str,
        sender_id: int,
        message_id: str
    ):
        """Notify room that a message was deleted"""
        await self.broadcast_to_room(
            room_id,
            ChatMessage(
                event=WSEventType.MESSAGE_DELETED,
                room_id=room_id,
                sender_id=sender_id,
                data={"message_id": message_id}
            ).to_dict()
        )

    async def send_reaction(
        self,
        room_id: str,
        user_id: int,
        message_id: str,
        emoji: str,
        action: str  # 'add' or 'remove'
    ):
        """Notify room of a reaction change"""
        await self.broadcast_to_room(
            room_id,
            ChatMessage(
                event=WSEventType.MESSAGE_REACTION,
                room_id=room_id,
                sender_id=user_id,
                data={
                    "message_id": message_id,
                    "emoji": emoji,
                    "action": action,
                    "user_id": user_id
                }
            ).to_dict()
        )

    async def send_read_receipt(
        self,
        room_id: str,
        user_id: int,
        last_read_message_id: str
    ):
        """Notify room that user has read messages"""
        await self.broadcast_to_room(
            room_id,
            ChatMessage(
                event=WSEventType.MESSAGES_READ,
                room_id=room_id,
                sender_id=user_id,
                data={
                    "user_id": user_id,
                    "last_read_message_id": last_read_message_id
                }
            ).to_dict(),
            exclude_user=user_id
        )

    def get_online_users_in_room(self, room_id: str) -> List[int]:
        """Get list of online users in a room"""
        if room_id not in self.room_members:
            return []
        return [
            user_id for user_id in self.room_members[room_id]
            if user_id in self.user_connections
        ]

    def get_user_rooms(self, user_id: int) -> List[str]:
        """Get list of rooms a user is currently in"""
        if user_id not in self.user_connections:
            return []
        return list(self.user_connections[user_id].rooms)


# Global connection manager
manager = ConnectionManager()
