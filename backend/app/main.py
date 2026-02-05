from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import get_settings
from app.core.rate_limit import limiter
from app.middleware.error_handler import global_exception_handler

try:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
except Exception:  # pragma: no cover - optional dependency at runtime
    sentry_sdk = None  # type: ignore
    FastApiIntegration = None  # type: ignore


settings = get_settings()

app = FastAPI(title="Instant Integrity API", version="0.2.0")  # Phase 2

# Import routers
from app.routes import auth, samples, results

# CORS
origins = settings.cors_origins_list()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sentry (optional)
if settings.SENTRY_DSN and sentry_sdk is not None and FastApiIntegration is not None:  # pragma: no cover
    sentry_sdk.init(dsn=settings.SENTRY_DSN, integrations=[FastApiIntegration()], environment=settings.SENTRY_ENVIRONMENT)

# Error handling middleware
app.middleware("http")(global_exception_handler)

# Rate limiting (slowapi) – attach limiter to app.state if enabled
if limiter is not None:
    # Defer adding SlowAPIMiddleware only when limiter is configured
    from slowapi.middleware import SlowAPIMiddleware

    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)


# Phase 2: Load ML models on startup
@app.on_event("startup")
async def startup_event():
    """Load chemometric models on application startup."""
    from app.services.analysis_service import load_models
    load_models()


# Register routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(samples.router, prefix="/api/v1/samples", tags=["samples"])
app.include_router(results.router, prefix="/api/v1/results", tags=["results"])


@app.get("/health")
async def health():
    """Health check endpoint."""
    db_status = "unknown"
    redis_status = "unknown"
    
    # Check database
    try:
        from app.core.database import engine
        from sqlalchemy import text
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    
    # Check Redis
    try:
        import redis.asyncio as aioredis
        from app.core.config import get_settings
        settings = get_settings()
        if settings.RATE_LIMIT_ENABLED:
            r = aioredis.from_url(settings.REDIS_URL)
            await r.ping()
            await r.close()
            redis_status = "healthy"
        else:
            redis_status = "disabled"
    except Exception:
        redis_status = "unhealthy"
    
    overall_status = "healthy" if db_status == "healthy" else "degraded"
    
    return {
        "status": overall_status,
        "database": db_status,
        "redis": redis_status
    }
