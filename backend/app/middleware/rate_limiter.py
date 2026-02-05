from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.rate_limit import limiter

# Export the configured limiter for use in routes
__all__ = ["limiter"]
