import json
from .models import DetectedEntities, EntityType
from .utils import preprocess_response
from ollama_instructor.ollama_instructor_client import OllamaInstructorClient
from typing import Dict, Optional

class DataFog:
    def __init__(self, host: str = "http://localhost:11434", model: str = "phi3", entity_types: Optional[Dict[str, str]] = None):
        self.client = OllamaInstructorClient(host=host)
        self.model = model
        self.entity_types = entity_types or {e.name: e.value for e in EntityType}

    def detect_entities(self, text: str) -> DetectedEntities:
        response = self.client.chat_completion(
            model=self.model,
            pydantic_model=DetectedEntities,
            messages=[
                {
                    "role": "user",
                    "content": f"Identify and classify named entities in the following text: '{text}'"
                }
            ],
            format="json"
        )

        if 'message' in response and 'content' in response['message']:
            try:
                content = response['message']['content']
                if isinstance(content, dict) and 'entities' in content:
                    # The response is already in the correct format
                    return DetectedEntities.model_validate(content)
                elif isinstance(content, dict):
                    preprocessed_response = preprocess_response(content, self.entity_types)
                else:
                    preprocessed_response = preprocess_response(json.loads(content), self.entity_types)
                
                return DetectedEntities.model_validate(preprocessed_response)
            except Exception as e:
                raise ValueError(f"Error processing response: {e}. Raw response: {response['message']['content']}")
        else:
            raise ValueError(f"Unexpected response format: {response}")

    def add_entity_type(self, name: str, value: str):
        self.entity_types[name.upper()] = value

    def remove_entity_type(self, name: str):
        if name.upper() in self.entity_types:
            del self.entity_types[name.upper()]

    def get_entity_types(self) -> Dict[str, str]:
        return self.entity_types