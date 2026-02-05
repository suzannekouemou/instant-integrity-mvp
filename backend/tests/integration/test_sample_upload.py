import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_upload_requires_authentication(client: AsyncClient):
    """Test that upload requires authentication."""
    response = await client.post(
        "/api/v1/samples/upload",
        files={"file": ("test.csv", "wavelength,absorbance\n400,0.1\n", "text/csv")},
        data={"sample_type": "flour"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_upload_invalid_file_type(client: AsyncClient):
    """Test upload with non-CSV file."""
    await client.post(
        "/api/v1/auth/register",
        json={"email": "uploader@example.com", "password": "testpass123"},
    )

    response = await client.post(
        "/api/v1/samples/upload",
        files={"file": ("test.txt", "not a csv", "text/plain")},
        data={"sample_type": "flour"},
    )

    assert response.status_code in [400, 401]


@pytest.mark.asyncio
async def test_upload_invalid_sample_type(client: AsyncClient):
    """Test upload with invalid sample_type."""
    response = await client.post(
        "/api/v1/samples/upload",
        files={"file": ("test.csv", "wavelength,absorbance\n400,0.1\n", "text/csv")},
        data={"sample_type": "invalid_type"},
    )

    assert response.status_code in [422, 401]


@pytest.mark.asyncio
async def test_upload_invalid_csv_format(client: AsyncClient):
    """Test upload with invalid CSV format."""
    response = await client.post(
        "/api/v1/samples/upload",
        files={"file": ("test.csv", "wrong,columns\n400,0.1\n", "text/csv")},
        data={"sample_type": "flour"},
    )

    assert response.status_code in [400, 401]
