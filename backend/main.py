import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlalchemy import select

from db import Base, SessionLocal, engine
from model import User


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
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
    lifespan=lifespan
)


@app.get("/")
def root():
    return {"message": "MAKE WORK FLOW backend is running"}


@app.get("/users")
def get_users():
    try:
        with SessionLocal() as db:
            users = db.scalars(select(User)).all()  # scalars() returns a list of User objects instead of a list of Row objects

            return users

    except Exception as e:
        logger.exception("Failed to fetch users")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch users",
        ) from e