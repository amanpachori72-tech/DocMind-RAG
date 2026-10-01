import os

from app.ingestion.pdf_loader import load_pdf
from app.ingestion.text_splitter import split_documents
from app.retrieval.embedding_model import EmbeddingModel
from app.retrieval.vector_store import VectorStore


class DocumentProcessor:

    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore()

    def process(self, file_path):

        # 1. Create a document identifier
        document_id = os.path.basename(file_path)

        # 2. Load PDF
        documents = load_pdf(file_path)

        # 3. Split into chunks
        chunks = split_documents(documents)

        # 4. Attach document ID to every chunk
        for chunk in chunks:
            chunk["document_id"] = document_id

        # 5. Generate embeddings
        embeddings = [
            self.embedding_model.embed_text(chunk["text"])
            for chunk in chunks
        ]

        # 6. Store chunks + embeddings + metadata
        self.vector_store.add_documents(
            chunks,
            embeddings
        )

        return {
            "document_id": document_id,
            "pages": len(documents),
            "chunks": len(chunks)
        }