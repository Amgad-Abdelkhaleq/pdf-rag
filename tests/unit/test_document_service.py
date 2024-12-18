import pytest
from src.services.document_service import DocumentService
import tempfile
import os

class TestDocumentService:
    @pytest.fixture
    def document_service(self):
        return DocumentService()
    
    def test_extract_text_from_pdf(self, document_service):
        # Create a temporary PDF for testing
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            # Here you would ideally create a real PDF, for now we'll simulate
            temp_pdf.write(b"Test PDF content")
            temp_pdf.close()
        
        try:
            text = document_service.extract_text_from_pdf(temp_pdf.name)
            assert isinstance(text, str)
            assert len(text) > 0
        finally:
            os.unlink(temp_pdf.name)
    
    def test_chunk_document(self, document_service):
        sample_text = "This is a test document. " * 100  # Repeat to create longer text
        chunks = document_service.chunk_document(sample_text)
        
        assert len(chunks) > 1
        assert all('text' in chunk for chunk in chunks)
        assert all(len(chunk['text']) > 0 for chunk in chunks)