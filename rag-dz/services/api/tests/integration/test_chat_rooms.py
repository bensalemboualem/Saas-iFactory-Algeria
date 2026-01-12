"""
Integration tests for Chat Rooms API endpoints
Tests for multi-user chat functionality including:
- Room CRUD operations
- Member management
- Messages
- Invitations
- WebSocket events
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
import json
from datetime import datetime, timedelta
import secrets


# ============================================
# Fixtures
# ============================================

@pytest.fixture
def mock_db_connection():
    """Mock database connection with cursor"""
    with patch("app.routers.chat_rooms.get_db_connection") as mock:
        conn = MagicMock()
        cursor = MagicMock()
        conn.cursor.return_value = cursor
        mock.return_value = conn
        yield {"conn": conn, "cursor": cursor}


@pytest.fixture
def mock_current_user():
    """Mock authenticated user"""
    return {
        "id": 1,
        "email": "testuser@test.com",
        "username": "testuser",
        "full_name": "Test User",
        "tenant_id": "test-tenant-id",
        "is_active": True,
    }


@pytest.fixture
def mock_websocket_manager():
    """Mock WebSocket manager"""
    with patch("app.routers.chat_rooms.manager") as mock:
        mock.broadcast_to_room = MagicMock()
        mock.send_chat_message = MagicMock()
        mock.join_room = MagicMock()
        mock.leave_room = MagicMock()
        mock.set_typing = MagicMock()
        mock.get_online_users_in_room.return_value = [1, 2]
        mock.get_typing_users.return_value = []
        yield mock


@pytest.fixture
def sample_room():
    """Sample room data"""
    return {
        "id": "room-uuid-123",
        "tenant_id": "test-tenant-id",
        "name": "Test Room",
        "description": "A test chat room",
        "room_type": "group",
        "color": "#6366f1",
        "avatar_url": None,
        "is_private": True,
        "allow_invites": True,
        "max_members": 100,
        "member_count": 2,
        "message_count": 10,
        "last_message_at": datetime.utcnow().isoformat(),
        "last_message_preview": "Hello!",
        "project_id": None,
        "agent_id": None,
        "is_archived": False,
        "archived_at": None,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "user_role": "owner",
        "unread_count": 0,
    }


@pytest.fixture
def sample_message():
    """Sample message data"""
    return {
        "id": "msg-uuid-123",
        "room_id": "room-uuid-123",
        "sender_id": 1,
        "sender_username": "testuser",
        "content": "Hello, world!",
        "content_type": "text",
        "reply_to_id": None,
        "mentions": [],
        "attachments": [],
        "reactions": {},
        "is_edited": False,
        "edited_at": None,
        "is_deleted": False,
        "deleted_at": None,
        "created_at": datetime.utcnow().isoformat(),
    }


@pytest.fixture
def sample_invitation():
    """Sample invitation data"""
    return {
        "id": "inv-uuid-123",
        "room_id": "room-uuid-123",
        "inviter_id": 1,
        "invitee_id": None,
        "invitee_email": "invited@test.com",
        "invite_token": secrets.token_urlsafe(32),
        "assigned_role": "member",
        "message": "Join our team!",
        "status": "pending",
        "expires_at": (datetime.utcnow() + timedelta(days=7)).isoformat(),
        "created_at": datetime.utcnow().isoformat(),
        "responded_at": None,
    }


# ============================================
# Room Tests
# ============================================

class TestChatRoomsAPI:
    """Test suite for /api/chat/rooms endpoints"""

    def test_list_rooms_empty(self, client: TestClient, mock_db_connection, mock_current_user):
        """Test listing rooms when user has no rooms"""
        mock_db_connection["cursor"].fetchall.return_value = []

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.get("/api/chat/rooms")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_rooms_with_data(self, client: TestClient, mock_db_connection, mock_current_user, sample_room):
        """Test listing rooms returns correct data"""
        mock_db_connection["cursor"].fetchall.return_value = [sample_room]

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.get("/api/chat/rooms")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Test Room"

    def test_create_room_success(self, client: TestClient, mock_db_connection, mock_current_user, sample_room):
        """Test successful room creation"""
        mock_db_connection["cursor"].fetchone.side_effect = [
            sample_room,  # INSERT RETURNING
            sample_room,  # SELECT after insert
        ]

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.post("/api/chat/rooms", json={
                "name": "Test Room",
                "room_type": "group",
                "description": "A test room",
            })

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Room"

    def test_create_room_missing_name(self, client: TestClient, mock_current_user):
        """Test room creation fails without name"""
        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.post("/api/chat/rooms", json={
                "room_type": "group",
            })

        assert response.status_code == 422  # Validation error

    def test_get_room_detail(self, client: TestClient, mock_db_connection, mock_current_user, sample_room):
        """Test getting room details"""
        mock_db_connection["cursor"].fetchone.return_value = sample_room
        mock_db_connection["cursor"].fetchall.return_value = [
            {"user_id": 1, "username": "testuser", "email": "test@test.com", "role": "owner", "joined_at": datetime.utcnow().isoformat()}
        ]

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.get(f"/api/chat/rooms/{sample_room['id']}")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Room"
        assert "members" in data

    def test_get_room_not_found(self, client: TestClient, mock_db_connection, mock_current_user):
        """Test getting non-existent room returns 404"""
        mock_db_connection["cursor"].fetchone.return_value = None

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.get("/api/chat/rooms/nonexistent-id")

        assert response.status_code == 404

    def test_update_room_as_owner(self, client: TestClient, mock_db_connection, mock_current_user, sample_room, mock_websocket_manager):
        """Test owner can update room"""
        mock_db_connection["cursor"].fetchone.side_effect = [
            {"role": "owner"},  # Permission check
            sample_room,  # UPDATE RETURNING
        ]

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.put(f"/api/chat/rooms/{sample_room['id']}", json={
                "name": "Updated Room Name",
            })

        assert response.status_code == 200

    def test_update_room_forbidden(self, client: TestClient, mock_db_connection, mock_current_user):
        """Test non-owner/admin cannot update room"""
        mock_db_connection["cursor"].fetchone.return_value = {"role": "member"}

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.put("/api/chat/rooms/room-id", json={
                "name": "Updated Name",
            })

        assert response.status_code == 403

    def test_archive_room(self, client: TestClient, mock_db_connection, mock_current_user):
        """Test archiving a room"""
        mock_db_connection["cursor"].fetchone.return_value = {"role": "owner"}

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.delete("/api/chat/rooms/room-id")

        assert response.status_code == 204


# ============================================
# Message Tests
# ============================================

class TestChatMessagesAPI:
    """Test suite for chat messages endpoints"""

    def test_get_messages(self, client: TestClient, mock_db_connection, mock_current_user, sample_room, sample_message):
        """Test fetching room messages"""
        mock_db_connection["cursor"].fetchone.side_effect = [
            sample_room,  # Room access check
            {"total": 1},  # Count query
        ]
        mock_db_connection["cursor"].fetchall.return_value = [sample_message]

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.get(f"/api/chat/rooms/{sample_room['id']}/messages")

        assert response.status_code == 200
        data = response.json()
        assert "messages" in data
        assert "has_more" in data

    def test_send_message(self, client: TestClient, mock_db_connection, mock_current_user, sample_room, sample_message, mock_websocket_manager):
        """Test sending a message"""
        mock_db_connection["cursor"].fetchone.side_effect = [
            {"role": "member"},  # Permission check
            sample_message,  # INSERT RETURNING
            sample_message,  # SELECT with username
        ]

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.post(f"/api/chat/rooms/{sample_room['id']}/messages", json={
                "content": "Hello, world!",
                "content_type": "text",
            })

        assert response.status_code == 201
        data = response.json()
        assert data["content"] == "Hello, world!"

    def test_send_empty_message(self, client: TestClient, mock_db_connection, mock_current_user, sample_room):
        """Test sending empty message fails"""
        mock_db_connection["cursor"].fetchone.return_value = {"role": "member"}

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.post(f"/api/chat/rooms/{sample_room['id']}/messages", json={
                "content": "",
                "content_type": "text",
            })

        # Should fail validation or be rejected
        assert response.status_code in [400, 422]

    def test_edit_own_message(self, client: TestClient, mock_db_connection, mock_current_user, sample_message, mock_websocket_manager):
        """Test editing own message"""
        mock_db_connection["cursor"].fetchone.side_effect = [
            sample_message,  # Get message
            {**sample_message, "content": "Edited content", "is_edited": True},  # UPDATE RETURNING
        ]

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.put(f"/api/chat/messages/{sample_message['id']}", json={
                "content": "Edited content",
            })

        assert response.status_code == 200

    def test_edit_others_message_forbidden(self, client: TestClient, mock_db_connection, mock_current_user, sample_message):
        """Test cannot edit another user's message"""
        other_user_message = {**sample_message, "sender_id": 999}
        mock_db_connection["cursor"].fetchone.return_value = other_user_message

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.put(f"/api/chat/messages/{sample_message['id']}", json={
                "content": "Trying to edit",
            })

        assert response.status_code == 403

    def test_delete_message(self, client: TestClient, mock_db_connection, mock_current_user, sample_message, mock_websocket_manager):
        """Test deleting a message (soft delete)"""
        mock_db_connection["cursor"].fetchone.return_value = sample_message

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.delete(f"/api/chat/messages/{sample_message['id']}")

        assert response.status_code == 204

    def test_add_reaction(self, client: TestClient, mock_db_connection, mock_current_user, sample_room, sample_message, mock_websocket_manager):
        """Test adding reaction to message"""
        mock_db_connection["cursor"].fetchone.side_effect = [
            {"room_id": sample_room["id"], "reactions": {}},  # Get message
            sample_room,  # Room access check
        ]

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.post(f"/api/chat/messages/{sample_message['id']}/reactions", json={
                "emoji": "👍",
                "action": "add",
            })

        assert response.status_code == 200


# ============================================
# Invitation Tests
# ============================================

class TestChatInvitationsAPI:
    """Test suite for invitation endpoints"""

    def test_create_invitation_by_email(self, client: TestClient, mock_db_connection, mock_current_user, sample_room, sample_invitation):
        """Test creating invitation by email"""
        mock_db_connection["cursor"].fetchone.side_effect = [
            {**sample_room, "role": "owner"},  # Room + permission check
            sample_invitation,  # INSERT RETURNING
            {"username": "testuser", "full_name": "Test User"},  # Inviter info
        ]

        with patch("app.routers.chat_rooms.get_notification_service") as mock_notification:
            mock_notification.return_value.send_chat_invitation_email.return_value = {"success": True}

            with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
                response = client.post(f"/api/chat/rooms/{sample_room['id']}/invitations", json={
                    "invitee_email": "invited@test.com",
                    "assigned_role": "member",
                    "message": "Join us!",
                })

        assert response.status_code == 200
        data = response.json()
        assert "invite_token" in data

    def test_create_invitation_without_permission(self, client: TestClient, mock_db_connection, mock_current_user, sample_room):
        """Test invitation creation fails without permission"""
        mock_db_connection["cursor"].fetchone.return_value = {
            **sample_room,
            "role": "member",
            "allow_invites": False,
        }

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.post(f"/api/chat/rooms/{sample_room['id']}/invitations", json={
                "invitee_email": "invited@test.com",
                "assigned_role": "member",
            })

        assert response.status_code == 403

    def test_get_invitation_public_info(self, client: TestClient, mock_db_connection, sample_invitation, sample_room):
        """Test getting public invitation info (no auth required)"""
        mock_db_connection["cursor"].fetchone.return_value = {
            **sample_invitation,
            "room_name": sample_room["name"],
            "room_type": sample_room["room_type"],
            "member_count": sample_room["member_count"],
            "inviter_username": "testuser",
        }

        response = client.get(f"/api/chat/invitations/{sample_invitation['invite_token']}")

        assert response.status_code == 200
        data = response.json()
        assert data["room_name"] == "Test Room"
        assert "is_valid" in data

    def test_accept_invitation(self, client: TestClient, mock_db_connection, mock_current_user, sample_invitation, mock_websocket_manager):
        """Test accepting an invitation"""
        mock_db_connection["cursor"].fetchone.return_value = {
            **sample_invitation,
            "status": "pending",
            "expires_at": datetime.utcnow() + timedelta(days=7),
        }
        mock_db_connection["cursor"].rowcount = 1

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.post(f"/api/chat/invitations/{sample_invitation['invite_token']}", json={
                "accept": True,
            })

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "accepted"

    def test_decline_invitation(self, client: TestClient, mock_db_connection, mock_current_user, sample_invitation):
        """Test declining an invitation"""
        mock_db_connection["cursor"].fetchone.return_value = {
            **sample_invitation,
            "status": "pending",
            "expires_at": datetime.utcnow() + timedelta(days=7),
        }

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.post(f"/api/chat/invitations/{sample_invitation['invite_token']}", json={
                "accept": False,
            })

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "declined"

    def test_expired_invitation(self, client: TestClient, mock_db_connection, mock_current_user, sample_invitation):
        """Test that expired invitations are rejected"""
        mock_db_connection["cursor"].fetchone.return_value = None  # Expired query returns nothing

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.post(f"/api/chat/invitations/expired-token", json={
                "accept": True,
            })

        assert response.status_code == 404


# ============================================
# Member Management Tests
# ============================================

class TestChatMembersAPI:
    """Test suite for member management endpoints"""

    def test_list_room_members(self, client: TestClient, mock_db_connection, mock_current_user, sample_room):
        """Test listing room members"""
        mock_db_connection["cursor"].fetchone.return_value = sample_room
        mock_db_connection["cursor"].fetchall.return_value = [
            {"user_id": 1, "username": "user1", "email": "user1@test.com", "role": "owner", "joined_at": datetime.utcnow().isoformat()},
            {"user_id": 2, "username": "user2", "email": "user2@test.com", "role": "member", "joined_at": datetime.utcnow().isoformat()},
        ]

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.get(f"/api/chat/rooms/{sample_room['id']}/members")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_add_member(self, client: TestClient, mock_db_connection, mock_current_user, sample_room, mock_websocket_manager):
        """Test adding a member to room"""
        mock_db_connection["cursor"].fetchone.side_effect = [
            {**sample_room, "role": "owner", "allow_invites": True, "max_members": 100},  # Permission check
            {"user_id": 3, "role": "member", "room_id": sample_room["id"]},  # INSERT RETURNING
            {"username": "newmember"},  # Get username
        ]
        mock_db_connection["cursor"].rowcount = 1

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.post(f"/api/chat/rooms/{sample_room['id']}/members", json={
                "user_id": 3,
                "role": "member",
            })

        assert response.status_code == 201

    def test_remove_member(self, client: TestClient, mock_db_connection, mock_current_user, sample_room, mock_websocket_manager):
        """Test removing a member from room"""
        mock_db_connection["cursor"].fetchone.side_effect = [
            {"role": "owner"},  # Permission check
            {"role": "member"},  # Member to remove
        ]

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.delete(f"/api/chat/rooms/{sample_room['id']}/members/3")

        assert response.status_code == 204

    def test_cannot_remove_owner(self, client: TestClient, mock_db_connection, mock_current_user, sample_room):
        """Test that owner cannot be removed"""
        mock_db_connection["cursor"].fetchone.side_effect = [
            {"role": "admin"},  # Permission check
            {"role": "owner"},  # Target is owner
        ]

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.delete(f"/api/chat/rooms/{sample_room['id']}/members/1")

        assert response.status_code == 400


# ============================================
# Read Receipts & Typing Tests
# ============================================

class TestChatStatusAPI:
    """Test suite for read receipts and typing indicators"""

    def test_mark_as_read(self, client: TestClient, mock_db_connection, mock_current_user, sample_room, mock_websocket_manager):
        """Test marking messages as read"""
        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.post(f"/api/chat/rooms/{sample_room['id']}/read", json={
                "last_read_message_id": "msg-123",
            })

        assert response.status_code == 200

    def test_typing_indicator(self, client: TestClient, mock_current_user, sample_room, mock_websocket_manager):
        """Test sending typing indicator"""
        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.post(f"/api/chat/rooms/{sample_room['id']}/typing", json={
                "is_typing": True,
            })

        assert response.status_code == 200
        mock_websocket_manager.set_typing.assert_called_once()

    def test_get_room_status(self, client: TestClient, mock_db_connection, mock_current_user, sample_room, mock_websocket_manager):
        """Test getting room online status"""
        mock_db_connection["cursor"].fetchone.return_value = sample_room

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.get(f"/api/chat/rooms/{sample_room['id']}/status")

        assert response.status_code == 200
        data = response.json()
        assert "online_users" in data
        assert "typing_users" in data


# ============================================
# Direct Chat Tests
# ============================================

class TestDirectChatAPI:
    """Test suite for direct chat functionality"""

    def test_create_direct_chat(self, client: TestClient, mock_db_connection, mock_current_user):
        """Test creating a direct chat"""
        mock_db_connection["cursor"].fetchone.side_effect = [
            {"id": 2},  # Target user exists
            None,  # No existing direct chat
            {"id": "direct-room-id"},  # New room created
        ]

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.post("/api/chat/direct", json={
                "target_user_id": 2,
            })

        assert response.status_code == 200
        data = response.json()
        assert "room_id" in data
        assert data["is_new"] == True

    def test_get_existing_direct_chat(self, client: TestClient, mock_db_connection, mock_current_user):
        """Test getting existing direct chat returns it"""
        mock_db_connection["cursor"].fetchone.side_effect = [
            {"id": 2},  # Target user exists
            {"id": "existing-direct-room"},  # Existing direct chat found
        ]

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.post("/api/chat/direct", json={
                "target_user_id": 2,
            })

        assert response.status_code == 200
        data = response.json()
        assert data["is_new"] == False

    def test_direct_chat_user_not_found(self, client: TestClient, mock_db_connection, mock_current_user):
        """Test direct chat with non-existent user fails"""
        mock_db_connection["cursor"].fetchone.return_value = None

        with patch("app.routers.chat_rooms.get_current_active_user", return_value=Mock(**mock_current_user)):
            response = client.post("/api/chat/direct", json={
                "target_user_id": 999,
            })

        assert response.status_code == 404
