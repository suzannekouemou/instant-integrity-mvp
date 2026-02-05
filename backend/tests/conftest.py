import os
import asyncio
from pathlib import Path
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

os.environ.setdefault(
    "DATABASE_URL", "postgresql+asyncpg:///instant_integrity?host=/var/run/postgresql"
)
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ["RATE_LIMIT_ENABLED"] = "false"


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


def get_test_db_url() -> str:
    from app.core.config import get_settings

    settings = get_settings()
    db_url = settings.DATABASE_URL
    if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return db_url


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    db_url = get_test_db_url()
    engine = create_async_engine(db_url, future=True, echo=False)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_session_factory(test_engine):
    return async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture
async def db_session(test_session_factory) -> AsyncGenerator[AsyncSession, None]:
    async with test_session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def client(test_session_factory):
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    from app.core.config import get_settings
    from app.core.database import get_session
    from app.routes import auth, samples, results
    from app.middleware.error_handler import global_exception_handler

    settings = get_settings()

    test_app = FastAPI(title="Instant Integrity API Test", version="0.2.0")

    origins = settings.cors_origins_list()
    test_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins if origins != ["*"] else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    test_app.middleware("http")(global_exception_handler)

    test_app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
    test_app.include_router(samples.router, prefix="/api/v1/samples", tags=["samples"])
    test_app.include_router(results.router, prefix="/api/v1/results", tags=["results"])

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        async with test_session_factory() as session:
            yield session

    test_app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
