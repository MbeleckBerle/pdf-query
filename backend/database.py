# from sqlalchemy import create_engine

# from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

from fastapi import Depends
from sqlmodel import SQLModel, create_engine, select, Session
from typing import Annotated

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Construct the SQLAlchemy connection string
SUPABASE_URL = (
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
)

# Create the SQLAlchemy engine
engine = create_engine(SUPABASE_URL)
# If using Transaction Pooler or Session Pooler, we want to ensure we disable SQLAlchemy client side pooling -
# https://docs.sqlalchemy.org/en/20/core/pooling.html#switching-pool-implementations
# engine = create_engine(DATABASE_URL, poolclass=NullPool)


def create_db_and_tables():
    """Create all database tables from SQLModel metadata."""

    try:
        with engine.connect() as connection:
            print("Connection successful!")
            SQLModel.metadata.create_all(engine)

    except Exception as e:
        print(f"Failed to connect: {e}")


async def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
