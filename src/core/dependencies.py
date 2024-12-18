from fastapi import Depends
from src.services.document_service import DocumentService
from src.services.embedding_service import EmbeddingService
from src.services.rag_service import RAGService
from src.services.chat_history_service import ChatHistoryService
from src.repositories.vector_store import VectorStoreRepository

# Singleton instances for dependencies
vector_store = VectorStoreRepository()
embedding_service = EmbeddingService()
chat_history_service = ChatHistoryService()

def get_document_service():
    """Dependency for DocumentService"""
    return DocumentService()

def get_embedding_service():
    """Dependency for EmbeddingService"""
    return embedding_service

def get_vector_store():
    """Dependency for VectorStoreRepository"""
    return vector_store

def get_chat_history_service():
    """Dependency for ChatHistoryService"""
    return chat_history_service

def get_rag_service():
    """Dependency for RAGService"""
    return RAGService(
        embedding_service=embedding_service,
        vector_store=vector_store,
        chat_history_service=chat_history_service
    )