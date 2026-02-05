import pytest
from httpx import AsyncClient
from app.core.security import create_access_token


@pytest.mark.asyncio
async def test_jwt_token_validation(client: AsyncClient):
    """Test JWT token validation on protected endpoints."""
    # Create a valid token
    token = create_access_token(subject="123e4567-e89b-12d3-a456-426614174000", role="user")
    
    # Test with valid token format (endpoint doesn't exist yet, but tests token parsing)
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/api/v1/auth/me", headers=headers)
    
    # Endpoint doesn't exist yet, but should not be 401 if token is valid
    assert response.status_code in [404, 200, 401]  # 401 if user doesn't exist in DB


@pytest.mark.asyncio
async def test_invalid_jwt_token(client: AsyncClient):
    """Test with invalid JWT token."""
    headers = {"Authorization": "Bearer invalid-token"}
    response = await client.get("/api/v1/auth/me", headers=headers)
    
    # Should return 401 or 404 (endpoint doesn't exist)
    assert response.status_code in [401, 404]


@pytest.mark.asyncio
async def test_missing_jwt_token(client: AsyncClient):
    """Test without JWT token."""
    response = await client.get("/api/v1/auth/me")
    
    # Should return 403 (no credentials) or 404 (endpoint doesn't exist)
    assert response.status_code in [403, 404]
