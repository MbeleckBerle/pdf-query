from typing import Union

from fastapi import FastAPI, Depends, APIRouter, UploadFile
from typing import Annotated

# from database import create_db_and_tables

# import models

from services import pdf_route

import io
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import json

from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import create_client
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter


import torch
from transformers import pipeline

router = APIRouter(prefix="/query", tags=["send query"])


load_dotenv("../backend/.env")

# Environment variables
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(supabase_url, supabase_key)

# FastAPI app
app = FastAPI()

# SentenceTransformer via LangChain wrapper
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


pipe = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    # device=0,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)


@router.get("/{query}")
async def send_query(query: str):

    try:
        # Create Supabase vector store
        vector_store = SupabaseVectorStore.from_documents(
            "",
            embedding_model,
            client=supabase,
            table_name="documents",
            query_name="match_documents",
        )

        # # Example query
        # query = "what is data science?"
        results = vector_store.similarity_search(query, k=1)
        content = str(results[0].page_content).replace("\n", " ")

        messages = [
            {
                "role": "system",
                "content": f"only use the proviced to answer the question{content}",
            },
            {
                "role": "user",
                "content": f"{query}",
            },
        ]

        prompt = pipe.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        response = pipe(
            prompt,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
        )

        return {
            "response": str(response[0]["generated_text"].split("<|assistant|>")[1])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
