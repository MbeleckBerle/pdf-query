from typing import Union

from fastapi import FastAPI, Depends, APIRouter, UploadFile
from typing import Annotated

# from database import create_db_and_tables

# import models

from services import pdf_route

router = APIRouter(prefix="/document", tags=["document"])


@router.get("/")
async def read_root():
    return {"Hello": "World"}


@router.post("/upload_document")
async def upload_document(file: UploadFile):
    return await pdf_route.upload_document(file)
