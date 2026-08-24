"""
extractor.py — Text Extraction Module
Handles PDF text extraction (PyMuPDF) and image OCR (pytesseract).
"""

try:
    import pymupdf as fitz  # PyMuPDF >= 1.25
except ImportError:
    import fitz  # PyMuPDF < 1.25 (legacy import)
import pytesseract
from PIL import Image
import io
import re


def extract_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from a PDF file while preserving structure.
    Returns the extracted text as a single string.
    """
    text_parts = []

    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page_num, page in enumerate(doc, 1):
            page_text = page.get_text("text")
            if page_text.strip():
                text_parts.append(f"[Page {page_num}]\n{page_text}")

    full_text = "\n\n".join(text_parts)
    return _clean_text(full_text)


def extract_from_image(file_bytes: bytes) -> str:
    """
    Extract text from an image file using Tesseract OCR.
    Returns the extracted text as a single string.
    """
    image = Image.open(io.BytesIO(file_bytes))

    # Convert to RGB if needed (handles RGBA/P mode images)
    if image.mode not in ("RGB", "L"):
        image = image.convert("RGB")

    # Use Tesseract with best config for document OCR
    custom_config = r"--oem 3 --psm 6"
    text = pytesseract.image_to_string(image, config=custom_config)

    return _clean_text(text)


def _clean_text(text: str) -> str:
    """
    Clean up extracted text: normalize whitespace while preserving paragraphs.
    """
    # Normalize multiple blank lines to at most two
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip leading/trailing whitespace per line
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)
    # Remove leading/trailing whitespace overall
    return text.strip()
