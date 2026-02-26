import pytest
import uuid
from httpx import AsyncClient
from uuid import UUID

base_url = pytest.data["base_url"]
GLOBAL_TEST_DATA = {}


@pytest.fixture(scope="session", autouse=True)
def reset_global_data():
    """Reset global test data before tests run"""
    GLOBAL_TEST_DATA["current_data"] = None


@pytest.fixture
def mock_notification():
    return {
        "title": "Test Notification Title",
        "message": "This is a test message.",
        "type": "info"
    }


@pytest.mark.asyncio
async def test_get_vapid_public_key():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.get("/notifications/vapid-public-key", headers=pytest.data["auth_header"])
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "VAPID public key"
        assert "publicKey" in response_data["data"]


@pytest.mark.asyncio
async def test_create_notification(mock_notification):
    async with AsyncClient(base_url=base_url) as client:
        response = await client.post(
            "/notifications",
            json=mock_notification,
            headers=pytest.data["auth_header"]
        )
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["message"] == "Notification created"
        data = response_data["data"]
        GLOBAL_TEST_DATA["current_data"] = data
        assert data["title"] == mock_notification["title"]
        assert data["message"] == mock_notification["message"]
        assert data["type"] == mock_notification["type"]
        assert UUID(data["id"])


@pytest.mark.asyncio
async def test_list_notifications():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.get("/notifications", headers=pytest.data["auth_header"])
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Notifications fetched"
        assert isinstance(response_data["data"], list)
        assert len(response_data["data"]) > 0


@pytest.mark.asyncio
async def test_unread_count():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.get("/notifications/count", headers=pytest.data["auth_header"])
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Unread count fetched"
        assert "count" in response_data["data"]
        assert isinstance(response_data["data"]["count"], int)
        assert response_data["data"]["count"] > 0


@pytest.mark.asyncio
async def test_mark_read():
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None

        response = await client.put(
            f"/notifications/{GLOBAL_TEST_DATA['current_data']['id']}/read",
            headers=pytest.data["auth_header"]
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Marked as read"


@pytest.mark.asyncio
async def test_mark_all_read():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.put("/notifications/read-all", headers=pytest.data["auth_header"])
        assert response.status_code == 200
        response_data = response.json()
        assert "notifications marked as read" in response_data["message"]
        assert "count" in response_data["data"]


@pytest.mark.asyncio
async def test_push_subscribe():
    mock_subscription = {
        "endpoint": "https://fcm.googleapis.com/fcm/send/test-endpoint-id",
        "keys": {
            "p256dh": "test-p256dh-key",
            "auth": "test-auth-key"
        }
    }
    async with AsyncClient(base_url=base_url) as client:
        response = await client.post(
            "/notifications/push/subscribe",
            json=mock_subscription,
            headers=pytest.data["auth_header"]
        )
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["message"] == "Push subscription saved"
        assert "id" in response_data["data"]


@pytest.mark.asyncio
async def test_push_unsubscribe():
    mock_unsubscription = {
        "endpoint": "https://fcm.googleapis.com/fcm/send/test-endpoint-id",
        "keys": {
            "p256dh": "test-p256dh-key",
            "auth": "test-auth-key"
        }
    }
    async with AsyncClient(base_url=base_url) as client:
        response = await client.post(
            "/notifications/push/unsubscribe",
            json=mock_unsubscription,
            headers=pytest.data["auth_header"]
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Push subscription removed"


@pytest.mark.asyncio
async def test_delete_notification():
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None

        response = await client.delete(
            f"/notifications/{GLOBAL_TEST_DATA['current_data']['id']}",
            headers=pytest.data["auth_header"]
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Notification deleted"
