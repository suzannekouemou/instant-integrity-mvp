import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_result_retrieval_requires_auth(client: AsyncClient):
    """Test that result retrieval requires authentication."""
    sample_id = uuid4()
    response = await client.get(f"/api/v1/results/{sample_id}")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_nonexistent_sample(client: AsyncClient):
    """Test retrieval of non-existent sample."""
    sample_id = uuid4()
    response = await client.get(f"/api/v1/results/{sample_id}")

    assert response.status_code in [401, 404]


@pytest.mark.asyncio
async def test_invalid_sample_id_format(client: AsyncClient):
    """Test with invalid UUID format."""
    response = await client.get("/api/v1/results/invalid-uuid")

    assert response.status_code in [422, 401]
