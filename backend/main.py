"""
main.py — FastAPI Application Entry Point
Document Summary Assistant Backend
"""

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

from extractor import extract_from_pdf, extract_from_image
from summarizer import generate_summary

import os
from dotenv import load_dotenv

# Load env variables from .env if present
load_dotenv()

# ─── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Document Summary Assistant API",
    description="Extract text from PDFs/images and generate AI-powered summaries.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Lock down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Supported file types ─────────────────────────────────────────────────────
PDF_TYPES = {"application/pdf"}
IMAGE_TYPES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/webp",
    "image/tiff",
    "image/bmp",
}
MAX_FILE_SIZE_MB = 20


# ─── Response Models ──────────────────────────────────────────────────────────
class ProcessResponse(BaseModel):
    summary: str
    key_points: list[str]
    improvement_suggestions: list[str]
    word_count: int
    char_count: int
    file_type: str


# ─── Endpoints ────────────────────────────────────────────────────────────────
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Document Summary Assistant API is running",
        "has_api_key": bool(os.environ.get("GEMINI_API_KEY")),
    }


@app.post("/process", response_model=ProcessResponse)
async def process_document(
    file: UploadFile = File(...),
    length: str = Form(default="medium"),
    api_key: str = Form(default=None),
):
    """
    Process a document (PDF or image) and generate an AI-powered summary.

    - **file**: PDF or image file (max 20MB)
    - **length**: Summary length — 'short', 'medium', or 'long'
    - **api_key**: Google Gemini API key (optional if backend .env has it)
    """
    # ── Validate length ──
    if length not in ("short", "medium", "long"):
        raise HTTPException(
            status_code=400,
            detail="Invalid length. Must be 'short', 'medium', or 'long'.",
        )

    # ── Resolve API key (Request Form vs Env) ──
    input_key = api_key.strip() if api_key else ""
    resolved_api_key = input_key or os.environ.get("GEMINI_API_KEY")
    if not resolved_api_key or len(resolved_api_key.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="A valid Gemini API key is required. Please set GEMINI_API_KEY in the backend environment/UI.",
        )

    # ── Read file ──
    file_bytes = await file.read()

    # ── Validate file size ──
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({size_mb:.1f}MB). Maximum allowed is {MAX_FILE_SIZE_MB}MB.",
        )

    content_type = file.content_type or ""
    logger.info(f"Processing file: {file.filename} ({content_type}, {size_mb:.2f}MB)")

    # ── Text Extraction ──
    try:
        if content_type in PDF_TYPES or file.filename.lower().endswith(".pdf"):
            extracted_text = extract_from_pdf(file_bytes)
            file_type = "pdf"
        elif content_type in IMAGE_TYPES or any(
            file.filename.lower().endswith(ext)
            for ext in (".png", ".jpg", ".jpeg", ".webp", ".tiff", ".bmp")
        ):
            extracted_text = extract_from_image(file_bytes)
            file_type = "image"
        else:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file type: {content_type}. Please upload a PDF or image file.",
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Text extraction failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract text from the document: {str(e)}",
        )

    # ── Validate extracted text ──
    if not extracted_text or len(extracted_text.strip()) < 50:
        raise HTTPException(
            status_code=422,
            detail="Could not extract meaningful text from the document. "
            "The file may be empty, corrupted, or contain only non-text content.",
        )

    logger.info(f"Extracted {len(extracted_text)} characters of text.")

    # ── AI Summary Generation ──
    try:
        result = generate_summary(extracted_text, length, resolved_api_key.strip())
    except Exception as e:
        logger.error(f"Summary generation failed: {e}")
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg or "api key" in error_msg.lower():
            raise HTTPException(
                status_code=401,
                detail="Invalid Gemini API key. Please check your key and try again.",
            )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate summary: {error_msg}",
        )

    word_count = len(extracted_text.split())
    char_count = len(extracted_text)

    return ProcessResponse(
        summary=result["summary"],
        key_points=result["key_points"],
        improvement_suggestions=result["improvement_suggestions"],
        word_count=word_count,
        char_count=char_count,
        file_type=file_type,
    )
