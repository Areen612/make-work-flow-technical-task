import asyncio
from collections.abc import Iterator
from datetime import UTC, datetime

import pytest
from httpx import ASGITransport, AsyncClient, Response
from sqlalchemy.exc import SQLAlchemyError

from db import get_db
from main import app
from model import User


class ScalarResult:
    def __init__(self, users: list[User]) -> None:
        self.users = users

    def all(self) -> list[User]:
        return self.users


class SuccessfulSession:
    def __init__(self, users: list[User]) -> None:
        self.users = users

    def scalars(self, _: object) -> ScalarResult:
        return ScalarResult(self.users)


class FailingSession:
    def scalars(self, _: object) -> ScalarResult:
        raise SQLAlchemyError("database unavailable")


@pytest.fixture(autouse=True)
def reset_dependency_overrides() -> Iterator[None]:
    yield
    app.dependency_overrides.clear()


async def request_users() -> Response:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        return await client.get("/users")


def test_get_users_returns_database_users() -> None:
    timestamp = datetime(2026, 1, 1, tzinfo=UTC)
    users = [
        User(
            id=1,
            name="Alice Johnson",
            email="alice@example.com",
            created_at=timestamp,
            updated_at=timestamp,
        )
    ]

    def override_get_db() -> Iterator[SuccessfulSession]:
        yield SuccessfulSession(users)

    app.dependency_overrides[get_db] = override_get_db

    response = asyncio.run(request_users())

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-01T00:00:00Z",
        }
    ]


def test_get_users_handles_database_errors() -> None:
    def override_get_db() -> Iterator[FailingSession]:
        yield FailingSession()

    app.dependency_overrides[get_db] = override_get_db

    response = asyncio.run(request_users())

    assert response.status_code == 500
    assert response.json() == {"detail": "Failed to fetch users"}
