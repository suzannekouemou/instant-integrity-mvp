import pytest
from app.utils.tokens import create_verification_token, verify_verification_token


def test_create_verification_token():
    """Test verification token creation."""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    token = create_verification_token(user_id)
    
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_verify_verification_token():
    """Test verification token validation."""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    token = create_verification_token(user_id)
    
    # Valid token
    decoded_id = verify_verification_token(token, max_age_hours=24)
    assert decoded_id == user_id
    
    # Invalid token
    invalid_decoded = verify_verification_token("invalid-token", max_age_hours=24)
    assert invalid_decoded is None
