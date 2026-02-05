from datetime import datetime, timedelta, timezone

from itsdangerous import URLSafeTimedSerializer

from app.core.config import get_settings


def create_verification_token(user_id: str) -> str:
    """Generate a secure URL-safe token for email verification."""
    settings = get_settings()
    serializer = URLSafeTimedSerializer(settings.JWT_SECRET)
    return serializer.dumps(user_id, salt="email-verification")


def verify_verification_token(token: str, max_age_hours: int = 24) -> str | None:
    """Verify and decode a verification token. Returns user_id or None if invalid."""
    settings = get_settings()
    serializer = URLSafeTimedSerializer(settings.JWT_SECRET)
    try:
        user_id = serializer.loads(token, salt="email-verification", max_age=max_age_hours * 3600)
        return user_id
    except Exception:
        return None
