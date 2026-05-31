import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    response = await client.post("/api/v1/auth/register", json={
        "email": "test@test.com",
        "full_name": "Test User",
        "password": "testpass"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@test.com"

@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    # first register
    await client.post("/api/v1/auth/register", json={
        "email": "login@test.com",
        "password": "secret"
    })
    response = await client.post("/api/v1/auth/login", data={
        "username": "login@test.com",
        "password": "secret"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data