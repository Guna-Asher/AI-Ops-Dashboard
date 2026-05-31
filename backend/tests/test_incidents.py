import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_incident(client: AsyncClient):
    # register and login to get token
    await client.post("/api/v1/auth/register", json={"email": "inc@test.com", "password": "pass"})
    login_res = await client.post("/api/v1/auth/login", data={"username": "inc@test.com", "password": "pass"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post("/api/v1/incidents/", json={
        "title": "High CPU Usage",
        "description": "Server CPU spike",
        "severity": "high"
    }, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "High CPU Usage"