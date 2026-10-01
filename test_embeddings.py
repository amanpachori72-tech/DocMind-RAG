from app.retrieval.embedding_model import EmbeddingModel


embedding_model = EmbeddingModel()

text = "Machine learning is a subset of artificial intelligence."

embedding = embedding_model.embed_text(text)

print("Embedding generated successfully!")
print("Vector dimensions:", len(embedding))
print("First 10 values:", embedding[:10])