"""PDF text extraction service."""

import logging
from typing import Optional
from PyPDF2 import PdfReader
from io import BytesIO

logger = logging.getLogger(__name__)


class PDFExtractionError(Exception):
    """Custom exception for PDF extraction errors."""

    pass


class PDFService:
    """Service for extracting text from PDF documents."""

    @staticmethod
    def extract_text(file_content: bytes, filename: str) -> str:
        """
        Extract text content from a PDF file.

        Args:
            file_content: Binary content of the PDF file
            filename: Name of the file (for logging)

        Returns:
            Extracted text content

        Raises:
            PDFExtractionError: If text extraction fails
        """
        try:
            pdf_file = BytesIO(file_content)
            reader = PdfReader(pdf_file)

            if len(reader.pages) == 0:
                raise PDFExtractionError(f"PDF file '{filename}' contains no pages")

            text_content = []
            for page_num, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
                    else:
                        logger.warning(
                            f"No text found on page {page_num + 1} of '{filename}'"
                        )
                except Exception as e:
                    logger.error(
                        f"Error extracting text from page {page_num + 1} "
                        f"of '{filename}': {str(e)}"
                    )
                    continue

            if not text_content:
                raise PDFExtractionError(
                    f"No text could be extracted from '{filename}'. "
                    "The PDF may be scanned or image-based."
                )

            full_text = "\n".join(text_content)
            logger.info(
                f"Successfully extracted {len(full_text)} characters "
                f"from {len(reader.pages)} pages in '{filename}'"
            )

            return full_text

        except PDFExtractionError:
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error extracting text from '{filename}': {str(e)}"
            )
            raise PDFExtractionError(f"Failed to extract text from PDF: {str(e)}")

    @staticmethod
    def validate_pdf(file_content: bytes) -> bool:
        """
        Validate if the file is a valid PDF.

        Args:
            file_content: Binary content of the file

        Returns:
            True if valid PDF, False otherwise
        """
        try:
            pdf_file = BytesIO(file_content)
            reader = PdfReader(pdf_file)
            # Try to access pages to ensure it's readable
            _ = len(reader.pages)
            return True
        except Exception as e:
            logger.warning(f"PDF validation failed: {str(e)}")
            return False
