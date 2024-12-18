import pytest
from fastapi.testclient import TestClient
from main import create_app
import tempfile

@pytest.fixture
def client():
    return TestClient(create_app())

def test_document_upload(client):
    # Create a temporary PDF
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
        temp_pdf.write(b"Test PDF content")
        temp_pdf.close()
    
    with open(temp_pdf.name, 'rb') as f:
        response = client.post(
            "/documents/upload",
            files={"file": f}
        )
    
    assert response.status_code == 200
    assert "document_id" in response.json()