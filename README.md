# 📄 DocMind – AI-Powered PDF Chatbot

> Chat with your PDF documents using Retrieval-Augmented Generation (RAG), FastAPI, React, FAISS, and Google Gemini.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Database-orange)
![Gemini](https://img.shields.io/badge/Google-Gemini-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🚀 Overview

DocMind is an AI-powered document assistant that enables users to upload PDF files and interact with them using natural language.

Instead of relying on keyword-based search, DocMind leverages **Retrieval-Augmented Generation (RAG)** to understand document context, retrieve the most relevant information using vector similarity search, and generate accurate answers with Google Gemini.

---

## ✨ Features

- 📂 Upload and manage multiple PDF documents
- 💬 Ask questions in natural language
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔍 Semantic search with FAISS
- 📄 Integrated PDF Viewer
- 📑 Automatic document chunking
- 🗑 Delete uploaded PDFs
- 💾 Persistent vector database
- 📝 Conversation history
- ⚡ FastAPI REST API
- 🎨 Modern React interface
- ☁️ Cloud deployment support

---

# 🏗 Architecture

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
             Final Answer
```

---

# 🛠 Tech Stack

## Frontend

- React
- Axios
- Vite
- CSS

## Backend

- FastAPI
- Python
- Google Gemini API
- FAISS
- NumPy
- PyPDF
- LangChain Text Splitters

## Deployment

- Render
- Vercel

---

# 📁 Project Structure

```text
DocMind/
│
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   ├── llm_service.py
│   │   ├── pdf_processor.py
│   │   ├── rag_service.py
│   │   ├── retriever.py
│   │   └── vector_store.py
│   │
│   ├── uploaded_pdfs/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# ⚙️ How It Works

### 1️⃣ Upload a PDF

The uploaded document is processed using **PyPDF**.

### 2️⃣ Text Chunking

The extracted text is divided into smaller semantic chunks using LangChain's Recursive Character Text Splitter.

### 3️⃣ Embedding Generation

Each chunk is converted into vector embeddings using Google's **Gemini Embedding Model**.

### 4️⃣ Vector Indexing

Embeddings are stored inside a **FAISS** vector database for efficient similarity search.

### 5️⃣ Ask Questions

When a user submits a query:

- Generate query embeddings
- Perform semantic similarity search
- Retrieve the most relevant document chunks
- Send retrieved context to Gemini
- Return an AI-generated response based only on the document

---

# 🔍 RAG Pipeline

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
Top Relevant Chunks
      │
      ▼
Prompt + Retrieved Context
      │
      ▼
Gemini LLM
      │
      ▼
Final Answer
```

---

# 🌐 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Health Check |
| POST | `/upload` | Upload PDF |
| GET | `/pdf-list` | List Uploaded PDFs |
| DELETE | `/delete-pdf/{filename}` | Delete PDF |
| POST | `/ask` | Ask Questions |
| POST | `/clear-chat` | Clear Conversation |

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/your-username/DocMind.git

cd DocMind
```

---

## Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# 🔑 Environment Variables

### Backend (`backend/.env`)

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### Frontend (`frontend/.env`)

```env
VITE_API_URL=https://your-render-backend.onrender.com
```

---

# 📸 Demo

> Add screenshots or a GIF demonstrating:

- Uploading a PDF
- Asking questions
- Viewing the PDF
- AI-generated responses

---

# 🌟 Future Enhancements

- User authentication
- Streaming AI responses
- OCR support for scanned PDFs
- Per-document vector indexes
- Hybrid Search (BM25 + Vector Search)
- Source highlighting inside PDFs
- Conversation memory
- Multi-agent architecture
- Database integration (PostgreSQL/Supabase)

---

# 🎯 Learning Outcomes

This project demonstrates practical implementation of:

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Databases
- Large Language Models (LLMs)
- FastAPI API Development
- React Frontend Development
- Cloud Deployment
- Full-Stack AI Application Development

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!
