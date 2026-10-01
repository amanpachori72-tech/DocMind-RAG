from app.ingestion.document_processor import DocumentProcessor


file_path = "data/documents/AResume.pdf"

processor = DocumentProcessor()

result = processor.process(file_path)

print("\nDOCUMENT PROCESSED SUCCESSFULLY")
print("=" * 60)

print(f"Document ID: {result['document_id']}")
print(f"Pages: {result['pages']}")
print(f"Chunks: {result['chunks']}")