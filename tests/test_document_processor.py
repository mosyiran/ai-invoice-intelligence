from app.services.document_processor import (
    process_document
)


def test_process_pdf():

    result = process_document(
        "sample_data/invoices/invoice_01.pdf"
    )

    assert result["document_type"] in [
        "digital_pdf",
        "scanned_pdf"
    ]


def test_process_image():

    result = process_document(
        "sample_data/invoices/invoice_03.png"
    )

    assert result["document_type"] == "image"