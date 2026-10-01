# 🧠 DocMind — Intelligent Document Q&A using RAG

DocMind is a Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask natural-language questions about their contents.

The system combines semantic search, keyword-based retrieval, cross-encoder reranking, and an LLM to generate grounded answers with document/page sources.

---

## 🚀 Features

- 📄 PDF document upload
- ✂️ Line-aware document chunking
- 🔢 Sentence Transformer embeddings
- 🗄️ Persistent ChromaDB vector storage
- 🔍 Semantic retrieval
- 🔤 Keyword-based retrieval
- 🔀 Hybrid retrieval
- 🎯 Cross-encoder reranking
- 🤖 Groq-powered LLM generation
- 💬 Conversation memory for follow-up questions
- 📚 Source and page references
- 🔒 Document-level retrieval isolation
- ⚡ FastAPI backend
- 🖥️ Streamlit frontend
- 📊 RAG evaluation framework

---

## 🏗️ Architecture

```text
                         ┌─────────────────┐
                         │  Streamlit UI   │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   FastAPI API   │
                         └────────┬────────┘
                                  │
                 ┌────────────────┴────────────────┐
                 │                                 │
                 ▼                                 ▼
        ┌─────────────────┐               ┌─────────────────┐
        │ Document Upload │               │  User Question  │
        └────────┬────────┘               └────────┬────────┘
                 │                                 │
                 ▼                                 ▼
        ┌─────────────────┐               ┌─────────────────┐
        │   PDF Loader    │               │    Retriever    │
        └────────┬────────┘               └────────┬────────┘
                 │                                  │
                 ▼                         ┌────────┴────────┐
        ┌─────────────────┐                │                 │
        │ Text Splitter   │                ▼                 ▼
        └────────┬────────┘         Semantic Search   Keyword Search
                 │                         │                 │
                 ▼                         └────────┬────────┘
        ┌─────────────────┐                         │
        │ Embedding Model │                         ▼
        └────────┬────────┘                ┌─────────────────┐
                 │                         │    Reranker     │
                 ▼                         └────────┬────────┘
        ┌─────────────────┐                         │
        │    ChromaDB     │◄────────────────────────┘
        └─────────────────┘                         │
                                                    ▼
                                           ┌─────────────────┐
                                           │   RAG Pipeline  │
                                           └────────┬────────┘
                                                    │
                                                    ▼
                                           ┌─────────────────┐
                                           │    Groq LLM     │
                                           └────────┬────────┘
                                                    │
                                                    ▼
                                           Answer + Sources

                                           🔄 RAG Pipeline
1. Document Ingestion

The uploaded PDF is processed through:

PDF
 ↓
Text Extraction
 ↓
Line-aware Chunking
 ↓
Document ID Assignment
 ↓
Embedding Generation
 ↓
ChromaDB

Each chunk stores metadata including:

Document ID
Source
Page number
2. Retrieval

When a user asks a question:

Question
   ↓
Query Embedding
   ↓
Semantic Retrieval
   +
Keyword Retrieval
   ↓
Candidate Combination
   ↓
Cross-Encoder Reranking
   ↓
Top Relevant Chunks
3. Generation

The retrieved chunks are supplied to the LLM as context.

The model is instructed to:

Use retrieved document context as the factual source
Use conversation history only for understanding follow-up questions
Avoid inventing information
Return a fallback response when the information cannot be found
Preserve document source references
🔒 Multi-Document Isolation

DocMind supports multiple uploaded documents without mixing their retrieval results.

Each processed document receives a document_id.

For example:

AResume.pdf
    ↓
document_id = AResume.pdf

During retrieval, ChromaDB filters results using the selected document ID.

This prevents a question about one uploaded document from retrieving chunks belonging to another document.

🛠️ Tech Stack
Component	Technology
Language	Python
Backend	FastAPI
Frontend	Streamlit
Embeddings	Sentence Transformers
Embedding Model	all-MiniLM-L6-v2
Vector Database	ChromaDB
Reranker	cross-encoder/ms-marco-MiniLM-L-6-v2
LLM Provider	Groq
PDF Processing	pypdf
API Communication	REST
Environment Management	python-dotenv
📁 Project Structure
DocMind-RAG/
│
├── app/
│   ├── api/
│   │   └── main.py
│   │
│   ├── generation/
│   │   ├── llm.py
│   │   └── rag_pipeline.py
│   │
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   ├── text_splitter.py
│   │   └── document_processor.py
│   │
│   ├── retrieval/
│   │   ├── embedding_model.py
│   │   ├── retriever.py
│   │   ├── reranker.py
│   │   └── vector_store.py
│   │
│   └── ui/
│       └── streamlit_app.py
│
├── tests/
│   ├── evaluation_questions.py
│   └── evaluate_rag.py
│
├── test_database.py
├── test_embeddings.py
├── test_llm.py
├── test_loader.py
├── test_processor.py
├── test_rag.py
├── test_reranker.py
├── test_retrieval.py
├── test_vector_store.py
│
├── .gitignore
└── README.md
⚙️ Installation
1. Clone the repository
git clone https://github.com/amanpachori72-tech/DocMind-RAG.git
cd DocMind-RAG
2. Create a virtual environment
python -m venv venv

Activate it on Windows:

venv\Scripts\activate
3. Install dependencies
pip install pypdf python-dotenv sentence-transformers chromadb groq fastapi uvicorn python-multipart streamlit requests
4. Configure environment variables

Create a .env file:

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b

Never commit your .env file.

▶️ Running the Application
Start the FastAPI backend
uvicorn app.api.main:app --reload

The API will run at:

http://127.0.0.1:8000
Start the Streamlit frontend

Open another terminal:

python -m streamlit run app/ui/streamlit_app.py

Streamlit will provide the local web interface.

🧪 Evaluation

DocMind includes an evaluation framework containing predefined questions and expected facts.

The current evaluation baseline is:

90% — 9/10 questions

The evaluation checks whether the generated response contains the required facts rather than relying only on exact string matching.

Example evaluation categories include:

Skills
Projects
Experience
Education
Certifications
🔐 Security

The repository intentionally excludes:

.env
venv/
data/chroma_db/
data/documents/

API keys and locally uploaded documents should never be committed to the repository.

📌 Future Improvements

Planned improvements include:

Multi-document UI selection
Better conversation management
Streaming LLM responses
Improved chunking strategies
Retrieval evaluation metrics
Better observability and logging
Docker deployment
Cloud deployment
Authentication
Automated testing and CI/CD
👨‍💻 Author

Aman Pachori

B.Tech — Internet of Things / AI & ML

GitHub:
https://github.com/amanpachori72-tech

⭐ Project Goal

DocMind was built as a practical implementation of a production-style RAG pipeline, focusing on retrieval quality, document grounding, reranking, source attribution, and document isolation rather than simply connecting an LLM to a PDF.