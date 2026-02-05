import pytest
from httpx import AsyncClient
from uuid import uuid4


def unique_email(prefix: str = "test") -> str:
    return f"{prefix}_{uuid4().hex[:8]}@example.com"


@pytest.mark.asyncio
async def test_user_registration(client: AsyncClient):
    """Test user registration endpoint."""
    email = unique_email("register")
    response = await client.post(
        "/api/v1/auth/register", json={"email": email, "password": "testpass123"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == email
    assert data["email_verified"] is False
    assert "id" in data


@pytest.mark.asyncio
async def test_duplicate_registration(client: AsyncClient):
    """Test duplicate email registration."""
    email = unique_email("duplicate")
    user_data = {"email": email, "password": "testpass123"}

    response1 = await client.post("/api/v1/auth/register", json=user_data)
    assert response1.status_code == 201

    response2 = await client.post("/api/v1/auth/register", json=user_data)
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"].lower()


@pytest.mark.asyncio
async def test_invalid_email_registration(client: AsyncClient):
    """Test registration with invalid email."""
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "invalid-email", "password": "testpass123"},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_short_password_registration(client: AsyncClient):
    """Test registration with short password."""
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": unique_email("short"), "password": "short"},
    )

    assert response.status_code == 422
