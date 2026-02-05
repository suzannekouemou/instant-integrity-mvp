import pytest
from app.core.security import get_password_hash, verify_password, create_access_token, decode_token


def test_password_hashing():
    """Test password hashing and verification."""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_jwt_token_creation():
    """Test JWT token creation and decoding."""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    role = "user"
    
    token = create_access_token(subject=user_id, role=role)
    assert token is not None
    
    payload = decode_token(token)
    assert payload["sub"] == user_id
    assert payload["role"] == role
    assert "exp" in payload
