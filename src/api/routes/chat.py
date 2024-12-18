from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.services.rag_service import RAGService
from src.services.chat_history_service import ChatHistoryService
from src.core.dependencies import get_rag_service, get_chat_history_service

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    query: str

@router.post("/chat")
async def chat_endpoint(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service),
    chat_history_service: ChatHistoryService = Depends(get_chat_history_service)
):
    """
    Process chat query and generate response
    
    Args:
        request (ChatRequest): Chat request with session ID and query
    
    Returns:
        Dict: Generated response and updated chat history
    """
    # Retrieve chat history
    chat_history = chat_history_service.get_history(request.session_id)
    
    # Add user message to history
    chat_history_service.add_message(
        request.session_id, 
        role="user", 
        content=request.query
    )
    
    # Generate response using RAG
    response = rag_service.generate_response(
        request.query, 
        chat_history
    )
    
    # Add assistant message to history
    chat_history_service.add_message(
        request.session_id, 
        role="assistant", 
        content=response
    )
    
    return {
        "response": response,
        "session_id": request.session_id
    }