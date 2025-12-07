import asyncio
import pytest
from httpx import AsyncClient

pytest.data = {"base_url": "http://127.0.0.1:8000/api/v1", "auth_header": {}}

# email = input("Enter email: ")
# password = input("Enter password: ")
username = "rohit"
password = "rohit123"


async def login():
    async with AsyncClient(base_url=pytest.data["base_url"]) as client:
        response = await client.post("/login", data={"username": username, "password": password})
        assert response.status_code == 200
        response_data = response.json()
        assert "data" in response_data
        assert "access_token" in response_data
        pytest.data["auth_header"] = {"Authorization": f"Bearer {response_data['access_token']}"}


def pytest_sessionstart(session):
    """Runs before any tests and ensures login happens first."""
    asyncio.run(login())  #
