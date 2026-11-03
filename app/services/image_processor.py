import cv2
from pathlib import Path


def preprocess_invoice_image(
    image_path: str,
    output_path: str
):

    image_path = Path(image_path)

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError("Unable to read image")

    # Convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Remove noise
    denoised = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    # Apply adaptive threshold
    processed = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    # Save processed image
    cv2.imwrite(
        str(output_path),
        processed
    )

    return str(output_path)