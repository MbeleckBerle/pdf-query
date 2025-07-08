from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List


class Documents_create(SQLModel):
    filename: str
    embedding: List[float]
