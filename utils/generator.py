import os

from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(question, context):

    prompt = f"""
You are a PDF Question Answering Assistant.

Rules:

1. Answer ONLY using the provided context.
2. If the answer is not present, reply:

"I couldn't find sufficient information in the uploaded document."

3. Never hallucinate.
4. Be detailed.
5. Use markdown formatting.

CONTEXT:

{context}

QUESTION:

{question}

ANSWER:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text