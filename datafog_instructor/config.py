import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self.llm_backend = os.getenv("DATAFOG_LLM_BACKEND", "ollama")
        self.llm_endpoint = os.getenv("DATAFOG_LLM_ENDPOINT", "http://localhost:11434")
        self.llm_model = os.getenv("DATAFOG_LLM_MODEL", "phi3")

config = Config()

