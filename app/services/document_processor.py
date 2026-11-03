from pathlib import Path

from app.services.pdf_processor import (
    extract_text_from_pdf,
    convert_pdf_to_images
)

from app.services.image_processor import (
    preprocess_invoice_image
)


def process_document(file_path: str):

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    extension = file_path.suffix.lower()

    if extension == ".pdf":

        pages = extract_text_from_pdf(str(file_path))

        has_text = any(
            page["text"].strip()
            for page in pages
        )

        if has_text:
            return {
                "document_type": "digital_pdf",
                "pages": pages
            }

        images = convert_pdf_to_images(
            str(file_path),
            "sample_data/processed"
        )

        return {
            "document_type": "scanned_pdf",
            "images": images
        }

    elif extension in [".jpg", ".jpeg", ".png"]:

        output_dir = Path("sample_data/processed")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = (
            output_dir / f"{file_path.stem}_processed.png"
        )

        preprocess_invoice_image(
            str(file_path),
            str(output_path)
        )

        return {
            "document_type": "image",
            "processed_image": str(output_path)
        }

    else:
        raise ValueError(
            f"Unsupported document format: {extension}"
        )