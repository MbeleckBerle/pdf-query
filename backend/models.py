from typing import List

from sqlmodel import Field, SQLModel, Column, JSON


class documents(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    filename: str = Field(index=True)
    embedding: List[float] = Field(sa_column=Column(JSON))
