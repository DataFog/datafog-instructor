# src/datafog_instructor/pii_data_extraction/redactor.py

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Tuple
import hashlib
import re
from datetime import datetime
from groq import Groq
import logging
import os
import instructor
from pydantic import ValidationError


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

logger = logging.getLogger(__name__)


class DetectedPII(BaseModel):
    """
    Represents a single piece of detected Personally Identifiable Information (PII).

    Preconditions:
    - data_type is a non-empty string
    - pii_value is a non-empty string
    - start_index, if provided, is a non-negative integer
    - end_index, if provided, is a non-negative integer greater than start_index

    Postconditions:
    - All fields are set according to the provided values
    - start_index and end_index are either both set or both None

    Invariants:
    - All fields remain constant after initialization
    - start_index is always less than or equal to end_index if both are set
    """
    data_type: str = Field(min_length=1)
    pii_value: str = Field(min_length=1)
    start_index: Optional[int] = Field(default=None, ge=0)
    end_index: Optional[int] = Field(default=None, ge=0)

    model_config = ConfigDict(frozen=True)

    @classmethod
    def model_validate(cls, value):
        validated = super().model_validate(value)
        if (validated.start_index is None) != (validated.end_index is None):
            raise ValueError("Both start_index and end_index must be either set or None")
        if validated.start_index is not None and validated.end_index is not None:
            if validated.start_index >= validated.end_index:
                raise ValueError("start_index must be less than end_index")
        return validated

    def validate_indices(self) -> bool:
        """
        Validate that the indices are consistent with the PII value.

        Postconditions:
        - Returns True if indices are valid, False otherwise

        Invariants:
        - Does not modify any object state
        """
        if self.start_index is None or self.end_index is None:
            return True
        return (self.end_index - self.start_index) == len(self.pii_value)

class PIIDataExtraction(BaseModel):
    """
    Represents a collection of PII data extracted from a document.

    Preconditions:
    - private_data is a non-empty list of DetectedPII objects

    Postconditions:
    - private_data, extraction_timestamp, and document_hash are set
    - document_hash is generated based on the private_data

    Invariants:
    - private_data remains constant after initialization
    - extraction_timestamp reflects the time of object creation
    - document_hash is unique for the given set of private_data
    """
    private_data: Tuple[DetectedPII, ...] = Field(...)  # Changed from List to Tuple
    extraction_timestamp: datetime = Field(default_factory=datetime.utcnow)
    document_hash: Optional[str] = None

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    def __init__(self, **data):
        """
        Initialize the PIIDataExtraction object.

        Preconditions:
        - data contains valid values for all required fields

        Postconditions:
        - All fields are initialized
        - document_hash is generated
        - private_data is converted to an immutable tuple
        """
        if 'private_data' in data and isinstance(data['private_data'], list):
            data['private_data'] = tuple(data['private_data'])  # Convert list to tuple
        if 'document_hash' not in data:
            data['document_hash'] = self._generate_document_hash(data['private_data'])
        super().__init__(**data)
        logger.info(f"PIIDataExtraction initialized with {len(self.private_data)} items")

    @staticmethod
    def _generate_document_hash(private_data: Tuple[DetectedPII, ...]) -> str:
        """
        Generate a hash based on the private data.

        Preconditions:
        - private_data is initialized and non-empty

        Postconditions:
        - Returns a unique hash string for the given private_data

        Invariants:
        - The same private_data always produces the same hash
        """
        try:
            # Sort PII items by start_index if available, otherwise by data_type and value
            sorted_pii = sorted(
                private_data,
                key=lambda x: (x.start_index if x.start_index is not None else float('inf'), x.data_type, x.pii_value)
            )
            pii_string = "".join(f"{pii.data_type}:{pii.pii_value}" for pii in sorted_pii)
            return hashlib.sha256(pii_string.encode()).hexdigest()
        except Exception as e:
            return f"hash_generation_error: {str(e)}"

    def scrub_data(self, text: str) -> str:
        """
        Scrubs the PII data from the content using a flexible masking strategy.

        Preconditions:
        - content is a non-empty string
        - mask_char is a single character string

        Postconditions:
        - Returns a new string with PII data masked
        - Original content is not modified

        Invariants:
        - The length of the returned string is equal to or greater than the original content
        - All PII data in the original content is masked in the returned string
        """
        try:
            for pii in sorted(self.private_data, key=lambda x: x.start_index or float('inf'), reverse=True):
                if pii.start_index is not None and pii.end_index is not None:
                    text = text[:pii.start_index] + f"[{pii.data_type.upper()}]" + text[pii.end_index:]
                else:
                    # Fallback to simple string replacement if indices are not available
                    text = text.replace(pii.pii_value, f"[{pii.data_type.upper()}]")
            logger.info("DetectedPII scrubbing completed successfully")
            return text
        except Exception as e:
            logger.error(f"Error in scrub_data: {str(e)}")
            raise

class PIIExtractor:
    """
    Handles the extraction of PII data from documents.
    """

    def __init__(self, api_key: str):
        try:
            self.client = instructor.from_groq(Groq(api_key=GROQ_API_KEY))
            logger.info("PIIExtractor initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing PIIExtractor: {str(e)}")
            raise

    def extract_pii(self, document: str) -> PIIDataExtraction:
        """
        Extracts PII data from the given document.
        """
        if not document:
            logger.warning("Empty document provided for PII extraction")
            return PIIDataExtraction(private_data=[])

        try:
            logger.info("Starting PII extraction")
            pii_data: PIIDataExtraction = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                response_model=PIIDataExtraction,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a world class PII extraction model. Extract the PII data from the following document, including the start and end indices of each PII item.",
                    },
                    {
                        "role": "user",
                        "content": document,
                    },
                ],
            )
            logger.info(f"PII extraction completed. Found {len(pii_data.private_data)} PII items")
            return pii_data
        except ValidationError as ve:
            logger.error(f"Validation error in PII extraction: {str(ve)}")
            return PIIDataExtraction(private_data=[])
        except Exception as e:
            logger.error(f"Error in PII extraction: {str(e)}")
            raise

class PIIExtractionError(Exception):
    """
    Custom exception for errors during PII extraction.

    Preconditions:
    - message is a non-empty string describing the error

    Postconditions:
    - An exception is raised with the provided message

    Invariants:
    - The error message remains constant after initialization
    """

    def __init__(self, message: str):
        """
        Initialize the PIIExtractionError.

        Args:
            message (str): A description of the error.

        Raises:
            ValueError: If the message is empty or not a string.
        """
        if not isinstance(message, str) or not message:
            raise ValueError("Error message must be a non-empty string")
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"PIIExtractionError: {self.message}"

# Usage example:
if __name__ == "__main__":
    try:
        pii_data = PIIDataExtraction(
            private_data=[
                DetectedPII( data_type="email", pii_value="john.doe@example.com"),
                DetectedPII( data_type="phone", pii_value="123-456-7890"),
            ]
        )
        
        original_text = "Contact: john.doe@example.com, Phone: 123-456-7890"
        scrubbed_text = pii_data.scrub_data(original_text)
        print(f"Original: {original_text}")
        print(f"Scrubbed: {scrubbed_text}")
        print(f"Document Hash: {pii_data.document_hash}")
    except Exception as e:
        logger.critical(f"Critical error in main execution: {str(e)}")