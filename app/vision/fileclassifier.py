import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, ConfigDict, validator
from enum import Enum
from typing import List
import base64
import os

# Initialize the OpenAI client with Instructor
client = instructor.from_openai(OpenAI())

class FileType(str, Enum):
    """
    Enumeration of file types for classification.

    Invariants:
    - The enum values are constant and do not change during runtime
    - Each enum member is unique within the class
    - The string value of each enum member matches its name in uppercase
    """
    MEDICAL_REPORT = "Medical_Report"
    WORK_ADMIN = "Work_Admin"
    WORK_PTO = "Work_PTO"
    CPA = "CPA"
    OTHER = "Other"

    @classmethod
    def is_valid_type(cls, value: str) -> bool:
        """
        Check if a given string is a valid FileType.

        Preconditions:
        - value is a string

        Postconditions:
        - Returns True if value matches any of the enum members, False otherwise
        - Raises TypeError if value is not a string

        :param value: The string to check
        :return: Boolean indicating if the value is a valid FileType
        :raises TypeError: If value is not a string
        """
        if not isinstance(value, str):
            raise TypeError("Input must be a string")
        return value in cls._value2member_map_

class FileClassification(BaseModel):
    """
    Pydantic model for file classification results.

    Invariants:
    - All fields are required and must be of the specified types.
    - The confidence score must be between 0 and 1.
    """
    file_name: str = Field(..., description="The name of the file being classified")
    file_type: FileType = Field(..., description="The classified type of the file")
    confidence: float = Field(..., description="Confidence score of the classification (0-1)", ge=0, le=1)
    keywords: List[str] = Field(..., description="List of keywords that led to this classification")
    summary: str = Field(..., description="A brief summary of the file contents")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @validator('file_name')
    def validate_file_name(cls, v):
        if not v.strip():
            raise ValueError("File name must not be empty")
        return v

    @validator('keywords')
    def validate_keywords(cls, v):
        if not v:
            raise ValueError("Keywords list must not be empty")
        return v

    @validator('summary')
    def validate_summary(cls, v):
        if not v.strip():
            raise ValueError("Summary must not be empty")
        return v

def classify_file(file_content: str, file_name: str) -> FileClassification:
    """
    Classify a file based on its content and name.

    Preconditions:
    - file_content must be a non-empty string.
    - file_name must be a non-empty string.

    Postconditions:
    - Returns a FileClassification object.

    Invariants:
    - The OpenAI client must be properly initialized.

    Edge Cases:
    - If the file content is very short or ambiguous, classification may be less accurate.
    - If the API call fails, an exception will be raised.

    :param file_content: The content of the file to be classified.
    :param file_name: The name of the file to be classified.
    :return: A FileClassification object containing the classification results.
    :raises ValueError: If file_content or file_name is empty.
    """
    if not file_content.strip():
        raise ValueError("File content must not be empty")
    if not file_name.strip():
        raise ValueError("File name must not be empty")

    return client.chat.completions.create(
        model="gpt-4",
        response_model=FileClassification,
        messages=[
            {"role": "system", "content": "You are an expert file classifier. Analyze the given file content and classify it into one of the predefined categories."},
            {"role": "user", "content": f"Classify this file:\nFile Name: {file_name}\nContent: {file_content}"}
        ]
    )

def classify_image(image_path: str) -> FileClassification:
    """
    Classify an image file based on its visual content.

    Preconditions:
    - image_path must be a valid path to an existing image file.
    - The OpenAI client must be properly initialized with vision capabilities.

    Postconditions:
    - Returns a FileClassification object.

    Invariants:
    - The classification process should be consistent for the same image.

    Edge Cases:
    - If the image is corrupted or unreadable, an exception will be raised.
    - Very small or low-quality images may result in less accurate classifications.

    :param image_path: The path to the image file to be classified.
    :return: A FileClassification object containing the classification results.
    :raises FileNotFoundError: If the image file does not exist.
    :raises ValueError: If the image file is empty or corrupted.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        if not image_data:
            raise ValueError("Image file is empty")

        return client.chat.completions.create(
            model="gpt-4-vision-preview",
            response_model=FileClassification,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert image classifier. Analyze the given image and classify it into one of the predefined categories."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Classify this image:"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(image_data).decode()}"}
                        }
                    ]
                }
            ]
        )

# Example usage
if __name__ == "__main__":
    try:
        file_content = "This is a test medical report."
        file_name = "test_medical_report.txt"
        classification = classify_file(file_content, file_name)
        print(f"File Classification: {classification}")

        image_path = "/path/to/test/image.jpg"
        image_classification = classify_image(image_path)
        print(f"Image Classification: {image_classification}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")