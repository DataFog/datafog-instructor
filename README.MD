# DataFog Instructor SDK

DataFog Instructor is a Python SDK for named entity recognition (NER) using the Ollama Instructor client. It provides an easy-to-use interface for detecting and classifying entities in text.

## Installation

To install the DataFog Instructor SDK, you can use pip:

```
pip install datafog-instructor
```

## Quick Start

Here's a simple example to get you started with DataFog Instructor:

```python
from datafog_instructor import DataFog

# Initialize DataFog with default settings
datafog = DataFog()

# Detect entities in text
text = "Cisco acquires Hess for $20 billion"
result = datafog.detect_entities(text)

# Print results
for entity in result.entities:
    print(f"Text: {entity.text}, Type: {entity.type}")
```

## Configuration

You can customize the DataFog instance with the following parameters:

- `host`: The host URL for the Ollama service (default: "http://localhost:11434")
- `model`: The model to use for entity detection (default: "phi3")
- `entity_types`: A dictionary of custom entity types (optional)

Example with custom settings:

```python
datafog = DataFog(
    host="http://custom-host:11434",
    model="custom-model",
    entity_types={"CUSTOM_TYPE": "Custom Entity"}
)
```

## Features

### Detect Entities

Use the `detect_entities` method to identify and classify named entities in a given text:

```python
text = "Apple Inc. reported $100 billion in revenue for Q4 2023"
result = datafog.detect_entities(text)

for entity in result.entities:
    print(f"Text: {entity.text}, Type: {entity.type}")
```

### Manage Entity Types

You can add or remove entity types dynamically:

```python
# Add a new entity type
datafog.add_entity_type("CUSTOM", "Custom Entity")

# Remove an entity type
datafog.remove_entity_type("CUSTOM")

# Get all entity types
entity_types = datafog.get_entity_types()
print(entity_types)
```

## Default Entity Types

The SDK comes with predefined entity types, including:

- ORG (Organization)
- PERSON
- TRANSACTION_TYPE
- DEAL_STRUCTURE
- FINANCIAL_INFO
- PRODUCT
- LOCATION
- DATE
- INDUSTRY
- ROLE
- REGULATORY
- SENSITIVE_INFO
- CONTACT
- ID (Identifier)
- STRATEGY
- COMPANY
- MONEY

## Error Handling

The SDK includes basic error handling. If there's an issue with processing the response or an unexpected response format, it will raise a `ValueError` with details about the error.

## Contributing

Contributions to the DataFog Instructor SDK are welcome! Please feel free to submit a Pull Request.

## License

MIT 

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository.