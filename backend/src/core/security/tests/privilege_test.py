import pytest
from uuid import UUID
import uuid
from httpx import AsyncClient

base_url = pytest.data["base_url"]


@pytest.fixture
def mock_privilege():
    return {"access": str(uuid.uuid4()).replace("-", "")[:8]}


GLOBAL_TEST_DATA = {}


@pytest.fixture(scope="session", autouse=True)
def reset_global_data():
    """Reset global test data before tests run"""
    GLOBAL_TEST_DATA["current_data"] = None


@pytest.mark.asyncio
async def test_create_privilege(mock_privilege):
    async with AsyncClient(base_url=base_url) as client:
        response = await client.post("/privileges", json=mock_privilege, headers=pytest.data["auth_header"])
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["message"] == "Data created successfully"
        data = response_data["data"]
        GLOBAL_TEST_DATA["current_data"] = data
        assert data["access"] == mock_privilege["access"]
        assert UUID(data["id"])


@pytest.mark.asyncio
async def test_create_without_authorization_privilege(mock_privilege):
    async with AsyncClient(base_url=base_url) as client:
        response = await client.post("/privileges", json=mock_privilege)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_create_without_data():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.post("/privileges", headers=pytest.data["auth_header"])
        assert response.status_code == 422
        response_data = response.json()
        assert response_data["detail"][0]["msg"] == "Field required"
        assert response_data["detail"][0]["type"] == "missing"
        assert response_data["detail"][0]["loc"][0] == "body"


@pytest.mark.asyncio
async def test_create_privilege_empty_access_data():
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored
        response = await client.post(
            "/privileges",
            json={"access": ""},
            headers=pytest.data["auth_header"],
        )
        assert response.status_code == 422
        response_data = response.json()
        assert response_data["detail"][0]["msg"] == "String should have at least 1 character"
        assert response_data["detail"][0]["loc"][0] == "body"
        assert response_data["detail"][0]["loc"][1] == "access"


@pytest.mark.asyncio
async def test_create_with_empty_data():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.post("/privileges", json={}, headers=pytest.data["auth_header"])
        assert response.status_code == 422
        response_data = response.json()
        assert response_data["detail"][0]["msg"] == "Field required"
        assert response_data["detail"][0]["type"] == "missing"
        assert response_data["detail"][0]["loc"][0] == "body"
        assert response_data["detail"][0]["loc"][1] == "access"


@pytest.mark.asyncio
async def test_validation_of_access_name():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.post("/privileges", json={"access": 256}, headers=pytest.data["auth_header"])
        assert response.status_code == 422
        response_data = response.json()
        assert response_data["detail"][0]["msg"] == "Input should be a valid string"
        assert response_data["detail"][0]["loc"][0] == "body"
        assert response_data["detail"][0]["loc"][1] == "access"


@pytest.mark.asyncio
async def test_get_all_privileges():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.get("/privileges", headers=pytest.data["auth_header"])
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Data fetched successfully"
        assert isinstance(response_data["data"], list)


@pytest.mark.asyncio
async def test_get_all_privileges_without_authorization_privilege():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.get("/privileges")
        assert response.status_code == 401
        response_data = response.json()
        assert response_data["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_get_privilege_by_id():
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored
        response = await client.get(
            f"/privileges/{GLOBAL_TEST_DATA['current_data']['id']}", headers=pytest.data["auth_header"]
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Data fetched successfully"
        data = response_data["data"]
        assert data["id"] == GLOBAL_TEST_DATA["current_data"]["id"]
        assert data["access"] == GLOBAL_TEST_DATA["current_data"]["access"]


@pytest.mark.asyncio
async def test_get_privilege_by_id_without_authorization():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.get(f"/privileges/{GLOBAL_TEST_DATA['current_data']['id']}")
        assert response.status_code == 401
        response_data = response.json()
        assert response_data["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_get_privilege_by_id_wrong_id():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.get(f"/privileges/{str(uuid.uuid4())}", headers=pytest.data["auth_header"])
        assert response.status_code == 404
        response_data = response.json()
        assert response_data["message"] == "Data not found"


@pytest.mark.asyncio
async def test_get_privilege_by_id_invalid_uuid():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.get("/privileges/invalid-uuid", headers=pytest.data["auth_header"])
        assert response.status_code == 422
        response_data = response.json()
        assert (
            response_data["detail"][0]["msg"]
            == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1"
        )
        assert response_data["detail"][0]["loc"][0] == "path"
        assert response_data["detail"][0]["loc"][1] == "uuid"


@pytest.mark.asyncio
async def test_update_privilege():
    updated_data = {"access": "Updated Privilege Test"}
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored
        response = await client.put(
            f"/privileges/{GLOBAL_TEST_DATA['current_data']['id']}",
            json=updated_data,
            headers=pytest.data["auth_header"],
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Data updated successfully"
        data = response_data["data"]
        assert data["id"] == GLOBAL_TEST_DATA["current_data"]["id"]


@pytest.mark.asyncio
async def test_update_privilege_without_authorization():
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored
        response = await client.put(
            f"/privileges/{GLOBAL_TEST_DATA['current_data']['id']}",
            json={"access": "Updated Privilege Test"},
        )
        assert response.status_code == 401
        response_data = response.json()
        assert response_data["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_update_privilege_without_data():
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored
        response = await client.put(
            f"/privileges/{GLOBAL_TEST_DATA['current_data']['id']}",
            headers=pytest.data["auth_header"],
        )
        assert response.status_code == 422
        response_data = response.json()
        assert response_data["detail"][0]["msg"] == "Field required"
        assert response_data["detail"][0]["type"] == "missing"
        assert response_data["detail"][0]["loc"][0] == "body"


@pytest.mark.asyncio
async def test_update_privilege_empty_data():
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored
        response = await client.put(
            f"/privileges/{GLOBAL_TEST_DATA['current_data']['id']}",
            json={},
            headers=pytest.data["auth_header"],
        )
        assert response.status_code == 422
        response_data = response.json()
        assert response_data["detail"][0]["msg"] == "Field required"
        assert response_data["detail"][0]["type"] == "missing"
        assert response_data["detail"][0]["loc"][0] == "body"
        assert response_data["detail"][0]["loc"][1] == "access"


@pytest.mark.asyncio
async def test_update_privilege_empty_access_data():
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored
        response = await client.put(
            f"/privileges/{GLOBAL_TEST_DATA['current_data']['id']}",
            json={"access": ""},
            headers=pytest.data["auth_header"],
        )
        assert response.status_code == 422
        response_data = response.json()
        assert response_data["detail"][0]["msg"] == "String should have at least 1 character"
        assert response_data["detail"][0]["loc"][0] == "body"
        assert response_data["detail"][0]["loc"][1] == "access"


@pytest.mark.asyncio
async def test_update_privilege_with_empty_data():
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored
        response = await client.put(
            f"/privileges/{GLOBAL_TEST_DATA['current_data']['id']}",
            json={},
            headers=pytest.data["auth_header"],
        )
        assert response.status_code == 422
        response_data = response.json()
        assert response_data["detail"][0]["msg"] == "Field required"
        assert response_data["detail"][0]["type"] == "missing"
        assert response_data["detail"][0]["loc"][0] == "body"
        assert response_data["detail"][0]["loc"][1] == "access"


@pytest.mark.asyncio
async def test_create_duplicate_privilege():
    duplicate_data = {"access": "Updated Privilege Test"}
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored

        response = await client.post("/privileges", json=duplicate_data, headers=pytest.data["auth_header"])
        assert response.status_code == 422
        response_data = response.json()
        assert response_data["message"] == "Privilege name already exists"


@pytest.mark.asyncio
async def test_delete_privilege():
    async with AsyncClient(base_url=base_url) as client:
        assert GLOBAL_TEST_DATA["current_data"] is not None  # Ensure data is stored

        response = await client.delete(
            f"/privileges/{GLOBAL_TEST_DATA['current_data']['id']}", headers=pytest.data["auth_header"]
        )
        assert response.status_code == 204

        response1 = await client.get(
            f"/privileges/{GLOBAL_TEST_DATA['current_data']['id']}", headers=pytest.data["auth_header"]
        )
        assert response1.status_code == 404
