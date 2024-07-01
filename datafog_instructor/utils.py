from typing import Dict, List

def preprocess_response(response: Dict, entity_types: Dict[str, str]) -> Dict:
    if 'entities' in response and isinstance(response['entities'], list):
        # The response is already in the correct format
        return response

    processed_entities = []
    for entity_name, entity_data in response.items():
        if isinstance(entity_data, dict):
            entity_type = entity_data.get('entity_type', '').upper().replace(' ', '_')
            if entity_type not in entity_types:
                entity_type = 'ORG'  # Default to ORG if type is not recognized
            processed_entities.append({
                'text': entity_data.get('text', entity_name),
                'start': entity_data.get('start'),
                'end': entity_data.get('end'),
                'type': entity_type
            })
    return {'entities': processed_entities}