import io

from typing import Annotated

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from sqlmodel import Session

from PyPDF2 import PdfReader

from schemas import Documents_create
from database import SessionDep


from langchain_openai import OpenAIEmbeddings


async def upload_document(file: UploadFile = File(...)):
    return {"file name": file.filename, "message": "File uploaded"}

    # # 1) Read the file bytes
    # contents = await file.read()
    # if not contents:
    #     raise HTTPException(400, "Empty file")

    # # 2) Load into a BytesIO and parse with PyPDF2
    # try:
    #     reader = PdfReader(io.BytesIO(contents))
    # except Exception:
    #     raise HTTPException(400, "Failed to parse PDF")

    # # 3) Extract text from each page
    # text_pages = []
    # for page in reader.pages:
    #     page_text = page.extract_text()
    #     if page_text:
    #         text_pages.append(page_text)
    # full_text = "\n\n".join(text_pages)

    # if not full_text:
    #     raise HTTPException(400, "No extractable text found in PDF")

    # # 4) Return a preview
    # preview = full_text  # first 1,000 characters
    # return JSONResponse(
    #     {
    #         "filename": file.filename,
    #         "content_type": file.content_type,
    #         "preview": preview,
    #     }
    # )
