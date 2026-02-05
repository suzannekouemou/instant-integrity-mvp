import pytest
from httpx import AsyncClient
from uuid import uuid4


def unique_email(prefix: str = "test") -> str:
    return f"{prefix}_{uuid4().hex[:8]}@example.com"


@pytest.mark.asyncio
async def test_successful_login(client: AsyncClient):
    """Test successful login flow."""
    email = unique_email("login")
    await client.post(
        "/api/v1/auth/register", json={"email": email, "password": "testpass123"}
    )

    response = await client.post(
        "/api/v1/auth/login", json={"email": email, "password": "testpass123"}
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_invalid_credentials(client: AsyncClient):
    """Test login with invalid credentials."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": unique_email("nonexistent"), "password": "wrongpass"},
    )

    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


@pytest.mark.asyncio
async def test_unverified_email_login(client: AsyncClient):
    """Test login with unverified email."""
    email = unique_email("unverified")
    await client.post(
        "/api/v1/auth/register", json={"email": email, "password": "testpass123"}
    )

    response = await client.post(
        "/api/v1/auth/login", json={"email": email, "password": "testpass123"}
    )

    assert response.status_code == 403
    assert "not verified" in response.json()["detail"].lower()
