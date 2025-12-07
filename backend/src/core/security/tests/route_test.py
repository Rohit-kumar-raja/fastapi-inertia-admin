import pytest
from httpx import AsyncClient

base_url = pytest.data["base_url"]  #  Keep the base URL, adjust as needed


@pytest.fixture
def mock_permission():
    return {
        "name": "Test Permission2",
        # "parent_id": str(uuid.uuid4()),  #  Needs to be string for JSON
        # "privilege_ids": [str(uuid.uuid4()), str(uuid.uuid4())],  #  Needs to be string for JSON
    }


GLOBAL_TEST_DATA = {}
CREATED_PERMISSIONS = []


@pytest.fixture(scope="session", autouse=True)
def reset_global_data():
    """Reset global test data before tests run"""
    GLOBAL_TEST_DATA["current_permission"] = None


@pytest.mark.asyncio
async def test_create_without_authorization_permission(mock_permission):
    async with AsyncClient(base_url=base_url) as client:
        response = await client.post("/routes", json=mock_permission)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data["detail"] == "Not authenticated"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_permission,auth_header,test_name,status_code,msg,loc",
    [
        (None, pytest.data["auth_header"], "Test without json", 422, "Field required", "body"),
        (
            {"name": ""},
            pytest.data["auth_header"],
            "Test with empty name",
            422,
            "String should have at least 1 character",
            "body",
        ),
        (
            {"name": 123},
            pytest.data["auth_header"],
            "Test with invalid name",
            422,
            "Input should be a valid string",
            "body",
        ),
        (
            {"name": "a" * 101},
            pytest.data["auth_header"],
            "Test with name too long",
            422,
            "String should have at most 100 characters",
            "body",
        ),
    ],
)
async def test_create_permission_validation(mock_permission, auth_header, test_name, status_code, msg, loc):
    print(f"Running test: {test_name}")
    async with AsyncClient(base_url=base_url) as client:
        response = await client.post("/routes", json=mock_permission, headers=auth_header)
        assert response.status_code == status_code
        response_data = response.json()
        if status_code == 422:
            assert response_data["detail"][0]["msg"] == msg
            assert response_data["detail"][0]["loc"][0] == loc
        elif status_code == 201:
            assert "data" in response_data
            data = response_data["data"]
            CREATED_PERMISSIONS.append(data)
            assert data["name"] == mock_permission["name"]
            assert response_data["message"] == msg


# @pytest.mark.asyncio
# async def test_get_all_permissions():
#     async with AsyncClient(base_url=base_url) as client:
#         response = await client.get("/routes", headers=pytest.data["auth_header"])
#         assert response.status_code == 200
#         response_data = response.json()
#         assert "data" in response_data
#         assert isinstance(response_data["data"], list)


# @pytest.mark.asyncio
# async def test_get_all_permissions_without_authorization():
#     async with AsyncClient(base_url=base_url) as client:
#         response = await client.get("/routes")
#         assert response.status_code == 403
#         response_data = response.json()
#         assert response_data["detail"] == "Not authenticated"


# @pytest.mark.asyncio
# async def test_get_permission_by_id():
#     async with AsyncClient(base_url=base_url) as client:
#         assert GLOBAL_TEST_DATA["current_permission"] is not None
#         permission_id = GLOBAL_TEST_DATA["current_permission"]["id"]
#         response = await client.get(f"/routes/{permission_id}", headers=pytest.data["auth_header"])
#         assert response.status_code == 200
#         response_data = response.json()
#         assert "data" in response_data
#         data = response_data["data"]
#         assert data["id"] == permission_id
#         assert data["name"] == GLOBAL_TEST_DATA["current_permission"]["name"]


# @pytest.mark.asyncio
# async def test_get_permission_by_id_witout_authorization():
#     async with AsyncClient(base_url=base_url) as client:
#         response = await client.get(f"/routes/{GLOBAL_TEST_DATA['current_permission']['id']}")
#         assert response.status_code == 403
#         response_data = response.json()
#         assert response_data["detail"] == "Not authenticated"


# @pytest.mark.asyncio
# async def test_get_permission_by_id_wrong_id():
#     async with AsyncClient(base_url=base_url) as client:
#         response = await client.get(f"/routes/{str(uuid.uuid4())}", headers=pytest.data["auth_header"])
#         assert response.status_code == 404
#         response_data = response.json()
#         assert response_data["message"] == "Data not found"


# @pytest.mark.asyncio
# async def test_get_permission_by_id_invalid_uuid():
#     async with AsyncClient(base_url=base_url) as client:
#         response = await client.get(f"/routes/invalid-uuid", headers=pytest.data["auth_header"])
#         assert response.status_code == 422
#         response_data = response.json()
#         assert (
#             response_data["detail"][0]["msg"]
#             == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1"
#         )
#         assert response_data["detail"][0]["loc"][0] == "path"
#         assert response_data["detail"][0]["loc"][1] == "uuid"


# @pytest.mark.asyncio
# async def test_update_permission():
#     updated_data = {
#         "name": "Updated Permission Test",
#     }
#     async with AsyncClient(base_url=base_url) as client:
#         assert GLOBAL_TEST_DATA["current_permission"] is not None
#         permission_id = GLOBAL_TEST_DATA["current_permission"]["id"]
#         response = await client.put(
#             f"/routes/{permission_id}", json=updated_data, headers=pytest.data["auth_header"]
#         )
#         assert response.status_code == 200
#         response_data = response.json()
#         assert "data" in response_data
#         data = response_data["data"]
#         assert data["id"] == permission_id
#         assert data["name"] == updated_data["name"]  #  check for the updated name
#         # assert data["parent_id"] == updated_data["parent_id"]
#         # assert data["privilege_ids"] == updated_data["privilege_ids"]


# @pytest.mark.asyncio
# async def test_create_duplicate_permission():
#     updated_data = {
#         "name": "Updated Permission Test",
#     }
#     async with AsyncClient(base_url=base_url) as client:
#         assert GLOBAL_TEST_DATA["current_permission"] is not None  #  make sure you have permission data available
#         response = await client.post(
#             "/routes", json=updated_data, headers=pytest.data["auth_header"]
#         )  # Reuse initial data
#         assert response.status_code == 422  # Expect a 422 Unprocessable Entity


# @pytest.mark.asyncio
# async def test_get_permission_tree():
#     async with AsyncClient(base_url=base_url) as client:
#         response = await client.get("/tree/routes", headers=pytest.data["auth_header"])
#         assert response.status_code == 200
#         assert "data" in response.json()
#         #  We don't know the *exact* length, but it should be a list.  Could be empty.
#         assert isinstance(response.json()["data"], list)


@pytest.mark.asyncio
async def test_delete_permission():
    async with AsyncClient(base_url=base_url) as client:
        assert CREATED_PERMISSIONS is not None
        for permission in CREATED_PERMISSIONS:
            response = await client.delete(f"/routes/{permission['id']}", headers=pytest.data["auth_header"])
            assert response.status_code == 200
            response_data = response.json()
            assert "data" in response_data
            # Verify it's actually gone
            response = await client.get(f"/routes/{permission['id']}", headers=pytest.data["auth_header"])
            assert response.status_code == 404
