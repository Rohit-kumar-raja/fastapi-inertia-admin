import pytest
from uuid import UUID
import uuid
from httpx import AsyncClient

base_url = pytest.data["base_url"]
GLOBAL_TEST_DATA = {}


@pytest.fixture
def mock_user():
    return {
        "username": str(uuid.uuid4()).replace("-", "")[:8],
        "password": "User@1234",
    }


@pytest.fixture(scope="session", autouse=True)
def reset_global_data():
    """Reset global test data before tests run"""
    GLOBAL_TEST_DATA["current_data"] = None


@pytest.mark.asyncio
async def test_create_user(mock_user):
    async with AsyncClient(base_url=base_url) as client:
        # Fetch available roles
        response_roles = await client.get("/roles", headers=pytest.data["auth_header"])
        assert response_roles.status_code == 200
        response_roles_data = response_roles.json()
        mock_user["role_ids"] = [response_roles_data["data"][0]["id"]]  # Assign first role

        response = await client.post("/users", json=mock_user, headers=pytest.data["auth_header"])
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["message"] == "Data created successfully"
        data = response_data["data"]
        GLOBAL_TEST_DATA["current_data"] = data
        assert data["username"] == mock_user["username"]
        assert UUID(data["id"])


@pytest.mark.asyncio
async def test_get_all_users():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.get("/users", headers=pytest.data["auth_header"])
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Data fetched successfully"
        assert isinstance(response_data["data"], list)


@pytest.mark.asyncio
async def test_get_user_by_id():
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored

        response = await client.get(
            f"/users/{GLOBAL_TEST_DATA['current_data']['id']}", headers=pytest.data["auth_header"]
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Data fetched successfully"
        data = response_data["data"]
        assert data["id"] == GLOBAL_TEST_DATA["current_data"]["id"]
        assert data["username"] == GLOBAL_TEST_DATA["current_data"]["username"]


@pytest.mark.asyncio
async def test_update_user():
    updated_data = {
        "username": "updatedUser",
        "password": "User@updated1234",
    }
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored

        # Fetch roles to update role_id
        response_roles = await client.get("/roles", headers=pytest.data["auth_header"])
        assert response_roles.status_code == 200
        response_roles_data = response_roles.json()
        updated_data["role_ids"] = [response_roles_data["data"][0]["id"]]  # Assign first role

        response = await client.put(
            f"/users/{GLOBAL_TEST_DATA['current_data']['id']}",
            json=updated_data,
            headers=pytest.data["auth_header"],
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Data updated successfully"
        # data = response_data["data"]
        # assert data["id"] == GLOBAL_TEST_DATA["current_data"]["id"]


@pytest.mark.asyncio
async def test_create_duplicate_user():
    duplicate_data = {
        "username": "updatedUser",
        "password": "User@updated1234",
    }
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored

        response_roles = await client.get("/roles", headers=pytest.data["auth_header"])
        assert response_roles.status_code == 200
        response_roles_data = response_roles.json()
        duplicate_data["role_ids"] = [response_roles_data["data"][0]["id"]]

        response = await client.post("/users", json=duplicate_data, headers=pytest.data["auth_header"])
        assert response.status_code == 422
        response_data = response.json()
        assert response_data["message"] == "Username already exists"


@pytest.mark.asyncio
async def test_delete_user():
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored

        response = await client.delete(
            f"/users/{GLOBAL_TEST_DATA['current_data']['id']}", headers=pytest.data["auth_header"]
        )
        assert response.status_code == 204
        response1 = await client.get(
            f"/users/{GLOBAL_TEST_DATA['current_data']['id']}", headers=pytest.data["auth_header"]
        )
        assert response1.status_code == 404
