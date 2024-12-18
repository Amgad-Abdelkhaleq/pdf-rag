from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from src.core.config import settings
from typing import List,Dict
import uuid

class VectorStoreRepository:
    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST, 
            port=settings.QDRANT_PORT
        )
        self.collection_name = "pdf_documents"
        # if self.client.get_collection(collection_name= self.collection_name):
        #     print(f"Collection `{ self.collection_name }` already exists.")
        # else:
        #     self.client.create_collection(
        #         collection_name=self.collection_name,
        #         vectors_config=VectorParams(
        #             size= 384, 
        #             distance=Distance.COSINE
        #         )
        #     )
    
    def upsert_documents(self, documents: List[Dict]):
        """
        Insert or update documents in vector store
        
        Args:
            documents (List[Dict]): Documents with text and embeddings
        """
        points = [
            {
                "id": str(uuid.uuid4()),  # "id": hash(doc['text']),
                "vector": doc['embedding'],
                "payload": {"text": doc['text']}
            } for doc in documents
        ]
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
    
    def search(self, query_embedding: List[float], top_k: int = 5):
        """
        Search similar documents
        
        Args:
            query_embedding (List[float]): Query vector
            top_k (int): Number of results
        
        Returns:
            List[Dict]: Matching documents
        """
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k
        )
        
        return [
            {"text": hit.payload["text"], "score": hit.score} 
            for hit in search_result
        ]