from app.generation.rag_pipeline import RAGPipeline


rag = RAGPipeline()

question = "What did I do in the AI-Based Surveillance System?"
answer = rag.ask(question, top_k=8)

print("\n==============================")
print("RAG ANSWER")
print("==============================")
print(answer)