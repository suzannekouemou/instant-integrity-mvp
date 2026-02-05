from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User
from app.models.email_token import EmailVerificationToken
from app.schemas.auth import UserCreate
from app.utils.tokens import create_verification_token, verify_verification_token
from app.services.email_service import send_verification_email
from app.core.config import get_settings


async def create_user(db: AsyncSession, user_data: UserCreate) -> tuple[User, str]:
    """Create new user, generate verification token, and send email."""
    settings = get_settings()

    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise ValueError("Email already registered")

    user = User(
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        email_verified=False,
        role="user",
    )
    db.add(user)
    await db.flush()

    token_str = create_verification_token(str(user.id))

    expires_at = datetime.utcnow() + timedelta(
        hours=settings.VERIFICATION_TOKEN_EXPIRY_HOURS
    )
    token = EmailVerificationToken(
        user_id=user.id, token=token_str, expires_at=expires_at
    )
    db.add(token)
    await db.commit()
    await db.refresh(user)

    await send_verification_email(user.email, token_str)

    return user, token_str


async def verify_email(db: AsyncSession, token: str) -> User:
    """Verify email using token and mark user as verified."""
    settings = get_settings()

    user_id_str = verify_verification_token(
        token, settings.VERIFICATION_TOKEN_EXPIRY_HOURS
    )
    if not user_id_str:
        raise ValueError("Invalid or expired token")

    user_id = UUID(user_id_str)

    result = await db.execute(
        select(EmailVerificationToken)
        .where(EmailVerificationToken.token == token)
        .where(EmailVerificationToken.user_id == user_id)
        .where(EmailVerificationToken.used == False)
    )
    db_token = result.scalar_one_or_none()

    if not db_token:
        raise ValueError("Token not found or already used")

    if db_token.expires_at < datetime.utcnow():
        raise ValueError("Token expired")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise ValueError("User not found")

    user.email_verified = True
    db_token.used = True

    await db.commit()
    await db.refresh(user)

    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    """Authenticate user with email and password. Returns user if credentials valid, None otherwise."""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user
