import json
from pathlib import Path

import pytest
import regex

from app.models import DetectedEntity, EntityDetector, EntityType


@pytest.fixture
def entity_detector():
    return EntityDetector()


def test_entity_detector_init(entity_detector):
    assert entity_detector.config["model_id"] == "gpt2"
    assert entity_detector.config["filename"] == "gpt2"
    assert isinstance(entity_detector.compiled_pattern, type(regex.compile("")))


# def test_load_config(entity_detector, tmp_path):
#     config = {"model_id": "test_model", "filename": "test_file"}
#     config_path = tmp_path / "config.json"
#     with open(config_path, "w") as f:
#         json.dump(config, f)

#     loaded_config = entity_detector.load_config()
#     assert loaded_config == config


def test_compile_pattern(entity_detector):
    entity_detector.compile_pattern(r"(TEST)")
    assert entity_detector.compiled_pattern.pattern == r"(TEST)"


# def test_detect_entities(entity_detector, mocker):
#     mocker.patch("app.models.complete_re", return_value=" PERSON is from LOCATION")
#     entities = entity_detector.detect_entities("John", 10)
#     assert len(entities) == 2
#     assert entities[0].text == "PERSON"
#     assert entities[1].text == "LOCATION"


def test_get_model_info(entity_detector):
    info = entity_detector.get_model_info()
    assert "model_id" in info
    assert "filename" in info
    assert "default_pattern" in info
    assert "model_type" in info


def test_save_config(entity_detector, tmp_path):
    entity_detector.config["test_key"] = "test_value"
    entity_detector.save_config()
    assert Path("config.json").exists()
    with open("config.json", "r") as f:
        saved_config = json.load(f)
    assert saved_config["test_key"] == "test_value"


def test_entity_type_enum():
    assert EntityType.PERSON.value == "PERSON"
    assert EntityType.COMPANY.value == "COMPANY"
    assert EntityType.LOCATION.value == "LOCATION"
    assert EntityType.ORG.value == "ORG"


def test_detected_entity():
    entity = DetectedEntity(text="John", start=0, end=4, entity_type=EntityType.PERSON)
    assert entity.text == "John"
    assert entity.start == 0
    assert entity.end == 4
    assert entity.entity_type == EntityType.PERSON
