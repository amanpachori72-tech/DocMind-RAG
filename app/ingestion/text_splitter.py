def split_documents(documents, chunk_size=500, chunk_overlap=100):

    chunks = []

    for document in documents:

        lines = [
            line.strip()
            for line in document["text"].splitlines()
            if line.strip()
        ]

        current_chunk = []

        for line in lines:

            current_text = "\n".join(current_chunk)

            # Add line if it fits
            if len(current_text) + len(line) + 1 <= chunk_size:
                current_chunk.append(line)

            else:

                if current_chunk:

                    chunks.append({
                        "text": "\n".join(current_chunk),
                        "page": document["page"],
                        "source": document["source"]
                    })

                # Start new chunk
                current_chunk = [line]

        # Add remaining lines
        if current_chunk:

            chunks.append({
                "text": "\n".join(current_chunk),
                "page": document["page"],
                "source": document["source"]
            })

    return chunks