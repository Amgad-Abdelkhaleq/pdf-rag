import pytest
from src.services.embedding_service import EmbeddingService

class TestEmbeddingService:
    @pytest.fixture
    def embedding_service(self):
        return EmbeddingService()
    
    def test_generate_embeddings(self, embedding_service):
        texts = ["Hello world", "This is a test sentence"]
        embeddings = embedding_service.generate_embeddings(texts)
        
        assert len(embeddings) == len(texts)
        assert all(len(emb) > 0 for emb in embeddings)
        assert isinstance(embeddings[0], list)