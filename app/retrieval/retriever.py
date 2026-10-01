from app.retrieval.embedding_model import EmbeddingModel
from app.retrieval.vector_store import VectorStore
from app.retrieval.reranker import Reranker


class Retriever:

    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore()
        self.reranker = Reranker()

    def retrieve(self, query, top_k=3, document_id=None):

        # -----------------------------
        # 1. Semantic retrieval
        # -----------------------------

        query_embedding = self.embedding_model.embed_text(query)

        semantic_results = self.vector_store.search(
            query_embedding,
            top_k=top_k,
            document_id=document_id
        )

        # -----------------------------
        # 2. Keyword retrieval
        # -----------------------------

        all_documents = self.vector_store.get_all_documents(
            document_id=document_id
        )

        query_words = query.lower().split()

        keyword_matches = []

        for document, metadata in zip(
            all_documents["documents"],
            all_documents["metadatas"]
        ):

            document_lower = document.lower()

            score = sum(
                1 for word in query_words
                if word in document_lower
            )

            if score > 0:
                keyword_matches.append({
                    "document": document,
                    "metadata": metadata,
                    "score": score
                })

        keyword_matches.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        # -----------------------------
        # 3. Combine results
        # -----------------------------

        combined_documents = []
        combined_metadatas = []

        for match in keyword_matches:

            if match["document"] not in combined_documents:

                combined_documents.append(
                    match["document"]
                )

                combined_metadatas.append(
                    match["metadata"]
                )

        for document, metadata in zip(
            semantic_results["documents"][0],
            semantic_results["metadatas"][0]
        ):

            if document not in combined_documents:

                combined_documents.append(document)
                combined_metadatas.append(metadata)

        # -----------------------------
        # 4. Rerank results
        # -----------------------------

        reranked = self.reranker.rerank(
            query,
            combined_documents,
            top_k=top_k
        )

        reranked_documents = [
            item["document"]
            for item in reranked
        ]

        reranked_metadatas = []

        for document in reranked_documents:

            index = combined_documents.index(document)

            reranked_metadatas.append(
                combined_metadatas[index]
            )

        # -----------------------------
        # 5. Return final results
        # -----------------------------

        return {
            "documents": [reranked_documents],
            "metadatas": [reranked_metadatas]
        }