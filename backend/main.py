from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

import google.generativeai as genai
import numpy as np
import faiss
import pickle
import os
import shutil

# =========================
# CONFIG
# =========================

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

app = FastAPI()

chat_history = []

UPLOAD_FOLDER = "uploaded_pdfs"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.mount(
    "/pdfs",
    StaticFiles(directory=UPLOAD_FOLDER),
    name="pdfs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# EMBEDDING MODEL
# =========================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# =========================
# HOME
# =========================

@app.get("/")
def home():
    return {
        "message": "Backend Running"
    }

# =========================
# UPLOAD PDF
# =========================

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):
    try:

        # Save PDF file
        pdf_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(
            pdf_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # Reset pointer
        file.file.seek(0)

        # Read PDF
        reader = PdfReader(
            file.file
        )

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        # Split text
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

        chunks = splitter.split_text(
            text
        )

        # Create document objects
        new_documents = []

        for chunk in chunks:

            new_documents.append({
                "text": chunk,
                "source": file.filename
            })

        # Load existing documents
        all_documents = []

        if os.path.exists("documents.pkl"):
            with open("documents.pkl", "rb") as f:
                all_documents = pickle.load(f)
        all_documents.extend(
            new_documents
        )

        # Save documents
        with open(
            "documents.pkl",
            "wb"
        ) as f:

            pickle.dump(
                all_documents,
                f
            )

        # Create embeddings
        all_texts = [
            doc["text"]
            for doc in all_documents
        ]

        embeddings = embedding_model.encode(
            all_texts
        )

        embeddings = np.array(
            embeddings,
            dtype=np.float32
        )

        # Build FAISS
        dimension = embeddings.shape[1]

        index = faiss.IndexFlatL2(
            dimension
        )

        index.add(
            embeddings
        )

        faiss.write_index(
            index,
            "faiss_index.bin"
        )

        return {
            "success": True,
            "filename": file.filename,
            "chunks_added": len(chunks),
            "total_chunks": len(all_documents),
            "message": "PDF added successfully"
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
@app.delete("/delete-pdf/{filename}")
async def delete_pdf(filename: str):
    try:

        pdf_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        if not os.path.exists(pdf_path):
            return {
                "success": False,
                "error": "PDF not found"
            }

        # Delete PDF file
        os.remove(pdf_path)

        # Remove chunks from documents.pkl
        if os.path.exists("documents.pkl"):

            with open(
                "documents.pkl",
                "rb"
            ) as f:
                documents = pickle.load(f)

            documents = [
                doc
                for doc in documents
                if doc["source"] != filename
            ]

            with open(
                "documents.pkl",
                "wb"
            ) as f:
                pickle.dump(
                    documents,
                    f
                )

        # Rebuild FAISS index
        if len(documents) > 0:

            texts = [
                doc["text"]
                for doc in documents
            ]

            embeddings = embedding_model.encode(
                texts
            )

            embeddings = np.array(
                embeddings,
                dtype=np.float32
            )

            index = faiss.IndexFlatL2(
                embeddings.shape[1]
            )

            index.add(
                embeddings
            )

            faiss.write_index(
                index,
                "faiss_index.bin"
            )

        return {
            "success": True,
            "message": "PDF deleted successfully"
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

# =========================
# LIST DOCUMENT NAMES
# =========================

@app.get("/documents")
async def get_documents():

    if not os.path.exists(
        "documents.pkl"
    ):
        return {
            "documents": []
        }

    with open(
        "documents.pkl",
        "rb"
    ) as f:

        documents = pickle.load(f)

    filenames = list(
        set(
            doc["source"]
            for doc in documents
        )
    )

    return {
        "documents": filenames
    }

# =========================
# PDF LIST WITH URLS
# =========================

@app.get("/pdf-list")
async def pdf_list():

    files = []

    if os.path.exists(
        UPLOAD_FOLDER
    ):

        for file in os.listdir(
            UPLOAD_FOLDER
        ):

            files.append({
                "name": file,
                "url": f"http://localhost:8000/pdfs/{file}"
            })

    return {
        "files": files
    }

# =========================
# ASK QUESTION
# =========================

@app.post("/ask")
async def ask_question(
    data: dict = Body(...)
):
    try:

        question = data["question"]

        pdf_name = data.get(
    "pdf_name",
    ""
)

        history_text = ""

        for chat in chat_history:

            history_text += (
                f"User: {chat['question']}\n"
                f"Assistant: {chat['answer']}\n\n"
            )

        with open(
            "documents.pkl",
            "rb"
        ) as f:

            documents = pickle.load(f)

        filtered_texts = [
    doc["text"]
    for doc in documents
]
        filtered_embeddings = embedding_model.encode(
    filtered_texts
)
        filtered_embeddings = np.array(
    filtered_embeddings,
    dtype=np.float32
)
        filtered_index = faiss.IndexFlatL2(
    filtered_embeddings.shape[1]
)
        filtered_index.add(
    filtered_embeddings
)
        question_embedding = embedding_model.encode(
    [question]
)
        question_embedding = np.array(
    question_embedding,
    dtype=np.float32
)
        k = min(
    3,
    len(documents)
)
        distances, indices = filtered_index.search(
    question_embedding,
    k=k
)
        

        retrieved_chunks = []

        for idx in indices[0]:

            if idx < len(documents):

                retrieved_chunks.append(
                    f"""
Source: {documents[idx]['source']}

Content:
{documents[idx]['text']}
"""
                )

        context = "\n\n".join(
            retrieved_chunks
        )

        prompt = f"""
You are a helpful PDF assistant.

Use ONLY the document context below.

If the answer is not present in the context,
reply exactly:

I could not find that information in the selected PDF.

Do not use outside knowledge.

Previous Conversation:
{history_text}

Document Context:
{context}

Question:
{question}
"""

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        response = model.generate_content(
            prompt
        )

        answer = response.text

        chat_history.append({
            "question": question,
            "answer": answer
        })

        return {
            "success": True,
            "answer": answer
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

# =========================
# CLEAR CHAT
# =========================

@app.post("/clear-chat")
async def clear_chat():

    global chat_history

    chat_history = []

    return {
        "success": True,
        "message": "Chat history cleared"
    }