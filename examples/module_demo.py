import os
os.environ['DATAFOG_LLM_ENDPOINT'] = 'http://localhost:11434'
os.environ['DATAFOG_LLM_MODEL'] = 'phi3'

from datafog_instructor import DataFog

# Initialize DataFog with defaults
datafog = DataFog()

# Or with custom settings
# datafog = DataFog(host="http://custom-host:11434", model="custom-model", entity_types={"CUSTOM_TYPE": "Custom Entity"})

# Detect entities in text
text = "Cisco acquires Hess for $20 billion"
result = datafog.detect_entities(text)

# Print results
for entity in result.entities:
    print(f"Text: {entity.text}, Type: {entity.type}")

# Add a new entity type
datafog.add_entity_type("CUSTOM", "Custom Entity")

# Remove an entity type
datafog.remove_entity_type("CUSTOM")