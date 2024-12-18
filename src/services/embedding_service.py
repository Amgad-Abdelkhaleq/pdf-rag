# src/services/embedding_service.py
from sentence_transformers import SentenceTransformer
from src.core.config import settings
import torch
from typing import List

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for given texts
        
        Args:
            texts (List[str]): List of text chunks
        
        Returns:
            List[List[float]]: List of embedding vectors
        """
        embeddings = self.model.encode(
            texts, 
            convert_to_tensor=False,
            device=self.device
        )
        return embeddings.tolist()