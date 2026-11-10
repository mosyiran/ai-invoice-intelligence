
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.schemas.invoice import InvoiceData
from app.services.prompts import INVOICE_EXTRACTION_PROMPT


# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")


# Initialize Gemini client
client = genai.Client(api_key=api_key)


def extract_invoice_data(ocr_text: str) -> InvoiceData:

    if not ocr_text or not ocr_text.strip():
        raise ValueError("OCR text is empty")

    prompt = INVOICE_EXTRACTION_PROMPT.format(
        ocr_text=ocr_text
    )

    # Generate structured JSON using Pydantic schema
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=InvoiceData,
            temperature=0
        )
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response")

    # Use parsed Pydantic object when available
    if response.parsed is not None:
        return InvoiceData.model_validate(response.parsed)

    # Fallback: validate JSON response
    return InvoiceData.model_validate_json(response.text)
