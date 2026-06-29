import os
import numpy as np

from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a)
        * np.linalg.norm(b)
    )


def retrieve_context(
    question,
    chunks,
    embeddings
):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    )

    query_embedding = response.embeddings[0].values

    similarities = [
        cosine_similarity(
            query_embedding,
            emb
        )
        for emb in embeddings
    ]

    best_index = int(np.argmax(similarities))

    best_score = similarities[best_index]

    if best_score < 0.25:

        return {
            "page": None,
            "text": None
        }

    return {
        "page": chunks[best_index]["page"],
        "text": chunks[best_index]["text"]
    }