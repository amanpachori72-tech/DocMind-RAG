import chromadb


client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = client.get_collection(
    name="documents"
)

results = collection.get(
    include=["documents", "metadatas"]
)

print(f"Total chunks in database: {len(results['documents'])}")

for i, (document, metadata) in enumerate(
    zip(results["documents"], results["metadatas"]),
    start=1
):

    print("\n" + "=" * 60)
    print(f"CHUNK {i}")
    print(f"Page: {metadata['page']}")
    print(f"Source: {metadata['source']}")
    print("=" * 60)

    print(document)