import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

def get_embedding(text):
    response = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document"
    )
    return response["embedding"]


def get_query_embedding(text):
    response = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_query"
    )
    return response["embedding"]

UPLOAD_FOLDER = "uploaded_pdfs"

DOCUMENTS_FILE = "documents.pkl"

INDEX_FILE = "faiss_index.bin"

VECTOR_DB = "vector_db"