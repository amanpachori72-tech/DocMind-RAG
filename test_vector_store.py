from app.ingestion.pdf_loader import load_pdf
from app.ingestion.text_splitter import split_documents
from app.retrieval.embedding_model import EmbeddingModel
from app.retrieval.vector_store import VectorStore


# 1. Load PDF
pdf_path = "data/documents/AResume.pdf"

documents = load_pdf(pdf_path)

print(f"Pages loaded: {len(documents)}")


# 2. Split into chunks
chunks = split_documents(documents)

print(f"Chunks created: {len(chunks)}")


# 3. Create embedding model
embedding_model = EmbeddingModel()


# 4. Generate embeddings
texts = [chunk["text"] for chunk in chunks]

embeddings = [
    embedding_model.embed_text(text)
    for text in texts
]

print(f"Embeddings generated: {len(embeddings)}")


# 5. Store everything in ChromaDB
vector_store = VectorStore()

vector_store.add_documents(
    chunks,
    embeddings
)

print("Documents successfully stored in ChromaDB!")