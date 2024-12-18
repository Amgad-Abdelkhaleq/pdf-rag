from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    """
    Represents a single chat message
    """
    role: str = Field(..., description="Message role (user/assistant)")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatSession(BaseModel):
    """
    Represents a complete chat session
    """
    session_id: str
    document_id: Optional[str] = None
    messages: List[ChatMessage] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        """Pydantic configuration"""
        orm_mode = True