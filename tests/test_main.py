import pytest
from fastapi.testclient import TestClient
from app.main import app, PIIDataExtraction, Entity

client = TestClient(app)

@pytest.mark.asyncio
async def test_extract_pii():
    content = "John Doe's SSN is 123-45-6789 and his email is john@example.com"
    response = client.post("/extract-pii", json={"content": content})
    assert response.status_code == 200
    pii_data = PIIDataExtraction(**response.json())
    assert len(pii_data.private_data) > 0
    assert any(data.data_type == "SSN" for data in pii_data.private_data)
    assert any(data.data_type == "EMAIL" for data in pii_data.private_data)

@pytest.mark.asyncio
async def test_extract_pii_stream():
    content = "Jane Doe's phone number is (555) 123-4567"
    response = client.post("/extract-pii-stream", json={"content": content})
    assert response.status_code == 200
    # Note: Streaming response testing might require additional setup

