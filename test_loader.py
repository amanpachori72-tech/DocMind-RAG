from app.ingestion.pdf_loader import load_pdf
from app.ingestion.text_splitter import split_documents


pdf_path = "data/documents/AResume.pdf"

documents = load_pdf(pdf_path)

print(f"Number of pages loaded: {len(documents)}")

chunks = split_documents(documents)

print(f"Number of chunks created: {len(chunks)}")

for i, chunk in enumerate(chunks[:10], start=1):
    print(f"\n--- Chunk {i} ---")
    print(f"Page: {chunk['page']}")
    print(f"Source: {chunk['source']}")
    print(chunk["text"])