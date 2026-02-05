from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


# Import models to ensure they're registered with Base
from .user import User
from .email_token import EmailVerificationToken
from .sample import Sample
from .result import Result
from .batch import Batch
