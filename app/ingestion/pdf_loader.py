from pypdf import PdfReader


def load_pdf(file_path):
    reader = PdfReader(file_path)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            documents.append({
                "text": text,
                "page": page_number,
                "source": file_path
            })

    return documents