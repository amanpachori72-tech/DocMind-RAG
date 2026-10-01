from fastapi import FastAPI, UploadFile, File
import shutil
import os

from pydantic import BaseModel

from app.generation.rag_pipeline import RAGPipeline
from app.ingestion.document_processor import DocumentProcessor


app = FastAPI(
    title="DocMind API",
    description="RAG-based document question answering system",
    version="1.0.0"
)


rag = RAGPipeline()
processor = DocumentProcessor()


class QuestionRequest(BaseModel):
    question: str
    document_id: str
    history: list[dict] = []


@app.get("/")
def root():
    return {
        "message": "DocMind API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    os.makedirs("data/documents", exist_ok=True)

    file_path = os.path.join(
        "data/documents",
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = processor.process(file_path)

    return {
    "filename": file.filename,
    "document_id": result["document_id"],
    "message": "Document uploaded and processed successfully",
    "pages": result["pages"],
    "chunks": result["chunks"]
}

@app.post("/ask")
def ask_question(request: QuestionRequest):

    result = rag.ask (  
    request.question,
    top_k = 8,
     history=request.history ,
     document_id=request.document_id
)

    return {
    "question": request.question,
    "answer": result["answer"], 
    "sources": result["sources"]
}