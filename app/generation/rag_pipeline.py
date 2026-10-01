from app.retrieval.retriever import Retriever
from app.generation.llm import LLM


class RAGPipeline:

    def __init__(self):
        self.retriever = Retriever()
        self.llm = LLM()

    def ask(self, question, top_k=8, history=None , document_id=None) :
        if history is None:
            history= []

        results = self.retriever.retrieve(
            question,
            top_k=top_k ,
            document_id=document_id
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        context_parts = []

        for document, metadata in zip(
            documents,
            metadatas
        ):

            source = metadata["source"]
            page = metadata["page"]

            context_parts.append(
                f"[Source: {source}, Page: {page}]\n"
                f"{document}"
            )

        context = "\n\n".join(context_parts)

        conversation = ""

        for message in history:
            conversation += (
        f"{message['role'].capitalize()}: "
        f"{message['content']}\n"
        )


        prompt = f"""
You are a helpful AI assistant answering questions
about uploaded documents.

Use ONLY the information provided in the context.

You may use the conversation history to understand
references and follow-up questions.

Do not treat conversation history as factual document
evidence. Use the retrieved document context as the
source of truth.

If the answer cannot be found in the context, say:
"I couldn't find this information in the uploaded documents."

Answer the question clearly and concisely.

Do NOT create or invent sources.

Conversation History:
{conversation}

Context:
{context}

Question:
{question}

Answer:
"""

        answer = self.llm.generate(prompt)

        sources = []

        for metadata in metadatas:

            source = metadata["source"]
            page = metadata["page"]

            source_name = source.replace(
                "data/documents/",
                ""
            )

            source_item = {
                "source": source_name,
                "page": page
            }

            if source_item not in sources:
                sources.append(source_item)

        return {
            "answer": answer,
            "sources": sources
        }