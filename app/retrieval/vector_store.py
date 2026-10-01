import chromadb


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="data/chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

    def add_documents(self, chunks, embeddings):

        ids = [
            f"{chunk['source']}_page_{chunk['page']}_chunk_{i}"
            for i, chunk in enumerate(chunks)
        ]

        documents = [
            chunk["text"]
            for chunk in chunks
        ]

        metadatas = [
            {
                "page": chunk["page"],
                "source": chunk["source"],
                "document_id": chunk["document_id"]
            }
            for chunk in chunks
        ]

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(self, query_embedding, top_k=3, document_id=None):

        where = None

        if document_id:
            where = {
                "document_id": document_id
            }

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where
        )

        return results

    def get_all_documents(self, document_id=None):

        where = None

        if document_id:
            where = {
            "document_id": document_id
        }

        results = self.collection.get(
        include=["documents", "metadatas"],
        where=where
    )

        return results