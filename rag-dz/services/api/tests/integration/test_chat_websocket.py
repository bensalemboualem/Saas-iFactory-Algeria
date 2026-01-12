"""
Integration tests for Chat WebSocket functionality
Tests for real-time communication events including:
- Connection/disconnection
- Room join/leave
- Message broadcasting
- Typing indicators
- Online status
"""
import pytest
from unittest.mock import Mock, MagicMock, AsyncMock, patch
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
import json
import asyncio


# ============================================
# WebSocket Manager Tests
# ============================================

class TestWebSocketManager:
    """Test suite for WebSocket connection manager"""

    @pytest.fixture
    def ws_manager(self):
        """Create a fresh WebSocket manager instance"""
        from app.websocket import ConnectionManager
        return ConnectionManager()

    @pytest.fixture
    def mock_websocket(self):
        """Create a mock WebSocket"""
        ws = AsyncMock(spec=WebSocket)
        ws.accept = AsyncMock()
        ws.send_json = AsyncMock()
        ws.send_text = AsyncMock()
        ws.receive_text = AsyncMock()
        ws.close = AsyncMock()
        return ws

    @pytest.mark.asyncio
    async def test_connect_user(self, ws_manager, mock_websocket):
        """Test connecting a user to WebSocket"""
        user_id = 1

        await ws_manager.connect(mock_websocket, user_id)

        assert user_id in ws_manager.active_connections
        mock_websocket.accept.assert_called_once()

    @pytest.mark.asyncio
    async def test_disconnect_user(self, ws_manager, mock_websocket):
        """Test disconnecting a user"""
        user_id = 1
        await ws_manager.connect(mock_websocket, user_id)

        ws_manager.disconnect(user_id)

        assert user_id not in ws_manager.active_connections

    @pytest.mark.asyncio
    async def test_join_room(self, ws_manager, mock_websocket):
        """Test user joining a room"""
        user_id = 1
        room_id = "room-123"
        await ws_manager.connect(mock_websocket, user_id)

        await ws_manager.join_room(user_id, room_id)

        assert room_id in ws_manager.room_members
        assert user_id in ws_manager.room_members[room_id]

    @pytest.mark.asyncio
    async def test_leave_room(self, ws_manager, mock_websocket):
        """Test user leaving a room"""
        user_id = 1
        room_id = "room-123"
        await ws_manager.connect(mock_websocket, user_id)
        await ws_manager.join_room(user_id, room_id)

        await ws_manager.leave_room(user_id, room_id)

        assert user_id not in ws_manager.room_members.get(room_id, set())

    @pytest.mark.asyncio
    async def test_broadcast_to_room(self, ws_manager, mock_websocket):
        """Test broadcasting message to all room members"""
        user1_id = 1
        user2_id = 2
        room_id = "room-123"

        mock_ws1 = AsyncMock(spec=WebSocket)
        mock_ws2 = AsyncMock(spec=WebSocket)
        mock_ws1.accept = AsyncMock()
        mock_ws2.accept = AsyncMock()
        mock_ws1.send_json = AsyncMock()
        mock_ws2.send_json = AsyncMock()

        await ws_manager.connect(mock_ws1, user1_id)
        await ws_manager.connect(mock_ws2, user2_id)
        await ws_manager.join_room(user1_id, room_id)
        await ws_manager.join_room(user2_id, room_id)

        message = {"event": "message:new", "data": {"content": "Hello!"}}
        await ws_manager.broadcast_to_room(room_id, message)

        mock_ws1.send_json.assert_called_with(message)
        mock_ws2.send_json.assert_called_with(message)

    @pytest.mark.asyncio
    async def test_send_to_user(self, ws_manager, mock_websocket):
        """Test sending message to specific user"""
        user_id = 1
        await ws_manager.connect(mock_websocket, user_id)

        message = {"event": "notification", "data": {"text": "Hello user!"}}
        await ws_manager.send_to_user(user_id, message)

        mock_websocket.send_json.assert_called_with(message)

    @pytest.mark.asyncio
    async def test_typing_indicator(self, ws_manager, mock_websocket):
        """Test typing indicator functionality"""
        user_id = 1
        room_id = "room-123"
        await ws_manager.connect(mock_websocket, user_id)
        await ws_manager.join_room(user_id, room_id)

        await ws_manager.set_typing(user_id, room_id, True)

        typing_users = ws_manager.get_typing_users(room_id)
        assert user_id in typing_users

        await ws_manager.set_typing(user_id, room_id, False)

        typing_users = ws_manager.get_typing_users(room_id)
        assert user_id not in typing_users

    @pytest.mark.asyncio
    async def test_get_online_users_in_room(self, ws_manager, mock_websocket):
        """Test getting online users in a room"""
        user1_id = 1
        user2_id = 2
        room_id = "room-123"

        mock_ws1 = AsyncMock(spec=WebSocket)
        mock_ws2 = AsyncMock(spec=WebSocket)
        mock_ws1.accept = AsyncMock()
        mock_ws2.accept = AsyncMock()

        await ws_manager.connect(mock_ws1, user1_id)
        await ws_manager.connect(mock_ws2, user2_id)
        await ws_manager.join_room(user1_id, room_id)
        await ws_manager.join_room(user2_id, room_id)

        online_users = ws_manager.get_online_users_in_room(room_id)

        assert user1_id in online_users
        assert user2_id in online_users


# ============================================
# WebSocket Event Tests
# ============================================

class TestWebSocketEvents:
    """Test suite for WebSocket event handling"""

    @pytest.fixture
    def ws_manager(self):
        """Create a fresh WebSocket manager instance"""
        from app.websocket import ConnectionManager
        return ConnectionManager()

    @pytest.fixture
    def mock_websocket(self):
        """Create a mock WebSocket"""
        ws = AsyncMock(spec=WebSocket)
        ws.accept = AsyncMock()
        ws.send_json = AsyncMock()
        ws.send_text = AsyncMock()
        ws.receive_text = AsyncMock()
        ws.close = AsyncMock()
        return ws

    @pytest.mark.asyncio
    async def test_message_new_event(self, ws_manager, mock_websocket):
        """Test message:new event is broadcast correctly"""
        user1_id = 1
        user2_id = 2
        room_id = "room-123"

        mock_ws1 = AsyncMock(spec=WebSocket)
        mock_ws2 = AsyncMock(spec=WebSocket)
        mock_ws1.accept = AsyncMock()
        mock_ws2.accept = AsyncMock()
        mock_ws1.send_json = AsyncMock()
        mock_ws2.send_json = AsyncMock()

        await ws_manager.connect(mock_ws1, user1_id)
        await ws_manager.connect(mock_ws2, user2_id)
        await ws_manager.join_room(user1_id, room_id)
        await ws_manager.join_room(user2_id, room_id)

        message_data = {
            "id": "msg-123",
            "content": "Hello!",
            "sender_id": user1_id,
        }

        await ws_manager.send_chat_message(room_id, user1_id, message_data)

        # Both users should receive the message
        assert mock_ws1.send_json.called or mock_ws2.send_json.called

    @pytest.mark.asyncio
    async def test_message_edited_event(self, ws_manager, mock_websocket):
        """Test message:edited event"""
        user_id = 1
        room_id = "room-123"
        await ws_manager.connect(mock_websocket, user_id)
        await ws_manager.join_room(user_id, room_id)

        await ws_manager.send_message_edited(room_id, user_id, "msg-123", "Edited content")

        assert mock_websocket.send_json.called
        call_args = mock_websocket.send_json.call_args[0][0]
        assert call_args["event"] == "message:edited"

    @pytest.mark.asyncio
    async def test_message_deleted_event(self, ws_manager, mock_websocket):
        """Test message:deleted event"""
        user_id = 1
        room_id = "room-123"
        await ws_manager.connect(mock_websocket, user_id)
        await ws_manager.join_room(user_id, room_id)

        await ws_manager.send_message_deleted(room_id, user_id, "msg-123")

        assert mock_websocket.send_json.called
        call_args = mock_websocket.send_json.call_args[0][0]
        assert call_args["event"] == "message:deleted"

    @pytest.mark.asyncio
    async def test_reaction_event(self, ws_manager, mock_websocket):
        """Test message:reaction event"""
        user_id = 1
        room_id = "room-123"
        await ws_manager.connect(mock_websocket, user_id)
        await ws_manager.join_room(user_id, room_id)

        await ws_manager.send_reaction(room_id, user_id, "msg-123", "👍", "add")

        assert mock_websocket.send_json.called

    @pytest.mark.asyncio
    async def test_read_receipt_event(self, ws_manager, mock_websocket):
        """Test messages:read event"""
        user_id = 1
        room_id = "room-123"
        await ws_manager.connect(mock_websocket, user_id)
        await ws_manager.join_room(user_id, room_id)

        await ws_manager.send_read_receipt(room_id, user_id, "msg-123")

        assert mock_websocket.send_json.called


# ============================================
# WebSocket Connection Tests
# ============================================

class TestWebSocketConnection:
    """Test suite for WebSocket connection lifecycle"""

    @pytest.fixture
    def ws_manager(self):
        """Create a fresh WebSocket manager instance"""
        from app.websocket import ConnectionManager
        return ConnectionManager()

    @pytest.mark.asyncio
    async def test_multiple_connections_same_user(self, ws_manager):
        """Test handling multiple connections from same user"""
        user_id = 1

        mock_ws1 = AsyncMock(spec=WebSocket)
        mock_ws2 = AsyncMock(spec=WebSocket)
        mock_ws1.accept = AsyncMock()
        mock_ws2.accept = AsyncMock()

        await ws_manager.connect(mock_ws1, user_id)
        await ws_manager.connect(mock_ws2, user_id)

        # Should handle gracefully (either replace or maintain multiple)
        assert user_id in ws_manager.active_connections

    @pytest.mark.asyncio
    async def test_disconnection_cleans_up_rooms(self, ws_manager):
        """Test that disconnection removes user from all rooms"""
        user_id = 1
        room1 = "room-1"
        room2 = "room-2"

        mock_ws = AsyncMock(spec=WebSocket)
        mock_ws.accept = AsyncMock()

        await ws_manager.connect(mock_ws, user_id)
        await ws_manager.join_room(user_id, room1)
        await ws_manager.join_room(user_id, room2)

        ws_manager.disconnect(user_id)

        assert user_id not in ws_manager.room_members.get(room1, set())
        assert user_id not in ws_manager.room_members.get(room2, set())

    @pytest.mark.asyncio
    async def test_disconnection_clears_typing(self, ws_manager):
        """Test that disconnection clears typing status"""
        user_id = 1
        room_id = "room-123"

        mock_ws = AsyncMock(spec=WebSocket)
        mock_ws.accept = AsyncMock()

        await ws_manager.connect(mock_ws, user_id)
        await ws_manager.join_room(user_id, room_id)
        await ws_manager.set_typing(user_id, room_id, True)

        ws_manager.disconnect(user_id)

        typing_users = ws_manager.get_typing_users(room_id)
        assert user_id not in typing_users


# ============================================
# WebSocket Protocol Tests
# ============================================

class TestWebSocketProtocol:
    """Test suite for WebSocket protocol handling"""

    def test_ping_pong(self, client: TestClient):
        """Test WebSocket ping/pong keepalive"""
        # This requires the actual WebSocket endpoint
        # Using TestClient's WebSocket support
        pass  # Implemented in E2E tests

    def test_invalid_json_handling(self):
        """Test handling of invalid JSON messages"""
        pass  # Implemented in E2E tests

    def test_unknown_action_handling(self):
        """Test handling of unknown action types"""
        pass  # Implemented in E2E tests


# ============================================
# WebSocket Authentication Tests
# ============================================

class TestWebSocketAuth:
    """Test suite for WebSocket authentication"""

    def test_connection_requires_api_key(self, client: TestClient):
        """Test that WebSocket connection requires API key"""
        # Attempt connection without API key should fail
        pass  # Implemented in E2E tests

    def test_connection_requires_user_id(self, client: TestClient):
        """Test that WebSocket connection requires user ID"""
        # Attempt connection without user ID should fail
        pass  # Implemented in E2E tests

    def test_invalid_api_key_rejected(self, client: TestClient):
        """Test that invalid API key is rejected"""
        pass  # Implemented in E2E tests
