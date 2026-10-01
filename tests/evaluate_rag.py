import re
def normalize_text(text):
    text = text.lower()

    # Convert punctuation/Markdown/special Unicode characters
    # into spaces.
    text = re.sub(r"[^a-z0-9]+", " ", text)

    # Normalize multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()

import sys

sys.stdout.reconfigure(encoding="utf-8")

from app.generation.rag_pipeline import RAGPipeline
from tests.evaluation_questions import evaluation_questions


rag = RAGPipeline()

results = []
correct = 0


for i, item in enumerate(evaluation_questions, start=1):

    question = item["question"]
    expected = item["expected"]

    print("\n" + "=" * 70)
    print(f"QUESTION {i}")
    print("=" * 70)
    print(question)

    result = rag.ask(
        question,
        top_k=8
    )

    answer = result["answer"]

    print("\nEXPECTED FACTS:")
    for fact in expected:
        print(f"- {fact}")

    print("\nACTUAL:")
    print(answer)

    # Check whether every required fact appears
    # somewhere in the generated answer.

    answer_normalized = normalize_text(answer)

    required_facts = [
    normalize_text(fact)
    for fact in expected
    ]

    missing_facts = [
        fact
        for fact in required_facts
        if fact not in answer_normalized
    ]

    if not missing_facts:

        correct += 1
        print("\nRESULT: PASS")

    else:
        print("\nRESULT: FAIL")
        print("Missing facts:")

    for fact in missing_facts:
        print(f"- {fact}")

    print("\nThis question needs investigation.")

    results.append({
    "question": question,
    "expected": expected,
    "answer": answer,
    "missing_facts": missing_facts
})


print("\n" + "=" * 70)
print("EVALUATION COMPLETE")
print("=" * 70)

total = len(results)

accuracy = (
    correct / total * 100
    if total > 0
    else 0
)

print("\nFAILED QUESTIONS")
print("-" * 70)

for result in results:

    if result.get("missing_facts"):

        print(f"\nQuestion: {result['question']}")
        print("Missing facts:")

        for fact in result["missing_facts"]:
            print(f"- {fact}")

print(f"Questions evaluated: {total}")
print(f"Correct answers: {correct}")
print(f"Incorrect answers: {total - correct}")
print(f"Evaluation accuracy: {accuracy:.2f}%")