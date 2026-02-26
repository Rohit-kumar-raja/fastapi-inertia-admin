import pytest
from httpx import AsyncClient

base_url = pytest.data["base_url"]


@pytest.mark.asyncio
async def test_login_success():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.post(
            "/login",
            data={
                "username": "rohit",
                "password": "rohit123"
            }
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "User has logged in successfully."
        assert "access_token" in response_data
        assert "data" in response_data
        assert "user" in response_data["data"]
        assert "permissions" in response_data["data"]


@pytest.mark.asyncio
async def test_login_invalid_password():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.post(
            "/login",
            data={
                "username": "rohit",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 400
        response_data = response.json()
        assert response_data["message"] == "Invalid password"


@pytest.mark.asyncio
async def test_login_user_not_found():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.post(
            "/login",
            data={
                "username": "nonexistentuser",
                "password": "password123"
            }
        )
        assert response.status_code == 404
        response_data = response.json()
        assert response_data["message"] == "User not found"


@pytest.mark.asyncio
async def test_reset_password_placeholder():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.post("/admin/login/reset-password")
        # Currently the endpoint just has 'pass' and returns 200 OK
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_forgot_password_placeholder():
    async with AsyncClient(base_url=base_url) as client:
        response = await client.post("/admin/login/forgot-password")
        # Currently the endpoint just has 'pass' and returns 200 OK
        assert response.status_code == 200
