import numpy as np

from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def retrieve_context(
    question,
    chunks,
    embeddings
):
    """
    Retrieve best matching chunk only.
    """

    query_embedding = model.encode(
        [question]
    )[0]

    similarities = np.dot(
        embeddings,
        query_embedding
    )

    best_index = int(
        np.argmax(similarities)
    )

    best_score = float(
        similarities[best_index]
    )

    if best_score < 0.25:

        return {
            "page": None,
            "text": None
        }

    return {
        "page": chunks[best_index]["page"],
        "text": chunks[best_index]["text"]
    }