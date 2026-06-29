from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_from_directory
)

import os
import uuid

from utils.pdf_reader import extract_pdf_text
from utils.chunker import create_chunks
from utils.embeddings import generate_embeddings
from utils.retriever import retrieve_context
from utils.generator import generate_answer
import pkgutil
print(sorted([m.name for m in pkgutil.iter_modules()]))

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ===================================
# GLOBAL STATE
# ===================================

current_pdf = None

current_chunks = None

current_embeddings = None

pdf_stats = {}

recent_questions = []


# ===================================
# HOME
# ===================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ===================================
# UPLOAD PDF
# ===================================

@app.route("/upload", methods=["POST"])
def upload_pdf():

    global current_pdf
    global current_chunks
    global current_embeddings
    global pdf_stats

    if "pdf" not in request.files:

        return jsonify(
            {
                "success": False,
                "message": "No PDF selected"
            }
        )

    file = request.files["pdf"]

    if file.filename == "":

        return jsonify(
            {
                "success": False,
                "message": "Empty filename"
            }
        )

    # Remove old PDF

    if current_pdf:

        try:

            os.remove(
                os.path.join(
                    UPLOAD_FOLDER,
                    current_pdf
                )
            )

        except:
            pass

    filename = (
        str(uuid.uuid4())
        + ".pdf"
    )

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(filepath)

    # Extract PDF text

    full_text, pages = extract_pdf_text(
        filepath
    )

    chunks = create_chunks(
        pages
    )

    embeddings = generate_embeddings(
        chunks
    )

    current_pdf = filename

    current_chunks = chunks

    current_embeddings = embeddings

    pdf_stats = {
        "pages": len(pages),
        "chunks": len(chunks),
        "words": len(
            full_text.split()
        )
    }

    return jsonify(
        {
            "success": True,
            "pdf_name": file.filename,
            "stats": pdf_stats
        }
    )


# ===================================
# ASK QUESTION
# ===================================

@app.route("/ask", methods=["POST"])
def ask():

    global recent_questions

    if current_pdf is None:

        return jsonify(
            {
                "answer":
                "Please upload a PDF first.",
                "page": None
            }
        )

    data = request.get_json()

    question = data.get(
        "question",
        ""
    ).strip()

    if question == "":

        return jsonify(
            {
                "answer":
                "Please enter a question.",
                "page": None
            }
        )

    question_lower = question.lower().strip()

    # ===================================
    # SPECIAL DOCUMENT QUESTIONS
    # ===================================

    if question_lower in [
        "summarize this document",
        "summarise this document",
        "summary"
    ]:

        context = "\n\n".join(
            chunk["text"]
            for chunk in current_chunks[:15]
        )

        answer = generate_answer(
            "Provide a detailed summary of this document including major topics, important points and conclusions.",
            context
        )

        return jsonify(
            {
                "answer": answer,
                "page": 1
            }
        )

    if question_lower == "what is the main objective?":

        context = "\n\n".join(
            chunk["text"]
            for chunk in current_chunks[:15]
        )

        answer = generate_answer(
            "Identify and explain the primary objective of this document.",
            context
        )

        return jsonify(
            {
                "answer": answer,
                "page": 1
            }
        )

    if question_lower == "what are the key findings?":

        context = "\n\n".join(
            chunk["text"]
            for chunk in current_chunks[:15]
        )

        answer = generate_answer(
            "List the key findings and important insights from this document.",
            context
        )

        return jsonify(
            {
                "answer": answer,
                "page": 1
            }
        )

    if question_lower == "what recommendations are mentioned?":

        context = "\n\n".join(
            chunk["text"]
            for chunk in current_chunks[:15]
        )

        answer = generate_answer(
            "List all recommendations mentioned in the document.",
            context
        )

        return jsonify(
            {
                "answer": answer,
                "page": 1
            }
        )

    # ===================================
    # NORMAL RAG FLOW
    # ===================================

    result = retrieve_context(
        question,
        current_chunks,
        current_embeddings
    )

    page = result["page"]

    context = result["text"]

    if context is None:

        return jsonify(
            {
                "answer":
                "I couldn't find sufficient information in the uploaded document.",
                "page": None
            }
        )

    answer = generate_answer(
        question,
        context
    )

    recent_questions.insert(
        0,
        question
    )

    recent_questions = recent_questions[:10]

    return jsonify(
        {
            "answer": answer,
            "page": page
        }
    )


# ===================================
# REMOVE PDF
# ===================================

@app.route(
    "/remove_pdf",
    methods=["POST"]
)
def remove_pdf():

    global current_pdf
    global current_chunks
    global current_embeddings
    global pdf_stats

    if current_pdf:

        try:

            os.remove(
                os.path.join(
                    UPLOAD_FOLDER,
                    current_pdf
                )
            )

        except:
            pass

    current_pdf = None

    current_chunks = None

    current_embeddings = None

    pdf_stats = {}

    return jsonify(
        {
            "success": True
        }
    )


# ===================================
# OPEN PDF
# ===================================

@app.route("/pdf")
def open_pdf():

    if current_pdf is None:

        return (
            "No PDF uploaded",
            404
        )

    return send_from_directory(
        UPLOAD_FOLDER,
        current_pdf
    )


# ===================================
# RECENT QUESTIONS
# ===================================

@app.route("/recent")
def recent():

    return jsonify(
        recent_questions
    )


# ===================================
# RUN
# ===================================

if __name__ == "__main__":
    import os

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )