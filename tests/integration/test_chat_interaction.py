import pytest
from fastapi.testclient import TestClient
from main import create_app
import uuid

@pytest.fixture
def client():
    return TestClient(create_app())

def test_chat_interaction(client):
    # First, upload a document
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
        temp_pdf.write(b"Test PDF content about machine learning")
        temp_pdf.close()
    
    with open(temp_pdf.name, 'rb') as f:
        upload_response = client.post(
            "/documents/upload",
            files={"file": f}
        )
    
    document_id = upload_response.json()["document_id"]
    
    # Now perform chat
    chat_response = client.post(
        "/chat/chat",
        json={
            "session_id": str(uuid.uuid4()),
            "query": "What is this document about?",
            "document_id": document_id
        }
    )
    
    assert chat_response.status_code == 200
    assert "response" in chat_response.json()
    assert len(chat_response.json()["response"]) > 0