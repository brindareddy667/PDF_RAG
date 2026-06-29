import fitz


def extract_pdf_text(pdf_path):
    """
    Extract text page-wise from PDF
    """

    doc = fitz.open(pdf_path)

    pages = []
    full_text = ""

    for i, page in enumerate(doc):

        text = page.get_text()

        pages.append(
            {
                "page": i + 1,
                "text": text
            }
        )

        full_text += text + "\n"

    doc.close()

    return full_text, pages