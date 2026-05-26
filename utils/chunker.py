def create_chunks(
    pages,
    chunk_size=400,
    overlap=100
):
    """
    Create overlapping chunks
    while preserving page number.
    """

    chunks = []

    for page_data in pages:

        page_number = page_data["page"]

        text = page_data["text"]

        words = text.split()

        start = 0

        while start < len(words):

            end = start + chunk_size

            chunk_words = words[start:end]

            chunk_text = " ".join(chunk_words)

            chunks.append(
                {
                    "page": page_number,
                    "text": chunk_text
                }
            )

            start += chunk_size - overlap

    return chunks