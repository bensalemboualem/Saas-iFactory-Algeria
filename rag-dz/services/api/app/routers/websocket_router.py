"""
WebSocket router for real-time updates
Extended with chat room support for multi-user messaging
"""
import logging
import json
from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from ..websocket import manager, WSEventType
from ..db import get_tenant_by_key, get_db_connection

logger = logging.getLogger(__name__)

router = APIRouter()


def get_user_by_api_key(api_key: str) -> Optional[dict]:
    """Get user info from API key"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.username, u.tenant_id
            FROM users u
            JOIN tenants t ON t.id = u.tenant_id
            WHERE t.api_key = %s
            LIMIT 1
        """, (api_key,))
        return cursor.fetchone()
    except Exception:
        return None
    finally:
        conn.close()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    api_key: str = Query(..., description="API key for authentication"),
    user_id: Optional[int] = Query(None, description="User ID for chat rooms")
):
    """
    WebSocket endpoint for real-time updates

    Query params:
        api_key: API key for authentication
        user_id: Optional user ID for chat room features

    Messages format (legacy progress):
        {
            "operation_id": "unique-id",
            "status": "started|progress|completed|error",
            "progress": 0-100,
            "message": "Status message",
            "data": {...}
        }

    Messages format (chat):
        {
            "action": "join_room|leave_room|typing|send_message",
            "room_id": "uuid",
            "data": {...}
        }
    """
    # Authenticate
    tenant = get_tenant_by_key(api_key)
    if not tenant:
        await websocket.close(code=4001, reason="Invalid API key")
        return

    tenant_id = tenant["id"]

    # Get user info if user_id provided
    actual_user_id = None
    if user_id:
        user_info = get_user_by_api_key(api_key)
        if user_info and user_info['id'] == user_id:
            actual_user_id = user_id
        else:
            # Try to verify user belongs to tenant
            conn = get_db_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id FROM users WHERE id = %s AND tenant_id = %s
                """, (user_id, tenant_id))
                if cursor.fetchone():
                    actual_user_id = user_id
            finally:
                conn.close()

    # Accept connection
    await manager.connect(websocket, tenant_id, actual_user_id)

    try:
        # Send welcome message
        welcome_data = {
            "type": "connection",
            "status": "connected",
            "tenant_id": tenant_id,
            "message": "WebSocket connected successfully"
        }
        if actual_user_id:
            welcome_data["user_id"] = actual_user_id
            welcome_data["chat_enabled"] = True

        await manager.send_personal_message(welcome_data, websocket)

        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()

            # Echo back for ping/pong
            if data == "ping":
                await manager.send_personal_message(
                    {"type": "pong"},
                    websocket
                )
                continue

            # Try to parse JSON for chat actions
            try:
                message = json.loads(data)
                action = message.get("action")
                room_id = message.get("room_id")

                if not actual_user_id:
                    await manager.send_personal_message(
                        {"type": "error", "message": "User ID required for chat actions"},
                        websocket
                    )
                    continue

                if action == "join_room" and room_id:
                    # Verify user is member of room before joining
                    conn = get_db_connection()
                    try:
                        cursor = conn.cursor()
                        cursor.execute("""
                            SELECT 1 FROM chat_room_members
                            WHERE room_id = %s AND user_id = %s
                        """, (room_id, actual_user_id))
                        if cursor.fetchone():
                            await manager.join_room(actual_user_id, room_id)
                            await manager.send_personal_message(
                                {"type": "room_joined", "room_id": room_id},
                                websocket
                            )
                        else:
                            await manager.send_personal_message(
                                {"type": "error", "message": "Not a member of this room"},
                                websocket
                            )
                    finally:
                        conn.close()

                elif action == "leave_room" and room_id:
                    await manager.leave_room(actual_user_id, room_id)
                    await manager.send_personal_message(
                        {"type": "room_left", "room_id": room_id},
                        websocket
                    )

                elif action == "typing" and room_id:
                    is_typing = message.get("is_typing", True)
                    await manager.set_typing(actual_user_id, room_id, is_typing)

                elif action == "get_online":
                    # Get online status for a room
                    if room_id:
                        online = manager.get_online_users_in_room(room_id)
                        typing = manager.get_typing_users(room_id)
                        await manager.send_personal_message(
                            {
                                "type": "online_status",
                                "room_id": room_id,
                                "online_users": online,
                                "typing_users": typing
                            },
                            websocket
                        )

                else:
                    logger.debug(f"Unknown action or missing room_id: {message}")

            except json.JSONDecodeError:
                # Not JSON, log and continue
                logger.debug(f"Received non-JSON WebSocket message: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket, tenant_id, actual_user_id)
        logger.info(f"Client disconnected: tenant {tenant_id}, user {actual_user_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket, tenant_id, actual_user_id)
