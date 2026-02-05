from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.rate_limit import limiter
from app.schemas.auth import UserCreate, UserResponse, Token, LoginRequest
from app.services.auth_service import create_user, verify_email, authenticate_user
from app.core.security import create_access_token

router = APIRouter()


def rate_limit_decorator(limit_string: str):
    """Return rate limit decorator if limiter is enabled, else passthrough."""
    if limiter:
        return limiter.limit(limit_string)
    return lambda func: func


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
@rate_limit_decorator("3/hour")
async def register(
    request: Request, user_data: UserCreate, db: AsyncSession = Depends(get_session)
):
    """Register a new user and send verification email."""
    try:
        user, _ = await create_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/verify-email", response_model=dict)
async def verify_email_endpoint(
    token: str = Query(...), db: AsyncSession = Depends(get_session)
):
    """Verify user email with token."""
    try:
        user = await verify_email(db, token)
        return {"message": "Email verified successfully", "email": user.email}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=Token)
@rate_limit_decorator("5/minute")
async def login(
    request: Request, credentials: LoginRequest, db: AsyncSession = Depends(get_session)
):
    """Login with email and password."""
    user = await authenticate_user(db, credentials.email, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified"
        )

    access_token = create_access_token(subject=str(user.id), role=user.role)
    return Token(access_token=access_token)
