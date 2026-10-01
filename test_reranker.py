from app.retrieval.retriever import Retriever
from app.retrieval.reranker import Reranker


retriever = Retriever()
reranker = Reranker()


query = "Is C++ present in this resume?"


# Get candidate documents
results = retriever.retrieve(
    query,
    top_k=8
)

documents = results["documents"][0]


# Rerank candidates
ranked_results = reranker.rerank(
    query,
    documents,
    top_k=5
)


for i, result in enumerate(
    ranked_results,
    start=1
):

    print("\n" + "=" * 60)
    print(f"RANK {i}")
    print(f"Score: {result['score']:.4f}")
    print("=" * 60)

    print(result["document"])