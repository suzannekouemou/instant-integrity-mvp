import logging
from typing import Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse

try:
    import sentry_sdk
except ImportError:
    sentry_sdk = None

logger = logging.getLogger(__name__)


async def global_exception_handler(request: Request, call_next: Callable) -> Response:
    """Global exception handler middleware that catches unhandled exceptions."""
    try:
        return await call_next(request)
    except Exception as exc:
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        
        if sentry_sdk is not None:
            sentry_sdk.capture_exception(exc)
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"}
        )
