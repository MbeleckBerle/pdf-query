import io

from typing import Annotated

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from sqlmodel import Session

# from PyPDF2 import PdfReader

# from schemas import Documents_create

# from database import SessionDep


from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import Client, create_client
from langchain_google_genai import GoogleGenerativeAIEmbeddings


from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

from dotenv import load_dotenv
import os

# Load environment variables from .env
env_path = "../backend/.env"
load_dotenv(dotenv_path=env_path)

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# # Construct the SQLAlchemy connection string
supabase_url = os.getenv("SUPABASE_URL")
google_genai_key = os.environ.get("GOOGLE_GENAI_KEY")


supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


# embeddings = GoogleGenerativeAIEmbeddings(
#     model="models/gemini-embedding-exp-03-07", key=google_genai_key
# )

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-exp-03-07",
    google_api_key=google_genai_key,
)

# vector = embeddings.embed_query("hello, world!")
# print(vector[:5])


async def upload_document():
    loader = TextLoader("data.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    vector_store = SupabaseVectorStore.from_documents(
        docs,
        embeddings,
        client=supabase,
        table_name="documents",
        query_name="match_documents",
        chunk_size=500,
    )

    vector_store = SupabaseVectorStore(
        embedding=embeddings,
        client=supabase,
        table_name="documents",
        query_name="match_documents",
    )

    query = "How is data science related to statistics?"
    matched_docs = vector_store.similarity_search(query)
    print(docs)
    print("\n")
    print(documents)
    print(type(docs), type(docs))

    return {"Matched_docs": matched_docs}

    # embeddings = GoogleGenerativeAIEmbeddings(
    #     model="models/gemini-embedding-exp-03-07",
    #     google_api_key=google_genai_key,
    # )
    # vector = embeddings.embed_query("hello, world!")
    # vector[:5]


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
