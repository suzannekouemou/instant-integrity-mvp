from __future__ import annotations

from typing import Optional

from slowapi import Limiter
from slowapi.util import get_remote_address

from .config import get_settings


_settings = get_settings()


def create_limiter() -> Optional[Limiter]:
    """
    Create a configured Limiter instance or return None if rate limiting disabled.
    """
    if not _settings.RATE_LIMIT_ENABLED:
        return None

    # slowapi supports Redis via storage_uri. It will fall back to in-memory
    # store if Redis is unreachable, but here we explicitly configure redis.
    storage_uri = _settings.REDIS_URL
    limiter = Limiter(key_func=get_remote_address, storage_uri=storage_uri)
    return limiter


# Singleton-style helper used by app initialization
limiter: Optional[Limiter] = create_limiter()
