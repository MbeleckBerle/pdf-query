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

# Load .env file
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


async def upload_document(file: UploadFile = File(...)):
    try:
        # Load and read the file
        contents = await file.read()
        text = contents.decode("utf-8")

        # Save it temporarily (optional, or stream it to loader)
        file_path = f"services/{file.filename}"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)

        # Load and split the text
        loader = TextLoader(file_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)

        # Create Supabase vector store
        vector_store = SupabaseVectorStore.from_documents(
            docs,
            embedding_model,
            client=supabase,
            table_name="documents",
            query_name="match_documents",
        )

        dtype = {
            "docs": str(type(docs)),
            "embedding model": str(type(embedding_model)),
        }
        print(dtype)
        # print(docs)

        # # Example query
        # query = "what is data science?"
        # results = vector_store.similarity_search(query, k=1)

        # return [doc.page_content for doc in (docs)]
        return docs

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#  "construct",
#     "copy",
#     "dict",
#     "from_orm",
#     "get_lc_namespace",
#     "id",
#     "is_lc_serializable",
#     "json",
#     "lc_attributes",
#     "lc_id",
#     "lc_secrets",
#     "metadata",
#     "model_computed_fields",
#     "model_config",
#     "model_construct",
#     "model_copy",
#     "model_dump",
#     "model_dump_json",
#     "model_extra",
#     "model_fields",
#     "model_fields_set",
#     "model_json_schema",
#     "model_parametrized_name",
#     "model_post_init",
#     "model_rebuild",
#     "model_validate",
#     "model_validate_json",
#     "model_validate_strings",
#     "page_content",
#     "parse_file",
#     "parse_obj",
#     "parse_raw",
#     "schema",
#     "schema_json",
#     "to_json",
#     "to_json_not_implemented",
#     "type",
#     "update_forward_refs",
#     "validate"
#   ]
# }
