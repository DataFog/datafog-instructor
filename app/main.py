# app/main.py
import logging
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, ValidationError, validator
from groq import Groq
import instructor
import os
from dotenv import load_dotenv
from .pii_redactor.redactor import PIIDataExtraction, DetectedPII, PIIExtractor, PIIExtractionError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

#load Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class LLMConfig(BaseModel):
    """
    Configuration for the Language Model.

    Preconditions:
    - api_key must be a non-empty string
    - model must be a valid model name supported by the API

    Postconditions:
    - api_key and model are set according to the provided values or defaults

    Invariants:
    - api_key remains constant after initialization
    - model remains constant after initialization
    """
    api_key: str = Field(..., min_length=1)
    model: str = Field(default="mixtral-8x7b-32768", min_length=1)

    model_config = ConfigDict(frozen=True)

    @validator('api_key', 'model')
    def check_non_empty(cls, v):
        if not v.strip():
            raise ValueError("Must not be empty")
        return v

class DataFogInstructor:
    """
    Main class for DataFog Instructor operations.

    Preconditions:
    - llm_config is either None or a valid LLMConfig instance

    Postconditions:
    - llm_config is set to the provided config or a default one
    - client is initialized with the Groq API
    - All component extractors and scanners are initialized

    Invariants:
    - llm_config, client, and component instances remain constant throughout the object's lifecycle
    """

    def __init__(self, llm_config: Optional[LLMConfig] = None):
        try:
            if llm_config is None:
                api_key = os.getenv("GROQ_API_KEY")
                if not api_key:
                    raise ValueError("GROQ_API_KEY environment variable is not set")
                self.llm_config = LLMConfig(api_key=api_key)
            else:
                self.llm_config = llm_config

            self.client = self._initialize_client()
            self.pii_extractor = PIIExtractor(self.llm_config.api_key)
            logger.info("DataFogInstructor initialized successfully")
        except ValueError as ve:
            logger.error(f"Configuration error: {str(ve)}")
            raise
        except TypeError as te:
            logger.error(f"Invalid argument type: {str(te)}")
            raise
        except AttributeError as ae:
            logger.error(f"Missing required attribute: {str(ae)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error initializing DataFogInstructor: {str(e)}")
            raise

    def _initialize_client(self):
        """
        Initialize the Groq client.

        Preconditions:
        - llm_config.api_key is a valid API key

        Postconditions:
        - Returns an initialized instructor client

        Exceptions:
        - Raises ValueError if API key is invalid
        - Raises ConnectionError if unable to connect to Groq API
        - Raises RuntimeError for other unexpected errors during initialization
        """
        try:
            if not self.llm_config.api_key or not isinstance(self.llm_config.api_key, str):
                raise ValueError("Invalid API key")
            
            groq_client = Groq(api_key=self.llm_config.api_key)
            instructor_client = instructor.from_groq(client=groq_client)
            
            # Test the connection
            instructor_client.chat.completions.create(response_model=PIIDataExtraction, model="mixtral-8x7b-32768", messages=[{"role": "user", "content": "Test"}])
            
            return instructor_client
        except ValueError as ve:
            logger.error(f"Invalid API key: {str(ve)}")
            raise
        except ConnectionError as ce:
            logger.error(f"Failed to connect to Groq API: {str(ce)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error initializing Groq client: {str(e)}")
            raise RuntimeError(f"Failed to initialize Groq client: {str(e)}")

    def extract_pii(self, document: str) -> PIIDataExtraction:
        """
        Extract PII from a document.

        Preconditions:
        - document is a non-empty string

        Postconditions:
        - Returns extracted PII information

        Exceptions:
        - ValueError: If the document is empty or not a string
        - PIIExtractionError: If there's an error during PII extraction
        - ValidationError: If the extracted data fails validation
        """
        if not isinstance(document, str) or not document:
            logger.error("Invalid document provided for PII extraction")
            raise ValueError("Document must be a non-empty string")

        try:
            logger.info("Starting PII extraction")
            extracted_data = self.pii_extractor.extract_pii(document)
            
            if not extracted_data or not extracted_data.private_data:
                logger.warning("No PII data extracted from the document")
                return PIIDataExtraction(private_data=[])

            pii_data = PIIDataExtraction(private_data=extracted_data.private_data)
            logger.info(f"PII extraction completed. Found {len(pii_data.private_data)} PII items")
            return pii_data

        except AttributeError as ae:
            logger.error(f"Attribute error during PII extraction: {str(ae)}")
            raise PIIExtractionError(f"Failed to access required attribute: {str(ae)}")
        except ValidationError as ve:
            logger.error(f"Validation error for extracted PII data: {str(ve)}")
            raise ValidationError(f"Extracted PII data failed validation: {str(ve)}")
        except Exception as e:
            logger.error(f"Unexpected error in extract_pii: {str(e)}")
            raise PIIExtractionError(f"Unexpected error during PII extraction: {str(e)}")
    def __enter__(self):
        """
        Enter the runtime context for DataFogInstructor.

        Postconditions:
        - Returns self for use in context manager

        Exceptions:
        - RuntimeError: If there's an error initializing resources
        """
        try:
            logger.info("Entering DataFogInstructor context")
            # Initialize any resources if needed
            return self
        except Exception as e:
            logger.error(f"Error entering DataFogInstructor context: {str(e)}")
            raise RuntimeError(f"Failed to enter DataFogInstructor context: {str(e)}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context for DataFogInstructor.

        Postconditions:
        - Performs any necessary cleanup

        Exceptions:
        - RuntimeError: If there's an error during cleanup
        """
        try:
            logger.info("Exiting DataFogInstructor context")
            # Clean up resources if needed
            if exc_type is not None:
                logger.error(f"An exception occurred: {exc_type.__name__}: {str(exc_val)}")
        except Exception as e:
            logger.error(f"Error exiting DataFogInstructor context: {str(e)}")
            raise RuntimeError(f"Failed to properly exit DataFogInstructor context: {str(e)}")

