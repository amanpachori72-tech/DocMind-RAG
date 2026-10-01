from app.retrieval.retriever import Retriever


retriever = Retriever()

query = "Is C++ present in this resume?"

results = retriever.retrieve(
    query,
    top_k=8,
    document_id="AResume.pdf"
)

documents = results["documents"][0]
metadatas = results["metadatas"][0]

print(f"\nRESULTS FOUND: {len(documents)}")

for i, (document, metadata) in enumerate(
    zip(documents, metadatas),
    start=1
):

    print("\n" + "=" * 60)
    print(f"RESULT {i}")
    print(f"Page: {metadata['page']}")
    print(f"Source: {metadata['source']}")
    print(f"Document ID: {metadata['document_id']}")
    print("=" * 60)

    print(document)