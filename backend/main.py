import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db import Base, SessionLocal, engine, get_db
from model import User
from schemas import MessageResponse, UserResponse


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DatabaseSession = Annotated[Session, Depends(get_db)]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # Create the schema and seed demo users once when the app starts.
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        user_exists = db.scalar(select(User.id).limit(1))

        if user_exists is None:
            db.add_all(
                [
                    User(
                        name="Alice Johnson",
                        email="alice@example.com",
                    ),
                    User(
                        name="Bob Smith",
                        email="bob@example.com",
                    ),
                ]
            )
            db.commit()
            logger.info("Seeded initial users")

    yield


app = FastAPI(
    title="MAKE WORK FLOW API",
    lifespan=lifespan,
)


@app.get("/")
def root() -> MessageResponse:
    return MessageResponse(message="MAKE WORK FLOW backend is running")


@app.get("/users")
def get_users(db: DatabaseSession) -> list[UserResponse]:
    try:
        users = db.scalars(select(User)).all()
        return [UserResponse.model_validate(user) for user in users]

    except SQLAlchemyError as exc:
        logger.exception("Failed to fetch users")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch users",
        ) from exc
