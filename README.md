# DocMind

> AI-powered PDF Chatbot built using **Retrieval-Augmented Generation (RAG)**, **FastAPI**, **React**, **FAISS**, and **Google Gemini**.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Database-orange)
![Gemini](https://img.shields.io/badge/Google-Gemini-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Overview

DocMind is an AI-powered document assistant that enables users to upload PDF documents and interact with them using natural language.

The application leverages **Retrieval-Augmented Generation (RAG)** to retrieve semantically relevant document chunks using **FAISS** and generate context-aware responses using **Google Gemini**.

---

## Features

- Upload and manage multiple PDF documents
- Natural language question answering
- Retrieval-Augmented Generation (RAG)
- Semantic search with FAISS
- Automatic PDF text chunking
- Integrated PDF viewer
- Persistent vector storage
- Conversation history
- REST API built with FastAPI
- Modern React-based user interface
- Deployable on Render and Vercel

---

## Architecture

```text
                User
                  │
                  ▼
           React Frontend
                  │
                  ▼
          FastAPI Backend
                  │
      ┌───────────┴───────────┐
      ▼                       ▼
 PDF Processing          User Question
      │                       │
      ▼                       ▼
 Text Chunking        Query Embedding
      │                       │
      ▼                       ▼
 Gemini Embeddings    Gemini Embeddings
      │                       │
      └───────────┬───────────┘
                  ▼
          FAISS Vector Search
                  │
                  ▼
        Relevant Context Chunks
                  │
                  ▼
         Gemini 2.5 Flash
                  │
                  ▼
            Final Response
```

---

## Technology Stack

### Frontend

- React
- Vite
- Axios
- CSS

### Backend

- FastAPI
- Python
- Google Gemini API
- FAISS
- NumPy
- PyPDF
- LangChain Text Splitters

### Deployment

- Render
- Vercel

---

## Project Structure

```text
DocMind
│
├── backend
│   ├── app
│   │   ├── config.py
│   │   ├── llm_service.py
│   │   ├── pdf_processor.py
│   │   ├── rag_service.py
│   │   ├── retriever.py
│   │   └── vector_store.py
│   │
│   ├── uploaded_pdfs
│   ├── main.py
│   └── requirements.txt
│
├── frontend
│   ├── src
│   ├── public
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## How It Works

### 1. Document Processing

Uploaded PDF files are processed using **PyPDF**, and the extracted text is divided into semantic chunks using LangChain's Recursive Character Text Splitter.

### 2. Embedding Generation

Each document chunk is converted into vector embeddings using Google's **Gemini Embedding Model**.

### 3. Vector Indexing

The generated embeddings are stored in a **FAISS** vector database for efficient similarity search.

### 4. Retrieval

For every user query:

- Generate query embeddings
- Search FAISS for the most relevant document chunks
- Retrieve contextual information
- Pass the retrieved context to Gemini

### 5. Response Generation

Gemini generates a concise response using only the retrieved document context, ensuring answers remain grounded in the uploaded PDFs.

---

## RAG Pipeline

```text
User Question
      │
      ▼
Generate Query Embedding
      │
      ▼
FAISS Similarity Search
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
Construct Prompt
      │
      ▼
Gemini LLM
      │
      ▼
Final Answer
```

---

## API Endpoints

| Method | Endpoint | Description |
|----------|-------------------------|--------------------------|
| GET | `/` | Health Check |
| POST | `/upload` | Upload a PDF |
| GET | `/pdf-list` | List uploaded PDFs |
| DELETE | `/delete-pdf/{filename}` | Delete a PDF |
| POST | `/ask` | Ask questions |
| POST | `/clear-chat` | Clear chat history |

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/DocMind.git

cd DocMind
```

### Backend

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## Environment Variables

### Backend (`backend/.env`)

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### Frontend (`frontend/.env`)

```env
VITE_API_URL=https://your-backend.onrender.com
```

---

## Future Improvements

- User authentication
- OCR support for scanned documents
- Streaming AI responses
- Source highlighting within PDFs
- Hybrid Search (BM25 + Vector Search)
- Conversation memory
- Database integration
- Multi-agent RAG architecture

---

## License

This project is licensed under the **MIT License**.
