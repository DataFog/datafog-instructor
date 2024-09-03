import json
from enum import Enum
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple, Union

import regex
from pydantic import BaseModel, ConfigDict, Field
from rellm import complete_re
from rich.console import Console
from transformers import AutoModelForCausalLM, AutoTokenizer

console = Console()


class EntityType(Enum):
    PERSON = "PERSON"
    COMPANY = "COMPANY"
    LOCATION = "LOCATION"
    ORG = "ORG"


class CustomEntity(BaseModel):
    entity_name: str = Field(..., description="The name of the entity to detect")
    regex: Optional[str] = Field(
        None, description="A regex pattern to match the entity"
    )
    entity_type: Optional[EntityType] = Field(
        None, description="The type of the entity to detect"
    )


class CustomEntities(BaseModel):
    entities: List[CustomEntity] = Field(default_factory=list)


class DetectedEntity(BaseModel):
    text: str
    start: Optional[int] = None
    end: Optional[int] = None
    entity_type: EntityType


class DetectedEntities(BaseModel):
    entities: List[DetectedEntity]


class EntityDetector:
    def __init__(self):
        self.config = {
            "model_id": "gpt2",
            "filename": "gpt2",
            "default_pattern": r"("
            + "|".join(entity.value for entity in EntityType)
            + ")",
            "model_type": "huggingface",
        }
        self.save_config()
        self.initialize()  # Call initialize in the constructor

    def initialize(self, force: bool = False):
        config_path = Path("fogprint.json")
        if config_path.exists() and not force:
            loaded_config = self.load_config()
            if loaded_config:
                self.config.update(loaded_config)
            console.print("[yellow]Configuration file loaded.[/yellow]")
        else:
            self.save_config()
            console.print("[green]Configuration file created.[/green]")

        self._load_tokenizer()
        self._load_model()
        self.compile_pattern(self.config["default_pattern"])
        console.print("[green]Initialization complete![/green]")

    def _load_tokenizer(self):
        if self.config["model_type"] == "gguf":
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config["model_id"], gguf_file=self.config["filename"]
            )
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(self.config["model_id"])

    def _load_model(self):
        if self.config["model_type"] == "gguf":
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config["model_id"], gguf_file=self.config["filename"]
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(self.config["model_id"])

    def load_config(self):
        config_path = Path("config.json")
        if config_path.exists():
            with open(config_path, "r") as f:
                return json.load(f)
        return None

    def compile_pattern(self, pattern: str):
        self.compiled_pattern = regex.compile(pattern)

    def detect_entities(self, prompt: str, max_new_tokens: int) -> List[DetectedEntity]:
        if not hasattr(self, "tokenizer") or not hasattr(self, "model"):
            self._load_tokenizer()
            self._load_model()

        generated_text = complete_re(
            tokenizer=self.tokenizer,
            model=self.model,
            prompt=prompt,
            pattern=self.compiled_pattern,
            do_sample=True,
            max_new_tokens=max_new_tokens,
        )

        full_text = prompt + generated_text
        entities = []

        for match in self.compiled_pattern.finditer(full_text):
            if match.group():
                entities.append(
                    DetectedEntity(
                        text=match.group(),
                        start=match.start(),
                        end=match.end(),
                        entity_type=EntityType(match.group()),
                    )
                )

        return entities

    def get_model_info(self) -> Dict[str, str]:
        return {
            "model_id": self.config.get("model_id", "Not set"),
            "filename": self.config.get("filename", "Not set"),
            "default_pattern": self.config.get("default_pattern", "Not set"),
            "model_type": self.config.get("model_type", "Not set"),
        }

    def save_config(self):
        config_path = Path("config.json")
        with open(config_path, "w") as f:
            json.dump(self.config, f)
        console.print("[green]Configuration saved successfully.[/green]")
