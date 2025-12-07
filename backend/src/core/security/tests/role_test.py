import pytest
from uuid import UUID
import uuid
from httpx import AsyncClient

base_url = pytest.data["base_url"]


@pytest.fixture
def mock_role():
    return {
        "name": str(uuid.uuid4()).replace("-", "")[:8],
    }


GLOBAL_TEST_DATA = {}


@pytest.fixture(scope="session", autouse=True)
def reset_global_data():
    """Reset global test data before tests run"""
    GLOBAL_TEST_DATA["current_data"] = None


@pytest.mark.asyncio
async def test_create_role(mock_role):
    async with AsyncClient(base_url=base_url) as client:
        response_permission = await client.get("/routes", headers=pytest.data["auth_header"])
        assert response_permission.status_code == 200
        response_permissions_data = response_permission.json()
        mock_role["permission_ids"] = [permissions["id"] for permissions in response_permissions_data["data"]]
        response = await client.post("/roles", json=mock_role, headers=pytest.data["auth_header"])
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["message"] == "Data created successfully"
        data = response_data["data"]
        GLOBAL_TEST_DATA["current_data"] = data
        assert data["name"] == mock_role["name"]
        assert UUID(data["id"])


@pytest.mark.asyncio
async def test_get_all_roles():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.get("/roles", headers=pytest.data["auth_header"])
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Data fetched successfully"
        assert isinstance(response_data["data"], list)


@pytest.mark.asyncio
async def test_get_role_by_id():
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored

        response = await client.get(
            f"/roles/{GLOBAL_TEST_DATA['current_data']['id']}", headers=pytest.data["auth_header"]
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Data fetched successfully"
        data = response_data["data"]
        assert data["id"] == GLOBAL_TEST_DATA["current_data"]["id"]
        assert data["name"] == GLOBAL_TEST_DATA["current_data"]["name"]


@pytest.mark.asyncio
async def test_update_role():
    updated_data = {"name": "Updated Role Test"}
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored

        response_permission = await client.get("/routes", headers=pytest.data["auth_header"])
        assert response_permission.status_code == 200
        response_permissions_data = response_permission.json()
        updated_data["permission_ids"] = [permissions["id"] for permissions in response_permissions_data["data"]]

        response = await client.put(
            f"/roles/{GLOBAL_TEST_DATA['current_data']['id']}",
            json=updated_data,
            headers=pytest.data["auth_header"],
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Data updated successfully"
        data = response_data["data"]
        assert data["id"] == GLOBAL_TEST_DATA["current_data"]["id"]


@pytest.mark.asyncio
async def test_create_duplicate_role():
    duplicate_data = {"name": "Updated Role Test"}
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored
        response_permission = await client.get("/routes", headers=pytest.data["auth_header"])
        assert response_permission.status_code == 200
        response_permissions_data = response_permission.json()
        duplicate_data["permission_ids"] = [permissions["id"] for permissions in response_permissions_data["data"]]
        response = await client.post("/roles", json=duplicate_data, headers=pytest.data["auth_header"])
        assert response.status_code == 422
        response_data = response.json()
        assert response_data["message"] == "Role name already exists"


@pytest.mark.asyncio
async def test_delete_role():
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored

        response = await client.delete(
            f"/roles/{GLOBAL_TEST_DATA['current_data']['id']}", headers=pytest.data["auth_header"]
        )
        assert response.status_code == 204
        response1 = await client.get(
            f"/roles/{GLOBAL_TEST_DATA['current_data']['id']}", headers=pytest.data["auth_header"]
        )
        assert response1.status_code == 404
