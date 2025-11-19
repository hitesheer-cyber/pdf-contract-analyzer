"""Tests for PDF service."""

import pytest
from app.services.pdf_service import PDFService, PDFExtractionError


def test_validate_pdf_invalid():
    """Test PDF validation with invalid content."""
    invalid_content = b"Not a PDF file"
    assert PDFService.validate_pdf(invalid_content) is False


def test_extract_text_invalid_pdf():
    """Test text extraction with invalid PDF."""
    invalid_content = b"Not a PDF file"

    with pytest.raises(PDFExtractionError):
        PDFService.extract_text(invalid_content, "test.pdf")
