from pydantic import BaseModel, Field
from typing import Optional, List

class DocumentUploadResponse(BaseModel):
    """
    Response schema for document upload
    """
    status: str
    document_id: str
    message: Optional[str] = None

class ChatRequest(BaseModel):
    """
    Request schema for chat interaction
    """
    session_id: str
    query: str
    document_id: Optional[str] = None

class ChatResponse(BaseModel):
    """
    Response schema for chat interaction
    """
    response: str
    session_id: str
    context_chunks: Optional[List[str]] = None