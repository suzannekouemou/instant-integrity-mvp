import pytest
from app.core.security import create_access_token


def test_jwt_token_structure():
    """Test JWT token structure and claims."""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    role = "user"
    
    token = create_access_token(subject=user_id, role=role, expires_minutes=60)
    
    assert token is not None
    assert isinstance(token, str)
    assert len(token.split('.')) == 3  # JWT has 3 parts
