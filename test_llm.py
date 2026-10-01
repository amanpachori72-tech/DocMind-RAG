from app.generation.llm import LLM


llm = LLM()

answer = llm.generate(
    "Explain what machine learning is in one sentence."
)

print("\nLLM Response:")
print(answer)