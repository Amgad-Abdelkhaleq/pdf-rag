from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "PDF Chatbot"
    
    # Model Configuration
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    LLM_MODEL: str =  "TinyLlama/TinyLlama-1.1B-Chat-v1.0" #"microsoft/phi-1_5" #"mistralai/Mistral-7B-Instruct-v0.2"
    
    # Vector Store
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    
    # Chunk Size for Document Processing
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()