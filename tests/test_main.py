import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from app.main import app

runner = CliRunner()


def test_init():
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "Initialization complete!" in result.stdout
    assert Path("fogprint.json").exists()


def test_init_force():
    result = runner.invoke(app, ["init", "--force"], input="y\n")
    assert result.exit_code == 0
    assert "Forcing reinitialization" in result.stdout


def test_detect_entities():
    result = runner.invoke(
        app, ["detect-entities", "--prompt", "John lives in New York"]
    )
    assert result.exit_code == 0


# def test_list_entities():
#     result = runner.invoke(app, ["list-entities"])
#     assert result.exit_code == 0
#     assert "Entities" in result.stdout


def test_show_fogprint():
    result = runner.invoke(app, ["show-fogprint"])
    assert result.exit_code == 0
    assert "default_pattern" in result.stdout


@pytest.fixture
def mock_fogprint(tmp_path):
    fogprint = {
        "default_pattern": "(PERSON|LOCATION|ORGANIZATION)",
        "custom_entities": [],
    }
    fogprint_path = tmp_path / "fogprint.json"
    fogprint_path.write_text(json.dumps(fogprint))
    return fogprint_path


# def test_list_entities_with_mock(mock_fogprint, monkeypatch):
#     monkeypatch.chdir(mock_fogprint.parent)
#     result = runner.invoke(app, ["list-entities"])
#     assert result.exit_code == 0
#     assert "PERSON" in result.stdout
#     assert "LOCATION" in result.stdout
#     assert "ORGANIZATION" in result.stdout


def test_show_fogprint_with_mock(mock_fogprint, monkeypatch):
    monkeypatch.chdir(mock_fogprint.parent)
    result = runner.invoke(app, ["show-fogprint"])
    assert result.exit_code == 0
    assert "default_pattern" in result.stdout
    assert "custom_entities" in result.stdout
