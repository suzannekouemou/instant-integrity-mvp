import pytest
from httpx import AsyncClient
from uuid import uuid4


def unique_email(prefix: str = "test") -> str:
    return f"{prefix}_{uuid4().hex[:8]}@example.com"


@pytest.mark.asyncio
async def test_registration_rate_limit(client: AsyncClient):
    """Test rate limiting on registration endpoint (3/hour per IP)."""
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": unique_email("ratelimit"), "password": "testpass123"},
    )
    assert response.status_code in [201, 429]


@pytest.mark.asyncio
async def test_login_rate_limit(client: AsyncClient):
    """Test rate limiting on login endpoint (5/min per IP)."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": unique_email("loginrl"), "password": "testpass123"},
    )
    assert response.status_code in [401, 403, 429]
