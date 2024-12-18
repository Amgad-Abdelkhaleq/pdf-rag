from fastapi import APIRouter, File, UploadFile, Depends
from src.services.document_service import DocumentService
from src.services.embedding_service import EmbeddingService
from src.repositories.vector_store import VectorStoreRepository
import uuid
import os
from src.core.config import settings
from src.core.dependencies import get_document_service, get_vector_store, get_embedding_service

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    document_service: DocumentService = Depends(get_document_service),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    vector_store: VectorStoreRepository = Depends(get_vector_store)
):
    """
    Upload and process PDF document
    
    Args:
        file (UploadFile): Uploaded PDF file
    
    Returns:
        Dict: Upload status and document ID
    """
    # Generate unique filename
    file_id = str(uuid.uuid4())
    file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.pdf")
    
    # Save file
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Extract text
    document_text = document_service.extract_text_from_pdf(file_path)
    
    # Chunk document
    document_chunks = document_service.chunk_document(document_text)
    
    # Generate embeddings
    embeddings = embedding_service.generate_embeddings(
        [chunk['text'] for chunk in document_chunks]
    )
    
    # Add embeddings to chunks
    for chunk, embedding in zip(document_chunks, embeddings):
        chunk['embedding'] = embedding
    
    # Store in vector database
    vector_store.upsert_documents(document_chunks)
    
    return {
        "status": "success", 
        "document_id": file_id
    }