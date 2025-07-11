import io
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from PyPDF2 import PdfReader
from langchain_core.documents import Document
from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import create_client
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

# Load .env file
load_dotenv("../backend/.env")

# Supabase setup
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(supabase_url, supabase_key)

# FastAPI app
app = FastAPI()

# Embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    try:
        # 1) Read raw bytes
        contents = await file.read()

        # 2) Extract text depending on file type
        documents = []
        if file.filename.lower().endswith(".pdf"):
            reader = PdfReader(io.BytesIO(contents))
            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                documents.append(
                    Document(
                        page_content=text,
                        metadata={"source": file.filename, "page": i + 1},
                    )
                )
        else:
            # treat as plain text
            text = contents.decode("utf-8")
            # you can still use TextLoader, but here we just wrap in Document
            documents.append(
                Document(page_content=text, metadata={"source": file.filename})
            )

        # 3) Split into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)

        # 4) Upsert into Supabase Vector Store
        vector_store = SupabaseVectorStore.from_documents(
            docs,
            embedding_model,
            client=supabase,
            table_name="documents",
            query_name="match_documents",
        )

        # 5) Return a simple list of chunk texts (or you could issue a query)
        return JSONResponse(
            {
                "filename": file.filename,
                "chunks_stored": len(docs),
                "chunks": [doc.page_content for doc in docs],
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
