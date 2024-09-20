from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Request
from openai import AsyncOpenAI
import instructor
import logfire
import asyncio
from collections.abc import Iterable
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import os
from typing import List, Dict
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Field
from typing import Optional
import pandas as pd
from sqlmodel import SQLModel, Field
from typing import Tuple
import traceback

class DetectedPII(BaseModel):
    """
    Detected PII data from a document
    """
    index: int
    data_type: str
    pii_value: str


class PIIDetectionFlow(BaseModel):
    """
    Extracted PII data from a document, all data_types should try to have consistent property names
    """

    detected_pii: list[DetectedPII] = Field(..., min_items=1)

    def __init__(self, **data):
        super().__init__(**data)
        self._validate_detected_pii()

    def _validate_detected_pii(self):
        """
        Validates the detected_pii list to ensure it meets the required conditions.

        Preconditions:
            - detected_pii is a non-empty list

        Postconditions:
            - All items in detected_pii are of type DetectedPII
            - All DetectedPII objects have unique indices

        Raises:
            ValueError: If any of the conditions are not met
        """
        if not self.detected_pii:
            raise ValueError("detected_pii list must not be empty")

        indices = set()
        for item in self.detected_pii:
            if not isinstance(item, DetectedPII):
                raise ValueError(f"All items in detected_pii must be of type DetectedPII. Found: {type(item)}")
            if item.index in indices:
                raise ValueError(f"Duplicate index found in detected_pii: {item.index}")
            indices.add(item.index)

        logfire.info("PIIDetectionFlow initialized", 
                     pii_count=len(self.detected_pii), 
                     unique_indices=len(indices))

    def __len__(self):
        return len(self.detected_pii)

    def __iter__(self):
        return iter(self.detected_pii)

    def __getitem__(self, index):
        return self.detected_pii[index]

    def redact_pii(self, content):
        """
        Iterates over the private data and replaces the value with a placeholder in the form of
        <{data_type}_{i}>

        Preconditions:
            - self.detected_pii is a non-empty list of DetectedPII objects
            - content is a non-empty string

        Postconditions:
            - Returns a string with all PII values replaced by placeholders
            - The number of replacements made is equal to the length of self.detected_pii
            - The returned string is not empty

        Invariants:
            - The structure of the content string is preserved, only PII values are replaced
        """

        # Preconditions
        assert self.detected_pii, "detected_pii list must not be empty"
        assert content, "content must not be empty"

        original_content = content
        replacement_count = 0

        for i, data in enumerate(self.detected_pii):
            new_content = content.replace(data.pii_value, f"<{data.data_type}_{i}>")
            if new_content != content:
                replacement_count += 1
            content = new_content
            logfire.info(f"Replaced PII: {data.data_type}", index=i, data_type=data.data_type)

        # Postconditions
        assert replacement_count == len(self.detected_pii), "Number of replacements should match detected PII count"
        assert content, "Redacted content must not be empty"
        assert len(content) >= len(original_content), "Redacted content should not be shorter than original"

        logfire.info("PII redaction completed", 
                     original_length=len(original_content), 
                     redacted_length=len(content), 
                     replacements_made=replacement_count)

        return content

app = FastAPI()

# ----------------------- Middleware Configuration -----------------------
# Configure logfire before adding any middleware to ensure they are set up correctly
logfire.configure(pydantic_plugin=logfire.PydanticPlugin(record="all"))

# Instrument FastAPI with logfire middleware
logfire.instrument_fastapi(app)
# ----------------------- End Middleware Configuration --------------------

# Global variables to be initialized on startup
openai_client: Optional[AsyncOpenAI] = None
client: Optional[instructor.from_openai] = None

@app.on_event("startup")
async def initialize_app():
    """
    Startup event to initialize and validate environment variables and clients.
    
    Preconditions:
        - Environment variables like OPENAI_API_KEY must be set.
    
    Postconditions:
        - openai_client is initialized and ready to use.
    """
    load_dotenv()
    global OPENAI_API_KEY, openai_client, client
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    if not OPENAI_API_KEY:
        logfire.error("OPENAI_API_KEY is not set in the environment")
        raise EnvironmentError("OPENAI_API_KEY must be set in the environment variables")
    
    openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    
    assert isinstance(app, FastAPI), "app must be an instance of FastAPI"
    assert isinstance(openai_client, AsyncOpenAI), "openai_client must be an instance of AsyncOpenAI"
    
    logfire.info("Application initialized",
                 api_key_set=bool(OPENAI_API_KEY),
                 app_type=type(app).__name__,
                 client_type=type(openai_client).__name__)
    
    logfire.instrument_openai(openai_client)
    client = instructor.from_openai(openai_client)

@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event to perform cleanup tasks.
    """
    if openai_client:
        await openai_client.aclose()
    logfire.info("Application shutdown complete.")

@app.post("/extract-pii")
async def extract_pii(request: Request) -> PIIDetectionFlow:
    """
    Extracts PII data from a document

    Preconditions:
        - content is a non-empty string in the request body
    
    Postconditions:
        - Returns a PIIDetectionFlow object
        - The returned object contains a non-empty list of DetectedPII objects in its detected_pii attribute

    Invariants:
        - The original content is not modified
        - The API call to OpenAI is made with the correct model and response_model
    """
    # Preconditions
    body = await request.json()
    assert isinstance(body, dict), "Request body must be a valid JSON object"
    
    content = body.get("content")
    
    # Invariant: content should not be modified after extraction
    original_content = content
    
    if not content or not isinstance(content, str) or content.strip() == "":
        logfire.error("Invalid or missing content in request", body=body)
        raise HTTPException(status_code=422, detail="Content is required and must be a non-empty string")
    
    # Postconditions
    assert content == original_content, "Content should not be modified during extraction"
    assert isinstance(content, str) and content.strip() != "", "Content must be a non-empty string"
    
    logfire.info("Content extracted from request", content_length=len(content))

    # Preconditions
    assert isinstance(content, str) and content.strip(), "Content must be a non-empty string"
    assert OPENAI_API_KEY, "OPENAI_API_KEY must be set"

    try:
        logfire.info("Initiating PII extraction", content_length=len(content))
        
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": content}],
            response_model=PIIDetectionFlow,
        )
        
        # Postconditions
        assert isinstance(response, PIIDetectionFlow), "Response must be a PIIDetectionFlow object"
        assert response.detected_pii, "Extracted PII data must not be empty"
        
        logfire.info("Successfully extracted PII data", 
                     pii_count=len(response.detected_pii),
                     pii_types=[pii.data_type for pii in response.detected_pii])
        
        # Invariant
        assert content == original_content, "Original content must not be modified during extraction"
        
        return response
    except ValueError as ve:
        logfire.warning("No PII data extracted", error=str(ve))
        raise HTTPException(status_code=204, detail="No PII data found in the content")
    except AssertionError as ae:
        logfire.error("Assertion failed during PII extraction", error=str(ae))
        raise HTTPException(status_code=500, detail=str(ae))
    except Exception as e:
        logfire.error("Unexpected error during PII extraction", 
                      error=str(e), 
                      error_type=type(e).__name__,
                      traceback=traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to extract PII data")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)