import os
import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

from app.services.prompts import INVOICE_EXTRACTION_PROMPT


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

model = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")

client = genai.Client(api_key=api_key)


def extract_invoice_data(ocr_text: str):

    if not ocr_text or not ocr_text.strip():
        raise ValueError("OCR text is empty")

    prompt = INVOICE_EXTRACTION_PROMPT.format(
        ocr_text=ocr_text
    )

    max_retries = 4

    for attempt in range(max_retries):

        try:
            print(f"Sending request to Gemini: {model}")

            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "temperature": 0
                }
            )

            if not response.text:
                raise ValueError("Gemini returned an empty response")

            return json.loads(response.text)

        except ServerError as error:

            if error.code != 503:
                raise

            if attempt == max_retries - 1:
                raise

            wait_time = 2 ** (attempt + 1)

            print(
                f"Gemini is temporarily unavailable. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)