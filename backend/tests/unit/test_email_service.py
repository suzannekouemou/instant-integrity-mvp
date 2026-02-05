import pytest
from app.services.email_service import send_verification_email


@pytest.mark.asyncio
async def test_send_verification_email():
    """Test email sending (no-op in dev)."""
    result = await send_verification_email("test@example.com", "test-token")
    assert result is True
