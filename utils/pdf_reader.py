from PyPDF2 import PdfReader


def extract_pdf_text(pdf_path):
    """
    Extract text page-wise from PDF
    """

    reader = PdfReader(pdf_path)

    pages = []

    full_text = ""

    for i, page in enumerate(reader.pages):

        text = page.extract_text()

        if text is None:
            text = ""

        pages.append(
            {
                "page": i + 1,
                "text": text
            }
        )

        full_text += text + "\n"

    return full_text, pages