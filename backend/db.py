from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = "postgresql+psycopg://localhost/make_work_flow"


engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(
    bind=engine,          # Connect sessions to this database
    autoflush=False,      # Flush changes only when we choose
    autocommit=False, 
)


class Base(DeclarativeBase):
    pass