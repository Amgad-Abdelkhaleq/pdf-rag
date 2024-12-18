# src/models/document.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DocumentChunk(BaseModel):
    """
    Represents a chunk of a document
    """
    text: str
    embedding: Optional[List[float]] = None
    page_number: Optional[int] = None
    
class Document(BaseModel):
    """
    Represents a processed document
    """
    id: str
    filename: str
    total_pages: int
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    chunks: List[DocumentChunk]
    
    class Config:
        """Pydantic configuration"""
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }