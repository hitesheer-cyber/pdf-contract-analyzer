"""NLP service for entity extraction using Hugging Face Transformers."""

import logging
from typing import List, Dict, Optional
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import torch

logger = logging.getLogger(__name__)


class EntityExtractionError(Exception):
    """Custom exception for entity extraction errors."""

    pass


class NLPService:
    """Service for extracting named entities from text using NLP."""

    def __init__(self, model_name: str = "dslim/bert-base-NER"):
        """
        Initialize the NLP service with a specified model.

        Args:
            model_name: Name of the Hugging Face model to use
        """
        self.model_name = model_name
        self._pipeline: Optional[any] = None
        self._initialized = False

    def _initialize_model(self) -> None:
        """Load the NLP model and tokenizer (lazy loading)."""
        if self._initialized:
            return

        try:
            logger.info(f"Loading NLP model: {self.model_name}")

            # Load tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model = AutoModelForTokenClassification.from_pretrained(self.model_name)

            # Create NER pipeline
            self._pipeline = pipeline(
                "ner",
                model=model,
                tokenizer=tokenizer,
                aggregation_strategy="simple",
                device=0 if torch.cuda.is_available() else -1,
            )

            self._initialized = True
            logger.info(
                f"NLP model loaded successfully. "
                f"Using device: {'CUDA' if torch.cuda.is_available() else 'CPU'}"
            )

        except Exception as e:
            logger.error(f"Failed to load NLP model: {str(e)}")
            raise EntityExtractionError(f"Failed to initialize NLP model: {str(e)}")

    def extract_entities(
        self, text: str, max_length: int = 5000
    ) -> List[Dict[str, any]]:
        """
        Extract named entities from text.

        Args:
            text: Input text to extract entities from
            max_length: Maximum text length to process (longer texts are chunked)

        Returns:
            List of dictionaries containing entity information:
            - text: The entity text
            - entity_type: Type of entity (PER, ORG, LOC, MISC)
            - position: Character position in original text
            - confidence: Model confidence score

        Raises:
            EntityExtractionError: If extraction fails
        """
        try:
            self._initialize_model()

            if not text or not text.strip():
                logger.warning("Empty text provided for entity extraction")
                return []

            # Process text in chunks if it's too long
            entities = []
            text_chunks = self._chunk_text(text, max_length)
            offset = 0

            for chunk in text_chunks:
                try:
                    # Run NER pipeline
                    raw_entities = self._pipeline(chunk)

                    # Process and standardize entities
                    for entity in raw_entities:
                        processed_entity = self._process_entity(entity, offset)
                        if processed_entity:
                            entities.append(processed_entity)

                    offset += len(chunk)

                except Exception as e:
                    logger.error(
                        f"Error processing text chunk at offset {offset}: {str(e)}"
                    )
                    continue

            # Remove duplicate entities
            entities = self._deduplicate_entities(entities)

            logger.info(f"Extracted {len(entities)} unique entities from text")
            return entities

        except EntityExtractionError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during entity extraction: {str(e)}")
            raise EntityExtractionError(f"Failed to extract entities: {str(e)}")

    def _chunk_text(self, text: str, max_length: int) -> List[str]:
        """
        Split text into chunks for processing.

        Args:
            text: Text to chunk
            max_length: Maximum chunk length

        Returns:
            List of text chunks
        """
        if len(text) <= max_length:
            return [text]

        chunks = []
        sentences = text.split(". ")
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_length:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def _process_entity(self, entity: Dict, offset: int) -> Optional[Dict[str, any]]:
        """
        Process and standardize a single entity.

        Args:
            entity: Raw entity from NER pipeline
            offset: Character offset in the original text

        Returns:
            Processed entity dictionary or None if invalid
        """
        try:
            # Map entity types to standard format
            entity_type_map = {
                "PER": "PERSON",
                "ORG": "ORG",
                "LOC": "LOC",
                "MISC": "MISC",
            }

            raw_type = entity.get("entity_group", "MISC")
            entity_type = entity_type_map.get(raw_type, "MISC")

            return {
                "text": entity["word"].strip(),
                "entity_type": entity_type,
                "position": entity["start"] + offset,
                "confidence": float(round(entity["score"], 4)),
            }
        except Exception as e:
            logger.warning(f"Error processing entity: {str(e)}")
            return None

    def _deduplicate_entities(
        self, entities: List[Dict[str, any]]
    ) -> List[Dict[str, any]]:
        """
        Remove duplicate entities based on text and position.

        Args:
            entities: List of entities

        Returns:
            Deduplicated list of entities
        """
        seen = set()
        unique_entities = []

        for entity in entities:
            key = (entity["text"], entity["position"])
            if key not in seen:
                seen.add(key)
                unique_entities.append(entity)

        return unique_entities


# Global NLP service instance (singleton pattern)
_nlp_service: Optional[NLPService] = None


def get_nlp_service(model_name: str = "dslim/bert-base-NER") -> NLPService:
    """
    Get or create the NLP service instance (singleton).

    Args:
        model_name: Name of the Hugging Face model to use

    Returns:
        NLPService instance
    """
    global _nlp_service
    if _nlp_service is None:
        _nlp_service = NLPService(model_name)
    return _nlp_service
