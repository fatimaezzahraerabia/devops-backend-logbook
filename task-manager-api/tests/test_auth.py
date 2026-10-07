import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_and_login_user(client: AsyncClient):
    # 1. Test Inscription
    register_payload = {
        "email": "testuser@example.com",
        "password": "Password123!",
        "full_name": "Test User"
    }
    response = await client.post("/api/v1/auth/register", json=register_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data

    # 2. Test Connexion
    login_payload = {
        "username": "testuser@example.com",
        "password": "Password123!"
    }
    login_response = await client.post("/api/v1/auth/login", data=login_payload)
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # 3. Test Profil Me avec Token JWT
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    me_response = await client.get("/api/v1/auth/me", headers=headers)
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["email"] == "testuser@example.com"
