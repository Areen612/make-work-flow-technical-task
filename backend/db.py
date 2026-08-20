from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from config import settings


engine = create_engine(settings.database_url)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    """Declarative base that provides shared metadata for all ORM models."""
    pass


def get_db() -> Generator[Session, None, None]:
    # Provide and close a database session for each request.
    with SessionLocal() as db:
        yield db
