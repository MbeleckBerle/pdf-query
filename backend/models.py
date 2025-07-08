from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, Column, JSON


class documents(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    filename: str = Field(index=True)
    embedding: List[float] = Field(sa_column=Column(JSON))
