import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .models import CustomEntities, CustomEntity, EntityDetector, EntityType

app = typer.Typer()
console = Console()


@app.command()
def init(
    force: bool = typer.Option(False, "--force", "-f", help="Force reinitialization")
):
    """Initialize/reinitialize datafog-instructor with a new fogprint file."""
    if force:
        console.print(
            "[yellow]Warning: Forcing reinitialization. This will overwrite existing configuration.[/yellow]"
        )
        typer.confirm("Are you sure you want to continue?", abort=True)

    entity_detector = EntityDetector()
    try:
        entity_detector.initialize(force=force)
        console.print("[green]Initialization complete![/green]")
    except Exception as e:
        console.print(f"[red]Error during initialization: {str(e)}[/red]")
        console.print(
            "[yellow]Ensure the model file 'gpt2' exists in the current directory.[/yellow]"
        )
    # Display model info in a table
    model_info = entity_detector.get_model_info()
    table = Table(title="Model Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="magenta")

    for key, value in model_info.items():
        table.add_row(key, value)

    console.print(table)


@app.command()
def detect_entities(
    prompt: str = typer.Option(
        ..., "--prompt", "-p", help="Text to detect entities in"
    ),
    max_new_tokens: int = typer.Option(
        50, "--max-new-tokens", "-m", help="Maximum number of new tokens to generate"
    ),
):
    """Classify entities in the given text."""
    entity_detector = EntityDetector()
    entities = entity_detector.detect_entities(prompt, max_new_tokens)
    table = Table(title="Detected Entities")
    table.add_column("Text", style="cyan")
    table.add_column("Start", style="magenta")
    table.add_column("End", style="magenta")
    table.add_column("Entity Type", style="green")

    for entity in entities:
        table.add_row(
            entity.text,
            str(entity.start),
            str(entity.end),
            entity.entity_type.value,  # Convert EntityType to string
        )

    console.print(table)


@app.command()
def list_entities():
    """List all entities in the fogprint."""
    fogprint_path = Path("datafog_config.json")
    if not fogprint_path.exists():
        console.print("[red]Fogprint not found. Use 'init' to create one.[/red]")
        return

    with open(fogprint_path, "r") as f:
        fogprint = json.load(f)

    default_pattern = fogprint.get("default_pattern", "")
    entities = default_pattern.strip("()").split("|")

    table = Table(title="Entities")
    table.add_column("Entity Type", style="cyan")

    for entity in entities:
        if entity in EntityType.__members__:
            table.add_row(entity)

    console.print(table)


@app.command()
def show_fogprint():
    """Display the current fogprint configuration."""
    fogprint_path = Path("datafog_config.json")
    if not fogprint_path.exists():
        console.print("[red]Fogprint not found. Use 'init' to create one.[/red]")
        return

    with open(fogprint_path, "r") as f:
        fogprint_content = f.read()

    console.print(fogprint_content)


if __name__ == "__main__":
    app()
