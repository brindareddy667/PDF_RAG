import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:1b"


def generate_answer(question, context):
    """
    Generate grounded answer from retrieved context.
    """

    prompt = f"""
You are a PDF Question Answering Assistant.

Rules:
1. Answer ONLY using the provided context.
2. If the answer is not present in the context, say:
   "I couldn't find sufficient information in the uploaded document."
3. Do not make up information.
4. Give detailed answers when information exists.
5. Use complete sentences and proper formatting.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        data = response.json()

        if "response" in data:
            return data["response"].strip()

        return "Unable to generate answer."

    except Exception as e:
        return f"Error generating answer: {str(e)}"