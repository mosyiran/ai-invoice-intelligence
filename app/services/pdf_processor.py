import pymupdf
from pathlib import Path


def extract_text_from_pdf(pdf_path: str):
    """
    Extract text from every page of a PDF file.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    extracted_pages = []

    with pymupdf.open(pdf_path) as document:

        for page_number, page in enumerate(document):

            text = page.get_text("text")

            extracted_pages.append({
                "page": page_number + 1,
                "text": text
            })

    return extracted_pages


def convert_pdf_to_images(
    pdf_path: str,
    output_dir: str,
    dpi: int = 300
):
    """
    Convert every PDF page into a PNG image.
    """

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    image_paths = []

    with pymupdf.open(pdf_path) as document:

        zoom = dpi / 72
        matrix = pymupdf.Matrix(zoom, zoom)

        for page_number, page in enumerate(document):

            pixmap = page.get_pixmap(
                matrix=matrix,
                alpha=False
            )

            image_path = (
                output_dir / f"page_{page_number + 1}.png"
            )

            pixmap.save(image_path)

            image_paths.append(str(image_path))

    return image_paths